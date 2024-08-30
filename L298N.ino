const int In1 = 4;
const int In2 = 5;
const int In3 = 6;      
const int In4 = 7;  
const int rotationTime = 1000; //轉圈時要走的時間,目前不知道要走多久先預設1秒
int action = random(3);
int g;

void setup(){
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);    
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


void loop(){
  if(g ==0){
  mstop();
  }
  else{
    if(g ==1){ //直走
    mfront();
  } 
  else if(g==2){//倒車
  mback();
  }
  else if(g==3){ //轉一圈
  mspin();
  delay(rotationTime);
  }
  else if(g ==4){
    if (action == 0) {//隨機往左前右走並返回
      mfront();
      delay(1000);
      mback();
      delay(1000);
    } else if (action == 1) {
      mright();
      delay(1000);
      mrright();
      delay(1000);
    } else {
      mleft();
      delay(1000);
      mrleft();
      delay(1000);
    }
  }
  }
}

