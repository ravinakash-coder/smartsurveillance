"""
SmartSurveillance GUI Application - Real-time detection with modern interface
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import logging
from pathlib import Path
from src.object_detector import ObjectDetector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gui_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SmartSurveillanceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartSurveillance - Real-Time Detection")
        self.root.geometry("1280x720")
        self.root.configure(bg="#f0f0f0")
        
        # Application state
        self.detector = None
        self.cap = None
        self.is_running = False
        self.video_source = 0
        self.current_frame = None
        
        # Setup UI
        self.setup_ui()
        
        logger.info("SmartSurveillance GUI started")
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Video display
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Video title
        video_title = ttk.Label(left_panel, text="Live Video Feed", font=("Arial", 12, "bold"))
        video_title.pack(pady=(0, 5))
        
        # Video canvas
        self.video_canvas = tk.Canvas(left_panel, bg="black", width=900, height=600)
        self.video_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Controls
        right_panel = ttk.Frame(main_frame, width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_panel.pack_propagate(False)
        
        # Tabs
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Camera
        self.camera_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.camera_tab, text="Camera")
        self.setup_camera_tab()
        
        # Tab 2: Detection
        self.detection_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.detection_tab, text="Detection")
        self.setup_detection_tab()
        
        # Tab 3: Alerts
        self.alerts_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.alerts_tab, text="Alerts")
        self.setup_alerts_tab()
        
        # Tab 4: Statistics
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="Statistics")
        self.setup_stats_tab()
    
    def setup_camera_tab(self):
        """Setup camera configuration tab"""
        frame = ttk.Frame(self.camera_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Camera source label
        ttk.Label(frame, text="Camera Source:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # Webcam option
        self.source_var = tk.StringVar(value="Webcam (0)")
        ttk.Radiobutton(frame, text="Webcam (0)", variable=self.source_var, 
                       value="Webcam (0)", command=self.on_source_change).pack(anchor=tk.W)
        ttk.Radiobutton(frame, text="Video File", variable=self.source_var, 
                       value="Video File", command=self.on_source_change).pack(anchor=tk.W)
        
        # Video file path
        ttk.Label(frame, text="Path to video file...", font=("Arial", 9)).pack(anchor=tk.W, pady=(10, 0))
        
        video_path_frame = ttk.Frame(frame)
        video_path_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.video_path_var = tk.StringVar()
        ttk.Entry(video_path_frame, textvariable=self.video_path_var, state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(video_path_frame, text="Browse", command=self.browse_video).pack(side=tk.LEFT, padx=(5, 0))
        
        # Control buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        self.start_btn = ttk.Button(button_frame, text="Start", command=self.start_detection)
        self.start_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.stop_btn = ttk.Button(button_frame, text="Stop", command=self.stop_detection, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Status label
        self.status_label = ttk.Label(frame, text="Status: Ready", font=("Arial", 9))
        self.status_label.pack(anchor=tk.W, pady=(10, 0))
    
    def setup_detection_tab(self):
        """Setup detection settings tab"""
        frame = ttk.Frame(self.detection_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Model selection
        ttk.Label(frame, text="Model:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        self.model_var = tk.StringVar(value="yolov8n.pt")
        models = ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt"]
        for model in models:
            ttk.Radiobutton(frame, text=model, variable=self.model_var, value=model).pack(anchor=tk.W)
        
        # Confidence threshold
        ttk.Label(frame, text="Confidence Threshold:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15, 5))
        
        threshold_frame = ttk.Frame(frame)
        threshold_frame.pack(fill=tk.X)
        
        self.confidence_scale = ttk.Scale(threshold_frame, from_=0, to=1, orient=tk.HORIZONTAL)
        self.confidence_scale.set(0.5)
        self.confidence_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.confidence_label = ttk.Label(threshold_frame, text="0.50", font=("Arial", 9))
        self.confidence_label.pack(side=tk.LEFT, padx=(5, 0))
        
        self.confidence_scale.config(command=self.update_confidence_label)
        
        # Detection info
        ttk.Label(frame, text="Detection Info:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(15, 5))
        
        self.detection_text = tk.Text(frame, height=8, width=35, font=("Courier", 9))
        self.detection_text.pack(fill=tk.BOTH, expand=True)
        self.detection_text.config(state=tk.DISABLED)
    
    def setup_alerts_tab(self):
        """Setup alerts tab"""
        frame = ttk.Frame(self.alerts_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Alerts:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        self.alerts_text = tk.Text(frame, height=10, width=35, font=("Courier", 9))
        self.alerts_text.pack(fill=tk.BOTH, expand=True)
        self.alerts_text.config(state=tk.DISABLED)
    
    def setup_stats_tab(self):
        """Setup statistics tab"""
        frame = ttk.Frame(self.stats_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Statistics:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        self.stats_text = tk.Text(frame, height=10, width=35, font=("Courier", 9))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        self.stats_text.config(state=tk.DISABLED)
        
        # Sample stats
        self.update_stats("Frames processed: 0\nObjects detected: 0\nAvg FPS: 0\nUptime: 0s")
    
    def update_confidence_label(self, value):
        """Update confidence threshold label"""
        self.confidence_label.config(text=f"{float(value):.2f}")
    
    def on_source_change(self):
        """Handle video source change"""
        source = self.source_var.get()
        if source == "Webcam (0)":
            self.video_source = 0
            self.video_path_var.set("")
        else:
            self.video_path_var.set("")
    
    def browse_video(self):
        """Browse for video file"""
        from tkinter import filedialog
        filepath = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi *.mov"), ("All files", "*.*")]
        )
        if filepath:
            self.video_path_var.set(filepath)
            self.video_source = filepath
            self.source_var.set("Video File")
    
    def start_detection(self):
        """Start detection"""
        try:
            logger.info(f"Starting detection from source: {self.video_source}")
            
            # Initialize detector
            if self.detector is None:
                self.detector = ObjectDetector(
                    model_name=self.model_var.get(),
                    confidence_threshold=float(self.confidence_scale.get())
                )
            
            # Open video capture
            self.cap = cv2.VideoCapture(self.video_source)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Failed to open video source!")
                return
            
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Running")
            
            # Start detection thread
            detection_thread = threading.Thread(target=self.detection_loop, daemon=True)
            detection_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start detection: {str(e)}")
            logger.error(f"Error starting detection: {e}")
    
    def stop_detection(self):
        """Stop detection"""
        self.is_running = False
        if self.cap:
            self.cap.release()
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped")
        
        logger.info("Detection stopped")
    
    def detection_loop(self):
        """Main detection loop running in separate thread"""
        frame_count = 0
        total_objects = 0
        
        try:
            while self.is_running:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Run detection
                detections = self.detector.detect(frame)
                total_objects += len(detections)
                
                # Draw detections
                output_frame = self.detector.draw_detections(frame, detections)
                
                # Add frame info
                info_text = f"Frame: {frame_count} | Detections: {len(detections)}"
                cv2.putText(output_frame, info_text, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Update canvas
                self.display_frame(output_frame)
                
                # Update detection info
                detection_info = f"Frame: {frame_count}\nDetections: {len(detections)}\n"
                for det in detections:
                    detection_info += f"  • {det.class_name}: {det.confidence:.2f}\n"
                
                self.update_detection_text(detection_info)
                self.update_stats(f"Frames: {frame_count}\nObjects: {total_objects}\nAvg Confidence: {sum(d.confidence for d in detections) / len(detections) if detections else 0:.2f}")
                
                # Small delay to prevent CPU overload
                cv2.waitKey(1)
        
        except Exception as e:
            logger.error(f"Error in detection loop: {e}")
        
        finally:
            self.is_running = False
            self.stop_btn.config(state=tk.DISABLED)
            self.start_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Stopped")
    
    def display_frame(self, frame):
        """Display frame on canvas"""
        try:
            # Resize frame to fit canvas
            h, w = frame.shape[:2]
            canvas_w = self.video_canvas.winfo_width()
            canvas_h = self.video_canvas.winfo_height()
            
            if canvas_w <= 1 or canvas_h <= 1:
                canvas_w, canvas_h = 900, 600
            
            # Calculate aspect ratio
            aspect = w / h
            if canvas_w / canvas_h > aspect:
                new_w = int(canvas_h * aspect)
                new_h = canvas_h
            else:
                new_w = canvas_w
                new_h = int(canvas_w / aspect)
            
            frame = cv2.resize(frame, (new_w, new_h))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PhotoImage
            img = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(img)
            
            # Update canvas
            self.video_canvas.delete("all")
            self.video_canvas.create_image(canvas_w // 2, canvas_h // 2, image=photo)
            self.video_canvas.image = photo
        
        except Exception as e:
            logger.error(f"Error displaying frame: {e}")
    
    def update_detection_text(self, text):
        """Update detection information"""
        self.detection_text.config(state=tk.NORMAL)
        self.detection_text.delete("1.0", tk.END)
        self.detection_text.insert("1.0", text)
        self.detection_text.config(state=tk.DISABLED)
    
    def update_stats(self, text):
        """Update statistics"""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert("1.0", text)
        self.stats_text.config(state=tk.DISABLED)
    
    def on_closing(self):
        """Handle window closing"""
        self.stop_detection()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = SmartSurveillanceGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
