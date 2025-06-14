from flask import render_template, jsonify, request
from app import app
from wikipedia_service import WikipediaService
import logging

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Serve the main map page"""
    return render_template('index.html')

@app.route('/api/landmarks')
def get_landmarks():
    """
    API endpoint to fetch landmarks based on map bounds
    Expects query parameters: north, south, east, west (coordinates)
    """
    try:
        # Get bounding box coordinates from query parameters
        north = float(request.args.get('north', 0))
        south = float(request.args.get('south', 0))
        east = float(request.args.get('east', 0))
        west = float(request.args.get('west', 0))
        
        logger.debug(f"Fetching landmarks for bounds: N:{north}, S:{south}, E:{east}, W:{west}")
        
        # Validate coordinates
        if not (-90 <= south <= north <= 90) or not (-180 <= west <= east <= 180):
            return jsonify({'error': 'Invalid coordinates'}), 400
        
        # Get landmarks from Wikipedia
        wikipedia_service = WikipediaService()
        landmarks = wikipedia_service.get_landmarks_in_bounds(north, south, east, west)
        
        logger.debug(f"Found {len(landmarks)} landmarks")
        return jsonify({'landmarks': landmarks})
        
    except ValueError as e:
        logger.error(f"Invalid coordinate values: {e}")
        return jsonify({'error': 'Invalid coordinate format'}), 400
    except Exception as e:
        logger.error(f"Error fetching landmarks: {e}")
        return jsonify({'error': 'Failed to fetch landmarks'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500
