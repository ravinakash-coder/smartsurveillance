# SmartSurveillance

Real-Time Automated Surveillance and Proactive Alert System using Deep Learning-Based Object Detection

A comprehensive smart surveillance system that uses YOLOv8 deep learning model for real-time object detection, PyQt5 for an intuitive GUI, and automated email alerts for detected security threats.

## Features

- **Real-Time Video Processing**: Capture and process video frames in real-time using OpenCV
- **YOLOv8 Object Detection**: State-of-the-art deep learning model for accurate object detection
- **PyQt5 GUI**: Professional user interface with live video feed and controls
- **FrameGrabber**: Efficient video frame capture from webcam or video files
- **Custom Orchestrator**: Seamless coordination between all system components
- **Email Alerts**: Automatic email notifications when objects are detected
- **Alert Frame Capture**: Save snapshots of detected events
- **Configurable Settings**: Easy configuration of detection parameters and alert settings
- **Multi-model Support**: Choose from YOLOv8 variants (nano, small, medium, large, xlarge)

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    PyQt5 GUI Interface                   │
├─────────────────────────────────────────────────────────┤
│                    Orchestrator                          │
│  ┌──────────────┬──────────────┬──────────────┐         │
│  │ FrameGrabber │ ObjectDetector│ AlertSystem │         │
│  └──────────────┴──────────────┴──────────────┘         │
├─────────────────────────────────────────────────────────┤
│  OpenCV        │  YOLOv8/PyTorch  │  Email/SMTP        │
└─────────────────────────────────────────────────────────┘
```

## Project Structure

```
SmartSurveillance/
├── src/
│   ├── __init__.py           # Package initialization
│   ├── frame_grabber.py      # Video capture module
│   ├── object_detector.py    # YOLOv8 detection
│   ├── alert_system.py       # Alert and notification system
│   ├── orchestrator.py       # System coordinator
│   ├── config.py             # Configuration management
│   └── gui.py                # PyQt5 interface
├── tests/
│   ├── __init__.py
│   └── test_components.py    # Unit tests
├── main.py                   # GUI entry point
├── console_example.py        # CLI example
├── config.json               # Configuration file
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
└── .gitignore               # Git ignore rules
```

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/SmartSurveillance.git
cd SmartSurveillance
```

### 2. Create virtual environment
```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

This will install:
- OpenCV for video processing
- YOLOv8/Ultralytics for object detection
- PyTorch (deep learning framework)
- PyQt5 for GUI
- And other required packages

## Usage

### GUI Mode (Recommended)

Run the PyQt application:
```bash
python main.py
```

**Features:**
- **Camera Tab**: Select camera source (webcam, USB camera, or video file)
- **Detection Tab**: Configure YOLOv8 model, confidence threshold, and target classes
- **Alerts Tab**: Set up email notifications
- **Statistics Tab**: View system statistics and alert history

### Console Mode

For headless/CLI usage:
```bash
python console_example.py
```

## Configuration

Edit `config.json` to customize system behavior:

```json
{
    "camera": {
        "source": 0,
        "width": 1280,
        "height": 720,
        "fps": 30
    },
    "detection": {
        "model_name": "yolov8n.pt",
        "confidence_threshold": 0.5,
        "target_classes": ["person"],
        "save_alert_frames": true,
        "alert_frame_dir": "alerts"
    },
    "alert": {
        "enable_email": false,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "your-email@gmail.com",
        "sender_password": "your-app-password",
        "recipient_emails": ["recipient@example.com"],
        "alert_cooldown_seconds": 30
    }
}
```

### Email Setup (Optional)

To enable email alerts:

1. **For Gmail:**
   - Enable 2-Factor Authentication
   - Generate an [App Password](https://support.google.com/accounts/answer/185833)
   - Use the app password in the configuration

2. **For other providers:**
   - Use your email provider's SMTP settings
   - Update `smtp_server` and `smtp_port` in config

## Components Overview

### FrameGrabber (`frame_grabber.py`)
Handles video capture from webcam or video files:
- Real-time frame extraction
- FPS and resolution configuration
- Video stream info retrieval

### ObjectDetector (`object_detector.py`)
Performs real-time object detection using YOLOv8:
- Detection in multiple model sizes
- Confidence threshold filtering
- Class-based filtering
- Bounding box visualization

### AlertSystem (`alert_system.py`)
Manages notifications and alerts:
- Email alerts with SMTP
- Alert frame capture and storage
- Alert history tracking
- Customizable alert messages

### SurveillanceOrchestrator (`orchestrator.py`)
Coordinates all components:
- System initialization and lifecycle
- Frame processing pipeline
- Detection triggering
- Alert management
- Statistics tracking

### GUI (`gui.py`)
PyQt5 user interface providing:
- Real-time video display
- Live detection overlay
- Configuration controls
- Alert history viewer
- System statistics

## Python Version

- Python 3.8 or higher

## Dependencies

See `requirements.txt` for complete list. Main dependencies:
- OpenCV 4.8+
- YOLOv8/Ultralytics
- PyTorch 2.0+
- PyQt5 5.15+
- NumPy 1.24+

## Running Tests

```bash
pytest tests/
```

Or with coverage:
```bash
pytest --cov=src tests/
```

## Performance Tips

1. **Use YOLOv8-nano** for real-time performance on CPU
2. **Enable GPU acceleration** if CUDA-capable GPU available
3. **Adjust confidence threshold** to reduce false positives
4. **Set alert cooldown** to prevent alert spam
5. **Use appropriate frame resolution** based on hardware

## Troubleshooting

### No video source detected
- Check camera connection
- Verify camera index (try 0, 1, 2, etc.)
- Check camera permissions (Linux/macOS)

### Poor detection accuracy
- Ensure adequate lighting
- Adjust confidence threshold (lower for more detections)
- Try larger YOLOv8 model (s, m, l, xl)
- Check target classes configuration

### Email not sending
- Verify SMTP settings
- Check internet connection
- Use app password for Gmail
- Check recipient email address
- Review application logs

## System Requirements

### Minimum
- CPU: Intel i5 or equivalent
- RAM: 4GB
- Python 3.8+

### Recommended
- CPU: Intel i7 or equivalent
- RAM: 8GB
- GPU: NVIDIA CUDA-capable (optional)
- Python 3.10+

## Logs

Logs are saved to `smartsurveillance.log` and printed to console with the following format:
```
2024-01-01 12:00:00,000 - module_name - INFO - Message
```

## Development

### Code Style
- Follow PEP 8
- Use type hints
- Document public functions

### Adding New Components

1. Create module in `src/`
2. Add unit tests in `tests/`
3. Integrate with orchestrator
4. Update documentation

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues and feature requests, please use the GitHub Issues page.

## Authors

Your Name and Contributors

## Acknowledgments

- YOLOv8 by Ultralytics
- OpenCV community
- PyQt5 framework
- All open-source contributors
