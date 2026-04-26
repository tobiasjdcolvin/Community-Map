const map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

document.getElementById("submit-btn").addEventListener("click", async () => {
    const symptoms = {
        cough_congestion: document.getElementById("cough_congestion").checked,
        nausea_vomiting:     document.getElementById("nausea_vomiting").checked,
        difficulty_breathing:     document.getElementById("difficulty_breathing").checked,
        sore_throat:     document.getElementById("sore_throat").checked,
        rash:     document.getElementById("rash").checked,
        fever:     document.getElementById("fever").checked,
        chills:     document.getElementById("chills").checked,
        diarrhea:     document.getElementById("diarrhea").checked,
        attending_a_recent_mass_gathering:     document.getElementById("attending_a_recent_mass_gathering").checked,
        history_of_travel:     document.getElementById("history_of_travel").checked,        
    }   

    try {
        const result = await api("/api/symptoms", { method: "POST", body: symptoms })
        console.log("Saved:", result)
    } catch (e) {
        console.error("Failed:", e.message)
    }
})

const users = [
  { lat: 47.6062, lng: -122.3321, label: "Seattle" },
  { lat: 51.5074, lng: -0.1278,   label: "London" },
  { lat: 35.6762, lng: 139.6503,  label: "Tokyo" },
  { lat: -33.8688, lng: 151.2093, label: "Sydney" },
  { lat: 48.8566, lng: 2.3522,    label: "Paris" },
  { lat: 40.7128, lng: -74.0060,  label: "New York" },
];

users.forEach(u => {
  L.circleMarker([u.lat, u.lng], {
    radius: 8,
    fillColor: '#378ADD',
    color: '#185FA5',
    weight: 1.5,
    fillOpacity: 0.8
  }).bindPopup(u.label).addTo(map);
});

async function api(path, options = {}) {
    const res = await fetch(path, {
        headers: { "Content-Type": "application/json" },
        ...options,
        body: options.body ? JSON.stringify(options.body) : undefined,
    })
    if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`)
    return res.json()
}