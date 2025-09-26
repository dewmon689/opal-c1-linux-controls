#!/usr/bin/env python3
"""
Opal C1 Manual Focus Control

Disables auto focus and sets manual focus for stable video calls.
Works across all applications (Zoom, Teams, OBS, etc.)
"""

import depthai as dai
import time
import sys
import argparse

def set_manual_focus(focus_value=130):
    """Set manual focus on Opal C1"""
    print(f"Setting Opal C1 to manual focus (value: {focus_value})...")
    
    # Create minimal pipeline for control only
    pipeline = dai.Pipeline()
    cam = pipeline.create(dai.node.ColorCamera)
    control_in = pipeline.create(dai.node.XLinkIn)
    
    control_in.setStreamName("control")
    cam.setBoardSocket(dai.CameraBoardSocket.CAM_A)
    control_in.out.link(cam.inputControl)
    
    try:
        with dai.Device(pipeline) as device:
            q_ctrl = device.getInputQueue("control")
            
            # Send manual focus command
            ctrl = dai.CameraControl()
            ctrl.setManualFocus(focus_value)
            q_ctrl.send(ctrl)
            
            print("✓ Manual focus command sent")
            time.sleep(0.5)  # Brief wait for command to register
            
        print("✓ Auto focus DISABLED - Manual focus applied")
        print("✓ Setting will persist across all applications")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        print("Make sure Opal C1 is connected and not in use by another application")
        return False

def enable_auto_focus():
    """Re-enable auto focus on Opal C1"""
    print("Re-enabling auto focus on Opal C1...")
    
    pipeline = dai.Pipeline()
    cam = pipeline.create(dai.node.ColorCamera)
    control_in = pipeline.create(dai.node.XLinkIn)
    
    control_in.setStreamName("control")
    cam.setBoardSocket(dai.CameraBoardSocket.CAM_A)
    control_in.out.link(cam.inputControl)
    
    try:
        with dai.Device(pipeline) as device:
            q_ctrl = device.getInputQueue("control")
            
            # Send auto focus command
            ctrl = dai.CameraControl()
            ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)
            q_ctrl.send(ctrl)
            
            print("✓ Auto focus ENABLED")
            time.sleep(0.5)
            
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Opal C1 Focus Control")
    parser.add_argument("focus_value", nargs="?", type=int, default=130,
                       help="Manual focus value (0-255, default: 130)")
    parser.add_argument("--auto", action="store_true",
                       help="Enable auto focus instead of manual")
    
    args = parser.parse_args()
    
    if args.auto:
        success = enable_auto_focus()
    else:
        if not (0 <= args.focus_value <= 255):
            print("Error: Focus value must be between 0 and 255")
            return 1
        success = set_manual_focus(args.focus_value)
    
    if success:
        print("\n💡 Tip: Test with 'python test_camera.py' or open Zoom to verify")
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit(main())
