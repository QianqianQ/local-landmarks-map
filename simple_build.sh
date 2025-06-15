#!/bin/bash
set -e

echo "Building Angular frontend for deployment..."

# Navigate to frontend directory
cd frontend

# Clean any existing build
rm -rf dist/landmarks-map
mkdir -p dist/landmarks-map

# Install dependencies if needed
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.bin/ng" ]; then
    echo "Installing dependencies..."
    npm install --silent --no-audit --no-fund
fi

# Build the Angular application
echo "Building Angular application..."
npx ng build --configuration production --output-path dist/landmarks-map --progress=false

# Verify the build
if [ -f "dist/landmarks-map/index.html" ]; then
    echo "Build successful! Files created:"
    ls -la dist/landmarks-map/
else
    echo "Build failed - index.html not found"
    exit 1
fi

echo "Frontend build completed successfully!"