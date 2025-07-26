#!/usr/bin/env python3
"""
Simple HTTP server to serve the MED AI frontend
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 3000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    # Change to frontend directory
    frontend_dir = Path(__file__).parent
    os.chdir(frontend_dir)
    
    # Create server
    handler = CustomHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("🎨 MED AI Frontend Server")
        print("="*40)
        print(f"🌐 Serving at: http://localhost:{PORT}")
        print(f"📁 Directory: {frontend_dir}")
        print("💡 To stop the server, press Ctrl+C")
        print("="*40)
        
        # Try to open browser
        try:
            webbrowser.open(f'http://localhost:{PORT}')
            print("🚀 Opening browser...")
        except Exception:
            print("⚠️  Could not open browser automatically")
            print(f"   Please open http://localhost:{PORT} manually")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Frontend server stopped.")

if __name__ == "__main__":
    main()