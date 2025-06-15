# Local Landmarks Map Application - Architecture Overview

## Overview

This is a full-stack web application that helps users discover interesting landmarks and historical sites around any location on Earth. The application combines a Flask backend with an Angular frontend to provide an interactive map experience powered by Wikipedia's geosearch API. Users can explore landmarks globally, view detailed information, and discover historical sites in real-time as they navigate the map.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python 3.12) with modular structure
- **Web Server**: Gunicorn for production deployment with autoscaling capabilities
- **API Design**: RESTful API endpoints for landmark data retrieval
- **Caching**: Flask-Caching with simple in-memory cache (5-minute TTL) for performance optimization
- **CORS**: Enabled for cross-origin requests to support frontend integration
- **Session Management**: Session secret key configured via environment variables
- **Proxy Support**: ProxyFix middleware for proper header handling in deployment

### Frontend Architecture
- **Framework**: Angular 19 with TypeScript for modern component-based architecture
- **Map Library**: Leaflet.js with Angular integration for interactive mapping
- **Clustering**: Leaflet MarkerCluster for performance optimization with large datasets
- **UI Framework**: Bootstrap 5.3 with Replit dark theme for consistent styling
- **Services**: Reactive programming with RxJS for data management and state handling
- **Build System**: Angular CLI with Webpack for optimized production builds
- **Responsive Design**: Mobile-first approach with responsive layouts

## Key Components

### Backend Components

1. **Application Entry Point** (`app.py`, `main.py`)
   - Flask application initialization with CORS and caching
   - Session configuration and middleware setup
   - Application factory pattern for modularity

2. **Route Handler** (`routes.py`)
   - API endpoints for landmark data retrieval
   - Static file serving for Angular frontend
   - Angular build verification and fallback handling
   - Cache-enabled responses for performance

3. **Wikipedia Service** (`wikipedia_service.py`)
   - Wikipedia API integration with geosearch functionality
   - HTTP session management with connection pooling
   - Rate limiting and error handling for external API calls
   - Landmark data processing and enrichment

### Frontend Components

1. **Core Application** (`app.component.ts`)
   - Main application container
   - Component communication coordination
   - Event handling between map and navigation components

2. **Map Component** (`map.component.ts`)
   - Leaflet map initialization and management
   - Marker clustering for performance optimization
   - Real-time landmark loading based on map bounds
   - Interactive popup generation with landmark details

3. **Navigation Component** (`navbar.component.ts`)
   - Geolocation services integration
   - Landmark count display and status updates
   - User interface controls for map interaction

4. **Service Layer**
   - **LandmarksService**: HTTP client for backend API communication
   - **GeolocationService**: Browser geolocation API wrapper with error handling

## Data Flow

1. **Map Interaction**: User pans/zooms the map
2. **Bounds Calculation**: Frontend calculates visible map bounds
3. **API Request**: Angular service sends bounds to Flask backend
4. **Wikipedia Query**: Backend queries Wikipedia geosearch API
5. **Data Processing**: Backend processes and enriches landmark data
6. **Response Caching**: Results cached for 5 minutes to reduce API calls
7. **Frontend Update**: Angular receives data and updates map markers
8. **User Interaction**: Users can click markers for detailed information

## External Dependencies

### Backend Dependencies
- **Wikipedia API**: Primary data source for landmark information
- **Flask Ecosystem**: Core web framework with extensions
- **Gunicorn**: Production WSGI server for deployment
- **Requests**: HTTP client library for external API calls

### Frontend Dependencies
- **Leaflet.js**: Interactive mapping library
- **Bootstrap**: UI component framework with dark theme
- **RxJS**: Reactive programming library for Angular
- **TypeScript**: Type-safe JavaScript development

### Infrastructure Dependencies
- **Node.js**: Required for Angular build process
- **PostgreSQL**: Configured in environment but not actively used
- **Replit Platform**: Development and deployment environment

## Deployment Strategy

### Build Process
1. **Frontend Build**: Angular CLI compiles TypeScript to optimized JavaScript bundles
2. **Asset Optimization**: CSS/JS minification and tree-shaking for production
3. **Static File Generation**: Angular build outputs to `frontend/dist/landmarks-map/`
4. **Backend Integration**: Flask serves Angular static files and provides API endpoints

### Production Configuration
- **Autoscaling**: Configured for automatic scaling based on demand
- **Port Configuration**: Backend runs on port 5000 with external port 80
- **Environment Variables**: Session secrets and configuration via environment
- **Error Handling**: Comprehensive error handling for missing builds and API failures

### Development Workflow
- **Frontend Development**: Angular CLI development server with hot reload
- **Backend Development**: Flask development server with debug mode
- **Build Automation**: Multiple build scripts for different deployment scenarios
- **Dependency Management**: npm for frontend, pip/uv for backend dependencies

## Changelog
- June 15, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.