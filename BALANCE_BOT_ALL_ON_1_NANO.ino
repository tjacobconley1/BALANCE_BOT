#include "I2Cdev.h"
#include<SoftwareSerial.h>
#include <Wire.h>
#include <PID_v1.h> 
#include "math.h"

//VARIABLES=========================================
//variables for the MPU and each piece of data 
const int MPU=0x68; 
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;
//Int pin on MPU6050 to Pin 2 Nano
const int gyroInt = 2; 
//pin that sends signal to the motor controller
const int MotorSig = 3; 
//string to hold serial readings 
String serialData;
//relay pin variables 
int relay1 = 5;
int relay2 = 4;
//pins that read encoders 
int ENpinR0 = A0;
int ENpinR1;
int ENpinR2 = A2;
int ENpinL3 = A3;
int ENpinL4 = A6;
int ENpinL5 = A7;
//variables to hold analog readings from encoders 
int ENpinR0_VAL = 0;
int ENpinR1_VAL = 0;
int ENpinR2_VAL = 0;
int ENpinL3_VAL = 0;
int ENpinL4_VAL = 0;
int ENpinL5_VAL = 0;
//variables to hold combined encoder values
int ENright_CALC = 0;
int ENleft_CALC = 0;
//variables to hold gyro/accel values
int Accel_X = 0;
int Accel_Y = 0;
int Accel_Z = 0;
int Gyro_X = 0;
int Gyro_Y = 0;
int Gyro_Z = 0; 
//POT PIN
int POT_PIN = A1;
//variable for POT
int POT_VAL;
//variable for accel angle
float accANGLE;
//variable for gyro angle 
float gyroANGLE;
//current angler holder 
float currentANGLE = 0; 
//previous angle holder 
float previousANGLE = 0; 
//variable for gyro rate 
int16_t gyroRate;
//variables for time 
unsigned long currentTIME, previousTIME = 0, loopTIME, sampleTIME = 0.005;
//variable to hold each iterative calculated error
float error = 0;
//variable to hold sum of error 
float errorSUM = 0;
//variable to hold the target angle 
float targetANGLE = 1;
//variable to hold current motor power needed 
float motorPOWER = 0;
//PID variables 
float Kp = 40;
float Ki = 40; 
float Kd = 0.05; 

//SETUP=====================================================================
void setup() {
    //initialize serial com
    Serial.begin(115200);

    //set pins to either input or output
    pinMode(relay1, OUTPUT);
    pinMode(relay2, OUTPUT);
    pinMode(gyroInt, OUTPUT);
    pinMode(MotorSig, OUTPUT);
     
    pinMode(ENpinR0, INPUT);
    pinMode(ENpinR1, INPUT);
    pinMode(ENpinR2, INPUT);
    pinMode(ENpinL3, INPUT);
    pinMode(ENpinL4, INPUT);
    pinMode(ENpinL5, INPUT);

 
    pinMode(POT_PIN, INPUT);
    //initialize MPU6050
    Wire.begin();
    Wire.beginTransmission(MPU);
    Wire.write(0x6B); 
    Wire.write(0);    
    Wire.endTransmission(true);
}




//LOOP=======================================================================
void loop() {


  //set time to miliseconds
  currentTIME = millis();
  //calculate time length of loop
  loopTIME = currentTIME - previousTIME;
  //set the current time value to the previous time variable 
  previousTIME = currentTIME;
  
  
  //open wire to read data 
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);  
  Wire.endTransmission(false);
  Wire.requestFrom(MPU,12,true);
    
  AcX=Wire.read()<<8|Wire.read();    
  AcY=Wire.read()<<8|Wire.read();  
  AcZ=Wire.read()<<8|Wire.read();  
  GyX=Wire.read()<<8|Wire.read();  
  GyY=Wire.read()<<8|Wire.read();  
  GyZ=Wire.read()<<8|Wire.read();  

  //assign new reading to corresponding holding variables 
  Accel_X = AcX;
  Accel_Y = AcY;
  Accel_Z = AcZ;

  Gyro_X = GyX;
  Gyro_Y = GyY;
  Gyro_Z = GyZ; 

  //read in encoder values and assign to corresponding holding variables 
  ENpinR0_VAL = analogRead(ENpinR0);
  ENpinR1_VAL = analogRead(ENpinR1);
  ENpinR2_VAL = analogRead(ENpinR2);
  ENpinL3_VAL = analogRead(ENpinL3);
  ENpinL4_VAL = analogRead(ENpinL4);
  ENpinL5_VAL = analogRead(ENpinL5);

  //combine encoders values and assign to holding variable 
  ENright_CALC = (ENpinR0_VAL + ENpinR1_VAL + ENpinR2_VAL);
  ENleft_CALC = (ENpinL3_VAL + ENpinL4_VAL + ENpinL5_VAL);
  
  //temporarily print results to the serial port
  Serial.println("ACCELEROMETER");
  Serial.println(Accel_X);
  Serial.println(Accel_Y);
  Serial.println(Accel_Z);
  Serial.println("GYROSCOPE");
  Serial.println(Gyro_X);
  Serial.println(Gyro_Y);
  Serial.println(Gyro_Z); 
  Serial.println("COMBINED ENCODER VALUES");
  Serial.println(ENright_CALC);
  Serial.println(ENleft_CALC); 
  delay(10); 

  //calculate accelerometer angle 
  accANGLE =abs( atan2(Accel_Y, Accel_Z)*RAD_TO_DEG );
    if(isnan(accANGLE));
    else{
      Serial.println("accANGLE");
      Serial.println(accANGLE);
  }
  
  //calculate gyro rate 
  gyroRate = map(Gyro_X, -32768, 32767, -250, 250);
  
  //calculate gyro angle 
  gyroANGLE = abs( gyroANGLE + (float)gyroRate*loopTIME/1000);
  Serial.println("gyroANGLE");
  Serial.println(gyroANGLE);
  Serial.println("\n\n\n\n\n");

  //calculate current angle 
  currentANGLE = 0.9934*(previousANGLE + gyroANGLE) + 0.0066*(accANGLE);
  Serial.println("CURRENT ANGLE");
  Serial.println(currentANGLE);
  
  //calculate amount of error 
  error = currentANGLE - targetANGLE;
  Serial.println("ERROR");
  Serial.println(error);
  
  errorSUM = errorSUM + error;
  Serial.println("errorSUM & errorSUM CONSTRAINED");
  Serial.println(errorSUM);
  //not sure what this constraint function does 
  errorSUM = constrain(errorSUM, -300,300);
  Serial.println(errorSUM);
   
  //use PID values to calculate how much power to send to the motors 
  motorPOWER = Kp*(error) + Ki*(errorSUM)*sampleTIME - Kd*(currentANGLE - previousANGLE)/sampleTIME;
  Serial.println("MOTOR POWER");
  Serial.println(motorPOWER);
  





//THIS WILL BE REPLACED WITH MOTOR CONTROL FUNCTIONS SO THAT====================
//THE RELAYS AND MOTOR SIGNAL RAMP UP/RAMP DOWN CANNOT BE MIS TIMED============= 

  //if tips past balance point relays must be switched
  //to change the direction of the wheels 
  if(accANGLE <= 136.5){
    digitalWrite(relay1, HIGH);
    digitalWrite(relay2, LOW);
    delay(10);
  }
  else if(accANGLE >= 138.5){
    digitalWrite(relay1, LOW);
    digitalWrite(relay2, HIGH);  
    delay(10);
  }
  else if(accANGLE < 138.5 and accANGLE >136.5){
   
    Serial.println("\n\n\n================BALANCED===============\n\n\n");  
  } 
//THIS WILL BE REPLACED WITH MOTOR CONTROL FUNCTIONS SO THAT====================
//THE RELAYS AND MOTOR SIGNAL RAMP UP/RAMP DOWN CANNOT BE MIS TIMED=============

  
    
}
