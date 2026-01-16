/**
 * Form Wizard Engine
 * Transforms standard forms into multi-step interactive experiences.
 */

class FormWizard {
    constructor(formId, options = {}) {
        this.form = document.getElementById(formId);
        if (!this.form) return;

        this.sections = Array.from(this.form.querySelectorAll('.forms-section'));
        this.currentStep = 0;
        this.options = {
            onComplete: null,
            ...options
        };

        this.init();
    }

    init() {
        // Create Progress Bar
        this.progressContainer = document.createElement('div');
        this.progressContainer.className = 'forms-progress vhv-fade-in';
        this.sections.forEach((_, i) => {
            const step = document.createElement('div');
            step.className = `forms-progress-step ${i === 0 ? 'active' : ''}`;
            step.innerHTML = `
                <div class="forms-progress-circle">${i + 1}</div>
                <div class="forms-progress-label">Paso ${i + 1}</div>
            `;
            this.progressContainer.appendChild(step);
        });
        this.form.prepend(this.progressContainer);

        // Hide all but first section
        this.sections.forEach((section, i) => {
            if (i !== 0) section.style.display = 'none';
            section.classList.add('vhv-slide-up');

            // Add navigation buttons to each section
            this.addNavButtons(section, i);
        });

        // Handle original submit button
        const originalSubmit = this.form.querySelector('button[type="submit"]');
        if (originalSubmit) {
            originalSubmit.style.display = 'none'; // We'll show it only on last step
            this.finalSubmit = originalSubmit;
        }
    }

    addNavButtons(section, index) {
        const btnContainer = document.createElement('div');
        btnContainer.className = 'forms-group';
        btnContainer.style.display = 'flex';
        btnContainer.style.gap = 'var(--space-md)';
        btnContainer.style.marginTop = 'var(--space-xl)';

        if (index > 0) {
            const backBtn = document.createElement('button');
            backBtn.type = 'button';
            backBtn.className = 'forms-btn forms-btn-secondary';
            backBtn.textContent = 'Atrás';
            backBtn.addEventListener('click', () => this.goToStep(index - 1));
            btnContainer.appendChild(backBtn);
        }

        if (index < this.sections.length - 1) {
            const nextBtn = document.createElement('button');
            nextBtn.type = 'button';
            nextBtn.className = 'forms-btn forms-btn-primary';
            nextBtn.style.flex = '1';
            nextBtn.textContent = 'Siguiente';
            nextBtn.addEventListener('click', () => {
                if (this.validateStep(index)) {
                    this.goToStep(index + 1);
                }
            });
            btnContainer.appendChild(nextBtn);
        } else {
            // Last step
            const submitBtn = document.createElement('button');
            submitBtn.type = 'submit';
            submitBtn.className = 'forms-btn forms-btn-primary forms-btn-full';
            submitBtn.style.flex = '1';
            submitBtn.textContent = this.finalSubmit ? this.finalSubmit.textContent : 'Finalizar';

            // Clone attributes from original submit if exists
            if (this.finalSubmit) {
                submitBtn.id = this.finalSubmit.id;
            }

            btnContainer.appendChild(submitBtn);
        }

        section.appendChild(btnContainer);
    }

    goToStep(step) {
        // Hide current
        this.sections[this.currentStep].style.display = 'none';

        // Update progress
        const steps = this.progressContainer.querySelectorAll('.forms-progress-step');
        steps[this.currentStep].classList.remove('active');
        if (step > this.currentStep) steps[this.currentStep].classList.add('completed');

        this.currentStep = step;

        // Show new
        this.sections[this.currentStep].style.display = 'block';
        steps[this.currentStep].classList.add('active');

        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    validateStep(index) {
        const section = this.sections[index];
        const inputs = Array.from(section.querySelectorAll('input[required], textarea[required], select[required]'));

        let valid = true;
        inputs.forEach(input => {
            if (!input.checkValidity()) {
                input.classList.add('error');
                valid = false;
            } else {
                input.classList.remove('error');
            }
        });

        if (!valid) {
            // Trigger browser validation UI
            section.querySelector('input:invalid, textarea:invalid, select:invalid')?.reportValidity();
        }

        return valid;
    }
}
