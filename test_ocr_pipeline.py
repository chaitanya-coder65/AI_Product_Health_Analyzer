from src.components.ocr_engine import OCREngine
from src.components.ingredient_detector import IngredientDetector
from src.components.health_analyzer import HealthAnalyzer

# Step 1: Read text from image
ocr = OCREngine()

text = ocr.extract_text("test_product.jpg")

print("OCR TEXT:")
print(text)


# Step 2: Detect ingredients
detector = IngredientDetector()

ingredients = detector.detect(text)

print("\nDetected Ingredients:")
print(ingredients)


# Step 3: Analyze health impact
analyzer = HealthAnalyzer()

results = analyzer.analyze(ingredients)

print("\nHealth Analysis:")

for r in results:
    print(r)