#!/bin/bash

# AutoMarket Testing Suite Runner
# This script sets up and runs the automated tests

echo "=========================================="
echo "AutoMarket Automated Testing Suite"
echo "=========================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

echo "✅ Python3 found"

# Create virtual environment for testing if it doesn't exist
if [ ! -d "test_env" ]; then
    echo "📦 Creating virtual environment for testing..."
    python3 -m venv test_env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source test_env/bin/activate

# Install testing dependencies
echo "📥 Installing testing dependencies..."
pip install requests selenium webdriver-manager pytest

# Check if server is running
echo "🌐 Checking if AutoMarket server is running..."
if curl -s http://localhost:5000 > /dev/null; then
    echo "✅ Server is running on port 5000"
    SERVER_RUNNING=true
else
    echo "⚠️  Server is not running on port 5000"
    echo "Please start the server with: gunicorn --bind 0.0.0.0:5000 main:app"
    SERVER_RUNNING=false
fi

# Run simple tests first
echo "🧪 Running simple connectivity tests..."
python3 run_tests.py

if [ "$SERVER_RUNNING" = true ]; then
    echo ""
    echo "🧪 Running full automation tests..."
    echo "Note: This requires Chrome/Chromium browser to be installed"
    
    # Try to run full selenium tests
    if command -v google-chrome &> /dev/null || command -v chromium-browser &> /dev/null; then
        echo "✅ Chrome browser found, running full tests..."
        python3 test_automation.py
    else
        echo "⚠️  Chrome browser not found. Skipping UI automation tests."
        echo "To run full tests, install Google Chrome or Chromium browser."
    fi
else
    echo "⚠️  Skipping full tests - server not running"
fi

echo ""
echo "=========================================="
echo "Testing Complete!"
echo "=========================================="
echo "Check the following files for results:"
echo "  📄 simple_test_report_*.json - Basic connectivity tests"
echo "  📄 test_report.json - Full automation test results (if ran)"
echo "  📄 test_results.log - Detailed test logs"
echo "=========================================="

# Deactivate virtual environment
deactivate