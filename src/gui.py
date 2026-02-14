"""
PyQt GUI Application for SmartSurveillance
"""

import sys
import cv2
import logging
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QSlider, QSpinBox,
                             QCheckBox, QLineEdit, QTextEdit, QComboBox, QTabWidget,
                             QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QFont
import numpy as np

from src.orchestrator import SurveillanceOrchestrator
from src.object_detector import Detection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProcessingThread(QThread):
    """Thread for frame processing"""
    
    frame_signal = pyqtSignal(np.ndarray)
    detection_signal = pyqtSignal(list)
    error_signal = pyqtSignal(str)
    
    def __init__(self, orchestrator: SurveillanceOrchestrator):
        super().__init__()
        self.orchestrator = orchestrator
        self.running = False
    
    def run(self):
        """Process frames in a separate thread"""
        self.running = True
        while self.running:
            try:
                if not self.orchestrator.is_running:
                    continue
                frame, detections = self.orchestrator.process_frame()
                if frame is not None:
                    self.frame_signal.emit(frame)
                    self.detection_signal.emit(detections)
            except Exception as e:
                self.error_signal.emit(str(e))
                break
    
    def stop(self):
        """Stop the processing thread"""
        self.running = False
        self.wait()


class SmartSurveillanceApp(QMainWindow):
    """Main PyQt application for SmartSurveillance"""
    
    def __init__(self):
        super().__init__()
        self.orchestrator = SurveillanceOrchestrator()
        self.processing_thread = None
        self.latest_detections = []  # Store latest detections for frame display
        self.init_ui()
        self.setWindowTitle("SmartSurveillance - Real-Time Detection")
        self.setGeometry(100, 100, 1600, 900)
    
    def init_ui(self):
        """Initialize the user interface"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Left side - Video and detections
        left_layout = QVBoxLayout()
        
        # Video display
        self.video_label = QLabel("No video source")
        self.video_label.setStyleSheet("background-color: black; min-width: 800px; min-height: 600px;")
        self.video_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(QLabel("Live Video Feed"), 0)
        left_layout.addWidget(self.video_label, 1)
        
        # Detection info
        self.detection_label = QLabel("Detections: 0")
        self.detection_label.setFont(QFont("Arial", 12, QFont.Bold))
        left_layout.addWidget(self.detection_label)
        
        # Right side - Controls
        right_layout = QVBoxLayout()
        
        # Create tabs for different sections
        tabs = QTabWidget()
        
        # Camera Tab
        camera_widget = self.create_camera_tab()
        tabs.addTab(camera_widget, "Camera")
        
        # Detection Tab
        detection_widget = self.create_detection_tab()
        tabs.addTab(detection_widget, "Detection")
        
        # Alert Tab
        alert_widget = self.create_alert_tab()
        tabs.addTab(alert_widget, "Alerts")
        
        # Statistics Tab
        stats_widget = self.create_stats_tab()
        tabs.addTab(stats_widget, "Statistics")
        
        right_layout.addWidget(tabs, 1)
        
        # Main layout
        layout.addLayout(left_layout, 2)
        layout.addLayout(right_layout, 1)
    
    def create_camera_tab(self) -> QWidget:
        """Create camera control tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Camera source selection
        layout.addWidget(QLabel("Camera Source:"))
        self.camera_combo = QComboBox()
        self.camera_combo.addItems(["Webcam (0)", "USB Camera (1)", "Video File"])
        layout.addWidget(self.camera_combo)
        
        # Video file selector
        self.video_file_input = QLineEdit()
        self.video_file_input.setPlaceholderText("Path to video file...")
        layout.addWidget(self.video_file_input)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_video_file)
        layout.addWidget(browse_btn)
        
        # Start/Stop buttons
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_surveillance)
        self.start_btn.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_surveillance)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        layout.addLayout(button_layout)
        
        layout.addStretch()
        return widget
    
    def create_detection_tab(self) -> QWidget:
        """Create detection settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Model selection
        layout.addWidget(QLabel("YOLOv8 Model:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(["yolov8n.pt", "yolov8s.pt", "yolov8m.pt", "yolov8l.pt"])
        layout.addWidget(self.model_combo)
        
        # Target classes
        layout.addWidget(QLabel("Target Classes (comma-separated):"))
        self.classes_input = QLineEdit()
        self.classes_input.setText("person")
        layout.addWidget(self.classes_input)
        
        # Confidence threshold
        layout.addWidget(QLabel("Confidence Threshold:"))
        self.confidence_slider = QSlider(Qt.Horizontal)
        self.confidence_slider.setMinimum(0)
        self.confidence_slider.setMaximum(100)
        self.confidence_slider.setValue(50)
        self.confidence_label = QLabel("0.50")
        self.confidence_slider.valueChanged.connect(self.update_confidence_label)
        layout.addWidget(self.confidence_slider)
        layout.addWidget(self.confidence_label)
        
        # Alert cooldown
        layout.addWidget(QLabel("Alert Cooldown (seconds):"))
        self.cooldown_spinbox = QSpinBox()
        self.cooldown_spinbox.setMinimum(5)
        self.cooldown_spinbox.setMaximum(300)
        self.cooldown_spinbox.setValue(30)
        layout.addWidget(self.cooldown_spinbox)
        
        # Save frames checkbox
        self.save_frames_check = QCheckBox("Save Alert Frames")
        self.save_frames_check.setChecked(True)
        layout.addWidget(self.save_frames_check)
        
        # Update button
        update_btn = QPushButton("Update Settings")
        update_btn.clicked.connect(self.update_detection_settings)
        layout.addWidget(update_btn)
        
        layout.addStretch()
        return widget
    
    def create_alert_tab(self) -> QWidget:
        """Create alert configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Email alerts checkbox
        self.email_alerts_check = QCheckBox("Enable Email Alerts")
        layout.addWidget(self.email_alerts_check)
        
        # Sender email
        layout.addWidget(QLabel("Sender Email:"))
        self.sender_email_input = QLineEdit()
        self.sender_email_input.setPlaceholderText("your-email@gmail.com")
        layout.addWidget(self.sender_email_input)
        
        # Sender password
        layout.addWidget(QLabel("Sender Password (Use App Password for Gmail):"))
        self.sender_password_input = QLineEdit()
        self.sender_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.sender_password_input)
        
        # Recipient emails
        layout.addWidget(QLabel("Recipient Emails (comma-separated):"))
        self.recipient_emails_input = QLineEdit()
        self.recipient_emails_input.setPlaceholderText("recipient1@example.com, recipient2@example.com")
        layout.addWidget(self.recipient_emails_input)
        
        # Configure button
        config_btn = QPushButton("Configure Alerts")
        config_btn.clicked.connect(self.configure_alerts)
        layout.addWidget(config_btn)
        
        # Alert test
        test_btn = QPushButton("Send Test Alert")
        test_btn.clicked.connect(self.send_test_alert)
        layout.addWidget(test_btn)
        
        layout.addStretch()
        return widget
    
    def create_stats_tab(self) -> QWidget:
        """Create statistics tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Stats display
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        layout.addWidget(self.stats_text)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Stats")
        refresh_btn.clicked.connect(self.update_stats)
        layout.addWidget(refresh_btn)
        
        return widget
    
    def browse_video_file(self):
        """Browse for video file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*)"
        )
        if file_path:
            self.video_file_input.setText(file_path)
    
    def start_surveillance(self):
        """Start the surveillance system"""
        try:
            # Determine camera source
            sel = self.camera_combo.currentText()
            if sel == "Video File":
                camera_source = self.video_file_input.text()
                if not camera_source:
                    QMessageBox.warning(self, "Error", "Please select a video file")
                    return
            else:
                # Extract numeric index from label like 'Webcam (0)'
                import re
                m = re.search(r"\((\d+)\)", sel)
                if m:
                    camera_source = int(m.group(1))
                else:
                    # fallback to 0
                    camera_source = 0
            
            # Initialize orchestrator
            model_name = self.model_combo.currentText()
            if not self.orchestrator.initialize(camera_source, model_name):
                QMessageBox.critical(self, "Error", "Failed to initialize system")
                return
            
            # Start orchestrator
            self.orchestrator.start()
            
            # Start processing thread
            self.processing_thread = ProcessingThread(self.orchestrator)
            self.processing_thread.frame_signal.connect(self.update_video_frame)
            self.processing_thread.detection_signal.connect(self.update_detections)
            self.processing_thread.error_signal.connect(self.handle_error)
            self.processing_thread.start()
            
            # Update UI
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            logger.info("Surveillance started")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start: {str(e)}")
            logger.error(f"Start error: {e}")
    
    def stop_surveillance(self):
        """Stop the surveillance system"""
        try:
            self.orchestrator.stop()
            if self.processing_thread:
                self.processing_thread.stop()
            
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.video_label.setText("Surveillance stopped")
            logger.info("Surveillance stopped")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to stop: {str(e)}")
    
    def update_video_frame(self, frame):
        """Update video display"""
        try:
            # Draw detections on the frame
            frame_with_detections = self.orchestrator.object_detector.draw_detections(
                frame,
                self.latest_detections
            )
            
            # Convert to RGB
            rgb_frame = cv2.cvtColor(frame_with_detections, cv2.COLOR_BGR2RGB)
            
            # Resize for display
            h, w, ch = rgb_frame.shape
            bytes_per_line = 3 * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            # Display
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaledToWidth(800, Qt.SmoothTransformation)
            self.video_label.setPixmap(scaled_pixmap)
            
        except Exception as e:
            logger.error(f"Frame update error: {e}")
    
    def update_detections(self, detections):
        """Update detection display"""
        self.latest_detections = detections
        self.detection_label.setText(f"Detections: {len(detections)}")
    
    def update_confidence_label(self):
        """Update confidence label"""
        value = self.confidence_slider.value() / 100.0
        self.confidence_label.setText(f"{value:.2f}")
    
    def update_detection_settings(self):
        """Update detection settings"""
        try:
            threshold = self.confidence_slider.value() / 100.0
            classes = [c.strip() for c in self.classes_input.text().split(',')]
            
            self.orchestrator.configure(
                confidence_threshold=threshold,
                alert_cooldown_seconds=self.cooldown_spinbox.value(),
                save_alert_frames=self.save_frames_check.isChecked()
            )
            self.orchestrator.set_target_classes(classes)
            
            QMessageBox.information(self, "Success", "Settings updated")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update settings: {str(e)}")
    
    def configure_alerts(self):
        """Configure email alerts"""
        try:
            if not self.email_alerts_check.isChecked():
                return
            
            sender = self.sender_email_input.text()
            password = self.sender_password_input.text()
            recipients = [r.strip() for r in self.recipient_emails_input.text().split(',')]
            
            if not sender or not password or not recipients:
                QMessageBox.warning(self, "Error", "Please fill in all email fields")
                return
            
            self.orchestrator.set_email_config(sender, password, recipients)
            QMessageBox.information(self, "Success", "Email alerts configured")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Configuration failed: {str(e)}")
    
    def send_test_alert(self):
        """Send a test alert"""
        try:
            subject = "SmartSurveillance Test Alert"
            message = "This is a test alert from SmartSurveillance system.\n\nAll systems operational."
            
            if self.orchestrator.alert_system.send_alert_email(subject, message):
                QMessageBox.information(self, "Success", "Test alert sent")
            else:
                QMessageBox.warning(self, "Error", "Failed to send test alert")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to send alert: {str(e)}")
    
    def update_stats(self):
        """Update statistics display"""
        stats = self.orchestrator.get_stats()
        alert_history = self.orchestrator.alert_system.get_alert_history()
        
        stats_text = f"System Status: {'Running' if stats['is_running'] else 'Stopped'}\n"
        stats_text += f"Total Detections: {stats['total_detections']}\n"
        stats_text += f"Last Alert: {stats['last_alert'] if stats['last_alert'] else 'None'}\n\n"
        stats_text += f"Configuration:\n"
        for key, value in stats['config'].items():
            stats_text += f"  {key}: {value}\n"
        
        stats_text += f"\nAlert History ({len(alert_history)} alerts):\n"
        for alert in alert_history[-10:]:  # Last 10 alerts
            stats_text += f"  - {alert['timestamp']}: {alert['subject']}\n"
        
        self.stats_text.setText(stats_text)
    
    def handle_error(self, error_msg: str):
        """Handle processing errors"""
        logger.error(f"Processing error: {error_msg}")
        self.stop_surveillance()
        QMessageBox.critical(self, "Error", f"Processing error: {error_msg}")
    
    def closeEvent(self, event):
        """Handle application close"""
        if self.orchestrator.is_running:
            self.stop_surveillance()
        event.accept()


def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    window = SmartSurveillanceApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
