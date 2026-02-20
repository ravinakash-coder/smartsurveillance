#!/usr/bin/env python3
"""
Batch detection for Pictures folder
"""
import logging
import cv2
import os
from pathlib import Path
from src.object_detector import ObjectDetector

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Folder path
folder_path = r"C:\Users\ELCOT\OneDrive\Pictures"

# Verify folder exists
if not os.path.isdir(folder_path):
    logger.error(f"Folder not found: {folder_path}")
    exit(1)

# Find all images
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
image_files = []
for ext in image_extensions:
    image_files.extend(Path(folder_path).rglob(f"*{ext}"))
    image_files.extend(Path(folder_path).rglob(f"*{ext.upper()}"))

image_files = list(set(image_files))  # Remove duplicates

if not image_files:
    logger.info(f"No images found in {folder_path}")
    exit(0)

logger.info(f"Found {len(image_files)} images")

# Initialize detector once
logger.info("Initializing detector...")
detector = ObjectDetector(model_name="yolov8n.pt")

# Process each image
total_detections = 0
for idx, img_path in enumerate(image_files, 1):
    logger.info(f"\n[{idx}/{len(image_files)}] Processing: {img_path.name}")
    
    image = cv2.imread(str(img_path))
    if image is None:
        logger.warning(f"  Could not read image")
        continue
    
    # Run detection
    detections = detector.detect(image)
    total_detections += len(detections)
    
    logger.info(f"  Detections: {len(detections)}")
    for det in detections:
        logger.info(f"    - {det.class_name}: {det.confidence:.1%}")
    
    # Draw and save
    result_image = detector.draw_detections(image, detections)
    output_path = str(img_path).replace(str(img_path)[-4:], "_detected" + str(img_path)[-4:])
    cv2.imwrite(output_path, result_image)

logger.info(f"\n{'='*50}")
logger.info(f"Batch processing complete!")
logger.info(f"Total images: {len(image_files)}")
logger.info(f"Total detections: {total_detections}")
