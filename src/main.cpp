#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

#define PIR_PIN 14

const char* ssid = "1731";
const char* password = "Templegirls@24";
const char* serverUrl = "http://192.168.1.178:5000/motion-event";
const char* apiToken = "SECRET123";

bool motionActive = false;
unsigned long motionStart = 0;

void connectToWiFi() {
  WiFi.begin(ssid, password);
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
    HTTPClient http;
    http.begin(serverUrl);

    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", "Bearer SECRET123");

    String json = "{";
    json += "\"sensor_id\":\"zone_1\",";
    json += "\"zone_name\":\"entry\",";
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
    Serial.println("{");
    Serial.println("  \"sensor_id\": \"zone_1\",");
    Serial.println("  \"zone_name\": \"entry\",");
    Serial.print("  \"duration_ms\": ");
    Serial.print(durationMs);
    Serial.println(",");
    Serial.print("  \"duration_seconds\": ");
    Serial.print(durationSec, 2);
    Serial.println(",");
    Serial.println("  \"device_status\": \"online\"");
    Serial.println("}");

    sendMotionEvent(durationMs, durationSec);
  }

  delay(50);
}