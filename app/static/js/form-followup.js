/**
 * Form Followup (Formulario B) - JavaScript Handler
 * 
 * Handles form submission for follow-up reports.
 * Sends data to /forms/follow-up API endpoint.
 * Requires authentication (JWT token).
 */

console.log('Form Followup script loaded');

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('followupForm');

    if (!form) {
        console.error('followupForm not found');
        return;
    }

    console.log('Followup form found, initializing...');

    // Set default date to today
    const dateField = document.getElementById('follow_up_date');
    if (dateField) {
        dateField.valueAsDate = new Date();
    }

    // Show/hide conditional fields based on active interchanges status
    document.querySelectorAll('input[name="active_interchanges_status"]').forEach(radio => {
        radio.addEventListener('change', function () {
            const workingGroup = document.getElementById('interchangesWorkingGroup');
            if (this.value !== 'none') {
                workingGroup.style.display = 'block';
            } else {
                workingGroup.style.display = 'none';
            }
        });
    });

    // Show/hide next followup date based on priority
    document.querySelectorAll('input[name="follow_up_priority"]').forEach(radio => {
        radio.addEventListener('change', function () {
            const nextGroup = document.getElementById('nextFollowupGroup');
            if (this.value !== 'closed') {
                nextGroup.style.display = 'block';
            } else {
                nextGroup.style.display = 'none';
            }
        });
    });

    // Form submission
    form.addEventListener('submit', async function (e) {
        console.log('Followup form submit triggered');
        e.preventDefault();

        const token = localStorage.getItem('access_token');
        if (!token) {
            showFollowupError('Debes iniciar sesión para registrar seguimientos');
            return;
        }

        // Validate required radio buttons
        const followUpTypeRadio = document.querySelector('input[name="follow_up_type"]:checked');
        const needLevelRadio = document.querySelector('input[name="need_level"]:checked');
        const situationChangeRadio = document.querySelector('input[name="situation_change"]:checked');
        const activeStatusRadio = document.querySelector('input[name="active_interchanges_status"]:checked');
        const priorityRadio = document.querySelector('input[name="follow_up_priority"]:checked');

        if (!followUpTypeRadio) {
            showFollowupError('Por favor selecciona el tipo de seguimiento');
            return;
        }
        if (!needLevelRadio) {
            showFollowupError('Por favor selecciona el nivel de necesidad actual');
            return;
        }
        if (!situationChangeRadio) {
            showFollowupError('Por favor indica cómo cambió la situación');
            return;
        }
        if (!activeStatusRadio) {
            showFollowupError('Por favor indica el estado de intercambios activos');
            return;
        }
        if (!priorityRadio) {
            showFollowupError('Por favor selecciona la prioridad de seguimiento');
            return;
        }

        const formData = {
            follow_up_date: document.getElementById('follow_up_date').value,
            participant_id: 1, // TODO: Get from participant lookup
            related_interchange_id: null, // TODO: Get from interchange lookup
            follow_up_type: followUpTypeRadio.value,
            current_situation: document.getElementById('current_situation').value,
            need_level: parseInt(needLevelRadio.value),
            situation_change: situationChangeRadio.value,
            active_interchanges_status: activeStatusRadio.value,
            interchanges_working_well: document.querySelector('input[name="interchanges_working_well"]:checked')?.value || null,
            new_needs_detected: getFollowupCheckedValues('new_needs_detected'),
            new_offers_detected: getFollowupCheckedValues('new_offers_detected'),
            emotional_state: document.querySelector('input[name="emotional_state"]:checked')?.value || null,
            community_connection: document.querySelector('input[name="community_connection"]:checked') ?
                parseInt(document.querySelector('input[name="community_connection"]:checked').value) : null,
            actions_required: getFollowupCheckedValues('actions_required'),
            follow_up_priority: priorityRadio.value,
            next_follow_up_date: document.getElementById('next_follow_up_date').value || null,
            facilitator_notes: document.getElementById('facilitator_notes').value || null,
            learnings: document.getElementById('learnings').value || null
        };

        console.log('Submitting followup data:', formData);

        await submitFollowupForm(formData, token);
    });
});

function getFollowupCheckedValues(name) {
    return Array.from(document.querySelectorAll(`input[name="${name}"]:checked`))
        .map(cb => cb.value);
}

function showFollowupError(message) {
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    if (errorMessage && errorText) {
        errorText.textContent = message;
        errorMessage.style.display = 'flex';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

async function submitFollowupForm(data, token) {
    const submitBtn = document.getElementById('submitBtn');
    const submitText = document.getElementById('submitText');
    const submitLoading = document.getElementById('submitLoading');
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');

    submitBtn.disabled = true;
    submitText.style.display = 'none';
    submitLoading.style.display = 'inline-block';
    errorMessage.style.display = 'none';

    try {
        console.log('Sending POST to /forms/follow-up');
        const response = await fetch('/forms/follow-up', {
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
            const priorityEmoji = data.follow_up_priority === 'high' ? '🔴' :
                data.follow_up_priority === 'medium' ? '🟡' :
                    data.follow_up_priority === 'low' ? '🟢' : '✅';
            document.getElementById('successDetails').textContent =
                `Seguimiento registrado con prioridad ${priorityEmoji} ${data.follow_up_priority}.`;
            document.getElementById('followupForm').style.display = 'none';
            document.getElementById('successMessage').style.display = 'block';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
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
        submitBtn.disabled = false;
        submitText.style.display = 'inline';
        submitLoading.style.display = 'none';
    }
}

function resetForm() {
    document.getElementById('followupForm').reset();
    document.getElementById('followupForm').style.display = 'block';
    document.getElementById('successMessage').style.display = 'none';
    document.getElementById('follow_up_date').valueAsDate = new Date();
    document.getElementById('interchangesWorkingGroup').style.display = 'none';
    document.getElementById('nextFollowupGroup').style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
