// Toggle navbar for mobile view
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
});

// Initialize the map
const map = L.map('map', {
    minZoom: 4,
    maxZoom: 20,
    zoomSnap: 0.5
}).setView([15.498, 73.828], 15); // Set initial view to Panjim

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Define the police icon
const policeIcon = L.icon({
    iconUrl: '/static/img/policeman.png', // Ensure this path is correct
    iconSize: [50, 100], // size of the icon
    iconAnchor: [25, 75], // point of the icon which will correspond to marker's location
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});

// Create feature groups for markers and duty circles
const officergroup = L.featureGroup().addTo(map);
const dutygroup = L.featureGroup().addTo(map);

// Function to fetch the officer data
function fetchOfficerData() {
    fetch('/static/map/combinedpoldat.json')  // Use the new endpoint
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        combinedJsonData = data.reverse(); // Reverse the fetched data
        console.log('Data fetched and reversed successfully:', combinedJsonData);

        // Clear previous markers and circles
        officergroup.clearLayers();
        dutygroup.clearLayers();

        const off_set = new Set();

        data.forEach(item => {
            // Check if coordinates are available
            if (typeof item.coords_lat === 'undefined' || typeof item.coords_long === 'undefined') {
                return;
            }

            // Ensure each officer is only added once
            if (off_set.has(item.off_name)) {
                return;
            }

            off_set.add(item.off_name);

            // Create a marker for the current officer's location
            const currentMarker = L.marker([item.coords_lat, item.coords_long], { icon: policeIcon }).addTo(officergroup);

            // Create a circle for the duty area
            const dutyCircle = L.circle([item.duty_lat, item.duty_long], {
                radius: item.range,
                color: 'red', // Default color
                fillColor: '#f03',
                fillOpacity: 0.5
            }).addTo(dutygroup);

            // Check if the officer is inside the duty circle
            const isInside = map.distance(
                L.latLng(item.coords_lat, item.coords_long),
                L.latLng(item.duty_lat, item.duty_long)
            ) <= item.range;

            // Update the circle's color based on the officer's status
            dutyCircle.setStyle({
                color: isInside ? 'blue' : 'red',
                fillColor: isInside ? '#30a3e6' : '#bd1122'
            });

            // Bind popup to the marker
            currentMarker.bindPopup(`
                Officer: ${item.off_name}<br>
                Current Location: (${item.coords_lat.toFixed(4)}, ${item.coords_long.toFixed(4)})<br>
                Duty Location: (${item.duty_lat.toFixed(4)}, ${item.duty_long.toFixed(4)})<br>
                Status: ${isInside ? "Inside" : "Outside"} the duty circle`);
        });

        // Fit map to officer markers
        const offbounds = officergroup.getBounds();
        if (offbounds.isValid()) {
            map.fitBounds(offbounds);
        } else {
            console.error('Invalid bounds:', offbounds);
        }
    })
    .catch(error => console.error('Error fetching the JSON:', error));
}

// Fetch the officer data every 5 seconds
setInterval(fetchOfficerData, 5000);
