"""Quick test script to verify all API endpoints are working."""
import requests
import json

BASE_URL = "https://agentic-workflows-pm7o.onrender.com"

def test_health():
    """Test health endpoint."""
    print("Testing /api/health...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_plugins_list():
    """Test plugins list endpoint."""
    print("Testing /api/plugins...")
    response = requests.get(f"{BASE_URL}/api/plugins")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        plugins = response.json()
        print(f"Found {len(plugins)} plugins:")
        for plugin in plugins:
            print(f"  - {plugin['name']}: {plugin['description']}")
    print()

def test_llm_providers():
    """Test LLM providers endpoint."""
    print("Testing /api/llm/providers...")
    response = requests.get(f"{BASE_URL}/api/llm/providers")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Available providers:")
        for provider in data.get('providers', []):
            print(f"  - {provider['name']}: {'✓' if provider['available'] else '✗'}")
    print()

def test_llm_chat():
    """Test LLM chat endpoint."""
    print("Testing /api/llm/chat...")
    response = requests.post(
        f"{BASE_URL}/api/llm/chat",
        json={"message": "What is a workflow?"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data.get('response', '')[:100]}...")
    print()

def test_plugin_details():
    """Test plugin details endpoint."""
    print("Testing /api/plugins/file_organizer...")
    response = requests.get(f"{BASE_URL}/api/plugins/file_organizer")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        plugin = response.json()
        print(f"Plugin: {plugin['name']}")
        print(f"Description: {plugin['description']}")
        print(f"Parameters: {list(plugin['parameters'].keys())}")
    print()

def test_workflows_list():
    """Test workflows list endpoint (requires auth)."""
    print("Testing /api/workflows (without auth)...")
    response = requests.get(f"{BASE_URL}/api/workflows")
    print(f"Status: {response.status_code}")
    if response.status_code == 401:
        print("✓ Correctly requires authentication")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("API ENDPOINT TESTS")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_plugins_list()
        test_llm_providers()
        test_llm_chat()
        test_plugin_details()
        test_workflows_list()
        
        print("=" * 60)
        print("✓ All tests completed!")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Error: {e}")
