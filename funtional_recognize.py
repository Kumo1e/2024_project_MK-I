import mediapipe as mp
import cv2
import numpy as np

class AppGestureRecognizer:
    
    def __init__(self, model_path, camera_id = 0):
        self.model_path = model_path
        self.camera_id = camera_id
        
        self.timestamp = 0
        self.result_gesture = ""
        self.recognized_gesture = None
        self.show_frame = np.zeros((640,480,3), np.uint8)
        
        self.init_gesture_recognizer()
        self.gesture_recognizer()


    def print_result(self,result, output_image, timestamp_ms):
        top_gesture = "No gesture"
        self.show_frame = output_image.numpy_view().copy()
        if len(result.gestures) > 0:
            top_gesture = result.gestures[0][0].category_name
        self.result_gesture = top_gesture

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
    
    def gesture_recognizer(self):
        cap = cv2.VideoCapture(self.camera_id)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        while True:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            self.recognizer.recognize_async(mp_image, self.timestamp)
            self.timestamp = self.timestamp + 1
            frame = self.show_frame
            cv2.imshow('frame', frame)
            print(self.result_gesture)
            key = cv2.waitKey(1)

            if key == ord('q') or key == ord("Q"):
                break
        
        cv2.destroyAllWindows()
            
if __name__ == "__main__":
    model_path = "./models/gesture_recognizer.task"
    camera = 0
    AppGestureRecognizer(model_path, camera)