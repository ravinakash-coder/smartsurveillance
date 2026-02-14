"""
Console-based example of SmartSurveillance system
Run this for command-line usage without PyQt GUI
"""

import logging
import time
import sys
from src.orchestrator import SurveillanceOrchestrator
from src.config import ConfigManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run SmartSurveillance in console mode"""
    
    # Load configuration
    config_manager = ConfigManager("config.json")
    logger.info("Configuration loaded")
    
    # Initialize orchestrator
    orchestrator = SurveillanceOrchestrator()
    
    # Configure from file
    orchestrator.configure(
        target_classes=config_manager.detection.target_classes,
        confidence_threshold=config_manager.detection.confidence_threshold,
        alert_cooldown_seconds=config_manager.alert.alert_cooldown_seconds,
        save_alert_frames=config_manager.detection.save_alert_frames,
        alert_frame_dir=config_manager.detection.alert_frame_dir
    )
    
    # Initialize system
    logger.info("Initializing surveillance system...")
    if not orchestrator.initialize(
        camera_source=config_manager.camera.source,
        model_name=config_manager.detection.model_name
    ):
        logger.error("Failed to initialize system")
        return 1
    
    # Configure email if enabled
    if config_manager.alert.enable_email:
        orchestrator.set_email_config(
            config_manager.alert.sender_email,
            config_manager.alert.sender_password,
            config_manager.alert.recipient_emails
        )
    
    # Start system
    orchestrator.start()
    logger.info("System started. Press Ctrl+C to stop.")
    
    try:
        frame_count = 0
        while orchestrator.is_running:
            frame, detections = orchestrator.process_frame()
            
            if frame is None:
                time.sleep(0.01)
                continue
            
            frame_count += 1
            
            # Log detections every second
            if frame_count % 30 == 0:
                if detections:
                    logger.info(f"Frame {frame_count}: {len(detections)} object(s) detected")
                    for det in detections:
                        logger.info(f"  - {det.class_name} ({det.confidence:.2%})")
                else:
                    logger.debug(f"Frame {frame_count}: No detections")
    
    except KeyboardInterrupt:
        logger.info("Stopping system...")
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1
    
    finally:
        orchestrator.stop()
        stats = orchestrator.get_stats()
        logger.info("System stopped")
        logger.info(f"Total frames processed: {frame_count}")
        logger.info(f"Total detections: {stats['total_detections']}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
