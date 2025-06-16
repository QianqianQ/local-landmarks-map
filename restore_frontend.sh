#!/bin/bash
# Quick frontend restoration script

cd frontend

# Kill any hanging build processes
pkill -9 -f "ng build" 2>/dev/null || true
sleep 2

# Clean and recreate dist directory
rm -rf dist/landmarks-map
mkdir -p dist/landmarks-map

# Create a minimal index.html with the new category filter components
cat > dist/landmarks-map/index.html << 'EOF'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Local Landmarks Map</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css">
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css">
  <style>
    .map { height: calc(100vh - 56px); width: 100%; }
    .map-container { position: relative; }
    .map-controls { z-index: 1000; }
    .landmark-popup { max-width: 300px; }
    .loading-overlay {
      position: fixed; top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0,0,0,0.7); z-index: 2000;
      display: flex; align-items: center; justify-content: center;
      color: white; font-size: 18px;
    }
    .error-alert {
      position: fixed; top: 70px; left: 50%; transform: translateX(-50%);
      z-index: 2000; min-width: 300px;
    }
  </style>
</head>
<body>
  <!-- Navigation with Category Filter -->
  <nav class="navbar navbar-dark bg-dark border-bottom">
    <div class="container-fluid">
      <span class="navbar-brand mb-0 h1">
        <i class="fas fa-map-marker-alt me-2"></i>
        Local Landmarks Map
      </span>
      <div class="d-flex align-items-center">
        <select id="categoryFilter" class="form-select form-select-sm me-2" style="width: auto; max-width: 200px;" title="Filter landmarks by category">
          <option value="all">All Landmarks</option>
          <option value="museums">Museums & Galleries</option>
          <option value="churches">Churches & Religious</option>
          <option value="monuments">Monuments & Memorials</option>
          <option value="parks">Parks & Gardens</option>
          <option value="buildings">Historic Buildings</option>
          <option value="entertainment">Entertainment</option>
          <option value="transport">Transportation</option>
        </select>
        <button id="locateBtn" class="btn btn-outline-secondary me-2" title="Find my location">
          <i class="fas fa-location-arrow" id="locateIcon"></i>
        </button>
        <span id="landmarkCount" class="badge bg-secondary">0 landmarks</span>
      </div>
    </div>
  </nav>

  <!-- Map Container -->
  <div class="map-container">
    <div id="map" class="map"></div>
    <div class="map-controls position-absolute top-0 end-0 m-3">
      <div class="btn-group-vertical" role="group">
        <button id="refreshBtn" class="btn btn-secondary" title="Refresh landmarks">
          <i class="fas fa-sync-alt"></i>
        </button>
      </div>
    </div>
  </div>

  <!-- Loading Overlay -->
  <div id="loadingOverlay" class="loading-overlay" style="display: none;">
    <div><i class="fas fa-spinner fa-spin me-2"></i>Loading landmarks...</div>
  </div>

  <!-- Error Alert -->
  <div id="errorAlert" class="alert alert-danger error-alert" style="display: none;">
    <button type="button" class="btn-close" aria-label="Close"></button>
    <div id="errorMessage"></div>
  </div>

  <!-- Scripts -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
  <script>
    // Initialize map and functionality
    let map, markersGroup, currentCategory = 'all', isLoading = false;

    // Initialize the application
    document.addEventListener('DOMContentLoaded', function() {
      initializeMap();
      setupEventListeners();
      loadLandmarks();
    });

    function initializeMap() {
      map = L.map('map').setView([60.1695, 24.9354], 12); // Helsinki default
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(map);

      markersGroup = L.markerClusterGroup({
        chunkedLoading: true,
        maxClusterRadius: 50
      });
      map.addLayer(markersGroup);

      map.on('moveend', loadLandmarks);
      map.on('zoomend', loadLandmarks);

      // Try to get user's location
      navigator.geolocation.getCurrentPosition(
        position => {
          map.setView([position.coords.latitude, position.coords.longitude], 13);
          loadLandmarks();
        },
        error => {
          console.log('Geolocation failed:', error);
          loadLandmarks();
        }
      );
    }

    function setupEventListeners() {
      // Category filter
      document.getElementById('categoryFilter').addEventListener('change', function() {
        currentCategory = this.value;
        loadLandmarks();
      });

      // Locate button
      document.getElementById('locateBtn').addEventListener('click', function() {
        const icon = document.getElementById('locateIcon');
        icon.className = 'fas fa-spinner fa-spin';
        
        navigator.geolocation.getCurrentPosition(
          position => {
            map.setView([position.coords.latitude, position.coords.longitude], 15);
            icon.className = 'fas fa-location-arrow';
          },
          error => {
            showError('Unable to get your location: ' + error.message);
            icon.className = 'fas fa-location-arrow';
          }
        );
      });

      // Refresh button
      document.getElementById('refreshBtn').addEventListener('click', loadLandmarks);

      // Error alert close
      document.querySelector('#errorAlert .btn-close').addEventListener('click', function() {
        document.getElementById('errorAlert').style.display = 'none';
      });
    }

    function loadLandmarks() {
      if (isLoading) return;
      
      isLoading = true;
      document.getElementById('loadingOverlay').style.display = 'flex';

      const bounds = map.getBounds();
      const params = new URLSearchParams({
        north: bounds.getNorth(),
        south: bounds.getSouth(),
        east: bounds.getEast(),
        west: bounds.getWest()
      });

      if (currentCategory !== 'all') {
        params.set('category', currentCategory);
      }

      fetch(`/api/landmarks?${params}`)
        .then(response => response.json())
        .then(data => {
          displayLandmarks(data.landmarks);
          isLoading = false;
          document.getElementById('loadingOverlay').style.display = 'none';
        })
        .catch(error => {
          console.error('Error loading landmarks:', error);
          showError('Failed to load landmarks: ' + error.message);
          isLoading = false;
          document.getElementById('loadingOverlay').style.display = 'none';
        });
    }

    function displayLandmarks(landmarks) {
      markersGroup.clearLayers();
      
      const count = landmarks.length;
      document.getElementById('landmarkCount').textContent = 
        count + ' landmark' + (count !== 1 ? 's' : '');

      landmarks.forEach(landmark => {
        const marker = L.marker([landmark.lat, landmark.lon]);
        
        const popupContent = `
          <div class="landmark-popup">
            ${landmark.thumbnail ? 
              `<img src="${landmark.thumbnail}" class="img-fluid rounded mb-2" 
                   alt="${landmark.title}" style="max-height: 150px;">` : ''}
            <h6>${landmark.title}</h6>
            <p class="small">${landmark.description.length > 200 ? 
              landmark.description.substring(0, 200) + '...' : landmark.description}</p>
            <a href="${landmark.url}" target="_blank" class="btn btn-sm btn-primary">
              <i class="fas fa-external-link-alt me-1"></i>Learn More
            </a>
          </div>
        `;
        
        marker.bindPopup(popupContent, {
          maxWidth: 300,
          className: 'landmark-popup'
        });
        
        markersGroup.addLayer(marker);
      });
    }

    function showError(message) {
      document.getElementById('errorMessage').textContent = message;
      document.getElementById('errorAlert').style.display = 'block';
      
      setTimeout(() => {
        document.getElementById('errorAlert').style.display = 'none';
      }, 5000);
    }
  </script>
</body>
</html>
EOF

# Create favicon
touch dist/landmarks-map/favicon.ico

echo "Frontend restored with category filtering functionality"
exit 0