import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { MapComponent } from './components/map/map.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { LoadingOverlayComponent } from './components/loading-overlay/loading-overlay.component';
import { ErrorAlertComponent } from './components/error-alert/error-alert.component';

import { LandmarksService } from './services/landmarks.service';
import { GeolocationService } from './services/geolocation.service';

@NgModule({
  declarations: [
    AppComponent,
    MapComponent,
    NavbarComponent,
    LoadingOverlayComponent,
    ErrorAlertComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule
  ],
  providers: [
    LandmarksService,
    GeolocationService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }