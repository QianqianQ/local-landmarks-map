#!/bin/bash
set -e

echo "Building Angular frontend..."
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

# Build the Angular application
echo "Compiling Angular application..."
npx ng build --configuration production --output-path dist/landmarks-map

echo "Build completed successfully!"
echo "Build files are located in: frontend/dist/landmarks-map/"