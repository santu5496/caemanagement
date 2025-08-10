# Auto Dealership Management System

## Overview

A Flask-based web application for managing and displaying vehicle inventory. The system provides a customer-facing catalog for browsing vehicles and an admin interface for managing listings. Built as an MVP with in-memory storage, the application handles vehicle listings with image uploads, search/filter functionality, and basic admin authentication.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Bootstrap 5 dark theme for responsive UI
- **Static Assets**: Custom CSS for vehicle image handling and hover effects, JavaScript for form enhancements and image galleries
- **User Interface**: Dual interface design - customer catalog view and single-page admin dashboard with modal-based CRUD
- **Responsive Design**: Mobile-optimized layout with adaptive image sizing and touch-friendly controls
- **Interactive Features**: AJAX-powered single-page CRUD operations with real-time updates and loading states

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
- **Current Implementation**: In-memory storage using Python dictionaries and Vehicle class instances
- **Data Persistence**: No persistent storage (data lost on restart) - designed for MVP/demonstration
- **Data Structure**: Vehicle model with comprehensive attributes including pricing, specifications, contact info, and image references
- **Admin Users**: Hardcoded admin credentials stored in memory with password hashing

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