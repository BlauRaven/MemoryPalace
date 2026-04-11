const MAPILLARY_TOKEN = 'MLY|25932380179773764|6461ad3ee4bbaa749ea11493fdbe3bb2';

async function fetchMapillaryImage(lat, lng, year, month) {
  const delta = 0.001;
  const bbox = `${lng - delta},${lat - delta},${lng + delta},${lat + delta}`;

  // Compute ±6 month window, handling year rollover
  let startMonth = month - 6;
  let startYear = year;
  if (startMonth < 1) { startMonth += 12; startYear--; }
  let endMonth = month + 6;
  let endYear = year;
  if (endMonth > 12) { endMonth -= 12; endYear++; }

  const startTime = `${startYear}-${String(startMonth).padStart(2, '0')}-01T00:00:00Z`;
  const endTime = `${endYear}-${String(endMonth).padStart(2, '0')}-28T23:59:59Z`;

  const url = `https://graph.mapillary.com/images?access_token=${MAPILLARY_TOKEN}&fields=id,thumb_1024_url,captured_at&bbox=${bbox}&start_time=${startTime}&end_time=${endTime}&limit=1`;

  try {
    const res = await fetch(url);
    if (!res.ok) return null;
    const json = await res.json();
    if (json.data && json.data.length > 0) return json.data[0];
    return null;
  } catch (e) {
    console.error("Mapillary fetch error:", e);
    return null;
  }
}

function openStreetView(imageId) {
  const overlay = document.getElementById('street-view-overlay');
  const iframe = document.getElementById('street-view-iframe');
  iframe.src = `https://www.mapillary.com/embed?image_key=${imageId}`;
  overlay.style.display = 'flex';
}

function closeStreetView() {
  const overlay = document.getElementById('street-view-overlay');
  const iframe = document.getElementById('street-view-iframe');
  overlay.style.display = 'none';
  iframe.src = '';
}

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

          const buildContent = (visitBtn) => `
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
              ${visitBtn}
            </div>`;

          infoWindow.setContent(buildContent(''));
          infoWindow.open(map, marker);

          fetchMapillaryImage(exp.lat, exp.lng, exp.year, exp.month).then(img => {
            if (img) {
              const btn = `<button onclick="openStreetView('${img.id}')" style="
                margin-top: 8px;
                padding: 5px 14px;
                background: #4285F4;
                color: #fff;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                cursor: pointer;
                font-family: sans-serif;
              ">Visit</button>`;
              infoWindow.setContent(buildContent(btn));
            }
          });
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
