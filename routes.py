from flask import jsonify, request, send_from_directory
from app import app, cache
from wikipedia_service import WikipediaService
import logging
import os
import hashlib

logger = logging.getLogger(__name__)

def get_angular_dist_path():
    """Get the absolute path to the Angular build directory"""
    return os.path.abspath(os.path.join(os.getcwd(), 'frontend', 'dist', 'landmarks-map'))

def check_angular_build():
    """Check if Angular build exists and contains index.html"""
    dist_path = get_angular_dist_path()
    index_path = os.path.join(dist_path, 'index.html')
    return os.path.exists(dist_path) and os.path.exists(index_path)

@app.route('/')
def index():
    """Serve the Angular frontend"""
    if not check_angular_build():
        logger.error("Angular build not found. Please build the frontend first.")
        return jsonify({
            'error': 'Frontend not built',
            'message': 'Angular application needs to be built. The build files are missing.',
            'suggestion': 'Run the build process to generate the frontend files.'
        }), 500
    
    angular_dist_path = get_angular_dist_path()
    return send_from_directory(angular_dist_path, 'index.html')

@app.route('/<path:filename>')
def angular_static(filename):
    """Serve Angular static files"""
    if not check_angular_build():
        logger.error(f"Angular build not found when requesting: {filename}")
        return jsonify({
            'error': 'Frontend not built',
            'message': 'Angular application needs to be built. Run "cd frontend && npm run build" first.'
        }), 500
    
    angular_dist_path = get_angular_dist_path()
    try:
        return send_from_directory(angular_dist_path, filename)
    except FileNotFoundError:
        logger.warning(f"Static file not found: {filename}")
        return "File not found", 404

@app.route('/api/landmarks')
def get_landmarks():
    """
    API endpoint to fetch landmarks based on map bounds
    Expects query parameters: north, south, east, west (coordinates)
    """
    try:
        # Get bounding box coordinates from query parameters with NaN protection
        def safe_float(value, default=0):
            """Convert to float with NaN protection"""
            if isinstance(value, str) and value.lower() in ('nan', '+nan', '-nan', 'inf', '+inf', '-inf'):
                raise ValueError(f"Invalid numeric value: {value}")
            result = float(value) if value is not None else default
            if not (result == result):  # NaN check (NaN != NaN)
                raise ValueError("NaN values not allowed")
            return result
        
        north = safe_float(request.args.get('north'), 0)
        south = safe_float(request.args.get('south'), 0)
        east = safe_float(request.args.get('east'), 0)
        west = safe_float(request.args.get('west'), 0)
        
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
    """Handle 404 errors - serve Angular frontend for client-side routing"""
    if not check_angular_build():
        logger.error("Angular build not found for 404 handler.")
        return jsonify({
            'error': 'Frontend not built',
            'message': 'Angular application needs to be built. Run "cd frontend && npm run build" first.'
        }), 404
    
    angular_dist_path = get_angular_dist_path()
    try:
        return send_from_directory(angular_dist_path, 'index.html'), 404
    except FileNotFoundError:
        return jsonify({'error': 'Frontend build files not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500
