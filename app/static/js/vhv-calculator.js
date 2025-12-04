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
    const result = await api.calculateVHV(formData);
    displayResults(result);
  } catch (error) {
    alert(`Error: ${error.message}`);
    console.error('Error calculating VHV:', error);
  }
}

// ... (displayResults and updateChart remain unchanged) ...

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
    const result = await api.calculateVHV(formData);
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
    currentParameters = await api.getVHVParameters();
    displayParameters();
  } catch (error) {
    console.error('Error loading parameters:', error);
  }
}

// ... (displayParameters remains unchanged) ...

// Load Case Studies
async function loadCaseStudies() {
  try {
    const data = await api.getVHVCaseStudies();
    caseStudies = data.case_studies;
    displayCaseStudies();
  } catch (error) {
    console.error('Error loading case studies:', error);
    document.getElementById('case-studies-container').innerHTML =
      '<p style="text-align: center; color: var(--color-life-danger);">Error al cargar casos de estudio</p>';
  }
}

// ... (displayCaseStudies and loadCaseStudy remain unchanged) ...

// Load Saved Products
async function loadSavedProducts() {
  try {
    const data = await api.getVHVProducts();
    savedProducts = data.products;
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
