/**
 * Form Exchange (Formulario A) - JavaScript Handler
 * 
 * Handles form submission for exchange registration.
 * Sends data to /forms/exchange API endpoint.
 * Requires authentication (JWT token).
 */

console.log('Form Exchange script loaded');

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('exchangeForm');

    if (!form) {
        console.error('exchangeForm not found');
        return;
    }

    console.log('Exchange form found, initializing...');

    // Show/hide followup date based on selection
    document.querySelectorAll('input[name="requires_followup"]').forEach(radio => {
        radio.addEventListener('change', function () {
            const followupDateGroup = document.getElementById('followupDateGroup');
            if (this.value === '1') {
                followupDateGroup.style.display = 'block';
            } else {
                followupDateGroup.style.display = 'none';
            }
        });
    });

    // Set default date to today
    const dateField = document.getElementById('date');
    if (dateField) {
        dateField.valueAsDate = new Date();
    }

    // Initialize form submission
    form.addEventListener('submit', async function (e) {
        console.log('Exchange form submit triggered');
        e.preventDefault();

        // Get auth token
        const token = localStorage.getItem('access_token');
        if (!token) {
            showExchangeError('Debes iniciar sesión para registrar intercambios');
            return;
        }

        // Validate required radio buttons
        const urgencyRadio = document.querySelector('input[name="urgency"]:checked');
        const resolutionRadio = document.querySelector('input[name="impact_resolution_score"]:checked');
        const reciprocityRadio = document.querySelector('input[name="reciprocity_status"]:checked');
        const coordinationRadio = document.querySelector('input[name="coordination_method"]:checked');
        const followupRadio = document.querySelector('input[name="requires_followup"]:checked');

        if (!urgencyRadio) {
            showExchangeError('Por favor selecciona la urgencia');
            return;
        }
        if (!resolutionRadio) {
            showExchangeError('Por favor indica si se resolvió la necesidad');
            return;
        }
        if (!reciprocityRadio) {
            showExchangeError('Por favor indica el estado de reciprocidad');
            return;
        }
        if (!coordinationRadio) {
            showExchangeError('Por favor indica cómo se coordinó el intercambio');
            return;
        }
        if (!followupRadio) {
            showExchangeError('Por favor indica si requiere seguimiento');
            return;
        }

        // Collect form data
        const formData = {
            interchange_id: document.getElementById('interchange_id').value,
            date: document.getElementById('date').value,
            giver_id: 1, // TODO: Get from participant lookup
            receiver_id: 2, // TODO: Get from participant lookup
            type: getExchangeCheckedValues('type').join(','),
            description: document.getElementById('description').value,
            urgency: urgencyRadio.value,
            uth_hours: parseFloat(document.getElementById('uth_hours').value) || null,
            economic_value_approx: document.getElementById('economic_value').value || null,
            urf_description: document.getElementById('urf_description').value || null,
            impact_resolution_score: parseInt(resolutionRadio.value),
            reciprocity_status: reciprocityRadio.value,
            human_dimension_attended: getExchangeCheckedValues('human_dimension').join(','),
            coordination_method: coordinationRadio.value,
            requires_followup: parseInt(followupRadio.value),
            followup_scheduled_date: document.getElementById('followup_date').value || null,
            facilitator_notes: document.getElementById('facilitator_notes').value || null
        };

        console.log('Submitting exchange data:', formData);

        // Submit form
        await submitExchangeForm(formData, token);
    });
});

function getExchangeCheckedValues(name) {
    return Array.from(document.querySelectorAll(`input[name="${name}"]:checked`))
        .map(cb => cb.value);
}

function showExchangeError(message) {
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    if (errorMessage && errorText) {
        errorText.textContent = message;
        errorMessage.style.display = 'flex';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

async function submitExchangeForm(data, token) {
    const submitBtn = document.getElementById('submitBtn');
    const submitText = document.getElementById('submitText');
    const submitLoading = document.getElementById('submitLoading');
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');

    // Show loading state
    submitBtn.disabled = true;
    submitText.style.display = 'none';
    submitLoading.style.display = 'inline-block';
    errorMessage.style.display = 'none';

    try {
        console.log('Sending POST to /forms/exchange');
        const response = await fetch('/forms/exchange', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log('Response:', result);

        if (response.ok && result.success) {
            // Show success message
            document.getElementById('successDetails').textContent =
                `Intercambio ${data.interchange_id} registrado exitosamente.`;
            document.getElementById('exchangeForm').style.display = 'none';
            document.getElementById('successMessage').style.display = 'block';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            // Show error message
            errorText.textContent = result.error || 'Ocurrió un error al enviar el formulario';
            errorMessage.style.display = 'flex';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    } catch (error) {
        console.error('Submit error:', error);
        errorText.textContent = 'Error de conexión. Por favor intenta de nuevo.';
        errorMessage.style.display = 'flex';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        submitText.style.display = 'inline';
        submitLoading.style.display = 'none';
    }
}

function resetForm() {
    document.getElementById('exchangeForm').reset();
    document.getElementById('exchangeForm').style.display = 'block';
    document.getElementById('successMessage').style.display = 'none';
    document.getElementById('date').valueAsDate = new Date();
    document.getElementById('followupDateGroup').style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
