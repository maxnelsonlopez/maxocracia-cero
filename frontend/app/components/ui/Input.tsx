import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className = "", ...props }, ref) => {
    return (
      <div className="flex flex-col gap-1 w-full">
        <label className="text-sm font-medium text-slate-300 ml-1">{label}</label>
        <input
          ref={ref}
          className={`px-4 py-3 bg-slate-900/50 backdrop-blur-md border rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 transition-all ${
            error ? "border-red-500/50" : "border-slate-800 focus:border-emerald-500/50"
          } ${className}`}
          {...props}
        />
        {error && <span className="text-xs text-red-400 ml-1">{error}</span>}
      </div>
    );
  }
);
Input.displayName = "Input";
