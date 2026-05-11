import React from "react";

interface FormTextAreaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label: string;
  error?: string;
}

export const FormTextArea = React.forwardRef<HTMLTextAreaElement, FormTextAreaProps>(
  ({ label, error, className = "", ...props }, ref) => {
    return (
      <div className="flex flex-col gap-1 w-full">
        <label className="text-sm font-medium text-slate-300 ml-1">{label}</label>
        <textarea
          ref={ref}
          className={`px-4 py-3 bg-slate-900/50 backdrop-blur-md border rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 transition-all min-h-[100px] resize-y ${
            error ? "border-red-500/50" : "border-slate-800 focus:border-emerald-500/50"
          } ${className}`}
          {...props}
        />
        {error && <span className="text-xs text-red-400 ml-1">{error}</span>}
      </div>
    );
  }
);
FormTextArea.displayName = "FormTextArea";
