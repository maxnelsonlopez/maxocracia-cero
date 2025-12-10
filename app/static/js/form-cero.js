/**
 * Form CERO (Participant Registration) - JavaScript Handler
 * 
 * Handles form submission for new participant registration.
 * Sends data to /forms/participant API endpoint.
 */

console.log('Form CERO script loaded');

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('participantForm');

    if (!form) {
        console.error('participantForm not found');
        return;
    }

    console.log('Form found, attaching submit handler');

    form.addEventListener('submit', async function (e) {
        console.log('Form submit triggered');
        e.preventDefault();

        // Validate radio button is selected
        const urgencyRadio = document.querySelector('input[name="need_urgency"]:checked');
        if (!urgencyRadio) {
            showFormError('Por favor selecciona la urgencia de tu necesidad');
            return;
        }

        // Collect form data
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            referred_by: document.getElementById('referred_by').value,
            phone_call: document.getElementById('phone_call').value,
            phone_whatsapp: document.getElementById('phone_whatsapp').value,
            telegram_handle: document.getElementById('telegram_handle').value,
            city: document.getElementById('city').value,
            neighborhood: document.getElementById('neighborhood').value,
            personal_values: document.getElementById('personal_values').value,
            offer_categories: getCheckedValues('offer_categories'),
            offer_description: document.getElementById('offer_description').value,
            offer_human_dimensions: getCheckedValues('offer_human_dimensions'),
            need_categories: getCheckedValues('need_categories'),
            need_description: document.getElementById('need_description').value,
            need_urgency: urgencyRadio.value,
            need_human_dimensions: getCheckedValues('need_human_dimensions'),
            consent_given: document.getElementById('consent_given').checked ? 1 : 0
        };

        console.log('Submitting form data:', formData);

        // Submit form
        await submitParticipantForm(formData);
    });
});

function getCheckedValues(name) {
    return Array.from(document.querySelectorAll(`input[name="${name}"]:checked`))
        .map(cb => cb.value);
}

function showFormError(message) {
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    if (errorMessage && errorText) {
        errorText.textContent = message;
        errorMessage.style.display = 'flex';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

async function submitParticipantForm(data) {
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
        console.log('Sending POST to /forms/participant');
        const response = await fetch('/forms/participant', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log('Response:', result);

        if (response.ok && result.success) {
            // Show success message
            document.getElementById('participantForm').style.display = 'none';
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
    document.getElementById('participantForm').reset();
    document.getElementById('participantForm').style.display = 'block';
    document.getElementById('successMessage').style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
