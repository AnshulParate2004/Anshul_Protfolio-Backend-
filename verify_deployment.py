"""
Quick test to verify the app can start
Run this locally before deploying to Vercel
"""
import sys
from pathlib import Path

# Add parent directory
sys.path.insert(0, str(Path(__file__).parent))

try:
    print("1. Testing imports...")
    from main import app
    from config import settings
    from profile_data import ANSHUL_PROFILE
    from agent import AnshulChatAgent
    print("   ✅ All imports successful")
    
    print("\n2. Testing FastAPI app...")
    print(f"   App name: {app.title}")
    print(f"   Version: {app.version}")
    print("   ✅ FastAPI app initialized")
    
    print("\n3. Testing configuration...")
    print(f"   API Key configured: {settings.is_configured()}")
    print(f"   Model: {settings.GEMINI_MODEL}")
    print("   ✅ Configuration loaded")
    
    print("\n4. Testing profile data...")
    print(f"   Name: {ANSHUL_PROFILE.contact.name}")
    print(f"   Projects: {len(ANSHUL_PROFILE.projects)}")
    print("   ✅ Profile data loaded")
    
    if settings.is_configured():
        print("\n5. Testing agent initialization...")
        agent = AnshulChatAgent()
        print("   ✅ Agent initialized successfully")
    else:
        print("\n5. ⚠️  Skipping agent test (no API key)")
    
    print("\n" + "="*50)
    print("🎉 ALL TESTS PASSED!")
    print("="*50)
    print("\nYou can now deploy to Vercel!")
    print("Remember to set GOOGLE_API_KEY in Vercel environment variables")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
