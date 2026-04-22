from flask import Flask, request, jsonify
import logging
from datetime import datetime, timezone
from database import save_event

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

API_TOKEN = "SECRET123"

@app.route("/", methods=["GET"])
def home():
    return "Smart Room backend is running"

@app.route("/motion-event", methods=["POST"])
def motion_event():
    auth_header = request.headers.get("Authorization", "")
    if auth_header != f"Bearer {API_TOKEN}":
        logging.warning("Unauthorized request")
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Missing JSON"}), 400

    required = ["sensor_id", "zone_name", "duration_ms", "duration_seconds", "device_status"]

    for field in required:
        if field not in data:
            return jsonify({"status": "error", "message": f"Missing {field}"}), 400

    data["received_at_utc"] = datetime.now(timezone.utc).isoformat()

    logging.info(f"Event received: {data}")
    save_event(data)

    return jsonify({
        "status": "success",
        "message": "Motion event received"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)