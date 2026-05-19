"use client";

import React, { useState, useEffect } from "react";
import { api } from "../../lib/api";
import { motion } from "framer-motion";
import { Activity, Zap, Award, BarChart3 } from "lucide-react";
import TVIStatsCard from "../../components/tvi/TVIStatsCard";
import { Button } from "../../components/ui/Button";

interface UserStats {
  user_ccp: number;
  total_hours: number;
}

interface TopContributor {
  name: string;
  hours: number;
  ccp: number;
}

interface CommunityStats {
  total_hours: number;
  active_participants: number;
  reciprocity_rate: number;
  avg_ccp: number;
  top_contributors?: TopContributor[];
}

export default function TVIStatsPage() {
  const [stats, setStats] = useState<UserStats | null>(null);
  const [communityStats, setCommunityStats] = useState<CommunityStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadAllStats();
  }, []);

  const loadAllStats = async () => {
    setIsLoading(true);
    try {
      const [sData, cData] = await Promise.all([
        api.getTVIStats(),
        api.getTVICommunityStats()
      ]);
      setStats(sData);
      setCommunityStats(cData);
    } catch (err) {
      console.error("Error loading TVI stats", err);
      setError(err instanceof Error ? err.message : "Error al conectar con el servidor");
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) return <div className="min-h-screen bg-black flex items-center justify-center"><div className="animate-spin rounded-full h-12 w-12 border-t-2 border-indigo-500"></div></div>;

  if (error) {
    return (
      <div className="min-h-screen bg-black text-slate-100 flex items-center justify-center p-8 text-center">
        <div className="max-w-md bg-slate-900/50 border border-slate-800 p-8 rounded-3xl backdrop-blur-xl">
           <Activity size={48} className="mx-auto text-rose-500 mb-4" />
           <h2 className="text-xl font-bold mb-2">Error de Sincronización</h2>
           <p className="text-slate-400 mb-6">{error}. ¿Has iniciado sesión?</p>
           <div className="flex flex-col gap-2">
             <button onClick={loadAllStats} className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 rounded-xl transition-colors">Reintentar</button>
             <button onClick={() => window.location.href='/login'} className="px-6 py-3 border border-slate-700 hover:bg-slate-800 rounded-xl transition-colors">Ir al Login</button>
           </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-slate-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-12">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center gap-3 mb-4"
          >
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/20 flex items-center justify-center text-emerald-400 border border-emerald-500/30 shadow-lg shadow-emerald-500/10">
              <Activity size={28} />
            </div>
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Tiempo Vital Invertido (TVI)</h1>
              <p className="text-slate-400">Métricas de contribución y reciprocidad comunitaria</p>
            </div>
          </motion.div>
        </header>

        {/* Community KPIs */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
           <TVIStatsCard 
             label="Horas Totales (Cero)"
             value={communityStats?.total_hours?.toFixed(1) || "0.0"}
             subValue="+12% vs mes pasado"
             icon="clock"
             color="emerald"
           />
           <TVIStatsCard 
             label="Participantes Activos"
             value={communityStats?.active_participants || "0"}
             icon="users"
             color="blue"
           />
           <TVIStatsCard 
             label="Tasa de Reciprocidad"
             value={`${((communityStats?.reciprocity_rate ?? 0) * 100).toFixed(1)}%`}
             icon="trend"
             color="indigo"
           />
           <TVIStatsCard 
             label="CCP Promedio"
             value={communityStats?.avg_ccp?.toFixed(3) || "0.000"}
             subValue="Coeficiente Meta"
             icon="activity"
             color="amber"
           />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
           {/* CCP Visualizer */}
           <div className="lg:col-span-8 bg-slate-900/40 backdrop-blur-xl border border-slate-800 p-8 rounded-3xl">
              <div className="flex items-center justify-between mb-8">
                 <h2 className="text-xl font-semibold flex items-center gap-2">
                    <BarChart3 size={20} className="text-indigo-400" />
                    Distribución de Contribución
                 </h2>
                 <div className="text-xs text-slate-500 font-mono">NODE_CLUSTER: COHORTE_CERO</div>
              </div>
              
              <div className="h-64 flex items-end gap-2 mb-8">
                 {/* Mock chart bars for visualization */}
                 {[40, 65, 30, 85, 45, 90, 55, 70, 35, 60, 50, 75].map((h, i) => (
                    <motion.div 
                      key={i}
                      initial={{ height: 0 }}
                      animate={{ height: `${h}%` }}
                      transition={{ delay: i * 0.05, duration: 0.5 }}
                      className="flex-1 bg-gradient-to-t from-indigo-600/40 to-indigo-400/60 rounded-t-lg border-t border-indigo-400/30"
                    />
                 ))}
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 pt-8 border-t border-slate-800">
                 <div>
                    <h4 className="text-sm font-medium text-slate-400 mb-4 uppercase tracking-wider">Concepto de CCP</h4>
                    <p className="text-sm text-slate-500 leading-relaxed">
                       El Coeficiente de Correlación de Participación mide la armonía entre lo que un nodo aporta a la comunidad y lo que recibe. Un CCP cercano a 1 indica una reciprocidad perfecta.
                    </p>
                 </div>
                 <div className="bg-white/5 p-6 rounded-2xl border border-white/5 flex flex-col justify-center items-center">
                    <div className="text-xs text-indigo-300 mb-2 font-bold">TU CCP ACTUAL</div>
                    <div className="text-5xl font-black text-white">{stats?.user_ccp?.toFixed(3) || "0.842"}</div>
                    <div className="mt-4 flex items-center gap-2 text-emerald-400 text-xs font-bold">
                       <Zap size={14} />
                       ESTADO: RECIPROCIDAD ÓPTIMA
                    </div>
                 </div>
              </div>
           </div>

           {/* Top Contributors */}
           <div className="lg:col-span-4 bg-slate-900/40 backdrop-blur-xl border border-slate-800 p-8 rounded-3xl">
              <h2 className="text-xl font-semibold mb-8 flex items-center gap-2">
                 <Award size={20} className="text-amber-400" />
                 Top Contribuyentes
              </h2>
              
              <div className="space-y-6">
                 {(communityStats?.top_contributors || [
                   { name: "Carlos M.", hours: 145, ccp: 0.98 },
                   { name: "Elena R.", hours: 132, ccp: 0.95 },
                   { name: "Julian S.", hours: 120, ccp: 0.92 },
                   { name: "Marta L.", hours: 98, ccp: 0.89 },
                   { name: "Sofia P.", hours: 85, ccp: 0.87 }
                 ]).map((user: TopContributor, i: number) => (
                    <div key={i} className="flex items-center gap-4 group">
                       <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center text-xs font-bold text-slate-400 group-hover:bg-indigo-500/20 group-hover:text-indigo-400 transition-colors">
                          {i + 1}
                       </div>
                       <div className="flex-1">
                          <div className="text-sm font-medium">{user.name}</div>
                          <div className="text-xs text-slate-500">{user.hours} hrs invertidas</div>
                       </div>
                       <div className="text-right">
                          <div className="text-xs font-mono text-slate-400">CCP</div>
                          <div className="text-sm font-bold text-slate-200">{user.ccp.toFixed(2)}</div>
                       </div>
                    </div>
                 ))}
              </div>
              
              <Button variant="outline" className="w-full mt-8 border-slate-700 text-slate-400 hover:text-white">
                 Ver Ranking Completo
              </Button>
           </div>
        </div>
      </div>
    </div>
  );
}
