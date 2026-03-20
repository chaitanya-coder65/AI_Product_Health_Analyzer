from src.utils.ingredient_vectorizer import IngredientVectorizer

vectorizer = IngredientVectorizer()

ingredients = ["sugar", "caffeine"]

vector = vectorizer.transform(ingredients)

print("Ingredients:", ingredients)
print("Vector length:", len(vector))
print("Vector:", vector[:20])  # print first 20 values