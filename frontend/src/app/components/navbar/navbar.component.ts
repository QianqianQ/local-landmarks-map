import { Component, EventEmitter, Output } from '@angular/core';
import { GeolocationService, GeolocationPosition } from '../../services/geolocation.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent {
  @Output() locationFound = new EventEmitter<GeolocationPosition>();
  @Output() refreshRequested = new EventEmitter<void>();
  @Output() errorOccurred = new EventEmitter<string>();
  @Output() categoryChanged = new EventEmitter<string>();

  landmarkCount = 0;
  isLocating = false;
  selectedCategory = 'all';
  
  categories = [
    { value: 'all', label: 'All Landmarks' },
    { value: 'museums', label: 'Museums & Galleries' },
    { value: 'churches', label: 'Churches & Religious' },
    { value: 'monuments', label: 'Monuments & Memorials' },
    { value: 'parks', label: 'Parks & Gardens' },
    { value: 'buildings', label: 'Historic Buildings' },
    { value: 'entertainment', label: 'Entertainment' },
    { value: 'transport', label: 'Transportation' }
  ];

  constructor(private geolocationService: GeolocationService) {
    this.geolocationService.isLocating$.subscribe(isLocating => {
      this.isLocating = isLocating;
    });
  }

  onLocateClick(): void {
    this.geolocationService.getCurrentPosition().subscribe({
      next: (position) => {
        this.locationFound.emit(position);
      },
      error: (error) => {
        this.errorOccurred.emit(`Unable to get your location: ${error.message}`);
      }
    });
  }

  onRefreshClick(): void {
    this.refreshRequested.emit();
  }

  updateLandmarkCount(count: number): void {
    this.landmarkCount = count;
  }
}