#!/usr/bin/env python3
"""
Opal C1 GUI Controls

Simple graphical interface for controlling Opal C1 camera settings.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import depthai as dai
import threading
import time

class OpalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Opal C1 Controls")
        self.root.geometry("400x300")
        
        # Current settings
        self.auto_focus_enabled = True
        self.current_focus = 130
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Opal C1 Camera Controls", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Focus controls
        focus_frame = ttk.LabelFrame(main_frame, text="Focus Control", padding="10")
        focus_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Auto focus toggle - clearer ON/OFF switch
        toggle_frame = ttk.Frame(focus_frame)
        toggle_frame.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(toggle_frame, text="Auto Focus:").pack(side=tk.LEFT)
        
        self.auto_focus_var = tk.BooleanVar(value=True)
        self.toggle_button = ttk.Button(toggle_frame, text="ON", width=6,
                                       command=self.toggle_auto_focus)
        self.toggle_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Manual focus slider
        ttk.Label(focus_frame, text="Manual Focus:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        self.focus_var = tk.IntVar(value=130)
        self.focus_scale = ttk.Scale(focus_frame, from_=0, to=255, 
                                    variable=self.focus_var, orient=tk.HORIZONTAL)
        self.focus_scale.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Bind the scale change event properly
        self.focus_scale.bind("<Motion>", self.on_focus_drag)
        self.focus_scale.bind("<ButtonRelease-1>", self.on_focus_release)
        
        self.focus_value_label = ttk.Label(focus_frame, text="130")
        self.focus_value_label.grid(row=2, column=1, padx=(10, 0))
        
        # Initially disable manual focus
        self.focus_scale.configure(state="disabled")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Apply Settings", 
                  command=self.apply_settings).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Test Camera", 
                  command=self.test_camera).pack(side=tk.LEFT)
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                foreground="blue")
        status_label.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        focus_frame.columnconfigure(0, weight=1)
        
    def toggle_auto_focus(self):
        """Toggle between auto and manual focus"""
        # Toggle the state
        self.auto_focus_enabled = not self.auto_focus_enabled
        
        if self.auto_focus_enabled:
            self.focus_scale.configure(state="disabled")
            self.toggle_button.configure(text="ON")
            self.status_var.set("Auto focus enabled")
            self.apply_auto_focus()
        else:
            self.focus_scale.configure(state="normal")
            self.toggle_button.configure(text="OFF")
            self.status_var.set("Manual focus enabled")
            self.apply_focus_only(self.current_focus)
            
    def on_focus_drag(self, event):
        """Update display while dragging"""
        if not self.auto_focus_enabled:
            focus_val = int(self.focus_scale.get())
            self.focus_value_label.config(text=str(focus_val))
            self.current_focus = focus_val
            
    def on_focus_release(self, event):
        """Apply focus when slider is released"""
        if not self.auto_focus_enabled:
            focus_val = int(self.focus_scale.get())
            self.focus_value_label.config(text=str(focus_val))
            self.current_focus = focus_val
            self.apply_focus_only(focus_val)
        
    def apply_settings(self):
        """Apply camera settings"""
        def apply_in_thread():
            try:
                self.status_var.set("Applying settings...")
                self.root.update()
                
                # Create depthai pipeline for controls
                pipeline = dai.Pipeline()
                cam = pipeline.create(dai.node.ColorCamera)
                control_in = pipeline.create(dai.node.XLinkIn)
                
                control_in.setStreamName("control")
                cam.setBoardSocket(dai.CameraBoardSocket.CAM_A)
                control_in.out.link(cam.inputControl)
                
                with dai.Device(pipeline) as device:
                    q_ctrl = device.getInputQueue("control")
                    ctrl = dai.CameraControl()
                    
                    if self.auto_focus_enabled:
                        ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)
                        self.status_var.set("✓ Auto focus enabled")
                    else:
                        ctrl.setManualFocus(self.current_focus)
                        self.status_var.set(f"✓ Manual focus set to {self.current_focus}")
                    
                    q_ctrl.send(ctrl)
                    time.sleep(0.5)
                    
            except Exception as e:
                self.status_var.set(f"✗ Error: {str(e)}")
                
        # Run in separate thread to avoid blocking UI
        threading.Thread(target=apply_in_thread, daemon=True).start()
        
    def apply_focus_only(self, focus_value):
        """Apply just focus setting quickly"""
        def apply_in_thread():
            try:
                self.status_var.set(f"Setting focus to {focus_value}...")
                
                pipeline = dai.Pipeline()
                cam = pipeline.create(dai.node.ColorCamera)
                control_in = pipeline.create(dai.node.XLinkIn)
                
                control_in.setStreamName("control")
                cam.setBoardSocket(dai.CameraBoardSocket.CAM_A)
                control_in.out.link(cam.inputControl)
                
                with dai.Device(pipeline) as device:
                    q_ctrl = device.getInputQueue("control")
                    ctrl = dai.CameraControl()
                    ctrl.setManualFocus(focus_value)
                    q_ctrl.send(ctrl)
                    time.sleep(0.2)
                    
                self.status_var.set(f"✓ Manual focus: {focus_value}")
                    
            except Exception as e:
                self.status_var.set(f"✗ Error: {str(e)[:30]}")
                
        threading.Thread(target=apply_in_thread, daemon=True).start()
        
    def apply_auto_focus(self):
        """Apply auto focus setting"""
        def apply_in_thread():
            try:
                self.status_var.set("Enabling auto focus...")
                
                pipeline = dai.Pipeline()
                cam = pipeline.create(dai.node.ColorCamera)
                control_in = pipeline.create(dai.node.XLinkIn)
                
                control_in.setStreamName("control")
                cam.setBoardSocket(dai.CameraBoardSocket.CAM_A)
                control_in.out.link(cam.inputControl)
                
                with dai.Device(pipeline) as device:
                    q_ctrl = device.getInputQueue("control")
                    ctrl = dai.CameraControl()
                    ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)
                    q_ctrl.send(ctrl)
                    time.sleep(0.2)
                    
                self.status_var.set("✓ Auto focus enabled")
                    
            except Exception as e:
                self.status_var.set(f"✗ Error: {str(e)[:30]}")
                
        threading.Thread(target=apply_in_thread, daemon=True).start()
        
    def test_camera(self):
        """Launch focus test"""
        import subprocess
        import os
        
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            test_script = os.path.join(script_dir, "focus_test.py")
            
            if os.path.exists(test_script):
                subprocess.Popen(["python3", test_script])
                self.status_var.set("Focus test launched - Watch for sharpness changes")
            else:
                # Fallback to original test
                test_script = os.path.join(script_dir, "test_camera.py")
                if os.path.exists(test_script):
                    subprocess.Popen(["python3", test_script])
                    self.status_var.set("Camera test launched")
                else:
                    messagebox.showwarning("Warning", "Test scripts not found")
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch test: {e}")

def main():
    root = tk.Tk()
    app = OpalGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
