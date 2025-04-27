import cv2
from pyzbar.pyzbar import decode
import time

def scan_qr():
    """Generator that yields scanned QR code data or manually entered registration IDs"""
    cap = cv2.VideoCapture(0)  # Try camera 0 by default
    
    if not cap.isOpened():
        print("Could not open camera 0, trying camera 1...")
        cap = cv2.VideoCapture(1)
    
    if not cap.isOpened():
        print("Warning: Could not open camera. Running in manual mode only.")
    
    print("\nBTF Attendance Scanner")
    print("-------------------------")
    print("Scan QR code or enter registration ID manually")
    print("Press 'm' to enter manual mode")
    print("Press 'q' to quit the scanner")
    
    manual_mode = False
    
    try:
        while True:
            if not manual_mode and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("Failed to grab frame. Switching to manual mode.")
                    manual_mode = True
                    continue
                
                # Process frame
                decoded = decode(frame)
                if decoded:
                    reg_id = decoded[0].data.decode('utf-8')
                    print(f"\nScanned: {reg_id}")
                    
                    # Display success indicator
                    cv2.putText(frame, f"Scanned: {reg_id}", (30, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.imshow('BTF Scanner', frame)
                    cv2.waitKey(1500)  # Display for 1.5 seconds
                    
                    yield reg_id
                
                # Display scanner window
                cv2.putText(frame, "Press 'm' for manual entry", (30, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.imshow('BTF Scanner', frame)
                
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
                elif key == ord('m'):
                    manual_mode = True
            
            # Manual registration mode
            if manual_mode:
                reg_id = input("\nEnter registration ID (or 'q' to quit, 'c' to continue scanning): ")
                
                if reg_id.lower() == 'q':
                    break
                elif reg_id.lower() == 'c':
                    manual_mode = False
                    continue
                elif reg_id.strip():
                    print(f"Processing registration ID: {reg_id}")
                    yield reg_id.strip()
    
    finally:
        if cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
