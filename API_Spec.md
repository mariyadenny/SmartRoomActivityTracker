```md
# API Specification

## POST /motion-event

### Description
Receives a completed motion event from the ESP32.

### Headers
Authorization: Bearer <token>  
Content-Type: application/json  

### Request Body
```json
{
  "sensor_id": "zone_1",
  "zone_name": "entry",
  "duration_ms": 41850,
  "duration_seconds": 41.85,
  "device_status": "online"
}

### Success ResponseS
```json
{
  "status": "success",
  "message": "Motion event stored"
}

### Failure Response
```json
{
  "status": "error",
  "message": "Unauthorized or invalid payload"
}