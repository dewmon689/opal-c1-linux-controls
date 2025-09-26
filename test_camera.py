#!/usr/bin/env python3
"""
Opal C1 Camera Test

Simple test to verify camera is working and check focus behavior.
"""

import cv2
import sys

def test_camera():
    """Test Opal C1 camera via UVC interface"""
    print("Testing Opal C1 camera...")
    
    # Try different video devices
    for device_id in [2, 0, 1, 3]:
        print(f"Trying /dev/video{device_id}...")
        cap = cv2.VideoCapture(device_id)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                height, width = frame.shape[:2]
                print(f"✓ Camera found on video{device_id}: {width}x{height}")
                
                if width == 1280 and height == 720:
                    print("✓ This appears to be the Opal C1 (1280x720)")
                    
                    print("\nCamera test window opened.")
                    print("- Move objects at different distances to test focus")
                    print("- Press 'q' to quit")
                    
                    while True:
                        ret, frame = cap.read()
                        if ret:
                            # Add info overlay
                            cv2.putText(frame, f"Opal C1 Test - video{device_id}", 
                                      (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            cv2.putText(frame, "Press 'q' to quit", 
                                      (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                            
                            cv2.imshow("Opal C1 Test", frame)
                            
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    
                    cap.release()
                    cv2.destroyAllWindows()
                    return True
                else:
                    print(f"  Different camera detected: {width}x{height}")
                    cap.release()
            else:
                print(f"  No video signal from video{device_id}")
                cap.release()
        else:
            print(f"  Cannot open video{device_id}")
    
    print("✗ Opal C1 not found")
    print("Make sure the camera is connected and not in use by another application")
    return False

def main():
    try:
        success = test_camera()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        cv2.destroyAllWindows()
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
