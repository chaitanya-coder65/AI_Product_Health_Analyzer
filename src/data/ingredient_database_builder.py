import pandas as pd
import sys
from src.logger import logging
from src.exception import CustomException


food = pd.read_csv(
    "datasets/processed/extracted_food_ingredients.csv"
)

cosmetic = pd.read_csv(
    "datasets/processed/extracted_cosmetic_ingredients.csv"
)

combined = pd.concat([food, cosmetic])

combined.drop_duplicates(inplace=True)

combined.to_csv(
    "datasets/processed/combined_ingredients.csv",
    index=False
)

print("Combined ingredient dataset created.")