import { collection, getDocs, addDoc, updateDoc, doc, increment } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

const MAPILLARY_TOKEN = 'MLY|25932380179773764|6461ad3ee4bbaa749ea11493fdbe3bb2';

// Global state for location selection mode
let isSelectingLocation = false;
let currentMapForSelection = null;
let mapClickListener = null;
let currentInfoWindow = null;
let currentMarker = null;
let currentExperience = null;

async function fetchMapillaryImage(lat, lng, year, month) {
  const delta = 0.001;
  const bbox = `${lng - delta},${lat - delta},${lng + delta},${lat + delta}`;

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

function openExperienceForm() {
  if (!currentMapForSelection) return;
  
  isSelectingLocation = true;
  const mapElement = document.getElementById('map');
  mapElement.style.cursor = 'url(./locate-svgrepo-com.svg) 16 16, auto';

  const addBtn = document.getElementById('add-experience-btn');
  addBtn.style.display = 'none';

  // Remove any existing listener
  if (mapClickListener) {
    google.maps.event.removeListener(mapClickListener);
  }
  
  // Set up map click listener for location selection
  mapClickListener = currentMapForSelection.addListener('click', handleMapClick);
}

function handleMapClick(event) {
  if (!isSelectingLocation) return;

  const lat = event.latLng.lat();
  const lng = event.latLng.lng();

  // Populate the form with selected coordinates
  document.getElementById('exp-lat').value = lat.toFixed(6);
  document.getElementById('exp-lng').value = lng.toFixed(6);

  // Restore cursor and button
  const mapElement = document.getElementById('map');
  mapElement.style.cursor = 'default';
  const addBtn = document.getElementById('add-experience-btn');
  addBtn.style.display = 'block';

  // Remove the click listener
  if (mapClickListener) {
    google.maps.event.removeListener(mapClickListener);
    mapClickListener = null;
  }

  // End selection mode
  isSelectingLocation = false;

  // Show the form modal
  const modal = document.getElementById('experience-modal');
  modal.style.display = 'flex';
}

function closeExperienceForm() {
  const modal = document.getElementById('experience-modal');
  modal.style.display = 'none';
  document.getElementById('experience-form').reset();

  // If still in selection mode, exit it
  if (isSelectingLocation) {
    isSelectingLocation = false;
    const mapElement = document.getElementById('map');
    mapElement.style.cursor = 'default';
    const addBtn = document.getElementById('add-experience-btn');
    addBtn.style.display = 'block';
    
    // Remove the click listener if still active
    if (mapClickListener) {
      google.maps.event.removeListener(mapClickListener);
      mapClickListener = null;
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('experience-modal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeExperienceForm();
      }
    });
  }
});

async function submitExperience() {
  const lat = parseFloat(document.getElementById('exp-lat').value);
  const lng = parseFloat(document.getElementById('exp-lng').value);
  const year = parseInt(document.getElementById('exp-year').value);
  const month = parseInt(document.getElementById('exp-month').value);
  const comment = document.getElementById('exp-comment').value;

  if (!lat || !lng || !year || !month || !comment) {
    alert('Please fill in all fields');
    return;
  }

  try {
    const docRef = await addDoc(collection(window.db, 'experiences'), {
      lat,
      lng,
      year,
      month,
      comment,
      likes: 0,
      timestamp: new Date()
    });

    alert('Memory added successfully!');
    closeExperienceForm();
    location.reload();
  } catch (error) {
    console.error('Error adding memory:', error);
    alert('Error adding memory: ' + error.message);
  }
}

async function loadExperiencesFromFirestore(map, infoWindow) {
  try {
    const querySnapshot = await getDocs(collection(window.db, 'experiences'));
    const experiences = [];
    querySnapshot.forEach((doc) => {
      experiences.push({ ...doc.data(), id: doc.id });
    });

    console.log(`Loaded ${experiences.length} experiences from Firestore`);

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

      marker.addListener('click', async () => {
        let imageHtml = '';
        const mapillaryImage = await fetchMapillaryImage(exp.lat, exp.lng, exp.year, exp.month);
        if (mapillaryImage) {
          imageHtml = `<img src="${mapillaryImage.thumb_1024_url}" style="width: 100%; border-radius: 8px 8px 0 0; cursor: pointer;" onclick="openStreetView('${mapillaryImage.id}')" title="Click to open street view">`;
        }

        const likeButton = `<button onclick="likeExperience('${exp.id}')" style="background: white; color: #000; border: 2px solid #000; padding: 8px 12px; border-radius: 20px; cursor: pointer; margin-top: 8px; font-weight: 500; display: inline-flex; align-items: center; gap: 6px;">♡ ${exp.likes || 0}</button>`;

        infoWindow.setContent(
          `<div class="info-content">
            ${imageHtml}
            <strong>${exp.year}-${String(exp.month).padStart(2, '0')}</strong><br>
            <em>${exp.comment}</em><br>
            ${likeButton}
          </div>`
        );
        infoWindow.open(map, marker);
        
        // Store current marker, info window, and experience data for updating likes
        currentMarker = marker;
        currentInfoWindow = infoWindow;
        currentExperience = exp;
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
  } catch (error) {
    console.error('Error loading experiences from Firestore:', error);
    alert('Error loading experiences: ' + error.message);
  }
}

async function likeExperience(experienceId) {
  try {
    const docRef = doc(window.db, 'experiences', experienceId);
    await updateDoc(docRef, {
      likes: increment(1)
    });
    
    // Close the info window
    if (currentInfoWindow) {
      currentInfoWindow.close();
    }
    
    // Small delay to ensure Firestore has updated
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Fetch updated experience data
    const updatedDoc = await getDocs(collection(window.db, 'experiences'));
    let updatedExperience = null;
    
    updatedDoc.forEach((docSnap) => {
      if (docSnap.id === experienceId) {
        updatedExperience = { ...docSnap.data(), id: docSnap.id };
      }
    });
    
    // Update stored experience with new like count
    if (updatedExperience) {
      currentExperience.likes = updatedExperience.likes;
    }
    
    if (currentInfoWindow && currentMarker && currentExperience) {
      // Reopen the info window with updated like count
      let imageHtml = '';
      const mapillaryImage = await fetchMapillaryImage(currentExperience.lat, currentExperience.lng, currentExperience.year, currentExperience.month);
      if (mapillaryImage) {
        imageHtml = `<img src="${mapillaryImage.thumb_1024_url}" style="width: 100%; border-radius: 8px 8px 0 0; cursor: pointer;" onclick="openStreetView('${mapillaryImage.id}')" title="Click to open street view">`;
      }
      
      const updatedLikeButton = `<button onclick="likeExperience('${currentExperience.id}')" style="background: white; color: #000; border: 2px solid #000; padding: 8px 12px; border-radius: 20px; cursor: pointer; margin-top: 8px; font-weight: 500; display: inline-flex; align-items: center; gap: 6px;">♡ ${currentExperience.likes || 0}</button>`;
      
      currentInfoWindow.setContent(
        `<div class="info-content">
          ${imageHtml}
          <strong>${currentExperience.year}-${String(currentExperience.month).padStart(2, '0')}</strong><br>
          <em>${currentExperience.comment}</em><br>
          ${updatedLikeButton}
        </div>`
      );
      currentInfoWindow.open(currentMapForSelection, currentMarker);
    }
  } catch (error) {
    console.error('Error liking memory:', error);
    alert('Error liking memory: ' + error.message);
  }
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

  // Store map reference for location selection
  currentMapForSelection = map;

  const infoWindow = new google.maps.InfoWindow();

  // Load experiences from Firestore
  await loadExperiencesFromFirestore(map, infoWindow);
}

window.initMap = initMap;
window.openStreetView = openStreetView;
window.closeStreetView = closeStreetView;
window.openExperienceForm = openExperienceForm;
window.closeExperienceForm = closeExperienceForm;
window.submitExperience = submitExperience;
window.likeExperience = likeExperience;
window.handleMapClick = handleMapClick;
