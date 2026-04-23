# Requirements

## Overview
This document defines the functional and non-functional requirements for the Smart Room Occupancy & Activity Monitor system.

The system tracks motion activity across multiple zones using PIR sensors and provides real-time visualization and analytics through a backend and dashboard.

---

## Use Case
The system is designed to monitor activity patterns in a shared indoor space such as:
- study rooms
- dorm lounges
- office environments

It helps answer:
- When is the room most active?
- How long does activity typically last?
- Which zones are used most frequently?

---

## Functional Requirements

### Sensor Layer (ESP32)
- Detect motion using PIR sensors
- Support multiple sensor zones (entry, hallway, room)
- Detect motion start and motion end
- Compute motion duration
- Label each event with sensor_id and zone_name
- Display events via Serial Monitor for debugging

---

### Network Communication
- Connect ESP32 to WiFi
- Send motion events to backend using HTTP POST
- Use JSON format for communication

---

### Backend (Flask API)
- Receive motion events via API endpoint
- Validate requests using Bearer token authentication
- Add UTC timestamp to each event
- Handle missing or invalid data gracefully
- Provide API endpoints for data retrieval

---

### Database (MongoDB)
- Store motion events as JSON documents
- Preserve all event data fields
- Allow retrieval of all stored events

---

### Dashboard (Frontend)
- Display real-time motion data
- Show total number of events
- Identify most active zone
- Display total activity duration
- Show zone-based summaries
- Provide activity chart visualization
- Display recent motion events in a table
- Allow filtering of events by time window
- Visualize movement path across zones

---

## Non-Functional Requirements

- Use event-based tracking instead of continuous logging
- Use UTC timestamps for consistency
- Ensure system is responsive and updates automatically
- Maintain simple and readable code structure
- Separate sensitive data from source code
- Provide clear documentation and modular design

---

## Constraints

- PIR sensors detect motion but not number of people
- PIR sensors may not detect stationary occupants
- System operates on local network (not cloud deployed)
- Accuracy depends on sensor placement

---

## Assumptions

- The monitored space is small enough for PIR coverage
- Users move between defined zones
- WiFi network is stable
- Backend and database are running during operation

---

## Future Requirements (Improvements)

If extended further, the system could include:

- Cloud deployment of backend
- User authentication and access control
- Heatmaps of activity over time
- Real-time updates using WebSockets
- Integration with additional sensors (camera, ultrasonic)
- Mobile-friendly dashboard

---