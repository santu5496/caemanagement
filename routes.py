import os
import uuid
from flask import render_template, request, redirect, url_for, flash, session, jsonify, render_template_string
from werkzeug.utils import secure_filename

from app import app, db
from models import Vehicle, AdminUser, add_vehicle, get_all_vehicles, get_vehicle, delete_vehicle, verify_admin, get_available_vehicles, get_vehicles_by_category, initialize_sample_data
from forms import VehicleForm, LoginForm

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def save_uploaded_files(files):
    """Save uploaded files and return list of filenames (max 6 images)"""
    filenames = []
    if not files:
        app.logger.info("No files provided to save_uploaded_files")
        return filenames
    
    # Ensure files is a list
    if not isinstance(files, list):
        files = [files] if files else []
    
    # Filter out None/empty files and limit to maximum 6 images
    valid_files = [f for f in files if f and hasattr(f, 'filename') and f.filename.strip()]
    limited_files = valid_files[:6]
    
    app.logger.info(f"Processing {len(limited_files)} valid files out of {len(files)} total files")

    for file in limited_files:
        if file and hasattr(file, 'filename') and file.filename and allowed_file(file.filename):
            try:
                # Generate unique filename
                original_filename = secure_filename(file.filename)
                filename = str(uuid.uuid4()) + '_' + original_filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Ensure upload directory exists
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                
                # Save the file
                file.save(filepath)
                filenames.append(filename)
                app.logger.info(f"Successfully saved file: {filename}")
                
            except Exception as e:
                app.logger.error(f"Error saving file {file.filename}: {e}")
                continue
        else:
            if file:
                app.logger.warning(f"File rejected - invalid filename or type: {getattr(file, 'filename', 'unknown')}")
    
    app.logger.info(f"Total files saved: {len(filenames)}")
    return filenames

@app.route('/')
def index():
    """Landing page redirects to admin login"""
    return redirect(url_for('admin_login'))

@app.route('/marketplace')
def marketplace():
    """Customer-facing catalog page"""
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')

    # Get available vehicles
    if category == 'all':
        vehicles = get_available_vehicles()
    else:
        vehicles = [v for v in get_available_vehicles() if v.category == category]

    # Simple search filter
    if search:
        vehicles = [v for v in vehicles if 
                   search.lower() in v.title.lower() or 
                   search.lower() in v.make.lower() or 
                   search.lower() in v.model.lower()]

    # Debug: Log vehicle images for troubleshooting
    for vehicle in vehicles:
        if not vehicle.images_list or len(vehicle.images_list) == 0:
            app.logger.warning(f"Vehicle \"{vehicle.title}\" has no images: {vehicle.images_list}")
        else:
            app.logger.info(f"Vehicle \"{vehicle.title}\" has images: {vehicle.images_list}")

    categories = ['Cars', 'Trucks', 'Commercial Vehicles']
    return render_template('index.html', vehicles=vehicles, categories=categories, 
                         current_category=category, search=search)

@app.route('/vehicle/<vehicle_id>')
def vehicle_detail(vehicle_id):
    """Vehicle detail page"""
    vehicle = get_vehicle(vehicle_id)
    if not vehicle:
        flash('Vehicle not found', 'error')
        return redirect(url_for('marketplace'))
    return render_template('vehicle_detail.html', vehicle=vehicle)

@app.route('/secret-admin-access-2025', methods=['GET', 'POST'])
def admin_login():
    """Admin login portal - always shows login form"""
    # First check if already logged in
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if username == "abc" and password == "123":
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Wrong username or password!', 'error')

    # Always show the login form
    return render_template('admin_login.html')

@app.route('/quick-login')
def quick_login():
    """Quick login test page"""
    from flask import render_template_string
    with open('direct_login_test.html', 'r') as f:
        return render_template_string(f.read())

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
def admin_dashboard():
    """Admin Dashboard with single-page JavaScript interface"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    return render_template('admin_single_page.html')

@app.route('/admin/wizard')
def admin_wizard():
    """Admin Dashboard with original wizard interface (legacy)"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    try:
        vehicles = get_all_vehicles()
        form = VehicleForm()
        return render_template('wizard_admin.html', vehicles=vehicles, form=form)
    except Exception as e:
        app.logger.error(f"Error loading admin dashboard: {e}")
        flash('Error loading dashboard. Please try again.', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/api/vehicles')
def admin_api_vehicles():
    """API endpoint to get all vehicles as JSON"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        vehicles = get_all_vehicles()
        vehicles_data = []
        
        for vehicle in vehicles:
            vehicle_dict = {
                'id': vehicle.id,
                'title': vehicle.title,
                'category': vehicle.category,
                'make': vehicle.make,
                'model': vehicle.model,
                'year': vehicle.year,
                'price': float(vehicle.price),
                'mileage': vehicle.mileage,
                'description': vehicle.description,
                'contact_name': vehicle.contact_name,
                'contact_phone': vehicle.contact_phone,
                'contact_email': vehicle.contact_email,
                'vehicle_number': vehicle.vehicle_number,
                'status': vehicle.status,
                'fuel_type': vehicle.fuel_type,
                'transmission': vehicle.transmission,
                'engine_size': vehicle.engine_size,
                'horsepower': vehicle.horsepower,
                'fuel_economy': vehicle.fuel_economy,
                'drivetrain': vehicle.drivetrain,
                'number_of_owners': vehicle.number_of_owners,
                'previous_owner_name': vehicle.previous_owner_name,
                'previous_owner_phone': vehicle.previous_owner_phone,
                'previous_owner_email': vehicle.previous_owner_email,
                'odometer_reading': vehicle.odometer_reading,
                'accident_history': vehicle.accident_history,
                'service_records': vehicle.service_records,
                'insurance_company': vehicle.insurance_company,
                'insurance_policy_number': vehicle.insurance_policy_number,
                'insurance_expiry': vehicle.insurance_expiry,
                'registration_number': vehicle.registration_number,
                'vin_number': vehicle.vin_number,
                'exterior_color': vehicle.exterior_color,
                'interior_color': vehicle.interior_color,
                'features': vehicle.features,
                'condition_rating': vehicle.condition_rating,
                'warranty_info': vehicle.warranty_info,
                'images': vehicle.images_list,
                'created_at': vehicle.created_at.isoformat() if vehicle.created_at else None,
                'updated_at': vehicle.updated_at.isoformat() if vehicle.updated_at else None
            }
            vehicles_data.append(vehicle_dict)
        
        return jsonify({
            'success': True,
            'vehicles': vehicles_data,
            'total': len(vehicles_data)
        })
    except Exception as e:
        app.logger.error(f"Error fetching vehicles API: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch vehicles'}), 500

@app.route('/admin/spa')
def admin_dashboard_spa():
    """Single Page Admin Dashboard (Alternative)"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    return render_template('admin_spa.html')

@app.route('/admin/old')
def admin_dashboard_old():
    """Professional admin dashboard with enhanced features"""
    # Check authentication
    if not session.get('admin_logged_in'):
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))

    try:
        vehicles = get_all_vehicles()
        form = VehicleForm()
        return render_template('wizard_admin.html', vehicles=vehicles, form=form)
    except Exception as e:
        app.logger.error(f"Error loading admin dashboard: {e}")
        flash('Error loading dashboard. Please try again.', 'error')
        return redirect(url_for('admin_login'))



@app.route('/admin/auth', methods=['POST'])
def admin_auth():
    """Simple authentication endpoint without CSRF for testing"""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    app.logger.debug(f"Auth attempt: {username}")

    if username == 'abc' and password == '123':
        session['admin_logged_in'] = True
        session['admin_username'] = username
        session.permanent = True
        flash('✅ Successfully logged in! Welcome to Admin Dashboard.', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('❌ Invalid username or password. Please use: abc / 123', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login_legacy():
    """Legacy admin login redirect - redirects to new secret URL"""
    return redirect('/secret-admin-access-2025')

# Direct admin access route for easy URL sharing
@app.route('/staff', methods=['GET', 'POST'])
def admin_staff():
    """Easy admin access route - /staff"""
    return redirect('/secret-admin-access-2025')

@app.route('/admin/add_vehicle_page')
def add_vehicle_page():
    """Display add vehicle form page"""
    if not session.get('admin_logged_in'):
        flash('Please log in to access the admin area.', 'error')
        return redirect(url_for('admin_login'))

    form = VehicleForm()
    return render_template('add_vehicle.html', form=form)

@app.route('/admin/add_vehicle', methods=['POST'])
def add_vehicle_route():
    """Add new vehicle via AJAX"""
    # Check authentication
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    form = VehicleForm()
    app.logger.debug(f"Raw form data: {dict(request.form)}")
    app.logger.debug(f"Form files: {list(request.files.keys())}")
    app.logger.debug(f"Form validation passed: {form.validate_on_submit()}")
    app.logger.debug(f"Form errors: {form.errors}")

    if form.validate_on_submit():
        try:
            # Save uploaded images - handle both single file and multiple files
            uploaded_files = form.images.data
            if not isinstance(uploaded_files, list):
                uploaded_files = [uploaded_files] if uploaded_files else []
            
            # Filter out empty files
            valid_files = [f for f in uploaded_files if f and hasattr(f, 'filename') and f.filename]
            
            image_filenames = save_uploaded_files(valid_files)
            app.logger.info(f"Saved {len(image_filenames)} images: {image_filenames}")

            # Create vehicle with comprehensive data
            vehicle = Vehicle(
                title=form.title.data,
                category=form.category.data,
                make=form.make.data,
                model=form.model.data,
                year=form.year.data,
                price=form.price.data,
                mileage=form.mileage.data,
                description=form.description.data,
                contact_name=form.contact_name.data,
                contact_phone=form.contact_phone.data,
                contact_email=form.contact_email.data or None,
                vehicle_number=form.vehicle_number.data or None,
                images=image_filenames,
                # Engine & Performance
                fuel_type=form.fuel_type.data or None,
                transmission=form.transmission.data or None,
                engine_size=form.engine_size.data or None,
                horsepower=form.horsepower.data or None,
                fuel_economy=form.fuel_economy.data or None,
                drivetrain=form.drivetrain.data or None,
                # Ownership & History
                number_of_owners=form.number_of_owners.data or None,
                previous_owner_name=form.previous_owner_name.data or None,
                previous_owner_phone=form.previous_owner_phone.data or None,
                previous_owner_email=form.previous_owner_email.data or None,
                odometer_reading=form.odometer_reading.data or None,
                accident_history=form.accident_history.data or None,
                service_records=form.service_records.data or None,
                # Insurance & Documentation
                insurance_company=form.insurance_company.data or None,
                insurance_policy_number=form.insurance_policy_number.data or None,
                insurance_expiry=form.insurance_expiry.data or None,
                registration_number=form.registration_number.data or None,
                vin_number=form.vin_number.data or None,
                # Features & Condition
                exterior_color=form.exterior_color.data or None,
                interior_color=form.interior_color.data or None,
                features=form.features.data or None,
                condition_rating=form.condition_rating.data or None,
                warranty_info=form.warranty_info.data or None
            )

            db.session.add(vehicle)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Vehicle added successfully', 'vehicle': vehicle.to_dict()})

        except Exception as e:
            app.logger.error(f"Error adding vehicle: {str(e)}")
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Error adding vehicle: {str(e)}'}), 500

    # Return validation errors
    errors = {}
    for field, error_list in form.errors.items():
        if isinstance(error_list, list) and error_list:
            errors[field] = error_list[0]
        else:
            errors[field] = 'Validation error'

    app.logger.debug(f"Validation errors: {errors}")
    return jsonify({'success': False, 'message': 'Please check all required fields', 'errors': errors}), 400

@app.route('/admin/vehicle/<vehicle_id>', methods=['GET'])
def get_vehicle_for_edit(vehicle_id):
    """Get vehicle data for editing in modal"""
    app.logger.debug(f"Session data: {dict(session)}")
    app.logger.debug(f"Admin logged in: {session.get('admin_logged_in')}")

    if not session.get('admin_logged_in'):
        app.logger.warning(f"Unauthorized access attempt to get vehicle {vehicle_id}")
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    try:
        # Close any existing connections and get fresh session
        db.session.close()
        
        # Use fresh query with proper session handling
        with db.session.begin():
            vehicle = db.session.get(Vehicle, vehicle_id)
            
            if not vehicle:
                app.logger.warning(f"Vehicle not found: {vehicle_id}")
                return jsonify({'success': False, 'message': 'Vehicle not found'}), 404

            # Convert vehicle data to format expected by form
            vehicle_data = vehicle.to_dict()
            
        # Ensure all fields have proper values for form binding
        form_data = {
            'id': vehicle_data.get('id', ''),
            'title': vehicle_data.get('title', ''),
            'category': vehicle_data.get('category', ''),
            'make': vehicle_data.get('make', ''),
            'model': vehicle_data.get('model', ''),
            'year': vehicle_data.get('year', ''),
            'price': vehicle_data.get('price', ''),
            'mileage': vehicle_data.get('mileage', ''),
            'description': vehicle_data.get('description', ''),
            'contact_name': vehicle_data.get('contact_name', ''),
            'contact_phone': vehicle_data.get('contact_phone', ''),
            'contact_email': vehicle_data.get('contact_email', ''),
            'vehicle_number': vehicle_data.get('vehicle_number', ''),
            'status': vehicle_data.get('status', 'available'),
            'fuel_type': vehicle_data.get('fuel_type', ''),
            'transmission': vehicle_data.get('transmission', ''),
            'engine_size': vehicle_data.get('engine_size', ''),
            'horsepower': vehicle_data.get('horsepower', ''),
            'fuel_economy': vehicle_data.get('fuel_economy', ''),
            'drivetrain': vehicle_data.get('drivetrain', ''),
            'number_of_owners': vehicle_data.get('number_of_owners', ''),
            'previous_owner_name': vehicle_data.get('previous_owner_name', ''),
            'previous_owner_phone': vehicle_data.get('previous_owner_phone', ''),
            'previous_owner_email': vehicle_data.get('previous_owner_email', ''),
            'odometer_reading': vehicle_data.get('odometer_reading', ''),
            'accident_history': vehicle_data.get('accident_history', ''),
            'service_records': vehicle_data.get('service_records', ''),
            'insurance_company': vehicle_data.get('insurance_company', ''),
            'insurance_policy_number': vehicle_data.get('insurance_policy_number', ''),
            'insurance_expiry': vehicle_data.get('insurance_expiry', ''),
            'registration_number': vehicle_data.get('registration_number', ''),
            'vin_number': vehicle_data.get('vin_number', ''),
            'exterior_color': vehicle_data.get('exterior_color', ''),
            'interior_color': vehicle_data.get('interior_color', ''),
            'features': vehicle_data.get('features', ''),
            'condition_rating': vehicle_data.get('condition_rating', ''),
            'warranty_info': vehicle_data.get('warranty_info', ''),
            'images': vehicle_data.get('images', [])
        }

        app.logger.debug(f"Returning vehicle data for {vehicle_id}: {form_data}")
        return jsonify({'success': True, 'vehicle': form_data})

    except Exception as e:
        app.logger.error(f"Database error when fetching vehicle {vehicle_id}: {str(e)}")
        # Try to refresh the database connection
        try:
            db.session.rollback()
            db.session.close()
        except:
            pass
        
        # Try alternative query method as fallback
        try:
            vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
            if vehicle:
                return jsonify({'success': True, 'vehicle': vehicle.to_dict()})
        except:
            pass
            
        return jsonify({'success': False, 'message': 'Database connection error. Please refresh the page and try again.'}), 500

@app.route('/admin/edit_vehicle/<vehicle_id>', methods=['GET', 'POST'])
def edit_vehicle(vehicle_id):
    """Edit existing vehicle via AJAX or form"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({'success': False, 'message': 'Vehicle not found'}), 404

    if request.method == 'GET':
        # For edit vehicle page
        form = VehicleForm(obj=vehicle)
        return render_template('edit_vehicle.html', form=form, vehicle=vehicle)

    # POST request for AJAX updates
    form = VehicleForm()

    if form.validate_on_submit():
        try:
            # Handle new image uploads
            new_images = save_uploaded_files(form.images.data)

            # Update vehicle with comprehensive data
            update_data = {
                'title': form.title.data,
                'category': form.category.data,
                'make': form.make.data,
                'model': form.model.data,
                'year': form.year.data,
                'price': form.price.data,
                'mileage': form.mileage.data,
                'description': form.description.data,
                'contact_name': form.contact_name.data,
                'contact_phone': form.contact_phone.data,
                'contact_email': form.contact_email.data or None,
                'vehicle_number': form.vehicle_number.data or None,
                'status': form.status.data,
                # Engine & Performance
                'fuel_type': form.fuel_type.data or None,
                'transmission': form.transmission.data or None,
                'engine_size': form.engine_size.data or None,
                'horsepower': form.horsepower.data or None,
                'fuel_economy': form.fuel_economy.data or None,
                'drivetrain': form.drivetrain.data or None,
                # Ownership & History
                'number_of_owners': form.number_of_owners.data or None,
                'previous_owner_name': form.previous_owner_name.data or None,
                'previous_owner_phone': form.previous_owner_phone.data or None,
                'previous_owner_email': form.previous_owner_email.data or None,
                'odometer_reading': form.odometer_reading.data or None,
                'accident_history': form.accident_history.data or None,
                'service_records': form.service_records.data or None,
                # Insurance & Documentation
                'insurance_company': form.insurance_company.data or None,
                'insurance_policy_number': form.insurance_policy_number.data or None,
                'insurance_expiry': form.insurance_expiry.data or None,
                'registration_number': form.registration_number.data or None,
                'vin_number': form.vin_number.data or None,
                # Features & Condition
                'exterior_color': form.exterior_color.data or None,
                'interior_color': form.interior_color.data or None,
                'features': form.features.data or None,
                'condition_rating': form.condition_rating.data or None,
                'warranty_info': form.warranty_info.data or None
            }

            # Add new images to existing ones
            if new_images:
                update_data['images'] = vehicle.images_list + new_images

            vehicle.update_from_dict(**update_data)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Vehicle updated successfully', 'vehicle': vehicle.to_dict()})

        except Exception as e:
            return jsonify({'success': False, 'message': f'Error updating vehicle: {str(e)}'}), 500

    # Return validation errors
    errors = {}
    for field, error_list in form.errors.items():
        if isinstance(error_list, list) and error_list:
            errors[field] = str(error_list[0])
        else:
            errors[field] = 'Validation error'
    return jsonify({'success': False, 'message': 'Validation failed', 'errors': errors}), 400

@app.route('/admin/vehicle/<vehicle_id>')
def get_vehicle_data(vehicle_id):
    """Get vehicle data for editing"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return jsonify({'success': False, 'message': 'Vehicle not found'}), 404

        return jsonify({'success': True, 'vehicle': vehicle.to_dict()})
    except Exception as e:
        app.logger.error(f"Error fetching vehicle {vehicle_id}: {str(e)}")
        return jsonify({'success': False, 'message': 'Database error'}), 500

@app.route('/admin/delete_vehicle/<vehicle_id>', methods=['POST', 'DELETE'])
def delete_vehicle_route(vehicle_id):
    """Delete vehicle via AJAX"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return jsonify({'success': False, 'message': 'Vehicle not found'}), 404
        
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Vehicle deleted successfully'})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting vehicle {vehicle_id}: {str(e)}")
        return jsonify({'success': False, 'message': 'Error deleting vehicle'}), 500

@app.route('/admin/toggle_status/<vehicle_id>', methods=['POST'])
def toggle_vehicle_status(vehicle_id):
    """Toggle vehicle status between available and sold via AJAX"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return jsonify({'success': False, 'message': 'Vehicle not found'}), 404
        
        new_status = 'sold' if vehicle.status == 'available' else 'available'
        vehicle.update_from_dict(status=new_status)
        db.session.commit()
        return jsonify({'success': True, 'message': f'Vehicle marked as {new_status}', 'new_status': new_status})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error toggling vehicle status {vehicle_id}: {str(e)}")
        return jsonify({'success': False, 'message': 'Error updating vehicle status'}), 500

# Single-page CRUD API endpoints for JavaScript frontend
@app.route('/admin/api/vehicles', methods=['POST'])
def admin_api_create_vehicle():
    """API endpoint to create a new vehicle"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        form_data = request.form.to_dict()
        
        # Handle file uploads
        files = request.files.getlist('images[]') if 'images[]' in request.files else []
        existing_images = request.form.getlist('existing_images')
        
        # Save uploaded files
        new_images = save_uploaded_files(files)
        all_images = existing_images + new_images
        
        # Create vehicle data
        vehicle_data = {
            'title': form_data.get('title', ''),
            'category': form_data.get('category', ''),
            'make': form_data.get('make', ''),
            'model': form_data.get('model', ''),
            'year': int(form_data.get('year', 2024)),
            'price': float(form_data.get('price', 0)),
            'mileage': int(form_data.get('mileage', 0)),
            'description': form_data.get('description', ''),
            'contact_name': form_data.get('contact_name', ''),
            'contact_phone': form_data.get('contact_phone', ''),
            'contact_email': form_data.get('contact_email', ''),
            'status': form_data.get('status', 'available'),
            'fuel_type': form_data.get('fuel_type'),
            'vehicle_number': form_data.get('vehicle_number'),
            'previous_owner_phone': form_data.get('previous_owner_phone'),
            'images': all_images
        }
        
        # Create vehicle object
        vehicle = Vehicle(**vehicle_data)
        
        # Add the vehicle to database
        db.session.add(vehicle)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Vehicle added successfully',
            'vehicle': {
                'id': vehicle.id,
                'title': vehicle.title,
                'category': vehicle.category,
                'make': vehicle.make,
                'model': vehicle.model,
                'year': vehicle.year,
                'price': float(vehicle.price),
                'mileage': vehicle.mileage,
                'status': vehicle.status,
                'vehicle_number': vehicle.vehicle_number,
                'previous_owner_phone': vehicle.previous_owner_phone,
                'images': vehicle.images_list
            }
        })
        
    except Exception as e:
        app.logger.error(f"Error creating vehicle: {e}")
        return jsonify({'success': False, 'message': 'Error creating vehicle'}), 500

@app.route('/admin/api/vehicles/<vehicle_id>', methods=['PUT'])
def admin_api_update_vehicle(vehicle_id):
    """API endpoint to update a vehicle"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        vehicle = get_vehicle(vehicle_id)
        if not vehicle:
            return jsonify({'success': False, 'message': 'Vehicle not found'}), 404
        
        form_data = request.form.to_dict()
        
        # Handle file uploads
        files = request.files.getlist('images[]') if 'images[]' in request.files else []
        existing_images = request.form.getlist('existing_images')
        
        # Save uploaded files
        new_images = save_uploaded_files(files)
        all_images = existing_images + new_images
        
        # Update vehicle fields
        update_data = {
            'title': form_data.get('title', vehicle.title),
            'category': form_data.get('category', vehicle.category),
            'make': form_data.get('make', vehicle.make),
            'model': form_data.get('model', vehicle.model),
            'year': int(form_data.get('year', vehicle.year)),
            'price': float(form_data.get('price', vehicle.price)),
            'mileage': int(form_data.get('mileage', vehicle.mileage)),
            'description': form_data.get('description', vehicle.description),
            'contact_name': form_data.get('contact_name', vehicle.contact_name),
            'contact_phone': form_data.get('contact_phone', vehicle.contact_phone),
            'contact_email': form_data.get('contact_email', vehicle.contact_email),
            'status': form_data.get('status', vehicle.status),
            'fuel_type': form_data.get('fuel_type', vehicle.fuel_type),
            'vehicle_number': form_data.get('vehicle_number', vehicle.vehicle_number),
            'previous_owner_phone': form_data.get('previous_owner_phone', vehicle.previous_owner_phone)
        }
        
        if all_images:
            update_data['images'] = all_images
            
        vehicle.update_from_dict(**update_data)
        
        # Save to database
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Vehicle updated successfully',
            'vehicle': {
                'id': vehicle.id,
                'title': vehicle.title,
                'category': vehicle.category,
                'make': vehicle.make,
                'model': vehicle.model,
                'year': vehicle.year,
                'price': float(vehicle.price),
                'mileage': vehicle.mileage,
                'status': vehicle.status,
                'vehicle_number': vehicle.vehicle_number,
                'previous_owner_phone': vehicle.previous_owner_phone,
                'images': vehicle.images_list
            }
        })
        
    except Exception as e:
        app.logger.error(f"Error updating vehicle: {e}")
        return jsonify({'success': False, 'message': 'Error updating vehicle'}), 500

@app.route('/admin/api/vehicles/<vehicle_id>', methods=['DELETE'])
def admin_api_delete_vehicle(vehicle_id):
    """API endpoint to delete a vehicle"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        if delete_vehicle(vehicle_id):
            return jsonify({'success': True, 'message': 'Vehicle deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Vehicle not found'}), 404
            
    except Exception as e:
        app.logger.error(f"Error deleting vehicle: {e}")
        return jsonify({'success': False, 'message': 'Error deleting vehicle'}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(error):
    return redirect(url_for('index'))