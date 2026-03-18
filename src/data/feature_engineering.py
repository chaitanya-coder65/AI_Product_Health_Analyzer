import pandas as pd
import sys
from src.logger import logging
from src.exception import CustomException

df = pd.read_csv(
    "datasets/processed/combined_ingredients.csv"
)
# remove very small invalid ingredients
df = df[df["ingredient"].str.len() > 3]

risk_map = {

# High risk food ingredients
"high fructose corn syrup":("food","high","diabetes risk"),
"trans fat":("food","high","heart disease"),
"aspartame":("food","high","metabolic disorder"),
"artificial color":("food","high","hyperactivity"),

# Medium risk food ingredients
"sugar":("food","medium","obesity risk"),
"sodium":("food","medium","blood pressure"),
"msg":("food","medium","headache"),
"palm oil":("food","medium","cholesterol"),
"caffeine":("food","medium","sleep disturbance"),

# Cosmetic risks
"parabens":("cosmetic","medium","hormone disruption"),
"sodium lauryl sulfate":("cosmetic","medium","skin irritation"),
"triclosan":("cosmetic","medium","antibiotic resistance"),
"formaldehyde":("cosmetic","high","carcinogen"),

# Safe ingredients
"glycerin":("cosmetic","safe","skin hydration"),
"zinc oxide":("cosmetic","safe","uv protection"),
"salicylic acid":("cosmetic","beneficial","acne treatment"),
"hyaluronic acid":("cosmetic","safe","skin hydration")

}

records = []

for ing in df["ingredient"]:

    ing = str(ing).lower().strip()

    if ing in risk_map:

        cat, risk, effect = risk_map[ing]

    else:

        cat = "unknown"
        risk = "unknown"
        effect = "unknown"

    records.append([ing, cat, risk, effect])

result = pd.DataFrame(
    records,
    columns=[
        "ingredient",
        "category",
        "risk_level",
        "health_effect"
    ]
)

result.to_csv(
    "datasets/final/ingredients_db.csv",
    index=False
)

print("Final ingredient database created.")