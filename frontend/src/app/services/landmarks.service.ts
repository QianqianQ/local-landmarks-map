import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { LandmarkBounds, LandmarksResponse } from '../models/landmark.interface';

@Injectable({
  providedIn: 'root'
})
export class LandmarksService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getLandmarks(bounds: LandmarkBounds, category?: string): Observable<LandmarksResponse> {
    let params = new HttpParams()
      .set('north', bounds.north.toString())
      .set('south', bounds.south.toString())
      .set('east', bounds.east.toString())
      .set('west', bounds.west.toString());

    if (category && category !== 'all') {
      params = params.set('category', category);
    }

    return this.http.get<LandmarksResponse>(`${this.apiUrl}/landmarks`, { params });
  }
}