import pandas as pd
import sys
from rapidfuzz import process
from src.logger import logging
from src.exception import CustomException
from src.utils.text_processing import clean_ocr_text, extract_tokens


class IngredientDetector:

    def __init__(self):

        try:

            logging.info("Loading ingredient database")

            df = pd.read_csv("datasets/final/ingredients_db.csv")

            df = df.dropna(subset=["ingredient"])

            self.ingredients = (
                df["ingredient"]
                .astype(str)
                .str.lower()
                .str.strip()
                .unique()
                .tolist()
            )

        except Exception as e:
            raise CustomException(e, sys)


    def detect(self, text):

        try:

            clean_text = clean_ocr_text(text)

            tokens = extract_tokens(clean_text)

            detected = []

            for token in tokens:

                # NLP fuzzy matching
                match, score, _ = process.extractOne(token, self.ingredients)

                # threshold (important)
                if score >= 85:
                    detected.append(match)

            detected = list(set(detected))

            return detected

        except Exception as e:
            raise CustomException(e, sys)