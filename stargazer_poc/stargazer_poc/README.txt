StarGazer Proof of Concept (POC)

What it does
------------
- Simple Flask + Skyfield backend computes which major planets are above the horizon "now"
  for a given latitude/longitude.
- Frontend page grabs your device location and shows a visibility list.

Quick Start
-----------
1) (Recommended) Create and activate a virtual environment:

   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate

2) Install dependencies:

   pip install -r requirements.txt

   NOTE: On first run, Skyfield will download an ephemeris file 'de421.bsp' (~20 MB).
   Keep internet on for that initial download.

3) Run the dev server:

   python app.py

4) Open your browser at:

   http://localhost:5000

5) Click "Use My Location" or enter lat/lon manually and press "Fetch Visibility".

Tech Notes
----------
- Visibility rule is intentionally simple for the POC:
  A planet is "visible now" if its altitude > 5° and the Sun altitude < -6° (civil twilight).
- For production, consider caching ephemeris data and adding constellations/star catalogs.
