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