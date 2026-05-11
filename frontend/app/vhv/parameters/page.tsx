"use client";

import React, { useState, useEffect } from "react";
import { api } from "../../lib/api";
import { motion, AnimatePresence } from "framer-motion";
import { Settings, Save, AlertTriangle, ShieldCheck, RotateCcw } from "lucide-react";
import { Input } from "../../components/ui/Input";
import { Button } from "../../components/ui/Button";

export default function VHVParametersPage() {
  const [params, setParams] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    loadParameters();
  }, []);

  const loadParameters = async () => {
    setIsLoading(true);
    try {
      const data = await api.getVHVParameters();
      setParams(data);
    } catch (err: any) {
      setError("Error al cargar parámetros. ¿Tienes permisos de administrador?");
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setParams((prev: any) => ({
      ...prev,
      [name]: parseFloat(value) || 0,
    }));
  };

  const handleSave = async () => {
    setIsSaving(true);
    setError(null);
    setSuccess(false);

    // Basic Axiom Validation
    if (params.alpha < 0 || params.beta < 0 || params.delta < 0) {
      setError("Violación de Axioma: Los coeficientes (α, β, δ) no pueden ser negativos.");
      setIsSaving(false);
      return;
    }

    if (params.gamma < 1) {
       setError("Violación de Axioma: El exponente vital (γ) debe ser ≥ 1 para penalizar exponencialmente el daño a la vida.");
       setIsSaving(false);
       return;
    }

    try {
      await api.updateVHVParameters(params);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err: any) {
      setError(err.message || "Error al actualizar parámetros");
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) return <div className="min-h-screen bg-black flex items-center justify-center"><div className="animate-spin rounded-full h-12 w-12 border-t-2 border-indigo-500"></div></div>;

  return (
    <div className="min-h-screen bg-black text-slate-100 p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-12">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-2xl bg-amber-500/20 flex items-center justify-center text-amber-400 border border-amber-500/30 shadow-lg shadow-amber-500/10">
              <Settings size={28} />
            </div>
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Parámetros Axiomáticos</h1>
              <p className="text-slate-400">Ajuste de los coeficientes base del motor económico</p>
            </div>
          </div>
        </header>

        <div className="grid grid-cols-1 gap-8">
          {/* Main Formula Card */}
          <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800 p-8 rounded-3xl shadow-xl relative overflow-hidden">
             <div className="absolute top-0 right-0 p-8 opacity-5">
                <ShieldCheck size={160} />
             </div>
             
             <div className="relative z-10">
                <h2 className="text-xl font-semibold mb-8 flex items-center gap-2">
                   <ShieldCheck size={20} className="text-emerald-400" />
                   Fórmula Maestra
                </h2>
                
                <div className="bg-black/40 p-6 rounded-2xl border border-slate-800 mb-8 text-center font-serif italic text-2xl text-slate-300">
                   Precio = <span className="text-coral-400 font-bold">α</span>·T + <span className="text-emerald-400 font-bold">β</span>·V<sup className="text-indigo-400 font-bold">γ</sup> + <span className="text-amber-500 font-bold">δ</span>·R
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                   <div className="space-y-6">
                      <Input 
                        label="Alfa (α) - Multiplicador de Tiempo"
                        name="alpha"
                        type="number"
                        step="0.01"
                        value={params?.alpha}
                        onChange={handleChange}
                        className="font-mono text-coral-400"
                      />
                      <p className="text-xs text-slate-500 italic">Determina el valor base de una hora de vida humana.</p>
                      
                      <Input 
                        label="Beta (β) - Multiplicador de Vida"
                        name="beta"
                        type="number"
                        step="0.01"
                        value={params?.beta}
                        onChange={handleChange}
                        className="font-mono text-emerald-400"
                      />
                      <p className="text-xs text-slate-500 italic">Escala el impacto del daño a organismos vivos.</p>
                   </div>
                   
                   <div className="space-y-6">
                      <Input 
                        label="Gamma (γ) - Exponente Vital"
                        name="gamma"
                        type="number"
                        step="0.1"
                        value={params?.gamma}
                        onChange={handleChange}
                        className="font-mono text-indigo-400"
                      />
                      <p className="text-xs text-slate-500 italic">Penalización exponencial por sufrimiento o destrucción biológica.</p>
                      
                      <Input 
                        label="Delta (δ) - Multiplicador de Recursos"
                        name="delta"
                        type="number"
                        step="0.01"
                        value={params?.delta}
                        onChange={handleChange}
                        className="font-mono text-amber-500"
                      />
                      <p className="text-xs text-slate-500 italic">Costo de extracción y uso de recursos no renovables.</p>
                   </div>
                </div>

                <div className="mt-12 flex flex-col md:flex-row gap-4 pt-8 border-t border-slate-800">
                   <Button onClick={handleSave} disabled={isSaving} className="flex-1 gap-2">
                      <Save size={18} />
                      {isSaving ? "Guardando..." : "Actualizar Parámetros"}
                   </Button>
                   <Button onClick={loadParameters} variant="outline" className="gap-2 border-slate-700 text-slate-400 hover:text-white">
                      <RotateCcw size={18} />
                      Restaurar
                   </Button>
                </div>
             </div>
          </div>

          {/* Alerts and Notices */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="p-6 bg-red-500/10 border border-red-500/30 rounded-2xl flex items-start gap-4 text-red-400"
              >
                <AlertTriangle className="shrink-0" />
                <div>
                  <h4 className="font-bold mb-1">Error de Validación</h4>
                  <p className="text-sm">{error}</p>
                </div>
              </motion.div>
            )}

            {success && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="p-6 bg-emerald-500/10 border border-emerald-500/30 rounded-2xl flex items-start gap-4 text-emerald-400"
              >
                <ShieldCheck className="shrink-0" />
                <div>
                  <h4 className="font-bold mb-1">Parámetros Actualizados</h4>
                  <p className="text-sm">El motor económico ha sido recalibrado exitosamente.</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
