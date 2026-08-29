import React from "react";
import InfoTip from "./InfoTip";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  /** Ayuda emergente (ℹ️) en lenguaje sencillo que explica el concepto. */
  hint?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, hint, className = "", id, name, required, ...props }, ref) => {
    const inputId = id ?? name;
    const errorId = error && inputId ? `${inputId}-error` : undefined;

    return (
      <div className="flex flex-col gap-1 w-full">
        <label htmlFor={inputId} className="text-sm font-medium text-slate-300 ml-1">
          {label}
          {required && <span className="ml-1 text-emerald-400" aria-hidden="true">*</span>}
          {required && <span className="sr-only"> (requerido)</span>}
          {hint && <InfoTip className="ml-2" text={hint} />}
        </label>
        <input
          ref={ref}
          id={inputId}
          name={name}
          required={required}
          aria-invalid={error ? "true" : undefined}
          aria-describedby={errorId}
          className={`px-4 py-3 bg-slate-900/50 backdrop-blur-md border rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 transition-all ${
            error ? "border-red-500/50" : "border-slate-800 focus:border-emerald-500/50"
          } ${className}`}
          {...props}
        />
        {error && (
          <span id={errorId} className="text-xs text-red-400 ml-1">
            {error}
          </span>
        )}
      </div>
    );
  }
);
Input.displayName = "Input";
