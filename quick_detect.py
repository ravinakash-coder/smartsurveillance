"""Quick image detection script with command line argument"""

import cv2
import sys
import logging
from src.object_detector import ObjectDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if len(sys.argv) < 2:
    print("Usage: python quick_detect.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]

logger.info(f"Processing: {image_path}")
detector = ObjectDetector(confidence_threshold=0.5)

frame = cv2.imread(image_path)
if frame is None:
    logger.error(f"Failed to read image: {image_path}")
    sys.exit(1)

detections = detector.detect(frame)
logger.info(f"Found {len(detections)} objects")

for det in detections:
    logger.info(f"  - {det.class_name}: {det.confidence:.2f}")

output_frame = detector.draw_detections(frame, detections)
output_path = image_path.replace('.', '_detected.')
cv2.imwrite(output_path, output_frame)
logger.info(f"Saved to: {output_path}")

cv2.imshow("Detection Result", output_frame)
logger.info("Press any key to close...")
cv2.waitKey(0)
cv2.destroyAllWindows()
