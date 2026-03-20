import pandas as pd
import sys
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from src.logger import logging
from src.exception import CustomException
from src.utils.ingredient_vectorizer import IngredientVectorizer


class TrainingPipeline:

    def __init__(self):
        self.data_path = "datasets/training_data.csv"
        self.model_path = "artifacts/models/health_prediction_model.pkl"
        self.scaler_path = "artifacts/models/scaler.pkl"

    def train(self):

        try:
            logging.info("Starting training pipeline")

            # ================= LOAD DATA =================
            df = pd.read_csv(self.data_path)

            vectorizer = IngredientVectorizer()

            X = []
            y = []

            for _, row in df.iterrows():

                ingredients = [
                    i.strip().lower()
                    for i in row["ingredients"].split(",")
                ]

                vector = vectorizer.transform(ingredients)

                X.append(vector)
                y.append(row["label"])

            # ================= SPLIT =================
            X_train, X_test, y_train, y_test = train_test_split(
                X, y,
                test_size=0.2,
                random_state=42,
                stratify=y   # 🔥 IMPORTANT (balances classes)
            )

            # ================= SCALING =================
            scaler = StandardScaler()

            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)

            # ================= MODEL =================
            model = LogisticRegression(
                max_iter=1000,
                C=0.5,                   # 🔥 regularization
                class_weight='balanced' # 🔥 handle imbalance
            )

            model.fit(X_train, y_train)

            # ================= EVALUATION =================
            train_pred = model.predict(X_train)
            test_pred = model.predict(X_test)

            train_acc = accuracy_score(y_train, train_pred)
            test_acc = accuracy_score(y_test, test_pred)

            print("\n================ MODEL EVALUATION ================\n")

            print(f"Train Accuracy: {train_acc:.2f}")
            print(f"Test Accuracy : {test_acc:.2f}")

            print("\nClassification Report:\n")
            print(classification_report(y_test, test_pred))

            print("\nConfusion Matrix:\n")
            print(confusion_matrix(y_test, test_pred))

            # ================= ANALYSIS =================
            print("\n================ MODEL ANALYSIS ================\n")

            if train_acc - test_acc > 0.10:
                print("⚠ Model is OVERFITTING")
            elif test_acc < 0.65:
                print("⚠ Model is UNDERFITTING")
            else:
                print("✔ Model is GOOD (balanced & generalizing)")

            # ================= SAVE =================
            os.makedirs("artifacts/models", exist_ok=True)

            joblib.dump(model, self.model_path)
            joblib.dump(scaler, self.scaler_path)

            print("\n✅ Model + Scaler saved successfully")

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = TrainingPipeline()
    obj.train()