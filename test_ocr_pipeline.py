from src.components.ocr_engine import OCREngine
from src.components.ingredient_detector import IngredientDetector
from src.components.nutrition_analyzer import NutritionAnalyzer
from src.components.health_predictor import HealthPredictor

from src.logger import logging
from src.exception import CustomException
import sys


def main():

    try:
        logging.info("Starting full pipeline")

        # =========================================================
        # STEP 1: OCR (Independent of ML training)
        # =========================================================
        ocr = OCREngine()
        text = ocr.extract_text("test_product.jpg")

        print("\n================ OCR TEXT (DEBUG) ================\n")
        print(text)

        # =========================================================
        # STEP 2: INGREDIENT DETECTION
        # =========================================================
        detector = IngredientDetector()
        ingredients = detector.detect(text)

        print("\n============= DETECTED INGREDIENTS =============\n")

        if not ingredients:
            print("❌ No ingredients detected")
            return

        for ing in ingredients:
            print(f"✔ {ing}")

        # =========================================================
        # STEP 3: RULE + QUANTITY ANALYSIS
        # =========================================================
        analyzer = NutritionAnalyzer()
        results, score, decision = analyzer.analyze(ingredients)

        print("\n============== RULE-BASED ANALYSIS ==============\n")

        if not results:
            print("❌ No health data found")
        else:
            for r in results:
                print(f"⚠ {r['ingredient']}")
                print(f"   → Effect: {r['effect']}")
                print(f"   → Risk: {r['risk']}\n")

        print("\n===========================================\n")
        print(f"Health Score: {score} / 10")

        

        predictor = HealthPredictor()
        ml_result = predictor.predict(ingredients)

        print("\n============== ML PREDICTION ==============\n")

        if ml_result == "low":
            print("✔ ML: SAFE")
        elif ml_result == "medium":
            print("⚠ ML: MODERATE")
        else:
            print("❌ ML: DANGEROUS")

        # =========================================================
        # FINAL DECISION (HYBRID LOGIC)
        # =========================================================
        print("\n============== FINAL DECISION ==============\n")

        if ml_result == "high" or decision == "DANGEROUS":
            print("❌ Product is NOT SAFE")
        elif ml_result == "medium" or decision == "MODERATE":
            print("⚠ Consume in MODERATION")
        else:
            print("✔ Product is SAFE")

        logging.info("Pipeline executed successfully")

    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    main()