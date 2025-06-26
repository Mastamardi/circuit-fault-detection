// Utility functions for the dashboard

// Format numbers with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Format date/time
function formatDateTime(date) {
    return new Date(date).toLocaleString();
}

// Show loading spinner
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="loading-spinner mx-auto"></div>';
    }
}

// Hide loading spinner
function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '';
    }
}

// Show error message
function showError(message) {
    alert(message);
}

// Show success message
function showSuccess(message) {
    alert(message);
}

// Handle file upload
function handleFileUpload(file, allowedTypes, maxSize) {
    if (!file) {
        showError('Please select a file');
        return false;
    }

    if (!allowedTypes.includes(file.type)) {
        showError('Invalid file type');
        return false;
    }

    if (file.size > maxSize) {
        showError('File size exceeds limit');
        return false;
    }

    return true;
}

// Update chart data
function updateChart(chart, newData) {
    if (chart && newData) {
        chart.data = newData;
        chart.update();
    }
}

// Export data to CSV
function exportToCSV(data, filename) {
    const csvContent = "data:text/csv;charset=utf-8," + data;
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Debounce function for search inputs
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

// Initialize tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Handle responsive charts
function handleResponsiveCharts() {
    const charts = document.querySelectorAll('canvas');
    charts.forEach(chart => {
        const parent = chart.parentElement;
        if (parent) {
            const resizeObserver = new ResizeObserver(entries => {
                for (let entry of entries) {
                    const chartInstance = Chart.getChart(chart);
                    if (chartInstance) {
                        chartInstance.resize();
                    }
                }
            });
            resizeObserver.observe(parent);
        }
    });
}

// Initialize all utility functions
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
    handleResponsiveCharts();
}); 