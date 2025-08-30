#!/usr/bin/env python3
"""
WSGI entry point for production deployment.
This file is used by web servers like Apache with mod_wsgi or Nginx with uWSGI.
"""

import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import your Flask application
from main import app

# This is what the web server will call
application = app

if __name__ == "__main__":
    # For development testing
    app.run(host='0.0.0.0', port=5000, debug=False)