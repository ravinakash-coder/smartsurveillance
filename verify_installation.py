#!/usr/bin/env python
"""
System Verification Script
Checks if SmartSurveillance is properly installed and ready to run
"""

import sys
import subprocess
from pathlib import Path

class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"{Colors.GREEN}✓{Colors.END} Python {version.major}.{version.minor} (Required: 3.8+)")
        return True
    else:
        print(f"{Colors.RED}✗{Colors.END} Python {version.major}.{version.minor} (Required: 3.8+)")
        return False


def check_package(package_name, import_name=None):
    """Check if a Python package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"{Colors.GREEN}✓{Colors.END} {package_name}")
        return True
    except ImportError:
        print(f"{Colors.RED}✗{Colors.END} {package_name} (not installed)")
        return False


def check_dependencies():
    """Check all required dependencies"""
    print("Checking Python dependencies...")
    
    packages = [
        ("OpenCV", "cv2"),
        ("NumPy", "numpy"),
        ("PyTorch", "torch"),
        ("TorchVision", "torchvision"),
        ("Ultralytics (YOLOv8)", "ultralytics"),
        ("PyQt5", "PyQt5"),
    ]
    
    results = []
    for package, import_name in packages:
        results.append(check_package(package, import_name))
    
    return all(results)


def check_project_structure():
    """Check if project structure is correct"""
    print("\nChecking project structure...")
    
    required_dirs = [
        "src",
        "tests",
        "Doc"
    ]
    
    required_files = [
        "main.py",
        "config.json",
        "requirements.txt",
        "README.md",
        ".gitignore"
    ]
    
    all_good = True
    
    for directory in required_dirs:
        if Path(directory).is_dir():
            print(f"{Colors.GREEN}✓{Colors.END} Directory: {directory}")
        else:
            print(f"{Colors.RED}✗{Colors.END} Directory: {directory} (missing)")
            all_good = False
    
    for filename in required_files:
        if Path(filename).is_file():
            print(f"{Colors.GREEN}✓{Colors.END} File: {filename}")
        else:
            print(f"{Colors.YELLOW}!{Colors.END} File: {filename} (missing)")
    
    return all_good


def check_source_files():
    """Check if source files exist"""
    print("\nChecking source files...")
    
    required_modules = [
        "src/__init__.py",
        "src/frame_grabber.py",
        "src/object_detector.py",
        "src/alert_system.py",
        "src/orchestrator.py",
        "src/config.py",
        "src/gui.py",
        "src/utils.py"
    ]
    
    results = []
    for module in required_modules:
        if Path(module).is_file():
            print(f"{Colors.GREEN}✓{Colors.END} {module}")
            results.append(True)
        else:
            print(f"{Colors.RED}✗{Colors.END} {module} (missing)")
            results.append(False)
    
    return all(results)


def check_camera():
    """Check if camera is accessible"""
    print("\nChecking camera access...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print(f"{Colors.GREEN}✓{Colors.END} Camera (index 0) is accessible")
            cap.release()
            return True
        else:
            print(f"{Colors.YELLOW}!{Colors.END} Camera (index 0) not found (this is OK if you plan to use video files)")
            return False
    except Exception as e:
        print(f"{Colors.YELLOW}!{Colors.END} Camera check skipped: {e}")
        return False


def check_model_files():
    """Check if YOLOv8 models are downloaded"""
    print("\nChecking YOLOv8 models...")
    
    try:
        from pathlib import Path as PathlibPath
        home = str(PathlibPath.home())
        yolo_dir = PathlibPath(home) / ".ultralytics"
        
        if yolo_dir.exists():
            models = list(yolo_dir.glob("*.pt"))
            if models:
                print(f"{Colors.GREEN}✓{Colors.END} YOLOv8 models directory found")
                print(f"  Models available: {len(models)}")
                return True
            else:
                print(f"{Colors.YELLOW}!{Colors.END} YOLOv8 models not downloaded yet")
                print("  Models will auto-download on first run")
                return False
        else:
            print(f"{Colors.YELLOW}!{Colors.END} YOLOv8 models not downloaded yet")
            print("  Models will auto-download on first run (~5-50MB depending on model)")
            return False
    except Exception as e:
        print(f"{Colors.YELLOW}!{Colors.END} Model check error: {e}")
        return False


def check_disk_space():
    """Check available disk space"""
    print("\nChecking disk space...")
    try:
        import shutil
        stat = shutil.disk_usage("/")
        free_gb = stat.free / (1024**3)
        
        if free_gb > 2:
            print(f"{Colors.GREEN}✓{Colors.END} Available disk space: {free_gb:.1f} GB")
            return True
        else:
            print(f"{Colors.YELLOW}!{Colors.END} Low disk space: {free_gb:.1f} GB (minimum 2GB recommended)")
            return False
    except Exception as e:
        print(f"{Colors.YELLOW}!{Colors.END} Disk space check skipped: {e}")
        return False


def check_pytorch_gpu():
    """Check if PyTorch can use GPU"""
    print("\nChecking GPU support...")
    try:
        import torch
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            print(f"{Colors.GREEN}✓{Colors.END} GPU available: {device_name}")
            return True
        else:
            print(f"{Colors.YELLOW}!{Colors.END} GPU not available (CPU mode will be used)")
            return False
    except Exception as e:
        print(f"{Colors.YELLOW}!{Colors.END} GPU check skipped: {e}")
        return False


def suggest_fixes(failed_checks):
    """Suggest fixes for failed checks"""
    if not failed_checks:
        return
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}Suggested fixes:{Colors.END}")
    
    if "dependencies" in failed_checks:
        print(f"\n{Colors.BOLD}Install dependencies:{Colors.END}")
        print(f"  pip install -r requirements.txt")
    
    if "project_structure" in failed_checks:
        print(f"\n{Colors.BOLD}Create missing directories:{Colors.END}")
        print(f"  mkdir -p src tests Doc")
    
    if "camera" in failed_checks:
        print(f"\n{Colors.BOLD}Camera setup:{Colors.END}")
        print(f"  - Connect a USB camera")
        print(f"  - Or use a video file with 'Video File' option")
        print(f"  - On Linux: set permissions with: sudo usermod -a -G video $USER")
    
    print()


def run_test():
    """Try to run a simple test"""
    print("\nRunning basic functionality test...")
    try:
        from src.orchestrator import SurveillanceOrchestrator
        orchestrator = SurveillanceOrchestrator()
        print(f"{Colors.GREEN}✓{Colors.END} Orchestrator initialized successfully")
        
        stats = orchestrator.get_stats()
        print(f"{Colors.GREEN}✓{Colors.END} System ready to use")
        return True
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.END} Error: {e}")
        return False


def main():
    """Run all checks"""
    print_header("SmartSurveillance System Verification")
    
    failed_checks = []
    
    # Check Python version
    if not check_python_version():
        print(f"{Colors.RED}FATAL: Python 3.8+ is required{Colors.END}\n")
        return 1
    
    # Check dependencies
    if not check_dependencies():
        failed_checks.append("dependencies")
        print(f"\n{Colors.RED}Some dependencies are missing{Colors.END}")
    
    # Check project structure
    if not check_project_structure():
        failed_checks.append("project_structure")
    
    # Check source files
    if not check_source_files():
        failed_checks.append("source_files")
    
    # Check camera
    check_camera()
    
    # Check models
    check_model_files()
    
    # Check disk space
    check_disk_space()
    
    # Check GPU
    check_pytorch_gpu()
    
    # Try to run basic test
    if not failed_checks:
        run_test()
    
    # Summary
    print_header("Verification Summary")
    
    if failed_checks:
        print(f"{Colors.RED}Status: INCOMPLETE{Colors.END}")
        print(f"\nFailed checks: {', '.join(failed_checks)}")
        suggest_fixes(failed_checks)
        return 1
    else:
        print(f"{Colors.GREEN}Status: ALL CHECKS PASSED ✓{Colors.END}")
        print(f"\n{Colors.BOLD}You're ready to run SmartSurveillance!{Colors.END}")
        print(f"\nStart the application with:")
        print(f"  python main.py          # GUI mode")
        print(f"  python console_example.py  # Console mode\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
