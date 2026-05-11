import React from "react";
import { Check } from "lucide-react";

interface Option {
  label: string;
  value: string;
  emoji?: string;
}

interface FormCheckboxGroupProps {
  label: string;
  options: Option[];
  selectedValues: string[];
  onChange: (values: string[]) => void;
  error?: string;
}

export const FormCheckboxGroup: React.FC<FormCheckboxGroupProps> = ({
  label,
  options,
  selectedValues,
  onChange,
  error,
}) => {
  const toggleOption = (value: string) => {
    if (selectedValues.includes(value)) {
      onChange(selectedValues.filter((v) => v !== value));
    } else {
      onChange([...selectedValues, value]);
    }
  };

  return (
    <div className="flex flex-col gap-3 w-full">
      <label className="text-sm font-medium text-slate-300 ml-1">{label}</label>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {options.map((option) => (
          <button
            key={option.value}
            type="button"
            onClick={() => toggleOption(option.value)}
            className={`flex items-center gap-3 p-4 rounded-xl border transition-all text-left group ${
              selectedValues.includes(option.value)
                ? "bg-emerald-500/10 border-emerald-500/50 text-emerald-400"
                : "bg-slate-900/50 border-slate-800 text-slate-400 hover:border-slate-700 hover:bg-slate-800/50"
            }`}
          >
            <div
              className={`w-5 h-5 rounded border flex items-center justify-center transition-all ${
                selectedValues.includes(option.value)
                  ? "bg-emerald-500 border-emerald-500 text-slate-950"
                  : "border-slate-700 bg-slate-950 group-hover:border-slate-600"
              }`}
            >
              {selectedValues.includes(option.value) && <Check size={14} strokeWidth={4} />}
            </div>
            <div className="flex flex-col">
              <span className="text-sm font-medium">
                {option.emoji && <span className="mr-2">{option.emoji}</span>}
                {option.label}
              </span>
            </div>
          </button>
        ))}
      </div>
      {error && <span className="text-xs text-red-400 ml-1">{error}</span>}
    </div>
  );
};
