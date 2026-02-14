# Getting Started with SmartSurveillance

Complete setup and usage guide for the SmartSurveillance system.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Webcam or video file for input
- ~4GB of disk space for YOLOv8 models

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/SmartSurveillance.git
cd SmartSurveillance
```

### Step 2: Create Virtual Environment

Create an isolated Python environment:

```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- OpenCV (`opencv-python`)
- YOLOv8 (`ultralytics`)
- PyTorch (deep learning framework)
- PyQt5 (GUI framework)
- And other dependencies

**Note:** Installation may take 10-15 minutes depending on internet speed.

### Step 5: Verify Installation

Test that everything is installed correctly:

```bash
python -c "import cv2; import torch; import PyQt5; print('All dependencies installed successfully!')"
```

## First Run

### Option 1: GUI Interface (Recommended for First-Time Users)

```bash
python main.py
```

This will launch the PyQt5 application. You should see:
- A window titled "SmartSurveillance - Real-Time Detection"
- Control tabs on the right side
- A black video display area (until you connect a camera)

### Option 2: Console Mode

```bash
python console_example.py
```

This runs the system without GUI. Press `Ctrl+C` to stop.

## Configuration

### Basic Configuration File

Edit `config.json` to customize settings:

```json
{
    "camera": {
        "source": 0,           // 0 = default webcam
        "width": 1280,
        "height": 720,
        "fps": 30
    },
    "detection": {
        "model_name": "yolov8n.pt",    // nano model (fastest)
        "confidence_threshold": 0.5,    // 50% confidence minimum
        "target_classes": ["person"],   // what to detect
        "save_alert_frames": true,
        "alert_frame_dir": "alerts"
    },
    "alert": {
        "enable_email": false,          // set to true to enable
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "your-email@gmail.com",
        "sender_password": "your-app-password",
        "recipient_emails": ["recipient@example.com"],
        "alert_cooldown_seconds": 30
    }
}
```

## Using the GUI

### Camera Tab
1. Select your camera source:
   - "Webcam (0)" for default camera
   - "USB Camera (1)" for external camera
   - "Video File" for pre-recorded video
2. Click "Start" to begin

### Detection Tab
1. **YOLOv8 Model:** Choose model based on your hardware
   - `yolov8n.pt` - Nano (fastest, least accurate) - CPU recommended
   - `yolov8s.pt` - Small
   - `yolov8m.pt` - Medium
   - `yolov8l.pt` - Large (slowest, most accurate)

2. **Target Classes:** Enter classes to detect (default: "person")
   - Other options: "car", "dog", "cat", "bicycle", etc.
   - Separate multiple with commas

3. **Confidence Threshold:** Adjust detection sensitivity
   - Lower = more detections (more false positives)
   - Higher = fewer detections (more false negatives)
   - Recommended: 0.4-0.6

4. **Alert Cooldown:** Prevent repeated alerts
   - Minimum time between alerts for same detection
   - Recommended: 30 seconds

5. Click "Update Settings" to apply changes

### Alerts Tab (Email Configuration)

#### Step 1: Enable Email Alerts
Check "Enable Email Alerts"

#### Step 2: Gmail Setup (if using Gmail)
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Factor Authentication
3. Generate [App Password](https://support.google.com/accounts/answer/185833)
4. Use the 16-character password in the application

#### Step 3: Configure
1. **Sender Email:** Your email address
2. **Sender Password:** Your app password (Gmail) or email password
3. **Recipients:** Comma-separated list of recipient emails

#### Step 4: Test
Click "Send Test Alert" to verify configuration

### Statistics Tab
View:
- System status (Running/Stopped)
- Total detections
- Alert history
- Current configuration

## Troubleshooting

### Issue: "No module named 'PyQt5'"

**Solution:** Reinstall dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Black screen or "No video source"

1. Check camera is connected
2. Try different camera index:
   - Open GUI and change camera source
   - Or modify `config.json` camera.source (try 0, 1, 2, etc.)
3. On Linux, check permissions:
   ```bash
   sudo usermod -a -G video $USER
   ```

### Issue: Very slow detection

**Solutions:**
1. Use smaller YOLOv8 model (yolov8n.pt)
2. Lower video resolution in config.json
3. Reduce FPS in config.json
4. Check CPU usage (might be limited)

### Issue: "Failed to load model"

**Solution:**
```bash
pip install --upgrade ultralytics torch
```

### Issue: Email alerts not sending

1. **Check credentials:**
   - Verify email and password are correct
   - For Gmail, use App Password (not regular password)

2. **Firewall/Network:**
   - Check internet connection
   - Check if firewall blocks SMTP port 587

3. **Test SMTP:**
   ```bash
   python -c "
   import smtplib
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login('your-email@gmail.com', 'your-password')
   print('SMTP connection successful')
   server.quit()
   "
   ```

## YOLOv8 Model Selection

| Model | Size | Speed (CPU) | Accuracy | Recommended For |
|-------|------|------------|----------|-----------------|
| nano  | 3.2M | 50ms       | Good     | Real-time (CPU) |
| small | 9.1M | 100ms      | Better   | Real-time       |
| medium| 25.9M| 250ms      | Very Good| Balanced        |
| large | 52.7M| 600ms      | Excellent| Accuracy focus  |
| xlarge| 134.3M| 1500ms    | Best     | GPU only        |

## Performance Tips

1. **For CPU Systems:**
   - Use yolov8n.pt (nano)
   - Lower resolution (640x480)
   - Reduce FPS (15)
   - Increase confidence threshold (0.6)

2. **For GPU Systems:**
   - Can use larger models
   - Higher resolution
   - GPU utilization improves speed significantly

3. **General Tips:**
   - Good lighting improves detection
   - Keep camera clean
   - Adequate ventilation for cooling
   - Close unnecessary applications

## Advanced Configuration

### Using Different SMTP Servers

**Gmail:**
```json
"smtp_server": "smtp.gmail.com",
"smtp_port": 587
```

**Outlook:**
```json
"smtp_server": "smtp-mail.outlook.com",
"smtp_port": 587
```

**Custom SMTP:**
```json
"smtp_server": "your-smtp-server.com",
"smtp_port": 587
```

### Detecting Multiple Object Classes

Edit `config.json` or use GUI:
```json
"target_classes": ["person", "car", "dog", "motorcycle"]
```

Available COCO classes:
person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, traffic light, fire hydrant, stop sign, parking meter, bench, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe, backpack, umbrella, handbag, tie, suitcase, frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake, chair, couch, potted plant, bed, dining table, toilet, tv, laptop, mouse, remote, keyboard, microwave, oven, toaster, sink, refrigerator, book, clock, vase, scissors, teddy bear, hair drier, toothbrush

## Running Tests

```bash
pytest tests/
```

With coverage report:
```bash
pytest --cov=src tests/
```

## Docker Deployment

### Build Docker Image

```bash
docker build -t smartsurveillance .
```

### Run with Docker

```bash
docker-compose up
```

### Stop Container

```bash
docker-compose down
```

## System Requirements

### Minimum
- CPU: Intel i5 or equivalent
- RAM: 4GB
- Storage: 4GB
- Python 3.8+

### Recommended
- CPU: Intel i7 or higher
- RAM: 8GB
- Storage: 8GB SSD
- GPU: NVIDIA CUDA-capable (optional)
- Python 3.10+

### For GPU Acceleration

1. Install NVIDIA CUDA Toolkit
2. Install cuDNN
3. Update PyTorch:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

## Next Steps

1. ✅ Installation complete
2. ✅ First run successful
3. 📝 Configure for your use case
4. 🎯 Set up email alerts
5. 📊 Monitor system performance
6. 🔧 Tune detection parameters

## Support

- Check logs in `smartsurveillance.log`
- Review GitHub Issues
- Check detailed README.md
- Test with console_example.py

## Learning Resources

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [OpenCV Tutorials](https://docs.opencv.org/)
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [PyTorch Documentation](https://pytorch.org/docs/)

Happy Surveillance! 🎥
