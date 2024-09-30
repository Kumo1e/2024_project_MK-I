const int In1 = 2; 
const int In2 = 3; 
const int In3 = 4;   
const int In4 = 7; 
const int ENA = 5;
const int ENB = 6;
const int rotationTime = 1000; //轉圈時要走的時間,目前不知道要走多久先預設1秒
int action = random(3);
int input_command;
int speed =100;

void setup(){
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
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


void loop(){
  if(input_command == "stop"){
  mstop();
  }
  else{
    if(input_command == "front"){ //直走
    mfront();
    } 
    else if(input_command == "back"){//倒車
    mback();
    }
    else if(input_command == "spin"){ //轉一圈
    mspin();
    delay(rotationTime);
    }
  }
}

