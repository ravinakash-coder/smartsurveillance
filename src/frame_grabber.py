"""
Frame Grabber Module - Handles video capture and frame extraction
"""

import cv2
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class FrameGrabber:
    """Captures video frames from camera or video file"""
    
    def __init__(self, source: int = 0, fps: int = 30):
        """
        Initialize the frame grabber
        
        Args:
            source: Camera index or video file path (default: 0 for webcam)
            fps: Frames per second
        """
        self.source = source
        self.fps = fps
        self.cap = None
        self.is_active = False
        self.frame_count = 0
        
    def open(self) -> bool:
        """Open the video capture device"""
        try:
            # On Windows prefer DirectShow backend which is more reliable for webcams
            try:
                self.cap = cv2.VideoCapture(self.source, cv2.CAP_DSHOW)
            except Exception:
                self.cap = cv2.VideoCapture(self.source)

            if not self.cap.isOpened():
                logger.error(f"Failed to open video source: {self.source}")
                return False
            
            # Set FPS
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            # Set frame size
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
            self.is_active = True
            logger.info(f"Video source opened: {self.source}")
            return True
        except Exception as e:
            logger.error(f"Error opening video source: {e}")
            return False
    
    def get_frame(self) -> Tuple[bool, Optional]:
        """
        Get the next frame from the video source
        
        Returns:
            Tuple of (success, frame)
        """
        if not self.is_active or self.cap is None:
            return False, None
        
        ret, frame = self.cap.read()
        if ret:
            self.frame_count += 1
        return ret, frame
    
    def get_frame_info(self) -> dict:
        """Get information about current video stream"""
        if self.cap is None:
            return {}
        
        return {
            'fps': self.cap.get(cv2.CAP_PROP_FPS),
            'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'frame_count': self.frame_count,
            'total_frames': int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        }
    
    def release(self):
        """Release the video capture device"""
        if self.cap is not None:
            self.cap.release()
            self.is_active = False
            logger.info("Video source released")
    
    def __del__(self):
        """Cleanup on deletion"""
        self.release()
