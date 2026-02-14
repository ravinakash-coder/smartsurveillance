"""
Configuration module for SmartSurveillance
"""

from dataclasses import dataclass
from typing import List
import json
from pathlib import Path

@dataclass
class CameraConfig:
    """Camera configuration"""
    source: int = 0  # Camera index (0 = default webcam)
    width: int = 1280
    height: int = 720
    fps: int = 30

@dataclass
class DetectionConfig:
    """Detection settings"""
    model_name: str = "yolov8n.pt"  # YOLOv8 model variant
    confidence_threshold: float = 0.5
    target_classes: List[str] = None
    save_alert_frames: bool = True
    alert_frame_dir: str = "alerts"
    
    def __post_init__(self):
        if self.target_classes is None:
            self.target_classes = ["person"]

@dataclass
class AlertConfig:
    """Alert configuration"""
    enable_email: bool = False
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: str = ""
    sender_password: str = ""
    recipient_emails: List[str] = None
    alert_cooldown_seconds: int = 30
    
    def __post_init__(self):
        if self.recipient_emails is None:
            self.recipient_emails = []

class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.camera = CameraConfig()
        self.detection = DetectionConfig()
        self.alert = AlertConfig()
        self.load()
    
    def load(self):
        """Load configuration from file"""
        if Path(self.config_file).exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self._update_from_dict(data)
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
    
    def save(self):
        """Save configuration to file"""
        try:
            data = {
                'camera': self.camera.__dict__,
                'detection': self.detection.__dict__,
                'alert': self.alert.__dict__
            }
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def _update_from_dict(self, data: dict):
        """Update configuration from dictionary"""
        if 'camera' in data:
            for key, value in data['camera'].items():
                if hasattr(self.camera, key):
                    setattr(self.camera, key, value)
        
        if 'detection' in data:
            for key, value in data['detection'].items():
                if hasattr(self.detection, key):
                    setattr(self.detection, key, value)
        
        if 'alert' in data:
            for key, value in data['alert'].items():
                if hasattr(self.alert, key):
                    setattr(self.alert, key, value)
