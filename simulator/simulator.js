// Core parameters for the Maxo valuation function
const params = {
    alpha: 0.25, // Time weight
    beta: 0.50,  // Life weight
    delta: 0.20, // Resource weight
    frg: 1.0,    // Factor de Rareza Geográfica (default)
    cs: 1.0      // Criticidad Sistémica (default)
};

// DOM Elements
const inputs = {
    time: document.getElementById('time-input'),
    life: document.getElementById('life-input'),
    resource: document.getElementById('resource-input'),
    gamma: document.getElementById('gamma-input')
};

const displays = {
    time: document.getElementById('time-val'),
    life: document.getElementById('life-val'),
    resource: document.getElementById('resource-val'),
    gamma: document.getElementById('gamma-val'),
    price: document.getElementById('price-result'),
    penalty: document.getElementById('penalty-val'),
    coop: document.getElementById('coop-val')
};

// Mathematical Engine
function calculatePrice() {
    const t = parseFloat(inputs.time.value);
    const v = parseFloat(inputs.life.value);
    const r = parseFloat(inputs.resource.value);
    const gamma = parseFloat(inputs.gamma.value);

    // Update value displays
    displays.time.innerText = `${t.toFixed(1)}h`;
    displays.life.innerText = `${v.toFixed(1)}x`;
    displays.resource.innerText = `${r.toFixed(1)}x`;
    displays.gamma.innerText = `${gamma.toFixed(1)}`;

    // Formula: Price = α·T + β·V^γ + δ·R·(FRG × CS)
    const timeComponent = params.alpha * t;
    const lifeComponent = params.beta * Math.pow(v, gamma);
    const resourceComponent = params.delta * r * (params.frg * params.cs);

    const price = timeComponent + lifeComponent + resourceComponent;

    // Animation effect for price
    animatePrice(price);

    // Calculate Ethics Penalty (how much V^gamma adds vs shared base)
    const baseLife = params.beta * v; // Linear part
    const penaltyRatio = lifeComponent > 0 ? ((lifeComponent - baseLife) / price) * 100 : 0;
    displays.penalty.innerText = `+${Math.max(0, penaltyRatio).toFixed(0)}%`;

    // Viability Logic
    if (v > 3.0 || price > 5.0) {
        displays.coop.innerText = "Baja";
        displays.coop.parentElement.style.color = "var(--danger)";
    } else if (v < 1.0) {
        displays.coop.innerText = "Óptima";
        displays.coop.parentElement.style.color = "var(--success)";
    } else {
        displays.coop.innerText = "Media";
        displays.coop.parentElement.style.color = "var(--primary-light)";
    }
}

let currentDisplayPrice = 0;
function animatePrice(target) {
    const step = (target - currentDisplayPrice) / 10;
    const interval = setInterval(() => {
        currentDisplayPrice += step;
        displays.price.innerText = currentDisplayPrice.toFixed(2);
        if (Math.abs(currentDisplayPrice - target) < 0.01) {
            currentDisplayPrice = target;
            displays.price.innerText = target.toFixed(2);
            clearInterval(interval);
        }
    }, 30);
}

// Scenarios
const scenarios = {
    'egg-ind': { t: 0.2, v: 4.5, r: 2.5, g: 1.8 },
    'egg-eth': { t: 0.8, v: 0.2, r: 0.5, g: 1.8 },
    'coop-dev': { t: 3.0, v: 0.5, r: 1.0, g: 1.5 }
};

window.loadScenario = function (scKey) {
    const sc = scenarios[scKey];
    if (!sc) return;

    inputs.time.value = sc.t;
    inputs.life.value = sc.v;
    inputs.resource.value = sc.r;
    inputs.gamma.value = sc.g;

    calculatePrice();
};

// Event Listeners
Object.values(inputs).forEach(input => {
    input.addEventListener('input', calculatePrice);
});

// Initial run
calculatePrice();
console.log("Nexus Simulator Engine initialized.");
