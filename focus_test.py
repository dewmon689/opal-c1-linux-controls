#!/usr/bin/env python3
"""
Focus Test - Visual feedback for focus changes

Shows live camera feed with focus instructions to help test settings.
"""

import cv2
import time

def focus_test():
    """Test focus with visual feedback"""
    print("Focus Test - Visual Feedback")
    print("=" * 40)
    
    cap = cv2.VideoCapture(2)
    if not cap.isOpened():
        print("✗ Cannot open Opal C1 camera")
        return False
        
    print("✓ Camera opened")
    print("\nFocus Test Instructions:")
    print("1. Hold text/object at arm's length (2-3 feet)")
    print("2. Use GUI to change focus settings")
    print("3. Watch for sharpness changes in this window")
    print("4. Press 'q' to quit test")
    print("\nTip: Try focus values 50 (close), 130 (medium), 200 (far)")
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Add helpful overlay
        height, width = frame.shape[:2]
        
        # Add focus test overlay
        cv2.rectangle(frame, (10, 10), (width-10, 120), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (width-10, 120), (0, 255, 0), 2)
        
        cv2.putText(frame, "FOCUS TEST - Watch text sharpness", 
                   (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Hold text at arm's length", 
                   (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, "Use GUI to change focus - Press 'q' to quit", 
                   (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Add center crosshair for focus reference
        center_x, center_y = width // 2, height // 2
        cv2.line(frame, (center_x - 20, center_y), (center_x + 20, center_y), (0, 255, 0), 2)
        cv2.line(frame, (center_x, center_y - 20), (center_x, center_y + 20), (0, 255, 0), 2)
        
        # Frame counter for reference
        cv2.putText(frame, f"Frame: {frame_count}", 
                   (width - 150, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow("Opal C1 Focus Test", frame)
        
        frame_count += 1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Focus test completed")
    return True

if __name__ == "__main__":
    focus_test()
