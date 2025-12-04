"""
Check if all requirements are met before starting the server
"""
import sys
import os

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        print("   Create .env file from .env.example")
        print("   Command: copy .env.example .env")
        return False
    print("✅ .env file exists")
    return True

def check_api_key():
    """Check if GOOGLE_API_KEY is set"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key or api_key == "your_google_api_key_here":
        print("❌ GOOGLE_API_KEY not configured")
        print("   Add your API key to .env file")
        print("   Get key from: https://makersuite.google.com/app/apikey")
        return False
    print("✅ GOOGLE_API_KEY configured")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "langchain",
        "langchain_google_genai",
        "python-dotenv"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)
    
    if missing:
        print("\n❌ Missing packages. Install them with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Run all checks"""
    print("=" * 50)
    print("🔍 Checking Requirements")
    print("=" * 50)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("API Key", check_api_key),
        ("Dependencies", check_dependencies)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        result = check_func()
        results.append(result)
    
    print("\n" + "=" * 50)
    print("📊 Summary")
    print("=" * 50)
    
    all_passed = all(results)
    
    if all_passed:
        print("\n🎉 All checks passed!")
        print("✅ You're ready to start the server")
        print("\nRun: python main.py")
    else:
        print("\n⚠️ Some checks failed")
        print("❌ Fix the issues above before starting")
        print("\nQuick fixes:")
        print("1. Install Python 3.8+")
        print("2. Create .env: copy .env.example .env")
        print("3. Add API key to .env")
        print("4. Install packages: pip install -r requirements.txt")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
