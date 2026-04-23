# Smart Room Occupancy & Activity Monitor

## Overview
This project is a real-time smart room monitoring system that tracks human activity across different zones using PIR motion sensors connected to an ESP32.

Instead of continuously logging motion as simple ON/OFF signals, this system records **event-based motion data**, capturing:
- where motion occurred (zone)
- how long motion lasted
- when the event happened

The system sends this data to a backend server, stores it in a database, and visualizes it through an interactive dashboard.

---

## Demo Features
- Multi-zone motion detection (Entry, Hallway, Room)
- Event-based tracking (start → end → duration)
- Live dashboard updates (auto-refresh)
- Most active zone detection
- Total activity time tracking
- Movement path visualization (animated person + fading trail)
- Time filtering (last 20 sec → 1 day)
- MongoDB storage and retrieval

---

## System Architecture

### 1. Sensor Layer (ESP32 + PIR Sensors)
- Hardware:
  - ESP32 microcontroller
  - 3 PIR motion sensors
- Language: C++ (Arduino framework)
- Function:
  - Detect motion per zone
  - Track motion duration
  - Send JSON events over WiFi

---

### 2. Backend (Flask API)
- Language: Python (Flask)
- Runs on: Local machine (localhost)
- Responsibilities:
  - Receive motion events via HTTP POST
  - Validate authentication token
  - Add UTC timestamp
  - Store events in MongoDB
  - Serve dashboard UI

---

### 3. Database (MongoDB)
- Stores all motion events
- Fields:
  - sensor_id
  - zone_name
  - duration_ms
  - duration_seconds
  - device_status
  - received_at_utc

---

### 4. Frontend Dashboard
- Built using:
  - HTML
  - CSS
  - JavaScript (no frameworks)
- Features:
  - Live statistics
  - Zone summaries
  - Activity charts
  - Filterable event table
  - Animated movement path visualization

---

## API Communication

### ESP32 → Backend
**POST /motion-event**

Headers:
```
Authorization: Bearer <API_TOKEN>
Content-Type: application/json
```

Body:
```json
{
  "sensor_id": "zone_1",
  "zone_name": "entry",
  "duration_ms": 27700,
  "duration_seconds": 27.7,
  "device_status": "online"
}
```

---

### Backend → Database
- Uses PyMongo
- Inserts JSON documents into `motion_events` collection

---

### Frontend → Backend
**GET /events**
- Fetches all motion events
- Used to update dashboard in real time

---

## Security

The system includes basic security measures:

- API requires a **Bearer token**
- Unauthorized requests return **401**
- Sensitive data is stored in:
  - `secrets.h` (ignored by Git)
- Example file provided:
  - `secrets_example.h`
- MongoDB runs locally (not publicly exposed)

---

## Testing

### Hardware Testing
- Verified motion detection from each PIR sensor
- Confirmed accurate duration calculation

### Backend Testing
- Unauthorized requests return 401
- Valid requests return 200
- Missing fields return errors

### Database Testing
- Events successfully stored in MongoDB
- UTC timestamps correctly added

### Integration Testing
- ESP32 → Backend → Database pipeline verified
- Dashboard reflects real-time updates

---

## Key Design Decisions

- **Event-based tracking** instead of continuous logging  
  → reduces noise and improves meaningful data

- **Multiple zones**  
  → enables movement tracking across space

- **Lightweight frontend (no frameworks)**  
  → faster and easier deployment

- **Local deployment**  
  → simpler setup for development and testing

---

## Limitations

- PIR sensors detect motion, not number of people
- Cannot detect stationary individuals
- Movement path is an estimate (not exact tracking)
- System currently runs locally (not cloud deployed)

---

## Future Improvements

If more time were available, I would:

- Deploy backend to cloud (AWS / Azure)
- Add user authentication system
- Improve movement tracking accuracy
- Add heatmaps of activity over time
- Use WebSockets for true real-time updates
- Integrate camera or additional sensors
- Add mobile-friendly dashboard

---

## How to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

---

### ESP32
- Open project in PlatformIO
- Update `secrets.h`
- Upload to ESP32

---

### Dashboard
Open in browser:
```
http://<your-ip>:5000/dashboard
```

---

## Project Structure

```
backend/
src/
include/
docs/
README.md
API_Spec.md
DATA_MODELS.md
REQUIREMENTS.md
TESTS.md
```

---

## Final Notes

This project demonstrates:
- Embedded systems integration
- Full-stack development
- API design
- Real-time data visualization
- System architecture design

---

## Author
Mariya Denny, 
Temple University