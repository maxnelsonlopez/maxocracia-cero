/**
 * Form Exchange (Formulario A) - JavaScript Handler
 * 
 * Handles form submission for exchange registration.
 * Sends data to /forms/exchange API endpoint.
 * Requires authentication (JWT token).
 */

console.log('Form Exchange script loaded');

document.addEventListener('DOMContentLoaded', function () {
    const wizard = new FormWizard('exchangeForm');

    // Set default date to today
    const dateField = document.getElementById('date');
    if (dateField) {
        dateField.valueAsDate = new Date();
    }

    // Handle wizard completion
    wizard.onComplete = async (formData) => {
        console.log('Wizard complete! Data:', formData);

        // Get auth token
        const token = localStorage.getItem('access_token');
        if (!token) {
            alert('Debes iniciar sesión para registrar intercambios');
            return;
        }

        // Add dummy IDs for now (will be replaced by real lookups)
        formData.giver_id = 1;
        formData.receiver_id = 2;

        try {
            const response = await fetch('/forms/exchange', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();
            if (response.ok && result.success) {
                // Show success message
                document.getElementById('successDetails').textContent =
                    `Intercambio ${formData.interchange_id || ''} registrado exitosamente.`;
                document.getElementById('exchangeForm').style.display = 'none';
                document.getElementById('successMessage').style.display = 'block';
                window.scrollTo({ top: 0, behavior: 'smooth' });
            } else {
                throw new Error(result.error || 'Error al enviar');
            }
        } catch (error) {
            console.error('Submit error:', error);
            alert('Error: ' + error.message);
        }
    };
});

function resetForm() {
    location.reload();
}
