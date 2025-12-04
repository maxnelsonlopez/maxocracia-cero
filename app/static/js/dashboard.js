/**
 * Dashboard Logic for Maxocracia Red de Apoyo
 * Handles data fetching and visualization.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Dashboard
    loadDashboardData();

    // Event Listeners
    document.getElementById('refreshBtn').addEventListener('click', loadDashboardData);
    document.getElementById('btnLogout').addEventListener('click', handleLogout);
});

async function loadDashboardData() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    updateLastUpdate();

    try {
        await Promise.all([
            fetchStats(token),
            fetchAlerts(token),
            fetchNetwork(token)
        ]);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        // Handle error (e.g., show toast)
    }
}

function updateLastUpdate() {
    const now = new Date();
    document.getElementById('lastUpdate').textContent = now.toLocaleTimeString();
}

async function fetchStats(token) {
    try {
        const response = await fetch('/forms/dashboard/stats', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error('Failed to fetch stats');

        const data = await response.json();

        // Update Overview Cards
        document.getElementById('totalParticipants').textContent = data.total_participants || 0;
        document.getElementById('totalExchanges').textContent = data.total_exchanges || 0;
        document.getElementById('totalUth').textContent = (data.total_uth || 0).toFixed(1);
        document.getElementById('networkHealth').textContent = data.network_health || '-';

        // Render Charts
        renderUrgencyChart(data.urgency_distribution || {});
        renderPriorityChart(data.followup_priorities || {});

    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

async function fetchAlerts(token) {
    try {
        const response = await fetch('/forms/dashboard/alerts', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error('Failed to fetch alerts');

        const data = await response.json();
        const alertsList = document.getElementById('alertsList');
        const alertCount = document.getElementById('alertCount');

        // Update Count
        alertCount.textContent = data.count || 0;

        // Clear List
        alertsList.innerHTML = '';

        if (!data.alerts || data.alerts.length === 0) {
            alertsList.innerHTML = '<div class="empty-state"><p>No hay alertas activas</p></div>';
            return;
        }

        // Render Alerts
        data.alerts.forEach(alert => {
            const alertEl = document.createElement('div');
            alertEl.className = 'alert-item';
            alertEl.innerHTML = `
                <div class="alert-header">
                    <span class="alert-name">${alert.name}</span>
                    <span class="alert-date">${new Date(alert.follow_up_date).toLocaleDateString()}</span>
                </div>
                <div class="alert-reason">
                    <strong>Razón:</strong> ${alert.follow_up_type.replace(/_/g, ' ')}
                </div>
                <div class="alert-actions">
                    <button class="btn-resolve" onclick="viewParticipant(${alert.participant_id})">Ver Detalles</button>
                </div>
            `;
            alertsList.appendChild(alertEl);
        });

    } catch (error) {
        console.error('Error fetching alerts:', error);
    }
}

async function fetchNetwork(token) {
    try {
        const response = await fetch('/forms/dashboard/network', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error('Failed to fetch network data');

        const data = await response.json();

        renderTable('topGiversTable', data.top_givers, ['user_id', 'count']);
        renderTable('topReceiversTable', data.top_receivers, ['user_id', 'count']);

        // Hub nodes need special handling for 2 columns
        const hubBody = document.querySelector('#hubNodesTable tbody');
        hubBody.innerHTML = '';
        if (data.hub_nodes) {
            data.hub_nodes.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>${item.user_id}</td><td>${item.gives} / ${item.receives}</td>`;
                hubBody.appendChild(row);
            });
        }

    } catch (error) {
        console.error('Error fetching network:', error);
    }
}

// Chart Instances
let urgencyChartInstance = null;
let priorityChartInstance = null;

function renderUrgencyChart(distribution) {
    const ctx = document.getElementById('urgencyChart').getContext('2d');

    if (urgencyChartInstance) urgencyChartInstance.destroy();

    const labels = Object.keys(distribution);
    const data = Object.values(distribution);

    // Colors matching urgency levels
    const colors = {
        'Alta': '#ef4444',
        'Media': '#f59e0b',
        'Baja': '#10b981'
    };

    const bgColors = labels.map(l => colors[l] || '#cbd5e1');

    urgencyChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: bgColors,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

function renderPriorityChart(priorities) {
    const ctx = document.getElementById('priorityChart').getContext('2d');

    if (priorityChartInstance) priorityChartInstance.destroy();

    const labels = Object.keys(priorities);
    const data = Object.values(priorities);

    // Colors matching priority levels
    const colors = {
        'high': '#ef4444',
        'medium': '#f59e0b',
        'low': '#10b981',
        'closed': '#6b7280'
    };

    const bgColors = labels.map(l => colors[l] || '#cbd5e1');

    priorityChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Seguimientos',
                data: data,
                backgroundColor: bgColors,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, ticks: { precision: 0 } }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function renderTable(tableId, data, columns) {
    const tbody = document.querySelector(`#${tableId} tbody`);
    tbody.innerHTML = '';

    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="2" style="text-align:center; color:#999;">Sin datos</td></tr>';
        return;
    }

    data.forEach(item => {
        const row = document.createElement('tr');
        let html = '';
        columns.forEach(col => {
            html += `<td>${item[col]}</td>`;
        });
        row.innerHTML = html;
        tbody.appendChild(row);
    });
}

function handleLogout() {
    localStorage.removeItem('token');
    window.location.href = 'index.html';
}

function viewParticipant(id) {
    // In a real app, this would navigate to a detail view
    alert(`Ver detalles del participante ID: ${id}`);
}
