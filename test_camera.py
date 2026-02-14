import cv2

for idx in range(3):
    print(f"Testing camera index {idx}...")
    cap = cv2.VideoCapture(idx)
    opened = cap.isOpened()
    print(f"  opened: {opened}")
    if opened:
        ret, frame = cap.read()
        print(f"  read ret: {ret}, frame type: {type(frame)}")
        cap.release()
    print()
