// Toggle navbar for mobile view
const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");

hamburger.addEventListener("click", () => {
  navMenu.classList.toggle("active");
});

// Initialize the map
const map = L.map("map", {
  minZoom: 4,
  maxZoom: 20,
  zoomSnap: 0.5,
}).setView([15.498, 73.828], 15); // Set initial view to Panjim

// Add OpenStreetMap tiles
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// Define the police icon
const policeIcon = L.icon({
  iconUrl: "/static/img/policeman.png", // Ensure this path is correct
  iconSize: [50, 100], // size of the icon
  iconAnchor: [25, 75], // point of the icon which will correspond to marker's location
  popupAnchor: [-3, -76], // point from which the popup should open relative to the iconAnchor
});

// Create feature groups for markers and duty circles
const officergroup = L.featureGroup().addTo(map);
const dutygroup = L.featureGroup().addTo(map);
let prevLoc = [15.4989, 73.8278];
let startCircle;

// Function to fetch the officer data
function fetchOfficerData() {
  fetch("/static/map/policedata.json") // Use the new endpoint
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      combinedJsonData = data.reverse(); // Reverse the fetched data
      console.log("Data fetched and reversed successfully:", combinedJsonData);

      // Clear previous markers and circles
      officergroup.clearLayers();
      dutygroup.clearLayers();

      const off_set = new Set();
      const circleRadius = 100; // Define the radius for the starting circle (in meters)

      data.forEach((item) => {
        // Check if coordinates are available
        if (
          typeof item.coords_lat === "undefined" ||
          typeof item.coords_long === "undefined"
        ) {
          return;
        }

        // Ensure each officer is only added once
        if (off_set.has(item.off_name)) {
          return;
        }

        off_set.add(item.off_name);

        // Check if there's a previous location to display
        if (prevLoc[0] !== 0 || prevLoc[1] !== 0) {
          // Create a marker for the previous officer's location
          const prevMarker = L.marker(prevLoc)
            .addTo(officergroup)
            .bindPopup(
              `Previous Location: (${prevLoc[0].toFixed(6)}, ${prevLoc[1].toFixed(6)})`,
            );
        }

        // Create a marker for the current officer's location
        const currentMarker = L.marker([item.coords_lat, item.coords_long], {
          icon: policeIcon,
        }).addTo(officergroup);

        prevLoc = [item.coords_lat, item.coords_long];

        // If the starting circle doesn't exist yet, create it
        if (!startCircle) {
          startCircle = L.circle(prevLoc, {
            radius: circleRadius,
            color: "blue", // Initial color of the circle is blue
            fillColor: "#30a3e6",
            fillOpacity: 0.5,
          }).addTo(map);

          // Zoom into the starting location and set the view
          map.setView(prevLoc, 16); // Set view to prevLoc with a zoom level of 16
        }

        // Check if the current marker is outside the starting circle
        const distance = map.distance(
          L.latLng(item.coords_lat, item.coords_long),
          L.latLng(prevLoc[0], prevLoc[1]),
        );

        if (distance > circleRadius) {
          // Change circle color to red if outside the circle
          startCircle.setStyle({
            color: "red",
            fillColor: "#bd1122",
          });
        } else {
          // Keep the circle blue if inside the circle
          startCircle.setStyle({
            color: "blue",
            fillColor: "#30a3e6",
          });
        }
        /*
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
                Current Location: (${item.coords_lat.toFixed(6)}, ${item.coords_long.toFixed(6)})<br>
                Duty Location: (${item.duty_lat.toFixed(6)}, ${item.duty_long.toFixed(6)})<br>
                Status: ${isInside ? "Inside" : "Outside"} the duty circle`);
            });*/
        currentMarker.bindPopup(`
                Officer: ${item.off_name}<br>
                Current Location: (${item.coords_lat.toFixed(6)}, ${item.coords_long.toFixed(6)})<br>`);
      });

      /*
        // Fit map to officer markers
        const offbounds = officergroup.getBounds();
        if (offbounds.isValid()) {
            map.fitBounds(offbounds);
        } else {
            console.error('Invalid bounds:', offbounds);
        }
            */
    })
    .catch((error) => console.error("Error fetching the JSON:", error));
}

// Fetch the officer data every 5 seconds
setInterval(fetchOfficerData, 5000);
