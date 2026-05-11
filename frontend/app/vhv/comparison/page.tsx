"use client";

import React, { useState, useEffect } from "react";
import { api } from "../../lib/api";
import { motion } from "framer-motion";
import { LayoutGrid, List, Trophy, Zap, Info, ArrowLeft } from "lucide-react";
import Link from "next/link";
import VHVChart from "../../components/vhv/VHVChart";

export default function VHVComparisonPage() {
  const [products, setProducts] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    setIsLoading(true);
    try {
      const data = await api.getVHVProducts();
      setProducts(data.products || []);
    } catch (err: any) {
      setError(err.message || "Error al cargar productos");
    } finally {
      setIsLoading(false);
    }
  };

  const sortedProducts = [...products].sort((a, b) => a.maxo_price - b.maxo_price);

  return (
    <div className="min-h-screen bg-black text-slate-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-12 flex flex-col md:flex-row md:items-end justify-between gap-6">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <Link href="/vhv/calculator" className="text-indigo-400 flex items-center gap-2 mb-4 hover:text-indigo-300 transition-colors">
              <ArrowLeft size={16} />
              Volver a la calculadora
            </Link>
            <h1 className="text-4xl font-bold tracking-tight">Comparador Ético</h1>
            <p className="text-slate-400 mt-2">Contrasta el impacto vital de tus productos guardados</p>
          </motion.div>

          <div className="flex bg-slate-900/50 p-1 rounded-xl border border-slate-800">
             <button className="p-2 bg-indigo-500/20 text-indigo-400 rounded-lg"><LayoutGrid size={20} /></button>
             <button className="p-2 text-slate-500 hover:text-slate-300"><List size={20} /></button>
          </div>
        </header>

        {isLoading ? (
          <div className="flex justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
          </div>
        ) : products.length === 0 ? (
          <div className="text-center py-20 bg-slate-900/20 border border-dashed border-slate-800 rounded-3xl">
            <Info size={48} className="mx-auto text-slate-600 mb-4" />
            <h2 className="text-xl font-medium text-slate-400">No hay productos guardados</h2>
            <p className="text-slate-500 mt-2 mb-8">Calcula y guarda productos para empezar a comparar</p>
            <Link href="/vhv/calculator">
              <button className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl transition-colors">
                Ir a la calculadora
              </button>
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {sortedProducts.map((product, index) => (
              <motion.div
                key={product.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`relative group bg-slate-900/40 backdrop-blur-xl border p-6 rounded-3xl shadow-xl transition-all hover:shadow-2xl hover:-translate-y-1 ${
                  index === 0 
                    ? "border-emerald-500/50 ring-1 ring-emerald-500/20" 
                    : "border-slate-800 hover:border-slate-700"
                }`}
              >
                {index === 0 && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-emerald-500 text-black text-xs font-black rounded-full shadow-lg flex items-center gap-1">
                    <Trophy size={12} />
                    MENOR COSTO VITAL
                  </div>
                )}

                <div className="mb-6">
                  <h3 className="text-xl font-bold text-white mb-1">{product.name}</h3>
                  <div className="text-xs text-slate-500 uppercase tracking-widest">{product.category || "General"}</div>
                </div>

                <div className="bg-white/5 rounded-2xl p-6 mb-6 text-center border border-white/5">
                  <div className="text-sm text-slate-400 mb-1">Precio Maxo</div>
                  <div className="text-4xl font-black text-white">
                    {product.maxo_price.toFixed(2)}
                    <span className="text-xl ml-1 text-indigo-400">Ⓜ</span>
                  </div>
                </div>

                <div className="h-40 mb-6">
                  <VHVChart 
                    type="doughnut"
                    timeContribution={product.breakdown?.time_contribution || 0}
                    lifeContribution={product.breakdown?.life_contribution || 0}
                    resourceContribution={product.breakdown?.resource_contribution || 0}
                  />
                </div>

                <div className="space-y-3 pt-6 border-t border-slate-800/50">
                   <div className="flex justify-between text-sm">
                      <span className="text-slate-500 flex items-center gap-1"><Zap size={14} className="text-coral-400" /> Tiempo (T)</span>
                      <span className="font-mono text-slate-300">{product.vhv?.T?.toFixed(4) || "0.00"}</span>
                   </div>
                   <div className="flex justify-between text-sm">
                      <span className="text-slate-500 flex items-center gap-1"><Zap size={14} className="text-emerald-400" /> Vida (V)</span>
                      <span className="font-mono text-slate-300">{product.vhv?.V?.toFixed(4) || "0.00"}</span>
                   </div>
                   <div className="flex justify-between text-sm">
                      <span className="text-slate-500 flex items-center gap-1"><Zap size={14} className="text-amber-500" /> Recursos (R)</span>
                      <span className="font-mono text-slate-300">{product.vhv?.R?.toFixed(4) || "0.00"}</span>
                   </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
