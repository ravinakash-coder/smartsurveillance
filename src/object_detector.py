"""
Object Detection Module - Uses YOLOv8 for real-time detection
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Detection:
    """Represents a detected object"""
    class_name: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x1, y1, x2, y2
    class_id: int


class ObjectDetector:
    """Real-time object detection using YOLOv8"""
    
    def __init__(self, model_name: str = "yolov8n.pt", confidence_threshold: float = 0.5):
        """
        Initialize the object detector
        
        Args:
            model_name: YOLOv8 model name (nano, small, medium, large, xlarge)
            confidence_threshold: Minimum confidence score
        """
        self.model_name = model_name
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.class_names = {}
        self.has_fallback = False
        self._initialize_model()

    class _MotionFallback:
        """Simple motion-based fallback detector using background subtraction"""
        def __init__(self, min_area: int = 500):
            self.backSub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)
            self.min_area = min_area

        def detect(self, frame: np.ndarray):
            mask = self.backSub.apply(frame)
            # Morphological ops to reduce noise
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            detections = []
            for cnt in contours:
                if cv2.contourArea(cnt) < self.min_area:
                    continue
                x, y, w, h = cv2.boundingRect(cnt)
                detections.append((x, y, x + w, y + h))
            return detections

        def draw_detections(self, frame: np.ndarray, detections):
            out = frame.copy()
            for (x1, y1, x2, y2) in detections:
                cv2.rectangle(out, (x1, y1), (x2, y2), (0, 255, 255), 2)
                cv2.putText(out, "motion", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            return out
    
    def _initialize_model(self):
        """Initialize YOLOv8 model"""
        try:
            from ultralytics import YOLO
            logger.info(f"Loading YOLOv8 model: {self.model_name}")
            self.model = YOLO(self.model_name)
            logger.info("YOLOv8 model loaded successfully")
        except ImportError:
            logger.error("ultralytics library not found. Falling back to motion detector.")
            self.model = None
            self.fallback = ObjectDetector._MotionFallback()
            self.has_fallback = True
            logger.info("Motion fallback detector initialized")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            logger.error("Falling back to motion detector.")
            self.model = None
            self.fallback = ObjectDetector._MotionFallback()
            self.has_fallback = True
            logger.info("Motion fallback detector initialized")
    
    def detect(self, frame: np.ndarray) -> List[Detection]:
        """
        Detect objects in a frame
        
        Args:
            frame: Input image frame
            
        Returns:
            List of detections
        """
        if self.model is None:
            # Use motion-based fallback when model unavailable
            if getattr(self, 'has_fallback', False):
                rects = self.fallback.detect(frame)
                detections = []
                for rect in rects:
                    x1, y1, x2, y2 = rect
                    detections.append(Detection(class_name='motion', confidence=1.0, bbox=(x1, y1, x2, y2), class_id=0))
                return detections
            return []
        
        try:
            results = self.model(frame, verbose=False)
            detections = []
            
            for result in results:
                for box in result.boxes:
                    confidence = float(box.conf)
                    if confidence >= self.confidence_threshold:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        class_id = int(box.cls)
                        class_name = result.names[class_id]
                        
                        detection = Detection(
                            class_name=class_name,
                            confidence=confidence,
                            bbox=(x1, y1, x2, y2),
                            class_id=class_id
                        )
                        detections.append(detection)
            
            return detections
        except Exception as e:
            logger.error(f"Error during detection: {e}")
            return []
    
    def filter_by_class(self, detections: List[Detection], 
                        class_names: List[str]) -> List[Detection]:
        """Filter detections by class names"""
        return [d for d in detections if d.class_name in class_names]
    
    def draw_detections(self, frame: np.ndarray, 
                       detections: List[Detection]) -> np.ndarray:
        """Draw bounding boxes on frame"""
        frame_copy = frame.copy()
        
        for detection in detections:
            x1, y1, x2, y2 = detection.bbox
            
            # Draw bounding box
            cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label
            label = f"{detection.class_name}: {detection.confidence:.2f}"
            cv2.putText(frame_copy, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame_copy
    
    def set_confidence_threshold(self, threshold: float):
        """Update confidence threshold"""
        self.confidence_threshold = max(0.0, min(1.0, threshold))
