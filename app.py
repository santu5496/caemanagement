import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_wtf.csrf import CSRFProtect

# Setup logging
log_level = logging.INFO if os.environ.get('FLASK_ENV') == 'production' else logging.DEBUG
logging.basicConfig(level=log_level)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "replit-automarket-secret-key-2025")
app.config['WTF_CSRF_ENABLED'] = False

# Initialize CSRF protection  
# csrf = CSRFProtect(app)

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1) # needed for url_for to generate with https

# configure the database, relative to the app instance folder
database_url = os.environ.get("DATABASE_URL")
if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///automarket.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure upload settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401

    db.create_all()

# Import routes after app creation
from routes import *