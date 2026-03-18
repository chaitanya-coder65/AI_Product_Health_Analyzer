import pandas as pd
import sys
from src.logger import logging
from src.exception import CustomException


def extract_food_ingredients():

    try:

        logging.info("Starting food ingredient extraction")

        df = pd.read_csv(
            "datasets/raw/en.openfoodfacts.org.products.tsv",
            sep="\t",
            low_memory=False,
            nrows=2000
        )

        ingredients = df["ingredients_text"].dropna()

        ingredient_list = []

        for item in ingredients:

            parts = item.split(",")

            for p in parts:
                ingredient_list.append(p.strip().lower())

        ingredient_list = list(set(ingredient_list))

        result = pd.DataFrame(
            ingredient_list,
            columns=["ingredient"]
        )

        result["category"] = "food"

        result.to_csv(
            "datasets/processed/extracted_food_ingredients.csv",
            index=False
        )

        logging.info("Food ingredients extracted successfully")

    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    extract_food_ingredients()