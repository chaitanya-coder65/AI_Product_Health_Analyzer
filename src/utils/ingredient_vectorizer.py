import pandas as pd
import os


class IngredientVectorizer:

    def __init__(self):
        self.db_path = "datasets/final/advanced_ingredients_db.csv"

        if not os.path.exists(self.db_path):
            raise Exception("Ingredient DB not found")

        df = pd.read_csv(self.db_path)

        # ✅ All known ingredients
        self.ingredients_list = sorted(df["ingredient"].dropna().unique())

        # mapping → ingredient → index
        self.index_map = {
            ing: idx for idx, ing in enumerate(self.ingredients_list)
        }

    def transform(self, ingredients):

        # vector size = total known ingredients
        vector = [0] * len(self.ingredients_list)

        for ing in ingredients:
            ing = ing.lower().strip()

            if ing in self.index_map:
                vector[self.index_map[ing]] = 1

        return vector