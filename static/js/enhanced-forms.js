// Enhanced Form Validation and User Experience
class VehicleFormManager {
    constructor() {
        this.form = document.getElementById('vehicleForm');
        this.modal = document.getElementById('vehicleModal');
        this.initializeFormValidation();
        this.initializeRealTimeValidation();
        this.initializeImagePreview();
        this.initializeDependentFields();
    }

    initializeFormValidation() {
        if (!this.form) return;

        this.form.addEventListener('submit', (e) => {
            if (!this.validateForm()) {
                e.preventDefault();
                e.stopPropagation();
                this.showValidationErrors();
            }
            this.form.classList.add('was-validated');
        });
    }

    initializeRealTimeValidation() {
        // Price formatting
        const priceField = document.getElementById('price');
        if (priceField) {
            priceField.addEventListener('input', (e) => {
                let value = e.target.value.replace(/[^\d.]/g, '');
                if (value) {
                    e.target.value = parseFloat(value).toLocaleString('en-IN');
                }
                this.validateField(e.target);
            });
        }

        // Mileage formatting
        const mileageField = document.getElementById('mileage');
        if (mileageField) {
            mileageField.addEventListener('input', (e) => {
                let value = e.target.value.replace(/[^\d]/g, '');
                if (value) {
                    e.target.value = parseInt(value).toLocaleString();
                }
                this.validateField(e.target);
            });
        }

        // Year validation
        const yearField = document.getElementById('year');
        if (yearField) {
            yearField.addEventListener('input', (e) => {
                const currentYear = new Date().getFullYear();
                const value = parseInt(e.target.value);
                if (value < 1990 || value > currentYear + 1) {
                    e.target.setCustomValidity(`Year must be between 1990 and ${currentYear + 1}`);
                } else {
                    e.target.setCustomValidity('');
                }
                this.validateField(e.target);
            });
        }

        // Phone number formatting
        const phoneFields = document.querySelectorAll('input[type="tel"], input[name*="phone"]');
        phoneFields.forEach(field => {
            field.addEventListener('input', (e) => {
                let value = e.target.value.replace(/[^\d]/g, '');
                if (value.length >= 6) {
                    value = value.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
                }
                e.target.value = value;
                this.validateField(e.target);
            });
        });

        // Email validation
        const emailFields = document.querySelectorAll('input[type="email"]');
        emailFields.forEach(field => {
            field.addEventListener('blur', (e) => {
                this.validateEmail(e.target);
            });
        });

        // VIN validation
        const vinField = document.getElementById('vin_number');
        if (vinField) {
            vinField.addEventListener('input', (e) => {
                let value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
                e.target.value = value;
                if (value.length > 0 && value.length !== 17) {
                    e.target.setCustomValidity('VIN must be exactly 17 characters');
                } else {
                    e.target.setCustomValidity('');
                }
                this.validateField(e.target);
            });
        }
    }

    initializeImagePreview() {
        const imageInput = document.getElementById('images');
        if (!imageInput) return;

        imageInput.addEventListener('change', (e) => {
            this.previewImages(e.target.files);
            this.validateImages(e.target.files);
        });
    }

    previewImages(files) {
        const container = document.getElementById('image-preview-container') || this.createImagePreviewContainer();
        container.innerHTML = '';

        if (files.length === 0) return;

        const maxFiles = 6;
        const filesToShow = Math.min(files.length, maxFiles);

        for (let i = 0; i < filesToShow; i++) {
            const file = files[i];
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const preview = this.createImagePreview(e.target.result, file.name, i);
                    container.appendChild(preview);
                };
                reader.readAsDataURL(file);
            }
        }

        if (files.length > maxFiles) {
            const warning = document.createElement('small');
            warning.className = 'text-warning';
            warning.textContent = `Note: Only first ${maxFiles} images will be uploaded.`;
            container.appendChild(warning);
        }
    }

    createImagePreviewContainer() {
        const container = document.createElement('div');
        container.id = 'image-preview-container';
        container.className = 'row g-2 mt-2';

        const imageInput = document.getElementById('images');
        imageInput.parentNode.appendChild(container);

        return container;
    }

    createImagePreview(src, name, index) {
        const col = document.createElement('div');
        col.className = 'col-4 col-md-3';

        col.innerHTML = `
            <div class="position-relative">
                <img src="${src}" class="img-thumbnail w-100" style="height: 80px; object-fit: cover;" alt="Preview ${index + 1}">
                <button type="button" class="btn btn-sm btn-danger position-absolute top-0 end-0" 
                        onclick="this.parentNode.parentNode.remove()" style="padding: 2px 6px;">
                    <i class="fas fa-times"></i>
                </button>
                <small class="text-muted d-block mt-1" style="font-size: 0.7rem;">${name.substring(0, 15)}...</small>
            </div>
        `;

        return col;
    }

    validateImages(files) {
        const maxSize = 16 * 1024 * 1024; // 16MB
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
        const maxFiles = 6;

        if (files.length > maxFiles) {
            this.showImageError(`Maximum ${maxFiles} images allowed`);
            return false;
        }

        for (let file of files) {
            if (!allowedTypes.includes(file.type)) {
                this.showImageError(`Invalid file type: ${file.name}. Only JPG, PNG, and GIF are allowed.`);
                return false;
            }
            if (file.size > maxSize) {
                this.showImageError(`File too large: ${file.name}. Maximum size is 16MB.`);
                return false;
            }
        }

        this.clearImageError();
        return true;
    }

    showImageError(message) {
        let errorDiv = document.getElementById('image-error');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'image-error';
            errorDiv.className = 'invalid-feedback d-block';
            document.getElementById('images').parentNode.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
    }

    clearImageError() {
        const errorDiv = document.getElementById('image-error');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    initializeDependentFields() {
        // Auto-populate title based on year, make, model
        const yearField = document.getElementById('year');
        const makeField = document.getElementById('make');
        const modelField = document.getElementById('model');
        const titleField = document.getElementById('title');

        if (yearField && makeField && modelField && titleField) {
            const updateTitle = () => {
                const year = yearField.value;
                const make = makeField.value;
                const model = modelField.value;

                if (year && make && model && !titleField.value) {
                    titleField.value = `${year} ${make} ${model}`;
                }
            };

            [yearField, makeField, modelField].forEach(field => {
                field.addEventListener('blur', updateTitle);
            });
        }

        // Auto-set odometer reading based on mileage if empty
        const mileageField = document.getElementById('mileage');
        const odometerField = document.getElementById('odometer_reading');

        if (mileageField && odometerField) {
            mileageField.addEventListener('blur', () => {
                if (mileageField.value && !odometerField.value) {
                    odometerField.value = mileageField.value;
                }
            });
        }
    }

    validateField(field) {
        const isValid = field.checkValidity();
        field.classList.remove('is-valid', 'is-invalid');
        field.classList.add(isValid ? 'is-valid' : 'is-invalid');

        // Update custom feedback
        const feedback = field.parentNode.querySelector('.invalid-feedback');
        if (feedback && !isValid) {
            feedback.textContent = field.validationMessage;
        }

        return isValid;
    }

    validateEmail(field) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const isValid = emailRegex.test(field.value) || field.value === '';

        if (!isValid && field.value) {
            field.setCustomValidity('Please enter a valid email address');
        } else {
            field.setCustomValidity('');
        }

        this.validateField(field);
        return isValid;
    }

    validateForm() {
        const requiredFields = this.form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        // Custom validation for price
        const priceField = document.getElementById('price');
        if (priceField && parseFloat(priceField.value.replace(/[^\d.]/g, '')) <= 0) {
            priceField.setCustomValidity('Price must be greater than 0');
            this.validateField(priceField);
            isValid = false;
        }

        return isValid;
    }

    showValidationErrors() {
        const invalidFields = this.form.querySelectorAll('.is-invalid');
        if (invalidFields.length > 0) {
            // Scroll to first invalid field
            invalidFields[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
            invalidFields[0].focus();

            // Show toast notification
            this.showToast('Please fill in all required fields correctly', 'error');
        }
    }

    showToast(message, type = 'info') {
        // Create toast if it doesn't exist
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            toastContainer.style.zIndex = '1060';
            document.body.appendChild(toastContainer);
        }

        const toastId = 'toast-' + Date.now();
        const bgClass = type === 'error' ? 'bg-danger' : type === 'success' ? 'bg-success' : 'bg-info';

        const toastHtml = `
            <div id="${toastId}" class="toast ${bgClass} text-white" role="alert">
                <div class="toast-body d-flex align-items-center">
                    <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'} me-2"></i>
                    ${message}
                    <button type="button" class="btn-close btn-close-white ms-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;

        toastContainer.insertAdjacentHTML('beforeend', toastHtml);

        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, { delay: 5000 });
        toast.show();

        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }

    resetForm() {
        this.form.reset();
        this.form.classList.remove('was-validated');

        // Clear all validation states
        this.form.querySelectorAll('.is-valid, .is-invalid').forEach(field => {
            field.classList.remove('is-valid', 'is-invalid');
        });

        // Clear image preview
        const previewContainer = document.getElementById('image-preview-container');
        if (previewContainer) {
            previewContainer.innerHTML = '';
        }

        // Clear image errors
        this.clearImageError();
    }
}

// Auto-save functionality for forms
class AutoSaveManager {
    constructor(formId, key) {
        this.form = document.getElementById(formId);
        this.storageKey = key;
        this.initializeAutoSave();
    }

    initializeAutoSave() {
        if (!this.form) return;

        // Load saved data
        this.loadFromStorage();

        // Save on input
        this.form.addEventListener('input', debounce(() => {
            this.saveToStorage();
        }, 1000));

        // Clear on successful submit
        this.form.addEventListener('submit', () => {
            this.clearStorage();
        });
    }

    saveToStorage() {
        const formData = new FormData(this.form);
        const data = {};

        for (let [key, value] of formData.entries()) {
            if (value && key !== 'csrf_token' && key !== 'images') {
                data[key] = value;
            }
        }

        localStorage.setItem(this.storageKey, JSON.stringify(data));
    }

    loadFromStorage() {
        const saved = localStorage.getItem(this.storageKey);
        if (!saved) return;

        try {
            const data = JSON.parse(saved);
            for (let [key, value] of Object.entries(data)) {
                const field = this.form.querySelector(`[name="${key}"]`);
                if (field && field.type !== 'file') {
                    field.value = value;
                }
            }
        } catch (e) {
            console.warn('Failed to load auto-saved data:', e);
        }
    }

    clearStorage() {
        localStorage.removeItem(this.storageKey);
    }
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Enhanced Forms JavaScript
// Remove duplicate declaration - uploadedImages is already declared globally in wizard_admin.html

document.addEventListener('DOMContentLoaded', function() {
    console.log('Enhanced forms loaded');

    // Initialize any enhanced form features here
    if (typeof initializeWizardSteps === 'function') {
        initializeWizardSteps();
    }
    if (typeof initializeImageSlots === 'function') {
        initializeImageSlots();
    }
});

function initializeWizardSteps() {
    // Wizard step navigation logic
    const nextBtns = document.querySelectorAll('.btn-next');
    const prevBtns = document.querySelectorAll('.btn-prev');

    nextBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const currentTab = document.querySelector('.tab-pane.active');
            const nextTabId = this.getAttribute('data-next');

            if (nextTabId) {
                // Hide current tab
                currentTab.classList.remove('show', 'active');

                // Show next tab
                const nextTab = document.getElementById(nextTabId);
                nextTab.classList.add('show', 'active');

                // Update progress
                updateProgress();
            }
        });
    });

    prevBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const currentTab = document.querySelector('.tab-pane.active');
            const prevTabId = this.getAttribute('data-prev');

            if (prevTabId) {
                // Hide current tab
                currentTab.classList.remove('show', 'active');

                // Show previous tab
                const prevTab = document.getElementById(prevTabId);
                prevTab.classList.add('show', 'active');

                // Update progress
                updateProgress();
            }
        });
    });
}

function initializeImageSlots() {
    // Initialize the slot content for all 6 slots
    for (let i = 1; i <= 6; i++) {
        const slot = document.getElementById(`image-slot-${i}`);
        if (slot) {
            const slotContent = slot.querySelector('.slot-content');
            if (slotContent) {
                slotContent.innerHTML = `
                    <i class="fas fa-cloud-upload-alt fa-2x text-primary mb-2"></i>
                    <p class="mb-1 fw-bold">Click to upload</p>
                    <small class="text-muted">or drag and drop image here</small>
                    <small class="d-block text-muted mt-1">Max 5MB • JPG, PNG, GIF</small>
                `;
            }

            // Add drag and drop functionality
            slot.addEventListener('dragover', function(e) {
                e.preventDefault();
                e.stopPropagation();
                const uploadSlot = this.querySelector('.image-upload-slot');
                if (uploadSlot) {
                    uploadSlot.style.background = 'linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%)';
                }
            });

            slot.addEventListener('dragleave', function(e) {
                e.preventDefault();
                e.stopPropagation();
                const uploadSlot = this.querySelector('.image-upload-slot');
                if (uploadSlot) {
                    uploadSlot.style.background = 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)';
                }
            });

            slot.addEventListener('drop', function(e) {
                e.preventDefault();
                e.stopPropagation();
                const uploadSlot = this.querySelector('.image-upload-slot');
                if (uploadSlot) {
                    uploadSlot.style.background = 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)';
                }

                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    const input = document.getElementById(`image-input-${i}`);
                    if (input) {
                        try {
                            input.files = files;
                            handleImageUpload(i, input);
                        } catch (error) {
                            console.error('Error handling dropped file:', error);
                            showToast('Error handling dropped file', 'danger');
                        }
                    }
                }
            });
        }
    }
}

function triggerImageUpload(slotNumber) {
    document.getElementById(`image-input-${slotNumber}`).click();
}

function handleImageUpload(slotNumber, input) {
    const file = input.files[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
        showToast('Please select a valid image file.', 'error');
        return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
        showToast('Image size should be less than 5MB.', 'error');
        return;
    }

    const slot = document.getElementById(`image-slot-${slotNumber}`);
    const preview = document.getElementById(`image-preview-${slotNumber}`);
    const slotContent = slot.querySelector('.slot-content');

    // Read and display the image
    const reader = new FileReader();
    reader.onload = function(e) {
        preview.src = e.target.result;
        preview.style.display = 'block';
        slotContent.style.display = 'none';

        // Add remove button
        let removeBtn = slot.querySelector('.remove-image-btn');
        if (!removeBtn) {
            removeBtn = document.createElement('button');
            removeBtn.type = 'button';
            removeBtn.className = 'btn btn-danger btn-sm position-absolute remove-image-btn';
            removeBtn.style.cssText = 'top: 5px; right: 5px; z-index: 10;';
            removeBtn.innerHTML = '<i class="fas fa-times"></i>';
            removeBtn.onclick = function() { removeImage(slotNumber); };
            slot.style.position = 'relative';
            slot.appendChild(removeBtn);
        }

        // Update slot styling
        const uploadSlot = slot.querySelector('.image-upload-slot');
        if (uploadSlot) {
            uploadSlot.style.border = '2px solid #28a745';
            uploadSlot.style.background = 'linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%)';
        }
    };
    reader.readAsDataURL(file);

    // Store the file for form submission
    uploadedImages[slotNumber - 1] = file;
    updateFormFileInput();
}

function removeImage(slotNumber) {
    const slot = document.getElementById(`image-slot-${slotNumber}`);
    const preview = document.getElementById(`image-preview-${slotNumber}`);
    const slotContent = slot.querySelector('.slot-content');
    const removeBtn = slot.querySelector('.remove-image-btn');
    const input = document.getElementById(`image-input-${slotNumber}`);

    // Hide preview and show upload content
    preview.style.display = 'none';
    preview.src = '';
    slotContent.style.display = 'flex';

    // Remove the remove button
    if (removeBtn) {
        removeBtn.remove();
    }

    // Clear the input
    input.value = '';

    // Reset slot styling
    const uploadSlot = slot.querySelector('.image-upload-slot');
    if (uploadSlot) {
        uploadSlot.style.border = '2px dashed #007bff';
        uploadSlot.style.background = 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)';
    }

    // Remove from uploaded images array
    uploadedImages[slotNumber - 1] = null;
    updateFormFileInput();
}

function updateFormFileInput() {
    const formFileInput = document.querySelector('input[name="images"]');
    if (formFileInput) {
        const dt = new DataTransfer();
        uploadedImages.forEach(file => {
            if (file) {
                dt.items.add(file);
            }
        });
        formFileInput.files = dt.files;
    }
}

function updateProgress() {
    const activeTab = document.querySelector('.tab-pane.active');
    const allTabs = document.querySelectorAll('.tab-pane');
    const activeIndex = Array.from(allTabs).indexOf(activeTab);
    const progress = ((activeIndex + 1) / allTabs.length) * 100;

    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        progressBar.style.width = progress + '%';
        progressBar.setAttribute('aria-valuenow', progress);
    }
}

function showToast(message, type) {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(toast);

    // Auto remove after 3 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 3000);
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Initialize form manager
    new VehicleFormManager();

    // Initialize auto-save for vehicle form
    new AutoSaveManager('vehicleForm', 'vehicle_form_autosave');
});

// Export for global access
window.VehicleFormManager = VehicleFormManager;
window.AutoSaveManager = AutoSaveManager;