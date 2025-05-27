// Recognition Status Check Script

document.addEventListener('DOMContentLoaded', function() {
    const statusForm = document.getElementById('statusForm');
    const statusResult = document.getElementById('statusResult');
    const noResult = document.getElementById('noResult');
    
    // Sample data for demonstration
    const sampleApplications = {
        'REC-2024-001234': {
            number: 'REC-2024-001234',
            applicantName: 'Иванов Иван Иванович',
            applicationDate: '25 мая 2024',
            educationType: 'Высшее образование (Магистратура)',
            expectedDate: '15 июля 2024',
            status: 'processing',
            timeline: [
                {
                    date: '25.05.2024',
                    title: 'Заявка подана',
                    description: 'Документы получены и зарегистрированы в системе',
                    status: 'completed'
                },
                {
                    date: '27.05.2024',
                    title: 'Первичная проверка',
                    description: 'Проверка комплектности документов завершена',
                    status: 'completed'
                },
                {
                    date: '01.06.2024',
                    title: 'Экспертиза документов',
                    description: 'Документы переданы на экспертизу специалистам',
                    status: 'current'
                },
                {
                    date: '15.07.2024',
                    title: 'Принятие решения',
                    description: 'Ожидается принятие окончательного решения',
                    status: 'pending'
                }
            ]
        },
        'REC-2024-005678': {
            number: 'REC-2024-005678',
            applicantName: 'Петрова Анна Сергеевна',
            applicationDate: '15 мая 2024',
            educationType: 'Высшее образование (Бакалавриат)',
            expectedDate: '01 июля 2024',
            status: 'approved',
            timeline: [
                {
                    date: '15.05.2024',
                    title: 'Заявка подана',
                    description: 'Документы получены и зарегистрированы в системе',
                    status: 'completed'
                },
                {
                    date: '17.05.2024',
                    title: 'Первичная проверка',
                    description: 'Проверка комплектности документов завершена',
                    status: 'completed'
                },
                {
                    date: '25.05.2024',
                    title: 'Экспертиза документов',
                    description: 'Документы прошли экспертизу специалистов',
                    status: 'completed'
                },
                {
                    date: '28.05.2024',
                    title: 'Решение принято',
                    description: 'Документы об образовании признаны. Свидетельство готово к выдаче',
                    status: 'completed'
                }
            ]
        }
    };
    
    statusForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const applicationNumber = document.getElementById('applicationNumber').value.trim().toUpperCase();
        
        // Hide previous results
        statusResult.style.display = 'none';
        noResult.style.display = 'none';
        
        // Show loading state
        const submitBtn = statusForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Поиск...';
        submitBtn.disabled = true;
        
        // Simulate API call
        setTimeout(() => {
            const application = sampleApplications[applicationNumber];
            
            if (application) {
                displayApplicationStatus(application);
            } else {
                noResult.style.display = 'block';
            }
            
            // Restore button
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
            
            // Scroll to result
            const resultElement = application ? statusResult : noResult;
            resultElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            
        }, 1500);
    });
    
    function displayApplicationStatus(application) {
        // Update basic info
        document.getElementById('resultApplicationNumber').textContent = application.number;
        document.getElementById('applicantName').textContent = application.applicantName;
        document.getElementById('applicationDate').textContent = application.applicationDate;
        document.getElementById('educationType').textContent = application.educationType;
        document.getElementById('expectedDate').textContent = application.expectedDate;
        
        // Update status badge
        const statusBadge = document.getElementById('statusBadge');
        const statusText = getStatusText(application.status);
        const statusClass = getStatusClass(application.status);
        
        statusBadge.textContent = statusText;
        statusBadge.className = `status-badge ${statusClass}`;
        
        // Update timeline
        updateTimeline(application.timeline);
        
        // Show result
        statusResult.style.display = 'block';
    }
    
    function getStatusText(status) {
        const statusTexts = {
            'pending': 'Ожидает рассмотрения',
            'processing': 'В обработке',
            'additional_check': 'Дополнительная проверка',
            'approved': 'Одобрено',
            'rejected': 'Отклонено'
        };
        return statusTexts[status] || status;
    }
    
    function getStatusClass(status) {
        const statusClasses = {
            'pending': 'status-pending',
            'processing': 'status-processing',
            'additional_check': 'status-processing',
            'approved': 'status-approved',
            'rejected': 'status-rejected'
        };
        return statusClasses[status] || 'status-pending';
    }
    
    function updateTimeline(timeline) {
        const timelineContainer = document.getElementById('statusTimeline');
        timelineContainer.innerHTML = '';
        
        timeline.forEach(item => {
            const timelineItem = document.createElement('div');
            timelineItem.className = `timeline-item ${item.status}`;
            
            timelineItem.innerHTML = `
                <div class="timeline-content">
                    <div class="timeline-date">${item.date}</div>
                    <div class="timeline-title">${item.title}</div>
                    <p class="timeline-description">${item.description}</p>
                </div>
            `;
            
            timelineContainer.appendChild(timelineItem);
        });
    }
    
    // Format application number input
    const applicationNumberInput = document.getElementById('applicationNumber');
    applicationNumberInput.addEventListener('input', function(e) {
        let value = e.target.value.toUpperCase();
        // Remove any non-alphanumeric characters except hyphens
        value = value.replace(/[^A-Z0-9-]/g, '');
        e.target.value = value;
    });
    
    // Auto-complete application number format
    applicationNumberInput.addEventListener('blur', function(e) {
        let value = e.target.value.trim();
        if (value && !value.startsWith('REC-')) {
            // Try to format as REC-YYYY-XXXXXX if it looks like just numbers
            if (/^\d{10}$/.test(value)) {
                const year = new Date().getFullYear();
                value = `REC-${year}-${value.substring(4)}`;
                e.target.value = value;
            }
        }
    });
});

// Global functions for buttons
function downloadDocuments() {
    // Show download modal or start download
    alert('Функция загрузки документов будет доступна после полной реализации системы.');
}

function contactSupport() {
    // Open support contact form or redirect
    const applicationNumber = document.getElementById('resultApplicationNumber').textContent;
    const message = `Здравствуйте! У меня есть вопрос по заявке ${applicationNumber}.`;
    const email = 'support@enic-kazakhstan.edu.kz';
    const subject = `Вопрос по заявке ${applicationNumber}`;
    
    const mailtoLink = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(message)}`;
    window.location.href = mailtoLink;
}

function openChat() {
    // Open live chat widget
    alert('Онлайн-чат будет доступен в рабочие часы: Пн-Пт 9:00-18:00');
}

// Check URL parameters for automatic search
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const applicationNumber = urlParams.get('number');
    
    if (applicationNumber) {
        document.getElementById('applicationNumber').value = applicationNumber;
        document.getElementById('statusForm').dispatchEvent(new Event('submit'));
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const form = document.getElementById('statusForm');
        if (form) {
            form.dispatchEvent(new Event('submit'));
        }
    }
});

// Print functionality
function printStatus() {
    const printContent = document.getElementById('statusResult').cloneNode(true);
    
    // Remove action buttons from print version
    const buttons = printContent.querySelectorAll('button, .btn');
    buttons.forEach(btn => btn.remove());
    
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Статус заявки - ENIC Kazakhstan</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
            <style>
                @media print {
                    .no-print { display: none !important; }
                    body { font-size: 12pt; }
                }
            </style>
        </head>
        <body class="p-4">
            <div class="mb-4">
                <h2>ENIC Kazakhstan - Статус заявки</h2>
                <hr>
            </div>
            ${printContent.innerHTML}
            <div class="mt-4">
                <small class="text-muted">Распечатано: ${new Date().toLocaleString('ru-RU')}</small>
            </div>
        </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}

// Add notification functionality
function setupNotifications() {
    if ('Notification' in window && 'serviceWorker' in navigator) {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                console.log('Notifications enabled');
            }
        });
    }
}

// Call on page load
document.addEventListener('DOMContentLoaded', setupNotifications); 