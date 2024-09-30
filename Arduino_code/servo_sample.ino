#include <Servo.h>

// 定義伺服馬達
Servo servoX;  // 水平伺服馬達
Servo servoY;  // 垂直伺服馬達

// smoothMove 函數的定義
void smoothMove(Servo &servo, int targetAngle, int delayTime) {
    int currentAngle = servo.read();
    while (currentAngle != targetAngle) {
        if (currentAngle < targetAngle) {
            currentAngle++;
        } else {
            currentAngle--;
        }
        servo.write(currentAngle);
        delay(delayTime);
    }
}


void setup() {
  // 初始化伺服馬達
  servoX.attach(9);   // 水平伺服馬達連接到D9引腳
  servoY.attach(10);
  servoX.write(95);
  servoY.write(90);  // 垂直伺服馬達連接到D10引腳

  // 設置串口通訊速度
  Serial.begin(9600);
}

void loop() {
  // 檢查是否有從串口接收到資料
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');

    // 分析收到的指令，假設格式為 "output_y output_x radius"
    int output_y = data.substring(0, data.indexOf(' ')).toInt();
    data = data.substring(data.indexOf(' ') + 1);
    int output_x = data.substring(0, data.indexOf(' ')).toInt();
    int radius = data.substring(data.indexOf(' ') + 1).toInt();

    // 根據Python程式的輸入值控制伺服馬達的角度
    int angleX = servoX.read();  // 讀取當前伺服馬達角度
    int angleY = servoY.read();

    // smoothMove(servoX, angleX, 2); // 每移動一步延遲10毫秒
    // smoothMove(servoY, angleY, 2);
    
    
    // 調整角度根據Python傳來的數據
    angleX += output_x * 2;  // 每次移動5度
    angleY += output_y * 2;

    // 確保角度在10到170度之間
    angleX = constrain(angleX, 10, 170);
    angleY = constrain(angleY, 10, 170);

    // 設定伺服馬達的新角度
    servoX.write(angleX);
    servoY.write(angleY);

    // 根據半徑控制車子的前進或後退
    if (radius > 50) {
      // 車子應該後退 (此處可以添加控制後退的程式碼)
    } else if (radius < 30) {
      // 車子應該前進 (此處可以添加控制前進的程式碼)
    } else {
      // 車子應該停下 (此處可以添加控制停下的程式碼)
    }
  }
}