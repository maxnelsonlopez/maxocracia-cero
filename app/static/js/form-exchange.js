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

    // Initialize searches
    initParticipantSearch('giver');
    initParticipantSearch('receiver');

    // Handle wizard completion
    wizard.onComplete = async (formData) => {
        console.log('Wizard complete! Data:', formData);

        // Check for required participant IDs
        if (!formData.giver_id || !formData.receiver_id) {
            alert('Por favor selecciona un aportante y un beneficiario válidos.');
            return;
        }

        try {
            const result = await api.registerInterchange(formData);
            if (result.success) {
                // Show success message
                document.getElementById('successDetails').textContent =
                    `Intercambio ${formData.interchange_id || ''} registrado exitosamente.`;
                document.getElementById('exchangeForm').style.display = 'none';
                document.getElementById('successMessage').style.display = 'block';
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        } catch (error) {
            console.error('Submit error:', error);
            alert('Error: ' + error.message);
        }
    };
});

/**
 * Initialize participant search functionality.
 */
function initParticipantSearch(type) {
    const searchInput = document.getElementById(`${type}_search`);
    const resultsContainer = document.getElementById(`${type}_results`);
    const idInput = document.getElementById(`${type}_id`);
    const badge = document.getElementById(`${type}_badge`);
    const badgeName = badge.querySelector('.selected-badge-name');

    let debounceTimer;

    searchInput.addEventListener('input', () => {
        const query = searchInput.value.trim();
        clearTimeout(debounceTimer);

        if (query.length < 2) {
            resultsContainer.style.display = 'none';
            return;
        }

        debounceTimer = setTimeout(async () => {
            resultsContainer.innerHTML = '<div class="search-loading"><div class="loading-spinner"></div> Buscando...</div>';
            resultsContainer.style.display = 'block';

            try {
                const data = await api.getParticipants({ search: query, limit: 10 });
                const participants = data.participants || data; // Handle different API response shapes

                if (!participants || participants.length === 0) {
                    resultsContainer.innerHTML = '<div class="search-no-results">No se encontraron participantes</div>';
                } else {
                    resultsContainer.innerHTML = '';
                    participants.forEach(p => {
                        const item = document.createElement('div');
                        item.className = 'search-result-item';
                        item.innerHTML = `
                            <span class="search-result-name">${p.name}</span>
                            <span class="search-result-email">${p.email || p.neighborhood || ''}</span>
                        `;
                        item.onclick = () => selectParticipant(type, p);
                        resultsContainer.appendChild(item);
                    });
                }
            } catch (error) {
                console.error('Search error:', error);
                resultsContainer.innerHTML = '<div class="search-no-results">Error al buscar</div>';
            }
        }, 300);
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
            resultsContainer.style.display = 'none';
        }
    });
}

function selectParticipant(type, participant) {
    const searchInput = document.getElementById(`${type}_search`);
    const resultsContainer = document.getElementById(`${type}_results`);
    const idInput = document.getElementById(`${type}_id`);
    const badge = document.getElementById(`${type}_badge`);
    const badgeName = badge.querySelector('.selected-badge-name');

    idInput.value = participant.id;
    badgeName.textContent = participant.name;

    searchInput.style.display = 'none';
    resultsContainer.style.display = 'none';
    badge.style.display = 'inline-flex';
}

function clearSelection(type) {
    const searchInput = document.getElementById(`${type}_search`);
    const idInput = document.getElementById(`${type}_id`);
    const badge = document.getElementById(`${type}_badge`);

    idInput.value = '';
    searchInput.value = '';
    searchInput.style.display = 'block';
    badge.style.display = 'none';
    searchInput.focus();
}

function resetForm() {
    location.reload();
}
