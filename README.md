# Smart Room Activity Tracker

## Project Proposal
This project will track room activity using a PIR motion sensor connected to an ESP32. When motion is detected, the system will measure how long the activity lasts and send the data over WiFi to a backend server.

The goal of this project is to analyze room usage patterns over time and identify when the room is most active or inactive.

## Data Collected
- Timestamp (when motion occurs)
- Motion detected (true/false)
- Duration of motion (seconds)
- Device status (online/offline)
- Sensor ID (only if i want to use multiple ones)

This data is collected to distinguish between brief movements and longer periods of activity, allowing for better analysis of room usage.

## Hardware Needed
- ESP32 microcontroller
- PIR motion sensor
- Breadboard and jumper wires

## End User Features
The user will be able to:
- View room activity over time
- Identify peak activity hours
- See how long activity occurs
- Detect long periods of inactivity
