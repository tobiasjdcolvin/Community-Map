const map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);
window.addEventListener('load', () => {
  map.invalidateSize();
  loadMarkers();
});

const markerLayer = L.layerGroup().addTo(map); // add this

document.getElementById("symptoms-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const symptoms = {
    cough_congestion: document.getElementById("cough_congestion").checked,
    nausea_vomiting: document.getElementById("nausea_vomiting").checked,
    difficulty_breathing: document.getElementById("difficulty_breathing").checked,
    sore_throat: document.getElementById("sore_throat").checked,
    rash: document.getElementById("rash").checked,
    fever: document.getElementById("fever").checked,
    chills: document.getElementById("chills").checked,
    diarrhea: document.getElementById("diarrhea").checked,
    attending_a_recent_mass_gathering: document.getElementById("attending_a_recent_mass_gathering").checked,
    history_of_travel: document.getElementById("history_of_travel").checked,
  };

  const city = document.getElementById("input_city").value;
  const state = document.getElementById("input_state_province").value;
  const country = document.getElementById("input_country").value;

  // Store payload and redirect to loading page
  sessionStorage.setItem("pendingSubmit", JSON.stringify({ symptoms, city, state, country }));
  window.location.href = "/test";
});

const SYMPTOM_COLORS = {
    cough_congestion:                { fill: '#4E9AF1', border: '#1A5FAD' },
    nausea_vomiting:                 { fill: '#F4A623', border: '#B8720A' },
    difficulty_breathing:            { fill: '#E05C5C', border: '#9E2020' },
    sore_throat:                     { fill: '#9B59B6', border: '#6C3483' },
    rash:                            { fill: '#2ECC71', border: '#1A7A44' },
    fever:                           { fill: '#E74C3C', border: '#922B21' },
    chills:                          { fill: '#1ABC9C', border: '#0E6655' },
    diarrhea:                        { fill: '#E67E22', border: '#935116' },
    attending_a_recent_mass_gathering: { fill: '#F1C40F', border: '#9A7D0A' },
    history_of_travel:               { fill: '#EC407A', border: '#880E4F' },
};


// One layer group per symptom
const symptomLayers = {};
Object.keys(SYMPTOM_COLORS).forEach(symptom => {
    symptomLayers[symptom] = L.layerGroup().addTo(map);
});

async function loadMarkers() {
    // Clear all layers
    Object.values(symptomLayers).forEach(layer => layer.clearLayers());

    // Fetch all symptoms in parallel
    const fetches = Object.keys(SYMPTOM_COLORS).map(symptom =>
        api(`/api/locations?symptom=${symptom}`).then(locations => ({ symptom, locations }))
    );

    const results = await Promise.all(fetches);

    results.forEach(({ symptom, locations }) => {
        const { fill, border } = SYMPTOM_COLORS[symptom];
        locations.forEach(u => {
            L.circleMarker([u.lat, u.lon], {
                radius: 8,
                fillColor: fill,
                color: border,
                weight: 1.5,
                fillOpacity: 0.6,  // slight transparency helps overlapping markers show through
            })
            .bindPopup(`<b>${symptom.replaceAll('_', ' ')}</b><br>Reports: ${u.count}`)
            .addTo(symptomLayers[symptom]);
        });
    });
}

/*
async function loadMarkers() {
    markerLayer.clearLayers()
    const locations = await api("/api/locations")
    locations.forEach(u => {
        L.circleMarker([u.lat, u.lon], {
            radius: 8,
            fillColor: '#378ADD',
            color: '#185FA5',
            weight: 1.5,
            fillOpacity: 0.8
        }).bindPopup(`Reports: ${u.count}`).addTo(markerLayer)
    })
}
*/


async function api(path, options = {}) {
    const res = await fetch(path, {
        headers: { "Content-Type": "application/json" },
        ...options,
        body: options.body ? JSON.stringify(options.body) : undefined,
    })
    if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`)
    return res.json()
}