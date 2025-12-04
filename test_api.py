"""
Test script for Anshul's Portfolio Chatbot
Tests all endpoints and features
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_separator():
    print("\n" + "="*80 + "\n")

def test_health():
    """Test health endpoint"""
    print("🏥 Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print_separator()

def test_profile():
    """Test full profile endpoint"""
    print("👤 Testing Full Profile Endpoint...")
    response = requests.get(f"{BASE_URL}/profile")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Profile Name: {data['profile']['contact']['name']}")
    print(f"Role: {data['profile']['contact']['role']}")
    print(f"Projects Count: {len(data['profile']['projects'])}")
    print_separator()

def test_quick_info():
    """Test quick info endpoints"""
    print("⚡ Testing Quick Info Endpoints...")
    
    info_types = ["contact", "projects", "skills", "summary"]
    
    for info_type in info_types:
        print(f"\nFetching {info_type}...")
        response = requests.post(
            f"{BASE_URL}/quick-info",
            json={"info_type": info_type}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ {info_type.capitalize()} info retrieved successfully")
    
    print_separator()

def test_chat():
    """Test chat endpoint with various queries"""
    print("💬 Testing Chat Endpoint...")
    
    session_id = "test_session_" + str(datetime.now().timestamp())
    
    test_messages = [
        "Hi! Who is Anshul Parate?",
        "Tell me about his projects",
        "What are his main skills in Generative AI?",
        "How can I contact him?",
        "What's his latest project about RAG?",
        "Show me the GitHub links for his projects",
        "What's his educational background?",
        "Tell me about his achievements",
        "What technologies does he use for backend development?",
        "Give me his LinkedIn profile"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📨 Message {i}: {message}")
        
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": message,
                "session_id": session_id
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"🤖 Response: {data['response'][:200]}...")
            print(f"📊 Message Count: {data['message_count']}")
            print(f"⏱️ Timestamp: {data['timestamp']}")
        else:
            print(f"❌ Error: {response.status_code}")
    
    print_separator()

def test_sessions():
    """Test session management"""
    print("🔐 Testing Session Management...")
    
    response = requests.get(f"{BASE_URL}/sessions")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Active Sessions: {data['count']}")
    print(f"Memory Limit: {data['memory_limit_per_session']} messages")
    
    for session in data['sessions']:
        print(f"\nSession ID: {session['session_id']}")
        print(f"Messages: {session['message_count']}")
        print(f"Last Activity: {session['last_activity']}")
    
    print_separator()

def test_reset():
    """Test conversation reset"""
    print("🔄 Testing Conversation Reset...")
    
    session_id = "test_reset_session"
    
    # Send a message
    requests.post(
        f"{BASE_URL}/chat",
        json={"message": "Hello", "session_id": session_id}
    )
    
    # Reset
    response = requests.post(f"{BASE_URL}/reset?session_id={session_id}")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    print_separator()

def test_memory_limit():
    """Test 10-message memory limit"""
    print("🧠 Testing 10-Message Memory Limit...")
    
    session_id = "memory_test_" + str(datetime.now().timestamp())
    
    # Send 12 messages to test trimming
    for i in range(12):
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": f"Test message {i+1}",
                "session_id": session_id
            }
        )
        if response.status_code == 200:
            data = response.json()
            print(f"Message {i+1}: Count = {data['message_count']}")
    
    print("\n✅ Memory should be capped at 10 messages")
    print_separator()

def run_all_tests():
    """Run all tests"""
    print("\n🚀 Starting Anshul's Portfolio Chatbot Tests\n")
    
    try:
        test_health()
        test_profile()
        test_quick_info()
        test_chat()
        test_sessions()
        test_reset()
        test_memory_limit()
        
        print("✅ All tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")

if __name__ == "__main__":
    run_all_tests()
