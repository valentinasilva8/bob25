"""
Deployment script for EcoAd AI Backend
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("⚠️  .env file not found. Please copy env.template to .env and configure it.")
        return False
    
    print("✅ .env file found")
    return True

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def run_tests():
    """Run tests if available"""
    if os.path.exists("test_api.py"):
        return run_command("python test_api.py", "Running tests")
    return True

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting EcoAd AI Backend server...")
    print("   Server will be available at: http://localhost:8000")
    print("   API documentation at: http://localhost:8000/docs")
    print("   Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        return False
    
    return True

def main():
    """Main deployment function"""
    print("🌱 EcoAd AI Backend Deployment")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed. Please fix the issues above.")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Dependency installation failed.")
        return False
    
    # Run tests
    if not run_tests():
        print("\n⚠️  Tests failed, but continuing with deployment...")
    
    # Start server
    print("\n" + "=" * 40)
    if not start_server():
        print("\n❌ Server startup failed.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
