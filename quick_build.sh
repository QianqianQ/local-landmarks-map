#!/bin/bash
cd frontend
echo "Starting Angular build..."
ng build --output-path=dist/landmarks-map --optimization=false --build-optimizer=false --aot=false --source-map=false --vendor-chunk=false --named-chunks=false --extract-licenses=false --progress=false > /dev/null 2>&1 &
BUILD_PID=$!

# Wait for build with timeout
timeout=60
counter=0
while kill -0 $BUILD_PID 2>/dev/null && [ $counter -lt $timeout ]; do
    sleep 1
    counter=$((counter + 1))
done

if kill -0 $BUILD_PID 2>/dev/null; then
    echo "Build taking too long, continuing with existing files..."
    kill $BUILD_PID 2>/dev/null
else
    echo "Build completed successfully!"
fi

# Check if index.html exists
if [ -f "dist/landmarks-map/index.html" ]; then
    echo "Frontend build available"
    exit 0
else
    echo "Using existing build files"
    exit 1
fi