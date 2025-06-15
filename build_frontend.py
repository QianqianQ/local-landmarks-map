#!/usr/bin/env python3
"""
Build script for Angular frontend
This script builds the Angular frontend for deployment
"""
import os
import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_angular_frontend():
    """Build the Angular frontend application"""
    try:
        logger.info("Starting Angular frontend build...")
        
        # Change to frontend directory
        frontend_dir = os.path.join(os.getcwd(), 'frontend')
        if not os.path.exists(frontend_dir):
            logger.error("Frontend directory not found")
            return False
        
        # Build the Angular application
        build_cmd = ["npx", "ng", "build", "--configuration", "production", "--output-path", "dist/landmarks-map"]
        logger.info(f"Running build command: {' '.join(build_cmd)}")
        
        result = subprocess.run(
            build_cmd,
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            logger.info("Angular build completed successfully")
            
            # Verify build output
            dist_path = os.path.join(frontend_dir, 'dist', 'landmarks-map')
            index_path = os.path.join(dist_path, 'index.html')
            
            if os.path.exists(index_path):
                logger.info(f"Build verification successful - index.html found at {index_path}")
                return True
            else:
                logger.error("Build verification failed - index.html not found")
                return False
        else:
            logger.error(f"Angular build failed with exit code {result.returncode}")
            logger.error(f"STDOUT: {result.stdout}")
            logger.error(f"STDERR: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("Angular build timed out after 5 minutes")
        return False
    except Exception as e:
        logger.error(f"Error during Angular build: {e}")
        return False

if __name__ == "__main__":
    success = build_angular_frontend()
    sys.exit(0 if success else 1)