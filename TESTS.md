```md
# Tests

## Hardware Tests
- Verify PIR sensor detects motion locally
- Verify motion start and end messages appear correctly
- Verify duration is calculated correctly

## Backend Tests
- Test valid motion event POST
- Test invalid token rejection
- Test missing field rejection

## Database Tests
- Test motion event insertion into MongoDB
- Test UTC timestamps are stored correctly

## Integration Tests
- ESP32 sends motion event to backend
- Backend stores event in database