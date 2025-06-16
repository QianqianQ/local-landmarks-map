import { Component, OnInit, AfterViewInit, ViewChild, ElementRef, Output, EventEmitter } from '@angular/core';
import * as L from 'leaflet';
import 'leaflet.markercluster';

import { LandmarksService } from '../../services/landmarks.service';
import { GeolocationService, GeolocationPosition } from '../../services/geolocation.service';
import { Landmark, LandmarkBounds } from '../../models/landmark.interface';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit, AfterViewInit {
  @ViewChild('mapContainer', { static: true }) mapContainer!: ElementRef;
  @Output() landmarkCountChanged = new EventEmitter<number>();

  private map!: L.Map;
  private markersGroup!: L.MarkerClusterGroup;
  private currentLandmarks: Landmark[] = [];
  private isLoading = false;
  private currentCategory = 'all';

  isLoadingVisible = false;
  isErrorVisible = false;
  errorMessage = '';
  landmarkCount = 0;

  constructor(
    private landmarksService: LandmarksService,
    private geolocationService: GeolocationService
  ) {}

  ngOnInit(): void {
    // Fix for default markers in Leaflet
    delete (L.Icon.Default.prototype as any)._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
      iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
    });
  }

  ngAfterViewInit(): void {
    this.initializeMap();
    this.setupEventListeners();
  }

  private initializeMap(): void {
    // Create map centered on Helsinki, Finland by default
    this.map = L.map(this.mapContainer.nativeElement).setView([60.1699, 24.9384], 13);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 18
    }).addTo(this.map);

    // Initialize marker cluster group
    this.markersGroup = L.markerClusterGroup({
      chunkedLoading: true,
      maxClusterRadius: 50
    });
    this.map.addLayer(this.markersGroup);

    // Set up map event listeners
    this.map.on('moveend', () => this.onMapMoveEnd());
    this.map.on('zoomend', () => this.onMapMoveEnd());

    // Try to get user's location
    this.geolocationService.getCurrentPosition().subscribe({
      next: (position) => {
        this.map.setView([position.lat, position.lng], 13);
        this.loadLandmarks();
      },
      error: (error) => {
        console.log('Geolocation failed:', error);
        this.loadLandmarks(); // Load landmarks anyway with default location
      }
    });
  }

  private setupEventListeners(): void {
    // Additional event listeners can be added here
  }

  private onMapMoveEnd(): void {
    if (!this.isLoading) {
      this.loadLandmarks();
    }
  }

  private loadLandmarks(): void {
    if (this.isLoading) return;

    this.isLoading = true;
    this.isLoadingVisible = true;

    const bounds = this.map.getBounds();
    const landmarkBounds: LandmarkBounds = {
      north: bounds.getNorth(),
      south: bounds.getSouth(),
      east: bounds.getEast(),
      west: bounds.getWest()
    };

    this.landmarksService.getLandmarks(landmarkBounds, this.currentCategory).subscribe({
      next: (response) => {
        this.displayLandmarks(response.landmarks);
        this.isLoading = false;
        this.isLoadingVisible = false;
      },
      error: (error) => {
        console.error('Error loading landmarks:', error);
        this.showError('Failed to load landmarks: ' + error.message);
        this.isLoading = false;
        this.isLoadingVisible = false;
      }
    });
  }

  private displayLandmarks(landmarks: Landmark[]): void {
    // Clear existing markers
    this.markersGroup.clearLayers();
    this.currentLandmarks = landmarks;

    // Update landmark count
    this.landmarkCount = landmarks.length;
    this.landmarkCountChanged.emit(landmarks.length);

    landmarks.forEach(landmark => {
      const marker = this.createLandmarkMarker(landmark);
      this.markersGroup.addLayer(marker);
    });
  }

  private createLandmarkMarker(landmark: Landmark): L.Marker {
    const marker = L.marker([landmark.lat, landmark.lon]);

    // Create popup content
    const popupContent = this.createPopupContent(landmark);
    marker.bindPopup(popupContent, {
      maxWidth: 300,
      className: 'landmark-popup'
    });

    return marker;
  }

  private createPopupContent(landmark: Landmark): string {
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

  onLocationFound(position: GeolocationPosition): void {
    this.map.setView([position.lat, position.lng], 15);
  }

  onRefreshRequested(): void {
    this.loadLandmarks();
  }

  onCategoryChanged(category: string): void {
    this.currentCategory = category;
    this.loadLandmarks();
  }

  private showError(message: string): void {
    this.errorMessage = message;
    this.isErrorVisible = true;

    // Auto-hide after 5 seconds
    setTimeout(() => {
      this.isErrorVisible = false;
    }, 5000);
  }

  onErrorOccurred(message: string): void {
    this.showError(message);
  }
}