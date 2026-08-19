import React from "react";

interface Option {
  label: string;
  value: string;
  emoji?: string;
  color?: string;
}

interface FormRadioGroupProps {
  label: string;
  options: Option[];
  selectedValue: string;
  onChange: (value: string) => void;
  error?: string;
  name?: string;
}

export const FormRadioGroup: React.FC<FormRadioGroupProps> = ({
  label,
  options,
  selectedValue,
  onChange,
  error,
  name,
}) => {
  const groupId = React.useId().replace(/:/g, "");
  const radioName = name ?? groupId;
  const errorId = `${groupId}-error`;

  return (
    <fieldset
      className="flex flex-col gap-3 w-full"
      aria-describedby={error ? errorId : undefined}
    >
      <legend className="text-sm font-medium text-slate-300 ml-1">{label}</legend>
      <div className="flex flex-wrap gap-3">
        {options.map((option) => {
          const inputId = `${groupId}-${option.value}`;
          const isSelected = selectedValue === option.value;

          return (
            <label
              key={option.value}
              htmlFor={inputId}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl border transition-all text-left group cursor-pointer focus-within:ring-2 focus-within:ring-emerald-500/50 ${
                isSelected
                  ? "bg-emerald-500/10 border-emerald-500/50 text-emerald-400"
                  : "bg-slate-900/50 border-slate-800 text-slate-400 hover:border-slate-700 hover:bg-slate-800/50"
              }`}
            >
              <input
                id={inputId}
                name={radioName}
                type="radio"
                value={option.value}
                checked={isSelected}
                onChange={() => onChange(option.value)}
                aria-describedby={error ? errorId : undefined}
                className="sr-only peer"
              />
              <span
                aria-hidden="true"
                className={`w-4 h-4 rounded-full border-2 flex items-center justify-center transition-all peer-focus-visible:ring-2 peer-focus-visible:ring-emerald-400/70 ${
                  isSelected
                    ? "border-emerald-500 bg-transparent"
                    : "border-slate-700 bg-transparent group-hover:border-slate-600"
                }`}
              >
                {isSelected && <span className="w-2 h-2 rounded-full bg-emerald-500" />}
              </span>
              <span className="text-sm font-medium">
                {option.emoji && <span className="mr-2" aria-hidden="true">{option.emoji}</span>}
                {option.label}
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
