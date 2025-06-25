#!/usr/bin/env python3
"""
Setup script for External LLM Email Generator
Helps users configure their environment for using external LLM APIs
"""

import os
import sys
import subprocess
import json

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_requirements():
    """Install required packages"""
    requirements = [
        "flask",
        "requests", 
        "openai"
    ]
    
    print("Installing required packages...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    return True

def setup_api_key():
    """Help user set up API key"""
    print("\n" + "="*50)
    print("API KEY SETUP")
    print("="*50)
    
    current_key = os.getenv('OPENAI_API_KEY')
    if current_key:
        print(f"✅ OpenAI API key is already set (ends with: ...{current_key[-4:]})")
        return True
    
    print("You need an OpenAI API key to generate emails.")
    print("1. Go to https://platform.openai.com/api-keys")
    print("2. Create a new API key")
    print("3. Set it as an environment variable:")
    print()
    
    if os.name == 'nt':  # Windows
        print("   For Windows (Command Prompt):")
        print("   set OPENAI_API_KEY=your-api-key-here")
        print()
        print("   For Windows (PowerShell):")
        print("   $env:OPENAI_API_KEY='your-api-key-here'")
    else:  # Unix/Linux/Mac
        print("   For Unix/Linux/Mac:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
    
    print()
    print("Or add it to your shell profile (.bashrc, .zshrc, etc.) for persistence")
    
    # Offer to set it temporarily
    api_key = input("\nEnter your OpenAI API key (or press Enter to skip): ").strip()
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
        print("✅ API key set for this session")
        return True
    else:
        print("⚠️  API key not set. You'll need to set it before generating emails.")
        return False

def test_backend_connection():
    """Test if backend server is accessible"""
    try:
        import requests
        response = requests.get("http://localhost:5000/categories", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running and accessible")
            return True
        else:
            print("⚠️  Backend server responded but with error")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend server is not running")
        print("Start it with: python backend/app.py")
        return False
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

def create_example_config():
    """Create example configuration file"""
    config = {
        "api_provider": "openai",
        "model": "gpt-3.5-turbo",
        "default_email_count": 10,
        "max_emails_per_request": 50,
        "difficulty_distribution": {
            "easy": 0.2,
            "medium": 0.6,
            "hard": 0.2
        }
    }
    
    with open("email_generator_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created example configuration file: email_generator_config.json")

def main():
    print("🚀 External LLM Email Generator Setup")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Setup API key
    api_key_set = setup_api_key()
    
    # Test backend connection
    backend_running = test_backend_connection()
    
    # Create example config
    create_example_config()
    
    print("\n" + "="*50)
    print("SETUP SUMMARY")
    print("="*50)
    print(f"✅ Python version: OK")
    print(f"✅ Required packages: Installed")
    print(f"{'✅' if api_key_set else '⚠️ '} API key: {'Set' if api_key_set else 'Not set'}")
    print(f"{'✅' if backend_running else '❌'} Backend server: {'Running' if backend_running else 'Not running'}")
    print(f"✅ Configuration: Created")
    
    print("\n" + "="*50)
    print("NEXT STEPS")
    print("="*50)
    
    if not backend_running:
        print("1. Start the backend server:")
        print("   python backend/app.py")
        print()
    
    if not api_key_set:
        print("2. Set your OpenAI API key:")
        if os.name == 'nt':
            print("   set OPENAI_API_KEY=your-api-key-here")
        else:
            print("   export OPENAI_API_KEY='your-api-key-here'")
        print()
    
    print("3. Generate and categorize emails:")
    print("   python email_training_tool.py --count 10")
    print()
    print("4. Or use the backend API directly:")
    print("   curl -X POST http://localhost:5000/generate-emails -H 'Content-Type: application/json' -d '{\"count\": 5}'")
    
    print("\n🎉 Setup complete! Happy email categorizing!")

if __name__ == "__main__":
    main()