// Recognition Application Form Script

document.addEventListener('DOMContentLoaded', function() {
    let currentStep = 1;
    const totalSteps = 4;
    
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    const form = document.getElementById('applicationForm');
    
    // Step Navigation
    function showStep(step) {
        // Hide all steps
        document.querySelectorAll('.form-step').forEach(stepEl => {
            stepEl.classList.remove('active');
        });
        
        // Show current step
        document.getElementById(`step${step}`).classList.add('active');
        
        // Update progress indicators
        document.querySelectorAll('.application-step').forEach((stepEl, index) => {
            if (index + 1 <= step) {
                stepEl.classList.add('active');
            } else {
                stepEl.classList.remove('active');
            }
        });
        
        // Update buttons
        prevBtn.style.display = step === 1 ? 'none' : 'inline-block';
        nextBtn.style.display = step === totalSteps ? 'none' : 'inline-block';
        submitBtn.style.display = step === totalSteps ? 'inline-block' : 'none';
    }
    
    function validateStep(step) {
        const stepElement = document.getElementById(`step${step}`);
        const requiredFields = stepElement.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });
        
        // Special validation for step 3 (file uploads)
        if (step === 3) {
            const requiredFiles = ['diploma', 'transcript', 'passport'];
            requiredFiles.forEach(fileType => {
                const fileContainer = document.getElementById(`${fileType}-files`);
                if (!fileContainer.children.length) {
                    const uploadArea = document.querySelector(`[data-target="${fileType}"]`);
                    uploadArea.classList.add('border-danger');
                    isValid = false;
                } else {
                    const uploadArea = document.querySelector(`[data-target="${fileType}"]`);
                    uploadArea.classList.remove('border-danger');
                }
            });
        }
        
        return isValid;
    }
    
    // Event Listeners
    nextBtn.addEventListener('click', function() {
        if (validateStep(currentStep)) {
            if (currentStep < totalSteps) {
                currentStep++;
                showStep(currentStep);
            }
        } else {
            // Show validation errors
            const firstInvalid = document.querySelector('.is-invalid, .border-danger');
            if (firstInvalid) {
                firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    });
    
    prevBtn.addEventListener('click', function() {
        if (currentStep > 1) {
            currentStep--;
            showStep(currentStep);
        }
    });
    
    // File Upload Functionality
    function setupFileUpload() {
        const uploadAreas = document.querySelectorAll('.file-upload-area');
        
        uploadAreas.forEach(area => {
            const input = area.querySelector('input[type="file"]');
            const target = area.dataset.target;
            const filesContainer = document.getElementById(`${target}-files`);
            
            // Click to upload
            area.addEventListener('click', () => input.click());
            
            // Drag and drop
            area.addEventListener('dragover', (e) => {
                e.preventDefault();
                area.classList.add('dragover');
            });
            
            area.addEventListener('dragleave', () => {
                area.classList.remove('dragover');
            });
            
            area.addEventListener('drop', (e) => {
                e.preventDefault();
                area.classList.remove('dragover');
                const files = e.dataTransfer.files;
                handleFiles(files, target, filesContainer);
            });
            
            // File input change
            input.addEventListener('change', (e) => {
                handleFiles(e.target.files, target, filesContainer);
            });
        });
    }
    
    function handleFiles(files, target, container) {
        Array.from(files).forEach(file => {
            // Validate file size (10MB max)
            if (file.size > 10 * 1024 * 1024) {
                alert('Файл слишком большой. Максимальный размер: 10MB');
                return;
            }
            
            // Validate file type
            const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
            if (!allowedTypes.includes(file.type)) {
                alert('Неподдерживаемый формат файла. Разрешены: PDF, JPG, PNG');
                return;
            }
            
            addFileToList(file, target, container);
        });
    }
    
    function addFileToList(file, target, container) {
        // Clear previous files (only one file per type for now)
        container.innerHTML = '';
        
        const fileElement = document.createElement('div');
        fileElement.className = 'uploaded-file';
        fileElement.innerHTML = `
            <div class="file-info">
                <i class="bi bi-file-earmark-pdf file-icon"></i>
                <div>
                    <div class="fw-medium">${file.name}</div>
                    <small class="text-muted">${formatFileSize(file.size)}</small>
                </div>
            </div>
            <button type="button" class="remove-file" onclick="removeFile(this, '${target}')">
                <i class="bi bi-x-circle"></i>
            </button>
        `;
        
        container.appendChild(fileElement);
        
        // Store file data for form submission
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        document.querySelector(`[data-target="${target}"] input`).files = dataTransfer.files;
    }
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Global function for removing files
    window.removeFile = function(button, target) {
        const container = document.getElementById(`${target}-files`);
        container.innerHTML = '';
        
        // Clear file input
        const input = document.querySelector(`[data-target="${target}"] input`);
        input.value = '';
    };
    
    // Form Submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!validateStep(currentStep)) {
            return;
        }
        
        // Show loading state
        form.classList.add('submitting');
        submitBtn.disabled = true;
        
        // Simulate form submission (replace with actual AJAX call)
        setTimeout(() => {
            alert('Заявка успешно отправлена! Вы получите подтверждение на указанный email.');
            // Redirect to status page or show success message
            window.location.href = '/recognition/check-status/';
        }, 2000);
    });
    
    // Remove validation errors on input
    document.addEventListener('input', function(e) {
        if (e.target.classList.contains('is-invalid')) {
            e.target.classList.remove('is-invalid');
        }
    });
    
    // Initialize
    setupFileUpload();
    showStep(1);
    
    // Phone number formatting
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.startsWith('7')) {
                value = value.substring(1);
            }
            if (value.length <= 10) {
                value = value.replace(/(\d{3})(\d{3})(\d{2})(\d{2})/, '+7 ($1) $2-$3-$4');
            }
            e.target.value = value;
        });
    }
    
    // Auto-resize textareas
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
});

// Additional utility functions
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Form auto-save functionality (optional)
function autoSaveForm() {
    const formData = new FormData(document.getElementById('applicationForm'));
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        if (value instanceof File) continue; // Skip files
        data[key] = value;
    }
    
    localStorage.setItem('recognition_application_draft', JSON.stringify(data));
}

// Load saved form data
function loadSavedData() {
    const saved = localStorage.getItem('recognition_application_draft');
    if (saved) {
        const data = JSON.parse(saved);
        Object.keys(data).forEach(key => {
            const element = document.querySelector(`[name="${key}"]`);
            if (element) {
                element.value = data[key];
            }
        });
    }
}

// Auto-save every 30 seconds
setInterval(autoSaveForm, 30000);

// Load saved data on page load
document.addEventListener('DOMContentLoaded', loadSavedData); 