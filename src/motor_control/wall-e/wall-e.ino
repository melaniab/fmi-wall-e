#include <stdlib.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

/*
The IO interfaces is used as the control interface for Arduino UNO and ESPduino. 
Thus, just the four ports D6, D7, D11, and D12 ( as for ESPduino, it is D12, D13, D3, D1) is defined as 
PWMB ( speed for motor B), DIRB (the turn direction for motor B) PWMA(speed for motor A), and DIRA( the turn direction for motor A). 
*/

#define MIN_PULSE_WIDTH       650
#define MAX_PULSE_WIDTH       2350
#define DEFAULT_PULSE_WIDTH   1500
#define FREQUENCY             50
#define DC_MOTOR_PWM_A        9
#define DC_MOTOR_DIR_A        8
#define DC_MOTOR_PWM_B        6
#define DC_MOTOR_DIR_B        7

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void AnalyzeCommand(char *Cmd);
void RotateStepper(int motorNum, int angle);
void AnalyzeCommand(char *Cmd);
void DCMotorInit();
int  ConvertArgToDec(char *Message);

char nextReceivedCommand[20];
int idx = 0;

void setup()
{
  DCMotorInit();    
  pwm.begin();
  pwm.setPWMFreq(FREQUENCY);
  Serial.begin(9600); 
}

void loop()
{
  if(Serial.available() > 0)
  {
    nextReceivedCommand[idx] = Serial.read();
    if (nextReceivedCommand[idx] == '\r')
    {       
       AnalyzeCommand(nextReceivedCommand);
       idx = 0;
    }
    else
    {
       idx++;
    }
  } 
}
/* -------------------------- */
void AnalyzeCommand(char *Cmd)
/* -------------------------- */
{
  char CmdID[2];
  CmdID[0] = Cmd[0];
  CmdID[1] = Cmd[1];
  String strCommand(CmdID);

  if (strCommand == "RM")
  {
    int motorNum = Cmd[3] - '0';
    int angle = ConvertArgToDec(&Cmd[5]);

    if(motorNum == 0)
    {
      pwm.setPWM(0, 0, pulseWidth(angle));
      pwm.setPWM(1, 0, pulseWidth(180 - angle));
    }
    else if(motorNum == 1) 
    {
      int a = 0;
    }
    else if (motorNum == 5)
    {
      if (angle > 100)
      {
        angle = 100;
      }
    }
    else 
    {
      pwm.setPWM(motorNum, 0, pulseWidth(angle));
    }

    String strMotorNum(motorNum);
    String strAngle(angle);
    
    Serial.println("Rotate Motor: \n\r");
    Serial.println("Motor Num: ");
    Serial.println(motorNum);
    Serial.println("  Angle: ");
    Serial.println(angle);
    Serial.println("\n\r");
    
  }
  else if (strCommand == "DM")
  {
     int dutyCycle = ConvertArgToDec(&Cmd[3]);
     digitalWrite(DC_MOTOR_DIR_A, LOW);
     analogWrite(DC_MOTOR_PWM_A, dutyCycle);
     digitalWrite(DC_MOTOR_DIR_B, LOW);
     analogWrite(DC_MOTOR_PWM_B, dutyCycle);

     String strMotorNum(dutyCycle);
    
     Serial.println("Move Motor: \n\r");
     Serial.println("Duty Cycle: ");
     Serial.println(dutyCycle);
     Serial.println("\n\r");
     
  }
  else if (strCommand = "SM")
  {
     analogWrite(DC_MOTOR_PWM_A, 0);
     analogWrite(DC_MOTOR_PWM_B, 0);
  }
}
#if 0
/* -------------------------- */
void RotateStepper(int motorNum, int angle)
/* -------------------------- */
{

  
  
}
/* -------------------------- */
void MoveDcMotor(char MotorDuty)
/* -------------------------- */
{
  
}

#endif
/* -------------------------- */
int ConvertArgToDec(char *Message)
/* -------------------------- */
{
  char StrPtr[10];
  int i = 0;
  int arg_num = 0;

  /* Check if the next symbol is a digit */
  while((Message[i] >= 0x30) && (Message[i] <= 0x39))
  {
    StrPtr[i] = Message[i];
    i++;
  }
  StrPtr[i] = '\0';

  /* Convert string to int using standard function from <stdlib.h> */
  arg_num = atoi(StrPtr);

  return arg_num;
}
/* -------------------------- */
int pulseWidth(int angle)
/* -------------------------- */
{
  int pulse_wide, analog_value;
  pulse_wide   = map(angle, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
  analog_value = int(float(pulse_wide) / 1000000 * FREQUENCY * 4096);
  return analog_value;
}
/* -------------------------- */
void DCMotorInit()
/* -------------------------- */
{
  pinMode(DC_MOTOR_PWM_A, OUTPUT);
  pinMode(DC_MOTOR_DIR_A, OUTPUT);
  pinMode(DC_MOTOR_PWM_B, OUTPUT);
  pinMode(DC_MOTOR_DIR_B, OUTPUT);

  digitalWrite(DC_MOTOR_DIR_A, LOW);
  digitalWrite(DC_MOTOR_DIR_B, HIGH);
}
/* -------------------------- */
