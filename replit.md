# AutoMarket - OLX-Style Vehicle Marketplace

## Overview

A Flask-based automotive marketplace web application similar to OLX, designed for browsing vehicles. The platform features a modern, mobile-first design with an intuitive customer catalog for viewing vehicles and an admin-only dashboard for managing listings. Regular users can only browse and view vehicles, while administrators have exclusive access to add, edit, and manage vehicle listings with photos. Built with SQLite database persistence, the application provides comprehensive vehicle browsing with search/filter functionality and admin authentication.

## Recent Changes

**Step-by-Step Wizard Complete (August 11, 2025)**: Successfully implemented a comprehensive 6-step vehicle entry wizard with proper form validation, error handling, and notification system. Fixed all save button functionality and authentication issues for smooth vehicle creation workflow.

**Admin Access Security (August 14, 2025)**: Removed admin login button from customer interface to prevent accidental access. Created admin URLs: `/secret-admin-access-2025` and `/staff` with public access to login form but protected dashboard access. Customers see clean marketplace without admin login visibility while administrators can access login form via direct URLs and authenticate to reach dashboard.

**Edit Functionality Verified (August 14, 2025)**: Comprehensive testing confirms all edit functionality working perfectly. Vehicle data fetching, form population, edit submission, and data persistence all verified through automated testing. JavaScript console errors eliminated with enhanced async/await error handling. Admin authentication, session management, and complete CRUD operations fully operational.

**CRUD Operations Fully Functional (August 17, 2025)**: Successfully resolved all CRUD functionality issues. Add, edit, and delete operations now work perfectly in the original wizard interface. Enhanced the system with JavaScript data management and REST API endpoints while maintaining the familiar visual layout. All vehicle management operations are fully operational with proper data persistence and form validation.

**JavaScript Backend Integration (August 17, 2025)**: Enhanced the existing wizard admin interface with pure JavaScript data management while maintaining the original visual layout. Added REST API endpoints for vehicle operations, enabling future single-page functionality without changing the familiar interface. The original wizard admin remains the default, with an alternative SPA version available at `/admin/spa` for future use.

**Landing Page Update (August 17, 2025)**: Changed the landing page from marketplace to admin login page. Now accessing the root URL (/) redirects directly to the admin login form. The marketplace is still accessible at `/marketplace` route for future reference. Admin logout also redirects to the login page for better user flow.

**Console Error Fixes (August 17, 2025)**: Fixed JavaScript console errors in edit functionality, added missing "Very Good" option to condition rating dropdown, resolved syntax errors in HTML template, and improved error handling in vehicle data fetching. Edit functionality now works perfectly with proper form population and validation.

**Database Enhancement (August 17, 2025)**: Added vehicle number and previous owner mobile number columns to enhance vehicle tracking capabilities. Updated admin dashboard table to display both new fields, with proper form validation and CRUD operations. Enhanced image upload system with clear hero image designation - first image slot serves as hero image displayed in admin table and marketplace browse views.

**Migration Complete (August 17, 2025)**: Successfully migrated from Replit Agent to standard Replit environment with enhanced security featuring CSRF protection, gunicorn web server deployment, and comprehensive package installation. All Flask dependencies installed, PostgreSQL database configured and working properly with 19 vehicles migrated, application running smoothly on port 5000. Vehicle creation, admin authentication, edit functionality, and all core features fully operational. Database connection issues resolved and type errors in image handling fixed for robust edit functionality.

**UI Optimization (August 12, 2025)**: Significantly reduced category button spacing for better mobile experience, compressed hero section layout, improved responsive design for smaller screens, and optimized overall page layout for faster loading and better space utilization.

**Mobile Enhancement (August 12, 2025)**: Major mobile optimization with ultra-compact layout for small screens, reduced category button heights to 35px on mobile, removed icons from category buttons, compressed hero section padding, hidden vehicle specs on very small screens for cleaner layout, and optimized all spacing for maximum content visibility on mobile devices.

**Localization Update (August 12, 2025)**: Updated application for Indian market with currency changed from USD ($) to Indian Rupee (₹), adjusted sample vehicle prices to realistic Indian market values (Honda Civic: ₹15,50,000, Ford F-150: ₹27,50,000, Toyota Camry: ₹20,80,000), updated admin credentials to "abc" with password "123", and changed all sample vehicle contact names to "Friendscars".

**Credentials Update (August 13, 2025)**: Updated admin login credentials to simple format - Username: "abc", Password: "123" for easier access.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Bootstrap 5 light theme for modern marketplace UI
- **Design System**: OLX-inspired design with gradient hero sections, card-based listings, and floating action buttons
- **Static Assets**: Custom CSS for marketplace styling, listing cards, favorite buttons, and mobile enhancements
- **User Interface**: Dual interface - modern customer marketplace and single-page seller dashboard with modal-based CRUD
- **Responsive Design**: Mobile-first design with touch-optimized controls, floating filter button, and adaptive layouts
- **Interactive Features**: AJAX-powered CRUD operations, favorite toggles, breadcrumb navigation, smooth animations, and tabbed comprehensive vehicle detail forms

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
- **Current Implementation**: PostgreSQL database with Flask-SQLAlchemy ORM for robust production persistence
- **Data Persistence**: Full database persistence with proper schema and relationships
- **Data Structure**: SQLAlchemy models with comprehensive vehicle details including:
  - Basic info (pricing, specifications, contact info, images)
  - Engine & Performance (fuel type, transmission, horsepower, drivetrain)
  - Ownership & History (number of owners, previous owner contact, odometer, accident history, service records)
  - Insurance & Documentation (insurance company, policy number, VIN, registration)
  - Features & Condition (colors, features list, condition rating, warranty info)
- **Admin Users**: Database-stored admin credentials with secure password hashing
- **Database Migration**: Enhanced with comprehensive vehicle detail fields for professional dealership management

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

## Testing Infrastructure

### Automated Testing Suite
- **Comprehensive Test Coverage**: Complete automation testing for vehicle management workflow
- **Multiple Testing Approaches**: Backend functional testing, UI automation with Selenium, and simple connectivity tests
- **Test Scripts**: 
  - `test_automation.py` - Full Selenium WebDriver UI testing
  - `test_vehicle_creation.py` - Functional backend testing with form validation
  - `run_tests.py` - Simple connectivity and route testing
  - `test_runner.sh` - Automated test suite runner with environment setup
- **Test Documentation**: 
  - `manual_test_checklist.md` - Comprehensive manual testing procedures
  - `README_TESTING.md` - Complete testing documentation and setup guide
- **Test Reporting**: Automated JSON reports with timestamps, test results, and detailed logs
- **Quality Assurance**: Form validation testing, data persistence verification, and UI element visibility testing

### Testing Capabilities
- **End-to-End Testing**: Complete vehicle creation workflow from form opening to data persistence
- **Validation Testing**: Required field validation, data type checking, and business rule enforcement
- **UI Testing**: Wizard navigation, form visibility, responsive design verification
- **Authentication Testing**: Admin login, session management, and access control verification
- **Performance Testing**: Response time measurement and load handling verification