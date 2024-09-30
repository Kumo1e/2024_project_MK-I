import cv2
import numpy as np
import serial
import time
from camera_init import initialize_camera, capture_frame, release_camera

def track_green_ball(port, camera_id):
    ser = serial.Serial(port, 9600)  # 替換為你的MATRIX板子的端口
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    move_command = f"0 0 35\n"
    stable_frames = 0  # 記錄穩定幀數
    stability_threshold = 4  # 設定穩定幀數的閾值 (降低以加快反應速度)
    last_x, last_y = 0, 0

    while True:
        ret, frame = cap.read()
        if ret is None:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # 定義螢光綠的範圍
        lower_green = (25, 60, 160)
        upper_green = (85, 255, 220)

        mask = cv2.inRange(hsv, lower_green, upper_green)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.putText(frame, "Green Ball", (int(x-radius), int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            

            if radius > 10:
                angle_x = 15 + int(int(x) / 640 * 150)  # 調整解析度後的比例
                angle_y = 15 + int(int(y) / 480 * 150)
                output_x = -1 if angle_x > 110 else (0 if angle_x > 70 else 1)
                output_y = 1 if angle_y > 110 else (0 if angle_y > 70 else -1)
                print(angle_x, angle_y)
                # 檢查球的位置是否穩定
                if abs(last_x - x) < 10 and abs(last_y - y) < 10:
                    stable_frames += 1
                else:
                    stable_frames = 0

                if stable_frames > stability_threshold:
                    move_command = f"{output_x} {output_y} {int(radius)}\n"
                else:
                    move_command = f"0 0 35\n"

                ser.write(move_command.encode())
                last_x, last_y = x, y
            else:
                move_command = f"0 0 35\n"
                ser.write(move_command.encode())
        else:
            move_command = f"0 0 35\n"
            ser.write(move_command.encode())
        # print(angle_x, angle_y)
        
        cv2.imshow("frame", frame)
        cv2.waitKey(50)
    release_camera(cap)

if __name__ == "__main__":
    port = 'COM6'  # 替換為你的MATRIX板子的端口
    camera_id = 0  # 啟動相機
    track_green_ball(port, camera_id)