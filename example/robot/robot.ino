#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define MIN_PULSE_WIDTH       650
#define MAX_PULSE_WIDTH       2350
#define DEFAULT_PULSE_WIDTH   1500
#define FREQUENCY             50

void setup() {
  pwm.begin();
  pwm.setPWMFreq(FREQUENCY);
}

void loop() {
//  int maxAge = 180;
//  pwm.setPWM(0, 0, pulseWidth(50));
//  pwm.setPWM(1, 0, pulseWidth(maxAge-50));
//  delay(5000);
//  pwm.setPWM(0, 0, pulseWidth(180));
//  pwm.setPWM(1, 0, pulseWidth(90));
//  delay(5000);


//  pwm.setPWM(0, 0, pulseWidth(180));
//  pwm.setPWM(1, 0, pulseWidth(0));

  int verticalAngle = 90;
  pwm.setPWM(0, 0, pulseWidth(verticalAngle));
  pwm.setPWM(1, 0, pulseWidth(180 - verticalAngle));
  
  pwm.setPWM(2, 0, pulseWidth(0));
  pwm.setPWM(3, 0, pulseWidth(5));
  pwm.setPWM(4, 0, pulseWidth(0));
  pwm.setPWM(5, 0, pulseWidth(0));
  pwm.setPWM(6, 0, pulseWidth(0));
  pwm.setPWM(7, 0, pulseWidth(5));
}

int pulseWidth(int angle)
{
  int pulse_wide, analog_value;
  pulse_wide   = map(angle, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
  analog_value = int(float(pulse_wide) / 1000000 * FREQUENCY * 4096);
  return analog_value;
}
