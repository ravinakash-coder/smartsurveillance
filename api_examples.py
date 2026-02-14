"""
API Usage Examples
Shows how to use SmartSurveillance programmatically without the GUI
"""

from src.orchestrator import SurveillanceOrchestrator
from src.config import ConfigManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Example 1: Basic Usage
def example_basic():
    """Basic surveillance with default settings"""
    logger.info("Example 1: Basic Usage")
    
    orchestrator = SurveillanceOrchestrator()
    
    # Initialize with default camera
    orchestrator.initialize(camera_source=0, model_name="yolov8n.pt")
    
    # Start surveillance
    orchestrator.start()
    
    # Process frames (in real application, run in loop)
    for i in range(10):
        frame, detections = orchestrator.process_frame()
        if detections:
            logger.info(f"Frame {i}: {len(detections)} objects detected")
    
    orchestrator.stop()


# Example 2: Custom Configuration
def example_custom_config():
    """Use custom configuration"""
    logger.info("Example 2: Custom Configuration")
    
    config = ConfigManager("config.json")
    orchestrator = SurveillanceOrchestrator()
    
    # Configure from file
    orchestrator.configure(
        target_classes=config.detection.target_classes,
        confidence_threshold=config.detection.confidence_threshold,
        alert_cooldown_seconds=config.alert.alert_cooldown_seconds
    )
    
    # Initialize
    orchestrator.initialize(
        camera_source=config.camera.source,
        model_name=config.detection.model_name
    )


# Example 3: Email Alerts
def example_with_email():
    """Enable email alerts"""
    logger.info("Example 3: Email Alerts")
    
    orchestrator = SurveillanceOrchestrator()
    orchestrator.initialize()
    
    # Configure email
    orchestrator.set_email_config(
        sender_email="your-email@gmail.com",
        sender_password="your-app-password",  # Use app password for Gmail
        recipients=["recipient@example.com", "another@example.com"]
    )
    
    # Enable alerts
    orchestrator.configure(enable_email_alerts=True)
    
    orchestrator.start()


# Example 4: Multiple Classes Detection
def example_multiple_classes():
    """Detect multiple object classes"""
    logger.info("Example 4: Multiple Classes")
    
    orchestrator = SurveillanceOrchestrator()
    orchestrator.initialize()
    
    # Set multiple target classes
    orchestrator.set_target_classes(['person', 'car', 'dog', 'bicycle'])
    
    orchestrator.start()


# Example 5: Video File Processing
def example_video_file():
    """Process video file instead of live camera"""
    logger.info("Example 5: Video File Processing")
    
    orchestrator = SurveillanceOrchestrator()
    
    # Use video file as source
    video_path = "path/to/video.mp4"
    orchestrator.initialize(camera_source=video_path)
    
    orchestrator.start()
    
    frame_count = 0
    total_detections = 0
    
    # Process entire video
    while orchestrator.is_running:
        frame, detections = orchestrator.process_frame()
        if frame is None:
            break
        
        frame_count += 1
        if detections:
            total_detections += len(detections)
            logger.info(f"Frame {frame_count}: {len(detections)} detections")
    
    orchestrator.stop()
    logger.info(f"Total frames: {frame_count}, Total detections: {total_detections}")


# Example 6: Getting Statistics
def example_statistics():
    """Get system statistics"""
    logger.info("Example 6: Statistics")
    
    orchestrator = SurveillanceOrchestrator()
    orchestrator.initialize()
    orchestrator.start()
    
    # Process some frames
    for _ in range(30):
        orchestrator.process_frame()
    
    # Get stats
    stats = orchestrator.get_stats()
    logger.info(f"System running: {stats['is_running']}")
    logger.info(f"Total detections: {stats['total_detections']}")
    logger.info(f"Configuration: {stats['config']}")
    
    orchestrator.stop()


# Example 7: Alert History
def example_alert_history():
    """Access alert history"""
    logger.info("Example 7: Alert History")
    
    orchestrator = SurveillanceOrchestrator()
    orchestrator.initialize()
    
    # Configure alerts
    orchestrator.set_email_config(
        sender_email="your-email@gmail.com",
        sender_password="your-password",
        recipients=["recipient@example.com"]
    )
    
    orchestrator.start()
    
    # Process frames...
    
    # Get alert history
    history = orchestrator.alert_system.get_alert_history()
    for alert in history:
        logger.info(f"Alert at {alert['timestamp']}: {alert['subject']}")
    
    orchestrator.stop()


# Example 8: Frame Manipulation
def example_frame_manipulation():
    """Work with frames and detections"""
    logger.info("Example 8: Frame Manipulation")
    
    import cv2
    
    orchestrator = SurveillanceOrchestrator()
    orchestrator.initialize()
    orchestrator.start()
    
    frame, detections = orchestrator.process_frame()
    
    if frame is not None:
        # Draw detections on frame
        frame_with_detections = orchestrator.object_detector.draw_detections(
            frame,
            detections
        )
        
        # Save annotated frame
        cv2.imwrite("annotated_frame.jpg", frame_with_detections)
        logger.info("Saved annotated frame")
        
        # Work with detections
        for detection in detections:
            logger.info(f"{detection.class_name}: {detection.confidence:.2%}")
            logger.info(f"  BBox: {detection.bbox}")
    
    orchestrator.stop()


# Example 9: Custom Detection Threshold
def example_custom_threshold():
    """Adjust detection confidence threshold"""
    logger.info("Example 9: Custom Threshold")
    
    orchestrator = SurveillanceOrchestrator()
    orchestrator.initialize()
    
    # Set high threshold for only confident detections
    orchestrator.configure(confidence_threshold=0.8)
    
    # Or access detector directly
    orchestrator.object_detector.set_confidence_threshold(0.7)
    
    orchestrator.start()


# Example 10: Headless Monitoring
def example_headless_monitoring():
    """Run headless surveillance with logging"""
    logger.info("Example 10: Headless Monitoring")
    
    import time
    
    orchestrator = SurveillanceOrchestrator()
    orchestrator.initialize()
    
    # Configure for security monitoring
    orchestrator.set_target_classes(['person'])
    orchestrator.configure(
        alert_cooldown_seconds=60,
        save_alert_frames=True,
        confidence_threshold=0.6
    )
    
    orchestrator.start()
    
    try:
        frame_count = 0
        detection_count = 0
        
        while True:
            frame, detections = orchestrator.process_frame()
            
            if frame is None:
                time.sleep(0.01)
                continue
            
            frame_count += 1
            
            if detections:
                detection_count += len(detections)
                logger.warning(f"[ALERT] {len(detections)} person(s) detected!")
            
            # Log every 300 frames (10 seconds at 30 FPS)
            if frame_count % 300 == 0:
                logger.info(f"Monitoring active: {frame_count} frames, "
                           f"{detection_count} detections")
    
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    
    finally:
        orchestrator.stop()
        logger.info(f"Monitoring complete: {frame_count} total frames")


if __name__ == "__main__":
    # Run examples (comment out as needed)
    
    # example_basic()
    # example_custom_config()
    # example_with_email()
    # example_multiple_classes()
    # example_video_file()
    # example_statistics()
    # example_alert_history()
    # example_frame_manipulation()
    # example_custom_threshold()
    # example_headless_monitoring()
    
    logger.info("See code comments for examples to run")
