import pandas as pd
import sys
from src.logger import logging
from src.exception import CustomException


def extract_cosmetic_ingredients():

    try:

        df = pd.read_csv(
            "datasets/raw/Sephora_all_423.csv"
        )

        ingredients = []

        for item in df["ingredients"].dropna():

            parts = item.split(",")

            for p in parts:
                ingredients.append(p.strip().lower())

        ingredients = list(set(ingredients))

        result = pd.DataFrame(
            ingredients,
            columns=["ingredient"]
        )

        result["category"] = "cosmetic"

        result.to_csv(
            "datasets/processed/extracted_cosmetic_ingredients.csv",
            index=False
        )

        logging.info("Cosmetic ingredients extracted successfully")

    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    extract_cosmetic_ingredients()