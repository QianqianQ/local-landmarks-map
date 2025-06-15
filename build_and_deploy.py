#!/usr/bin/env python3
"""
Build and deployment script for the Local Landmarks Map application
This script handles Angular frontend building and deployment preparation
"""
import os
import subprocess
import sys
import logging
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_node_and_npm():
    """Check if Node.js and npm are available"""
    try:
        node_result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        npm_result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        
        if node_result.returncode == 0 and npm_result.returncode == 0:
            logger.info(f"Node.js version: {node_result.stdout.strip()}")
            logger.info(f"npm version: {npm_result.stdout.strip()}")
            return True
        else:
            logger.error("Node.js or npm not found")
            return False
    except FileNotFoundError:
        logger.error("Node.js or npm not installed")
        return False

def install_frontend_dependencies():
    """Install Angular frontend dependencies"""
    frontend_dir = os.path.join(os.getcwd(), 'frontend')
    
    if not os.path.exists(frontend_dir):
        logger.error("Frontend directory not found")
        return False
    
    logger.info("Installing frontend dependencies...")
    
    try:
        # Install dependencies with npm ci for faster, reliable builds
        result = subprocess.run(
            ['npm', 'ci', '--silent', '--no-audit', '--no-fund'],
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            timeout=180  # 3 minute timeout
        )
        
        if result.returncode == 0:
            logger.info("Frontend dependencies installed successfully")
            return True
        else:
            logger.error(f"Failed to install dependencies: {result.stderr}")
            # Try regular npm install as fallback
            logger.info("Trying fallback npm install...")
            result = subprocess.run(
                ['npm', 'install', '--silent', '--no-audit', '--no-fund'],
                cwd=frontend_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                logger.info("Frontend dependencies installed with fallback method")
                return True
            else:
                logger.error(f"Fallback install also failed: {result.stderr}")
                return False
                
    except subprocess.TimeoutExpired:
        logger.error("Dependency installation timed out")
        return False
    except Exception as e:
        logger.error(f"Error installing dependencies: {e}")
        return False

def build_angular_frontend():
    """Build the Angular frontend application"""
    frontend_dir = os.path.join(os.getcwd(), 'frontend')
    
    if not os.path.exists(frontend_dir):
        logger.error("Frontend directory not found")
        return False
    
    logger.info("Building Angular frontend...")
    
    try:
        # Use ng build with optimized settings for deployment
        build_cmd = [
            'npx', 'ng', 'build', 
            '--configuration', 'production',
            '--output-path', 'dist/landmarks-map',
            '--progress=false',
            '--verbose=false'
        ]
        
        logger.info(f"Running: {' '.join(build_cmd)}")
        
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
                logger.info(f"Build verification successful - index.html found")
                
                # List build files for verification
                build_files = os.listdir(dist_path)
                logger.info(f"Build files created: {', '.join(build_files)}")
                return True
            else:
                logger.error("Build verification failed - index.html not found")
                return False
        else:
            logger.error(f"Angular build failed with exit code {result.returncode}")
            logger.error(f"Build output: {result.stdout}")
            logger.error(f"Build errors: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("Build process timed out")
        return False
    except Exception as e:
        logger.error(f"Error during build: {e}")
        return False

def verify_build():
    """Verify that the build was successful and all necessary files exist"""
    frontend_dir = os.path.join(os.getcwd(), 'frontend')
    dist_path = os.path.join(frontend_dir, 'dist', 'landmarks-map')
    
    required_files = ['index.html']
    
    for file in required_files:
        file_path = os.path.join(dist_path, file)
        if not os.path.exists(file_path):
            logger.error(f"Required file missing: {file}")
            return False
    
    # Check file sizes to ensure they're not empty
    index_path = os.path.join(dist_path, 'index.html')
    if os.path.getsize(index_path) < 100:  # Basic sanity check
        logger.error("index.html appears to be too small")
        return False
    
    logger.info("Build verification passed")
    return True

def main():
    """Main build and deployment function"""
    logger.info("Starting build and deployment process...")
    
    # Check prerequisites
    if not check_node_and_npm():
        logger.error("Node.js/npm check failed")
        return False
    
    # Install dependencies
    if not install_frontend_dependencies():
        logger.error("Failed to install frontend dependencies")
        return False
    
    # Build frontend
    if not build_angular_frontend():
        logger.error("Failed to build Angular frontend")
        return False
    
    # Verify build
    if not verify_build():
        logger.error("Build verification failed")
        return False
    
    logger.info("Build and deployment preparation completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)