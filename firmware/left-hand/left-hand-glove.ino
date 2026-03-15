/*
BSL Smart Glove - Left Hand Firmware

Author: Gouri N. Bandoji
Platform: Arduino Nano 33 IoT

Description:
Reads flex sensors, capacitive touch sensors, and IMU data.
Transmits sensor values via WiFi UDP for gesture data collection.
*/
#include <Wire.h>
#include <MPU6050.h>
#include <WiFiNINA.h>
#include <WiFiUdp.h>
char ssid[] = "YOUR_WIFI_SSID";
char pass[] =
"YOUR_WIFI_PASSWORD";
WiFiUDP Udp;
const char* udpAddress =
"192.168.87.152";
// Laptop IP
const int udpPort = 4211;
// Left hand port
int flexPins[5] = {A0, A1, A2,
A3, A6};
int touchPins[2] = {2, 3};
MPU6050 mpu;
void setup() {
 Serial.begin(115200);
 // Connect Wi-Fi
 WiFi.begin(ssid, pass);
 while (WiFi.status() !=
WL_CONNECTED) {
 delay(500);
 Serial.print(".");
 }
 Serial.println("\nLeft hand
connected to Wi-Fi");
 Udp.begin(udpPort);
 // MPU setup
 Wire.begin();
 mpu.initialize();
 if (!mpu.testConnection()) {
 Serial.println("MPU6050
connection failed!");
 } else {
 Serial.println("MPU6050
ready.");
}
 // Touch pin setup
 for (int i = 0; i < 2; i++) {
 pinMode(touchPins[i], INPUT);
 }
}
void loop() {
 String message = "";
 // Flex readings
 for (int i = 0; i < 5; i++) {
 message +=
analogRead(flexPins[i]);
 message += ",";
 }
 // Touch readings
 for (int i = 0; i < 2; i++) {
 message +=
digitalRead(touchPins[i]);
 message += ",";
 }
 // MPU readings
 int16_t ax, ay, az, gx, gy, gz;
 mpu.getMotion6(&ax, &ay, &az,
&gx, &gy, &gz);
 message += String(ax) + "," +
String(ay) + "," + String(az) +
",";
 message += String(gx) + "," +
String(gy) + "," + String(gz);
 // Send over UDP
 Udp.beginPacket(udpAddress,
udpPort);
 Udp.print(message);
 Udp.endPacket();
 Serial.println(message);
 delay(50); // 20 Hz
}
