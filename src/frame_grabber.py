"""
Frame Grabber Module - Handles video capture and frame extraction
Optimized with threading and frame buffering for continuous capture
"""

import cv2
from typing import Optional, Tuple
import logging
from threading import Thread, Lock
from queue import Queue, Full
from collections import deque
import time

logger = logging.getLogger(__name__)


class FrameGrabber:
    """Captures video frames from camera or video file with threading and buffering"""
    
    def __init__(self, source: int = 0, fps: int = 30, buffer_size: int = 30):
        """
        Initialize the frame grabber with buffering
        
        Args:
            source: Camera index or video file path (default: 0 for webcam)
            fps: Frames per second
            buffer_size: Maximum frames to buffer (default: 30)
        """
        logger.debug(f"Initializing FrameGrabber - source={source}, fps={fps}, buffer_size={buffer_size}")
        self.source = source
        self.fps = fps
        self.buffer_size = buffer_size
        self.cap = None
        self.is_active = False
        self.frame_count = 0
        
        # Threading components
        self.frame_buffer = deque(maxlen=buffer_size)  # Circular buffer
        self.buffer_lock = Lock()
        self.capture_thread = None
        self.is_running = False
        self.fps_counter = 0
        self.last_fps_time = time.time()
        self.frame_errors = 0
        self.total_frames_processed = 0
        logger.debug("FrameGrabber initialization complete")
        
    def open(self) -> bool:
        """Open the video capture device and start capture thread"""
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
            self.is_running = True
            
            # Start continuous frame capture thread
            self.capture_thread = Thread(target=self._capture_frames, daemon=True)
            self.capture_thread.start()
            
            logger.info(f"Video source opened: {self.source} with buffer size {self.buffer_size}")
            return True
        except Exception as e:
            logger.error(f"Error opening video source: {e}")
            return False
    
    def _capture_frames(self):
        """Continuously capture frames in a separate thread"""
        logger.info("Frame capture thread started")
        while self.is_running and self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                with self.buffer_lock:
                    self.frame_buffer.append((ret, frame.copy()))
                    self.frame_count += 1
                    
                    # Update FPS counter
                    self.fps_counter += 1
                    current_time = time.time()
                    if current_time - self.last_fps_time >= 1.0:
                        logger.debug(f"Actual capture FPS: {self.fps_counter}")
                        self.fps_counter = 0
                        self.last_fps_time = current_time
            else:
                logger.warning("Failed to read frame from video source")
                time.sleep(0.01)  # Prevent busy waiting
    
    def get_frame(self) -> Tuple[bool, Optional]:
        """
        Get the latest frame from the buffer
        
        Returns:
            Tuple of (success, frame)
        """
        if not self.is_active:
            return False, None
        
        with self.buffer_lock:
            if len(self.frame_buffer) > 0:
                # Get the most recent frame
                ret, frame = self.frame_buffer[-1]
                return ret, frame
        
        return False, None
    
    def get_buffered_frames(self) -> list:
        """
        Get all buffered frames
        
        Returns:
            List of (ret, frame) tuples
        """
        with self.buffer_lock:
            return list(self.frame_buffer)
    
    def get_buffer_size(self) -> int:
        """Get current number of frames in buffer"""
        with self.buffer_lock:
            return len(self.frame_buffer)
    
    def get_frame_info(self) -> dict:
        """Get information about current video stream"""
        if self.cap is None:
            return {}
        
        return {
            'fps': self.cap.get(cv2.CAP_PROP_FPS),
            'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'frame_count': self.frame_count,
            'total_frames': int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'buffer_size': self.get_buffer_size()
        }
    
    def release(self):
        """Release the video capture device"""
        self.is_running = False
        if self.capture_thread is not None:
            self.capture_thread.join(timeout=2.0)
        
        if self.cap is not None:
            self.cap.release()
            self.is_active = False
            logger.info("Video source released")
    
    def __del__(self):
        """Cleanup on deletion"""
        self.release()
