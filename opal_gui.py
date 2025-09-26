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
        
        # Auto focus toggle
        self.auto_focus_var = tk.BooleanVar(value=True)
        auto_focus_check = ttk.Checkbutton(focus_frame, text="✓ Auto Focus Enabled", 
                                          variable=self.auto_focus_var,
                                          command=self.toggle_auto_focus)
        auto_focus_check.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        self.auto_focus_check = auto_focus_check
        
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
        auto_enabled = self.auto_focus_var.get()
        
        if auto_enabled:
            self.focus_scale.configure(state="disabled")
            self.auto_focus_check.configure(text="✓ Auto Focus Enabled")
        else:
            self.focus_scale.configure(state="normal")
            self.auto_focus_check.configure(text="✗ Manual Focus")
            
        self.auto_focus_enabled = auto_enabled
        
        # Apply the change immediately
        if auto_enabled:
            self.apply_auto_focus()
        else:
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
                    
            except Exception:
                pass  # Fail silently for real-time updates
                
        threading.Thread(target=apply_in_thread, daemon=True).start()
        
    def apply_auto_focus(self):
        """Apply auto focus setting"""
        def apply_in_thread():
            try:
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
                    
            except Exception:
                pass
                
        threading.Thread(target=apply_in_thread, daemon=True).start()
        
    def test_camera(self):
        """Launch camera test"""
        import subprocess
        import os
        
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            test_script = os.path.join(script_dir, "test_camera.py")
            
            if os.path.exists(test_script):
                subprocess.Popen(["python3", test_script])
                self.status_var.set("Camera test launched")
            else:
                messagebox.showwarning("Warning", "test_camera.py not found")
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch camera test: {e}")

def main():
    root = tk.Tk()
    app = OpalGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
