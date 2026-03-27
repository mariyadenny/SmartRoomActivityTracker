# Requirements

## Use Case
The system monitors activity patterns in a shared indoor room such as a study room, dorm lounge, or office using PIR motion sensors connected to an ESP32.

## Functional Requirements
- Detect motion using a PIR sensor
- Record motion start and motion end
- Compute motion event duration
- Label each event with a sensor zone
- Display events locally through serial output
- Connect ESP32 to tuiot WiFi
- Send events to a backend API
- Store events in a database
- Display activity data on a dashboard

## Non-Functional Requirements
- Event-driven collection instead of constant true/false logging
- Use UTC timestamps in backend
- Secure API communication
- Logging and error handling
- Clear documentation and modular code

## Constraints
- PIR sensors detect infrared motion changes, not exact people count
- PIR sensors may miss stationary occupants