import pandas as pd
import sys
from src.logger import logging
from src.exception import CustomException


class HealthAnalyzer:

    def __init__(self):

        try:
            logging.info("Loading advanced ingredient database")

            self.db = pd.read_csv("datasets/final/advanced_ingredients_db.csv")

        except Exception as e:
            raise CustomException(e, sys)

    def analyze(self, ingredients):

        try:
            results = []
            score = 10

            for ing in ingredients:

                row = self.db[self.db["ingredient"] == ing]

                if row.empty:
                    continue

                risk = row["risk_level"].values[0]
                effect = row["health_effect"].values[0]

                # 🎯 Rule-Based Risk Evaluation
                if risk == "high":
                    score -= 4
                elif risk == "medium":
                    score -= 2
                elif risk == "low":
                    score -= 1

                results.append({
                    "ingredient": ing,
                    "risk": risk,
                    "effect": effect
                })

            # 🎯 Final Decision Rule
            if score >= 7:
                decision = "SAFE"
            elif score >= 4:
                decision = "MODERATE"
            else:
                decision = "DANGEROUS"

            return results, score, decision

        except Exception as e:
            raise CustomException(e, sys)