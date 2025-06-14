# Local Landmarks Map Application

## Overview

This is a Flask-based web application that displays local landmarks on an interactive map using Wikipedia's geosearch API. The application allows users to explore historical sites, monuments, and points of interest within their current view area on a dynamic map interface.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python 3.11) with a modular structure
- **Web Server**: Gunicorn for production deployment with autoscaling
- **API Layer**: RESTful API endpoints for landmark data retrieval
- **External Services**: Wikipedia API integration for landmark information
- **CORS**: Enabled for cross-origin requests

### Frontend Architecture
- **Map Library**: Leaflet.js for interactive mapping
- **UI Framework**: Bootstrap with Replit dark theme
- **Clustering**: Leaflet MarkerCluster for performance optimization
- **Responsive Design**: Mobile-first approach with responsive layouts

## Key Components

### Backend Components

1. **Application Entry Point** (`app.py`, `main.py`)
   - Flask application initialization
   - CORS configuration
   - Proxy handling for deployment environments
   - Debug logging setup

2. **Route Handlers** (`routes.py`)
   - Main page route serving the HTML interface
   - `/api/landmarks` endpoint for fetching landmark data based on map bounds
   - Error handling for 404 and API errors
   - Input validation for coordinate parameters

3. **Wikipedia Service** (`wikipedia_service.py`)
   - Service class for Wikipedia API interactions
   - Geosearch functionality for finding landmarks within bounding boxes
   - Coordinate-based radius calculations
   - HTTP session management with proper user agent headers

4. **Models** (`models.py`)
   - Placeholder file for future database models if needed
   - Currently no database persistence required

### Frontend Components

1. **Main Interface** (`templates/index.html`)
   - Bootstrap-based responsive layout
   - Map container with navigation header
   - Loading overlay for user feedback
   - Landmark counter display

2. **Map Functionality** (`static/js/map.js`)
   - Leaflet map initialization and configuration
   - Geolocation support for user positioning
   - Dynamic landmark loading based on map viewport
   - Marker clustering for performance
   - Event handling for map interactions

3. **Styling** (`static/css/style.css`)
   - Dark theme integration with Bootstrap
   - Custom map control styling
   - Responsive layout adjustments
   - Marker cluster customizations

## Data Flow

1. **User Location Detection**: Browser geolocation API determines initial map position
2. **Map Interaction**: User pans/zooms the map triggering viewport change events
3. **Coordinate Extraction**: Map bounds (north, south, east, west) are calculated
4. **API Request**: Frontend sends AJAX request to `/api/landmarks` with coordinates
5. **Wikipedia Query**: Backend calculates center point and radius, queries Wikipedia geosearch API
6. **Data Processing**: Landmark data is formatted and validated
7. **Map Updates**: Frontend receives data and updates markers with clustering

## External Dependencies

### Python Packages
- **Flask**: Web framework and routing
- **Flask-CORS**: Cross-origin resource sharing
- **Flask-SQLAlchemy**: Database ORM (prepared for future use)
- **Requests**: HTTP client for Wikipedia API calls
- **Gunicorn**: WSGI HTTP server for production
- **Psycopg2-binary**: PostgreSQL adapter (prepared for future database use)

### Frontend Libraries
- **Leaflet.js**: Interactive mapping library
- **Leaflet MarkerCluster**: Marker clustering plugin
- **Bootstrap**: UI framework with dark theme
- **Font Awesome**: Icon library

### External APIs
- **Wikipedia API**: Geosearch and article data
- **OpenStreetMap**: Map tile provider
- **Browser Geolocation API**: User location detection

## Deployment Strategy

### Development Environment
- **Platform**: Replit with Nix package management
- **Runtime**: Python 3.11 with required system packages (OpenSSL, PostgreSQL)
- **Development Server**: Flask built-in server with hot reload

### Production Deployment
- **Target**: Autoscale deployment on Replit
- **Server**: Gunicorn with multiple worker processes
- **Configuration**: Proxy-aware setup for load balancing
- **Port Binding**: 0.0.0.0:5000 for external access

### Environment Configuration
- Session secrets via environment variables
- Database connection preparation (PostgreSQL ready)
- CORS enabled for API access
- Debug logging for troubleshooting

## User Preferences

Preferred communication style: Simple, everyday language.

## Changelog

Changelog:
- June 14, 2025. Initial setup