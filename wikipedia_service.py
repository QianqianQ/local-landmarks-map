import requests
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class WikipediaService:
    """Service class for interacting with Wikipedia APIs"""
    
    def __init__(self):
        self.base_url = "https://en.wikipedia.org/api/rest_v1"
        self.api_url = "https://en.wikipedia.org/w/api.php"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'LandmarksMapApp/1.0 (https://replit.com)'
        })
    
    def get_landmarks_in_bounds(self, north: float, south: float, east: float, west: float) -> List[Dict]:
        """
        Fetch landmarks within the given bounding box using Wikipedia's geosearch API
        
        Args:
            north, south, east, west: Bounding box coordinates
            
        Returns:
            List of landmark dictionaries with title, coordinates, description, etc.
        """
        try:
            # Calculate center point and radius for the search
            center_lat = (north + south) / 2
            center_lon = (east + west) / 2
            
            # Calculate approximate radius in meters (rough estimation)
            lat_diff = abs(north - south)
            lon_diff = abs(east - west)
            radius = max(lat_diff, lon_diff) * 111000 / 2  # Convert degrees to meters roughly
            radius = min(radius, 10000)  # Cap at 10km to avoid too many results
            radius = max(radius, 1000)   # Minimum 1km to ensure we get some results
            
            logger.debug(f"Searching around {center_lat}, {center_lon} with radius {radius}m")
            
            # Search for pages near the location
            params = {
                'action': 'query',
                'list': 'geosearch',
                'gscoord': f"{center_lat}|{center_lon}",
                'gsradius': int(radius),
                'gslimit': 50,
                'format': 'json'
            }
            
            response = self.session.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'query' not in data or 'geosearch' not in data['query']:
                logger.warning("No geosearch results found in Wikipedia response")
                return []
            
            landmarks = []
            pages = data['query']['geosearch']
            
            # Filter results to only those within our bounding box
            for page in pages:
                lat = page.get('lat')
                lon = page.get('lon')
                
                if (lat is not None and lon is not None and 
                    south <= lat <= north and west <= lon <= east):
                    
                    # Get additional details for this page
                    landmark_info = self._get_page_details(page['pageid'], page['title'])
                    if landmark_info:
                        landmark_info.update({
                            'lat': lat,
                            'lon': lon,
                            'title': page['title']
                        })
                        landmarks.append(landmark_info)
            
            logger.debug(f"Filtered to {len(landmarks)} landmarks within bounds")
            return landmarks
            
        except requests.RequestException as e:
            logger.error(f"Wikipedia API request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Error processing Wikipedia data: {e}")
            return []
    
    def _get_page_details(self, pageid: int, title: str) -> Optional[Dict]:
        """
        Get additional details for a Wikipedia page including extract and thumbnail
        
        Args:
            pageid: Wikipedia page ID
            title: Page title
            
        Returns:
            Dictionary with page details or None if failed
        """
        try:
            params = {
                'action': 'query',
                'pageids': pageid,
                'prop': 'extracts|pageimages',
                'exintro': True,
                'explaintext': True,
                'exsentences': 3,
                'piprop': 'thumbnail',
                'pithumbsize': 300,
                'format': 'json'
            }
            
            response = self.session.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'query' not in data or 'pages' not in data['query']:
                return None
            
            page_data = data['query']['pages'].get(str(pageid))
            if not page_data:
                return None
            
            result = {
                'description': page_data.get('extract', 'No description available.'),
                'url': f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                'thumbnail': None
            }
            
            # Add thumbnail if available
            if 'thumbnail' in page_data:
                result['thumbnail'] = page_data['thumbnail']['source']
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting page details for {title}: {e}")
            return {
                'description': 'Description unavailable.',
                'url': f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                'thumbnail': None
            }
