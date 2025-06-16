# Local Landmarks Map Application

## Overview

The Local Landmarks Map Application is a full-stack web application that helps users discover interesting landmarks and historical sites around any location on Earth. The application combines a Flask backend with an Angular frontend to provide an interactive map experience powered by Wikipedia's geosearch API. Users can explore landmarks in real-time as they navigate the map, with automatic loading of nearby points of interest.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python 3.12) with WSGI deployment via Gunicorn
- **Web Server**: Gunicorn with autoscaling deployment target for production
- **API Design**: RESTful API endpoints serving landmark data
- **Caching**: Flask-Caching with simple cache backend (5-minute TTL) for performance optimization
- **CORS**: Enabled via Flask-CORS for cross-origin requests from Angular frontend
- **Proxy Support**: ProxyFix middleware for proper header handling in deployment

### Frontend Architecture
- **Framework**: Angular 19 with TypeScript for modern component-based architecture
- **Build System**: Angular CLI with Webpack bundling and production optimization
- **Map Integration**: Leaflet.js for interactive mapping capabilities
- **Clustering**: Leaflet MarkerCluster for performance optimization with large datasets
- **UI Framework**: Bootstrap 5.3 with Replit dark theme integration
- **Reactive Programming**: RxJS for data management and API communication
- **Responsive Design**: Mobile-first approach with responsive layouts

## Key Components

### Backend Components

1. **Application Entry Point** (`app.py`, `main.py`)
   - Flask application initialization with CORS and caching configuration
   - ProxyFix middleware for deployment compatibility
   - Session management with environment-based secret key

2. **API Routes** (`routes.py`)
   - Angular static file serving with build verification
   - API endpoint for landmark data retrieval
   - Error handling for missing frontend builds

3. **Wikipedia Integration** (`wikipedia_service.py`)
   - Service class for Wikipedia API interaction
   - Geosearch API integration for landmark discovery
   - Connection pooling and retry logic for reliability
   - Response caching to minimize API calls

### Frontend Components

1. **Application Shell** (`app.component.ts`)
   - Main application component coordinating map and navigation
   - Event handling between navbar and map components

2. **Interactive Map** (`map.component.ts`)
   - Leaflet.js integration with marker clustering
   - Real-time landmark loading based on map bounds
   - Popup generation with landmark details and images

3. **Navigation Bar** (`navbar.component.ts`)
   - Geolocation services integration
   - Landmark count display and location controls

4. **Supporting Components**
   - Loading overlay for user feedback during API calls
   - Error alert system for graceful error handling

### Services

1. **Landmarks Service** (`landmarks.service.ts`)
   - HTTP client wrapper for backend API communication
   - Environment-aware API URL configuration

2. **Geolocation Service** (`geolocation.service.ts`)
   - Browser geolocation API wrapper
   - Observable-based location tracking with loading states

## Data Flow

1. **Map Interaction**: User pans/zooms the map, triggering bounds change events
2. **API Request**: Map component calls LandmarksService with current bounds
3. **Backend Processing**: Flask routes handler forwards request to WikipediaService
4. **External API**: Wikipedia geosearch API returns landmark data within bounds
5. **Response Processing**: Backend formats and caches Wikipedia response
6. **Frontend Update**: Angular components update map markers and UI elements
7. **User Interaction**: Clicking markers displays detailed landmark information

## External Dependencies

### Backend Dependencies
- **Flask**: Web framework with CORS and caching extensions
- **Requests**: HTTP client for Wikipedia API integration
- **Gunicorn**: WSGI server for production deployment

### Frontend Dependencies
- **Angular 19**: Modern frontend framework with TypeScript
- **Leaflet.js**: Interactive mapping library
- **Bootstrap 5**: UI framework with responsive design
- **RxJS**: Reactive programming library for Angular

### Third-party Integrations
- **Wikipedia API**: Geosearch and page content APIs for landmark data
- **CDN Resources**: Bootstrap themes, Leaflet assets, Font Awesome icons

## Deployment Strategy

### Build Process
- **Frontend Build**: Angular CLI production build with optimization
- **Backend Deployment**: Gunicorn WSGI server with autoscaling
- **Static File Serving**: Flask serves Angular build artifacts
- **Environment Configuration**: Separate development and production API URLs

### Infrastructure Requirements
- **Node.js 20**: Required for Angular development and building
- **Python 3.12**: Backend runtime environment
- **PostgreSQL**: Available in environment but not currently utilized
- **OpenSSL**: For secure HTTP communications

### Performance Optimizations
- **Caching**: Server-side caching of Wikipedia API responses
- **Marker Clustering**: Frontend clustering for large datasets
- **Connection Pooling**: HTTP session reuse for external API calls
- **Build Optimization**: Angular production build with tree-shaking and minification

## Changelog

- June 16, 2025. Fixed deployment and auto-location issues
  - Fixed Python dependency conflicts and Gunicorn import errors
  - Created working frontend build with proper static file serving
  - Added automatic geolocation on page load instead of defaulting to London
  - Enhanced error handling for geolocation failures
- June 16, 2025. Added category filtering system
  - Backend: Wikipedia category detection and smart filtering
  - Frontend: Category dropdown with 8 filter types
  - API: Enhanced with category parameter support
- June 15, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.