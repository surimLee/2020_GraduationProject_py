#include <Arduino_LSM6DS3.h>

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (true); // halt program
  } 
  Serial.println("IMU initialized!");
}
 
void loop() {
  float aX, aY, aZ;
  float gX, gY, gZ;

  int AC_X, AC_Y, AC_Z;
  int GY_X, GY_Y, GY_Z;

  int ax_Min = -100, ay_Min = -100, az_Min = -100;
  int ax_Max = 100, ay_Max = 100, az_Max = 100;

  int gx_Min = -12500, gy_Min = -12500, gz_Min = -12500;
  int gx_Max = 12500, gy_Max = 12500, gz_Max = 12500;

  AC_X = int(aX * 100);
  AC_Y = int(aY * 100);
  AC_Z = int(aZ * 100);

  GY_X = int(gX * 100);
  GY_Y = int(gY * 100);
  GY_Z = int(gZ * 100);

  AC_X = constrain(AC_X, ax_Min, ax_Max);
  AC_Y = constrain(AC_Y, ay_Min, ay_Max);
  AC_Z = constrain(AC_Z, az_Min, az_Max);

  AC_X = map(AC_X, ax_Min, ax_Max, -90, 90);
  AC_Y = map(AC_Y, ay_Min, ay_Max, -90, 90);
  AC_Z = map(AC_Z, az_Min, az_Max, -90, 90);

  GY_X = constrain(GY_X, gx_Min, gx_Max);
  GY_Y = constrain(GY_Y, gy_Min, gy_Max);
  GY_Z = constrain(GY_Z, gz_Min, gz_Max);

  GY_X = map(GY_X, gx_Min, gx_Max, -30, 30);
  GY_Y = map(GY_Y, gy_Min, gy_Max, -30, 30);
  GY_Z = map(GY_Z, gz_Min, gz_Max, -30, 30);

  if (
    IMU.accelerationAvailable() 
    && IMU.gyroscopeAvailable()
  ) {      
    IMU.readAcceleration(aX, aY, aZ);
    IMU.readGyroscope(gX, gY, gZ);
    Serial.print(AC_X); Serial.print(" ");
    Serial.print(AC_Y); Serial.print(" ");
    Serial.print(AC_Z); Serial.print(" ");
    Serial.print(GY_X); Serial.print(" ");
    Serial.print(GY_Y); Serial.print(" ");
    Serial.println(GY_Z);
    delay(250);
  }
}
