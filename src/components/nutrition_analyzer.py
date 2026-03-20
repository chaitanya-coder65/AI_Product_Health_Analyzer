import pandas as pd
import sys

from src.logger import logging
from src.exception import CustomException


class NutritionAnalyzer:

    def __init__(self):

        try:
            self.df = pd.read_csv("datasets/final/advanced_ingredients_db.csv")

        except Exception as e:
            raise CustomException(e, sys)

    def analyze(self, ingredients):

        try:
            results = []
            score = 10

            for ing in ingredients:

                row = self.df[self.df["ingredient"] == ing]

                if row.empty:
                    continue

                row = row.iloc[0]

                risk = row["risk_level"]
                effect = row["health_effect"]
                threshold = row["high_risk_threshold"]

                # dummy value (until OCR quantity extraction)
                value = threshold

                # scoring logic
                if risk == "high":
                    score -= 3
                elif risk == "medium":
                    score -= 2
                elif risk == "low":
                    score -= 0

                results.append({
                    "ingredient": ing,
                    "risk": risk,
                    "effect": effect,
                    "value": value,
                    "threshold": threshold
                })

            # clamp score
            score = max(score, 0)

            # decision
            if score >= 7:
                decision = "SAFE"
            elif score >= 4:
                decision = "MODERATE"
            else:
                decision = "DANGEROUS"

            return results, score, decision

        except Exception as e:
            raise CustomException(e, sys)