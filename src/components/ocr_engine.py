import easyocr
import sys
import re
from src.logger import logging
from src.exception import CustomException


class OCREngine:

    def __init__(self):

        try:

            logging.info("Initializing OCR Engine")

            self.reader = easyocr.Reader(['en'])

        except Exception as e:
            raise CustomException(e, sys)


    def extract_text(self, image_path):

        try:

            logging.info("Running OCR detection")

            result = self.reader.readtext(image_path)

            detected_text = []

            for detection in result:
                text = detection[1]
                detected_text.append(text)

            final_text = " ".join(detected_text)

            # Clean OCR text
            final_text = final_text.lower()

            final_text = re.sub(r"[^a-zA-Z ]", " ", final_text)

            return final_text

        except Exception as e:
            raise CustomException(e, sys)