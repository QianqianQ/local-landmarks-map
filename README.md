# Local Landmarks Map

A full-stack web application that displays local landmarks on an interactive map using Wikipedia's geosearch API. Explore historical sites, monuments, and points of interest in any area with a modern, responsive interface.

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.1.1-green.svg)
![Angular](https://img.shields.io/badge/angular-19-red.svg)
![TypeScript](https://img.shields.io/badge/typescript-5.8-blue.svg)

## Features

- **Interactive Map**: Pan and zoom to explore different areas
- **Real-time Data**: Fetches landmark information from Wikipedia based on current viewport
- **Geolocation**: Find landmarks near your current location
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Detailed Information**: Click markers to view descriptions, images, and Wikipedia links
- **Marker Clustering**: Efficiently displays large numbers of landmarks
- **Dark Theme**: Modern dark UI optimized for extended use

## Technology Stack

### Backend
- **Python 3.12** - Runtime environment
- **Flask** - Web framework and API server
- **Gunicorn** - WSGI HTTP server for production
- **Wikipedia API** - Data source for landmark information
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **Angular 19** - Modern TypeScript framework
- **Leaflet.js** - Interactive mapping library
- **Bootstrap** - UI framework with dark theme
- **RxJS** - Reactive programming for data management
- **TypeScript** - Type-safe development

## Quick Start

### Prerequisites
- Python 3.12 or higher
- Node.js 20 or higher
- npm or yarn package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/local-landmarks-map.git
   cd local-landmarks-map
   ```

2. **Set up Python environment**
   ```bash
   # Install Python dependencies using uv (preferred)
   uv install
   # or using pip if uv is not available
   pip install -e .
   ```

3. **Set up Angular frontend**
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

4. **Run the application**
   ```bash
   # Start Flask server
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## Development

### Backend Development
The Flask backend provides a RESTful API with the following endpoints:

- `GET /` - Serves the Angular frontend
- `GET /api/landmarks` - Fetches landmarks for given map bounds
  - Query parameters: `north`, `south`, `east`, `west` (coordinates)

### Frontend Development
The Angular frontend is built with modern TypeScript and includes:

- **Map Component**: Interactive Leaflet map with clustering
- **Services**: Geolocation and landmark data management
- **Responsive UI**: Bootstrap-based dark theme interface

To run frontend in development mode:
```bash
cd frontend
ng serve
```

### Project Structure
```
├── app.py                 # Flask application setup
├── main.py               # Application entry point
├── routes.py             # API routes and frontend serving
├── wikipedia_service.py  # Wikipedia API integration
├── models.py            # Database models (prepared for future use)
├── frontend/            # Angular application
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/
│   │   │   ├── services/
│   │   │   └── models/
│   │   └── ...
│   └── ...
├── pyproject.toml       # Python dependencies
└── README.md           # This file
```

## API Documentation

### GET /api/landmarks

Fetches landmarks within specified geographic bounds.

**Parameters:**
- `north` (float): Northern boundary latitude
- `south` (float): Southern boundary latitude  
- `east` (float): Eastern boundary longitude
- `west` (float): Western boundary longitude

**Response:**
```json
{
  "landmarks": [
    {
      "lat": 40.7589,
      "lon": -73.9851,
      "title": "Central Park",
      "description": "Large public park in Manhattan...",
      "url": "https://en.wikipedia.org/wiki/Central_Park",
      "thumbnail": "https://upload.wikimedia.org/..."
    }
  ]
}
```

## Deployment

### Replit Deployment
This application is optimized for Replit deployment:

1. Import the project to Replit
2. Dependencies will be installed automatically
3. The application runs on port 5000 by default
4. Use Replit's deployment feature for production hosting

### Manual Deployment
For other platforms:

1. Ensure Python 3.12+ is available
2. Install dependencies: `uv install` or `pip install -e .`
3. Build Angular frontend: `cd frontend && npm run build`
4. Run with Gunicorn: `gunicorn --bind 0.0.0.0:5000 main:app`

## Configuration

### Environment Variables
- `SESSION_SECRET` - Flask session secret key
- `DATABASE_URL` - PostgreSQL connection string (optional)

### Map Configuration
The application uses OpenStreetMap tiles by default. Leaflet configuration can be modified in the Angular map component.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Wikipedia](https://www.wikipedia.org/) for providing the landmark data
- [OpenStreetMap](https://www.openstreetmap.org/) for map tiles
- [Leaflet](https://leafletjs.com/) for the mapping library
- [Angular](https://angular.io/) for the frontend framework
- [Flask](https://flask.palletsprojects.com/) for the backend framework
