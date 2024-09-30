import cv2
import mediapipe as mp
import queue

class Camera:
    def __init__(self, camera_id=0):
        # 初始化攝像頭設定
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    def capture_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        # 轉換顏色遮罩
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return hsv, rgb
    
    
    def release_camera(self):
        # 釋放攝像頭
        self.cap.release()

class TrackGreenBall:
    def __init__(self):
        self.move_command = f"0 0 35\n"
        self.stable_frames = 0  # 記錄穩定幀數
        self.stability_threshold = 3  # 設定穩定幀數的閾值 (降低以加快反應速度)
        self.last_x, self.last_y = 0, 0

    def track_green_ball(self, hsv):
        # 設定顏色區間
        lower_green = (25, 60, 160)
        upper_green = (85, 255, 220)

        mask = cv2.inRange(hsv, lower_green, upper_green)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            if radius > 10:
                angle_x = 15 + int(int(x) / 640 * 150)  # 調整解析度後的比例
                angle_y = 15 + int(int(y) / 480 * 150)
                output_x = -1 if angle_x > 110 else (0 if angle_x > 70 else 1)
                output_y = 1 if angle_y > 110 else (0 if angle_y > 70 else -1)

                # 檢查球的位置是否穩定
                if abs(self.last_x - x) < 10 and abs(self.last_y - y) < 10:
                    self.stable_frames += 1
                else:
                    self.stable_frames = 0

                if self.stable_frames > self.stability_threshold:
                    self.move_command =  f"{output_x} {output_y} {int(radius)}\n"
                else:
                    self.move_command = f"0 0 35\n"

                self.last_x, self.last_y = x, y
            else:
                self.move_command = f"0 0 35\n"
        else:
            self.move_command = f"0 0 35\n"
        return self.move_command

class AppGestureRecognizer:
    def __init__(self, model_path):
        self.model_path = model_path
        
        self.timestamp = 0
        self.result_queue = queue.Queue(1)

        
        self.init_gesture_recognizer()

    def print_result(self,result, output_image, timestamp_ms):
        top_gesture = ""
        if len(result.gestures) > 0:
            top_gesture = result.gestures[0][0].category_name
        self.result_queue.put((top_gesture,))

    def init_gesture_recognizer(self):
        BaseOptions = mp.tasks.BaseOptions
        GestureRecognizer = mp.tasks.vision.GestureRecognizer
        GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        with open(self.model_path, 'rb') as model: # 建立檔案和程式碼的通道
            model_file = model.read()

        options = GestureRecognizerOptions(
            base_options = BaseOptions(model_asset_buffer=model_file),
            running_mode = VisionRunningMode.LIVE_STREAM, # 用於直播模式
            result_callback = self.print_result
        )
        self.recognizer = GestureRecognizer.create_from_options(options)
    

    def gesture_recognizer(self, frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        self.recognizer.recognize_async(mp_image, self.timestamp)
        self.timestamp = self.timestamp + 1
        text = self.result_queue.get()[0]
        print(text)
        return text

    


if __name__ == "__main__":
    camera_id = 0
    model_path = "./models/gesture_recognizer.task"
    cap = Camera(camera_id)
    track_ball = TrackGreenBall()
    recognize = AppGestureRecognizer(model_path)
    while True:
        hsv, frame = cap.capture_frame()
        track_ball_result = track_ball.track_green_ball(hsv)
        recognize_result = recognize.gesture_recognizer(frame)

        print(track_ball_result)
        print(recognize_result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release_camera(cap)
    
