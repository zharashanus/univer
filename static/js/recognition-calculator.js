// Recognition Calculator Script

document.addEventListener('DOMContentLoaded', function() {
    // Pricing configuration
    const pricing = {
        education_level: {
            secondary: 10000,
            bachelor: 15000,
            master: 18000,
            phd: 25000
        },
        country_multiplier: {
            cis: 1.0,
            europe: 1.2,
            america: 1.3,
            asia: 1.25,
            other: 1.35
        },
        speed: {
            standard: 0,
            fast: 10000
        },
        additional_services: {
            translation: 5000,
            apostille: 3000,
            consultation: 2000
        },
        processing_days: {
            education_level: {
                secondary: { min: 20, max: 30 },
                bachelor: { min: 30, max: 45 },
                master: { min: 30, max: 60 },
                phd: { min: 45, max: 75 }
            },
            country_modifier: {
                cis: 1.0,
                europe: 1.2,
                america: 1.3,
                asia: 1.15,
                other: 1.4
            },
            speed_modifier: {
                standard: 1.0,
                fast: 0.5
            }
        }
    };

    let selectedOptions = {};

    // Setup option card selection
    setupOptionCards();

    function setupOptionCards() {
        const optionCards = document.querySelectorAll('.option-card');
        
        optionCards.forEach(card => {
            card.addEventListener('click', function() {
                const option = this.dataset.option;
                const value = this.dataset.value;
                
                // Handle single select options
                if (['education_level', 'country', 'speed'].includes(option)) {
                    // Remove selection from other cards in the same option group
                    document.querySelectorAll(`[data-option="${option}"]`).forEach(c => {
                        c.classList.remove('selected');
                    });
                    
                    // Select this card
                    this.classList.add('selected');
                    selectedOptions[option] = value;
                } 
                // Handle multi-select options (additional services)
                else if (['translation', 'apostille', 'consultation'].includes(option)) {
                    if (this.classList.contains('selected')) {
                        this.classList.remove('selected');
                        delete selectedOptions[option];
                    } else {
                        this.classList.add('selected');
                        selectedOptions[option] = value;
                    }
                }
                
                // Update calculate button state
                updateCalculateButton();
            });
        });
    }

    function updateCalculateButton() {
        const button = document.querySelector('[onclick="calculateCost()"]');
        const requiredOptions = ['education_level', 'country', 'speed'];
        const hasAllRequired = requiredOptions.every(option => selectedOptions[option]);
        
        if (hasAllRequired) {
            button.disabled = false;
            button.classList.remove('btn-secondary');
            button.classList.add('btn-primary');
        } else {
            button.disabled = true;
            button.classList.remove('btn-primary');
            button.classList.add('btn-secondary');
        }
    }

    // Global calculate function
    window.calculateCost = function() {
        if (!validateSelections()) {
            showValidationError();
            return;
        }

        const results = performCalculation();
        displayResults(results);
        
        // Scroll to results
        document.getElementById('resultsPanel').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
        
        // Save calculation to localStorage
        saveCalculationData(results);
    };

    function validateSelections() {
        const requiredOptions = ['education_level', 'country', 'speed'];
        return requiredOptions.every(option => selectedOptions[option]);
    }

    function showValidationError() {
        // Highlight missing selections
        const requiredOptions = ['education_level', 'country', 'speed'];
        requiredOptions.forEach(option => {
            if (!selectedOptions[option]) {
                const section = document.querySelector(`[data-option="${option}"]`).closest('.calculator-section');
                section.scrollIntoView({ behavior: 'smooth', block: 'center' });
                
                // Add a temporary highlight effect
                section.style.border = '2px solid #dc3545';
                setTimeout(() => {
                    section.style.border = '';
                }, 3000);
                
                return; // Stop at first missing option
            }
        });
        
        showToast('Пожалуйста, выберите все обязательные опции', 'warning');
    }

    function performCalculation() {
        const educationLevel = selectedOptions.education_level;
        const country = selectedOptions.country;
        const speed = selectedOptions.speed;
        
        // Calculate base cost
        let baseCost = pricing.education_level[educationLevel];
        
        // Apply country multiplier
        baseCost *= pricing.country_multiplier[country];
        
        // Add speed cost
        baseCost += pricing.speed[speed];
        
        // Add additional services
        let additionalCost = 0;
        ['translation', 'apostille', 'consultation'].forEach(service => {
            if (selectedOptions[service]) {
                additionalCost += pricing.additional_services[service];
            }
        });
        
        const totalCost = Math.round(baseCost + additionalCost);
        
        // Calculate processing time
        const baseDays = pricing.processing_days.education_level[educationLevel];
        const countryModifier = pricing.processing_days.country_modifier[country];
        const speedModifier = pricing.processing_days.speed_modifier[speed];
        
        const minDays = Math.round(baseDays.min * countryModifier * speedModifier);
        const maxDays = Math.round(baseDays.max * countryModifier * speedModifier);
        
        return {
            totalCost,
            processingTime: { min: minDays, max: maxDays },
            breakdown: {
                baseCost: Math.round(baseCost - pricing.speed[speed]),
                speedCost: pricing.speed[speed],
                additionalCost,
                countryMultiplier: pricing.country_multiplier[country]
            },
            selections: { ...selectedOptions }
        };
    }

    function displayResults(results) {
        // Show results panel
        const resultsPanel = document.getElementById('resultsPanel');
        resultsPanel.style.display = 'block';
        
        // Update cost
        document.getElementById('totalCost').textContent = 
            results.totalCost.toLocaleString('ru-RU') + ' ₸';
        
        // Update processing time
        document.getElementById('processingTime').textContent = 
            `${results.processingTime.min}-${results.processingTime.max}`;
        
        // Validity period is always 5 years for recognition certificates
        document.getElementById('validityPeriod').textContent = '5';
        
        // Add animation
        resultsPanel.classList.add('fade-in');
    }

    function saveCalculationData(results) {
        const calculationData = {
            timestamp: new Date().toISOString(),
            results,
            url: window.location.href
        };
        
        // Save to localStorage
        const savedCalculations = JSON.parse(localStorage.getItem('recognition_calculations') || '[]');
        savedCalculations.unshift(calculationData);
        
        // Keep only last 10 calculations
        if (savedCalculations.length > 10) {
            savedCalculations.splice(10);
        }
        
        localStorage.setItem('recognition_calculations', JSON.stringify(savedCalculations));
    }

    // Global save calculation function
    window.saveCalculation = function() {
        const savedCalculations = JSON.parse(localStorage.getItem('recognition_calculations') || '[]');
        
        if (savedCalculations.length > 0) {
            const latestCalculation = savedCalculations[0];
            
            // Create a shareable link
            const params = new URLSearchParams();
            Object.keys(latestCalculation.results.selections).forEach(key => {
                params.set(key, latestCalculation.results.selections[key]);
            });
            
            const shareableUrl = `${window.location.origin}${window.location.pathname}?${params.toString()}`;
            
            // Copy to clipboard
            navigator.clipboard.writeText(shareableUrl).then(() => {
                showToast('Ссылка на расчет скопирована в буфер обмена', 'success');
            }).catch(() => {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = shareableUrl;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                showToast('Ссылка на расчет скопирована', 'success');
            });
        }
    };

    // Load calculation from URL parameters
    function loadFromUrlParams() {
        const urlParams = new URLSearchParams(window.location.search);
        
        let hasParams = false;
        ['education_level', 'country', 'speed', 'translation', 'apostille', 'consultation'].forEach(param => {
            const value = urlParams.get(param);
            if (value) {
                selectedOptions[param] = value;
                
                // Select the corresponding card
                const card = document.querySelector(`[data-option="${param}"][data-value="${value}"]`);
                if (card) {
                    card.classList.add('selected');
                    hasParams = true;
                }
            }
        });
        
        if (hasParams) {
            updateCalculateButton();
            // Auto-calculate if all required options are present
            if (validateSelections()) {
                setTimeout(() => {
                    calculateCost();
                }, 500);
            }
        }
    }

    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3 fade-in`;
        toast.style.zIndex = '9999';
        toast.style.minWidth = '300px';
        toast.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <span>${message}</span>
                <button type="button" class="btn-close btn-close-white" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }

    // Initialize
    updateCalculateButton();
    loadFromUrlParams();

    // Add helpful tooltips
    addTooltips();

    function addTooltips() {
        const tooltipData = {
            'education_level': 'Выберите уровень вашего образования',
            'country': 'Страна, где вы получили образование, влияет на сложность процедуры',
            'speed': 'Ускоренная обработка сократит сроки в 2 раза',
            'translation': 'Нотариальный перевод документов на казахский/русский язык',
            'apostille': 'Консультация по получению апостиля или консульской легализации',
            'consultation': 'Личная встреча со специалистом для разбора вашего случая'
        };

        Object.keys(tooltipData).forEach(option => {
            const cards = document.querySelectorAll(`[data-option="${option}"]`);
            cards.forEach(card => {
                card.title = tooltipData[option];
            });
        });
    }

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.target.classList.contains('option-card')) {
            e.target.click();
        }
    });

    // Analytics tracking (placeholder)
    function trackCalculation(results) {
        // Here you would send analytics data to your tracking service
        console.log('Calculation performed:', results);
    }

    // Make option cards accessible
    document.querySelectorAll('.option-card').forEach(card => {
        card.setAttribute('role', 'button');
        card.setAttribute('tabindex', '0');
        card.setAttribute('aria-pressed', 'false');
        
        card.addEventListener('click', function() {
            this.setAttribute('aria-pressed', this.classList.contains('selected'));
        });
    });
});

// Print calculation results
function printCalculation() {
    const resultsPanel = document.getElementById('resultsPanel');
    if (resultsPanel.style.display === 'none') {
        alert('Сначала выполните расчет');
        return;
    }

    const printContent = resultsPanel.cloneNode(true);
    
    // Remove buttons from print version
    const buttons = printContent.querySelectorAll('button, .btn');
    buttons.forEach(btn => btn.remove());

    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Расчет стоимости признания - ENIC Kazakhstan</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                @media print {
                    body { font-size: 12pt; }
                    .results-panel { background: white !important; color: black !important; }
                }
            </style>
        </head>
        <body class="p-4">
            <div class="mb-4">
                <h2>ENIC Kazakhstan - Расчет стоимости признания</h2>
                <hr>
            </div>
            ${printContent.innerHTML}
            <div class="mt-4">
                <small class="text-muted">Расчет выполнен: ${new Date().toLocaleString('ru-RU')}</small>
                <br>
                <small class="text-muted">Данный расчет носит информационный характер</small>
            </div>
        </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
} 