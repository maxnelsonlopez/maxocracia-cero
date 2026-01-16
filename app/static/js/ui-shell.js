/**
 * UI Shell - Unified Navigation & Auth State
 */

document.addEventListener('DOMContentLoaded', () => {
    initShell();
});

function initShell() {
    const container = document.querySelector('.dashboard-container') || document.querySelector('.forms-container') || document.querySelector('.vhv-container') || document.querySelector('.dashboard-main');

    if (!container) return;

    // Create sidebar if not exists
    if (!document.querySelector('.dashboard-sidebar')) {
        const sidebar = createSidebar();
        document.body.prepend(sidebar);

        // Adjust main padding
        const main = document.querySelector('.dashboard-main') || container;
        if (main) {
            main.style.marginLeft = '280px';
        }
    }

    updateActiveNavItem();
    initAuthObserver();
    initTheme();
}

function createSidebar() {
    const sidebar = document.createElement('aside');
    sidebar.className = 'dashboard-sidebar';
    sidebar.innerHTML = `
        <div class="sidebar-header">
            <div class="logo-area">
                <h2>Maxocracia</h2>
                <span class="badge-beta">BETA</span>
            </div>
            <button id="themeToggle" class="btn-icon" title="Cambiar Tema">
                <span class="icon-theme">🌓</span>
            </button>
        </div>

        <nav class="sidebar-nav">
            <a href="dashboard.html" class="nav-item" data-nav="dashboard">
                <span class="icon">📊</span> Dashboard
            </a>
            <a href="form-cero.html" class="nav-item" data-nav="form-cero">
                <span class="icon">📝</span> Inscripción
            </a>
            <a href="form-exchange.html" class="nav-item" data-nav="form-exchange">
                <span class="icon">🤝</span> Intercambios
            </a>
            <a href="form-followup.html" class="nav-item" data-nav="form-followup">
                <span class="icon">📋</span> Seguimiento
            </a>
            <a href="vhv-calculator.html" class="nav-item" data-nav="vhv-calculator">
                <span class="icon">🧮</span> Calculadora VHV
            </a>
        </nav>

        <div class="sidebar-footer">
            <div class="user-info" id="userInfo">
                <div class="avatar">👤</div>
                <div class="details">
                    <span class="name" id="shellUserName">Usuario</span>
                    <span class="role" id="shellUserRole">Facilitador</span>
                </div>
            </div>
            <button id="btnLogoutShell" class="btn-logout">Cerrar Sesión</button>
        </div>
    `;

    // Event Listeners
    sidebar.querySelector('#btnLogoutShell').addEventListener('click', () => {
        if (typeof api !== 'undefined') {
            api.logout();
            window.location.href = 'index.html';
        }
    });

    sidebar.querySelector('#themeToggle').addEventListener('click', toggleTheme);

    return sidebar;
}

function updateActiveNavItem() {
    const path = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-item');

    navItems.forEach(item => {
        item.classList.remove('active');
        const href = item.getAttribute('href');
        if (path.endsWith(href) || (href === 'dashboard.html' && path === '/')) {
            item.classList.add('active');
        }
    });
}

function initAuthObserver() {
    if (typeof api !== 'undefined' && api.isAuthenticated()) {
        api.getProfile().then(user => {
            if (user) {
                const nameEl = document.getElementById('shellUserName');
                const roleEl = document.getElementById('shellUserRole');
                if (nameEl) nameEl.textContent = user.name || user.email;
                if (roleEl && user.is_admin) roleEl.textContent = 'Administrador';
            }
        }).catch(err => {
            console.error('Error fetching profile for shell:', err);
        });
    }
}

// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('maxo-theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = savedTheme || (systemPrefersDark ? 'dark' : 'light');
    applyTheme(theme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.dataset.theme || 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
    localStorage.setItem('maxo-theme', newTheme);
}

function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    const icon = document.querySelector('.icon-theme');
    if (icon) {
        icon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}
