"""Simple real-time object detection without GUI"""

import cv2
import logging
from src.object_detector import ObjectDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Initializing object detector...")
    detector = ObjectDetector(confidence_threshold=0.5)
    
    logger.info("Opening camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        logger.error("Failed to open camera!")
        return
    
    logger.info("Camera opened. Starting detection... (Press 'q' to quit)")
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            logger.error("Failed to read frame")
            break
        
        frame_count += 1
        
        # Run detection
        detections = detector.detect(frame)
        
        # Draw detections
        output_frame = detector.draw_detections(frame, detections)
        
        # Add frame info
        info_text = f"Frame: {frame_count} | Detections: {len(detections)}"
        cv2.putText(output_frame, info_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Display
        cv2.imshow("SmartSurveillance - Real-time Detection", output_frame)
        
        # Log detections
        if detections:
            logger.info(f"Frame {frame_count}: Detected {len(detections)} objects")
            for det in detections:
                logger.info(f"  - {det.class_name}: {det.confidence:.2f}")
        
        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            logger.info("Exiting...")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    logger.info("Detection stopped")

if __name__ == "__main__":
    main()
