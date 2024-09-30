import mediapipe as mp
import cv2
import time
import queue

result_queue = queue.Queue(1)
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult

def init_gesture_recognizer(model_path):    
    BaseOptions = mp.tasks.BaseOptions
    GestureRecognizer = mp.tasks.vision.GestureRecognizer
    GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode
    
    with open(model_path, 'rb') as model: # 建立檔案和程式碼的通道
        model_file = model.read()

    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_buffer=model_file),
        running_mode=VisionRunningMode.LIVE_STREAM, # 用於直播模式
        result_callback=print_result
    )
    recognizer = GestureRecognizer.create_from_options(options)
    return recognizer


def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int): # type: ignore

    top_gesture = result.gestures
    # frame = output_image.numpy_view().copy()
    text = ""
    if top_gesture:
        text = f"{top_gesture[0][0].category_name}"
        # print('gesture recognize result: {}'.format(top_gesture))
        # put_cv2_text(frame, text, (20,20))
    # result_queue.put(frame)
    result_queue.put((text, ))


def gesture_recognizer(recognizer, camera_id):
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
 
    while True:
        timestamp = int(round(time.time()*1000))

        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        recognizer.recognize_async(mp_image, timestamp)

        # frame = result_queue.get()
        t = result_queue.get()
        print(t[0])

        cv2.imshow('frame', frame)
        # print(f'{1 / (time.time() - timestamp):.2f}')
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord("Q"):
            break
 
    cv2.destroyAllWindows()

if __name__ == "__main__":
    model_path = "./models/gesture_recognizer.task"
    camera = 0
    model = init_gesture_recognizer(model_path)
    gesture_recognizer(model, camera)
    