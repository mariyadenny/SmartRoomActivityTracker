# API Specification

## POST /motion-event

### Description
Receives a completed motion event from the ESP32.

### Headers
Authorization: Bearer <token>  
Content-Type: application/json  

### Request Body
{
  "sensor_id": "zone_1",
  "zone_name": "entry",
  "duration_ms": 41850,
  "duration_seconds": 41.85,
  "device_status": "online"
}

### Success Response
{
  "status": "success",
  "message": "Motion event stored"
}

### Failure Response
{
  "status": "error",
  "message": "Unauthorized or invalid payload"
}