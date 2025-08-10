# AutoMarket Testing Suite

This directory contains comprehensive testing tools for the AutoMarket vehicle management system.

## Testing Files Overview

### 1. `test_automation.py` - Full Selenium Automation
**Comprehensive UI automation testing using Selenium WebDriver**

**Features:**
- Complete end-to-end testing of vehicle addition workflow
- Wizard navigation testing
- Form validation testing
- UI element visibility verification
- Automated report generation

**Requirements:**
- Selenium WebDriver
- Chrome/Chromium browser
- Python 3.7+

**Usage:**
```bash
python3 test_automation.py
```

### 2. `run_tests.py` - Simple Backend Testing
**Lightweight testing without browser automation**

**Features:**
- Server connectivity testing
- Route accessibility verification
- Basic login functionality testing
- API endpoint validation

**Usage:**
```bash
python3 run_tests.py
```

### 3. `test_runner.sh` - Automated Test Executor
**Complete test suite runner with environment setup**

**Features:**
- Automatic virtual environment creation
- Dependency installation
- Server status checking
- Sequential test execution

**Usage:**
```bash
./test_runner.sh
```

### 4. `manual_test_checklist.md` - Manual Testing Guide
**Comprehensive manual testing checklist**

**Covers:**
- Step-by-step testing procedures
- Expected results for each test case
- Browser compatibility testing
- Mobile responsiveness verification
- Performance and accessibility testing

## Quick Start

### Option 1: Run All Tests Automatically
```bash
./test_runner.sh
```

### Option 2: Run Simple Tests Only
```bash
python3 run_tests.py
```

### Option 3: Manual Testing
Follow the checklist in `manual_test_checklist.md`

## Test Scenarios Covered

### 1. Server Availability
- ✅ Server running and accessible
- ✅ Core routes responding
- ✅ Database connectivity

### 2. Authentication
- ✅ Admin login functionality
- ✅ Session management
- ✅ Access control

### 3. Vehicle Management UI
- ✅ Modal opening and closing
- ✅ Wizard navigation (6 steps)
- ✅ Progress indicators
- ✅ Form field visibility

### 4. Form Functionality
- ✅ Required field validation
- ✅ Data entry and persistence
- ✅ Form submission
- ✅ Success/error handling

### 5. Data Operations
- ✅ Create new vehicle records
- ✅ Edit existing vehicles
- ✅ Delete vehicles
- ✅ Status updates

### 6. UI/UX Validation
- ✅ Text visibility and contrast
- ✅ Responsive design
- ✅ Navigation flow
- ✅ Error messaging

## Test Data

The automation tests use the following test vehicle data:

```json
{
  "title": "2023 Tesla Model 3 Performance - Pristine Condition",
  "category": "Cars",
  "make": "Tesla",
  "model": "Model 3",
  "year": "2023",
  "price": "52000",
  "mileage": "12500",
  "description": "Excellent condition Tesla Model 3 Performance...",
  "fuel_type": "Electric",
  "transmission": "Automatic",
  "contact_name": "John Smith",
  "contact_phone": "(555) 123-4567"
}
```

## Test Reports

### Automated Reports
- `test_report.json` - Complete test results with timestamps
- `test_results.log` - Detailed execution logs
- `simple_test_report_*.json` - Basic connectivity test results

### Manual Testing
- Use `manual_test_checklist.md` to track manual test progress
- Document results directly in the checklist

## Dependencies

### For Full Automation Testing
```bash
pip install selenium webdriver-manager requests pytest
```

### For Simple Testing
```bash
pip install requests
```

## Browser Requirements

For Selenium automation testing:
- **Chrome/Chromium** (recommended)
- **Firefox** (with geckodriver)
- **Safari** (macOS only)
- **Edge** (Windows)

## Troubleshooting

### Common Issues

1. **"WebDriver not found"**
   - Install Chrome browser
   - Install webdriver-manager: `pip install webdriver-manager`

2. **"Server not accessible"**
   - Ensure server is running on port 5000
   - Check firewall settings
   - Verify database is running

3. **"Permission denied on test_runner.sh"**
   - Make script executable: `chmod +x test_runner.sh`

4. **Tests fail due to timing**
   - Increase timeout values in test files
   - Check server performance

### Debug Mode

To run tests with more verbose output:

```bash
# For automation tests
python3 -u test_automation.py

# For simple tests with debug logging
python3 -c "import logging; logging.basicConfig(level=logging.DEBUG); exec(open('run_tests.py').read())"
```

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run AutoMarket Tests
  run: |
    python3 run_tests.py
    ./test_runner.sh
```

## Contributing to Tests

When adding new features to AutoMarket:

1. Add corresponding test cases to `test_automation.py`
2. Update the manual test checklist
3. Ensure all tests pass before deployment
4. Update test data if needed

## Test Coverage

Current test coverage includes:
- ✅ User authentication
- ✅ Vehicle CRUD operations
- ✅ UI wizard navigation
- ✅ Form validation
- ✅ Database operations
- ✅ Error handling
- ⏳ Image upload (basic testing)
- ⏳ Advanced search/filtering
- ⏳ Performance under load

## Support

For testing issues or questions:
1. Check the troubleshooting section above
2. Review test logs in `test_results.log`
3. Verify server status and dependencies
4. Ensure all required services are running

---

**Note**: Always run tests in a development environment, not in production!