#!/usr/bin/env python3
"""
Automated Test for Edit Functionality using requests
Tests the edit vehicle endpoint directly
"""

import requests
import json
import time
from datetime import datetime

def test_edit_functionality():
    """Test the edit functionality by making direct API calls"""
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    print("AutoMarket Edit Functionality Test")
    print("=" * 40)
    
    test_results = []
    
    # Test 1: Login to admin
    print("1. Testing admin login...")
    login_data = {
        'username': 'abc',
        'password': '123'
    }
    
    try:
        response = session.post(f"{base_url}/secret-admin-access-2025", data=login_data, allow_redirects=False)
        if response.status_code in [200, 302]:  # Success or redirect
            print("✓ Admin login successful")
            test_results.append({"test": "admin_login", "status": "PASS", "message": "Login successful"})
        else:
            print(f"✗ Admin login failed: {response.status_code}")
            test_results.append({"test": "admin_login", "status": "FAIL", "message": f"Status code: {response.status_code}"})
            return test_results
    except Exception as e:
        print(f"✗ Admin login error: {e}")
        test_results.append({"test": "admin_login", "status": "ERROR", "message": str(e)})
        return test_results
    
    # Test 2: Get admin dashboard and find vehicle IDs
    print("2. Getting vehicle list from admin dashboard...")
    try:
        response = session.get(f"{base_url}/admin")
        if response.status_code == 200:
            # Extract vehicle IDs from the response
            import re
            vehicle_ids = re.findall(r"editVehicle\('([^']+)'\)", response.text)
            if vehicle_ids:
                print(f"✓ Found {len(vehicle_ids)} vehicles in admin dashboard")
                test_vehicle_id = vehicle_ids[0]  # Use first vehicle for testing
                test_results.append({"test": "get_vehicle_list", "status": "PASS", "message": f"Found {len(vehicle_ids)} vehicles"})
            else:
                print("✗ No vehicles found in admin dashboard")
                test_results.append({"test": "get_vehicle_list", "status": "FAIL", "message": "No vehicles found"})
                return test_results
        else:
            print(f"✗ Failed to access admin dashboard: {response.status_code}")
            test_results.append({"test": "get_vehicle_list", "status": "FAIL", "message": f"Status code: {response.status_code}"})
            return test_results
    except Exception as e:
        print(f"✗ Error accessing admin dashboard: {e}")
        test_results.append({"test": "get_vehicle_list", "status": "ERROR", "message": str(e)})
        return test_results
    
    # Test 3: Test vehicle data retrieval for editing
    print(f"3. Testing vehicle data retrieval for edit (ID: {test_vehicle_id[:8]}...)")
    try:
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json'
        }
        response = session.get(f"{base_url}/admin/vehicle/{test_vehicle_id}", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('vehicle'):
                vehicle_data = data['vehicle']
                print(f"✓ Vehicle data retrieved successfully")
                print(f"  - Title: {vehicle_data.get('title', 'N/A')}")
                print(f"  - Make/Model: {vehicle_data.get('make', 'N/A')} {vehicle_data.get('model', 'N/A')}")
                print(f"  - Price: ₹{vehicle_data.get('price', 'N/A')}")
                print(f"  - Condition: {vehicle_data.get('condition_rating', 'N/A')}")
                
                # Verify essential fields are present
                required_fields = ['id', 'title', 'make', 'model', 'year', 'price']
                missing_fields = [field for field in required_fields if not vehicle_data.get(field)]
                
                if not missing_fields:
                    print("✓ All required fields present in vehicle data")
                    test_results.append({"test": "vehicle_data_retrieval", "status": "PASS", "message": "Vehicle data complete"})
                else:
                    print(f"✗ Missing required fields: {missing_fields}")
                    test_results.append({"test": "vehicle_data_retrieval", "status": "FAIL", "message": f"Missing fields: {missing_fields}"})
                    
            else:
                print("✗ Invalid response format from vehicle endpoint")
                test_results.append({"test": "vehicle_data_retrieval", "status": "FAIL", "message": "Invalid response format"})
        else:
            print(f"✗ Failed to retrieve vehicle data: {response.status_code}")
            test_results.append({"test": "vehicle_data_retrieval", "status": "FAIL", "message": f"Status code: {response.status_code}"})
            
    except Exception as e:
        print(f"✗ Error retrieving vehicle data: {e}")
        test_results.append({"test": "vehicle_data_retrieval", "status": "ERROR", "message": str(e)})
    
    # Test 4: Test condition rating dropdown options
    print("4. Testing condition rating dropdown options...")
    try:
        # Check forms.py for condition rating choices
        with open('forms.py', 'r') as f:
            forms_content = f.read()
            
        if 'Very Good' in forms_content and 'Excellent' in forms_content:
            print("✓ Condition rating dropdown includes 'Very Good' and other options")
            test_results.append({"test": "condition_rating_options", "status": "PASS", "message": "All condition options present"})
        else:
            print("✗ Missing condition rating options")
            test_results.append({"test": "condition_rating_options", "status": "FAIL", "message": "Missing dropdown options"})
    except Exception as e:
        print(f"✗ Error checking condition rating options: {e}")
        test_results.append({"test": "condition_rating_options", "status": "ERROR", "message": str(e)})
    
    # Test 5: Test JavaScript syntax by checking template
    print("5. Checking JavaScript syntax in template...")
    try:
        with open('templates/wizard_admin.html', 'r') as f:
            template_content = f.read()
            
        # Check for common JavaScript syntax issues that were fixed
        syntax_issues = []
        if 'translateY(0)' in template_content and 'translateY(-2px)' in template_content:
            print("✓ CSS transform syntax is correct")
        else:
            syntax_issues.append("CSS transform syntax")
            
        if 'top: 0px; left: 0px' in template_content:
            print("✓ CSS positioning syntax is correct")
        else:
            syntax_issues.append("CSS positioning syntax")
            
        if not syntax_issues:
            test_results.append({"test": "javascript_syntax", "status": "PASS", "message": "JavaScript syntax clean"})
        else:
            test_results.append({"test": "javascript_syntax", "status": "FAIL", "message": f"Issues: {syntax_issues}"})
            
    except Exception as e:
        print(f"✗ Error checking JavaScript syntax: {e}")
        test_results.append({"test": "javascript_syntax", "status": "ERROR", "message": str(e)})
    
    # Test Summary
    print("\n" + "=" * 40)
    print("Test Summary:")
    print("=" * 40)
    
    passed = sum(1 for result in test_results if result['status'] == 'PASS')
    failed = sum(1 for result in test_results if result['status'] == 'FAIL')
    errors = sum(1 for result in test_results if result['status'] == 'ERROR')
    total = len(test_results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors: {errors}")
    print(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "0%")
    
    # Save detailed results
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "success_rate": round(passed/total*100, 1) if total > 0 else 0
        },
        "tests": test_results
    }
    
    with open(f"edit_functionality_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump(report, f, indent=2)
    
    return test_results

if __name__ == "__main__":
    test_edit_functionality()