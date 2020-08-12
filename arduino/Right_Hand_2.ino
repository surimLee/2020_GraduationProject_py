#include <Arduino_LSM6DS3.h>
#include <ArduinoBLE.h>

BLEService RightService("19b10000-e8f2-537e-4f6c-d104768a1214");
BLEStringCharacteristic RightChar("D8756BD2-7EFC-4B48-B53C-47EBCA8C2300", BLERead | BLENotify, 100);

/*
 A0~A3, A6 : FLEX SENSOR
 LSM6DS3 : I2C로 연결 [A4/SDA, A5/SCL]
 Acceleration Range [-4 | +4]
 Gyroscope range [-2000 | +2000]
 

오른손 64:fe:15:11:58:93
왼손 60:24:66:1c:40:e3

엄지 검지 중지 약지 새끼
0 새끼
1 약지
2 중지
3 검지
6 엄지
*/
//768 709 764 751 747 
//831 796 869 855 884
//variable initializtion
//엄지손가락
int FLEX_PIN1 = A6;
int sensorMin1 = 768;
int sensorMax1 = 831;

//검지손가락
int FLEX_PIN2 = A3;
int sensorMin2 = 709;
int sensorMax2 = 796;

//중지손가락
int FLEX_PIN3 = A2;
int sensorMin3 = 764;
int sensorMax3 = 869;

//약지손가락
int FLEX_PIN4 = A1;
int sensorMin4 = 751;
int sensorMax4 = 855;

//새끼손가락
int FLEX_PIN5 = A0;
int sensorMin5 = 747;
int sensorMax5 = 884;

float ac_x, ac_y, ac_z;
float gy_x, gy_y, gy_z;
String Right_String;

void setup() {
  
  Serial.begin(9600);
  
  if (!IMU.begin()) { //LSM9DS3 begin
    Serial.println("LSM9DS3 error!");
    while (1);
  }
  
  if (!BLE.begin()) {
    Serial.println("BLE error!");
    while (1);
  }

  // set advertised local name and service UUID:
  BLE.setAdvertisedService(RightService); // add the service UUID
  RightService.addCharacteristic(RightChar);
  BLE.addService(RightService);
  
  // start advertising
  BLE.setLocalName("RIGHT");
  
  // start advertising
  BLE.advertise();
}

void updateData() {

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
  
  if (IMU.accelerationAvailable() 
      && IMU.gyroscopeAvailable()) {
    IMU.readAcceleration(ac_x, ac_y, ac_z);
    IMU.readGyroscope(gy_x, gy_y, gy_z);
  }
  /*
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gy_x, gy_y, gy_z);
  }
*/
  int AC_X;
  int AC_Y;
  int AC_Z;
  int GY_X;
  int GY_Y;
  int GY_Z;
  
  AC_X = int(ac_x*100);
  AC_Y = int(ac_y*100);
  AC_Z = int(ac_z*100);

  GY_X = int(gy_x*100);
  GY_Y = int(gy_y*100);
  GY_Z = int(gy_z*100);

  String flex1 = String(angle1);
  String flex2 = String(angle2);
  String flex3 = String(angle3);
  String flex4 = String(angle4);
  String flex5 = String(angle5);
  String ax = String(AC_X);
  String ay = String(AC_Y);
  String az = String(AC_Z);
  String gx = String(GY_X);
  String gy = String(GY_Y);
  String gz = String(GY_Z);
  
/*
  String flex1 = String(flexADC1);
  String flex2 = String(flexADC2);
  String flex3 = String(flexADC3);
  String flex4 = String(flexADC4);
  String flex5 = String(flexADC5);
  */

  Right_String = "R " + flex1 + " " + flex2 + " " + flex3 + " " + flex4 + " "+ flex5 + " "
                 + ax + " " + ay + " " + az + " "
                 + gx + " " + gy + " " + gz + " Q";
  
  /*
  Level_String = "R " + ax + " " + String(AC_Y) + " " + String(AC_Z) + " "
              + String(GY_X) + " " + String(GY_Y) + " " + String(GY_Z) + " Q"; 
  */
  RightChar.writeValue(Right_String);
  Serial.println(Right_String);
}

void loop() {
  // listen for BLE peripherals to connect:
  BLEDevice central = BLE.central();

  // if a central is connected to peripheral:
  if (central) {
    while (central.connected()) {
      /*
        Serial.print("Connected to central: ");
        Serial.println(central.address());
        */
        updateData();
        delay(250);
      }
    }
}
