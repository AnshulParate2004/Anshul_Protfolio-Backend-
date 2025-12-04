"""
Test script for the minimal API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_health():
    """Test health check"""
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_profile():
    """Test profile endpoint"""
    print("\n=== Testing Profile Endpoint ===")
    response = requests.get(f"{BASE_URL}/profile")
    print(f"Status: {response.status_code}")
    profile = response.json()
    print(f"Name: {profile['profile']['contact']['name']}")
    print(f"Role: {profile['profile']['contact']['role']}")
    print(f"Projects: {len(profile['profile']['projects'])}")

def test_quick_info():
    """Test quick info endpoint"""
    print("\n=== Testing Quick Info ===")
    
    info_types = ["contact", "skills", "projects"]
    for info_type in info_types:
        print(f"\n--- {info_type.upper()} ---")
        response = requests.post(
            f"{BASE_URL}/quick-info",
            json={"info_type": info_type}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data['success']}")
            if info_type == "contact":
                print(f"Email: {data['data']['email']}")
            elif info_type == "skills":
                print(f"Categories: {list(data['data'].keys())}")
            elif info_type == "projects":
                print(f"Number of projects: {len(data['data'])}")

def test_chat():
    """Test chat endpoint"""
    print("\n=== Testing Chat Endpoint ===")
    
    messages = [
        "Hi, who is Anshul?",
        "What are his top projects?",
        "How can I contact him?"
    ]
    
    session_id = "test_session_123"
    
    for i, message in enumerate(messages, 1):
        print(f"\n--- Message {i} ---")
        print(f"User: {message}")
        
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": message,
                "session_id": session_id
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"AI: {data['response'][:200]}...")  # First 200 chars
            print(f"Message Count: {data['message_count']}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

def test_sessions():
    """Test sessions endpoint"""
    print("\n=== Testing Sessions ===")
    response = requests.get(f"{BASE_URL}/sessions")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Active Sessions: {data['count']}")
    for session in data['sessions']:
        print(f"  - {session['session_id']}: {session['message_count']} messages")

def test_reset():
    """Test reset endpoint"""
    print("\n=== Testing Reset ===")
    response = requests.post(
        f"{BASE_URL}/reset",
        params={"session_id": "test_session_123"}
    )
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("🧪 Starting API Tests...")
    print(f"Base URL: {BASE_URL}")
    
    try:
        test_root()
        test_health()
        test_profile()
        test_quick_info()
        test_chat()
        test_sessions()
        test_reset()
        
        print("\n✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API")
        print("Make sure the server is running: python main.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
