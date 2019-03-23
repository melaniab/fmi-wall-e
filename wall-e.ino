#include <stdlib.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define MIN_PULSE_WIDTH       650
#define MAX_PULSE_WIDTH       2350
#define DEFAULT_PULSE_WIDTH   1500
#define FREQUENCY             50

void setup()
{
  pwm.begin();
  pwm.setPWMFreq(FREQUENCY);
  Serial.begin(9600); 
}

void AnalyzeCommand(char *Cmd);
void RotateStepper(int motorNum, int angle);
void AnalyzeCommand(char *Cmd);
int  ConvertArgToDec(char *Message);

char nextReceivedCommand[20];
int idx = 0;

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

  if (strCommand = "RM")
  {
    int motorNum = Cmd[3] - '0';
    int angle = ConvertArgToDec(&Cmd[5]);
    pwm.setPWM(motorNum, 0, pulseWidth(angle));


    String strMotorNum(motorNum);
    String strAngle(angle);
    
    Serial.println("Rotate Motor: \n\r");
    Serial.println("Motor Num: ");
    Serial.println(motorNum);
    Serial.println("  Angle: ");
    Serial.println(angle);
    Serial.println("\n\r");
    
  }
  else if (strCommand == "MM")
  {
     // To be implemented ...
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
