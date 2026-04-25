const map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

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