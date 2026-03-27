# Smart Room Occupancy and Activity Monitor

## Project Proposal
This project monitors activity patterns in a shared indoor room such as a study room, dorm lounge, or office using PIR motion sensors connected to an ESP32.

The goal is not just to detect motion, but to record meaningful motion events, including which sensor zone triggered, how long the activity lasted, and when the room is being used over time.

Instead of continuously storing true/false motion states, the system uses an event-driven approach. When motion begins and ends, the ESP32 records a motion event locally. In later stages, these events will be sent over WiFi to a backend API, stored in a database, and visualized on a web dashboard.

## Use Case
This system can be used to monitor shared room usage and activity patterns.

Possible users include:
- Students using shared study rooms
- RAs or staff monitoring common spaces
- Anyone interested in room occupancy trends

The system helps answer:
- When is the room usually active?
- How long does activity last?
- Which zone of the room is most active?

## Data Collected
Each motion event currently includes:
- sensor_id
- zone_name
- duration_ms
- duration_seconds
- device_status

Future versions will also include:
- UTC timestamps
- WiFi status
- server receive time
- multiple sensor zones

## Hardware
- ESP32
- PIR motion sensor


## Current Progress
- ESP32 configured in PlatformIO
- PIR sensor connected and tested successfully
- Local motion detection working
- Motion event duration being recorded locally

## Planned Modules
- WiFi connection to tuiot
- Flask backend API
- MongoDB database
- Dashboard for room activity trends

## Stretch Goals
- Multiple sensor zones
- Activity summaries by time of day
- Real-time event upload