#!/usr/bin/env python3
"""
Complete Edit Functionality Test
Tests the full edit workflow: fetch -> modify -> save -> verify
"""

import requests
import json
import time
from datetime import datetime

def test_edit_complete_flow():
    """Test the complete edit functionality workflow"""
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    print("AutoMarket Complete Edit Functionality Test")
    print("=" * 50)
    
    test_results = []
    
    # Step 1: Login to admin
    print("1. Logging into admin...")
    login_data = {'username': 'abc', 'password': '123'}
    
    try:
        response = session.post(f"{base_url}/secret-admin-access-2025", data=login_data, allow_redirects=False)
        if response.status_code in [200, 302]:
            print("✓ Admin login successful")
        else:
            print(f"✗ Admin login failed: {response.status_code}")
            return
    except Exception as e:
        print(f"✗ Admin login error: {e}")
        return
    
    # Step 2: Get a vehicle to edit
    print("2. Finding a vehicle to test edit...")
    try:
        response = session.get(f"{base_url}/admin")
        import re
        vehicle_ids = re.findall(r"editVehicle\('([^']+)'\)", response.text)
        if not vehicle_ids:
            print("✗ No vehicles found for testing")
            return
        
        test_vehicle_id = vehicle_ids[0]
        print(f"✓ Selected vehicle ID: {test_vehicle_id[:8]}...")
    except Exception as e:
        print(f"✗ Error finding vehicles: {e}")
        return
    
    # Step 3: Fetch original vehicle data
    print("3. Fetching original vehicle data...")
    try:
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json'
        }
        response = session.get(f"{base_url}/admin/vehicle/{test_vehicle_id}", headers=headers)
        
        if response.status_code == 200:
            original_data = response.json()
            if original_data.get('success') and original_data.get('vehicle'):
                vehicle = original_data['vehicle']
                print(f"✓ Original data fetched")
                print(f"  - Title: {vehicle.get('title')}")
                print(f"  - Price: ₹{vehicle.get('price')}")
                print(f"  - Mileage: {vehicle.get('mileage')}")
                print(f"  - Description: {vehicle.get('description')[:50]}...")
            else:
                print("✗ Invalid response format")
                return
        else:
            print(f"✗ Failed to fetch vehicle data: {response.status_code}")
            return
    except Exception as e:
        print(f"✗ Error fetching vehicle data: {e}")
        return
    
    # Step 4: Test CSRF token handling and form structure
    print("4. Testing form structure and CSRF handling...")
    try:
        # Get the admin page to extract CSRF token
        admin_response = session.get(f"{base_url}/admin")
        
        # Extract CSRF token from the page
        import re
        csrf_match = re.search(r'name="csrf_token" value="([^"]+)"', admin_response.text)
        csrf_token = csrf_match.group(1) if csrf_match else ""
        
        if csrf_token:
            print(f"✓ CSRF token found: {csrf_token[:10]}...")
        else:
            print("⚠ No CSRF token found, proceeding without it")
        
        # Test basic form validation
        print("5. Testing form validation with minimal data...")
        
        # Try with minimal required fields
        minimal_edit_data = {
            'csrf_token': csrf_token,
            'title': vehicle.get('title') + ' [TEST]',
            'category': vehicle.get('category'),
            'make': vehicle.get('make'),
            'model': vehicle.get('model'),
            'year': str(vehicle.get('year')),
            'price': str(float(vehicle.get('price', 0)) + 1000),
            'mileage': str(int(vehicle.get('mileage', 0)) + 100),
            'contact_name': vehicle.get('contact_name'),
            'contact_phone': vehicle.get('contact_phone'),
            'description': (vehicle.get('description') or '') + ' [AUTOMATED TEST]'
        }
        
        # Submit the edit
        edit_response = session.post(
            f"{base_url}/admin/edit_vehicle/{test_vehicle_id}",
            data=minimal_edit_data,
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )
        
        print(f"Edit response status: {edit_response.status_code}")
        print(f"Edit response headers: {dict(edit_response.headers)}")
        
        if edit_response.status_code == 200:
            try:
                edit_result = edit_response.json()
                print(f"Edit response JSON: {edit_result}")
                
                if edit_result.get('success'):
                    print("✓ Edit submitted successfully!")
                    print(f"  Message: {edit_result.get('message')}")
                    
                    # Verify the change
                    time.sleep(1)
                    verify_response = session.get(f"{base_url}/admin/vehicle/{test_vehicle_id}", headers=headers)
                    
                    if verify_response.status_code == 200:
                        verify_data = verify_response.json()
                        if verify_data.get('success'):
                            updated_vehicle = verify_data['vehicle']
                            updated_title = updated_vehicle.get('title', '')
                            
                            if '[TEST]' in updated_title:
                                print("✓ Edit verification successful - changes were saved!")
                                test_results.append({"test": "edit_functionality", "status": "PASS", "message": "Edit and save successful"})
                                
                                # Clean up by removing the test marker
                                cleanup_data = minimal_edit_data.copy()
                                cleanup_data['title'] = vehicle.get('title')  # Original title
                                cleanup_data['price'] = str(vehicle.get('price'))  # Original price
                                cleanup_data['mileage'] = str(vehicle.get('mileage'))  # Original mileage
                                cleanup_data['description'] = vehicle.get('description', '')  # Original description
                                
                                cleanup_response = session.post(
                                    f"{base_url}/admin/edit_vehicle/{test_vehicle_id}",
                                    data=cleanup_data,
                                    headers={'X-Requested-With': 'XMLHttpRequest'}
                                )
                                
                                if cleanup_response.status_code == 200:
                                    print("✓ Test data cleaned up successfully")
                                else:
                                    print("⚠ Test successful but cleanup failed")
                                    
                            else:
                                print("✗ Changes were not saved properly")
                                test_results.append({"test": "edit_functionality", "status": "FAIL", "message": "Changes not persisted"})
                        else:
                            print("✗ Failed to verify changes")
                            test_results.append({"test": "edit_functionality", "status": "FAIL", "message": "Verification failed"})
                    else:
                        print(f"✗ Verification request failed: {verify_response.status_code}")
                        test_results.append({"test": "edit_functionality", "status": "FAIL", "message": f"Verification failed: {verify_response.status_code}"})
                        
                else:
                    print(f"✗ Edit failed: {edit_result.get('message')}")
                    if 'errors' in edit_result:
                        print(f"  Validation errors: {edit_result['errors']}")
                    test_results.append({"test": "edit_functionality", "status": "FAIL", "message": edit_result.get('message')})
                    
            except json.JSONDecodeError:
                print(f"✗ Invalid JSON response: {edit_response.text[:200]}")
                test_results.append({"test": "edit_functionality", "status": "FAIL", "message": "Invalid JSON response"})
                
        else:
            print(f"✗ Edit request failed with status {edit_response.status_code}")
            print(f"Response content: {edit_response.text[:500]}")
            test_results.append({"test": "edit_functionality", "status": "FAIL", "message": f"HTTP {edit_response.status_code}"})
            
    except Exception as e:
        print(f"✗ Error during edit testing: {e}")
        import traceback
        traceback.print_exc()
        test_results.append({"test": "edit_functionality", "status": "ERROR", "message": str(e)})
    
    # Summary
    print("\n" + "=" * 50)
    print("COMPLETE EDIT FUNCTIONALITY TEST RESULTS")
    print("=" * 50)
    
    if test_results:
        for result in test_results:
            status_symbol = "✓" if result['status'] == 'PASS' else "⚠" if result['status'] == 'PARTIAL' else "✗"
            print(f"{status_symbol} {result['test'].upper()}: {result['status']}")
            print(f"   {result['message']}")
    else:
        print("✗ No test results generated - test setup failed")
    
    return test_results

if __name__ == "__main__":
    test_edit_complete_flow()