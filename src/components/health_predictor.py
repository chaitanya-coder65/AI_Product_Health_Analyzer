import joblib
import os
import sys

from src.logger import logging
from src.exception import CustomException
from src.utils.ingredient_vectorizer import IngredientVectorizer


class HealthPredictor:

    def __init__(self):

        try:
            self.model_path = "artifacts/models/health_prediction_model.pkl"
            self.scaler_path = "artifacts/models/scaler.pkl"

            if not os.path.exists(self.model_path):
                raise Exception("Model not found. Train first.")

            if not os.path.exists(self.scaler_path):
                raise Exception("Scaler not found. Train first.")

            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)

            self.vectorizer = IngredientVectorizer()

        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, ingredients):

        try:
            vector = self.vectorizer.transform(ingredients)

            vector = self.scaler.transform([vector])

            prediction = self.model.predict(vector)[0]

            return prediction

        except Exception as e:
            raise CustomException(e, sys)