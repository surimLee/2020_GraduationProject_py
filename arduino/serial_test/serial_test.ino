#include <SoftwareSerial.h>

#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

//A0~A3, A6,A7 : FLEX SENEOR
//D10 : Tx
//D11 : Rx

//hc06(Tx,Rx)
SoftwareSerial hc06(10,11);
MPU6050 accelgyro;

String temp = " ";
String Character = " ";

//variable initializtion
//엄지손가락
int FLEX_PIN1 = A0;
int sensorMin1 = 710;
int sensorMax1 = 880;

void setup()
{
  hc06.begin(9600);  
  Wire.begin();
  Serial.begin(9600);
  
  
  while (!Serial)
  {
    ; // wait for serial port to connect. Needed for native USB port only
    Serial.println("연결 오류");
  }
}

/*
void printfun(char cp) //to avoid printing repeating symbols
{
  if (cp != temp)
  {
    //// mySerial.print(cp);
    Serial.print(cp);
    temp = cp;
  }
}
*/

void printChar(String Character){
  if(Character != " "){
    if (Character == temp)
    {
      
    }
    else{
      hc06.println(Character);
      Serial.println(Character);
      temp = Character;
    }
  }
}


void loop()
{
  
  //센서값을 저장할 변수
  int flexADC1;

  int angle1;

  // 아날로그 입력받음 (0~1023)
  flexADC1 = analogRead(FLEX_PIN1);


  //값 한정 (01023)
  flexADC1 = constrain(flexADC1, sensorMin1, sensorMax1);
 

  //값 매핑 (0~90으로)
  angle1 = map(flexADC1, sensorMin1, sensorMax1, 0, 10);

  Serial.print("[");
   Serial.print(millis());
   Serial.print(",");
   Serial.print(angle1);
   Serial.println("]");
  //Serial.print(angle1); Serial.print(" ");

  //hc06.println(Character);
//Serial.println();
  delay(100);

}
