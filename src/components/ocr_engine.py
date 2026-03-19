import easyocr
import cv2
import re
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from src.utils.text_processing import clean_ocr_text, extract_tokens, correct_spelling, rebuild_text


class OCREngine:

    def __init__(self):

        try:
            logging.info("Initializing OCR Engine")
            self.reader = easyocr.Reader(['en'])

            # Load ingredient database for correction
            df = pd.read_csv("datasets/final/ingredients_db.csv")

            self.ingredients = (
                df["ingredient"]
                .dropna()
                .astype(str)
                .str.lower()
                .tolist()
            )

        except Exception as e:
            raise CustomException(e, sys)

    def preprocess_image(self, image_path):

        try:
            img = cv2.imread(image_path)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

            blur = cv2.GaussianBlur(gray, (5, 5), 0)

            _, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)

            return thresh

        except Exception as e:
            raise CustomException(e, sys)

    def extract_text(self, image_path):

        try:
            logging.info("Running OCR")

            processed_img = self.preprocess_image(image_path)

            result = self.reader.readtext(processed_img)

            raw_text = " ".join([res[1] for res in result])

            # Step 1: Clean text
            clean_text = clean_ocr_text(raw_text)

            # Step 2: Tokenize
            tokens = extract_tokens(clean_text)

            # Step 3: Correct spelling using NLP
            corrected_tokens = correct_spelling(tokens, self.ingredients)

            # Step 4: Rebuild corrected text
            final_text = rebuild_text(corrected_tokens)

            return final_text

        except Exception as e:
            raise CustomException(e, sys)