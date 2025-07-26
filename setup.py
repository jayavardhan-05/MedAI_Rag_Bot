#!/usr/bin/env python3
"""
MED AI Setup Script
Installs dependencies and prepares the environment
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} is supported")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} is not supported. Please use Python 3.8+")
        return False

def install_dependencies():
    """Install backend dependencies"""
    backend_dir = Path(__file__).parent / "backend"
    requirements_file = backend_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"❌ Requirements file not found at {requirements_file}")
        return False
    
    cmd = f"pip install -r {requirements_file}"
    return run_command(cmd, "Installing backend dependencies")

def check_faiss_index():
    """Check if FAISS index exists"""
    possible_locations = [
        Path(__file__).parent / "my_faiss_index",
        Path(__file__).parent / "backend" / "my_faiss_index",
    ]
    
    for location in possible_locations:
        if location.exists() and (location / "index.faiss").exists():
            print(f"✅ FAISS index found at {location}")
            return True
    
    print("⚠️  FAISS index not found. Please run the notebook to create it.")
    print("   Expected locations:")
    for loc in possible_locations:
        print(f"   - {loc}")
    return False

def make_scripts_executable():
    """Make startup scripts executable on Unix systems"""
    if os.name != 'nt':  # Not Windows
        scripts = [
            "start_med_ai.py",
            "backend/run_server.py",
            "frontend/serve.py"
        ]
        
        for script in scripts:
            script_path = Path(__file__).parent / script
            if script_path.exists():
                run_command(f"chmod +x {script_path}", f"Making {script} executable")

def main():
    """Main setup function"""
    print("🏥 MED AI Setup")
    print("="*40)
    print("🛠️  Preparing your MED AI environment...")
    print("="*40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies. Please check the error messages above.")
        sys.exit(1)
    
    # Check FAISS index
    faiss_available = check_faiss_index()
    
    # Make scripts executable
    make_scripts_executable()
    
    print("\n" + "="*40)
    print("🎉 MED AI Setup Complete!")
    print("="*40)
    
    if faiss_available:
        print("✅ Everything is ready! You can now start MED AI:")
        print("   python start_med_ai.py")
    else:
        print("⚠️  Setup complete, but FAISS index is missing.")
        print("   Please run the Jupyter notebook first to create the index.")
    
    print("\n📖 For detailed instructions, see README.md")
    print("🌐 Backend will run on: http://localhost:8000")
    print("🎨 Frontend will run on: http://localhost:3000")

if __name__ == "__main__":
    main()