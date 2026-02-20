#!/usr/bin/env python3
"""
Simple detection script without display dependencies
"""
import sys
import logging
import cv2
import os
from src.object_detector import ObjectDetector

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Get image path from argument or use default
if len(sys.argv) > 1:
    image_path = sys.argv[1]
else:
    image_path = r"C:\Users\ELCOT\OneDrive\Documents\New folder\BMW.jpg"

# Verify file exists
if not os.path.exists(image_path):
    logger.error(f"File not found: {image_path}")
    sys.exit(1)

logger.info(f"Loading: {image_path}")
image = cv2.imread(image_path)

if image is None:
    logger.error(f"Could not read image from {image_path}")
    sys.exit(1)

logger.info(f"Image shape: {image.shape}")

# Initialize detector
logger.info("Initializing detector...")
detector = ObjectDetector(model_name="yolov8n.pt")

# Run detection
logger.info("Running detection...")
detections = detector.detect(image)

# Report results
logger.info(f"\nDetections: {len(detections)} objects found")
for i, det in enumerate(detections, 1):
    logger.info(f"  {i}. {det.class_name}: {det.confidence:.2%}")

# Draw and save
result_image = detector.draw_detections(image, detections)
output_path = image_path.replace(image_path[-4:], "_detected" + image_path[-4:])
cv2.imwrite(output_path, result_image)
logger.info(f"\nSaved: {output_path}")
