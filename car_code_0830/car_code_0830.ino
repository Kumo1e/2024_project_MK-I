#include <Servo.h>

const int In1 = 4;
const int In2 = 5;
const int In3 = 6;      
const int In4 = 7;  
const int LED_PIN = 13;
const int rotationTime = 1000; //轉圈時要走的時間,目前不知道要走多久先預設1秒
int action = random(3);
int g;
int k;
// 定義伺服馬達
Servo servoX;  // 水平伺服馬達
Servo servoY;  // 垂直伺服馬達

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

void setup(){
  pinMode(LED_PIN, OUTPUT);
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);
    // 初始化伺服馬達
  servoX.attach(9);   // 水平伺服馬達連接到D9引腳
  servoY.attach(10);
  servoX.write(95);
  servoY.write(90);  // 垂直伺服馬達連接到D10引腳

  // 設置串口通訊速度
  Serial.begin(9600);
    
}

void mstop(){
  digitalWrite(In1, LOW);
  digitalWrite(In2, LOW);
  digitalWrite(In3, LOW);
  digitalWrite(In4, LOW);
}
void mfront(){
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
}
void mback(){
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
}
void mspin(){
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
}
void mright(){
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  digitalWrite(In3, LOW);
  digitalWrite(In4, LOW);
}
void mleft(){
  digitalWrite(In1, LOW);
  digitalWrite(In2, LOW);
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
}
void mrleft(){
  digitalWrite(In1, LOW);
  digitalWrite(In2, LOW);
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
}
void mrright(){
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  digitalWrite(In3, LOW);
  digitalWrite(In4, LOW);
}

void loop() {
  if (Serial.available() > 0){  // 是否接收到指令
    String data = Serial.readStringUntil('\n');  // data 為鳩收到的指令
    if(data == "Thumb_Up"){  // 前進
      digitalWrite(LED_PIN, LOW);
      mfront();
    }
    else if(data == "Thumb_Down"){ // 後退
      digitalWrite(LED_PIN, LOW);
      mback();
    }
    else if(data == "Pointing_Up"){  // 轉圈
      digitalWrite(LED_PIN, LOW);
      mspin();
      delay(rotationTime);
    }
    else if(data == "Closed_Fist"){  // 停止跟隨，關閉LED，攝像頭回到初始點
      digitalWrite(LED_PIN, LOW);
      servoX.write(95);
      servoY.write(90); 
    }
    else{
      digitalWrite(LED_PIN, HIGH);

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
        mback();
      } 
      else if (radius < 30) {
        mfront();
      } 
      else {
        mstop();
      }
    }
  }
  mstop(); // 沒有接收到指令 停止
}
