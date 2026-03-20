from ultralytics import YOLO
import cv2


class ProductDetector:

    def __init__(self):
        # Use pretrained model (no training needed initially)
        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):

        results = self.model(frame)

        for r in results:
            for box in r.boxes:

                class_id = int(box.cls[0])
                label = self.model.names[class_id]

                # SIMPLE MAPPING
                if "bottle" in label or "cup" in label:
                    return "cold_drink"

                elif "packet" in label or "bag" in label:
                    return "chips"

                elif "tube" in label:
                    return "toothpaste"

                elif "box" in label:
                    return "cosmetic"

        return "unknown"