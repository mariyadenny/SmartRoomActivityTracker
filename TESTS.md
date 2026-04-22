# Tests

## Hardware Tests
- PIR sensor detects motion
- Motion start and end messages appear
- Duration is calculated correctly

## Backend Tests
- Valid motion event POST works
- Invalid token is rejected
- Missing fields return error

## Database Tests
- Motion event is stored in MongoDB
- Timestamp is stored in UTC

## Integration Tests
- ESP32 sends event to backend
- Backend stores event