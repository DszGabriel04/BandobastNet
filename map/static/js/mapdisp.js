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

/*
// Add a marker for the duty location (static)
const dutyLocation = [15.4909, 73.8278]; // Example coordinates for duty
const dutyRadius = 500; // Example radius in meters

const dutyCircle = L.circle(dutyLocation, {
    radius: dutyRadius,
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5
}).addTo(map);
*/

// Real-time tracking of officer's location
let officerMarker;
let combinedJsonData;

// Fetch the JSON data
fetch('/static/map/combinedpoldat.json')
    .then(response => {
        // Check if the response is ok (status in the range 200-299)
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        combinedJsonData = data; // Store the fetched data in the variable
        console.log('Data fetched successfully:', combinedJsonData);

        // Now that we have the data, we can process it
        const officergroup = L.featureGroup().addTo(map); // Create a feature group to hold markers
        const dutygroup = L.featureGroup().addTo(map); // Create a feature group to hold markers
        const off_set = new Set()
        combinedJsonData.forEach(item => {
            // Create a marker for the current coordinates
            if (typeof item.coords_lat === 'undefined' || typeof item.coords_long === 'undefined'){
                return;
            }

            if(off_set.has(item.off_name)){
                return;
            }

            off_set.add(item.off_name);
            const currentMarker = L.marker([item.coords_lat, item.coords_long], {icon: policeIcon}).addTo(officergroup);
            
            // Create a circle for the duty area
            const dutyCircle = L.circle([item.duty_lat, item.duty_long], {
                radius: item.range,
                color: 'red', // Default color
                fillColor: '#f03',
                fillOpacity: 0.5
            }).addTo(dutygroup);

            
            // Check if the current coordinates are inside the duty circle
            const isInside = map.distance(
                L.latLng(item.coords_lat, item.coords_long),
                L.latLng(item.duty_lat, item.duty_long)
            ) <= item.range;

            // Change the color based on whether it's inside the duty circle
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

            // Fit the map bounds to include all markers
            const offbounds = officergroup.getBounds();
            console.log('Bounds:', offbounds);

            if (offbounds.isValid()) {
                map.fitBounds(offbounds);
            } else {
                console.error('Invalid bounds:', offbounds);
            }
        });
    })
    .catch(error => console.error('Error fetching the JSON:', error));
    dutygroup.addTo(map);
/*
if (navigator.geolocation) {
    navigator.geolocation.watchPosition(position => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        // Update or create officer's marker
        if (!officerMarker) {
            officerMarker = L.marker([lat, lon], { icon: policeIcon }).addTo(map);
        } else {
            officerMarker.setLatLng([lat, lon]);
        }

        // Check if officer is within the duty area
        const isInsideDutyArea = map.distance(L.latLng(lat, lon), L.latLng(dutyLocation[0], dutyLocation[1])) <= dutyRadius;

        dutyCircle.setStyle({
            color: isInsideDutyArea ? 'blue' : 'red',
            fillColor: isInsideDutyArea ? '#30a3e6' : '#bd1122'
        });

        officerMarker.bindPopup(`
            Officer's Current Location:<br>
            Latitude: ${lat.toFixed(4)}<br>
            Longitude: ${lon.toFixed(4)}<br>
            Status: ${isInsideDutyArea ? "Inside" : "Outside"} the duty area
        `).openPopup();
    }, err => {
        console.error('Error getting location:', err);
    }, {
        enableHighAccuracy: false,
        maximumAge: 10000,
        timeout: 5000
    });
} else {
    console.error("Geolocation is not supported by this browser.");
}
*/
