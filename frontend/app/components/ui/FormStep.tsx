import React from "react";

interface FormStepProps {
  title: string;
  description?: string;
  children: React.ReactNode;
}

export const FormStep: React.FC<FormStepProps> = ({ title, description, children }) => {
  return (
    <div className="space-y-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-white mb-2 flex items-center gap-2">
          {title}
        </h2>
        {description && <p className="text-slate-400 text-sm">{description}</p>}
      </div>
      <div className="grid gap-6">
        {children}
      </div>
    </div>
  );
};
