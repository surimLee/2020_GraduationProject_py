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

//검지손가락
int FLEX_PIN2 = A1;
int sensorMin2 = 779;
int sensorMax2 = 890;

//중지손가락
int FLEX_PIN3 = A2;
int sensorMin3 = 782;
int sensorMax3 = 900;

//약지손가락
int FLEX_PIN4 = A3;
int sensorMin4 = 718;
int sensorMax4 = 850;

//새끼손가락
int FLEX_PIN5 = A6;
int sensorMin5 = 779;
int sensorMax5 = 920;

//손목 - 추가 예정
//int FLEX_PIN0 = A7;
//int sensorMin0 = 1023;
//int sensorMax0 = 0;

//Accelerometer x, y, z
int16_t ax, ay, az;
int A_ax, A_ay, A_az;
int ax_Min = -16383, ay_Min = -16383, az_Min = -16383;
int ax_Max = 16383, ay_Max = 16383, az_Max = 16383;

//Gyro x, y, z
int16_t gx, gy, gz;
int G_gx, G_gy, G_gz;
int gx_Min = -250, gy_Min = -250, gz_Min = -250;
int gx_Max = 2000, gy_Max = 2000, gz_Max = 2000;

void setup()
{
  hc06.begin(9600);  
  Wire.begin();
  accelgyro.initialize();
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
  Serial.println("센서값 받음");


  //값 한정 (01023)
  flexADC1 = constrain(flexADC1, sensorMin1, sensorMax1);
  flexADC2 = constrain(flexADC2, sensorMin2, sensorMax2);
  flexADC3 = constrain(flexADC3, sensorMin3, sensorMax3);
  flexADC4 = constrain(flexADC4, sensorMin4, sensorMax4);
  flexADC5 = constrain(flexADC5, sensorMin5, sensorMax5);


  //값 매핑 (0~90으로)
  angle1 = map(flexADC1, sensorMin1, sensorMax1, 0, 3);
  angle2 = map(flexADC2, sensorMin2, sensorMax2, 0, 3);
  angle3 = map(flexADC3, sensorMin3, sensorMax3, 0, 3);
  angle4 = map(flexADC4, sensorMin4, sensorMax4, 0, 3);
  angle5 = map(flexADC5, sensorMin5, sensorMax5, 0, 3);

  if(angle1==0 && angle2==0 && angle3==0 && angle4==0 && angle5==0){ printChar(" "); }
  if(angle1==0 && angle2==0 && angle3>=2 && angle4>=2 && angle5>=2 && A_ay>20){ printChar("ㄱ"); }
  if(angle1==0 && angle2==0 && angle3>=2 && angle4>=2 && angle5>=2 && A_ay<-20 && A_az<=15){ printChar("ㄴ"); }
  if(angle1>=2 && angle2==0 && angle3==0 && angle4>=2 && angle5>=2){ printChar("ㄷ"); }
  if(angle1>=1 && angle2==0 && angle3==0 && angle4==0 && angle5>=2){ printChar("ㄹ"); }
  if(angle1>=1 && angle2==3 && angle3==3 && angle4>=3 && angle5>=2){ printChar("ㅁ"); }
  if(angle1>=2 && angle2==0 && angle3==0 && angle4==0 && angle5==0){ printChar("ㅂ"); }

  Serial.print(angle1); Serial.print(" ");
  Serial.print(angle2);Serial.print(" ");
  Serial.print(angle3);Serial.print(" ");
  Serial.print(angle4);Serial.print(" ");
  Serial.println(angle5);
  
  accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);


  //값 한정
  A_ax = constrain(ax, ax_Min, ax_Max);
  A_ay = constrain(ay, ay_Min, ay_Max);
  A_az = constrain(az, az_Min, az_Max);
  G_gx = constrain(gx, gx_Min, gx_Max);
  G_gy = constrain(gy, gy_Min, gy_Max);
  G_gz = constrain(gz, gz_Min, gz_Max);


  //값 매핑
  A_ax = map(A_ax, ax_Min, ax_Max, -90, 90);
  A_ay = map(A_ay, ay_Min, ay_Max, -90, 90);
  A_az = map(A_az, az_Min, az_Max, -90, 90);
  G_gx = map(G_gx, gx_Min, gx_Max, 0, 30);
  G_gy = map(G_gy, gy_Min, gy_Max, 0, 30);
  G_gz = map(G_gz, gz_Min, gz_Max, 0, 30);


  Serial.print(A_ax); Serial.print("\t");
  Serial.print(A_ay); Serial.print("\t");
  Serial.print(A_az); Serial.print("\t");
  Serial.print(G_gx); Serial.print("\t");
  Serial.print(G_gy); Serial.print("\t");
  Serial.println(G_gz);
  //Serial.println(Character);
  //hc06.println(Character);
  Serial.println();
  //delay(1000);

}
