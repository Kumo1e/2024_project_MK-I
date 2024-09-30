# 【寵物MK-I】

## 說明
本專題將使用MediaPipe 手勢辨識模型偵測手勢，根據手勢下達相對指令給Arduino 車子執行，指令包含控制車子前進、後退、轉圈、停止動作以及開啟追蹤模式，其中追蹤模式開啟後車子將自動跟隨網球(螢光綠色的物體)移動，利用兩顆伺服馬達調整攝像頭角度將球固定於畫面正中央，並控制車子前進後退將球固定在規定範圍內。

必要工具：一顆攝像頭、Raspberry Pi(非必要)、Arduino UNO、兩顆伺服馬達、兩顆直流馬達以及L298n模板。

使用套件：
1. OpenCV套件，輸入pip install opencv-python 安裝
2. MediaPipe套件，輸入pip install mediapipe 安裝
3. 下載手勢辨識模型 [MediaPipe網站](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer?hl=zh-tw)

## 實作
![image](https://github.com/Kumo1e/hfu_project/blob/main/img/MK-I%E8%A8%AD%E8%A8%88%E5%9C%96.png)

### 電腦端或Raspberry Pi

app.py 與car_functuon.py 放在相同資料夾中，並創建models 資料夾裡面放入mediapipe 手勢辨識模型。
![image](https://github.com/Kumo1e/2024_project_MK-I/blob/main/img/1.png)

開啟app.py，根據自身條件更改

```
    port = "COM6" # arduino port
    camera_id = 0 # camera id 如果只有一個攝像頭預設為0
    model_path = "./models/gesture_recognizer.task" # 手勢辨識模型存放位置
    ser = serial.Serial(port, 9600)  # 替換為你的MATRIX板子的端口
```

手勢辨識的結果共有7種，"Closed_Fist", "Open_Palm", "Pointing_Up", "Thumb_Down", "Thumb_Up", "Victory", "ILoveYou"。

預設模式:
  - "Thumb_Up": 前進
  - "Thumb_Down": 後退
  - "Pointing_Up": 轉圈
  - "ILoveYou": 進入追蹤模式
  - "Open_Palm": 停止所有動作以及離開追蹤模式

為可根據自身喜好更改下方辦別式。

```
gesture = recognize.gesture_recognizer(frame) # 當前辨識結果
if gesture == "Thumb_Down":   # 可更改為自己喜歡的手勢
  command = f"back\n"         # 與Arduino UNO 通信訊息，與arduino_car_cotrol.ino 須一致
  ser.write(command.encode()) # 傳輸訊息給Arduino UNO
```

### Arduino 端

將arduino_car_cotrol.ino 上傳至Arduino UNO板上，Arduino UNO需裝有兩顆伺服馬達、L298n模板與兩顆直流馬達。

```
// 後退動作
void mback(){ 
  analogWrite(ENA,speed); // 使用L298n控制馬達轉速
  analogWrite(ENB,speed);
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
}

// 判斷輸入訊息
if(data == "back") { 
  digitalWrite(LED_PIN, LOW);
  mback();     // 執行動作
  delay(10);   // 延遲時間
    }
```

## 參考資料
- [MediaPipe官網](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer?hl=zh-tw)
- [STEAM教育網](https://steam.oxxostudio.tw/category/python/ai/opencv-color-tracking.html)
