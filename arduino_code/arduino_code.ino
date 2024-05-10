#include "Wire.h"
#include "Adafruit_PWMServoDriver.h"

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// you can also call it with a different address you want
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);
// you can also call it with a different address and I2C interface
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40, Wire);

#define USMIN  600 // This is the rounded 'minimum' microsecond length based on the minimum pulse of 150
#define USMAX  2400 // This is the rounded 'maximum' microsecond length based on the maximum pulse of 600
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates
int param1=20;
int param2=135;
int param3=130;
int param4=30;
int param5=90;
int param6=0;

float pre_param1=19;
float pre_param2=134;
float pre_param3=129;
float pre_param4=25;
float pre_param5=1;
float pre_param6=1;

// our servo
uint8_t servonum = 0;

void setServoPos(int servo, int pos){
  //This first bit of code makes sure we are not trying to set the servo outside of limits
  int sendPos;
  if(pos > 179){
    pos = 179;
  }
  if(pos < 0){
    pos = 0;
  }
  sendPos = USMIN + ((USMAX - USMIN)/180 * pos);
  if(servo > -1 && servo < 16){//only try to move valid servo addresses
    pwm.writeMicroseconds(servo, sendPos);
  }
}

void setup() {
  Serial.begin(9600);
  // Serial.println("16 channel Servo test!");

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates
  delay(10);
}

void loop() 
{
  // Serial.print("HEllo");
  if (Serial.available() > 0) {
    // Read the incoming string until newline character
    String input = Serial.readStringUntil('\n');

    char charArray[input.length() + 1];
    input.toCharArray(charArray, sizeof(charArray));
    param1 = atof(strtok(charArray, " "));
    param2 = atof(strtok(NULL, " "));
    param3 = atof(strtok(NULL, " "));
    param4 = atof(strtok(NULL, " "));
    param5 = atof(strtok(NULL, " "));
    param6 = atof(strtok(NULL, " "));  

    Serial.print(param1);
    Serial.print(" ");
    Serial.print(param2);
    Serial.print(" ");
    Serial.print(param3);
    Serial.print(" ");
    Serial.print(param4);
    Serial.print(" ");
    Serial.print(param5);
    Serial.print(" ");
    Serial.println(param6);

  }

  //joint 1 

  if (pre_param1 != param1){
    if (pre_param1 < param1){
      pre_param1=pre_param1+1;
      setServoPos(1,pre_param1+65);
    }

    else if(pre_param1 > param1){
      pre_param1=pre_param1-1;
      setServoPos(1,pre_param1+65);
    }

  }

  //joint 2

  if (pre_param2 != param2){
    if (pre_param2 < param2){
      pre_param2=pre_param2+1;
      setServoPos(3,180-pre_param2+15);
    }

    else if(pre_param2 > param2){
      pre_param2=pre_param2-1;
      setServoPos(3,180-pre_param2+15);
    }

    
  }

  //joint 3

  if (pre_param3 != param3){
    if (pre_param3 < param3){
      pre_param3=pre_param3+1;
      setServoPos(5,180-pre_param3);
    }

    else if(pre_param3 > param3){
      pre_param3=pre_param3-1;
      setServoPos(5,180-pre_param3);
    }

    
  }

  //joint 4
  setServoPos(7,25);
  

  //joint 5

  if (pre_param5 != param5){
    if (pre_param5 < param5){
      pre_param5=pre_param5+1;
      setServoPos(9,60-param5);
    }

    else if(pre_param5 > param5){
      pre_param5=pre_param5-1;
      setServoPos(9,60-pre_param5);
    }

    
  }

  //joint 6

  if (pre_param6 != param6){
    if (pre_param6 < param6){
      pre_param6=pre_param6+1;
      setServoPos(12,90-pre_param6);
    }

    else if(pre_param6 > param6){
      pre_param6=pre_param6-1;
      setServoPos(12,90-pre_param6);
    }

    
  }

  delay(50);

}




