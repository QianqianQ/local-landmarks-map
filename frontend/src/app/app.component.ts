import { Component, ViewChild } from '@angular/core';
import { MapComponent } from './components/map/map.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { GeolocationPosition } from './services/geolocation.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  @ViewChild('mapComponent') mapComponent!: MapComponent;
  @ViewChild('navbar') navbar!: NavbarComponent;

  title = 'Local Landmarks Map';

  onLocationFound(position: GeolocationPosition): void {
    this.mapComponent.onLocationFound(position);
  }

  onRefreshRequested(): void {
    this.mapComponent.onRefreshRequested();
  }

  onErrorOccurred(message: string): void {
    this.mapComponent.onErrorOccurred(message);
  }

  onCategoryChanged(category: string): void {
    this.mapComponent.onCategoryChanged(category);
  }

  onLandmarkCountChanged(count: number): void {
    this.navbar.updateLandmarkCount(count);
  }
}