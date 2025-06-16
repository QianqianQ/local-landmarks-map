# Overview

This is a full-stack web application that helps users discover interesting landmarks and historical sites around any location on Earth using interactive maps. The application consists of a Flask backend that serves Wikipedia landmark data and an Angular frontend with Leaflet.js mapping functionality.

# System Architecture

## Backend Architecture
- **Framework**: Flask (Python 3.12) with modular structure
- **Web Server**: Gunicorn for production deployment with autoscaling capabilities
- **API Layer**: RESTful API endpoints for landmark data retrieval
- **Caching**: Flask-Caching with simple in-memory caching (5-minute timeout)
- **CORS**: Enabled for cross-origin requests between frontend and backend
- **Proxy Support**: ProxyFix middleware for proper handling of forwarded headers

## Frontend Architecture
- **Framework**: Angular 19 with TypeScript for modern component-based architecture
- **Map Library**: Leaflet.js for interactive mapping with Angular integration
- **UI Framework**: Bootstrap 5.3 with Replit dark theme
- **Clustering**: Leaflet MarkerCluster for performance optimization with large datasets
- **Services**: Reactive programming with RxJS for data management
- **Build System**: Angular CLI with Webpack for optimized production builds
- **Responsive Design**: Mobile-first approach with responsive layouts

# Key Components

## Backend Components

1. **Application Entry Point** (`app.py`, `main.py`)
   - Flask application factory pattern
   - CORS configuration for cross-origin requests
   - Caching setup for performance optimization
   - ProxyFix for deployment compatibility

2. **API Routes** (`routes.py`)
   - RESTful endpoints for landmark data
   - Angular static file serving
   - Error handling for missing frontend builds
   - Cache key generation for Wikipedia API responses

3. **Wikipedia Service** (`wikipedia_service.py`)
   - Wikipedia API integration for landmark data
   - Geosearch functionality with bounding box queries
   - Category filtering support (museums, churches, monuments, etc.)
   - Connection pooling and retry logic for reliability
   - Response caching to minimize API calls

## Frontend Components

1. **Core Application** (`app.component.ts`)
   - Main application coordinator
   - Event handling between navbar and map components
   - Cross-component communication management

2. **Interactive Map** (`map.component.ts`)
   - Leaflet.js integration with marker clustering
   - Real-time landmark loading based on map bounds
   - Custom popup content with landmark details
   - Category-based filtering
   - Geolocation support

3. **Navigation Bar** (`navbar.component.ts`)
   - Category filter dropdown
   - Location finder button
   - Landmark count display
   - User interaction controls

4. **Service Layer**
   - **LandmarksService**: HTTP client for API communication
   - **GeolocationService**: Browser geolocation wrapper with observables

# Data Flow

1. **User Interaction**: User pans/zooms map or selects category filter
2. **Bounds Calculation**: Frontend calculates current map viewport bounds
3. **API Request**: Angular service makes HTTP request to Flask backend with bounds and category
4. **Wikipedia Query**: Backend queries Wikipedia's geosearch API with location parameters
5. **Data Processing**: Backend processes and filters Wikipedia response
6. **Cache Storage**: Processed data cached for 5 minutes to improve performance
7. **Response Delivery**: Landmark data returned to frontend as JSON
8. **Map Update**: Frontend updates map markers with clustering for performance
9. **User Feedback**: Loading states and error handling provide user feedback

# External Dependencies

## Backend Dependencies
- **Wikipedia API**: Primary data source for landmark information
- **Flask-CORS**: Cross-origin request handling
- **Flask-Caching**: Response caching for performance
- **Requests**: HTTP client for Wikipedia API calls
- **Gunicorn**: Production WSGI server

## Frontend Dependencies
- **Leaflet.js**: Interactive mapping library
- **MarkerCluster**: Performance optimization for large datasets
- **Bootstrap**: UI framework with dark theme
- **RxJS**: Reactive programming for data streams
- **Font Awesome**: Icon library for UI elements

## External Services
- **Wikipedia Geosearch API**: Landmark data retrieval
- **CDN Resources**: Bootstrap, Leaflet, and Font Awesome assets

# Deployment Strategy

## Production Build Process
1. **Frontend Build**: Angular CLI compiles TypeScript to optimized JavaScript bundles
2. **Asset Optimization**: Webpack optimizes CSS, JavaScript, and static assets
3. **Static File Serving**: Flask serves pre-built Angular assets
4. **API Routing**: Backend handles `/api/*` routes, frontend handles all other routes

## Server Configuration
- **Gunicorn**: WSGI server with auto-scaling deployment target
- **Port Configuration**: Backend on port 5000, external port 80
- **Process Management**: Parallel workflows for frontend build and server startup
- **Build Scripts**: Multiple build strategies (quick, simple, full) for different deployment scenarios

## Environment Management
- **Development**: Angular dev server with Flask backend proxy
- **Production**: Static file serving through Flask with optimized builds
- **Configuration**: Environment-specific API URLs and settings

# Changelog

Changelog:
- June 16, 2025. Initial setup

# User Preferences

Preferred communication style: Simple, everyday language.