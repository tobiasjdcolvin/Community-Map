const map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

const markerLayer = L.layerGroup().addTo(map); // add this

document.getElementById("submit-btn").addEventListener("click", async () => {
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
    }

    const city = document.getElementById("input_city").value
    const state = document.getElementById("input_state_province").value
    const country = document.getElementById("input_country").value

    try {
        const result = await api(`/api/symptoms?city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}&country=${encodeURIComponent(country)}`, { 
            method: "POST", 
            body: symptoms 
        })
        console.log("Saved:", result)
        loadMarkers() // refresh map after submit
    } catch (e) {
        console.error("Failed:", e.message)
    }
})

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


async function api(path, options = {}) {
    const res = await fetch(path, {
        headers: { "Content-Type": "application/json" },
        ...options,
        body: options.body ? JSON.stringify(options.body) : undefined,
    })
    if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`)
    return res.json()
}

loadMarkers()