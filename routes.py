import os
import uuid
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from app import app, db
from models import Vehicle, AdminUser, add_vehicle, get_all_vehicles, get_vehicle, delete_vehicle, verify_admin, get_available_vehicles, get_vehicles_by_category, initialize_sample_data
from forms import VehicleForm, LoginForm

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def save_uploaded_files(files):
    """Save uploaded files and return list of filenames (max 6 images)"""
    filenames = []
    # Limit to maximum 6 images
    limited_files = files[:6] if files else []

    for file in limited_files:
        if file and file.filename and allowed_file(file.filename):
            # Generate unique filename
            filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            filenames.append(filename)
    return filenames

@app.route('/')
def index():
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

    categories = ['Cars', 'Trucks', 'Commercial Vehicles']
    return render_template('index.html', vehicles=vehicles, categories=categories, 
                         current_category=category, search=search)

@app.route('/vehicle/<vehicle_id>')
def vehicle_detail(vehicle_id):
    """Vehicle detail page"""
    vehicle = get_vehicle(vehicle_id)
    if not vehicle:
        flash('Vehicle not found', 'error')
        return redirect(url_for('index'))
    return render_template('vehicle_detail.html', vehicle=vehicle)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Simple admin login"""
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        if username == "Friendscars" and password == "Friendscars@54961828":
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Wrong username or password!', 'error')
    
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
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    """Professional admin dashboard with enhanced features"""
    # Check authentication
    if not session.get('admin_logged_in'):
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))

    try:
        vehicles = get_all_vehicles()
        form = VehicleForm()
        return render_template('enhanced_admin.html', vehicles=vehicles, form=form)
    except Exception as e:
        app.logger.error(f"Error loading admin dashboard: {e}")
        flash('Error loading dashboard. Please try again.', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard_direct():
    """Direct admin dashboard access for testing"""
    # For demo purposes, bypass session check temporarily
    vehicles = get_all_vehicles()
    form = VehicleForm()
    return render_template('enhanced_admin.html', vehicles=vehicles, form=form)

@app.route('/admin-dark')
def admin_dark_dashboard():
    """Dark theme admin dashboard - direct access"""
    # Set session for demo
    session['admin_logged_in'] = True
    session['admin_username'] = 'Friendscars'
    vehicles = get_all_vehicles()
    form = VehicleForm()
    return render_template('enhanced_admin.html', vehicles=vehicles, form=form)

@app.route('/admin/auth', methods=['POST'])
def admin_auth():
    """Simple authentication endpoint without CSRF for testing"""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    app.logger.debug(f"Auth attempt: {username}")
    
    if username == 'Friendscars' and password == 'Friendscars@54961828':
        session['admin_logged_in'] = True
        session['admin_username'] = username
        session.permanent = True
        flash('✅ Successfully logged in! Welcome to Admin Dashboard.', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('❌ Invalid username or password. Please use: Friendscars / Friendscars@54961828', 'error')
        return redirect(url_for('admin_login'))

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
    # Temporarily disable authentication for testing
    # if not session.get('admin_logged_in'):
    #     return jsonify({'success': False, 'message': 'Authentication required'}), 401

    form = VehicleForm()
    app.logger.debug(f"Raw form data: {dict(request.form)}")
    app.logger.debug(f"Form files: {list(request.files.keys())}")
    app.logger.debug(f"Form validation passed: {form.validate_on_submit()}")
    app.logger.debug(f"Form errors: {form.errors}")

    if form.validate_on_submit():
        try:
            # Save uploaded images
            image_filenames = save_uploaded_files(form.images.data)

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

@app.route('/admin/edit_vehicle/<vehicle_id>', methods=['GET', 'POST'])
def edit_vehicle(vehicle_id):
    """Edit existing vehicle via AJAX or form"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    vehicle = get_vehicle(vehicle_id)
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
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401

    vehicle = get_vehicle(vehicle_id)
    if not vehicle:
        return jsonify({'success': False, 'message': 'Vehicle not found'}), 404

    return jsonify(vehicle.to_dict())

@app.route('/admin/delete_vehicle/<vehicle_id>', methods=['POST', 'DELETE'])
def delete_vehicle_route(vehicle_id):
    """Delete vehicle via AJAX"""
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401

    if delete_vehicle(vehicle_id):
        return jsonify({'success': True, 'message': 'Vehicle deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Vehicle not found'}), 404

@app.route('/admin/toggle_status/<vehicle_id>', methods=['POST'])
def toggle_vehicle_status(vehicle_id):
    """Toggle vehicle status between available and sold via AJAX"""
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401

    vehicle = get_vehicle(vehicle_id)
    if vehicle:
        new_status = 'sold' if vehicle.status == 'available' else 'available'
        vehicle.update_from_dict(status=new_status)
        db.session.commit()
        return jsonify({'success': True, 'message': f'Vehicle marked as {new_status}', 'new_status': new_status})
    else:
        return jsonify({'success': False, 'message': 'Vehicle not found'}), 404

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(error):
    return redirect(url_for('index'))