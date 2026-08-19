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
  name?: string;
}

export const FormCheckboxGroup: React.FC<FormCheckboxGroupProps> = ({
  label,
  options,
  selectedValues,
  onChange,
  error,
  name,
}) => {
  const groupId = React.useId().replace(/:/g, "");
  const errorId = `${groupId}-error`;

  const toggleOption = (value: string, checked: boolean) => {
    if (checked) {
      onChange(selectedValues.includes(value) ? selectedValues : [...selectedValues, value]);
    } else {
      onChange(selectedValues.filter((selectedValue) => selectedValue !== value));
    }
  };

  return (
    <fieldset
      className="flex flex-col gap-3 w-full"
      aria-describedby={error ? errorId : undefined}
    >
      <legend className="text-sm font-medium text-slate-300 ml-1">{label}</legend>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {options.map((option) => {
          const inputId = `${groupId}-${option.value}`;
          const isSelected = selectedValues.includes(option.value);

          return (
            <label
              key={option.value}
              htmlFor={inputId}
              className={`flex items-center gap-3 p-4 rounded-xl border transition-all text-left group cursor-pointer focus-within:ring-2 focus-within:ring-emerald-500/50 ${
                isSelected
                  ? "bg-emerald-500/10 border-emerald-500/50 text-emerald-400"
                  : "bg-slate-900/50 border-slate-800 text-slate-400 hover:border-slate-700 hover:bg-slate-800/50"
              }`}
            >
              <input
                id={inputId}
                name={name}
                type="checkbox"
                value={option.value}
                checked={isSelected}
                onChange={(event) => toggleOption(option.value, event.target.checked)}
                aria-invalid={error ? "true" : undefined}
                aria-describedby={error ? errorId : undefined}
                className="sr-only peer"
              />
              <span
                aria-hidden="true"
                className={`w-5 h-5 rounded border flex items-center justify-center transition-all peer-focus-visible:ring-2 peer-focus-visible:ring-emerald-400/70 ${
                  isSelected
                    ? "bg-emerald-500 border-emerald-500 text-slate-950"
                    : "border-slate-700 bg-slate-950 group-hover:border-slate-600"
                }`}
              >
                {isSelected && <Check size={14} strokeWidth={4} />}
              </span>
              <span className="flex flex-col">
                <span className="text-sm font-medium">
                  {option.emoji && <span className="mr-2" aria-hidden="true">{option.emoji}</span>}
                  {option.label}
                </span>
              </span>
            </label>
          );
        })}
      </div>
      {error && (
        <span id={errorId} role="alert" className="text-xs text-red-400 ml-1">
          {error}
        </span>
      )}
    </fieldset>
  );
};
