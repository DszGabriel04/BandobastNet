document.addEventListener("DOMContentLoaded", function () {
  // retrieve tracking button
  const trackingButton = document.getElementById("trackingButton");
  trackingButton.addEventListener("click", startTrackingLocation);
});

function startTrackingLocation() {
  console.log("Button clicked, starting location tracking...");

  if (navigator.geolocation) {
    navigator.geolocation.watchPosition(
      function (position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        document.getElementById("locationDisplay").innerHTML = `
                    Latitude: ${latitude} <br>
                    Longitude: ${longitude}
                `;

        // Send the location to the server
        sendLocationToServer(latitude, longitude);
      },
      function (error) {
        console.error("Error obtaining location: ", error);
        alert("Error obtaining location: " + error.message); // Show the error message.
      },
      {
        enableHighAccuracy: true,
        maximumAge: 30000,
        timeout: 27000,
      },
    );
  } else {
    alert("Geolocation is not supported by this browser.");
  }
}

function sendLocationToServer(latitude, longitude) {
  const data = {
    latitude: latitude,
    longitude: longitude,
  };

  console.log("Sending location to server:", data); // Debugging log

  fetch("/track-location/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token if necessary
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Location sent successfully:", data);
    })
    .catch((error) => {
      console.error("Error sending location to server:", error);
    });
}

// Function to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
