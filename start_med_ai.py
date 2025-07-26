#!/usr/bin/env python3
"""
MED AI - Master Startup Script
Launches both backend and frontend servers
"""

import subprocess
import time
import sys
import os
import signal
from pathlib import Path
import threading

def run_backend():
    """Run the backend server"""
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    try:
        subprocess.run([sys.executable, "run_server.py"], check=True)
    except KeyboardInterrupt:
        print("Backend server stopped by user")
    except Exception as e:
        print(f"Backend error: {e}")

def run_frontend():
    """Run the frontend server"""
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    try:
        subprocess.run([sys.executable, "serve.py"], check=True)
    except KeyboardInterrupt:
        print("Frontend server stopped by user")
    except Exception as e:
        print(f"Frontend error: {e}")

def main():
    """Main function to start both servers"""
    print("🏥 MED AI - Complete Application Startup")
    print("="*50)
    print("🚀 Starting both backend and frontend servers...")
    print("💡 Press Ctrl+C to stop both servers")
    print("="*50)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(3)
    
    # Start frontend in main thread
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\n👋 Stopping MED AI application...")
        # The daemon backend thread will stop automatically
        sys.exit(0)

if __name__ == "__main__":
    main()