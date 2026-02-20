#!/usr/bin/env python
"""Detect objects in uploaded image"""

import sys
import cv2
from pathlib import Path
from src.object_detector import ObjectDetector

# Initialize detector
detector = ObjectDetector(confidence_threshold=0.5)

# Image path - saved from attachment
image_path = "uploaded_image.jpg"

print(f"Loading image: {image_path}")
frame = cv2.imread(image_path)

if frame is None:
    print(f"Error: Failed to load image: {image_path}")
    sys.exit(1)

print(f"Image shape: {frame.shape}")

# Run detection
print("Running detection...")
detections = detector.detect(frame)

print(f"\n{'='*60}")
print(f"DETECTION RESULTS")
print(f"{'='*60}")
print(f"Total objects detected: {len(detections)}\n")

if detections:
    for i, det in enumerate(detections, 1):
        print(f"[{i}] {det.class_name.upper()}")
        print(f"    Confidence: {det.confidence:.2%}")
        print(f"    Location: x1={det.bbox[0]}, y1={det.bbox[1]}, x2={det.bbox[2]}, y2={det.bbox[3]}")
        print()
else:
    print("No objects detected")

# Draw detections
output_frame = detector.draw_detections(frame, detections)

# Save output
output_path = "uploaded_image_detected.jpg"
cv2.imwrite(output_path, output_frame)
print(f"Output saved: {output_path}")

print(f"{'='*60}\n")
