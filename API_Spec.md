# API Specification

## Overview
This API allows the ESP32 sensor system and the frontend dashboard to communicate with the backend server.

The backend is built using Flask and handles:
- Receiving motion events
- Storing them in MongoDB
- Serving data to the dashboard

---

## Base URL
```
http://<your-ip>:5000
```

---

## 1. POST /motion-event

### Description
Receives a completed motion event from the ESP32.

---

### Headers
```
Authorization: Bearer <API_TOKEN>
Content-Type: application/json
```

---

### Request Body
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

### Field Descriptions

| Field | Type | Description |
|------|------|-------------|
| sensor_id | string | Unique sensor identifier |
| zone_name | string | Location of sensor (entry, hallway, room) |
| duration_ms | number | Duration of motion in milliseconds |
| duration_seconds | number | Duration in seconds |
| device_status | string | Status of sensor (usually "online") |

---

### Success Response (200)
```json
{
  "status": "success",
  "message": "Motion event received"
}
```

---

### Error Responses

#### Unauthorized (401)
```json
{
  "status": "error",
  "message": "Unauthorized"
}
```

#### Bad Request (400)
```json
{
  "status": "error",
  "message": "Missing required field"
}
```

---

## 2. GET /events

### Description
Returns all stored motion events from MongoDB.

---

### Request
```
GET /events
```

---

### Response (200)
```json
[
  {
    "sensor_id": "zone_1",
    "zone_name": "entry",
    "duration_ms": 27700,
    "duration_seconds": 27.7,
    "device_status": "online",
    "received_at_utc": "2026-04-23T18:32:10Z"
  }
]
```

---

## 3. GET /dashboard

### Description
Serves the frontend dashboard UI.

---

### Request
```
GET /dashboard
```

---

### Response
- Returns HTML page
- Displays:
  - live statistics
  - charts
  - movement visualization
  - filtered event table

---

## Authentication

The API uses a simple **Bearer token** for authentication.

- The ESP32 includes the token in every request:
```
Authorization: Bearer <API_TOKEN>
```

- If the token is missing or incorrect:
  - request is rejected with **401 Unauthorized**

---

## Data Flow Summary

### Sensor → Backend
- ESP32 sends motion event using POST request

### Backend → Database
- Flask inserts event into MongoDB collection

### Frontend → Backend
- Dashboard fetches events using GET /events

---

## Notes

- All timestamps are stored in **UTC format**
- Data is stored in MongoDB under:
  - Database: `smart_room`
  - Collection: `motion_events`
- API is designed for local network usage

---