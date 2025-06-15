import requests
from requests.adapters import HTTPAdapter
import logging
from typing import List, Dict, Optional
import time

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
        # Cache for landmark details to avoid repeated API calls
        self._details_cache = {}
        # Connection pooling for better performance
        adapter = HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=3
        )
        self.session.mount('https://', adapter)
    
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
            filtered_pages = []
            
            # Filter results to only those within our bounding box
            for page in pages:
                lat = page.get('lat')
                lon = page.get('lon')
                
                if (lat is not None and lon is not None and 
                    south <= lat <= north and west <= lon <= east):
                    
                    # Collect pages for batch processing
                    filtered_pages.append({
                        'pageid': page['pageid'],
                        'title': page['title'],
                        'lat': lat,
                        'lon': lon
                    })
            
            # Batch process page details for better performance
            if filtered_pages:
                page_details = self._get_page_details_batch(
                    [(p['pageid'], p['title']) for p in filtered_pages]
                )
                
                for page in filtered_pages:
                    pageid = page['pageid']
                    if pageid in page_details:
                        landmark_info = page_details[pageid].copy()
                        landmark_info.update({
                            'lat': page['lat'],
                            'lon': page['lon'],
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
    
    def _get_page_details_batch(self, page_list: List[tuple]) -> Dict[int, Dict]:
        """
        Get details for multiple pages in a single API call for better performance
        
        Args:
            page_list: List of (pageid, title) tuples
            
        Returns:
            Dictionary mapping pageid to page details
        """
        if not page_list:
            return {}
        
        # Check cache first
        uncached_pages = []
        results = {}
        
        for pageid, title in page_list:
            if pageid in self._details_cache:
                results[pageid] = self._details_cache[pageid]
            else:
                uncached_pages.append((pageid, title))
        
        if not uncached_pages:
            return results
        
        # Batch request for uncached pages (max 50 per request)
        batch_size = 50
        for i in range(0, len(uncached_pages), batch_size):
            batch = uncached_pages[i:i + batch_size]
            pageids = [str(pageid) for pageid, _ in batch]
            
            try:
                params = {
                    'action': 'query',
                    'pageids': '|'.join(pageids),
                    'prop': 'extracts|pageimages',
                    'exintro': True,
                    'explaintext': True,
                    'exsentences': 3,
                    'piprop': 'thumbnail',
                    'pithumbsize': 300,
                    'format': 'json'
                }
                
                response = self.session.get(self.api_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if 'query' in data and 'pages' in data['query']:
                    for pageid_str, page_data in data['query']['pages'].items():
                        pageid = int(pageid_str)
                        title = next((t for pid, t in batch if pid == pageid), '')
                        
                        landmark_info = {
                            'description': page_data.get('extract', 'No description available.'),
                            'url': f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                            'thumbnail': None
                        }
                        
                        if 'thumbnail' in page_data:
                            landmark_info['thumbnail'] = page_data['thumbnail']['source']
                        
                        # Cache the result
                        self._details_cache[pageid] = landmark_info
                        results[pageid] = landmark_info
                        
            except Exception as e:
                logger.error(f"Error fetching batch details: {e}")
                # Add fallback data for failed requests
                for pageid, title in batch:
                    if pageid not in results:
                        fallback_info = {
                            'description': 'Details unavailable.',
                            'url': f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                            'thumbnail': None
                        }
                        self._details_cache[pageid] = fallback_info
                        results[pageid] = fallback_info
        
        return results

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
