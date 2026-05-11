import React from "react";

interface Option {
  label: string;
  value: string;
  emoji?: string;
  color?: string; // e.g. "bg-red-500", "bg-yellow-500", "bg-green-500"
}

interface FormRadioGroupProps {
  label: string;
  options: Option[];
  selectedValue: string;
  onChange: (value: string) => void;
  error?: string;
}

export const FormRadioGroup: React.FC<FormRadioGroupProps> = ({
  label,
  options,
  selectedValue,
  onChange,
  error,
}) => {
  return (
    <div className="flex flex-col gap-3 w-full">
      <label className="text-sm font-medium text-slate-300 ml-1">{label}</label>
      <div className="flex flex-wrap gap-3">
        {options.map((option) => (
          <button
            key={option.value}
            type="button"
            onClick={() => onChange(option.value)}
            className={`flex items-center gap-3 px-4 py-3 rounded-xl border transition-all text-left group ${
              selectedValue === option.value
                ? "bg-emerald-500/10 border-emerald-500/50 text-emerald-400"
                : "bg-slate-900/50 border-slate-800 text-slate-400 hover:border-slate-700 hover:bg-slate-800/50"
            }`}
          >
            <div
              className={`w-4 h-4 rounded-full border-2 flex items-center justify-center transition-all ${
                selectedValue === option.value
                  ? "border-emerald-500 bg-transparent"
                  : "border-slate-700 bg-transparent group-hover:border-slate-600"
              }`}
            >
              {selectedValue === option.value && (
                <div className="w-2 h-2 rounded-full bg-emerald-500" />
              )}
            </div>
            <span className="text-sm font-medium">
              {option.emoji && <span className="mr-2">{option.emoji}</span>}
              {option.label}
            </span>
          </button>
        ))}
      </div>
      {error && <span className="text-xs text-red-400 ml-1">{error}</span>}
    </div>
  );
};
