void setup(){
 Serial.begin(9600); 
}
String recieved;

void loop(){
  Serial.println("listening...");
 if(Serial.available() > 0){
  recieved = Serial.readString();
  Serial.println(recieved);
 } 
 
 delay(1500);
}
