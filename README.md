# 【寵物MK-I】

## 說明
本專題將使用MediaPipe 手勢辨識模型偵測手勢，根據手勢下達相對指令給Arduino 車子執行，指令包含控制車子前進、後退、轉圈、停止動作以及開啟追蹤模式，其中追蹤模式開啟後車子將自動跟隨網球(螢光綠色的物體)移動，利用兩顆伺服馬達調整攝像頭角度將球固定於畫面正中央，並控制車子前進後退將球固定在規定範圍內。

必要工具：一顆攝像頭、Raspberry Pi(非必要)、Arduino UNO、兩顆伺服馬達、兩顆直流馬達以及L298N模板。

使用套件：
1. OpenCV套件，輸入pip install opencv-python 安裝
2. MediaPipe套件，輸入pip install mediapipe 安裝
3. 下載手勢辨識模型 [MediaPipe網站](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer?hl=zh-tw)

## 實作
![image](https://github.com/Kumo1e/hfu_project/blob/main/img/MK-I%E8%A8%AD%E8%A8%88%E5%9C%96.png?raw=true)
