# AutoMarket - OLX-Style Vehicle Marketplace

## Overview

A Flask-based automotive marketplace web application similar to OLX, designed for browsing vehicles. The platform features a modern, mobile-first design with an intuitive customer catalog for viewing vehicles and an admin-only dashboard for managing listings. Regular users can only browse and view vehicles, while administrators have exclusive access to add, edit, and manage vehicle listings with photos. Built as an MVP with in-memory storage, the application provides comprehensive vehicle browsing with search/filter functionality and admin authentication.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Bootstrap 5 light theme for modern marketplace UI
- **Design System**: OLX-inspired design with gradient hero sections, card-based listings, and floating action buttons
- **Static Assets**: Custom CSS for marketplace styling, listing cards, favorite buttons, and mobile enhancements
- **User Interface**: Dual interface - modern customer marketplace and single-page seller dashboard with modal-based CRUD
- **Responsive Design**: Mobile-first design with touch-optimized controls, floating filter button, and adaptive layouts
- **Interactive Features**: AJAX-powered CRUD operations, favorite toggles, breadcrumb navigation, and smooth animations

### Backend Architecture
- **Framework**: Flask web framework with modular route organization
- **Form Handling**: Flask-WTF for form validation and file uploads with CSRF protection
- **File Management**: Werkzeug for secure file uploads with UUID-based naming to prevent conflicts
- **Session Management**: Flask sessions for admin authentication state
- **Data Layer**: In-memory storage using Python dictionaries and classes (MVP approach)
- **API Design**: RESTful AJAX endpoints for single-page CRUD operations with JSON responses

### Authentication & Authorization
- **Admin Authentication**: Simple username/password authentication with password hashing using Werkzeug
- **Session Management**: Flask sessions to maintain admin login state
- **Access Control**: Route-level protection for admin-only functionality
- **Security**: CSRF protection on all forms, secure filename handling for uploads

### Data Storage Solution
- **Current Implementation**: PostgreSQL database with Flask-SQLAlchemy ORM for production-ready persistence
- **Data Persistence**: Full database persistence with proper schema and relationships
- **Data Structure**: SQLAlchemy models with comprehensive attributes including pricing, specifications, contact info, and image references
- **Admin Users**: Database-stored admin credentials with secure password hashing
- **Database Migration**: Migrated from in-memory storage to PostgreSQL for Replit compatibility and data safety

### File Upload System
- **Image Storage**: Local file system in static/uploads directory
- **File Validation**: Restricted to image formats (PNG, JPG, JPEG, GIF)
- **File Naming**: UUID prefix to prevent naming conflicts and enhance security
- **Size Limits**: 16MB maximum file size per upload
- **Multiple Images**: Support for multiple images per vehicle listing

### Search & Filter Functionality
- **Category Filtering**: Filter vehicles by type (Cars, Trucks, Commercial Vehicles)
- **Text Search**: Search across vehicle title, make, and model fields
- **Status Filtering**: Automatic filtering to show only available vehicles on public catalog
- **Real-time Updates**: JavaScript-enhanced forms with auto-submit on category changes

## External Dependencies

### Frontend Libraries
- **Bootstrap 5**: CSS framework with dark theme variant from Replit CDN
- **Font Awesome 6**: Icon library for UI enhancement
- **Bootstrap JavaScript**: For interactive components (carousels, modals, tooltips)

### Python Packages
- **Flask**: Core web framework
- **Flask-WTF**: Form handling and validation with CSRF protection
- **WTForms**: Form field definitions and validators
- **Werkzeug**: WSGI utilities, security functions, and file handling

### Infrastructure
- **ProxyFix Middleware**: Handles reverse proxy headers for proper URL generation
- **File System**: Local storage for uploaded images
- **Environment Variables**: SESSION_SECRET for secure session management

### Development Tools
- **Logging**: Python logging module configured for debug level
- **Debug Mode**: Flask debug mode enabled for development environment
- **Hot Reload**: Development server with automatic reloading on code changes