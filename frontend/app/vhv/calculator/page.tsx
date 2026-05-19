"use client";

import React, { useState, useEffect } from "react";
import VHVForm, { VHVFormData } from "../../components/vhv/VHVForm";
import VHVChart from "../../components/vhv/VHVChart";
import { api } from "../../lib/api";
import { motion, AnimatePresence } from "framer-motion";
import { Calculator, Info, Save, BookOpen, ArrowRight } from "lucide-react";
import { Button } from "../../components/ui/Button";

interface CalculationResult {
  maxo_price: number;
  breakdown: {
    time_contribution: number;
    life_contribution: number;
    resource_contribution: number;
  };
  input_data: VHVFormData;
}

interface CaseStudy {
  name: string;
  data: Partial<VHVFormData>;
}

export default function VHVCalculatorPage() {
  const [calculationResult, setCalculationResult] = useState<CalculationResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [caseStudies, setCaseStudies] = useState<CaseStudy[]>([]);
  const [selectedCaseStudy, setSelectedCaseStudy] = useState<CaseStudy | null>(null);

  const loadCaseStudies = async () => {
    try {
      const data = await api.getVHVCaseStudies();
      setCaseStudies(data.case_studies || []);
    } catch (err) {
      console.error("Error loading case studies", err);
    }
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadCaseStudies();
  }, []);

  const handleCalculate = async (formData: VHVFormData) => {
    setError(null);
    try {
      const result = await api.calculateVHV(formData);
      setCalculationResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al calcular el VHV");
    }
  };

  const handleSaveProduct = async () => {
    if (!calculationResult) return;
    try {
      await api.calculateVHV({ ...calculationResult.input_data, save: true });
      alert("Producto guardado exitosamente");
    } catch (err) {
      alert("Error al guardar: " + (err instanceof Error ? err.message : "Error desconocido"));
    }
  };

  const selectCaseStudy = (study: CaseStudy) => {
    setSelectedCaseStudy(study);
    // This will trigger the useEffect in VHVForm to update the fields
  };

  return (
    <div className="min-h-screen bg-black text-slate-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-12">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center gap-3 mb-4"
          >
            <div className="w-12 h-12 rounded-2xl bg-indigo-500/20 flex items-center justify-center text-indigo-400 border border-indigo-500/30 shadow-lg shadow-indigo-500/10">
              <Calculator size={28} />
            </div>
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Calculadora VHV</h1>
              <p className="text-slate-400">Determina el Precio Maxo basado en el Valor Humano Vital</p>
            </div>
          </motion.div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column: Form and Presets */}
          <div className="lg:col-span-7 space-y-8">
            <section className="bg-slate-900/40 backdrop-blur-xl border border-slate-800 p-6 rounded-2xl">
              <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                <BookOpen size={20} className="text-indigo-400" />
                Casos de Estudio / Presets
              </h2>
              <div className="flex flex-wrap gap-3">
                {caseStudies.map((study) => (
                  <button
                    key={study.name}
                    onClick={() => selectCaseStudy(study)}
                    className={`px-4 py-2 rounded-xl border transition-all flex items-center gap-2 ${
                      selectedCaseStudy?.name === study.name
                        ? "bg-indigo-500/20 border-indigo-500/50 text-indigo-300"
                        : "bg-slate-800/50 border-slate-700 text-slate-400 hover:border-slate-600"
                    }`}
                  >
                    {study.name}
                    <ArrowRight size={14} />
                  </button>
                ))}
              </div>
            </section>

            <VHVForm onCalculate={handleCalculate} initialData={selectedCaseStudy?.data} />
          </div>

          {/* Right Column: Results and Chart */}
          <div className="lg:col-span-5">
            <div className="sticky top-8 space-y-6">
              <AnimatePresence mode="wait">
                {calculationResult ? (
                  <motion.div
                    key="result"
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    className="space-y-6"
                  >
                    {/* Final Price Card */}
                    <div className="bg-gradient-to-br from-indigo-600/20 to-purple-600/20 backdrop-blur-2xl border border-indigo-500/30 p-8 rounded-3xl shadow-2xl relative overflow-hidden group">
                      <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                        <Calculator size={120} />
                      </div>
                      <div className="relative z-10">
                        <h3 className="text-sm font-medium text-indigo-300 mb-2 uppercase tracking-widest">Precio Maxo Calculado</h3>
                        <div className="flex items-baseline gap-2">
                          <span className="text-6xl font-black text-white">
                            {calculationResult.maxo_price.toFixed(2)}
                          </span>
                          <span className="text-2xl font-bold text-indigo-400">Ⓜ</span>
                        </div>
                        <div className="mt-6 flex gap-4">
                          <Button onClick={handleSaveProduct} variant="outline" className="w-full bg-white/5 border-white/10 hover:bg-white/10 text-white gap-2">
                            <Save size={18} />
                            Guardar Producto
                          </Button>
                        </div>
                      </div>
                    </div>

                    {/* Breakdown Chart */}
                    <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800 p-6 rounded-2xl shadow-xl">
                      <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                        <Info size={20} className="text-indigo-400" />
                        Desglose de Contribución
                      </h3>
                      <VHVChart
                        timeContribution={calculationResult.breakdown.time_contribution}
                        lifeContribution={calculationResult.breakdown.life_contribution}
                        resourceContribution={calculationResult.breakdown.resource_contribution}
                      />
                      
                      <div className="mt-8 grid grid-cols-3 gap-4">
                        <div className="p-4 bg-coral-500/10 border border-coral-500/20 rounded-xl text-center">
                          <div className="text-xs text-coral-400 mb-1">Tiempo (T)</div>
                          <div className="text-lg font-bold">{calculationResult.breakdown.time_contribution.toFixed(2)}Ⓜ</div>
                        </div>
                        <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-center">
                          <div className="text-xs text-emerald-400 mb-1">Vida (V)</div>
                          <div className="text-lg font-bold">{calculationResult.breakdown.life_contribution.toFixed(2)}Ⓜ</div>
                        </div>
                        <div className="p-4 bg-amber-600/10 border border-amber-600/20 rounded-xl text-center">
                          <div className="text-xs text-amber-500 mb-1">Recursos (R)</div>
                          <div className="text-lg font-bold">{calculationResult.breakdown.resource_contribution.toFixed(2)}Ⓜ</div>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ) : (
                  <motion.div
                    key="placeholder"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="h-[600px] bg-slate-900/20 border border-dashed border-slate-800 rounded-3xl flex flex-col items-center justify-center text-center p-8"
                  >
                    <div className="w-20 h-20 rounded-full bg-slate-800/50 flex items-center justify-center text-slate-500 mb-6">
                      <Calculator size={40} />
                    </div>
                    <h3 className="text-xl font-medium text-slate-300 mb-2">Esperando Cálculo</h3>
                    <p className="text-slate-500 max-w-xs">
                      Completa el formulario de la izquierda para ver el desglose detallado del Precio Maxo.
                    </p>
                  </motion.div>
                )}
              </AnimatePresence>
              
              {error && (
                <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm">
                  {error}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
