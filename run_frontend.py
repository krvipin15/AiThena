#!/usr/bin/env python3
"""
AiThena Frontend Runner
Run this script to start the Streamlit frontend application.
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting AiThena Frontend...")
    print("📱 Make sure your backend is running on http://localhost:8000")
    print("🌐 Frontend will be available at http://localhost:8501")
    print("-" * 50)
    
    # Change to frontend directory
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    os.chdir(frontend_dir)
    
    # Run Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "Home.py", 
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Frontend stopped by user")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

if __name__ == "__main__":
    main() 