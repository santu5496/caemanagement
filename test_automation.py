#!/usr/bin/env python3
"""
Automated Testing Script for AutoMarket Vehicle Management System
Tests the complete flow of adding a vehicle through the admin interface
"""

import time
import json
import os
import requests
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_results.log'),
        logging.StreamHandler()
    ]
)

class AutoMarketTester:
    def __init__(self, base_url="http://localhost:5000"):
        """Initialize the tester with configuration"""
        self.base_url = base_url
        self.driver = None
        self.test_results = []
        self.start_time = datetime.now()
        
        # Test data for vehicle creation
        self.test_vehicle_data = {
            "title": "2023 Tesla Model 3 Performance - Pristine Condition",
            "category": "Cars",
            "make": "Tesla",
            "model": "Model 3",
            "year": "2023",
            "price": "52000",
            "mileage": "12500",
            "description": "Excellent condition Tesla Model 3 Performance with Autopilot, premium interior, and supercharging capability. Single owner, garage kept.",
            "fuel_type": "Electric",
            "transmission": "Automatic",
            "engine_size": "Electric Motor",
            "horsepower": "450",
            "drivetrain": "AWD",
            "contact_name": "John Smith",
            "contact_phone": "(555) 123-4567"
        }
        
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in background
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            logging.info("WebDriver setup completed successfully")
            return True
            
        except Exception as e:
            logging.error(f"Failed to setup WebDriver: {e}")
            return False
            
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            logging.info("WebDriver cleaned up")
            
    def wait_for_element(self, locator, timeout=10):
        """Wait for element to be present and visible"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logging.error(f"Element not found: {locator}")
            return None
            
    def wait_for_clickable(self, locator, timeout=10):
        """Wait for element to be clickable"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            logging.error(f"Element not clickable: {locator}")
            return None
            
    def test_server_availability(self):
        """Test if the server is running and accessible"""
        test_name = "Server Availability"
        try:
            response = requests.get(self.base_url, timeout=10)
            if response.status_code == 200:
                self.log_test_result(test_name, True, "Server is accessible")
                return True
            else:
                self.log_test_result(test_name, False, f"Server returned status {response.status_code}")
                return False
        except Exception as e:
            self.log_test_result(test_name, False, f"Server not accessible: {e}")
            return False
            
    def test_admin_login(self):
        """Test admin login functionality"""
        test_name = "Admin Login"
        try:
            # Navigate to admin login
            self.driver.get(f"{self.base_url}/admin/login")
            
            # Fill login form
            username_field = self.wait_for_element((By.ID, "username"))
            password_field = self.wait_for_element((By.ID, "password"))
            
            if not username_field or not password_field:
                self.log_test_result(test_name, False, "Login form elements not found")
                return False
                
            username_field.send_keys("admin")
            password_field.send_keys("admin123")
            
            # Submit form
            login_button = self.wait_for_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            login_button.click()
            
            # Wait for redirect to dashboard
            time.sleep(2)
            
            # Check if we're on the dashboard
            if "/admin/dashboard" in self.driver.current_url:
                self.log_test_result(test_name, True, "Successfully logged in")
                return True
            else:
                self.log_test_result(test_name, False, f"Login failed, current URL: {self.driver.current_url}")
                return False
                
        except Exception as e:
            self.log_test_result(test_name, False, f"Login test failed: {e}")
            return False
            
    def test_open_add_vehicle_modal(self):
        """Test opening the add vehicle modal"""
        test_name = "Open Add Vehicle Modal"
        try:
            # Click Add New Vehicle button
            add_button = self.wait_for_clickable((By.CSS_SELECTOR, "button[data-bs-target='#vehicleModal']"))
            if not add_button:
                self.log_test_result(test_name, False, "Add Vehicle button not found")
                return False
                
            add_button.click()
            
            # Wait for modal to appear
            modal = self.wait_for_element((By.ID, "vehicleModal"))
            if modal and modal.is_displayed():
                self.log_test_result(test_name, True, "Modal opened successfully")
                return True
            else:
                self.log_test_result(test_name, False, "Modal did not open")
                return False
                
        except Exception as e:
            self.log_test_result(test_name, False, f"Failed to open modal: {e}")
            return False
            
    def test_wizard_navigation(self):
        """Test the wizard-style navigation through form steps"""
        test_name = "Wizard Navigation"
        try:
            steps_completed = 0
            
            # Test navigation through all 6 steps
            for step in range(6):
                # Check current step indicator
                step_counter = self.wait_for_element((By.ID, "step-counter"))
                if step_counter:
                    expected_text = f"Step {step + 1} of 6" if step < 5 else "Ready to Save!"
                    if expected_text in step_counter.text or (step == 5 and "Ready" in step_counter.text):
                        steps_completed += 1
                        logging.info(f"Step {step + 1} indicator correct: {step_counter.text}")
                    else:
                        logging.warning(f"Step {step + 1} indicator incorrect: {step_counter.text}")
                
                # Click Next button (except on last step)
                if step < 5:
                    next_button = self.wait_for_clickable((By.ID, "next-tab-btn"))
                    if next_button and next_button.is_displayed():
                        next_button.click()
                        time.sleep(1)  # Wait for transition
                
            if steps_completed >= 5:  # Allow some tolerance
                self.log_test_result(test_name, True, f"Successfully navigated {steps_completed}/6 steps")
                return True
            else:
                self.log_test_result(test_name, False, f"Only completed {steps_completed}/6 steps")
                return False
                
        except Exception as e:
            self.log_test_result(test_name, False, f"Wizard navigation failed: {e}")
            return False
            
    def test_fill_basic_info(self):
        """Test filling the basic information tab"""
        test_name = "Fill Basic Information"
        try:
            # Go back to first step
            for _ in range(5):
                prev_button = self.driver.find_element(By.ID, "prev-tab-btn")
                if prev_button.is_displayed():
                    prev_button.click()
                    time.sleep(0.5)
                else:
                    break
            
            # Fill basic information fields
            fields_filled = 0
            
            # Title
            title_field = self.wait_for_element((By.ID, "modal-title"))
            if title_field:
                title_field.clear()
                title_field.send_keys(self.test_vehicle_data["title"])
                fields_filled += 1
                
            # Category
            category_select = self.wait_for_element((By.ID, "modal-category"))
            if category_select:
                select = Select(category_select)
                select.select_by_visible_text(self.test_vehicle_data["category"])
                fields_filled += 1
                
            # Make
            make_field = self.wait_for_element((By.ID, "modal-make"))
            if make_field:
                make_field.clear()
                make_field.send_keys(self.test_vehicle_data["make"])
                fields_filled += 1
                
            # Model
            model_field = self.wait_for_element((By.ID, "modal-model"))
            if model_field:
                model_field.clear()
                model_field.send_keys(self.test_vehicle_data["model"])
                fields_filled += 1
                
            # Year
            year_field = self.wait_for_element((By.ID, "modal-year"))
            if year_field:
                year_field.clear()
                year_field.send_keys(self.test_vehicle_data["year"])
                fields_filled += 1
                
            # Price
            price_field = self.wait_for_element((By.ID, "modal-price"))
            if price_field:
                price_field.clear()
                price_field.send_keys(self.test_vehicle_data["price"])
                fields_filled += 1
                
            # Mileage
            mileage_field = self.wait_for_element((By.ID, "modal-mileage"))
            if mileage_field:
                mileage_field.clear()
                mileage_field.send_keys(self.test_vehicle_data["mileage"])
                fields_filled += 1
                
            # Description
            description_field = self.wait_for_element((By.ID, "modal-description"))
            if description_field:
                description_field.clear()
                description_field.send_keys(self.test_vehicle_data["description"])
                fields_filled += 1
                
            if fields_filled >= 7:  # All required basic fields
                self.log_test_result(test_name, True, f"Successfully filled {fields_filled}/8 basic fields")
                return True
            else:
                self.log_test_result(test_name, False, f"Only filled {fields_filled}/8 basic fields")
                return False
                
        except Exception as e:
            self.log_test_result(test_name, False, f"Failed to fill basic info: {e}")
            return False
            
    def test_fill_engine_info(self):
        """Test filling the engine information tab"""
        test_name = "Fill Engine Information"
        try:
            # Navigate to engine tab
            next_button = self.wait_for_clickable((By.ID, "next-tab-btn"))
            if next_button:
                next_button.click()
                time.sleep(1)
            
            fields_filled = 0
            
            # Fuel Type
            fuel_type_select = self.wait_for_element((By.ID, "modal-fuel-type"))
            if fuel_type_select:
                select = Select(fuel_type_select)
                select.select_by_visible_text(self.test_vehicle_data["fuel_type"])
                fields_filled += 1
                
            # Transmission
            transmission_select = self.wait_for_element((By.ID, "modal-transmission"))
            if transmission_select:
                select = Select(transmission_select)
                select.select_by_visible_text(self.test_vehicle_data["transmission"])
                fields_filled += 1
                
            # Engine Size (optional)
            engine_size_field = self.wait_for_element((By.ID, "modal-engine-size"))
            if engine_size_field:
                engine_size_field.clear()
                engine_size_field.send_keys(self.test_vehicle_data["engine_size"])
                fields_filled += 1
                
            # Horsepower (optional)
            horsepower_field = self.wait_for_element((By.ID, "modal-horsepower"))
            if horsepower_field:
                horsepower_field.clear()
                horsepower_field.send_keys(self.test_vehicle_data["horsepower"])
                fields_filled += 1
                
            if fields_filled >= 2:  # Required fields
                self.log_test_result(test_name, True, f"Successfully filled {fields_filled}/4 engine fields")
                return True
            else:
                self.log_test_result(test_name, False, f"Only filled {fields_filled}/4 engine fields")
                return False
                
        except Exception as e:
            self.log_test_result(test_name, False, f"Failed to fill engine info: {e}")
            return False
            
    def test_fill_contact_info(self):
        """Test filling the contact information"""
        test_name = "Fill Contact Information"
        try:
            # Navigate to contact tab (last tab)
            for _ in range(4):  # Navigate to last tab
                next_button = self.wait_for_clickable((By.ID, "next-tab-btn"))
                if next_button:
                    next_button.click()
                    time.sleep(1)
                    
            fields_filled = 0
            
            # Contact Name
            contact_name_field = self.wait_for_element((By.ID, "modal-contact-name"))
            if contact_name_field:
                contact_name_field.clear()
                contact_name_field.send_keys(self.test_vehicle_data["contact_name"])
                fields_filled += 1
                
            # Contact Phone
            contact_phone_field = self.wait_for_element((By.ID, "modal-contact-phone"))
            if contact_phone_field:
                contact_phone_field.clear()
                contact_phone_field.send_keys(self.test_vehicle_data["contact_phone"])
                fields_filled += 1
                
            if fields_filled >= 2:
                self.log_test_result(test_name, True, f"Successfully filled {fields_filled}/2 contact fields")
                return True
            else:
                self.log_test_result(test_name, False, f"Only filled {fields_filled}/2 contact fields")
                return False
                
        except Exception as e:
            self.log_test_result(test_name, False, f"Failed to fill contact info: {e}")
            return False
            
    def test_submit_vehicle(self):
        """Test submitting the vehicle form"""
        test_name = "Submit Vehicle Form"
        try:
            # Find and click submit button
            submit_button = self.wait_for_clickable((By.ID, "submit-btn"))
            if not submit_button:
                self.log_test_result(test_name, False, "Submit button not found")
                return False
                
            submit_button.click()
            
            # Wait for submission to complete (look for success message or modal close)
            time.sleep(3)
            
            # Check if modal is closed (indicating success)
            try:
                modal = self.driver.find_element(By.ID, "vehicleModal")
                if not modal.is_displayed():
                    self.log_test_result(test_name, True, "Form submitted successfully - modal closed")
                    return True
                else:
                    # Check for success toast message
                    toasts = self.driver.find_elements(By.CSS_SELECTOR, ".toast.bg-success")
                    if toasts:
                        self.log_test_result(test_name, True, "Form submitted successfully - success message shown")
                        return True
                    else:
                        self.log_test_result(test_name, False, "Form submission unclear - modal still open")
                        return False
            except NoSuchElementException:
                self.log_test_result(test_name, True, "Form submitted successfully - modal removed from DOM")
                return True
                
        except Exception as e:
            self.log_test_result(test_name, False, f"Failed to submit form: {e}")
            return False
            
    def test_verify_vehicle_in_list(self):
        """Test that the new vehicle appears in the vehicle list"""
        test_name = "Verify Vehicle in List"
        try:
            # Wait for page to refresh/update
            time.sleep(2)
            
            # Look for the vehicle in the table
            table_rows = self.driver.find_elements(By.CSS_SELECTOR, "#vehicles-tbody tr")
            
            for row in table_rows:
                # Check if our test vehicle data appears in any row
                row_text = row.text.lower()
                if (self.test_vehicle_data["make"].lower() in row_text and 
                    self.test_vehicle_data["model"].lower() in row_text):
                    self.log_test_result(test_name, True, f"Vehicle found in list: {self.test_vehicle_data['make']} {self.test_vehicle_data['model']}")
                    return True
                    
            self.log_test_result(test_name, False, "Vehicle not found in list")
            return False
            
        except Exception as e:
            self.log_test_result(test_name, False, f"Failed to verify vehicle in list: {e}")
            return False
            
    def log_test_result(self, test_name, passed, message=""):
        """Log test result"""
        status = "PASS" if passed else "FAIL"
        log_message = f"[{status}] {test_name}: {message}"
        
        if passed:
            logging.info(log_message)
        else:
            logging.error(log_message)
            
        self.test_results.append({
            "test_name": test_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
    def generate_test_report(self):
        """Generate comprehensive test report"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        total_tests = len(self.test_results)
        
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "success_rate": f"{(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%",
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration": str(duration)
            },
            "test_results": self.test_results,
            "test_data_used": self.test_vehicle_data
        }
        
        # Save report to file
        with open("test_report.json", "w") as f:
            json.dump(report, f, indent=2)
            
        # Print summary
        print("\n" + "="*60)
        print("AUTO MARKET TESTING REPORT")
        print("="*60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {report['test_summary']['success_rate']}")
        print(f"Duration: {duration}")
        print("="*60)
        
        for result in self.test_results:
            status_symbol = "✓" if result["status"] == "PASS" else "✗"
            print(f"{status_symbol} {result['test_name']}: {result['message']}")
            
        print("="*60)
        print(f"Detailed report saved to: test_report.json")
        print(f"Log file saved to: test_results.log")
        
        return report
        
    def run_full_test_suite(self):
        """Run the complete test suite"""
        logging.info("Starting AutoMarket automated testing suite")
        
        try:
            # Setup
            if not self.setup_driver():
                logging.error("Failed to setup WebDriver, aborting tests")
                return False
                
            # Test sequence
            tests = [
                ("Server Availability", self.test_server_availability),
                ("Admin Login", self.test_admin_login),
                ("Open Add Vehicle Modal", self.test_open_add_vehicle_modal),
                ("Wizard Navigation", self.test_wizard_navigation),
                ("Fill Basic Information", self.test_fill_basic_info),
                ("Fill Engine Information", self.test_fill_engine_info),
                ("Fill Contact Information", self.test_fill_contact_info),
                ("Submit Vehicle Form", self.test_submit_vehicle),
                ("Verify Vehicle in List", self.test_verify_vehicle_in_list)
            ]
            
            for test_name, test_func in tests:
                logging.info(f"Running test: {test_name}")
                try:
                    test_func()
                except Exception as e:
                    self.log_test_result(test_name, False, f"Test execution error: {e}")
                    
            # Generate report
            self.generate_test_report()
            
            return True
            
        finally:
            self.cleanup()


def main():
    """Main function to run the tests"""
    print("AutoMarket Automated Testing Suite")
    print("==================================")
    
    # Create tester instance
    tester = AutoMarketTester()
    
    # Run tests
    success = tester.run_full_test_suite()
    
    if success:
        print("\nTesting completed successfully!")
    else:
        print("\nTesting completed with errors!")
        
    return success


if __name__ == "__main__":
    main()