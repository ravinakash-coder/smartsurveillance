"""Image-based object detection with upload support"""

import cv2
import os
import logging
from pathlib import Path
from src.object_detector import ObjectDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_image(image_path: str, detector: ObjectDetector) -> bool:
    """
    Process a single image and display results
    
    Args:
        image_path: Path to the image file
        detector: ObjectDetector instance
        
    Returns:
        True if successful, False otherwise
    """
    if not os.path.exists(image_path):
        logger.error(f"Image not found: {image_path}")
        return False
    
    # Read image
    frame = cv2.imread(image_path)
    if frame is None:
        logger.error(f"Failed to read image: {image_path}")
        return False
    
    logger.info(f"Processing: {image_path}")
    logger.info(f"Image size: {frame.shape}")
    
    # Run detection
    detections = detector.detect(frame)
    logger.info(f"Found {len(detections)} objects")
    
    # Log detections
    for det in detections:
        logger.info(f"  - {det.class_name}: {det.confidence:.2f}")
    
    # Draw detections
    output_frame = detector.draw_detections(frame, detections)
    
    # Save result
    output_path = image_path.replace('.', '_detected.')
    cv2.imwrite(output_path, output_frame)
    logger.info(f"Saved result to: {output_path}")
    
    # Display (press any key to continue)
    cv2.imshow("Detection Result", output_frame)
    logger.info("Press any key to continue...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return True


def main():
    logger.info("Initializing object detector...")
    detector = ObjectDetector(confidence_threshold=0.5)
    
    # Ask user for image path
    print("\n" + "="*60)
    print("SmartSurveillance - Image Detection")
    print("="*60)
    print("\nOptions:")
    print("1. Process a single image")
    print("2. Process all images in a folder")
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == '1':
        image_path = input("Enter image path: ").strip()
        process_image(image_path, detector)
        
    elif choice == '2':
        folder_path = input("Enter folder path: ").strip()
        if not os.path.isdir(folder_path):
            logger.error(f"Folder not found: {folder_path}")
            return
        
        # Supported formats
        image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
        image_files = [f for f in os.listdir(folder_path) 
                      if f.lower().endswith(image_extensions)]
        
        if not image_files:
            logger.warning("No image files found in folder")
            return
        
        logger.info(f"Found {len(image_files)} images to process")
        
        for filename in image_files:
            image_path = os.path.join(folder_path, filename)
            process_image(image_path, detector)
            
        logger.info("Batch processing complete!")
        
    elif choice == '3':
        logger.info("Exiting...")
        return
    else:
        logger.error("Invalid option")


if __name__ == "__main__":
    main()
