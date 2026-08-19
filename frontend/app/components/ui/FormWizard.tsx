import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { AlertCircle, ChevronLeft, ChevronRight, Check } from "lucide-react";
import { Button } from "./Button";

interface FormWizardProps {
  steps: string[];
  children: React.ReactNode[];
  onComplete: (data: Record<string, unknown>) => void;
  isSubmitting?: boolean;
  validateStep?: (step: number) => string | null;
}

export const FormWizard: React.FC<FormWizardProps> = ({
  steps,
  children,
  onComplete,
  isSubmitting = false,
  validateStep,
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [stepError, setStepError] = useState("");
  const totalSteps = steps.length;

  const handleNext = () => {
    const validationError = validateStep?.(currentStep) ?? null;

    if (validationError) {
      setStepError(validationError);
      return;
    }

    setStepError("");

    if (currentStep < totalSteps - 1) {
      setCurrentStep((step) => step + 1);
    } else {
      onComplete({});
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setStepError("");
      setCurrentStep((step) => step - 1);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div className="mb-8" aria-label="Progreso del formulario">
        <div className="flex justify-between mb-2">
          {steps.map((step, index) => (
            <div
              key={step}
              aria-current={index === currentStep ? "step" : undefined}
              className={`flex flex-col items-center flex-1 ${
                index <= currentStep ? "text-emerald-400" : "text-slate-500"
              }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center border-2 mb-1 transition-all ${
                  index < currentStep
                    ? "bg-emerald-500 border-emerald-500 text-slate-950"
                    : index === currentStep
                      ? "border-emerald-500 text-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.3)]"
                      : "border-slate-700 text-slate-500"
                }`}
              >
                {index < currentStep ? <Check size={16} strokeWidth={3} /> : index + 1}
              </div>
              <span className="text-[10px] uppercase tracking-wider font-bold text-center px-1">
                {step}
              </span>
            </div>
          ))}
        </div>
        <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${((currentStep + 1) / totalSteps) * 100}%` }}
            className="h-full bg-emerald-500"
          />
        </div>
      </div>

      <div className="relative min-h-[400px] bg-slate-900/40 backdrop-blur-xl border border-slate-800/50 rounded-3xl p-6 md:p-8 shadow-2xl">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep}
            role="tabpanel"
            aria-label={`Paso ${currentStep + 1}: ${steps[currentStep]}`}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            {children[currentStep]}
          </motion.div>
        </AnimatePresence>

        {stepError && (
          <div
            role="alert"
            aria-live="assertive"
            className="mt-6 flex items-start gap-3 rounded-xl border border-amber-500/30 bg-amber-500/10 p-4 text-sm text-amber-200"
          >
            <AlertCircle size={20} className="mt-0.5 shrink-0 text-amber-400" aria-hidden="true" />
            <p>{stepError}</p>
          </div>
        )}

        <div className="flex justify-between mt-10 pt-6 border-t border-slate-800/50">
          <Button
            type="button"
            variant="ghost"
            onClick={handleBack}
            disabled={currentStep === 0 || isSubmitting}
            className={currentStep === 0 ? "opacity-0 pointer-events-none" : ""}
          >
            <ChevronLeft size={20} aria-hidden="true" />
            Atrás
          </Button>

          <Button
            type="button"
            variant="primary"
            onClick={handleNext}
            isLoading={isSubmitting}
            className="min-w-[140px]"
          >
            {currentStep === totalSteps - 1 ? "Finalizar" : "Siguiente"}
            {currentStep !== totalSteps - 1 && <ChevronRight size={20} aria-hidden="true" />}
          </Button>
        </div>
      </div>
    </div>
  );
};
