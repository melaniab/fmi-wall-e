/***************************************************
  Example for 2 DC motor && 16 Servo Drive Shield.

  Results: Servo run forward, and then backward....

  by DOIT. http://www.doit.am
 ****************************************************/

#include <Wire.h>
#include <ServoDriver.h>

ServoDriver pwm = ServoDriver();

#define SERVOMIN  102 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  512 // this is the 'maximum' pulse length count (out of 4096)

// IMPORTANT: Servo num #
uint8_t servonum = 0;

void setup() {

  pwm.begin();
  pwm.setPWMFreq(50);  // servos run at 50 Hz
}

void loop() {
  // Drive ONE servo  at a time

  for (uint16_t pulselen = SERVOMIN; pulselen < SERVOMAX; pulselen++) {
    pwm.setPWM(servonum, 0, pulselen);
  }
  delay(300);
  for (uint16_t pulselen = SERVOMAX; pulselen > SERVOMIN; pulselen--) {
    pwm.setPWM(servonum, 0, pulselen);
  }
  delay(300);
}
