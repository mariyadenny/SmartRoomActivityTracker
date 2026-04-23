# Tests

## Overview
This document describes the testing strategy used for the Smart Room Occupancy & Activity Monitor system.

The system was tested at four levels:
1. Hardware testing
2. Backend/API testing
3. Database testing
4. Full integration testing

---

## 1. Hardware Testing

### Goal
Verify that each PIR sensor correctly detects motion and that the ESP32 reads each zone independently.

### Tests Performed
- Confirmed each PIR sensor powers on correctly
- Verified motion detection on:
  - zone_1 (entry)
  - zone_2 (hallway)
  - zone_3 (room)
- Verified each sensor is connected to a different GPIO pin
- Confirmed motion duration is calculated correctly
- Verified ESP32 connects to WiFi successfully

### Expected Behavior
- Motion near sensor triggers correct zone
- Duration is printed in Serial Monitor
- ESP32 sends event after motion ends

### Observed Result
- All three zones triggered successfully
- Durations were captured and printed
- WiFi connection was successful
- Events were sent to backend with HTTP 200 response

---

## 2. Backend / API Testing

### Goal
Ensure the Flask API correctly accepts valid requests and rejects invalid ones.

### Manual API Tests
Performed using Thunder Client / browser-based testing.

#### Test: Valid POST request
- Sent valid motion event JSON
- Included correct Bearer token

**Expected result:**  
- Response code 200
- Message: `"Motion event received"`

**Observed result:**  
- Passed

#### Test: Missing token
- Sent request without Authorization header

**Expected result:**  
- Response code 401
- Unauthorized message returned

**Observed result:**  
- Passed

#### Test: Missing required fields
- Sent incomplete JSON payload

**Expected result:**  
- Response code 400
- Error message returned

**Observed result:**  
- Passed

---

## 3. Database Testing

### Goal
Ensure valid motion events are stored correctly in MongoDB.

### Tests Performed
- Verified backend inserts event documents into MongoDB
- Confirmed events appear in:
  - Database: `smart_room`
  - Collection: `motion_events`
- Confirmed `received_at_utc` field is added by backend
- Verified multiple sensor zones are stored correctly

### Expected Behavior
- Each valid event appears as a MongoDB document
- Stored data matches API payload plus UTC timestamp

### Observed Result
- Passed

---

## 4. Dashboard Testing

### Goal
Ensure the frontend dashboard correctly displays live data.

### Tests Performed
- Verified `/dashboard` loads successfully
- Confirmed event table updates automatically
- Verified dropdown filter updates table data
- Verified movement path updates using recent events
- Verified zone summary cards update correctly
- Verified bar chart reflects zone event counts
- Verified most active zone and total recorded time update correctly

### Expected Behavior
- Dashboard reflects database contents
- Auto-refresh updates display without manual reload
- Movement path animation updates based on latest events

### Observed Result
- Passed

---

## 5. Full Integration Testing

### Goal
Verify complete end-to-end communication across the entire system.

### System Pipeline Tested
ESP32 → Flask API → MongoDB → Dashboard

### Steps Tested
1. Trigger motion in one of the PIR sensor zones
2. ESP32 detects motion and computes duration
3. ESP32 sends JSON event over WiFi
4. Flask backend receives and validates request
5. Flask stores event in MongoDB
6. Dashboard fetches updated event list
7. Dashboard updates cards, chart, table, and movement path

### Expected Behavior
- Full pipeline completes successfully
- Event appears in Serial Monitor, backend logs, MongoDB, and dashboard

### Observed Result
- Passed

---

## 6. Unit Test Example

### Existing Automated Test
A backend unit test was created to verify that requests without a token are rejected.

Example:
```python
from app import app

def test_missing_token():
    client = app.test_client()

    response = client.post("/motion-event", json={
        "sensor_id": "zone_1",
        "zone_name": "entry",
        "duration_ms": 1000,
        "duration_seconds": 1.0,
        "device_status": "online"
    })

    assert response.status_code == 401
```

### Suggested Additional Unit Tests
If more time were available, additional automated tests would include:
- valid request returns 200
- missing field returns 400
- database insert is mocked and verified
- `/events` route returns JSON list
- dashboard route returns HTML

---

## 7. Mocking / Future Test Improvements

The current testing suite uses:
- real hardware sensors
- real local Flask backend
- real MongoDB database

### If more time were available:
- use a mock database for backend unit tests
- mock API calls to isolate components
- create automated frontend tests
- add continuous integration testing in GitHub Actions

---

## Final Testing Summary

| Test Area | Status |
|----------|--------|
| PIR hardware detection | Passed |
| ESP32 WiFi connection | Passed |
| Motion duration tracking | Passed |
| API authentication | Passed |
| API validation | Passed |
| MongoDB insertion | Passed |
| Dashboard updates | Passed |
| End-to-end pipeline | Passed |

---