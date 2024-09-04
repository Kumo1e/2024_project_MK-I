import serial
from car_funtion import Camera,\
                        TrackGreenBall,\
                        AppGestureRecognizer
import cv2


if __name__ == "__main__":
    port = "COM6"
    camera_id = 0
    model_path = "./models/gesture_recognizer.task"
    
    # ser = serial.Serial(port, 9600)  # 替換為你的MATRIX板子的端口
    cap = Camera(camera_id)
    track_ball = TrackGreenBall()
    recognize = AppGestureRecognizer(model_path)
    command = ""
    turn = 0

    try:
        while True:
            hsv, frame = cap.capture_frame()
            gesture = recognize.gesture_recognizer(frame)
            if gesture == "Pointing_Up": # 轉圈
                turn += 1
                if turn%5 == 0:
                    print("轉圈")
                    command = f"c\n"
                    # ser.write(command.encode())
                    cv2.waitKey(1000)
            elif gesture == "Thumb_Down": # 後退
                print("後退")
                command = f"b\n"
                # ser.write(command.encode())
            elif gesture == "Thumb_Up": # 前進
                print("前進")
                command = f"a\n"
                # ser.write(command.encode())
            elif gesture == "Open_Palm": # 前進
                print("停")
                command = f"w\n"
                # ser.write(command.encode())
            elif gesture == "ILoveYou": # 跟隨
                is_follow = True
                while is_follow:
                    hsv, frame = cap.capture_frame()
                    move = track_ball.track_green_ball(hsv)
                    gesture = recognize.gesture_recognizer(frame)
                    command = move
                    # ser.write(command.encode())
                    cv2.waitKey(10)
                    command = ""
                    # ser.write(command.encode())
                    print(move)
                    if gesture == "Open_Palm":
                        is_follow = False
                        command = f"d\n"
                        # ser.write(command.encode())
            else:
                print(gesture)
                command = f"j\n"
                # ser.write(command.encode())
            cv2.waitKey(200)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Interrupt by user")
    finally:
        cap.release_camera()
        