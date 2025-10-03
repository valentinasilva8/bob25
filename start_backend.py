#!/usr/bin/env python3
"""
AWE Agency - Backend Server
Simple startup script for the FastAPI backend
"""

import uvicorn
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

if __name__ == "__main__":
    print("🚀 Starting AWE Agency Backend...")
    print("📍 API will be available at: http://localhost:8002")
    print("📚 API docs at: http://localhost:8002/docs")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    uvicorn.run(
        "backend.simple_main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )