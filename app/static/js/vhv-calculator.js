// VHV Calculator JavaScript
// Handles form submission, API calls, and visualization

// State
let currentParameters = null;
let savedProducts = [];
let caseStudies = [];
let vhvChart = null;

// API Base URL
const API_BASE = '';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeForm();
    loadParameters();
    loadCaseStudies();
    loadSavedProducts();
});

// Tab Navigation
function initializeTabs() {
    const tabs = document.querySelectorAll('.vhv-tab');
    const tabContents = document.querySelectorAll('.vhv-tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;

            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Update active content
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === `${targetTab}-tab`) {
                    content.classList.add('active');
                }
            });
        });
    });
}

// Form Initialization
function initializeForm() {
    const form = document.getElementById('vhv-form');
    const loadExampleBtn = document.getElementById('load-example');
    const saveProductBtn = document.getElementById('save-product');

    form.addEventListener('submit', handleFormSubmit);
    loadExampleBtn.addEventListener('click', loadExampleData);
    saveProductBtn.addEventListener('click', saveProduct);
}

// Load Example Data (Huevo Ético)
function loadExampleData() {
    document.getElementById('product-name').value = 'Huevo Ético';
    document.getElementById('t-direct').value = '1.5';
    document.getElementById('t-inherited').value = '0.5';
    document.getElementById('t-future').value = '0.1';
    document.getElementById('v-organisms').value = '0.001';
    document.getElementById('v-consciousness').value = '0.9';
    document.getElementById('v-suffering').value = '1.1';
    document.getElementById('v-abundance').value = '0.0006';
    document.getElementById('v-rarity').value = '1.0';
    document.getElementById('r-minerals').value = '0.1';
    document.getElementById('r-water').value = '0.05';
    document.getElementById('r-petroleum').value = '0.0';
    document.getElementById('r-land').value = '0.0';
    document.getElementById('r-frg').value = '1.0';
    document.getElementById('r-cs').value = '1.0';
}

// Handle Form Submit
async function handleFormSubmit(e) {
    e.preventDefault();

    const formData = {
        name: document.getElementById('product-name').value,
        t_direct_hours: parseFloat(document.getElementById('t-direct').value),
        t_inherited_hours: parseFloat(document.getElementById('t-inherited').value),
        t_future_hours: parseFloat(document.getElementById('t-future').value),
        v_organisms_affected: parseFloat(document.getElementById('v-organisms').value),
        v_consciousness_factor: parseFloat(document.getElementById('v-consciousness').value),
        v_suffering_factor: parseFloat(document.getElementById('v-suffering').value),
        v_abundance_factor: parseFloat(document.getElementById('v-abundance').value),
        v_rarity_factor: parseFloat(document.getElementById('v-rarity').value),
        r_minerals_kg: parseFloat(document.getElementById('r-minerals').value),
        r_water_m3: parseFloat(document.getElementById('r-water').value),
        r_petroleum_l: parseFloat(document.getElementById('r-petroleum').value),
        r_land_hectares: parseFloat(document.getElementById('r-land').value),
        r_frg_factor: parseFloat(document.getElementById('r-frg').value),
        r_cs_factor: parseFloat(document.getElementById('r-cs').value),
        save: false
    };

    try {
        const response = await fetch(`${API_BASE}/vhv/calculate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al calcular VHV');
        }

        const result = await response.json();
        displayResults(result);
    } catch (error) {
        alert(`Error: ${error.message}`);
        console.error('Error calculating VHV:', error);
    }
}

// Display Results
function displayResults(result) {
    // Show results container
    document.getElementById('results-container').style.display = 'block';
    document.getElementById('results-placeholder').style.display = 'none';

    // Update Maxo price
    document.getElementById('maxo-price').textContent = result.maxo_price.toFixed(2);

    // Update VHV components
    document.getElementById('vhv-t').textContent = result.vhv.T.toFixed(4);
    document.getElementById('vhv-v').textContent = result.vhv.V.toFixed(6);
    document.getElementById('vhv-r').textContent = result.vhv.R.toFixed(4);

    // Update contribution breakdown
    document.getElementById('contrib-t').textContent = result.breakdown.time_contribution.toFixed(2) + ' Ⓜ';
    document.getElementById('contrib-v').textContent = result.breakdown.life_contribution.toFixed(2) + ' Ⓜ';
    document.getElementById('contrib-r').textContent = result.breakdown.resource_contribution.toFixed(2) + ' Ⓜ';

    // Update chart
    updateChart(result);

    // Add fade-in animation
    document.getElementById('results-container').classList.add('vhv-fade-in');

    // Store result for saving
    window.lastCalculation = result;
}

// Update Chart
function updateChart(result) {
    const ctx = document.getElementById('vhv-chart').getContext('2d');

    // Destroy existing chart if any
    if (vhvChart) {
        vhvChart.destroy();
    }

    vhvChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Tiempo (T)', 'Vida (V)', 'Recursos (R)'],
            datasets: [{
                data: [
                    result.breakdown.time_contribution,
                    result.breakdown.life_contribution,
                    result.breakdown.resource_contribution
                ],
                backgroundColor: [
                    'rgba(255, 107, 107, 0.8)',
                    'rgba(46, 204, 113, 0.8)',
                    'rgba(139, 69, 19, 0.8)'
                ],
                borderColor: [
                    'rgba(255, 107, 107, 1)',
                    'rgba(46, 204, 113, 1)',
                    'rgba(139, 69, 19, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            size: 14,
                            family: 'system-ui'
                        },
                        padding: 15
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value.toFixed(2)} Ⓜ (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Save Product
async function saveProduct() {
    if (!window.lastCalculation) {
        alert('Primero calcula el VHV de un producto');
        return;
    }

    const formData = {
        name: document.getElementById('product-name').value,
        t_direct_hours: parseFloat(document.getElementById('t-direct').value),
        t_inherited_hours: parseFloat(document.getElementById('t-inherited').value),
        t_future_hours: parseFloat(document.getElementById('t-future').value),
        v_organisms_affected: parseFloat(document.getElementById('v-organisms').value),
        v_consciousness_factor: parseFloat(document.getElementById('v-consciousness').value),
        v_suffering_factor: parseFloat(document.getElementById('v-suffering').value),
        v_abundance_factor: parseFloat(document.getElementById('v-abundance').value),
        v_rarity_factor: parseFloat(document.getElementById('v-rarity').value),
        r_minerals_kg: parseFloat(document.getElementById('r-minerals').value),
        r_water_m3: parseFloat(document.getElementById('r-water').value),
        r_petroleum_l: parseFloat(document.getElementById('r-petroleum').value),
        r_land_hectares: parseFloat(document.getElementById('r-land').value),
        r_frg_factor: parseFloat(document.getElementById('r-frg').value),
        r_cs_factor: parseFloat(document.getElementById('r-cs').value),
        save: true
    };

    try {
        const response = await fetch(`${API_BASE}/vhv/calculate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error('Error al guardar producto');
        }

        const result = await response.json();
        alert(`Producto "${formData.name}" guardado exitosamente con ID: ${result.product_id}`);
        loadSavedProducts(); // Refresh product list
    } catch (error) {
        alert(`Error: ${error.message}`);
        console.error('Error saving product:', error);
    }
}

// Load Parameters
async function loadParameters() {
    try {
        const response = await fetch(`${API_BASE}/vhv/parameters`);
        if (!response.ok) throw new Error('Error loading parameters');

        currentParameters = await response.json();
        displayParameters();
    } catch (error) {
        console.error('Error loading parameters:', error);
    }
}

// Display Parameters
function displayParameters() {
    if (!currentParameters) return;

    const container = document.getElementById('parameters-container');
    container.innerHTML = `
    <div class="vhv-grid">
      <div class="vhv-card">
        <h3 class="vhv-card-title">Parámetros Actuales</h3>
        <div style="display: grid; gap: var(--space-md); margin-top: var(--space-md);">
          <div>
            <strong>α (Alpha)</strong> - Peso del Tiempo
            <div style="font-size: var(--font-size-2xl); color: var(--color-time-end);">${currentParameters.alpha}</div>
            <div class="vhv-axiom-badge">Axioma: α > 0 ✓</div>
          </div>
          <div>
            <strong>β (Beta)</strong> - Peso de la Vida
            <div style="font-size: var(--font-size-2xl); color: var(--color-life-primary);">${currentParameters.beta}</div>
            <div class="vhv-axiom-badge">Axioma: β > 0 ✓</div>
          </div>
          <div>
            <strong>γ (Gamma)</strong> - Exponente de Aversión al Sufrimiento
            <div style="font-size: var(--font-size-2xl); color: var(--color-life-warning);">${currentParameters.gamma}</div>
            <div class="vhv-axiom-badge">Axioma: γ ≥ 1 ✓</div>
          </div>
          <div>
            <strong>δ (Delta)</strong> - Peso de Recursos
            <div style="font-size: var(--font-size-2xl); color: var(--color-resource-primary);">${currentParameters.delta}</div>
            <div class="vhv-axiom-badge">Axioma: δ ≥ 0 ✓</div>
          </div>
        </div>
        ${currentParameters.notes ? `<p style="margin-top: var(--space-md); color: var(--color-text-secondary);"><em>${currentParameters.notes}</em></p>` : ''}
        <p style="margin-top: var(--space-lg); color: var(--color-text-secondary); font-size: var(--font-size-sm);">
          <strong>Nota:</strong> La actualización de parámetros requiere autenticación y se realiza a través del API.
        </p>
      </div>
    </div>
  `;
}

// Load Case Studies
async function loadCaseStudies() {
    try {
        const response = await fetch(`${API_BASE}/vhv/case-studies`);
        if (!response.ok) throw new Error('Error loading case studies');

        caseStudies = await response.json();
        displayCaseStudies();
    } catch (error) {
        console.error('Error loading case studies:', error);
        document.getElementById('case-studies-container').innerHTML =
            '<p style="text-align: center; color: var(--color-life-danger);">Error al cargar casos de estudio</p>';
    }
}

// Display Case Studies
function displayCaseStudies() {
    const container = document.getElementById('case-studies-container');

    if (caseStudies.length === 0) {
        container.innerHTML = '<p style="text-align: center;">No hay casos de estudio disponibles</p>';
        return;
    }

    container.innerHTML = `
    <div class="vhv-comparison">
      ${caseStudies.map(study => `
        <div class="vhv-card vhv-comparison-card ${study.name.includes('Ético') ? 'winner' : ''}">
          ${study.name.includes('Ético') ? '<div class="vhv-comparison-badge">✓ Más Ético</div>' : ''}
          <h3 class="vhv-card-title">${study.name}</h3>
          <p class="vhv-card-subtitle">${study.description || ''}</p>
          
          <div class="vhv-result" style="margin: var(--space-md) 0;">
            <div class="vhv-result-label">Precio Maxo</div>
            <div class="vhv-result-value" style="font-size: var(--font-size-2xl);">
              ${study.maxo_price.toFixed(2)} Ⓜ
            </div>
          </div>

          <div class="vhv-result-breakdown">
            <div class="vhv-breakdown-item">
              <div class="vhv-breakdown-label"><span class="vhv-component-badge time">T</span></div>
              <div class="vhv-breakdown-value">${study.vhv.T.toFixed(2)}</div>
            </div>
            <div class="vhv-breakdown-item">
              <div class="vhv-breakdown-label"><span class="vhv-component-badge life">V</span></div>
              <div class="vhv-breakdown-value">${study.vhv.V.toFixed(4)}</div>
            </div>
            <div class="vhv-breakdown-item">
              <div class="vhv-breakdown-label"><span class="vhv-component-badge resource">R</span></div>
              <div class="vhv-breakdown-value">${study.vhv.R.toFixed(2)}</div>
            </div>
          </div>

          <button class="vhv-btn vhv-btn-secondary" style="width: 100%; margin-top: var(--space-md);" onclick="loadCaseStudy('${study.name}')">
            Cargar en Calculadora
          </button>
        </div>
      `).join('')}
    </div>
  `;
}

// Load Case Study into Form
function loadCaseStudy(name) {
    const study = caseStudies.find(s => s.name === name);
    if (!study) return;

    // Switch to calculator tab
    document.querySelector('.vhv-tab[data-tab="calculator"]').click();

    // Populate form
    document.getElementById('product-name').value = study.name;
    document.getElementById('t-direct').value = study.data.t_direct_hours || 0;
    document.getElementById('t-inherited').value = study.data.t_inherited_hours || 0;
    document.getElementById('t-future').value = study.data.t_future_hours || 0;
    document.getElementById('v-organisms').value = study.data.v_organisms_affected || 0;
    document.getElementById('v-consciousness').value = study.data.v_consciousness_factor || 0;
    document.getElementById('v-suffering').value = study.data.v_suffering_factor || 1;
    document.getElementById('v-abundance').value = study.data.v_abundance_factor || 1;
    document.getElementById('v-rarity').value = study.data.v_rarity_factor || 1;
    document.getElementById('r-minerals').value = study.data.r_minerals_kg || 0;
    document.getElementById('r-water').value = study.data.r_water_m3 || 0;
    document.getElementById('r-petroleum').value = study.data.r_petroleum_l || 0;
    document.getElementById('r-land').value = study.data.r_land_hectares || 0;
    document.getElementById('r-frg').value = study.data.r_frg_factor || 1;
    document.getElementById('r-cs').value = study.data.r_cs_factor || 1;

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Load Saved Products
async function loadSavedProducts() {
    try {
        const response = await fetch(`${API_BASE}/vhv/products`);
        if (!response.ok) throw new Error('Error loading products');

        savedProducts = await response.json();
        displaySavedProducts();
    } catch (error) {
        console.error('Error loading products:', error);
        document.getElementById('comparison-container').innerHTML =
            '<p style="text-align: center; color: var(--color-text-secondary);">No hay productos guardados aún</p>';
    }
}

// Display Saved Products for Comparison
function displaySavedProducts() {
    const container = document.getElementById('comparison-container');

    if (savedProducts.length === 0) {
        container.innerHTML = '<p style="text-align: center;">No hay productos guardados. Calcula y guarda productos primero.</p>';
        return;
    }

    // Sort by maxo_price
    const sorted = [...savedProducts].sort((a, b) => a.maxo_price - b.maxo_price);

    container.innerHTML = `
    <div class="vhv-comparison">
      ${sorted.map((product, index) => `
        <div class="vhv-card vhv-comparison-card ${index === 0 ? 'winner' : ''}">
          ${index === 0 ? '<div class="vhv-comparison-badge">✓ Menor Costo Vital</div>' : ''}
          <h3 class="vhv-card-title">${product.name}</h3>
          ${product.category ? `<p class="vhv-card-subtitle">${product.category}</p>` : ''}
          
          <div class="vhv-result" style="margin: var(--space-md) 0;">
            <div class="vhv-result-label">Precio Maxo</div>
            <div class="vhv-result-value" style="font-size: var(--font-size-2xl);">
              ${product.maxo_price.toFixed(2)} Ⓜ
            </div>
          </div>

          <div class="vhv-result-breakdown">
            <div class="vhv-breakdown-item">
              <div class="vhv-breakdown-label"><span class="vhv-component-badge time">T</span></div>
              <div class="vhv-breakdown-value">${(product.t_direct_hours + product.t_inherited_hours + product.t_future_hours).toFixed(2)}</div>
            </div>
            <div class="vhv-breakdown-item">
              <div class="vhv-breakdown-label"><span class="vhv-component-badge life">V</span></div>
              <div class="vhv-breakdown-value">${(product.v_organisms_affected * product.v_consciousness_factor * Math.pow(product.v_suffering_factor, 1) * product.v_abundance_factor * product.v_rarity_factor).toFixed(4)}</div>
            </div>
            <div class="vhv-breakdown-item">
              <div class="vhv-breakdown-label"><span class="vhv-component-badge resource">R</span></div>
              <div class="vhv-breakdown-value">${((product.r_minerals_kg + product.r_water_m3 + product.r_petroleum_l + product.r_land_hectares) * product.r_frg_factor * product.r_cs_factor).toFixed(2)}</div>
            </div>
          </div>
        </div>
      `).join('')}
    </div>
  `;
}
