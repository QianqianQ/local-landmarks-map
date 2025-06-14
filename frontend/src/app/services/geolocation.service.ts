import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';

export interface GeolocationPosition {
  lat: number;
  lng: number;
}

@Injectable({
  providedIn: 'root'
})
export class GeolocationService {
  private isLocatingSubject = new BehaviorSubject<boolean>(false);
  public isLocating$ = this.isLocatingSubject.asObservable();

  constructor() { }

  getCurrentPosition(): Observable<GeolocationPosition> {
    return new Observable(observer => {
      if (!navigator.geolocation) {
        observer.error(new Error('Geolocation is not supported by this browser'));
        return;
      }

      this.isLocatingSubject.next(true);

      navigator.geolocation.getCurrentPosition(
        (position) => {
          this.isLocatingSubject.next(false);
          observer.next({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
          observer.complete();
        },
        (error) => {
          this.isLocatingSubject.next(false);
          observer.error(error);
        },
        {
          timeout: 10000,
          enableHighAccuracy: true
        }
      );
    });
  }
}