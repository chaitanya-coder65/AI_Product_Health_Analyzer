import pandas as pd
import sys
import re

from src.logger import logging
from src.exception import CustomException


class IngredientDetector:

    def __init__(self):

        try:
            df = pd.read_csv("datasets/final/advanced_ingredients_db.csv")

            # ✅ clean ingredient list
            self.known_ingredients = list(
                set(df["ingredient"].dropna().str.lower().str.strip())
            )

        except Exception as e:
            raise CustomException(e, sys)

    def clean_text(self, text):

        text = text.lower()

        # remove special chars
        text = re.sub(r'[^a-z\s]', ' ', text)

        # remove extra spaces
        text = re.sub(r'\s+', ' ', text)

        return text

    def detect(self, text):

        try:
            text = self.clean_text(text)

            detected = set()

            for ingredient in self.known_ingredients:

                # exact word match (IMPORTANT FIX)
                pattern = r'\b' + re.escape(ingredient) + r'\b'

                if re.search(pattern, text):
                    detected.add(ingredient)

            return list(detected)

        except Exception as e:
            raise CustomException(e, sys)