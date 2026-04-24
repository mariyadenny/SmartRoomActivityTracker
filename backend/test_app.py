from app import app

# test to check if request without token is rejected
def test_missing_token():
    # create test client for the app
    client = app.test_client()

    # send POST request without Authorization header
    response = client.post("/motion-event", json={
        "sensor_id": "zone_1",
        "zone_name": "entry",
        "duration_ms": 1000,
        "duration_seconds": 1.0,
        "device_status": "online"
    })

    # expect 401 Unauthorized
    assert response.status_code == 401