#!/usr/bin/env python3
"""
Simple Unified SIGHT-SYSTEMs Launcher
Starts all three applications using threading instead of multiprocessing
"""

import os
import sys
import time
import signal
import threading
import subprocess
import psutil
import logging
from logging.handlers import RotatingFileHandler

# Configure logging with UTF-8 encoding
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('logs/unified_launcher.log', maxBytes=1024*1024, backupCount=5, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Application configurations
APPS = {
    'BOTSIGHT': {
        'path': 'BOTSIGHT',
        'port': 5000,
        'protocol': 'HTTPS',
        'main_file': 'run_eventlet.py',
        'description': 'Bot Assembly & Quality Management'
    },
    'CHIPSIGHT': {
        'path': 'CHIPSIGHT',
        'port': 5001,
        'protocol': 'HTTP',
        'main_file': 'run.py',
        'description': 'Digital Twin for Manufacturing'
    },
    'PLANT_UNION': {
        'path': 'plant_union',
        'port': 5002,
        'protocol': 'HTTP',
        'main_file': 'app.py',
        'description': 'Landing Page & SSO Gateway'
    }
}

def check_port_available(port):
    """Check if a port is available"""
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def kill_process_on_port(port):
    """Kill any process using the specified port"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            connections = proc.connections()
            for conn in connections:
                if conn.laddr.port == port:
                    logger.info(f"Killing process {proc.pid} on port {port}")
                    proc.terminate()
                    proc.wait(timeout=5)
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def start_botsight():
    """Start BOTSIGHT application"""
    try:
        # Change to BOTSIGHT directory
        os.chdir('BOTSIGHT')
        
        # Check if SSL certificates exist
        cert_file = "localhost.pem"
        key_file = "localhost-key.pem"
        
        if not (os.path.exists(cert_file) and os.path.exists(key_file)):
            logger.warning("SSL certificates not found. Generating self-signed certificates...")
            # Generate self-signed certificates using mkcert if available
            if os.path.exists("mkcert.exe"):
                subprocess.run(["./mkcert.exe", "localhost"], check=True)
            else:
                logger.error("mkcert.exe not found. Cannot start BOTSIGHT with HTTPS.")
                return False
        
        # Start BOTSIGHT with eventlet
        logger.info("Starting BOTSIGHT on port 5000 (HTTPS)...")
        subprocess.run([sys.executable, "run_eventlet.py"], check=True)
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start BOTSIGHT: {e}")
        return False
    except Exception as e:
        logger.error(f"Error starting BOTSIGHT: {e}")
        return False

def start_chipsight():
    """Start CHIPSIGHT application"""
    try:
        # Change to CHIPSIGHT directory
        os.chdir('CHIPSIGHT')
        
        # Initialize database if needed
        if not os.path.exists('instance/chipsight.db'):
            logger.info("Initializing CHIPSIGHT database...")
            subprocess.run([sys.executable, "init_db.py"], check=True)
        
        # Start CHIPSIGHT with Flask
        logger.info("Starting CHIPSIGHT on port 5001 (HTTP)...")
        subprocess.run([sys.executable, "run.py"], check=True)
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start CHIPSIGHT: {e}")
        return False
    except Exception as e:
        logger.error(f"Error starting CHIPSIGHT: {e}")
        return False

def start_plant_union():
    """Start PLANT_UNION application"""
    try:
        # Change to plant_union directory
        os.chdir('plant_union')
        
        # Start PLANT_UNION with Flask
        logger.info("Starting PLANT_UNION on port 5002 (HTTP)...")
        subprocess.run([sys.executable, "app.py"], check=True)
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start PLANT_UNION: {e}")
        return False
    except Exception as e:
        logger.error(f"Error starting PLANT_UNION: {e}")
        return False

def start_app_thread(app_name, app_config):
    """Thread function to start an application"""
    try:
        logger.info(f"Starting {app_name} ({app_config['description']}) on port {app_config['port']}...")
        
        # Start the appropriate application
        if app_name == 'BOTSIGHT':
            start_botsight()
        elif app_name == 'CHIPSIGHT':
            start_chipsight()
        elif app_name == 'PLANT_UNION':
            start_plant_union()
            
    except Exception as e:
        logger.error(f"Error in {app_name} thread: {e}")

def main():
    """Main function to start all applications"""
    logger.info("Starting SIGHT-SYSTEMs Unified Launcher...")
    
    # Check if we're in the right directory
    if not all(os.path.exists(app_config['path']) for app_config in APPS.values()):
        logger.error("Please run this script from the SIGHT-SYSTEMs root directory")
        sys.exit(1)
    
    # Check and clean up ports
    for app_name, app_config in APPS.items():
        port = app_config['port']
        if not check_port_available(port):
            logger.warning(f"Port {port} is in use. Attempting to clean up...")
            kill_process_on_port(port)
            time.sleep(2)
    
    # Start all applications in separate threads
    threads = {}
    
    try:
        for app_name, app_config in APPS.items():
            logger.info(f"Launching {app_name}...")
            thread = threading.Thread(
                target=start_app_thread,
                args=(app_name, app_config),
                name=app_name,
                daemon=True
            )
            thread.start()
            threads[app_name] = thread
            time.sleep(3)  # Give each app time to start
        
        # Wait for all threads
        logger.info("All applications started successfully!")
        logger.info("\n" + "="*60)
        logger.info("SIGHT-SYSTEMs is now running:")
        logger.info(f"   • PLANT_UNION (Landing Page): http://localhost:5002")
        logger.info(f"   • BOTSIGHT (Bot Assembly): https://localhost:5000")
        logger.info(f"   • CHIPSIGHT (Digital Twin): http://localhost:5001")
        logger.info("="*60)
        logger.info("Press Ctrl+C to stop all applications")
        
        # Keep the main process alive
        while True:
            time.sleep(1)
            # Check if any thread has died
            for app_name, thread in threads.items():
                if not thread.is_alive():
                    logger.error(f"{app_name} has stopped unexpectedly")
                    return
            
    except KeyboardInterrupt:
        logger.info("\nShutting down SIGHT-SYSTEMs...")
        
        # Clean up ports
        for app_config in APPS.values():
            kill_process_on_port(app_config['port'])
        
        logger.info("All applications stopped successfully")
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main() 