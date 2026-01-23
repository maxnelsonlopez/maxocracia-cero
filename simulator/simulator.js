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
    coop: document.getElementById('coop-val'),
    // NEW Elements
    gammaWell: document.getElementById('gamma-well-val'),
    wellnessBar: document.getElementById('wellness-bar'),
    status: document.getElementById('contract-status'),
    oracleToggle: document.getElementById('oracle-mode-toggle')
};

// State
let isOracleMode = false;

// Mathematical Engine
function calculatePrice() {
    const t = parseFloat(inputs.time.value);
    let v = parseFloat(inputs.life.value);
    const r = parseFloat(inputs.resource.value);

    // Dynamic Oracle Logic: If enabled, Gamma Exponent adjusts based on Suffering (V)
    if (isOracleMode) {
        // Enhanced Oracle Rule: Non-linear scaling of gamma based on suffering
        // More aggressive scaling for higher suffering values
        let targetGamma = 1.0; // Base value for V <= 0.5
        
        if (v > 0.5) {
            // Cubic scaling for V > 0.5 to make high suffering extremely costly
            const normalizedV = (v - 0.5) / 4.5; // Normalize to 0-1 range for V=0.5-5.0
            targetGamma = 1.0 + Math.pow(normalizedV * 4, 2); // Quadratic scaling
        }
        
        // Cap gamma between 1.0 and 5.0
        targetGamma = Math.max(1.0, Math.min(5.0, targetGamma));

        // Update input visually and value
        inputs.gamma.value = targetGamma.toFixed(1);
        inputs.gamma.classList.add('slider-active-anim');
        
        // Add visual feedback when oracle adjusts gamma
        const gammaDisplay = document.getElementById('gamma-val');
        gammaDisplay.classList.add('pulse-animation');
        setTimeout(() => gammaDisplay.classList.remove('pulse-animation'), 500);
    } else {
        inputs.gamma.classList.remove('slider-active-anim');
    }

    const gammaExponent = parseFloat(inputs.gamma.value);

    // Update value displays
    displays.time.innerText = `${t.toFixed(1)}h`;
    displays.life.innerText = `${v.toFixed(1)}x`;
    displays.resource.innerText = `${r.toFixed(1)}x`;
    displays.gamma.innerText = `${gammaExponent.toFixed(1)}`;

    // Formula: Price = α·T + β·V^γ + δ·R·(FRG × CS)
    const timeComponent = params.alpha * t;
    const lifeComponent = params.beta * Math.pow(v, gammaExponent);
    const resourceComponent = params.delta * r * (params.frg * params.cs);

    const price = timeComponent + lifeComponent + resourceComponent;

    // Animation effect for price
    animatePrice(price);

    // Calculate Ethics Penalty (how much V^gamma adds vs shared base)
    const baseLife = params.beta * v; // Linear part
    const penaltyRatio = lifeComponent > 0 ? ((lifeComponent - baseLife) / price) * 100 : 0;
    displays.penalty.innerText = `+${Math.max(0, penaltyRatio).toFixed(0)}%`;

    // --- NEW: Participant Wellness & Contract Status Logic ---
    // Enhanced Wellness Index Calculation (0.0-2.0)
    // Non-linear model that better reflects real-world impact
    let wellnessIndex;
    
    if (v <= 0.5) {
        // Flourishing zone: Small positive values slightly boost wellness
        wellnessIndex = 1.0 + (0.5 - v) * 1.0; // 1.0 to 1.5 range
    } else if (v <= 2.0) {
        // Neutral to concerning: Linear decrease
        wellnessIndex = 1.0 - ((v - 0.5) * 0.33);
    } else {
        // High suffering: Steeper decline
        const excess = v - 2.0;
        wellnessIndex = Math.max(0, 0.5 - (excess * 0.2));
    }
    
    // Apply non-linear scaling to make extreme values more impactful
    wellnessIndex = Math.max(0, Math.min(2.0, wellnessIndex));
    
    // Add small random fluctuation to simulate real-world variability
    wellnessIndex += (Math.random() - 0.5) * 0.02;
    wellnessIndex = Math.max(0, Math.min(2.0, wellnessIndex));

    // Update Wellness Visuals
    displays.gammaWell.innerText = wellnessIndex.toFixed(2);
    const wellnessPercent = Math.min(100, (wellnessIndex / 1.5) * 100);
    displays.wellnessBar.style.width = `${wellnessPercent}%`;

    // Color coding for Wellness
    if (wellnessIndex >= 1.0) {
        displays.gammaWell.style.color = "var(--success)";
        displays.wellnessBar.style.background = "var(--success)";
    } else if (wellnessIndex >= 0.8) {
        displays.gammaWell.style.color = "#f59e0b"; // Warning
        displays.wellnessBar.style.background = "#f59e0b";
    } else {
        displays.gammaWell.style.color = "var(--danger)";
        displays.wellnessBar.style.background = "var(--danger)";
    }

    // Update MaxoContract Status
    updateContractStatus(wellnessIndex);

    // Equity Dashboard Logic (Modelo de Tres Cuentas)
    const totalEffort = t * (1 + v * 0.5);
    const cdd = (totalEffort * 0.4).toFixed(1); // Contribución Doméstica
    const ceh = (price * 0.6).toFixed(1);       // Contribución Económica
    const ted = (Math.max(0, 24 - t - 8)).toFixed(1); // Tiempo libre

    document.getElementById('cdd-val').innerText = cdd;
    document.getElementById('ceh-val').innerText = ceh;
    document.getElementById('ted-val').innerText = ted;

    updateWisdom(v, price);
    updateViability(v, price);
}

function updateContractStatus(wellnessIndex) {
    displays.status.className = "status-panel"; // Reset

    if (wellnessIndex >= 1.0) {
        displays.status.innerText = "ESTADO: ACTIVO (Flourishing)";
        displays.status.classList.add("status-active");
    } else if (wellnessIndex >= 0.8) {
        displays.status.innerText = "ESTADO: RIESGO (Warning)";
        displays.status.classList.add("status-warning");
    } else {
        displays.status.innerText = "ESTADO: RETRACTADO (Wellness Violation)";
        displays.status.classList.add("status-retracted");
    }
}

function updateWisdom(v, price) {
    const wisdomText = document.getElementById('wisdom-text');
    if (v > 3.0) {
        wisdomText.innerText = '"Dividir y extraer genera escasez artificial. El sistema detecta alta fricción ética; el costo de restaurar la vida supera el beneficio inmediato."';
    } else if (v < 1.0 && price < 4.0) {
        wisdomText.innerText = '"La estrategia Cooperativa (C) es la más estable. Al minimizar el sufrimiento, liberas recursos para la abundancia fractal."';
    } else {
        wisdomText.innerText = '"La verdad es neutra, pero la cooperación es eficiente. Mantener el equilibrio de las Tres Cuentas asegura la resiliencia del hogar."';
    }
}

function updateViability(v, price) {
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
    // Clear previous interval if needed (basic implementation)
    // For smoother anim, we might need a global interval var, but this works for MVP

    let frames = 0;
    const interval = setInterval(() => {
        currentDisplayPrice += step;
        frames++;
        displays.price.innerText = currentDisplayPrice.toFixed(2);
        if (frames >= 10 || Math.abs(currentDisplayPrice - target) < 0.01) {
            currentDisplayPrice = target;
            displays.price.innerText = target.toFixed(2);
            clearInterval(interval);
        }
    }, 30);
}

// Enhanced Scenarios for MaxoContracts
const scenarios = {
    // Basic Examples
    'egg-ind': { 
        name: 'Huevo Industrial',
        t: 0.2, v: 4.5, r: 2.5, g: 1.8,
        desc: 'Producción industrial: bajo tiempo humano, alto sufrimiento animal.'
    },
    'egg-eth': { 
        name: 'Huevo Ético',
        t: 0.8, v: 0.2, r: 0.5, g: 1.8,
        desc: 'Producción ética: más tiempo humano, casi nulo sufrimiento.'
    },
    
    // Cohorte Cero Scenarios
    'limpieza': {
        name: 'Limpieza Compartida',
        t: 2.0, v: 0.3, r: 0.7, g: 1.5,
        desc: 'Tareas domésticas en hogar compartido (Cohorte Cero).'
    },
    'prestamo': {
        name: 'Préstamo Solidario',
        t: 1.5, v: 0.1, r: 3.0, g: 1.6,
        desc: 'Préstamo sin intereses entre miembros de la cohorte.'
    },
    'comida': {
        name: 'Comida Cooperativa',
        t: 1.0, v: 0.2, r: 1.2, g: 1.4,
        desc: 'Preparación de comidas en grupo para ahorro colectivo.'
    },
    
    // Edge Cases
    'explotacion': {
        name: 'Trabajo Explotador',
        t: 10.0, v: 4.8, r: 0.5, g: 2.0,
        desc: 'Jornada laboral extenuante con condiciones inhumanas.'
    },
    'voluntariado': {
        name: 'Voluntariado',
        t: 4.0, v: -0.5, r: 0.3, g: 1.2,
        desc: 'Trabajo voluntario que genera bienestar comunitario.'
    }
};

window.loadScenario = function (scKey) {
    const sc = scenarios[scKey];
    if (!sc) return;

    // Update input values
    inputs.time.value = sc.t;
    inputs.life.value = sc.v;
    inputs.resource.value = sc.r;
    
    // Update scenario info display
    const scenarioInfo = document.getElementById('scenario-info');
    if (scenarioInfo) {
        scenarioInfo.innerHTML = `
            <h4>${sc.name || 'Escenario'}</h4>
            <p>${sc.desc || ''}</p>
            <div class="scenario-stats">
                <span>T: ${sc.t}h</span>
                <span>V: ${sc.v}</span>
                <span>R: ${sc.r}</span>
                ${!isOracleMode ? `<span>γ: ${sc.g}</span>` : ''}
            </div>
        `;
    }
    
    // Note: Gamma input is ignored in Oracle Mode, but we set it for static mode
    if (!isOracleMode) {
        inputs.gamma.value = sc.g;
    }

    calculatePrice();
};

// Event Listeners
Object.values(inputs).forEach(input => {
    input.addEventListener('input', calculatePrice);
});

// Oracle Toggle Listener
displays.oracleToggle.addEventListener('change', (e) => {
    isOracleMode = e.target.checked;
    if (isOracleMode) {
        inputs.gamma.classList.add('slider-locked');
        calculatePrice(); // Trigger dynamic calculation immediately
    } else {
        inputs.gamma.classList.remove('slider-locked');
    }
});

// Initial run
calculatePrice();
console.log("Nexus Simulator Engine initialized v2.1 (Dynamic Gamma).");
