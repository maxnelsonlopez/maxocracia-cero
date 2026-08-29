"use client";

import React, { useState } from "react";
import { HelpCircle } from "lucide-react";

/**
 * InfoTip — ayuda emergente en lenguaje sencillo.
 *
 * La UI de la Maxocracia habla en lenguaje de calle; el concepto complejo
 * (T13: "lenguaje civil" + "el cálculo se explica, no se confiesa") vive
 * detrás del icono ℹ️, disponible solo para quien quiere profundizar.
 * Funciona con hover (desktop) y con clic (móvil/teclado).
 */
export default function InfoTip({ text, className }: { text: string; className?: string }) {
  const [open, setOpen] = useState(false);

  return (
    <span
      className={`relative inline-flex items-center align-middle ${className ?? ""}`}
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
      onClick={() => setOpen((o) => !o)}
      onKeyDown={(e) => {
        if (e.key === "Escape") setOpen(false);
      }}
      role="button"
      tabIndex={0}
      aria-label="Explicación (pasa el cursor o toca)"
    >
      <HelpCircle className="w-3.5 h-3.5 text-slate-400 hover:text-white transition-colors cursor-help" />
      {open && (
        <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 z-50 w-64 px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-[11px] leading-relaxed text-slate-300 shadow-xl pointer-events-none">
          {text}
        </span>
      )}
    </span>
  );
}
