void setup(){
 Serial.begin(9600); 
}

void loop(){
  Serial.println("dobre li e");
 if(Serial.available() > 0){
  char recieved = Serial.read();
  Serial.println(recieved);
 } 
 
 delay(1000);
}
