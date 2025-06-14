// Global variables
let map;
let markersGroup;
let currentLandmarks = [];
let isLoading = false;

// Initialize the map when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    setupEventListeners();
});

/**
 * Initialize the Leaflet map
 */
function initializeMap() {
    // Create map centered on New York City by default
    map = L.map('map').setView([40.7128, -74.0060], 13);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18
    }).addTo(map);
    
    // Initialize marker cluster group
    markersGroup = L.markerClusterGroup({
        chunkedLoading: true,
        maxClusterRadius: 50
    });
    map.addLayer(markersGroup);
    
    // Set up map event listeners
    map.on('moveend', onMapMoveEnd);
    map.on('zoomend', onMapMoveEnd);
    
    // Try to get user's location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                map.setView([lat, lng], 13);
                loadLandmarks();
            },
            function(error) {
                console.log('Geolocation failed:', error);
                loadLandmarks(); // Load landmarks anyway with default location
            },
            { timeout: 10000 }
        );
    } else {
        loadLandmarks();
    }
}

/**
 * Set up event listeners for UI controls
 */
function setupEventListeners() {
    // Locate button
    document.getElementById('locate-btn').addEventListener('click', function() {
        if (navigator.geolocation) {
            this.disabled = true;
            const icon = this.querySelector('i');
            icon.className = 'fas fa-spinner fa-spin';
            
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;
                    map.setView([lat, lng], 15);
                    
                    // Reset button
                    document.getElementById('locate-btn').disabled = false;
                    icon.className = 'fas fa-location-arrow';
                },
                function(error) {
                    showError('Unable to get your location: ' + error.message);
                    document.getElementById('locate-btn').disabled = false;
                    icon.className = 'fas fa-location-arrow';
                }
            );
        } else {
            showError('Geolocation is not supported by this browser');
        }
    });
    
    // Refresh button
    document.getElementById('refresh-btn').addEventListener('click', function() {
        loadLandmarks();
    });
}

/**
 * Handle map move/zoom events
 */
function onMapMoveEnd() {
    if (!isLoading) {
        loadLandmarks();
    }
}

/**
 * Load landmarks for the current map bounds
 */
async function loadLandmarks() {
    if (isLoading) return;
    
    isLoading = true;
    showLoading(true);
    
    try {
        const bounds = map.getBounds();
        const params = new URLSearchParams({
            north: bounds.getNorth(),
            south: bounds.getSouth(),
            east: bounds.getEast(),
            west: bounds.getWest()
        });
        
        const response = await fetch(`/api/landmarks?${params}`);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to load landmarks');
        }
        
        const data = await response.json();
        displayLandmarks(data.landmarks);
        
    } catch (error) {
        console.error('Error loading landmarks:', error);
        showError('Failed to load landmarks: ' + error.message);
    } finally {
        isLoading = false;
        showLoading(false);
    }
}

/**
 * Display landmarks on the map
 */
function displayLandmarks(landmarks) {
    // Clear existing markers
    markersGroup.clearLayers();
    currentLandmarks = landmarks;
    
    // Update landmark count
    document.getElementById('landmark-count').textContent = 
        `${landmarks.length} landmark${landmarks.length !== 1 ? 's' : ''}`;
    
    landmarks.forEach(landmark => {
        const marker = createLandmarkMarker(landmark);
        markersGroup.addLayer(marker);
    });
}

/**
 * Create a marker for a landmark
 */
function createLandmarkMarker(landmark) {
    const marker = L.marker([landmark.lat, landmark.lon]);
    
    // Create popup content
    const popupContent = createPopupContent(landmark);
    marker.bindPopup(popupContent, {
        maxWidth: 300,
        className: 'landmark-popup'
    });
    
    return marker;
}

/**
 * Create HTML content for landmark popup
 */
function createPopupContent(landmark) {
    const thumbnail = landmark.thumbnail ? 
        `<img src="${landmark.thumbnail}" class="img-fluid rounded mb-2" alt="${landmark.title}" style="max-height: 150px;">` : 
        '';
    
    const description = landmark.description || 'No description available.';
    const truncatedDescription = description.length > 200 ? 
        description.substring(0, 200) + '...' : description;
    
    return `
        <div class="landmark-popup-content">
            <h6 class="fw-bold mb-2">${landmark.title}</h6>
            ${thumbnail}
            <p class="small mb-2">${truncatedDescription}</p>
            <a href="${landmark.url}" target="_blank" class="btn btn-sm btn-outline-primary">
                <i class="fas fa-external-link-alt me-1"></i>
                Read more on Wikipedia
            </a>
        </div>
    `;
}

/**
 * Show or hide loading overlay
 */
function showLoading(show) {
    const overlay = document.getElementById('loading-overlay');
    if (show) {
        overlay.classList.remove('d-none');
    } else {
        overlay.classList.add('d-none');
    }
}

/**
 * Show error message
 */
function showError(message) {
    const errorAlert = document.getElementById('error-alert');
    const errorMessage = document.getElementById('error-message');
    
    errorMessage.textContent = message;
    errorAlert.classList.remove('d-none');
    errorAlert.classList.add('show');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorAlert.classList.remove('show');
        errorAlert.classList.add('d-none');
    }, 5000);
}
