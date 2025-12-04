/**
 * Forms JavaScript - Shared utilities for Red de Apoyo forms
 */

// API Base URL
const API_BASE = '';

// Helper function to get authentication token
function getAuthToken() {
    return localStorage.getItem('access_token');
}

// Helper function to make authenticated API calls
async function apiCall(endpoint, options = {}) {
    const token = getAuthToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token && options.requiresAuth !== false) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers
    });

    return response;
}

// Form validation helpers
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    // Basic phone validation (allows various formats)
    const re = /^[\d\s\+\-\(\)]+$/;
    return re.test(phone) && phone.replace(/\D/g, '').length >= 7;
}

// Show error message
function showError(message, elementId = 'errorMessage') {
    const errorEl = document.getElementById(elementId);
    const errorText = document.getElementById('errorText');
    if (errorEl && errorText) {
        errorText.textContent = message;
        errorEl.style.display = 'flex';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// Hide error message
function hideError(elementId = 'errorMessage') {
    const errorEl = document.getElementById(elementId);
    if (errorEl) {
        errorEl.style.display = 'none';
    }
}

// Show success message
function showSuccess(message, elementId = 'successMessage') {
    const successEl = document.getElementById(elementId);
    if (successEl) {
        successEl.style.display = 'block';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// Format date for API (YYYY-MM-DD)
function formatDate(date) {
    if (typeof date === 'string') {
        return date;
    }
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Get current date in YYYY-MM-DD format
function getCurrentDate() {
    return formatDate(new Date());
}

// Debounce function for input validation
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

// Auto-save functionality (optional)
function enableAutoSave(formId, storageKey) {
    const form = document.getElementById(formId);
    if (!form) return;

    // Load saved data
    const savedData = localStorage.getItem(storageKey);
    if (savedData) {
        try {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(key => {
                const input = form.elements[key];
                if (input) {
                    if (input.type === 'checkbox') {
                        input.checked = data[key];
                    } else if (input.type === 'radio') {
                        const radio = form.querySelector(`input[name="${key}"][value="${data[key]}"]`);
                        if (radio) radio.checked = true;
                    } else {
                        input.value = data[key];
                    }
                }
            });
        } catch (e) {
            console.error('Error loading saved form data:', e);
        }
    }

    // Save on input
    const saveData = debounce(() => {
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        localStorage.setItem(storageKey, JSON.stringify(data));
    }, 1000);

    form.addEventListener('input', saveData);
    form.addEventListener('change', saveData);
}

// Clear auto-saved data
function clearAutoSave(storageKey) {
    localStorage.removeItem(storageKey);
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        apiCall,
        validateEmail,
        validatePhone,
        showError,
        hideError,
        showSuccess,
        formatDate,
        getCurrentDate,
        debounce,
        enableAutoSave,
        clearAutoSave
    };
}
