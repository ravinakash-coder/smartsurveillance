"""
Alert System Module - Handles notifications and alerts
"""

import smtplib
import cv2
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class AlertSystem:
    """Manages alerts and notifications"""
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        """
        Initialize alert system
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP port number
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = None
        self.sender_password = None
        self.recipient_emails = []
        self.alert_history = []
    
    def configure_email(self, sender_email: str, sender_password: str):
        """Configure email credentials"""
        self.sender_email = sender_email
        self.sender_password = sender_password
        logger.info(f"Email configured for: {sender_email}")
    
    def add_recipient(self, email: str):
        """Add email recipient"""
        if email not in self.recipient_emails:
            self.recipient_emails.append(email)
            logger.info(f"Recipient added: {email}")
    
    def send_alert_email(self, subject: str, message: str, 
                         attachment_path: str = None) -> bool:
        """
        Send alert email
        
        Args:
            subject: Email subject
            message: Email body
            attachment_path: Path to image attachment (optional)
            
        Returns:
            True if successful
        """
        if not self.sender_email or not self.sender_password:
            logger.error("Email not configured")
            return False
        
        if not self.recipient_emails:
            logger.error("No recipients configured")
            return False
        
        try:
            # Create email
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(self.recipient_emails)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            # Add attachment if provided
            if attachment_path and Path(attachment_path).exists():
                self._attach_image(msg, attachment_path)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            self.alert_history.append({
                'timestamp': datetime.now(),
                'subject': subject,
                'recipients': self.recipient_emails.copy()
            })
            
            logger.info(f"Alert email sent to {len(self.recipient_emails)} recipient(s)")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def _attach_image(self, msg: MIMEMultipart, image_path: str):
        """Attach image to email"""
        try:
            with open(image_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {Path(image_path).name}')
            msg.attach(part)
            logger.info(f"Image attached: {image_path}")
        except Exception as e:
            logger.error(f"Failed to attach image: {e}")
    
    def save_alert_frame(self, frame, output_dir: str = "alerts") -> str:
        """
        Save alert frame to disk
        
        Args:
            frame: Image frame
            output_dir: Directory to save frames
            
        Returns:
            Path to saved image
        """
        try:
            Path(output_dir).mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"alert_{timestamp}.jpg"
            filepath = Path(output_dir) / filename
            
            cv2.imwrite(str(filepath), frame)
            logger.info(f"Alert frame saved: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to save alert frame: {e}")
            return None
    
    def get_alert_history(self) -> List[dict]:
        """Get alert history"""
        return self.alert_history.copy()
