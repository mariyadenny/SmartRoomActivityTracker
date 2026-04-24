#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "secrets.h"

// PIR sensor pins
#define PIR1 14   // entry
#define PIR2 27   // hallway
#define PIR3 26   // room

// track if motion is currently active
bool motionActive1 = false;
bool motionActive2 = false;
bool motionActive3 = false;

// store start time of motion
unsigned long motionStart1 = 0;
unsigned long motionStart2 = 0;
unsigned long motionStart3 = 0;

// connect ESP32 to WiFi
void connectToWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi connected");
    Serial.print("ESP32 IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("WiFi connection failed");
  }
}

// send motion data to backend
void sendMotionEvent(String sensor_id, String zone_name, unsigned long durationMs, float durationSec) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(SERVER_URL);

    // add headers
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", String("Bearer ") + API_TOKEN);

    // build JSON manually
    String json = "{";
    json += "\"sensor_id\":\"" + sensor_id + "\",";
    json += "\"zone_name\":\"" + zone_name + "\",";
    json += "\"duration_ms\":" + String(durationMs) + ",";
    json += "\"duration_seconds\":" + String(durationSec, 2) + ",";
    json += "\"device_status\":\"online\"";
    json += "}";

    Serial.println("Sending JSON:");
    Serial.println(json);

    // send POST request
    int httpResponseCode = http.POST(json);

    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    // print server response
    String response = http.getString();
    Serial.println("Server response:");
    Serial.println(response);

    http.end();
  } else {
    Serial.println("WiFi not connected");
  }
}

void setup() {
  Serial.begin(115200);

  // set PIR pins as input
  pinMode(PIR1, INPUT);
  pinMode(PIR2, INPUT);
  pinMode(PIR3, INPUT);

  Serial.println("Smart Room Occupancy Monitor Started");

  connectToWiFi();
}

void loop() {
  // read sensor values
  int motion1 = digitalRead(PIR1);
  int motion2 = digitalRead(PIR2);
  int motion3 = digitalRead(PIR3);

  // -------- SENSOR 1: ENTRY --------
  if (motion1 == HIGH && !motionActive1) {
    motionActive1 = true;
    motionStart1 = millis(); // start timing
    Serial.println("Zone 1 motion started");
  }

  if (motion1 == LOW && motionActive1) {
    motionActive1 = false;

    // calculate duration
    unsigned long durationMs = millis() - motionStart1;
    float durationSec = durationMs / 1000.0;

    Serial.println("Zone 1 motion event");
    Serial.print("Duration (ms): ");
    Serial.println(durationMs);
    Serial.print("Duration (sec): ");
    Serial.println(durationSec, 2);

    // send event
    sendMotionEvent("zone_1", "entry", durationMs, durationSec);
  }

  // -------- SENSOR 2: HALLWAY --------
  if (motion2 == HIGH && !motionActive2) {
    motionActive2 = true;
    motionStart2 = millis();
    Serial.println("Zone 2 motion started");
  }

  if (motion2 == LOW && motionActive2) {
    motionActive2 = false;

    unsigned long durationMs = millis() - motionStart2;
    float durationSec = durationMs / 1000.0;

    Serial.println("Zone 2 motion event");
    Serial.print("Duration (ms): ");
    Serial.println(durationMs);
    Serial.print("Duration (sec): ");
    Serial.println(durationSec, 2);

    sendMotionEvent("zone_2", "hallway", durationMs, durationSec);
  }

  // -------- SENSOR 3: ROOM --------
  if (motion3 == HIGH && !motionActive3) {
    motionActive3 = true;
    motionStart3 = millis();
    Serial.println("Zone 3 motion started");
  }

  if (motion3 == LOW && motionActive3) {
    motionActive3 = false;

    unsigned long durationMs = millis() - motionStart3;
    float durationSec = durationMs / 1000.0;

    Serial.println("Zone 3 motion event");
    Serial.print("Duration (ms): ");
    Serial.println(durationMs);
    Serial.print("Duration (sec): ");
    Serial.println(durationSec, 2);

    sendMotionEvent("zone_3", "room", durationMs, durationSec);
  }

  // small delay to avoid noise
  delay(50);
}