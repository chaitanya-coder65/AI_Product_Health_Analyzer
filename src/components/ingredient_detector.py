import pandas as pd
import sys
import re
from src.logger import logging
from src.exception import CustomException


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

            text = text.lower()

            import re
            words = re.findall(r'\b[a-zA-Z]+\b', text)

            detected = []

            for ingredient in self.ingredients:

                ingredient = str(ingredient).lower().strip()

                # ignore small words
                if len(ingredient) < 4:
                    continue

                # only detect if word exists in OCR words
                if ingredient in words:
                    detected.append(ingredient)

            detected = list(set(detected))

            return detected

        except Exception as e:
            raise CustomException(e, sys)