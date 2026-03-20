import cv2
from src.components.product_detector import ProductDetector
from src.components.ocr_engine import OCREngine
from src.components.ingredient_detector import IngredientDetector
from src.components.nutrition_analyzer import NutritionAnalyzer
from src.components.health_predictor import HealthPredictor


def main():

    cap = cv2.VideoCapture(0)

    product_detector = ProductDetector()
    ocr = OCREngine()
    ingredient_detector = IngredientDetector()
    analyzer = NutritionAnalyzer()
    predictor = HealthPredictor()

    print("\nPress 'c' to capture image")
    print("Press 'q' to quit\n")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1)

        # PRESS C → CAPTURE
        if key == ord('c'):

            print("\n📸 Capturing image...\n")

            # STEP 1: Detect product
            product = product_detector.detect(frame)
            print("Detected Product:", product)

            # STEP 2: Save image for OCR
            cv2.imwrite("captured.jpg", frame)

            # STEP 3: OCR
            text = ocr.extract_text("captured.jpg")

            # STEP 4: Ingredient detection
            ingredients = ingredient_detector.detect(text)

            print("\nIngredients:")
            for ing in ingredients:
                print(f"✔ {ing}")

            # STEP 5: Rule analysis
            results, score, decision = analyzer.analyze(ingredients)

            print("\nHealth Analysis:")
            for r in results:
                print(f"⚠ {r['ingredient']} → {r['effect']} ({r['risk']})")

            print("\nHealth Score:", score, "/10")

            # STEP 6: ML Prediction
            ml_result = predictor.predict(ingredients)

            print("\nML Prediction:", ml_result)

            # FINAL DECISION
            print("\nFinal Decision:")

            if ml_result == "high" or decision == "DANGEROUS":
                print("❌ NOT SAFE")
            elif ml_result == "medium":
                print("⚠ MODERATE")
            else:
                print("✔ SAFE")

        # PRESS Q → EXIT
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()