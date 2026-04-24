from flask import Flask, request, jsonify
import logging
from datetime import datetime, timezone
from database import save_event, get_all_events

app = Flask(__name__)

# basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# simple token for authentication
API_TOKEN = "SECRET123"

# home route just to check if backend is running
@app.route("/", methods=["GET"])
def home():
    return """
    <h1>Smart Room Backend</h1>
    <p>Backend is running.</p>
    <ul>
        <li><a href="/events">View raw events JSON</a></li>
        <li><a href="/dashboard">View live dashboard</a></li>
    </ul>
    """

# endpoint to receive motion data from ESP32
@app.route("/motion-event", methods=["POST"])
def motion_event():
    # check auth header
    auth_header = request.headers.get("Authorization", "")
    if auth_header != f"Bearer {API_TOKEN}":
        logging.warning("Unauthorized request")
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    # get json data
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Missing JSON"}), 400

    # required fields check
    required = ["sensor_id", "zone_name", "duration_ms", "duration_seconds", "device_status"]
    for field in required:
        if field not in data:
            return jsonify({"status": "error", "message": f"Missing {field}"}), 400

    # add timestamp
    data["received_at_utc"] = datetime.now(timezone.utc).isoformat()

    # save to database
    logging.info(f"Event received: {data}")
    save_event(data)

    return jsonify({
        "status": "success",
        "message": "Motion event received"
    }), 200

# get all events (used by dashboard)
@app.route("/events", methods=["GET"])
def events():
    return jsonify(get_all_events())

# dashboard UI route
@app.route("/dashboard", methods=["GET"])
def dashboard():
    return """
    <!-- HTML dashboard (kept same, just added minimal comments below in JS) -->
    <html>
    <head>
        <title>Smart Room Activity Dashboard</title>
        ...
        <script>
            // helper to capitalize text
            function titleCase(text) {
                if (!text) return "N/A";
                return text.charAt(0).toUpperCase() + text.slice(1);
            }

            // return color class based on zone
            function zoneColorClass(zone) {
                if (zone === "entry") return "entry-bar";
                if (zone === "hallway") return "hallway-bar";
                return "room-bar";
            }

            // fixed positions for zones on map
            function zonePosition(zone) {
                if (zone === "entry") return { left: 10, top: 48 };
                if (zone === "hallway") return { left: 45, top: 23 };
                if (zone === "room") return { left: 84, top: 48 };
                return { left: 10, top: 48 };
            }

            // convert dropdown value to ms
            function getWindowMilliseconds(value) {
                if (value === "20s") return 20 * 1000;
                if (value === "1m") return 60 * 1000;
                if (value === "5m") return 5 * 60 * 1000;
                if (value === "1h") return 60 * 60 * 1000;
                if (value === "1d") return 24 * 60 * 60 * 1000;
                return null;
            }

            // filter events for table
            function getFilteredEvents(events) {
                const selected = document.getElementById("time-window").value;
                const windowMs = getWindowMilliseconds(selected);

                if (windowMs === null) return events;

                const now = new Date();
                return events.filter(event => {
                    if (!event.received_at_utc) return false;
                    const eventTime = new Date(event.received_at_utc);
                    return (now - eventTime) <= windowMs;
                });
            }

            // get only recent events for movement animation
            function getMovementEvents(events) {
                const now = new Date();
                return events.filter(event => {
                    if (!event.received_at_utc) return false;
                    const eventTime = new Date(event.received_at_utc);
                    return (now - eventTime) <= 20000;
                });
            }

            // update movement path animation
            function updateMovementPath(movementEvents) {
                const recentEvents = movementEvents.slice().reverse();

                const cleaned = [];
                for (const event of recentEvents) {
                    const zone = event.zone_name;
                    if (!zone) continue;

                    if (cleaned.length === 0 || cleaned[cleaned.length - 1].zone !== zone) {
                        cleaned.push({ zone: zone, time: event.received_at_utc });
                    }
                }

                const pathText = document.getElementById("path-text");
                const person = document.getElementById("person-marker");
                const trailLayer = document.getElementById("trail-layer");

                trailLayer.innerHTML = "";

                if (cleaned.length === 0) {
                    pathText.textContent = "Recent Path: No recent movement";
                    person.style.left = "10%";
                    person.style.top = "48%";
                    return;
                }

                pathText.textContent =
                    "Recent Path: " + cleaned.map(item => titleCase(item.zone)).join(" → ");

                // draw trail dots
                for (let i = 0; i < cleaned.length; i++) {
                    const pos = zonePosition(cleaned[i].zone);
                    const dot = document.createElement("div");
                    dot.className = "trail-dot";
                    dot.style.left = pos.left + "%";
                    dot.style.top = pos.top + "%";

                    const opacity = 0.2 + (i + 1) / cleaned.length * 0.6;
                    dot.style.opacity = opacity;

                    trailLayer.appendChild(dot);
                }

                clearInterval(window.personAnimationInterval);

                let index = 0;

                function movePerson() {
                    const pos = zonePosition(cleaned[index].zone);
                    person.style.left = pos.left + "%";
                    person.style.top = pos.top + "%";
                    index++;

                    if (index >= cleaned.length) {
                        clearInterval(window.personAnimationInterval);
                    }
                }

                movePerson();

                if (cleaned.length > 1) {
                    window.personAnimationInterval = setInterval(movePerson, 900);
                }
            }

            // main function to load and update dashboard
            async function loadDashboard() {
                const response = await fetch('/events');
                const events = await response.json();

                let totalDuration = 0;
                const zoneStats = {};

                // calculate stats
                for (const event of events) {
                    const zone = event.zone_name || "unknown";
                    const duration = parseFloat(event.duration_seconds || 0);
                    totalDuration += duration;

                    if (!zoneStats[zone]) {
                        zoneStats[zone] = { count: 0, total_duration: 0 };
                    }

                    zoneStats[zone].count += 1;
                    zoneStats[zone].total_duration += duration;
                }

                // update summary cards
                document.getElementById('total-events').textContent = events.length;
                document.getElementById('total-time').textContent = totalDuration.toFixed(2) + 's';

                const tableFilteredEvents = getFilteredEvents(events);
                const movementEvents = getMovementEvents(events);

                const tableBody = document.getElementById('events-table');
                tableBody.innerHTML = '';

                // update table
                for (const event of tableFilteredEvents.slice(0, 20)) {
                    tableBody.innerHTML += `
                        <tr>
                            <td>${event.sensor_id || ''}</td>
                            <td>${event.zone_name || ''}</td>
                            <td>${event.duration_ms || ''}</td>
                            <td>${event.duration_seconds || ''}</td>
                            <td>${event.device_status || ''}</td>
                            <td>${event.received_at_utc || ''}</td>
                        </tr>
                    `;
                }

                updateMovementPath(movementEvents);
            }

            // load dashboard every 3 seconds
            document.addEventListener("DOMContentLoaded", function() {
                document.getElementById("time-window").addEventListener("change", loadDashboard);
                loadDashboard();
                setInterval(loadDashboard, 3000);
            });
        </script>
    </body>
    </html>
    """

# run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)