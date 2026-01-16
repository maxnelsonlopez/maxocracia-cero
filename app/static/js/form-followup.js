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

    // Initialize participant search
    initParticipantSearch();

    // Handle wizard completion
    wizard.onComplete = async (formData) => {
        console.log('Wizard complete! Data:', formData);

        if (!formData.participant_id) {
            alert('Por favor selecciona un participante válido.');
            return;
        }

        try {
            const result = await api.registerFollowup(formData);
            if (result.success) {
                document.getElementById('successDetails').textContent = 'Seguimiento registrado exitosamente.';
                document.getElementById('followupForm').style.display = 'none';
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
 * Initialize participant search and selection.
 */
function initParticipantSearch() {
    const searchInput = document.getElementById('participant_search');
    const resultsContainer = document.getElementById('participant_results');
    const idInput = document.getElementById('participant_id');
    const badge = document.getElementById('participant_badge');
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
                const participants = data.participants || data;

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
                        item.onclick = () => selectParticipant(p);
                        resultsContainer.appendChild(item);
                    });
                }
            } catch (error) {
                console.error('Search error:', error);
                resultsContainer.innerHTML = '<div class="search-no-results">Error al buscar</div>';
            }
        }, 300);
    });

    async function selectParticipant(p) {
        idInput.value = p.id;
        badgeName.textContent = p.name;
        searchInput.style.display = 'none';
        resultsContainer.style.display = 'none';
        badge.style.display = 'inline-flex';

        // Load active interchanges for this participant
        await loadActiveExchanges(p.id);
    }

    // Close dropdown
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
            resultsContainer.style.display = 'none';
        }
    });
}

/**
 * Fetch and display active exchanges for the selected participant.
 */
async function loadActiveExchanges(participantId) {
    const exchangeGroup = document.getElementById('interchange_selection_group');
    const exchangeSelect = document.getElementById('related_interchange_id');

    try {
        // Fetch where participant is giver
        const givenData = await api.getExchanges({ giver_id: participantId, limit: 50 });
        const givenExchanges = givenData.exchanges || givenData;

        // Fetch where participant is receiver
        const receivedData = await api.getExchanges({ receiver_id: participantId, limit: 50 });
        const receivedExchanges = receivedData.exchanges || receivedData;

        // Combine and de-duplicate
        const allExchanges = [...(givenExchanges || []), ...(receivedExchanges || [])];
        const uniqueExchanges = Array.from(new Map(allExchanges.map(item => [item.id, item])).values());

        if (uniqueExchanges.length > 0) {
            exchangeSelect.innerHTML = '<option value="">Selecciona un intercambio...</option>';
            uniqueExchanges.forEach(ex => {
                const opt = document.createElement('option');
                opt.value = ex.id;
                // Use a descriptive label: Date - Type: Desc
                const desc = ex.description ? (ex.description.substring(0, 30) + '...') : 'Sin descripción';
                opt.textContent = `${ex.date || 'S/F'} - ${ex.type || 'Otro'}: ${desc}`;
                exchangeSelect.appendChild(opt);
            });
            exchangeGroup.style.display = 'block';
        } else {
            exchangeGroup.style.display = 'none';
        }
    } catch (error) {
        console.error('Error loading exchanges:', error);
        exchangeGroup.style.display = 'none';
    }
}

function clearParticipant() {
    const searchInput = document.getElementById('participant_search');
    const idInput = document.getElementById('participant_id');
    const badge = document.getElementById('participant_badge');
    const exchangeGroup = document.getElementById('interchange_selection_group');

    idInput.value = '';
    searchInput.value = '';
    searchInput.style.display = 'block';
    badge.style.display = 'none';
    exchangeGroup.style.display = 'none';
    searchInput.focus();
}

function resetForm() {
    location.reload();
}
