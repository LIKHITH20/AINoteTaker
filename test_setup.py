#!/usr/bin/env python3
"""
Test script to verify AI Interview Note Taker setup
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'flask',
        'flask_socketio',
        'openai',
        'dotenv',
        'pyaudio',
        'numpy',
        'soundfile',
        'librosa',
        'pydub'
    ]
    
    print("🔍 Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    return len(failed_imports) == 0

def test_audio_devices():
    """Test if audio devices are accessible"""
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        
        print("\n🔍 Testing audio devices...")
        
        # Get default input device info
        try:
            default_input = p.get_default_input_device_info()
            print(f"✅ Default input device: {default_input['name']}")
        except Exception as e:
            print(f"⚠️  No default input device: {e}")
        
        # List all input devices
        input_devices = []
        for i in range(p.get_device_count()):
            try:
                device_info = p.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    input_devices.append(device_info['name'])
            except:
                pass
        
        if input_devices:
            print(f"✅ Found {len(input_devices)} input device(s)")
            for device in input_devices[:3]:  # Show first 3
                print(f"   - {device}")
        else:
            print("❌ No input devices found")
        
        p.terminate()
        return True
        
    except Exception as e:
        print(f"❌ Audio test failed: {e}")
        return False

def test_openai_config():
    """Test OpenAI configuration"""
    try:
        from dotenv import load_dotenv
        import os
        
        print("\n🔍 Testing OpenAI configuration...")
        
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        
        if api_key and api_key != 'your_openai_api_key_here':
            print("✅ OpenAI API key configured")
            return True
        else:
            print("⚠️  OpenAI API key not configured")
            print("   Please add your API key to the .env file")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI config test failed: {e}")
        return False

def test_flask_app():
    """Test if Flask app can be created"""
    try:
        print("\n🔍 Testing Flask application...")
        
        # Test basic Flask setup
        from flask import Flask
        app = Flask(__name__)
        print("✅ Flask app created successfully")
        
        # Test SocketIO
        from flask_socketio import SocketIO
        socketio = SocketIO(app)
        print("✅ SocketIO initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎤 AI Interview Note Taker - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Audio Devices", test_audio_devices),
        ("OpenAI Configuration", test_openai_config),
        ("Flask Application", test_flask_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("Run 'python app.py' to start the application.")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        print("Refer to README.md for troubleshooting steps.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)