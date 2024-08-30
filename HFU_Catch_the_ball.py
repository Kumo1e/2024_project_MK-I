import cv2
import numpy as np
import serial
import time
from camera_init import initialize_camera, capture_frame, release_camera

def track_green_ball(port, camera_id):
    ser = serial.Serial(port, 9600)  # 替換為你的MATRIX板子的端口
    cap = initialize_camera(camera_id)

    move_command = f"0 0 5\n"
    stable_frames = 0  # 記錄穩定幀數
    stability_threshold = 4  # 設定穩定幀數的閾值 (降低以加快反應速度)
    last_x, last_y = 0, 0

    while True:
        hsv = capture_frame(cap)
        if hsv is None:
            break

        # 定義螢光綠的範圍
        lower_green = (35, 40, 40)
        upper_green = (85, 255, 255)

        mask = cv2.inRange(hsv, lower_green, upper_green)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            if radius > 10:
                angle_x = 15 + int(int(x) / 320 * 150)  # 調整解析度後的比例
                angle_y = 15 + int(int(y) / 240 * 150)
                output_x = -1 if angle_x > 160 else (0 if angle_x > 120 else 1)
                output_y = 1 if angle_y > 160 else (0 if angle_y > 120 else -1)

                # 檢查球的位置是否穩定
                if abs(last_x - x) < 10 and abs(last_y - y) < 10:
                    stable_frames += 1
                else:
                    stable_frames = 0

                if stable_frames > stability_threshold:
                    move_command = f"{output_y} {output_x} {int(radius)}\n"
                else:
                    move_command = f"0 0 5\n"

                ser.write(move_command.encode())
                last_x, last_y = x, y
            else:
                move_command = f"0 0 5\n"
                ser.write(move_command.encode())
        else:
            move_command = f"0 0 5\n"
            ser.write(move_command.encode())
        print(move_command)
    release_camera(cap)

if __name__ == "__main__":
    port = 'COM6'  # 替換為你的MATRIX板子的端口
    camera_id = 1  # 啟動相機
    track_green_ball(port, camera_id)