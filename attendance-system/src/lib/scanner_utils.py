import cv2
from pyzbar.pyzbar import decode

def scan_qr():
    cap = cv2.VideoCapture(1)
    while True:
        _, frame = cap.read()
        decoded = decode(frame)
        if decoded:
            yield decoded[0].data.decode('utf-8')
            cv2.waitKey(1500)
        cv2.imshow('BTF Scanner', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
