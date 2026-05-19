"use client";

import React, { useState } from "react";
import { 
  Settings, 
  Sliders, 
  ShieldAlert, 
  Key, 
  Save, 
  RefreshCw,
  ToggleLeft,
  ToggleRight
} from "lucide-react";
import { motion } from "framer-motion";

export default function AdminSettings() {
  // Configuración de Pesos Axiomáticos
  const [alpha, setAlpha] = useState(0.25);
  const [beta, setBeta] = useState(0.50);
  const [gamma, setGamma] = useState(1.8);
  const [delta, setDelta] = useState(0.20);

  // Configuración de Sistema
  const [tolerance, setTolerance] = useState(0.15);
  const [matchingLimit, setMatchingLimit] = useState(10);
  const [useOracles, setUseOracles] = useState(true);
  const [strictValidation, setStrictValidation] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaving(true);
    setSaved(false);
    setTimeout(() => {
      setSaving(false);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    }, 1200);
  };

  return (
    <div className="space-y-8 max-w-5xl">
      {/* Encabezado e Intro */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
          <Settings className="w-5 h-5 text-emerald-400" />
          Configuración Global de Gobernanza
        </h3>
        <p className="text-xs text-slate-400 leading-relaxed">
          Calibración del Sistema Operativo Maxocracia. Estos parámetros configuran los pesos del motor de cálculo VHV,
          el umbral de tolerancia para el emparejamiento de necesidades y los mecanismos de validación de contratos en el grafo de reputación.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        
        {/* Pesos VHV */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 space-y-6">
          <div className="flex items-center gap-2 pb-4 border-b border-slate-800">
            <Sliders className="w-4 h-4 text-emerald-400" />
            <h4 className="font-semibold text-white">Pesos de la Ecuación VHV</h4>
          </div>

          <div className="space-y-5">
            <WeightSlider 
              label="Alpha (α) - Tiempo Colectivo" 
              value={alpha} 
              onChange={setAlpha} 
              min={0.05} 
              max={1.00} 
              step={0.05} 
              description="Impacto del tiempo vital directo sobre el precio"
            />
            <WeightSlider 
              label="Beta (β) - Impacto Vital" 
              value={beta} 
              onChange={setBeta} 
              min={0.10} 
              max={1.50} 
              step={0.05} 
              description="Escalar del factor de impacto vital subjetivo"
            />
            <WeightSlider 
              label="Gamma (γ) - Exponente Vital" 
              value={gamma} 
              onChange={setGamma} 
              min={1.0} 
              max={3.0} 
              step={0.1} 
              description="Exponente de urgencia vital (Axioma T2)"
            />
            <WeightSlider 
              label="Delta (δ) - Riqueza/Recursos" 
              value={delta} 
              onChange={setDelta} 
              min={0.05} 
              max={1.00} 
              step={0.05} 
              description="Peso del impacto ecológico y consumo de materias primas"
            />
          </div>
        </div>

        {/* Parámetros del Motor de Matching */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 space-y-6">
          <div className="flex items-center gap-2 pb-4 border-b border-slate-800">
            <ShieldAlert className="w-4 h-4 text-emerald-400" />
            <h4 className="font-semibold text-white">Límites y Tolerancia Operativa</h4>
          </div>

          <div className="space-y-6">
            <WeightSlider 
              label="Tolerancia de Coherencia" 
              value={tolerance} 
              onChange={setTolerance} 
              min={0.05} 
              max={0.50} 
              step={0.01} 
              format={(v) => `${(v * 100).toFixed(0)}%`}
              description="Desvío máximo permitido entre oferta y demanda vital"
            />

            <div className="space-y-2">
              <label className="block text-xs font-semibold text-slate-300">
                Máximo de Iteraciones de Matching
              </label>
              <input 
                type="number"
                value={matchingLimit}
                onChange={(e) => setMatchingLimit(parseInt(e.target.value) || 1)}
                className="w-full px-3 py-2 text-xs rounded-lg bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500 text-white font-mono"
              />
              <span className="text-[10px] text-slate-500 block">Límite de profundidad para el emparejamiento recurrente.</span>
            </div>

            {/* Toggles */}
            <div className="space-y-4 pt-2">
              <ToggleRow 
                label="Validación Estricta de Axiomas" 
                checked={strictValidation} 
                onChange={setStrictValidation} 
                description="Rechazar contratos con violaciones de Coherencia"
              />
              <ToggleRow 
                label="Habilitar Oráculos de Reputación" 
                checked={useOracles} 
                onChange={setUseOracles} 
                description="Conectar con oráculos externos para auditoría"
              />
            </div>
          </div>
        </div>

      </div>

      {/* API e Integraciones */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 space-y-6">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Key className="w-4 h-4 text-emerald-400" />
            <h4 className="font-semibold text-white">Integración con Stripe & Pasarelas</h4>
          </div>
          <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            Conexión Segura Activa
          </span>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="block text-xs font-semibold text-slate-300">Webhook Secret</label>
            <div className="flex gap-2">
              <input 
                type="password" 
                value="whsec_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" 
                disabled 
                className="flex-1 px-3 py-2 text-xs rounded-lg bg-slate-950 border border-slate-800 text-slate-500 font-mono"
              />
              <button className="px-3 py-2 rounded-lg bg-slate-850 border border-slate-800 text-xs text-slate-300 hover:text-white transition-colors">
                Rotar
              </button>
            </div>
            <span className="text-[10px] text-slate-500 block">Firma y verificación de eventos Stripe Checkout.</span>
          </div>

          <div className="space-y-2">
            <label className="block text-xs font-semibold text-slate-300">Modo de Operación</label>
            <select className="w-full px-3 py-2 text-xs rounded-lg bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500 text-white">
              <option value="test">Sandbox / Pruebas de Red</option>
              <option value="live" disabled>Producción Coherente (Requiere Consenso)</option>
            </select>
            <span className="text-[10px] text-slate-500 block">Selecciona el entorno de transacciones.</span>
          </div>
        </div>
      </div>

      {/* Botón de Guardado */}
      <div className="flex justify-end gap-4">
        <button 
          onClick={handleSave}
          disabled={saving}
          className="flex items-center gap-2 px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold transition-all hover:scale-102 hover:shadow-lg disabled:opacity-50"
        >
          {saving ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              Guardando Parámetros...
            </>
          ) : (
            <>
              <Save className="w-4 h-4" />
              Guardar Configuración Axiomática
            </>
          )}
        </button>
      </div>

      {/* Notificación de Guardado */}
      {saved && (
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold text-center"
        >
          ✅ Configuración guardada e inyectada exitosamente en el Motor de Gobernanza Maxo OS.
        </motion.div>
      )}
    </div>
  );
}

// Componente Slider de Pesos
interface WeightSliderProps {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  onChange: (val: number) => void;
  format?: (val: number) => string;
  description: string;
}

function WeightSlider({ label, value, min, max, step, onChange, format, description }: WeightSliderProps) {
  const percentage = ((value - min) / (max - min)) * 100;
  const displayVal = format ? format(value) : value.toFixed(2);

  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center text-xs">
        <label className="font-semibold text-slate-300">{label}</label>
        <span className="font-mono text-emerald-400 font-bold">{displayVal}</span>
      </div>
      <input 
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
        style={{
          background: `linear-gradient(to right, #10b981 ${percentage}%, #1e293b ${percentage}%)`
        }}
      />
      <span className="text-[10px] text-slate-500 block leading-relaxed">{description}</span>
    </div>
  );
}

// Componente Toggle Row
interface ToggleRowProps {
  label: string;
  checked: boolean;
  onChange: (val: boolean) => void;
  description: string;
}

function ToggleRow({ label, checked, onChange, description }: ToggleRowProps) {
  return (
    <div className="flex items-start justify-between gap-4 p-3 rounded-lg bg-slate-950/40 border border-slate-900">
      <div className="space-y-0.5">
        <p className="text-xs font-semibold text-slate-300">{label}</p>
        <p className="text-[10px] text-slate-500 leading-relaxed">{description}</p>
      </div>
      <button 
        onClick={() => onChange(!checked)}
        className="text-slate-400 hover:text-white transition-colors"
      >
        {checked ? (
          <ToggleRight className="w-6 h-6 text-emerald-500" />
        ) : (
          <ToggleLeft className="w-6 h-6 text-slate-600" />
        )}
      </button>
    </div>
  );
}
