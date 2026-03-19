from src.components.ocr_engine import OCREngine
from src.components.ingredient_detector import IngredientDetector
from src.components.health_analyzer import HealthAnalyzer


def main():

    try:
        # ================= STEP 1: OCR =================
        ocr = OCREngine()
        text = ocr.extract_text("test_product.jpg")

        # ================= STEP 2: INGREDIENT DETECTION =================
        detector = IngredientDetector()
        ingredients = detector.detect(text)

        # ================= STEP 3: HEALTH ANALYSIS =================
        analyzer = HealthAnalyzer()
        results, score, decision = analyzer.analyze(ingredients)

        # ================= FINAL OUTPUT =================

        print("\n================ OCR TEXT (FOR DEBUG ONLY) ================\n")
        print(text)

        print("\n============= DETECTED INGREDIENTS =============\n")

        if not ingredients:
            print("No ingredients detected")
        else:
            for ing in ingredients:
                print(f"✔ {ing}")

        print("\n============== HEALTH ANALYSIS ==============\n")

        if not results:
            print("No health risks identified")
        else:
            for r in results:
                print(f"⚠ {r['ingredient']} → {r['effect']} ({r['risk']})")

        print("\n===========================================\n")
        print(f"Health Score: {score} / 10")

        # ================= FINAL DECISION =================

        if decision == "SAFE":
            print("✔ Product is SAFE to consume")
        elif decision == "MODERATE":
            print("⚠ Product should be consumed in MODERATION")
        else:
            print("❌ Product is NOT SAFE for frequent consumption")


    except Exception as e:
        print("Error occurred:", e)


if __name__ == "__main__":
    main()