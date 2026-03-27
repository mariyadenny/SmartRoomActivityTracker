#include <Arduino.h>

#define PIR_PIN 14

bool motionActive = false;
unsigned long motionStart = 0;

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  Serial.println("Smart Room Occupancy Monitor Started");
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
  }

  delay(50);
}