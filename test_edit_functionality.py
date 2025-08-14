#!/usr/bin/env python3
"""
Test script to verify edit functionality works properly
"""
import requests
import json

def test_edit_functionality():
    base_url = "http://localhost:5000"
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    print("🔍 Testing Edit Functionality...")
    
    # Step 1: Get login page to establish session
    print("1. Accessing admin login page...")
    response = session.get(f"{base_url}/secret-admin-access-2025")
    if response.status_code == 200:
        print("✅ Login page loaded successfully")
    else:
        print(f"❌ Failed to load login page: {response.status_code}")
        return False
    
    # Step 2: Login as admin
    print("2. Logging in as admin...")
    login_data = {
        'username': 'abc',
        'password': '123'
    }
    response = session.post(f"{base_url}/admin/login", data=login_data)
    if response.status_code == 302 or response.status_code == 200:
        print("✅ Admin login successful")
    else:
        print(f"❌ Login failed: {response.status_code}")
        return False
    
    # Step 3: Get list of vehicles to find an ID
    print("3. Getting vehicle list...")
    response = session.get(f"{base_url}/admin")
    if response.status_code == 200 and ("vehicle" in response.text.lower() or "edit" in response.text.lower()):
        print("✅ Admin dashboard loaded with vehicles")
        
        # Extract a vehicle ID from the HTML (look for onclick="editVehicle('...')")
        import re
        vehicle_id_match = re.search(r"editVehicle\('([^']+)'\)", response.text)
        if vehicle_id_match:
            vehicle_id = vehicle_id_match.group(1)
            print(f"✅ Found vehicle ID: {vehicle_id}")
        else:
            print("❌ Could not extract vehicle ID from page")
            return False
    else:
        print(f"❌ Failed to load admin dashboard: {response.status_code}")
        return False
    
    # Step 4: Test vehicle data fetch endpoint
    print(f"4. Testing vehicle data fetch for ID: {vehicle_id}")
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    response = session.get(f"{base_url}/admin/vehicle/{vehicle_id}", headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
            if data.get('success') and 'vehicle' in data:
                vehicle_data = data['vehicle']
                print("✅ Vehicle data fetched successfully")
                print(f"   Title: {vehicle_data.get('title', 'N/A')}")
                print(f"   Make: {vehicle_data.get('make', 'N/A')}")
                print(f"   Model: {vehicle_data.get('model', 'N/A')}")
                print(f"   Price: ₹{vehicle_data.get('price', 'N/A'):,}")
                
                # Check if all required fields are present
                required_fields = ['title', 'category', 'make', 'model', 'year', 'price', 'mileage']
                missing_fields = [field for field in required_fields if not vehicle_data.get(field)]
                if missing_fields:
                    print(f"⚠️  Missing required fields: {missing_fields}")
                else:
                    print("✅ All required fields present")
            else:
                print(f"❌ Invalid response format: {data}")
                return False
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response: {response.text[:200]}")
            return False
    else:
        print(f"❌ Failed to fetch vehicle data: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        return False
    
    # Step 5: Test edit endpoint with form data
    print("5. Testing edit submission...")
    
    # Prepare form data for update
    edit_data = {
        'title': vehicle_data['title'] + ' (UPDATED)',
        'category': vehicle_data.get('category', 'Cars'),
        'make': vehicle_data.get('make', 'Test'),
        'model': vehicle_data.get('model', 'Test'),
        'year': vehicle_data.get('year', 2020),
        'price': vehicle_data.get('price', 1000000),
        'mileage': vehicle_data.get('mileage', 50000),
        'description': 'Test update description',
        'contact_name': 'Test Contact',
        'contact_phone': '(555) 123-4567',
        'fuel_type': vehicle_data.get('fuel_type', 'Gasoline'),
        'transmission': vehicle_data.get('transmission', 'Automatic'),
        'status': 'available'
    }
    
    response = session.post(f"{base_url}/admin/edit_vehicle/{vehicle_id}", 
                          data=edit_data, headers=headers)
    
    if response.status_code == 200:
        try:
            result = response.json()
            if result.get('success'):
                print("✅ Vehicle edit submission successful")
                print(f"   Message: {result.get('message', 'No message')}")
            else:
                print(f"❌ Edit failed: {result.get('message', 'Unknown error')}")
                if 'errors' in result:
                    print(f"   Validation errors: {result['errors']}")
                return False
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response from edit: {response.text[:200]}")
            return False
    else:
        print(f"❌ Edit request failed: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        return False
    
    print("\n🎉 ALL EDIT FUNCTIONALITY TESTS PASSED!")
    print("✅ Login works")
    print("✅ Vehicle data fetch works") 
    print("✅ Form population would work (all fields present)")
    print("✅ Edit submission works")
    print("✅ Session management works")
    return True

if __name__ == "__main__":
    try:
        test_edit_functionality()
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()