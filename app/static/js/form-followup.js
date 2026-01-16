/**
 * Form Followup (Formulario B) - JavaScript Handler
 */

console.log('Form Followup script loaded');

document.addEventListener('DOMContentLoaded', function () {
    const wizard = new FormWizard('followupForm');

    // Set default date to today
    const dateField = document.getElementById('follow_up_date');
    if (dateField) {
        dateField.valueAsDate = new Date();
    }

    // Handle wizard completion
    wizard.onComplete = async (formData) => {
        console.log('Wizard complete! Data:', formData);

        // Get auth token
        const token = localStorage.getItem('access_token');
        if (!token) {
            alert('Debes iniciar sesión para registrar seguimientos');
            return;
        }

        // Add dummy IDs for now
        formData.participant_id = 1;

        try {
            const response = await fetch('/forms/follow-up', {
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
                document.getElementById('successDetails').textContent = 'Seguimiento registrado exitosamente.';
                document.getElementById('followupForm').style.display = 'none';
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
