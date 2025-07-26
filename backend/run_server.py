#!/usr/bin/env python3
"""
MED AI Backend Server Startup Script
"""

import os
import sys
import shutil
from pathlib import Path

def setup_faiss_index():
    """Setup the FAISS index by copying it to the backend directory if needed."""
    backend_dir = Path(__file__).parent
    root_dir = backend_dir.parent
    
    # Look for FAISS index in various locations
    possible_locations = [
        backend_dir / "my_faiss_index",
        root_dir / "my_faiss_index",
        Path("/content/drive/My Drive/my_faiss_index"),  # Google Drive location from notebook
    ]
    
    faiss_index_path = None
    for location in possible_locations:
        if location.exists() and (location / "index.faiss").exists():
            faiss_index_path = location
            break
    
    if not faiss_index_path:
        print("❌ FAISS index not found in any of the expected locations:")
        for loc in possible_locations:
            print(f"   - {loc}")
        print("\nPlease run the notebook to create the FAISS index first, or copy it to one of these locations.")
        return False
    
    target_path = backend_dir / "my_faiss_index"
    
    # If found in a different location, copy it to backend directory
    if faiss_index_path != target_path:
        print(f"📁 Copying FAISS index from {faiss_index_path} to {target_path}")
        if target_path.exists():
            shutil.rmtree(target_path)
        shutil.copytree(faiss_index_path, target_path)
    
    print(f"✅ FAISS index ready at {target_path}")
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        import langchain
        import sentence_transformers
        import faiss
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def main():
    """Main function to start the MED AI backend server."""
    print("🚀 Starting MED AI Backend Server...")
    print("="*50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup FAISS index
    if not setup_faiss_index():
        sys.exit(1)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    print("\n🏥 MED AI Backend Setup Complete!")
    print("📡 Starting FastAPI server...")
    print("🌐 Frontend will be available at: http://localhost:8000 (if served)")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    print("💡 To stop the server, press Ctrl+C")
    print("="*50)
    
    # Start the server
    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 MED AI Backend server stopped.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()