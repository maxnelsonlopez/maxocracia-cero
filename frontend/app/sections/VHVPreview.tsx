"""
VHV Preview Section - Landing Page
===================================

Demo interactivo del Vector de Huella Vital:
- Sliders para T, V, R
- Cálculo en tiempo real
- Visualización del resultado

Autor: Kimi (Moonshot AI)
"""

"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Calculator, ArrowRight } from "lucide-react";
import Link from "next/link";

export function VHVPreview() {
  const [time, setTime] = useState(1.0);
  const [life, setLife] = useState(1.0);
  const [resources, setResources] = useState(1.0);
  const [gamma, setGamma] = useState(1.8);
  const [price, setPrice] = useState(0);

  // Calculate price based on formula: α·T + β·V^γ + δ·R·(FRG × CS)
  useEffect(() => {
    const alpha = 0.25;
    const beta = 0.50;
    const delta = 0.20;
    const frg = 1.0;
    const cs = 1.0;

    const timeComponent = alpha * time;
    const lifeComponent = beta * Math.pow(life, gamma);
    const resourceComponent = delta * resources * (frg * cs);

    setPrice(timeComponent + lifeComponent + resourceComponent);
  }, [time, life, resources, gamma]);

  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Calcula el valor real
          </h2>
          <p className="text-slate-400 max-w-2xl mx-auto">
            El Vector de Huella Vital (VHV) transforma tiempo, impacto vital y recursos 
            en una medida coherente: el Maxo.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 items-center">
          {/* Controls */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="bg-slate-900/50 backdrop-blur border border-slate-800 rounded-2xl p-6 sm:p-8"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-emerald-500/10 rounded-lg flex items-center justify-center">
                <Calculator className="w-5 h-5 text-emerald-400" />
              </div>
              <h3 className="font-semibold text-white">Simulador VHV</h3>
            </div>

            <div className="space-y-6">
              {/* Time Slider */}
              <SliderControl
                label="Tiempo (T)"
                value={time}
                min={0.1}
                max={10}
                step={0.1}
                unit="h"
                color="bg-blue-500"
                onChange={setTime}
              />

              {/* Life Slider */}
              <SliderControl
                label="Impacto Vital (V)"
                value={life}
                min={0}
                max={5}
                step={0.1}
                unit="x"
                color="bg-amber-500"
                onChange={setLife}
              />

              {/* Resources Slider */}
              <SliderControl
                label="Recursos (R)"
                value={resources}
                min={0.1}
                max={5}
                step={0.1}
                unit="x"
                color="bg-purple-500"
                onChange={setResources}
              />

              {/* Gamma Slider */}
              <SliderControl
                label="Factor Gamma (γ)"
                value={gamma}
                min={1}
                max={5}
                step={0.1}
                unit=""
                color="bg-emerald-500"
                onChange={setGamma}
              />
            </div>
          </motion.div>

          {/* Result */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="flex flex-col items-center justify-center"
          >
            <div className="text-center mb-8">
              <p className="text-slate-400 mb-2">Valor en Maxos</p>
              <motion.div
                key={price}
                initial={{ scale: 0.9 }}
                animate={{ scale: 1 }}
                className="text-6xl sm:text-7xl font-bold text-white"
              >
                {price.toFixed(2)}
              </motion.div>
              <p className="text-emerald-400 text-lg mt-2">Maxos Vitales</p>
            </div>

            {/* Formula */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4 mb-8 font-mono text-sm text-slate-400">
              <p className="text-center">
                0.25 × {time.toFixed(1)} + 0.50 × {life.toFixed(1)}
                <sup>{gamma.toFixed(1)}</sup> + 0.20 × {resources.toFixed(1)}
              </p>
            </div>

            <Link
              href="http://localhost:5001/vhv-calculator.html"
              target="_blank"
              className="flex items-center gap-2 text-emerald-400 hover:text-emerald-300 transition-colors"
            >
              Calculadora completa con gráficos
              <ArrowRight className="w-4 h-4" />
            </Link>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

interface SliderControlProps {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  unit: string;
  color: string;
  onChange: (value: number) => void;
}

function SliderControl({ 
  label, 
  value, 
  min, 
  max, 
  step, 
  unit, 
  color,
  onChange 
}: SliderControlProps) {
  const percentage = ((value - min) / (max - min)) * 100;

  return (
    <div>
      <div className="flex justify-between items-center mb-2">
        <label className="text-sm font-medium text-slate-300">{label}</label>
        <span className="text-sm text-emerald-400 font-mono">
          {value.toFixed(1)}{unit}
        </span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-500"
        style={{
          background: `linear-gradient(to right, ${color.replace('bg-', '')} ${percentage}%, #334155 ${percentage}%)`
        }}
      />
    </div>
  );
}
