from flask import Flask, request, jsonify
import logging
from datetime import datetime, timezone
from database import save_event, get_all_events

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
        <li><a href="/dashboard">View live dashboard</a></li>
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
    return """
    <html>
    <head>
        <title>Smart Room Activity Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 30px;
                background: #f4f6f8;
                color: #222;
            }
            h1 {
                margin-bottom: 10px;
            }
            .muted {
                color: #666;
                font-size: 14px;
            }
            .top-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 20px;
                margin-bottom: 25px;
            }
            .card {
                background: white;
                border-radius: 14px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            }
            .big-number {
                font-size: 28px;
                font-weight: bold;
                margin-top: 10px;
            }
            .middle-grid {
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 20px;
                margin-bottom: 25px;
            }
            .summary-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 20px;
            }
            .summary-card {
                background: white;
                border-radius: 14px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            }
            .section-title {
                margin: 25px 0 12px 0;
            }
            .chart-card {
                background: white;
                border-radius: 14px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                margin-bottom: 25px;
            }
            .bar-row {
                margin: 14px 0;
            }
            .bar-label {
                font-weight: bold;
                margin-bottom: 6px;
            }
            .bar-bg {
                width: 100%;
                background: #e5e7eb;
                border-radius: 10px;
                overflow: hidden;
                height: 24px;
            }
            .bar-fill {
                height: 24px;
                line-height: 24px;
                color: white;
                font-size: 13px;
                padding-left: 10px;
                box-sizing: border-box;
                border-radius: 10px;
                transition: width 0.4s ease;
            }
            .entry-bar { background: #2563eb; }
            .hallway-bar { background: #16a34a; }
            .room-bar { background: #9333ea; }

            .movement-card {
                background: white;
                border-radius: 14px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                min-height: 320px;
            }
            .filter-box {
                margin-top: 10px;
                margin-bottom: 14px;
            }
            select {
                padding: 8px 12px;
                border-radius: 8px;
                border: 1px solid #cbd5e1;
                background: white;
                font-size: 14px;
            }
            .map-box {
                position: relative;
                width: 100%;
                height: 220px;
                background: #f8fafc;
                border: 2px solid #dbe3ea;
                border-radius: 16px;
                margin-top: 12px;
                overflow: hidden;
            }
            .zone-node {
                position: absolute;
                width: 90px;
                text-align: center;
                font-weight: bold;
                color: #333;
                z-index: 2;
            }
            .zone-circle {
                width: 18px;
                height: 18px;
                border-radius: 50%;
                margin: 0 auto 8px auto;
            }
            .entry-node .zone-circle { background: #2563eb; }
            .hallway-node .zone-circle { background: #16a34a; }
            .room-node .zone-circle { background: #9333ea; }

            .entry-node {
                left: 8%;
                top: 40%;
            }
            .hallway-node {
                left: 40%;
                top: 15%;
            }
            .room-node {
                right: 8%;
                top: 40%;
            }

            .path-line {
                position: absolute;
                height: 4px;
                background: repeating-linear-gradient(
                    to right,
                    #cbd5e1 0px,
                    #cbd5e1 10px,
                    transparent 10px,
                    transparent 18px
                );
                top: 50%;
                transform: translateY(-50%);
                border-radius: 4px;
                z-index: 1;
            }
            .line-1 {
                left: 22%;
                width: 22%;
            }
            .line-2 {
                left: 51%;
                width: 22%;
            }

            #trail-layer {
                position: absolute;
                inset: 0;
                z-index: 3;
                pointer-events: none;
            }

            .trail-dot {
                position: absolute;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: rgba(239, 68, 68, 0.7);
                transform: translate(-50%, -50%);
                transition: opacity 0.8s ease;
            }

            .person-marker {
                position: absolute;
                width: 34px;
                height: 34px;
                border-radius: 50%;
                background: white;
                border: 2px solid #ef4444;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                left: 10%;
                top: 48%;
                transform: translate(-50%, -50%);
                transition: left 0.9s ease, top 0.9s ease;
                z-index: 4;
            }

            .path-text {
                margin-top: 16px;
                font-size: 15px;
                line-height: 1.6;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                background: white;
                border-radius: 14px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            }
            th, td {
                padding: 12px;
                border-bottom: 1px solid #e5e7eb;
                text-align: left;
                font-size: 14px;
            }
            th {
                background: #eef2f7;
            }
            tr:hover {
                background: #fafafa;
            }

            @media (max-width: 900px) {
                .middle-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <h1>Smart Room Activity Dashboard</h1>
        <p class="muted">Live overview of PIR motion events collected by the ESP32 system. Updates every 3 seconds.</p>

        <div class="top-grid">
            <div class="card">
                <div>Total Motion Events</div>
                <div class="big-number" id="total-events">0</div>
            </div>

            <div class="card">
                <div>Most Active Zone</div>
                <div class="big-number" id="most-active-zone">N/A</div>
            </div>

            <div class="card">
                <div>Longest Total Activity</div>
                <div class="big-number" id="longest-zone">N/A</div>
            </div>

            <div class="card">
                <div>Total Recorded Time</div>
                <div class="big-number" id="total-time">0s</div>
            </div>
        </div>

        <div class="middle-grid">
            <div>
                <h2 class="section-title">Zone Summary</h2>
                <div class="summary-grid" id="zone-summary"></div>

                <h2 class="section-title">Zone Activity Chart</h2>
                <div class="chart-card" id="zone-chart"></div>
            </div>

            <div>
                <h2 class="section-title">Recent Movement Path</h2>
                <div class="movement-card">
                    <div class="muted">Estimated path from events in the last 20 seconds.</div>

                    <div class="map-box">
                        <div class="path-line line-1"></div>
                        <div class="path-line line-2"></div>

                        <div class="zone-node entry-node">
                            <div class="zone-circle"></div>
                            Entry
                        </div>

                        <div class="zone-node hallway-node">
                            <div class="zone-circle"></div>
                            Hallway
                        </div>

                        <div class="zone-node room-node">
                            <div class="zone-circle"></div>
                            Room
                        </div>

                        <div id="trail-layer"></div>
                        <div class="person-marker" id="person-marker">🚶</div>
                    </div>

                    <div class="path-text" id="path-text">Recent Path: No recent movement</div>
                </div>
            </div>
        </div>

        <h2 class="section-title">Recent Motion Events</h2>

        <div class="filter-box">
            <label for="time-window"><strong>Show table data from:</strong></label>
            <select id="time-window">
                <option value="20s">Last 20 seconds</option>
                <option value="1m" selected>Last 1 minute</option>
                <option value="5m">Last 5 minutes</option>
                <option value="1h">Last 1 hour</option>
                <option value="1d">Last 1 day</option>
                <option value="all">All time</option>
            </select>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Sensor ID</th>
                    <th>Zone</th>
                    <th>Duration (ms)</th>
                    <th>Duration (sec)</th>
                    <th>Status</th>
                    <th>Received UTC</th>
                </tr>
            </thead>
            <tbody id="events-table"></tbody>
        </table>

        <script>
            function titleCase(text) {
                if (!text) return "N/A";
                return text.charAt(0).toUpperCase() + text.slice(1);
            }

            function zoneColorClass(zone) {
                if (zone === "entry") return "entry-bar";
                if (zone === "hallway") return "hallway-bar";
                return "room-bar";
            }

            function zonePosition(zone) {
                if (zone === "entry") return { left: 10, top: 48 };
                if (zone === "hallway") return { left: 45, top: 23 };
                if (zone === "room") return { left: 84, top: 48 };
                return { left: 10, top: 48 };
            }

            function getWindowMilliseconds(value) {
                if (value === "20s") return 20 * 1000;
                if (value === "1m") return 60 * 1000;
                if (value === "5m") return 5 * 60 * 1000;
                if (value === "1h") return 60 * 60 * 1000;
                if (value === "1d") return 24 * 60 * 60 * 1000;
                return null;
            }

            function getFilteredEvents(events) {
                const selected = document.getElementById("time-window").value;
                const windowMs = getWindowMilliseconds(selected);

                if (windowMs === null) {
                    return events;
                }

                const now = new Date();
                return events.filter(event => {
                    if (!event.received_at_utc) return false;
                    const eventTime = new Date(event.received_at_utc);
                    return (now - eventTime) <= windowMs;
                });
            }

            function getMovementEvents(events) {
                const now = new Date();
                return events.filter(event => {
                    if (!event.received_at_utc) return false;
                    const eventTime = new Date(event.received_at_utc);
                    return (now - eventTime) <= 20000;
                });
            }

            function updateMovementPath(movementEvents) {
                const recentEvents = movementEvents.slice().reverse();

                const cleaned = [];
                for (const event of recentEvents) {
                    const zone = event.zone_name;
                    if (!zone) continue;

                    if (cleaned.length === 0 || cleaned[cleaned.length - 1].zone !== zone) {
                        cleaned.push({
                            zone: zone,
                            time: event.received_at_utc
                        });
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

            async function loadDashboard() {
                const response = await fetch('/events');
                const events = await response.json();

                let totalDuration = 0;
                const zoneStats = {};

                for (const event of events) {
                    const zone = event.zone_name || "unknown";
                    const duration = parseFloat(event.duration_seconds || 0);
                    totalDuration += duration;

                    if (!zoneStats[zone]) {
                        zoneStats[zone] = {
                            count: 0,
                            total_duration: 0
                        };
                    }

                    zoneStats[zone].count += 1;
                    zoneStats[zone].total_duration += duration;
                }

                let mostActiveZone = "N/A";
                let mostEvents = 0;
                let longestZone = "N/A";
                let longestDuration = 0;

                for (const zone in zoneStats) {
                    if (zoneStats[zone].count > mostEvents) {
                        mostEvents = zoneStats[zone].count;
                        mostActiveZone = zone;
                    }

                    if (zoneStats[zone].total_duration > longestDuration) {
                        longestDuration = zoneStats[zone].total_duration;
                        longestZone = zone;
                    }
                }

                document.getElementById('total-events').textContent = events.length;
                document.getElementById('most-active-zone').textContent = titleCase(mostActiveZone);
                document.getElementById('longest-zone').textContent = titleCase(longestZone);
                document.getElementById('total-time').textContent = totalDuration.toFixed(2) + 's';

                const summaryDiv = document.getElementById('zone-summary');
                summaryDiv.innerHTML = '';

                for (const zone in zoneStats) {
                    summaryDiv.innerHTML += `
                        <div class="summary-card">
                            <h3>${titleCase(zone)}</h3>
                            <p><strong>Events:</strong> ${zoneStats[zone].count}</p>
                            <p><strong>Total Time:</strong> ${zoneStats[zone].total_duration.toFixed(2)} sec</p>
                        </div>
                    `;
                }

                const chartDiv = document.getElementById('zone-chart');
                chartDiv.innerHTML = '';

                let maxCount = 1;
                for (const zone in zoneStats) {
                    if (zoneStats[zone].count > maxCount) {
                        maxCount = zoneStats[zone].count;
                    }
                }

                for (const zone in zoneStats) {
                    const widthPercent = (zoneStats[zone].count / maxCount) * 100;
                    chartDiv.innerHTML += `
                        <div class="bar-row">
                            <div class="bar-label">${titleCase(zone)} — ${zoneStats[zone].count} events</div>
                            <div class="bar-bg">
                                <div class="bar-fill ${zoneColorClass(zone)}" style="width: ${widthPercent}%;">
                                    ${zoneStats[zone].count}
                                </div>
                            </div>
                        </div>
                    `;
                }

                const tableFilteredEvents = getFilteredEvents(events);
                const movementEvents = getMovementEvents(events);

                const tableBody = document.getElementById('events-table');
                tableBody.innerHTML = '';

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

            document.addEventListener("DOMContentLoaded", function() {
                document.getElementById("time-window").addEventListener("change", loadDashboard);
                loadDashboard();
                setInterval(loadDashboard, 3000);
            });
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)