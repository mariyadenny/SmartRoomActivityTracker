from flask import Flask, request, jsonify
import logging
from datetime import datetime, timezone
from database import save_event, get_all_events, get_event_count

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

API_TOKEN = "SECRET123"

@app.route("/", methods=["GET"])
def home():
    return """
    <h1>Smart Room Backend</h1>
    <p>Backend is running.</p>
    <ul>
        <li><a href="/events">View raw events JSON</a></li>
        <li><a href="/dashboard">View dashboard</a></li>
    </ul>
    """

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

@app.route("/events", methods=["GET"])
def events():
    return jsonify(get_all_events())

@app.route("/dashboard", methods=["GET"])
def dashboard():
    events = get_all_events()
    count = get_event_count()

    rows = ""
    for event in events:
        rows += f"""
        <tr>
            <td>{event.get('sensor_id', '')}</td>
            <td>{event.get('zone_name', '')}</td>
            <td>{event.get('duration_ms', '')}</td>
            <td>{event.get('duration_seconds', '')}</td>
            <td>{event.get('device_status', '')}</td>
            <td>{event.get('received_at_utc', '')}</td>
        </tr>
        """

    return f"""
    <html>
    <head>
        <title>Smart Room Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 30px;
                background: #f7f7f7;
            }}
            h1 {{
                color: #222;
            }}
            .card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }}
            th {{
                background: #eaeaea;
            }}
        </style>
    </head>
    <body>
        <h1>Smart Room Activity Dashboard</h1>

        <div class="card">
            <h2>Total Motion Events: {count}</h2>
            <p>Showing most recent events first.</p>
        </div>

        <div class="card">
            <table>
                <tr>
                    <th>Sensor ID</th>
                    <th>Zone</th>
                    <th>Duration (ms)</th>
                    <th>Duration (sec)</th>
                    <th>Status</th>
                    <th>Received UTC</th>
                </tr>
                {rows}
            </table>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)