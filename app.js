async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");

  const map = new Map(document.getElementById("map"), {
    center: { lat: 20, lng: 0 },
    zoom: 2,
    minZoom: 2,
    maxZoom: 20,
    disableDefaultUI: true,
    gestureHandling: "greedy",
    isFractionalZoomEnabled: true,
    restriction: {
      latLngBounds: { north: 85, south: -85, west: -180, east: 180 },
      strictBounds: true
    },
    styles: [
      { elementType: "labels", stylers: [{ visibility: "off" }] },
      { elementType: "geometry", stylers: [{ color: "#F64A8A" }] },
      { featureType: "landscape", elementType: "geometry", stylers: [{ color: "#feead5" }] },
      { featureType: "administrative", elementType: "geometry", stylers: [{ color: "#b0b0b0" }] },
      { featureType: "poi", stylers: [{ visibility: "off" }] },
      { featureType: "road", elementType: "geometry", stylers: [{ color: "#F85E9D" }] },
      { featureType: "road", elementType: "labels", stylers: [{ visibility: "off" }] },
      { featureType: "transit", stylers: [{ visibility: "off" }] },
      { featureType: "water", elementType: "geometry", stylers: [{ color: "#d0e0e3" }] },
      { featureType: "administrative.country", elementType: "labels.text", stylers: [{ visibility: "on" }] },
      { featureType: "administrative.country", elementType: "labels.text.fill", stylers: [{ color: "#ffffff" }] },
      { featureType: "administrative.country", elementType: "labels.text.stroke", stylers: [{ color: "#444444" }, { weight: 2 }] },
      { featureType: "administrative.province", elementType: "labels.text", stylers: [{ visibility: "on" }] },
      { featureType: "administrative.province", elementType: "labels.text.fill", stylers: [{ color: "#ffffff" }] },
      { featureType: "administrative.province", elementType: "labels.text.stroke", stylers: [{ color: "#444444" }, { weight: 2 }] },
      { featureType: "water", elementType: "labels.text", stylers: [{ visibility: "on" }] },
      { featureType: "water", elementType: "labels.text.fill", stylers: [{ color: "#f0d5f0" }] },
      { featureType: "water", elementType: "labels.text.stroke", stylers: [{ color: "#5a3d5f" }, { weight: 2 }] }
    ]
  });

  const infoWindow = new google.maps.InfoWindow();

  fetch("experiences.json")
    .then(response => response.json())
    .then(experiences => {
      experiences.forEach(exp => {
        const marker = new google.maps.Marker({
          map,
          position: { lat: exp.lat, lng: exp.lng },
          icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 3,
            fillColor: '#000000',
            fillOpacity: 1,
            strokeWeight: 0
          }
        });

        marker.addListener("click", () => {
          const monthNames = ["", "January", "February", "March", "April", "May", "June", 
            "July", "August", "September", "October", "November", "December"];
          const monthYear = `${monthNames[exp.month]} ${exp.year}`;
          const content = `
            <div style="
              padding: 12px 16px;
              font-family: sans-serif;
              min-width: 160px;
              border-left: 4px solid #4285F4;
            ">
              <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #888; margin-bottom: 4px;">
                ${monthYear}
              </div>
              <div style="font-size: 14px; color: #222; line-height: 1.4;">
                ${exp.comment}
              </div>
              <div style="margin-top: 8px; font-size: 12px; color: #888;">
                ♥ ${exp.likes.toLocaleString()} likes
              </div>
            </div>`;
          infoWindow.setContent(content);
          infoWindow.open(map, marker);
        });

        marker.addListener("mouseover", () => {
          marker.setIcon({
            path: google.maps.SymbolPath.CIRCLE,
            scale: 3,
            fillColor: '#87CEEB',
            fillOpacity: 1,
            strokeWeight: 0
          });
        });

        marker.addListener("mouseout", () => {
          marker.setIcon({
            path: google.maps.SymbolPath.CIRCLE,
            scale: 3,
            fillColor: '#000000',
            fillOpacity: 1,
            strokeWeight: 0
          });
        });
      });
    })
    .catch(err => console.error("Error loading experiences:", err));
}

window.initMap = initMap;
