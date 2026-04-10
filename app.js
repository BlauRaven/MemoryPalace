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
          infoWindow.setContent('<div class="info-content">' + exp.comment + '</div>');
          infoWindow.open(map, marker);
        });
      });
    })
    .catch(err => console.error("Error loading experiences:", err));
}

window.initMap = initMap;
