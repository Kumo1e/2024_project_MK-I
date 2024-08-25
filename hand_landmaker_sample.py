import mediapipe as mp
import cv2
import time
import queue
 
result_queue = queue.Queue(1)
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult

def init_hand_landmaker(model_path):    
    BaseOptions = mp.tasks.BaseOptions
    HandLandmarker = mp.tasks.vision.HandLandmarker
    HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode
    
    with open(model_path, 'rb') as model: # 建立檔案和程式碼的通道
        model_file = model.read()

    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_buffer=model_file),
        running_mode=VisionRunningMode.LIVE_STREAM, # 用於直播模式
        num_hands=2,
        result_callback=print_result
    )
    landmarker = HandLandmarker.create_from_options(options)
    return landmarker


def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int): # type: ignore
#    print('hand landmarker result: {}'.format(result))
   frame = output_image.numpy_view().copy()
   for i, landmark in enumerate(result.hand_landmarks):
       hand_name = result.handedness[i][0].category_name
       for j, point in enumerate(landmark):
           x = int(point.x * frame.shape[1])
           y = int(point.y * frame.shape[0])
           if hand_name == 'Left':
               cv2.circle(frame, (x, y), 3, (255,255,0), -1)
           else:
               cv2.circle(frame, (x, y), 3, (0,255,255), -1)
   result_queue.put(frame)

def hand_landmaker(landmarker, camera_id):
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
 
    while True:
        timestamp = int(round(time.time()*1000))
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
 
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        landmarker.detect_async(mp_image, timestamp)
 
        frame = result_queue.get()
        cv2.imshow('frame', frame)
        print(f'{1 / (time.time() - timestamp):.2f}')
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord("Q"):
            break
 
    cv2.destroyAllWindows()

if __name__ == "__main__":
    model_path = "./model/hand_landmarker.task"
    camera = 0
    landmarker = init_hand_landmaker(model_path)
    hand_landmaker(landmarker, camera)