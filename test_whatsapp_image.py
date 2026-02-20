#!/usr/bin/env python3
import logging
import cv2
import os
from src.object_detector import ObjectDetector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

image_path = r"C:\Users\ELCOT\OneDrive\Documents\New folder\BMW.jpg"

if not os.path.exists(image_path):
    print(f"Error: Image file not found at {image_path}")
    exit(1)

print(f"Loading image: {image_path}")
image = cv2.imread(image_path)

if image is None:
    print(f"Error: Could not read image from {image_path}")
    exit(1)

print(f"Image loaded successfully. Shape: {image.shape}")

# Initialize detector
print("\nInitializing object detector...")
detector = ObjectDetector(model_name="yolov8n.pt")

# Run detection
print("Running detection...")
detections = detector.detect(image)

print(f"\nDetections found: {len(detections)}")
for i, detection in enumerate(detections):
    print(f"  {i+1}. {detection.class_name} (confidence: {detection.confidence:.2f})")

# Draw detections
result_image = detector.draw_detections(image, detections)

# Save result
output_path = image_path.replace(".jpeg", "_detected.jpeg").replace(".jpg", "_detected.jpg")
cv2.imwrite(output_path, result_image)
print(f"\nResult saved to: {output_path}")

# Display
try:
    cv2.imshow("Detection Result", result_image)
    print("Press any key to close the window...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
except Exception as e:
    print(f"Could not display image (headless environment): {e}")
