import pandas as pd
import sys
from src.logger import logging
from src.exception import CustomException

class HealthAnalyzer:

    def __init__(self):

        self.db = pd.read_csv("datasets/final/ingredients_db.csv")


    def analyze(self, ingredient_list):

        results = []

        for ing in ingredient_list:

            row = self.db[self.db["ingredient"] == ing]

            if row.empty:
                continue

            risk = row["risk_level"].values[0]
            effect = row["health_effect"].values[0]

            # Ignore ingredients with unknown risk
            if risk == "unknown":
                continue

            results.append({
                "ingredient": ing,
                "risk": risk,
                "effect": effect
            })

        return results