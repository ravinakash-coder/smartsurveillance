"""
Utility functions for SmartSurveillance
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


def resize_frame(frame: np.ndarray, height: int = None, width: int = None) -> np.ndarray:
    """
    Resize frame while maintaining aspect ratio
    
    Args:
        frame: Input image
        height: Target height (width calculated if provided)
        width: Target width (height calculated if provided)
        
    Returns:
        Resized frame
    """
    if height is None and width is None:
        return frame
    
    h, w = frame.shape[:2]
    
    if width is not None and height is None:
        ratio = width / w
        height = int(h * ratio)
    elif height is not None and width is None:
        ratio = height / h
        width = int(w * ratio)
    
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)


def add_timestamp(frame: np.ndarray) -> np.ndarray:
    """
    Add timestamp to frame
    
    Args:
        frame: Input frame
        
    Returns:
        Frame with timestamp
    """
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return frame


def add_info_text(frame: np.ndarray, text: str, position: Tuple[int, int] = (10, 60)) -> np.ndarray:
    """
    Add custom text to frame
    
    Args:
        frame: Input frame
        text: Text to add
        position: (x, y) position
        
    Returns:
        Frame with text
    """
    cv2.putText(frame, text, position,
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return frame


def draw_roi(frame: np.ndarray, roi: Tuple[int, int, int, int], color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
    """
    Draw region of interest on frame
    
    Args:
        frame: Input frame
        roi: (x1, y1, x2, y2) coordinates
        color: BGR color tuple
        
    Returns:
        Frame with ROI drawn
    """
    x1, y1, x2, y2 = roi
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    return frame


def check_roi_intersection(bbox: Tuple[int, int, int, int], 
                           roi: Tuple[int, int, int, int]) -> bool:
    """
    Check if bounding box intersects with region of interest
    
    Args:
        bbox: (x1, y1, x2, y2) bounding box
        roi: (x1, y1, x2, y2) region of interest
        
    Returns:
        True if bounding box intersects with ROI
    """
    x1_bb, y1_bb, x2_bb, y2_bb = bbox
    x1_roi, y1_roi, x2_roi, y2_roi = roi
    
    return not (x2_bb < x1_roi or x2_roi < x1_bb or y2_bb < y1_roi or y2_roi < y1_bb)


def create_directories():
    """Create necessary directories"""
    directories = ['alerts', 'logs', 'config']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"Ensured directory exists: {directory}")


def validate_image_file(filepath: str) -> bool:
    """
    Validate if file is a valid image
    
    Args:
        filepath: Path to image file
        
    Returns:
        True if valid image file
    """
    try:
        img = cv2.imread(filepath)
        return img is not None
    except Exception as e:
        logger.error(f"Invalid image file {filepath}: {e}")
        return False


def validate_video_file(filepath: str) -> bool:
    """
    Validate if file is a valid video
    
    Args:
        filepath: Path to video file
        
    Returns:
        True if valid video file
    """
    try:
        cap = cv2.VideoCapture(filepath)
        ret = cap.isOpened()
        cap.release()
        return ret
    except Exception as e:
        logger.error(f"Invalid video file {filepath}: {e}")
        return False


def get_frame_dimensions(frame: np.ndarray) -> Tuple[int, int]:
    """
    Get frame dimensions
    
    Args:
        frame: Input frame
        
    Returns:
        (height, width) tuple
    """
    h, w = frame.shape[:2]
    return h, w


def apply_blur(frame: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """
    Apply Gaussian blur to frame
    
    Args:
        frame: Input frame
        kernel_size: Blur kernel size (must be odd)
        
    Returns:
        Blurred frame
    """
    if kernel_size % 2 == 0:
        kernel_size += 1
    return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)


def apply_edge_detection(frame: np.ndarray) -> np.ndarray:
    """
    Apply Canny edge detection
    
    Args:
        frame: Input frame
        
    Returns:
        Edge-detected frame
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return edges


def compare_frames(frame1: np.ndarray, frame2: np.ndarray) -> float:
    """
    Compare two frames and return similarity score
    
    Args:
        frame1: First frame
        frame2: Second frame
        
    Returns:
        Similarity score (0-1)
    """
    if frame1.shape != frame2.shape:
        return 0.0
    
    # Calculate mean squared error
    mse = np.mean((frame1.astype(float) - frame2.astype(float)) ** 2)
    # Convert MSE to similarity score
    similarity = np.exp(-mse / (255 ** 2))
    return float(similarity)
