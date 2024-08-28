import cv2
import numpy as np
import serial

ser = serial.Serial('COM6', 9600)  # 替換為你的MATRIX板子的端口

# 啟動相機
cap = cv2.VideoCapture(1)
move_command = f"0 0 5\n"
i = 0
while True:
    # 讀取影像
    ret, frame = cap.read()
    if not ret:
        break

    # 將影像轉換成HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 定義螢光綠的範圍
    lower_green = (30, 40, 40)
    upper_green = (90, 255, 255)

    # 產生遮罩
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # 找出輪廓
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # 找到最大輪廓
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        
        # 繪製圓形並顯示
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.putText(frame, "Green Ball Detected", (int(x-radius), int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            angle_x = 15+ int(int(x)/610 * 150)
            angle_y = 15+int(int(y)/ 475 * 150)
            if angle_x > 110:
                output_x = 1
            elif angle_x > 70:
                output_x = 0
            else:
                output_x = -1
            if angle_y > 110:
                output_y = -1
            elif angle_y > 70:
                output_y = 0
            else:
                output_y = 1
            i+=1
            if i % 2 == 0:
                move_command = f"{output_y} {output_x} {int(radius)}\n"            
                ser.write(move_command.encode())
        else:
            move_command = f"0 0 5\n"
            ser.write(move_command.encode())
    else:
        move_command = f"0 0 5\n"
        ser.write(move_command.encode())
    
    # 顯示影像
    cv2.imshow('frame', frame)
    print(move_command.encode())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()