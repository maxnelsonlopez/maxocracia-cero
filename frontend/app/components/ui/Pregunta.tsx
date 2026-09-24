"use client";

import React, { useState } from "react";

/**
 * Pregunta — reemplazo del prompt()/confirm() nativo, hostil en celular.
 * Hoja inferior en la página (nada de ventanas del navegador): input
 * opcional + botones claros. En modo confirmar no hay input.
 */
interface PreguntaProps {
  titulo: string;
  texto?: string;
  placeholder?: string;
  confirmar: string;
  cancelar?: string;
  tipo?: "text" | "number";
  valorInicial?: string;
  confirmarVacio?: boolean;
  onConfirmar: (valor: string) => void;
  onCancelar: () => void;
}

export default function Pregunta({
  titulo,
  texto,
  placeholder,
  confirmar,
  cancelar = "Cancelar",
  tipo = "text",
  valorInicial = "",
  confirmarVacio = false,
  onConfirmar,
  onCancelar,
}: PreguntaProps) {
  const [valor, setValor] = useState(valorInicial);
  // Modo confirmar (sin input): sin placeholder, tipo texto y sin valor inicial.
  const conInput =
    tipo === "number" || placeholder !== undefined || valorInicial !== "";
  const valido = confirmarVacio || valor.trim() !== "";

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/70 p-4">
      <div className="w-full max-w-md rounded-2xl border border-slate-700 bg-slate-900 p-5 space-y-4">
        <h3 className="font-bold text-white">{titulo}</h3>
        {texto && <p className="text-sm text-slate-400">{texto}</p>}
        {conInput && (
          <input
            autoFocus
            type={tipo}
            value={valor}
            onChange={(e) => setValor(e.target.value)}
            placeholder={placeholder}
            onKeyDown={(e) => {
              if (e.key === "Enter" && valido) onConfirmar(valor.trim());
              if (e.key === "Escape") onCancelar();
            }}
            className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
          />
        )}
        <div className="flex gap-3">
          <button
            onClick={onCancelar}
            className="flex-1 px-4 py-2.5 rounded-xl border border-slate-700 text-slate-300 text-sm font-bold"
          >
            {cancelar}
          </button>
          <button
            onClick={() => valido && onConfirmar(valor.trim())}
            disabled={!valido}
            className="flex-1 px-4 py-2.5 rounded-xl bg-emerald-600 text-white text-sm font-bold disabled:opacity-40"
          >
            {confirmar}
          </button>
        </div>
      </div>
    </div>
  );
}
