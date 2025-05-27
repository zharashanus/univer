/**
 * ENIC Kazakhstan - Main JavaScript
 * Основные интерактивные функции сайта
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== CSRF Token Setup for AJAX =====
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    
    // Setup CSRF for all AJAX requests
    if (typeof jQuery !== 'undefined') {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!this.crossDomain && !/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.noCSRF) {
                    xhr.setRequestHeader("X-CSRFToken", csrfToken);
                }
            }
        });
    }
    
    // ===== Accessibility Features =====
    const accessibilityToggle = document.getElementById('accessibility-toggle');
    const accessibilityVersion = document.getElementById('accessibility-version');
    let isAccessibilityMode = localStorage.getItem('accessibility-mode') === 'true';
    
    // Apply accessibility mode if enabled
    if (isAccessibilityMode) {
        enableAccessibilityMode();
    }
    
    // Accessibility toggle handlers
    if (accessibilityToggle) {
        accessibilityToggle.addEventListener('click', toggleAccessibilityMode);
    }
    if (accessibilityVersion) {
        accessibilityVersion.addEventListener('click', toggleAccessibilityMode);
    }
    
    function toggleAccessibilityMode() {
        isAccessibilityMode = !isAccessibilityMode;
        localStorage.setItem('accessibility-mode', isAccessibilityMode);
        
        if (isAccessibilityMode) {
            enableAccessibilityMode();
        } else {
            disableAccessibilityMode();
        }
    }
    
    function enableAccessibilityMode() {
        document.body.classList.add('accessibility-high-contrast', 'accessibility-large-text');
        updateAccessibilityButtons('Обычная версия');
    }
    
    function disableAccessibilityMode() {
        document.body.classList.remove('accessibility-high-contrast', 'accessibility-large-text');
        updateAccessibilityButtons('Версия для слабовидящих');
    }
    
    function updateAccessibilityButtons(text) {
        if (accessibilityToggle) {
            accessibilityToggle.innerHTML = `<i class="bi bi-eye"></i> ${text}`;
        }
        if (accessibilityVersion) {
            accessibilityVersion.innerHTML = `<i class="bi bi-eye"></i> ${text}`;
        }
    }
    
    // ===== Back to Top Button =====
    const backToTopBtn = document.getElementById('back-to-top');
    
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.style.display = 'block';
            } else {
                backToTopBtn.style.display = 'none';
            }
        });
        
        backToTopBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // ===== Smooth Scrolling for Anchor Links =====
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // ===== Auto-hide Alerts =====
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentNode) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000); // Hide after 5 seconds
    });
    
    // ===== Form Validation Enhancement =====
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalidField = form.querySelector(':invalid');
                if (firstInvalidField) {
                    firstInvalidField.focus();
                }
            }
            form.classList.add('was-validated');
        });
    });
    
    // ===== File Upload Enhancement =====
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        const maxSize = 5 * 1024 * 1024; // 5MB
        const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        
        input.addEventListener('change', function() {
            const files = this.files;
            let isValid = true;
            let errorMessage = '';
            
            for (let file of files) {
                // Check file size
                if (file.size > maxSize) {
                    isValid = false;
                    errorMessage = `Файл "${file.name}" превышает максимальный размер 5MB.`;
                    break;
                }
                
                // Check file type
                if (!allowedTypes.includes(file.type)) {
                    isValid = false;
                    errorMessage = `Файл "${file.name}" имеет недопустимый тип. Разрешены: PDF, JPG, PNG, DOC, DOCX.`;
                    break;
                }
            }
            
            if (!isValid) {
                this.value = '';
                showAlert(errorMessage, 'danger');
            } else {
                // Update label with selected file names
                const label = this.parentNode.querySelector('label');
                if (label && files.length > 0) {
                    const fileNames = Array.from(files).map(f => f.name).join(', ');
                    label.textContent = fileNames.length > 50 ? fileNames.substring(0, 50) + '...' : fileNames;
                }
            }
        });
    });
    
    // ===== Search Enhancement =====
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length >= 3) {
                searchTimeout = setTimeout(() => {
                    // Implement live search suggestions here
                    showSearchSuggestions(query);
                }, 300);
            } else {
                hideSearchSuggestions();
            }
        });
    }
    
    // ===== Loading States =====
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            if (form && form.checkValidity()) {
                showLoadingState(this);
            }
        });
    });
    
    function showLoadingState(button) {
        const originalText = button.innerHTML;
        button.innerHTML = '<span class="spinner"></span> Загрузка...';
        button.disabled = true;
        
        // Store original text for restoration
        button.setAttribute('data-original-text', originalText);
    }
    
    function hideLoadingState(button) {
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
            button.innerHTML = originalText;
            button.disabled = false;
            button.removeAttribute('data-original-text');
        }
    }
    
    // ===== Utility Functions =====
    function showAlert(message, type = 'info') {
        const alertsContainer = document.querySelector('.messages-container') || createAlertsContainer();
        
        const alertElement = document.createElement('div');
        alertElement.className = `alert alert-${type} alert-dismissible fade show`;
        alertElement.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        alertsContainer.appendChild(alertElement);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertElement.parentNode) {
                const bsAlert = new bootstrap.Alert(alertElement);
                bsAlert.close();
            }
        }, 5000);
    }
    
    function createAlertsContainer() {
        const container = document.createElement('div');
        container.className = 'messages-container';
        
        const innerContainer = document.createElement('div');
        innerContainer.className = 'container mt-3';
        
        container.appendChild(innerContainer);
        
        const mainContent = document.getElementById('main-content');
        if (mainContent) {
            mainContent.parentNode.insertBefore(container, mainContent);
        } else {
            document.body.insertBefore(container, document.body.firstChild);
        }
        
        return innerContainer;
    }
    
    function showSearchSuggestions(query) {
        // This would typically make an AJAX request to get suggestions
        // For now, just placeholder functionality
        console.log('Searching for:', query);
    }
    
    function hideSearchSuggestions() {
        const suggestions = document.querySelector('.search-suggestions');
        if (suggestions) {
            suggestions.remove();
        }
    }
    
    // ===== Animation on Scroll =====
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animateElements = document.querySelectorAll('.card, .feature-item, .news-item');
    animateElements.forEach(el => observer.observe(el));
    
    // ===== Keyboard Navigation Enhancement =====
    document.addEventListener('keydown', function(e) {
        // Escape key to close modals, dropdowns
        if (e.key === 'Escape') {
            const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
            openDropdowns.forEach(dropdown => {
                const toggle = dropdown.previousElementSibling;
                if (toggle) {
                    bootstrap.Dropdown.getInstance(toggle).hide();
                }
            });
        }
        
        // Alt + H for home
        if (e.altKey && e.key === 'h') {
            e.preventDefault();
            window.location.href = '/';
        }
        
        // Alt + S for search
        if (e.altKey && e.key === 's') {
            e.preventDefault();
            const searchInput = document.querySelector('input[name="q"]');
            if (searchInput) {
                searchInput.focus();
            }
        }
    });
    
    // ===== Print Functionality =====
    const printButtons = document.querySelectorAll('.btn-print');
    printButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            window.print();
        });
    });
    
    // ===== Copy to Clipboard =====
    const copyButtons = document.querySelectorAll('.btn-copy');
    copyButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const targetSelector = this.getAttribute('data-copy-target');
            const targetElement = document.querySelector(targetSelector);
            
            if (targetElement) {
                const textToCopy = targetElement.textContent || targetElement.value;
                
                if (navigator.clipboard) {
                    navigator.clipboard.writeText(textToCopy).then(() => {
                        showAlert('Скопировано в буфер обмена', 'success');
                    });
                } else {
                    // Fallback for older browsers
                    const textArea = document.createElement('textarea');
                    textArea.value = textToCopy;
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                    showAlert('Скопировано в буфер обмена', 'success');
                }
            }
        });
    });
    
    // ===== Language Preferences =====
    const languageLinks = document.querySelectorAll('.language-switcher a');
    languageLinks.forEach(link => {
        link.addEventListener('click', function() {
            const lang = new URL(this.href).searchParams.get('language');
            if (lang) {
                localStorage.setItem('preferred-language', lang);
            }
        });
    });
    
    // ===== Performance Optimization =====
    // Lazy load images
    const lazyImages = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
    
    // ===== Error Handling =====
    window.addEventListener('error', function(e) {
        console.error('JavaScript error:', e.error);
        // In production, you might want to send this to an error tracking service
    });
    
    // ===== Debug Info (Development Only) =====
    if (document.body.getAttribute('data-debug') === 'true') {
        console.log('ENIC Kazakhstan website loaded successfully');
        console.log('Accessibility mode:', isAccessibilityMode);
        console.log('Browser:', navigator.userAgent);
    }
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // ===== Chatbot Mockup =====
    const chatbotToggler = document.querySelector('.chatbot-toggler');
    const chatbotWindow = document.getElementById('chatbotWindow');
    const chatbotCloseBtn = document.querySelector('.chatbot-close-btn');

    if (chatbotToggler && chatbotWindow && chatbotCloseBtn) {
        chatbotToggler.addEventListener('click', () => {
            const isHidden = chatbotWindow.style.display === 'none' || chatbotWindow.style.display === '';
            chatbotWindow.style.display = isHidden ? 'flex' : 'none'; // Use flex as it's a flex container
        });

        chatbotCloseBtn.addEventListener('click', () => {
            chatbotWindow.style.display = 'none';
        });

        // Optional: Close chatbot if a click occurs outside of it
        document.addEventListener('click', function(event) {
            if (!chatbotWindow.contains(event.target) && !chatbotToggler.contains(event.target)) {
                // chatbotWindow.style.display = 'none'; // Uncomment if you want this behavior
            }
        });
         // Optional: Close chatbot with Escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && chatbotWindow.style.display === 'flex') {
                chatbotWindow.style.display = 'none';
            }
        });
    }

});

// ===== Global Utility Functions =====
window.EnicUtils = {
    showAlert: function(message, type = 'info') {
        // This function is available globally for use in other scripts
        const event = new CustomEvent('showAlert', {
            detail: { message, type }
        });
        document.dispatchEvent(event);
    },
    
    toggleLoading: function(element, show = true) {
        if (show) {
            element.innerHTML = '<span class="spinner"></span> Загрузка...';
            element.disabled = true;
        } else {
            const originalText = element.getAttribute('data-original-text');
            if (originalText) {
                element.innerHTML = originalText;
                element.disabled = false;
            }
        }
    }
}; 