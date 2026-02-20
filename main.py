"""Main entry point for the SmartSurveillance application."""

import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('smartsurveillance.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Try to import GUI first, fall back to CLI if needed
try:
    from gui_app import main as gui_main
    USE_GUI = True
except ImportError as e:
    logger.warning(f"GUI unavailable: {e}. Falling back to CLI.")
    USE_GUI = False
    import cv2
    from pathlib import Path
    from src.object_detector import ObjectDetector


def run_live_detection():
    """Run real-time detection from camera"""
    logger.info("Starting live detection from camera...")
    detector = ObjectDetector(confidence_threshold=0.5)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.error("Failed to open camera!")
        return False
    
    logger.info("Camera opened. Detection running... (Press 'q' to quit)")
    frame_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.error("Failed to read frame")
                break
            
            frame_count += 1
            detections = detector.detect(frame)
            output_frame = detector.draw_detections(frame, detections)
            
            info_text = f"Frame: {frame_count} | Detections: {len(detections)}"
            cv2.putText(output_frame, info_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow("SmartSurveillance - Live Detection", output_frame)
            
            if detections:
                logger.info(f"Frame {frame_count}: {len(detections)} objects detected")
                for det in detections:
                    logger.info(f"  - {det.class_name}: {det.confidence:.2f}")
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                logger.info("Live detection stopped by user")
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    return True


def run_image_detection(image_path: str):
    """Run detection on a single image"""
    if not os.path.exists(image_path):
        logger.error(f"Image not found: {image_path}")
        return False
    
    logger.info(f"Processing image: {image_path}")
    detector = ObjectDetector(confidence_threshold=0.5)
    
    frame = cv2.imread(image_path)
    if frame is None:
        logger.error(f"Failed to load image: {image_path}")
        return False
    
    logger.info(f"Image shape: {frame.shape}")
    detections = detector.detect(frame)
    output_frame = detector.draw_detections(frame, detections)
    
    # Save output
    output_path = os.path.splitext(image_path)[0] + "_detected" + os.path.splitext(image_path)[1]
    cv2.imwrite(output_path, output_frame)
    logger.info(f"Saved: {output_path}")
    
    logger.info(f"Detections: {len(detections)} objects found")
    for det in detections:
        logger.info(f"  - {det.class_name}: {det.confidence:.2f}")
    
    return True


def run_batch_detection(folder_path: str):
    """Run detection on all images in a folder"""
    if not os.path.isdir(folder_path):
        logger.error(f"Folder not found: {folder_path}")
        return False
    
    logger.info(f"Starting batch detection on folder: {folder_path}")
    detector = ObjectDetector(confidence_threshold=0.5)
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    image_files = [f for f in Path(folder_path).rglob('*') 
                  if f.suffix.lower() in image_extensions]
    
    logger.info(f"Found {len(image_files)} images to process")
    
    total_detections = 0
    
    for idx, image_path in enumerate(image_files, 1):
        try:
            frame = cv2.imread(str(image_path))
            if frame is None:
                logger.warning(f"[{idx}/{len(image_files)}] Skipped: {image_path.name}")
                continue
            
            detections = detector.detect(frame)
            total_detections += len(detections)
            
            logger.info(f"[{idx}/{len(image_files)}] {image_path.name}: {len(detections)} objects")
            
            if detections:
                output_frame = detector.draw_detections(frame, detections)
                output_path = str(image_path.parent / (image_path.stem + "_detected" + image_path.suffix))
                cv2.imwrite(output_path, output_frame)
                
                for det in detections:
                    logger.info(f"    - {det.class_name}: {det.confidence:.2f}")
        
        except Exception as e:
            logger.error(f"Error processing {image_path.name}: {e}")
    
    logger.info(f"Batch complete! Total detections: {total_detections} across {len(image_files)} images")
    return True


def display_menu():
    """Display main menu and return user choice"""
    print("\n" + "="*50)
    print("SmartSurveillance - Object Detection System")
    print("="*50)
    print("1. Live Camera Detection")
    print("2. Single Image Detection")
    print("3. Batch Folder Detection")
    print("4. Exit")
    print("="*50)
    
    choice = input("Select option (1-4): ").strip()
    return choice


def main():
    """Main application entry point"""
    if USE_GUI:
        try:
            logger.info("Starting SmartSurveillance GUI...")
            gui_main()
        except Exception as e:
            logger.error(f"GUI error: {e}", exc_info=True)
            logger.info("Please close the GUI window to exit.")
    else:
        # CLI fallback
        try:
            while True:
                choice = display_menu()
                
                if choice == "1":
                    run_live_detection()
                
                elif choice == "2":
                    image_path = input("\nEnter image path: ").strip().strip('"')
                    if image_path:
                        run_image_detection(image_path)
                    else:
                        logger.warning("No path provided")
                
                elif choice == "3":
                    folder_path = input("\nEnter folder path: ").strip().strip('"')
                    if folder_path:
                        run_batch_detection(folder_path)
                    else:
                        logger.warning("No path provided")
                
                elif choice == "4":
                    logger.info("Exiting SmartSurveillance")
                    sys.exit(0)
                
                else:
                    print("Invalid option. Please try again.")
        
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            sys.exit(1)


if __name__ == "__main__":
    main()
