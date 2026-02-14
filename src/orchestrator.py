"""
System Orchestrator - Coordinates all components
"""

import logging
from typing import List, Optional
from datetime import datetime, timedelta
from src.frame_grabber import FrameGrabber
from src.object_detector import ObjectDetector
from src.alert_system import AlertSystem

logger = logging.getLogger(__name__)


class SurveillanceOrchestrator:
    """Main orchestrator for the surveillance system"""
    
    def __init__(self):
        """Initialize the orchestrator"""
        self.frame_grabber: Optional[FrameGrabber] = None
        self.object_detector: Optional[ObjectDetector] = None
        self.alert_system: AlertSystem = AlertSystem()
        self.is_running = False
        
        # Configuration
        self.config = {
            'target_classes': ['person'],
            'confidence_threshold': 0.5,
            'alert_cooldown_seconds': 30,  # Prevent repeated alerts
            'enable_email_alerts': False,
            'save_alert_frames': True,
            'alert_frame_dir': 'alerts'
        }
        
        self.last_alert_time = None
        self.detection_history = []
    
    def initialize(self, camera_source: int = 0, model_name: str = "yolov8n.pt"):
        """
        Initialize all system components
        
        Args:
            camera_source: Camera index or video file path
            model_name: YOLOv8 model name
        """
        try:
            logger.info("Initializing surveillance system...")
            
            # Initialize frame grabber
            self.frame_grabber = FrameGrabber(source=camera_source, fps=30)
            if not self.frame_grabber.open():
                logger.error("Failed to initialize frame grabber")
                return False
            
            # Initialize object detector (may fall back to a lightweight detector)
            self.object_detector = ObjectDetector(
                model_name=model_name,
                confidence_threshold=self.config['confidence_threshold']
            )
            if self.object_detector.model is None and not getattr(self.object_detector, 'has_fallback', False):
                logger.warning("Object detector not available (YOLO/PyTorch missing). Running without detection or using simple fallback.")
            
            logger.info("Surveillance system initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            return False
    
    def process_frame(self):
        """
        Process a single frame
        
        Returns:
            Tuple of (frame, detections)
        """
        if self.frame_grabber is None:
            return None, []
        
        ret, frame = self.frame_grabber.get_frame()
        if not ret:
            return None, []
        
        # Run detection
        detections = self.object_detector.detect(frame)
        
        # Filter by target classes
        target_detections = self.object_detector.filter_by_class(
            detections,
            self.config['target_classes']
        )
        
        # Check if alert should be triggered
        if target_detections:
            self._handle_detection(frame, target_detections)
        
        # Store in history
        self.detection_history.append({
            'timestamp': datetime.now(),
            'detections': target_detections,
            'detection_count': len(target_detections),
            'frame_info': self.frame_grabber.get_frame_info()
        })
        
        return frame, target_detections
    
    def _handle_detection(self, frame, detections):
        """Handle object detection"""
        # Check alert cooldown
        if self.last_alert_time and \
           (datetime.now() - self.last_alert_time).seconds < \
           self.config['alert_cooldown_seconds']:
            return
        
        self.last_alert_time = datetime.now()
        
        # Log detection
        logger.warning(f"Alert triggered! Detected {len(detections)} object(s)")
        for det in detections:
            logger.warning(f"  - {det.class_name} ({det.confidence:.2f})")
        
        # Save alert frame
        if self.config['save_alert_frames']:
            frame_path = self.alert_system.save_alert_frame(
                frame,
                self.config['alert_frame_dir']
            )
        else:
            frame_path = None
        
        # Send email alert
        if self.config['enable_email_alerts']:
            subject = f"Security Alert: {len(detections)} Objects Detected"
            message = self._create_alert_message(detections)
            self.alert_system.send_alert_email(subject, message, frame_path)
    
    def _create_alert_message(self, detections) -> str:
        """Create alert message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Smart Surveillance Alert\n"
        message += f"Time: {timestamp}\n"
        message += f"Objects Detected: {len(detections)}\n\n"
        
        for det in detections:
            message += f"- {det.class_name} (Confidence: {det.confidence:.2%})\n"
        
        return message
    
    def start(self):
        """Start the surveillance system"""
        if self.frame_grabber is None:
            logger.error("System not initialized")
            return False
        
        self.is_running = True
        logger.info("Surveillance system started")
        return True
    
    def stop(self):
        """Stop the surveillance system"""
        self.is_running = False
        if self.frame_grabber:
            self.frame_grabber.release()
        logger.info("Surveillance system stopped")
    
    def configure(self, **kwargs):
        """Update configuration"""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
                logger.info(f"Configuration updated: {key} = {value}")
    
    def set_target_classes(self, classes: List[str]):
        """Set target detection classes"""
        self.config['target_classes'] = classes
        logger.info(f"Target classes set to: {classes}")
    
    def set_email_config(self, sender_email: str, sender_password: str, 
                        recipients: List[str]):
        """Configure email alerts"""
        self.alert_system.configure_email(sender_email, sender_password)
        for recipient in recipients:
            self.alert_system.add_recipient(recipient)
        self.config['enable_email_alerts'] = True
    
    def get_stats(self) -> dict:
        """Get system statistics"""
        return {
            'is_running': self.is_running,
            'total_detections': len(self.detection_history),
            'last_alert': self.last_alert_time,
            'config': self.config.copy()
        }
