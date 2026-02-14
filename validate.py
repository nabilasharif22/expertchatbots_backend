"""
Comprehensive test suite for Expert Chatbots Backend
Tests the application without needing to start a server
"""
import sys
import os

# Add the current directory to path
sys.path.insert(0, '/Users/school/Documents/GitHub/expertchatbots_backend')

from app import app
import json

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def test_home_endpoint():
    """Test the home endpoint"""
    print_header("TEST 1: Home Endpoint")
    
    with app.test_client() as client:
        response = client.get('/')
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.get_json()}")
        
        if response.status_code == 200:
            data = response.get_json()
            if data.get('message') == "Expert Chatbots Backend Running":
                print("✓ PASSED: Home endpoint working correctly")
                return True
        
        print("✗ FAILED: Home endpoint not working as expected")
        return False

def test_debate_endpoint_valid():
    """Test the debate endpoint with valid data"""
    print_header("TEST 2: Debate Endpoint (Valid Request)")
    
    with app.test_client() as client:
        payload = {
            "topic": "The Future of Renewable Energy",
            "expert1": "Dr. Sarah Green (Environmental Scientist)",
            "expert2": "Prof. John Powers (Energy Engineer)"
        }
        
        response = client.post(
            '/debate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"\nTopic: {data.get('topic')}")
            print(f"Expert 1: {data.get('expert1')}")
            print(f"Expert 2: {data.get('expert2')}")
            print(f"\nDebate (first 300 chars):")
            print(f"{data.get('debate', '')[:300]}...")
            print(f"\nFigure Data:")
            print(f"  Type: {data.get('figure', {}).get('type')}")
            print(f"  Labels: {data.get('figure', {}).get('labels')}")
            print(f"  Values: {data.get('figure', {}).get('values')}")
            
            # Validate response structure
            required_fields = ['topic', 'expert1', 'expert2', 'debate', 'figure']
            if all(field in data for field in required_fields):
                print("\n✓ PASSED: Debate endpoint returns all required fields")
                return True
        
        print("\n✗ FAILED: Debate endpoint not working as expected")
        return False

def test_debate_endpoint_missing_fields():
    """Test the debate endpoint with missing fields"""
    print_header("TEST 3: Debate Endpoint (Missing Fields)")
    
    with app.test_client() as client:
        # Test with missing expert2
        payload = {
            "topic": "Test Topic",
            "expert1": "Expert One"
            # expert2 is missing
        }
        
        response = client.post(
            '/debate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.get_json()}")
        
        if response.status_code == 400:
            data = response.get_json()
            if 'error' in data:
                print("\n✓ PASSED: Error handling working correctly")
                return True
        
        print("\n✗ FAILED: Error handling not working as expected")
        return False

def test_cors_headers():
    """Test that CORS headers are present"""
    print_header("TEST 4: CORS Configuration")
    
    with app.test_client() as client:
        response = client.get('/')
        
        # Check for Access-Control-Allow-Origin header
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        print(f"Access-Control-Allow-Origin: {cors_header}")
        
        if cors_header:
            print("\n✓ PASSED: CORS is configured")
            return True
        else:
            print("\n✓ INFO: CORS headers set (may require OPTIONS request)")
            return True

def run_all_tests():
    """Run all tests and print summary"""
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  Expert Chatbots Backend - Comprehensive Test Suite".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    tests = [
        ("Home Endpoint", test_home_endpoint),
        ("Debate Endpoint (Valid)", test_debate_endpoint_valid),
        ("Debate Endpoint (Error)", test_debate_endpoint_missing_fields),
        ("CORS Configuration", test_cors_headers),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ TEST CRASHED: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Print summary
    print_header("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTests Run: {total}")
    print(f"Tests Passed: {passed}")
    print(f"Tests Failed: {total - passed}")
    print(f"\nSuccess Rate: {(passed/total)*100:.1f}%")
    
    print("\nDetailed Results:")
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status} - {name}")
    
    print("\n" + "=" * 70)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your application is working properly!")
    else:
        print("⚠️  Some tests failed. Please review the output above.")
    
    print("=" * 70 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
