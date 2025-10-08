from flask import Flask, request, jsonify, render_template
from skyfield.api import load, wgs84
import math

app = Flask(__name__)

# Load timescale and ephemeris once (Skyfield will download 'de421.bsp' on first run)
ts = load.timescale()
eph = load('de421.bsp')

# Planet keys available in de421 (barycenters are fine for a POC)
PLANETS = {
    "Mercury": "mercury",
    "Venus": "venus",
    "Mars": "mars",
    "Jupiter": "jupiter barycenter",
    "Saturn": "saturn barycenter",
    "Uranus": "uranus barycenter",
    "Neptune": "neptune barycenter"
}

def compute_visibility(lat: float, lon: float):
    """Return a simple visibility report for major planets at current time."""
    t = ts.now()
    topos = wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon)

    # Sun altitude to estimate darkness
    sun = eph['sun']
    sun_alt, sun_az, _ = topos.at(t).observe(sun).apparent().altaz()

    report = []
    for name, key in PLANETS.items():
        body = eph[key]
        alt, az, distance = topos.at(t).observe(body).apparent().altaz()
        visible = (alt.degrees > 5) and (sun_alt.degrees < -6)  # >5° and civil twilight or darker
        report.append({
            "name": name,
            "altitude_deg": round(alt.degrees, 2),
            "azimuth_deg": round(az.degrees, 2),
            "distance_au": round(distance.au, 3),
            "visible_now": bool(visible)
        })

    return {
        "sun_altitude_deg": round(sun_alt.degrees, 2),
        "location": {"lat": lat, "lon": lon},
        "timestamp": t.utc_strftime("%Y-%m-%d %H:%M:%S UTC"),
        "planets": report
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/visible")
def visible():
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
    except (TypeError, ValueError):
        return jsonify({"error": "Please supply numeric lat and lon query params"}), 400
    data = compute_visibility(lat, lon)
    return jsonify(data)

if __name__ == "__main__":
    # For local dev only
    app.run(host="0.0.0.0", port=5000, debug=True)
