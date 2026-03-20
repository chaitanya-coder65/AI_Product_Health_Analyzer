import pandas as pd
import random
import sys
from src.logger import logging
from src.exception import CustomException


class TrainingDataGenerator:

    def __init__(self):
        self.db_path = "datasets/final/advanced_ingredients_db.csv"
        self.output_path = "datasets/training_data.csv"

    def generate(self, n_samples=1500):
        try:
            df = pd.read_csv(self.db_path)

            ingredients = df["ingredient"].dropna().tolist()
            risk_map = dict(zip(df["ingredient"], df["risk_level"]))

            data = []

            # 🔥 FORCE BALANCED CLASSES
            for label in ["low", "medium", "high"]:

                for _ in range(n_samples // 3):

                    selected = random.sample(ingredients, random.randint(2, 6))

                    score = 0

                    for ing in selected:
                        risk = risk_map.get(ing, "low")

                        if risk == "high":
                            score += 3
                        elif risk == "medium":
                            score += 2
                        else:
                            score += 1

                    if label == "high" and score >= 9:
                        data.append([",".join(selected), "high"])

                    elif label == "medium" and 5 <= score < 9:
                        data.append([",".join(selected), "medium"])

                    elif label == "low" and score < 5:
                        data.append([",".join(selected), "low"])

            result = pd.DataFrame(data, columns=["ingredients", "label"])
            result.to_csv(self.output_path, index=False)
        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = TrainingDataGenerator()
    obj.generate(1000)