export interface LandmarkBounds {
  north: number;
  south: number;
  east: number;
  west: number;
}

export interface Landmark {
  lat: number;
  lon: number;
  title: string;
  description: string;
  url: string;
  thumbnail?: string;
  categories?: string[];
}

export interface LandmarksResponse {
  landmarks: Landmark[];
}