import os
import uuid
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from app import app
from models import Vehicle, add_vehicle, get_all_vehicles, get_vehicle, delete_vehicle, verify_admin, get_available_vehicles, get_vehicles_by_category
from forms import VehicleForm, LoginForm

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def save_uploaded_files(files):
    """Save uploaded files and return list of filenames"""
    filenames = []
    for file in files:
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
    """Admin login page"""
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        if verify_admin(form.username.data, form.password.data):
            session['admin_logged_in'] = True
            session['admin_username'] = form.username.data
            flash('Logged in successfully', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin_login.html', form=form)

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard with single-page CRUD"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    vehicles = get_all_vehicles()
    form = VehicleForm()  # Form for modal dialogs
    return render_template('admin.html', vehicles=vehicles, form=form)

@app.route('/admin/add_vehicle', methods=['POST'])
def add_vehicle_route():
    """Add new vehicle via AJAX"""
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    form = VehicleForm()
    if form.validate_on_submit():
        try:
            # Save uploaded images
            image_filenames = save_uploaded_files(form.images.data)
            
            # Create vehicle
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
                images=image_filenames
            )
            
            add_vehicle(vehicle)
            return jsonify({'success': True, 'message': 'Vehicle added successfully', 'vehicle': vehicle.to_dict()})
            
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error adding vehicle: {str(e)}'}), 500
    
    # Return validation errors
    errors = {}
    for field, error_list in form.errors.items():
        errors[field] = error_list[0] if error_list else ''
    return jsonify({'success': False, 'message': 'Validation failed', 'errors': errors}), 400

@app.route('/admin/edit_vehicle/<vehicle_id>', methods=['POST'])
def edit_vehicle(vehicle_id):
    """Edit existing vehicle via AJAX"""
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    vehicle = get_vehicle(vehicle_id)
    if not vehicle:
        return jsonify({'success': False, 'message': 'Vehicle not found'}), 404
    
    form = VehicleForm()
    
    if form.validate_on_submit():
        try:
            # Handle new image uploads
            new_images = save_uploaded_files(form.images.data)
            
            # Update vehicle
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
                'status': form.status.data
            }
            
            # Add new images to existing ones
            if new_images:
                update_data['images'] = vehicle.images + new_images
            
            vehicle.update(**update_data)
            return jsonify({'success': True, 'message': 'Vehicle updated successfully', 'vehicle': vehicle.to_dict()})
            
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error updating vehicle: {str(e)}'}), 500
    
    # Return validation errors
    errors = {}
    for field, error_list in form.errors.items():
        errors[field] = error_list[0] if error_list else ''
    return jsonify({'success': False, 'message': 'Validation failed', 'errors': errors}), 400

@app.route('/admin/get_vehicle/<vehicle_id>')
def get_vehicle_data(vehicle_id):
    """Get vehicle data for editing"""
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    vehicle = get_vehicle(vehicle_id)
    if not vehicle:
        return jsonify({'success': False, 'message': 'Vehicle not found'}), 404
    
    return jsonify({'success': True, 'vehicle': vehicle.to_dict()})

@app.route('/admin/delete_vehicle/<vehicle_id>', methods=['POST'])
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
        vehicle.update(status=new_status)
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
