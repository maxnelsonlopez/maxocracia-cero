/**
 * Form CERO (Participant Registration) - JavaScript Handler
 */

console.log('Form CERO script loaded');

document.addEventListener('DOMContentLoaded', function () {
    const wizard = new FormWizard('participantForm');

    // Handle wizard completion
    wizard.onComplete = async (formData) => {
        console.log('Wizard complete! Data:', formData);

        try {
            const response = await fetch('/forms/participant', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();
            if (response.ok && result.success) {
                // Show success message
                document.getElementById('participantForm').style.display = 'none';
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
