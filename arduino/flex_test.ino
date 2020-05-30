#include <SoftwareSerial.h>

#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

//A0~A3, A6,A7 : FLEX SENEOR
//D10 : Tx
//D11 : Rx

//hc06(Tx,Rx)

String temp = " ";
String Character = " ";

//variable initializtion
//엄지손가락
int FLEX_PIN1 = A0;
int sensorMin1 = 777;
int sensorMax1 = 900;


//검지손가락
int FLEX_PIN2 = A1;
int sensorMin2 = 748;
int sensorMax2 = 926;


//중지손가락
int FLEX_PIN3 = A2;
int sensorMin3 = 773;
int sensorMax3 = 911;


//약지손가락
int FLEX_PIN4 = A3;
int sensorMin4 = 782;
int sensorMax4 = 895;


//새끼손가락
int FLEX_PIN5 = A6;
int sensorMin5 = 766;
int sensorMax5 = 893;

//손목 - 추가 예정
//int FLEX_PIN0 = A7;
//int sensorMin0 = 1023;
//int sensorMax0 = 0;

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  
  //센서값을 저장할 변수
  int flexADC1;
  int flexADC2;
  int flexADC3;
  int flexADC4;
  int flexADC5;

 int angle1;
 int angle2;
 int angle3;
 int angle4;
 int angle5;

  // 아날로그 입력받음 (0~1023)
  flexADC1 = analogRead(FLEX_PIN1);
  flexADC2 = analogRead(FLEX_PIN2);
  flexADC3 = analogRead(FLEX_PIN3);
  flexADC4 = analogRead(FLEX_PIN4);
  flexADC5 = analogRead(FLEX_PIN5);

  flexADC1 = constrain(flexADC1, sensorMin1, sensorMax1);
  angle1 = map(flexADC1, sensorMin1, sensorMax1, 0, 10);
 
  flexADC2 = constrain(flexADC2, sensorMin2, sensorMax2);
  angle2 = map(flexADC2, sensorMin2, sensorMax2, 0, 10);
 
  flexADC3 = constrain(flexADC3, sensorMin3, sensorMax3);
  angle3 = map(flexADC3, sensorMin3, sensorMax3, 0, 10);
 
  flexADC4 = constrain(flexADC4, sensorMin4, sensorMax4);
  angle4 = map(flexADC4, sensorMin4, sensorMax4, 0, 10);

  flexADC5 = constrain(flexADC5, sensorMin5, sensorMax5);
  angle5 = map(flexADC5, sensorMin5, sensorMax5, 0, 10);
 
 

 // Serial.print(flexADC1);Serial.println(" ");
 Serial.print(angle1);Serial.print(" ");
 
// Serial.print(flexADC2);Serial.println(" ");
 Serial.print(angle2);Serial.print(" ");
 
//  Serial.print(flexADC3);Serial.println(" ");
  Serial.print(angle3);Serial.print(" ");
  
//  Serial.print(flexADC4);Serial.println(" ");
  Serial.print(angle4);Serial.print(" ");
  
//  Serial.print(flexADC5);Serial.println(" ");
  Serial.println(angle5);

delay(1000);

}
