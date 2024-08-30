import cv2

def initialize_camera(camera_id):
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    return cap

def capture_frame(cap):
    ret, frame = cap.read()
    if not ret:
        return None
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return hsv

def release_camera(cap):
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_id = 1  # 啟動相機
    cap = initialize_camera(camera_id)
    while True:
        frame = capture_frame(cap)
        if frame is None:
            break
        # 在這裡處理你的圖像或顯示 (例如: cv2.imshow('frame', frame))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    release_camera(cap)