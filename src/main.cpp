#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "secrets.h"

#define PIR_PIN 14

bool motionActive = false;
unsigned long motionStart = 0;

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

void sendMotionEvent(unsigned long durationMs, float durationSec) {
  if (WiFi.status() == WL_CONNECTED) {

    String sensor_id;
    String zone_name;

    int zone = random(1, 4);

    if (zone == 1) {
      sensor_id = "zone_1";
      zone_name = "entry";
    } else if (zone == 2) {
      sensor_id = "zone_2";
      zone_name = "hallway";
    } else {
      sensor_id = "zone_3";
      zone_name = "room";
    }

    HTTPClient http;
    http.begin(SERVER_URL);

    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", String("Bearer ") + API_TOKEN);

    String json = "{";
    json += "\"sensor_id\":\"" + sensor_id + "\",";
    json += "\"zone_name\":\"" + zone_name + "\",";
    json += "\"duration_ms\":" + String(durationMs) + ",";
    json += "\"duration_seconds\":" + String(durationSec, 2) + ",";
    json += "\"device_status\":\"online\"";
    json += "}";

    Serial.println("Sending JSON:");
    Serial.println(json);

    int httpResponseCode = http.POST(json);

    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

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
  pinMode(PIR_PIN, INPUT);
  randomSeed(millis());

  Serial.println("Smart Room Occupancy Monitor Started");

  connectToWiFi();
}

void loop() {
  int motion = digitalRead(PIR_PIN);

  if (motion == HIGH && !motionActive) {
    motionActive = true;
    motionStart = millis();
    Serial.println("Motion started");
  }

  if (motion == LOW && motionActive) {
    motionActive = false;

    unsigned long durationMs = millis() - motionStart;
    float durationSec = durationMs / 1000.0;

    Serial.println("Motion event:");
    Serial.print("Duration (ms): ");
    Serial.println(durationMs);
    Serial.print("Duration (sec): ");
    Serial.println(durationSec, 2);

    sendMotionEvent(durationMs, durationSec);
  }

  delay(50);
}