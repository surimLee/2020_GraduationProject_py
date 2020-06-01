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

//Accelerometer x, y, z
int16_t ax, ay, az;
int A_ax, A_ay, A_az;
int ax_Min = -16383, ay_Min = -16383, az_Min = -16383;
int ax_Max = 16383, ay_Max = 16383, az_Max = 16383;

//Gyro x, y, z
int16_t gx, gy, gz;
int G_gx, G_gy, G_gz;
int gx_Min = -10848, gy_Min = -10848, gz_Min = -10848;
int gx_Max = 10848, gy_Max = 10848, gz_Max = 10848;

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

  //플렉스센서값 한정
  flexADC1 = constrain(flexADC1, sensorMin1, sensorMax1);
  flexADC2 = constrain(flexADC2, sensorMin2, sensorMax2);
  flexADC3 = constrain(flexADC3, sensorMin3, sensorMax3);
  flexADC4 = constrain(flexADC4, sensorMin4, sensorMax4);
  flexADC5 = constrain(flexADC5, sensorMin5, sensorMax5);

  //플렉스센서값 매핑
  angle1 = map(flexADC1, sensorMin1, sensorMax1, 0, 10);
  angle2 = map(flexADC2, sensorMin2, sensorMax2, 0, 10);
  angle3 = map(flexADC3, sensorMin3, sensorMax3, 0, 10);
  angle4 = map(flexADC4, sensorMin4, sensorMax4, 0, 10);
  angle5 = map(flexADC5, sensorMin5, sensorMax5, 0, 10);

  String angle1_str(angle1);
  String angle2_str(angle2);
  String angle3_str(angle3);
  String angle4_str(angle4);
  String angle5_str(angle5);
  
 //플렉스센서 매핑값 수정 시 사용
/*
  Serial.print(flexADC1); Serial.print(" ");
  Serial.println(angle1);
  Serial.print(flexADC2); Serial.print(" ");
  Serial.println(angle2);
  Serial.print(flexADC3); Serial.print(" ");
  Serial.println(angle3);
  Serial.print(flexADC4); Serial.print(" ");
  Serial.println(angle4);
  Serial.print(flexADC5); Serial.print(" ");
  Serial.println(angle5);
*/

  accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  //MPU-6050 센서값 한정
  A_ax = constrain(ax, ax_Min, ax_Max);
  A_ay = constrain(ay, ay_Min, ay_Max);
  A_az = constrain(az, az_Min, az_Max);
  G_gx = constrain(gx, gx_Min, gx_Max);
  G_gy = constrain(gy, gy_Min, gy_Max);
  G_gz = constrain(gz, gz_Min, gz_Max);

  //MPU-6050 센서값 매핑
  A_ax = map(A_ax, ax_Min, ax_Max, -90, 90);
  A_ay = map(A_ay, ay_Min, ay_Max, -90, 90);
  A_az = map(A_az, az_Min, az_Max, -90, 90);
  G_gx = map(G_gx, gx_Min, gx_Max, -30, 30);
  G_gy = map(G_gy, gy_Min, gy_Max, -30, 30);
  G_gz = map(G_gz, gz_Min, gz_Max, -30, 30);
  
  String A_ax_str(A_ax);
  String A_ay_str(A_ay);
  String A_az_str(A_az);
  String G_gx_str(G_gx);
  String G_gy_str(G_gy);
  String G_gz_str(G_gz);
  
  //MPU-6050 매핑값 수정 시 사용
  /*
  Serial.print(A_ax); Serial.print(" ");
  Serial.print(A_ay); Serial.print(" ");
  Serial.print(A_az); Serial.print(" ");
  Serial.print(G_gx); Serial.print(" ");
  Serial.print(G_gy); Serial.print(" ");
  Serial.println(G_gz);
  Serial.print(ax); Serial.print(" "):
  Serial.print(ay); Serial.print(" ");
  Serial.print(ax); Serial.print(" ");
  Serial.print(gx); Serial.print(" ");
  Serial.print(gy); Serial.print(" ");
  Serial.println(gz);
  */

  String str = "L " + angle1_str + " " + angle2_str + " " + angle3_str + " " + angle4_str + " " + angle5_str 
              + " " + A_ax_str + " " + A_ay_str + " " + A_az_str
              + " " + G_gx_str + " " + G_gy_str + " " + G_gz_str + " Q";
              
  Serial.println(str);
  hc06.println(str);
  
  delay(300);

}
