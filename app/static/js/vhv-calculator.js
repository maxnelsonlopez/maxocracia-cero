// ============================================
// State
// ============================================
let currentParameters = null;
let savedProducts = [];
let caseStudies = [];
let vhvChart = null;

// ============================================
// Initialize on page load
// ============================================
document.addEventListener('DOMContentLoaded', () => {
  initializeTabs();
  initializeForm();
  loadParameters();
  loadCaseStudies();
  loadSavedProducts();
});

// ============================================
// Tab Navigation with ARIA Support
// ============================================
function initializeTabs() {
  const tabs = document.querySelectorAll('.vhv-tab');
  const tabContents = document.querySelectorAll('.vhv-tab-content');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetTab = tab.dataset.tab;

      // Update ARIA states
      tabs.forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');

      // Update active content with animation
      tabContents.forEach(content => {
        content.classList.remove('active');
        if (content.id === `${targetTab}-tab`) {
          content.classList.add('active');
          content.classList.add('vhv-fade-in');
          // Remove animation class after it completes
          setTimeout(() => content.classList.remove('vhv-fade-in'), 250);
        }
      });
    });

    // Keyboard navigation for tabs
    tab.addEventListener('keydown', (e) => {
      const tabsArray = Array.from(tabs);
      const currentIndex = tabsArray.indexOf(tab);
      let newIndex;

      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault();
        newIndex = (currentIndex + 1) % tabsArray.length;
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        newIndex = (currentIndex - 1 + tabsArray.length) % tabsArray.length;
      } else if (e.key === 'Home') {
        e.preventDefault();
        newIndex = 0;
      } else if (e.key === 'End') {
        e.preventDefault();
        newIndex = tabsArray.length - 1;
      }

      if (newIndex !== undefined) {
        tabsArray[newIndex].focus();
        tabsArray[newIndex].click();
      }
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

// ============================================
// Display Results with Animations
// ============================================
function displayResults(result) {
  // Store for save functionality
  window.lastCalculation = result;

  // Get elements
  const resultsContainer = document.getElementById('results-container');
  const placeholder = document.getElementById('results-placeholder');
  const resultBox = document.querySelector('.vhv-result');
  const resultValue = document.querySelector('.vhv-result-value');

  // Show results, hide placeholder
  resultsContainer.style.display = 'block';
  placeholder.style.display = 'none';

  // Add animation classes
  if (resultBox) {
    resultBox.classList.remove('animate');
    void resultBox.offsetWidth; // Trigger reflow
    resultBox.classList.add('animate');
  }

  // Animate the price counter
  const finalPrice = result.maxo_price;
  animateCounter('maxo-price', 0, finalPrice, 800);

  // Update VHV components
  document.getElementById('vhv-t').textContent = result.vhv.T.toFixed(4);
  document.getElementById('vhv-v').textContent = result.vhv.V.toFixed(4);
  document.getElementById('vhv-r').textContent = result.vhv.R.toFixed(4);

  // Update contributions with animation
  const contributions = [
    { id: 'contrib-t', value: result.breakdown.time_contribution },
    { id: 'contrib-v', value: result.breakdown.life_contribution },
    { id: 'contrib-r', value: result.breakdown.resource_contribution }
  ];

  contributions.forEach((contrib, index) => {
    setTimeout(() => {
      const el = document.getElementById(contrib.id);
      el.textContent = `${contrib.value.toFixed(2)} Ⓜ`;
      el.classList.add('vhv-scale-in');
      setTimeout(() => el.classList.remove('vhv-scale-in'), 250);
    }, index * 100);
  });

  // Update chart
  updateChart(result);

  // Announce for screen readers
  announceResult(result.maxo_price);
}

// Animated counter effect
function animateCounter(elementId, start, end, duration) {
  const element = document.getElementById(elementId);
  const startTime = performance.now();
  const diff = end - start;

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);

    // Easing function (ease-out cubic)
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = start + diff * eased;

    element.textContent = current.toFixed(2);

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

// Announce result for screen readers
function announceResult(price) {
  let announcer = document.getElementById('result-announcer');
  if (!announcer) {
    announcer = document.createElement('div');
    announcer.id = 'result-announcer';
    announcer.setAttribute('aria-live', 'assertive');
    announcer.setAttribute('aria-atomic', 'true');
    announcer.className = 'sr-only';
    document.body.appendChild(announcer);
  }
  announcer.textContent = `Cálculo completado. Precio en Maxos: ${price.toFixed(2)}`;
}

// ============================================
// Chart Update
// ============================================
function updateChart(result) {
  const ctx = document.getElementById('vhv-chart');
  if (!ctx) return;

  const chartData = {
    labels: ['Tiempo (T)', 'Vida (V)', 'Recursos (R)'],
    datasets: [{
      label: 'Contribución al Precio (Maxos)',
      data: [
        result.breakdown.time_contribution,
        result.breakdown.life_contribution,
        result.breakdown.resource_contribution
      ],
      backgroundColor: [
        'rgba(255, 107, 107, 0.8)',  // Time - coral
        'rgba(46, 204, 113, 0.8)',   // Life - green
        'rgba(139, 69, 19, 0.8)'     // Resources - brown
      ],
      borderColor: [
        'rgba(255, 107, 107, 1)',
        'rgba(46, 204, 113, 1)',
        'rgba(139, 69, 19, 1)'
      ],
      borderWidth: 2,
      borderRadius: 8
    }]
  };

  // Destroy existing chart if it exists
  if (vhvChart) {
    vhvChart.destroy();
  }

  // Create new chart with animation
  vhvChart = new Chart(ctx, {
    type: 'bar',
    data: chartData,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 800,
        easing: 'easeOutQuart'
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleFont: { size: 14 },
          bodyFont: { size: 13 },
          padding: 12,
          cornerRadius: 8,
          callbacks: {
            label: function (context) {
              return `${context.parsed.y.toFixed(2)} Maxos`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(0, 0, 0, 0.05)'
          },
          ticks: {
            callback: function (value) {
              return value + ' Ⓜ';
            }
          }
        },
        x: {
          grid: {
            display: false
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
