# Design Notes

## Current State
ESP32 with PIR sensor detects motion and records event durations locally.

## Next Steps
1. Connect ESP32 to tuiot WiFi
2. Send HTTP POST requests to Flask backend
3. Store events in MongoDB
4. Add authentication token

## Timestamp Plan
Backend will store timestamps in UTC.
ESP32 may later sync time using NTP.