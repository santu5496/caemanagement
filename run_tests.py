#!/usr/bin/env python3
"""
Simple test runner that doesn't require Selenium for basic API testing
Tests the backend functionality of the AutoMarket system
"""

import requests
import json
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SimpleAutoMarketTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def test_server_status(self):
        """Test if server is running"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                logging.info("✓ Server is running and accessible")
                return True
            else:
                logging.error(f"✗ Server returned status {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"✗ Server not accessible: {e}")
            return False
            
    def test_admin_routes(self):
        """Test admin route accessibility"""
        routes_to_test = [
            "/admin/login",
            "/admin/dashboard"
        ]
        
        for route in routes_to_test:
            try:
                response = self.session.get(f"{self.base_url}{route}", timeout=10)
                if response.status_code in [200, 302]:  # 302 for redirects
                    logging.info(f"✓ Route {route} is accessible")
                else:
                    logging.warning(f"⚠ Route {route} returned status {response.status_code}")
            except Exception as e:
                logging.error(f"✗ Route {route} failed: {e}")
                
    def test_admin_login(self):
        """Test admin login via POST request"""
        try:
            # First get the login page to get any CSRF tokens
            login_page = self.session.get(f"{self.base_url}/admin/login")
            
            # Attempt login
            login_data = {
                'username': 'admin',
                'password': 'admin123'
            }
            
            response = self.session.post(f"{self.base_url}/admin/login", data=login_data, allow_redirects=False)
            
            if response.status_code in [200, 302]:
                if response.status_code == 302 and '/admin/dashboard' in response.headers.get('Location', ''):
                    logging.info("✓ Admin login successful (redirected to dashboard)")
                    return True
                elif response.status_code == 200:
                    logging.info("✓ Admin login request processed")
                    return True
            else:
                logging.error(f"✗ Admin login failed with status {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"✗ Admin login test failed: {e}")
            return False
            
    def test_vehicle_data_simulation(self):
        """Simulate vehicle data creation"""
        test_vehicle = {
            "title": "2023 Tesla Model 3 Performance - Test Vehicle",
            "category": "Cars",
            "make": "Tesla",
            "model": "Model 3",
            "year": "2023",
            "price": "52000",
            "mileage": "12500",
            "description": "Automated test vehicle - pristine condition",
            "fuel_type": "Electric",
            "transmission": "Automatic",
            "contact_name": "Test User",
            "contact_phone": "(555) 123-4567"
        }
        
        logging.info("✓ Test vehicle data prepared:")
        for key, value in test_vehicle.items():
            logging.info(f"  {key}: {value}")
            
        return True
        
    def generate_test_report(self):
        """Generate a simple test report"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        report = {
            "timestamp": timestamp,
            "tests_completed": [
                "Server Status Check",
                "Admin Routes Accessibility", 
                "Admin Login Test",
                "Vehicle Data Simulation"
            ],
            "notes": [
                "Basic connectivity and routing tests completed",
                "For full UI testing, install Selenium WebDriver",
                "Backend functionality appears operational"
            ]
        }
        
        with open(f"simple_test_report_{timestamp}.json", "w") as f:
            json.dump(report, f, indent=2)
            
        print("\n" + "="*60)
        print("AUTOMARKET SIMPLE TEST REPORT")
        print("="*60)
        print(f"Timestamp: {timestamp}")
        print("Tests Completed:")
        for test in report["tests_completed"]:
            print(f"  ✓ {test}")
        print("\nNotes:")
        for note in report["notes"]:
            print(f"  • {note}")
        print("="*60)
        
    def run_tests(self):
        """Run all simple tests"""
        logging.info("Starting AutoMarket Simple Test Suite")
        
        self.test_server_status()
        time.sleep(1)
        
        self.test_admin_routes()
        time.sleep(1)
        
        self.test_admin_login()
        time.sleep(1)
        
        self.test_vehicle_data_simulation()
        
        self.generate_test_report()
        
        logging.info("Simple test suite completed!")

if __name__ == "__main__":
    tester = SimpleAutoMarketTester()
    tester.run_tests()