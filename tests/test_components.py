"""
Tests for SmartSurveillance components
"""

import unittest
import numpy as np
from src.object_detector import ObjectDetector, Detection
from src.frame_grabber import FrameGrabber
from src.alert_system import AlertSystem
from src.orchestrator import SurveillanceOrchestrator

class TestFrameGrabber(unittest.TestCase):
    """Test frame grabber functionality"""
    
    def test_frame_grabber_initialization(self):
        """Test frame grabber can be initialized"""
        grabber = FrameGrabber(source=0)
        self.assertIsNotNone(grabber)
        self.assertEqual(grabber.source, 0)
        self.assertEqual(grabber.fps, 30)
    
    def test_frame_grabber_info(self):
        """Test frame grabber info retrieval"""
        grabber = FrameGrabber(source=0)
        # Info should be empty before opening
        self.assertEqual(grabber.get_frame_info(), {})


class TestObjectDetection(unittest.TestCase):
    """Test object detection functionality"""
    
    def test_detection_creation(self):
        """Test Detection dataclass"""
        det = Detection(
            class_name="person",
            confidence=0.95,
            bbox=(10, 20, 30, 40),
            class_id=0
        )
        self.assertEqual(det.class_name, "person")
        self.assertEqual(det.confidence, 0.95)
        self.assertEqual(det.bbox, (10, 20, 30, 40))
    
    def test_detector_initialization(self):
        """Test object detector initialization"""
        detector = ObjectDetector()
        self.assertIsNotNone(detector)
        self.assertEqual(detector.confidence_threshold, 0.5)


class TestAlertSystem(unittest.TestCase):
    """Test alert system functionality"""
    
    def test_alert_system_initialization(self):
        """Test alert system can be initialized"""
        alerts = AlertSystem()
        self.assertIsNotNone(alerts)
        self.assertEqual(len(alerts.recipient_emails), 0)
    
    def test_add_recipient(self):
        """Test adding email recipient"""
        alerts = AlertSystem()
        alerts.add_recipient("test@example.com")
        self.assertIn("test@example.com", alerts.recipient_emails)
    
    def test_duplicate_recipient(self):
        """Test that duplicate recipients are not added"""
        alerts = AlertSystem()
        alerts.add_recipient("test@example.com")
        alerts.add_recipient("test@example.com")
        self.assertEqual(len(alerts.recipient_emails), 1)


class TestOrchestrator(unittest.TestCase):
    """Test surveillance orchestrator functionality"""
    
    def test_orchestrator_initialization(self):
        """Test orchestrator can be initialized"""
        orchestrator = SurveillanceOrchestrator()
        self.assertIsNotNone(orchestrator)
        self.assertFalse(orchestrator.is_running)
    
    def test_configuration(self):
        """Test configuration updates"""
        orchestrator = SurveillanceOrchestrator()
        orchestrator.configure(alert_cooldown_seconds=60)
        self.assertEqual(orchestrator.config['alert_cooldown_seconds'], 60)
    
    def test_target_classes(self):
        """Test setting target classes"""
        orchestrator = SurveillanceOrchestrator()
        orchestrator.set_target_classes(['person', 'car'])
        self.assertEqual(orchestrator.config['target_classes'], ['person', 'car'])


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_orchestrator_stats(self):
        """Test orchestrator statistics"""
        orchestrator = SurveillanceOrchestrator()
        stats = orchestrator.get_stats()
        self.assertIn('is_running', stats)
        self.assertIn('config', stats)
        self.assertIn('total_detections', stats)


if __name__ == '__main__':
    unittest.main()
