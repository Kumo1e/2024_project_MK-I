#include <Servo.h>

const int In1 = 2; 
const int In2 = 3; 
const int In3 = 4;   
const int In4 = 7; 
const int ENA = 5;
const int ENB = 6;
const int LED_PIN = 13;
const int rotationTime = 800; //轉圈時要走的時間,目前不知道要走多久先預設1秒
int action = random(3);
int g;
int k;
int speed =100;
int follow_speed =70;
int turn_speed = 25;

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
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  // 初始化伺服馬達
  servoX.attach(9);   // 水平伺服馬達連接到D9引腳
  servoY.attach(10);
  servoX.write(85);
  servoY.write(90);  // 垂直伺服馬達連接到D10引腳

  // 設置串口通訊速度
  Serial.begin(9600);
    
}

void mstop(){
  analogWrite(ENB,0);
  analogWrite(ENA,0);
  digitalWrite(In1, LOW);
  digitalWrite(In2, LOW);
  digitalWrite(In3, LOW);
  digitalWrite(In4, LOW);

}
void mfront(){
  analogWrite(ENA,speed);
  analogWrite(ENB,speed);
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
}
void mback(){
  analogWrite(ENA,speed);
  analogWrite(ENB,speed);
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
}
void mspin(){
  analogWrite(ENA,speed);
  analogWrite(ENB,speed);
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
}
void mspin1(){
  analogWrite(ENA,speed);
  analogWrite(ENB,speed);
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
}
void mright(){
  analogWrite(ENA,speed);
  analogWrite(ENB,speed); 
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  digitalWrite(In3, LOW);
  digitalWrite(In4, LOW);
}
void mleft(){
  analogWrite(ENA,speed);
  analogWrite(ENB,speed);
  digitalWrite(In1, LOW);
  digitalWrite(In2, LOW);
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
}


void follow_front(){
  analogWrite(ENA,follow_speed);
  analogWrite(ENB,follow_speed);
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
}
void follow_back(){
  analogWrite(ENA,follow_speed);
  analogWrite(ENB,follow_speed);
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
}

void loop() {

  if (Serial.available()){  // 是否接收到指令
    String data = Serial.readStringUntil('\n');  // data 為收到的指令
    digitalWrite(LED_PIN, HIGH);
    if(data == "front"){  // 前進
      digitalWrite(LED_PIN, LOW);
      mfront();
      delay(10);
    }
    else if(data == "back"){ // 後退
      digitalWrite(LED_PIN, LOW);
      mback();
      delay(10);
      // mstop();
    }
    else if(data == "spin"){  // 轉圈
      digitalWrite(LED_PIN, LOW);
      mspin1();
      delay(800);
      mstop();
      delay(10);
      digitalWrite(LED_PIN, LOW);
      mspin();
      delay(1600);
      mstop();
      delay(10);
      digitalWrite(LED_PIN, LOW);
      mspin1();
      delay(1250);
      mstop();
    }
    else if(data == "wait"){  // 停止跟隨，關閉LED，攝像頭回到初始點
      digitalWrite(LED_PIN, LOW);
      servoX.write(85);
      servoY.write(90); 
      mstop();
    }
    else if(data == "none"){  // 沒有接收到指令 停止
      mstop();
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
      
      
      // 調整角度根據Python傳來的數據
      angleX += output_x * 2;  // 每次移動5度
      angleY += output_y * 2;

      // 確保角度在10到170度之間
      angleX = constrain(angleX, 10, 170);
      angleY = constrain(angleY, 70, 150);

      // 設定伺服馬達的新角度
      servoX.write(angleX);
      servoY.write(angleY);

  
      // 根據半徑控制車子的前進或後退
      if (radius < 30) {
        follow_front();
      } 
      else if (radius > 40) {
        follow_back();
      } 
      else {
        mstop();
      }
    }
  }
}