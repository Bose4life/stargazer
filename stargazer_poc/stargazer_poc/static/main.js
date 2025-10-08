async function fetchVisibility(lat, lon) {
  const status = document.getElementById("status");
  const results = document.getElementById("results");
  status.textContent = "Loading…";
  results.innerHTML = "";

  try {
    const resp = await fetch(`/visible?lat=${lat}&lon=${lon}`);
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || "Request failed");

    status.innerHTML = `<div class="card"><strong>Time:</strong> ${data.timestamp}<br><strong>Sun Altitude:</strong> ${data.sun_altitude_deg}°</div>`;

    data.planets.forEach(p => {
      const div = document.createElement("div");
      div.className = "card";
      div.innerHTML = `
        <h3>${p.name} <span class="pill ${p.visible_now ? "ok" : "no"}">${p.visible_now ? "Visible now" : "Not visible"}</span></h3>
        <div>Altitude: <code>${p.altitude_deg}°</code></div>
        <div>Azimuth: <code>${p.azimuth_deg}°</code></div>
        <div>Distance: <code>${p.distance_au} AU</code></div>
      `;
      results.appendChild(div);
    });
  } catch (e) {
    status.textContent = "Error: " + e.message;
  }
}

document.getElementById("useLocation").addEventListener("click", () => {
  if (!navigator.geolocation) {
    alert("Geolocation not supported.");
    return;
  }
  navigator.geolocation.getCurrentPosition(
    pos => {
      const lat = pos.coords.latitude.toFixed(6);
      const lon = pos.coords.longitude.toFixed(6);
      document.getElementById("lat").value = lat;
      document.getElementById("lon").value = lon;
      fetchVisibility(lat, lon);
    },
    err => alert("Location error: " + err.message),
    { enableHighAccuracy: true, timeout: 10000 }
  );
});

document.getElementById("fetchBtn").addEventListener("click", () => {
  const lat = parseFloat(document.getElementById("lat").value);
  const lon = parseFloat(document.getElementById("lon").value);
  if (Number.isNaN(lat) || Number.isNaN(lon)) {
    alert("Enter numeric latitude and longitude");
    return;
  }
  fetchVisibility(lat, lon);
});
