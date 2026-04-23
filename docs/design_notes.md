# Design Notes

## Overview
This document explains the design decisions, architecture choices, and reasoning behind the Smart Room Occupancy & Activity Monitor system.

The system is designed to track activity in a shared indoor space using motion sensors and provide meaningful insights through a backend and dashboard.

---

## System Architecture

The system is divided into four main layers:

### 1. Sensor Layer (ESP32 + PIR Sensors)
- Uses an ESP32 microcontroller with multiple PIR sensors
- Each sensor represents a specific zone:
  - Entry
  - Hallway
  - Room
- Detects motion and measures how long motion lasts
- Sends motion events as JSON over WiFi

---

### 2. Backend Layer (Flask API)
- Built using Python and Flask
- Runs locally on a laptop
- Responsibilities:
  - Receives motion events via HTTP POST
  - Validates authentication token
  - Adds UTC timestamp
  - Stores events in MongoDB
  - Serves dashboard interface

---

### 3. Database Layer (MongoDB)
- Stores motion events as JSON documents
- Schema is flexible and allows future expansion
- Each event includes sensor data and backend timestamp

---

### 4. Frontend Layer (Dashboard)
- Built with HTML, CSS, and JavaScript
- No external frameworks used
- Displays:
  - real-time event data
  - zone statistics
  - activity charts
  - movement path visualization

---

## Key Design Decisions

### 1. Event-Based Motion Tracking
Instead of continuously logging motion states (true/false), the system records **complete motion events**.

Each event includes:
- start of motion
- end of motion
- duration

**Reason:**
- Reduces unnecessary data
- Produces more meaningful insights
- Improves dashboard clarity

---

### 2. Multiple Sensor Zones
The system uses multiple PIR sensors to represent different areas of the room.

**Reason:**
- Enables tracking movement across space
- Allows detection of most active zones
- Supports movement path visualization

---

### 3. JSON-Based Communication
All communication between ESP32 and backend uses JSON format.

**Reason:**
- Lightweight and easy to parse
- Compatible with both embedded systems and web applications
- Standard format for APIs

---

### 4. Local Backend Deployment
The Flask backend runs on a local machine.

**Reason:**
- Simpler setup for development
- No cloud infrastructure required
- Easier debugging and testing

---

### 5. Frontend Without Frameworks
The dashboard is built using plain HTML, CSS, and JavaScript.

**Reason:**
- Lightweight and fast
- No dependency overhead
- Easier to understand and modify

---

## Movement Visualization Design

The movement path feature:
- Uses recent motion events
- Orders events by timestamp
- Removes consecutive duplicate zones
- Displays movement as:
  - animated person icon
  - fading trail dots

**Reason:**
- Provides intuitive understanding of movement
- Keeps visualization simple without complex tracking algorithms

---

## Security Design

Basic security is implemented through:

- Bearer token authentication for API requests
- Separation of sensitive data in `secrets.h`
- `.gitignore` prevents secrets from being uploaded
- MongoDB runs locally and is not publicly exposed

**Reason:**
- Prevent unauthorized API access
- Protect sensitive credentials
- Maintain safe local environment

---

## Limitations

- PIR sensors detect motion but not number of people
- Cannot detect stationary individuals
- Movement path is an estimation, not exact tracking
- System is not cloud deployed
- No user authentication beyond API token

---

## Future Improvements

If more time were available, the system could be improved by:

### Backend / Deployment
- Deploy backend to cloud (AWS, Azure, etc.)
- Add user authentication and role-based access

### Sensors
- Add more sensors for better coverage
- Combine PIR with other sensors (camera, ultrasonic)

### Data & Analytics
- Add heatmaps for activity patterns
- Analyze activity by time of day or week
- Detect abnormal patterns

### Frontend
- Add dark mode
- Improve UI/UX design
- Add mobile responsiveness

### Real-Time Improvements
- Replace polling with WebSockets
- Improve animation smoothness

---

## Final Notes

This system demonstrates:
- integration of hardware and software
- real-time data processing
- API design and communication
- full-stack system architecture

The design focuses on simplicity, clarity, and scalability for future improvements.

---