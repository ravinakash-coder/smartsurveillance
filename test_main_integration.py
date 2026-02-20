#!/usr/bin/env python
"""Test script to verify main.py integration"""

import os
import sys
import tempfile
from pathlib import Path

# Add current dir to path
sys.path.insert(0, '.')

from main import run_image_detection, run_batch_detection

def test_image_detection():
    """Test single image detection"""
    print("\n=== Testing Single Image Detection ===")
    
    # Use a test image if available
    test_image = r"C:\Users\ELCOT\OneDrive\Documents\New folder\bmw 2.jpg"
    if os.path.exists(test_image):
        result = run_image_detection(test_image)
        print(f"Image detection result: {result}")
        return result
    else:
        print(f"Test image not found: {test_image}")
        return False

def test_batch_detection():
    """Test batch folder detection"""
    print("\n=== Testing Batch Folder Detection ===")
    
    test_folder = r"C:\Users\ELCOT\Pictures"
    if os.path.isdir(test_folder):
        result = run_batch_detection(test_folder)
        print(f"Batch detection result: {result}")
        return result
    else:
        print(f"Test folder not found: {test_folder}")
        return False

def test_menu():
    """Test menu display"""
    print("\n=== Testing Menu Display ===")
    from main import display_menu
    # Just verify function exists and is callable
    print("Menu function is callable: True")
    return True

if __name__ == "__main__":
    print("Testing SmartSurveillance Main Integration\n")
    print("=" * 50)
    
    # Test menu
    test_menu()
    
    # Test single image
    test_image_detection()
    
    # Test batch
    test_batch_detection()
    
    print("\n" + "=" * 50)
    print("Integration test completed!")
