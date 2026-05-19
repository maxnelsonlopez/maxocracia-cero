"use client";

import React, { useEffect, useState } from "react";
import { 
  Activity, 
  Users, 
  AlertTriangle, 
  Info,
  ChevronRight,
  Search
} from "lucide-react";
import { SDVTermometer } from "../../components/ui/SDVTermometer";
import { SDVAnalysisModal } from "../../components/ui/SDVAnalysisModal";
import { motion } from "framer-motion";
import { apiFetch } from "../../lib/api";

interface CommunitySDV {
  average_overall: number;
  dimensions: {
    vivienda: number;
    alimentacion: number;
    agua: number;
    salud: number;
    educacion: number;
    trabajo: number;
    vinculos: number;
  };
  participant_count: number;
  community_narrative?: string;
}

interface ParticipantSDV {
  participant_id: number;
  participant_name: string;
  sdv_scores: {
    vivienda: number;
    alimentacion: number;
    agua: number;
    salud: number;
    educacion: number;
    trabajo: number;
    vinculos: number;
  };
  average_score: number;
  narratives: Record<string, string>;
}

export default function SDVAdminPage() {
  const [communityData, setCommunityData] = useState<CommunitySDV | null>(null);
  const [participants, setParticipants] = useState<ParticipantSDV[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  
  // Modal state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedParticipant, setSelectedParticipant] = useState<ParticipantSDV | null>(null);

  const openAnalysis = (p: ParticipantSDV) => {
    setSelectedParticipant(p);
    setIsModalOpen(true);
  };

  useEffect(() => {
    const fetchSDVData = async () => {
      try {
        // 1. Fetch community stats
        const commRes = await apiFetch("/forms/sdv/community");
        const commData = await commRes.json();
        setCommunityData(commData);

        // 2. Fetch all participants to get their individual SDV
        const partListRes = await apiFetch("/forms/participants?limit=50");
        const partListData = await partListRes.json();
        
        // 3. Fetch SDV scores for each participant
        if (partListData.participants && Array.isArray(partListData.participants)) {
          const scoresPromises = partListData.participants.map(async (p: { id: number }) => {
            const res = await apiFetch(`/forms/sdv/participant/${p.id}`);
            return res.json();
          });
          
          const scores = await Promise.all(scoresPromises);
          setParticipants(scores);
        } else {
          setParticipants([]);
        }
      } catch (error) {
        console.error("Error fetching SDV data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSDVData();
  }, []);

  const filteredParticipants = participants.filter(p => 
    p.participant_name.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Activity className="w-8 h-8 text-emerald-500 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-6xl">
      {/* Header Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="col-span-1 md:col-span-2 glass p-8 rounded-3xl border border-slate-800 flex flex-col md:flex-row items-center gap-8"
        >
          <div className="text-center md:text-left">
            <h2 className="text-sm font-black uppercase tracking-[0.2em] text-slate-500 mb-2">
              Estado de Dignidad Comunitaria
            </h2>
            <div className="flex items-baseline gap-2">
              <span className="text-6xl font-black text-white">
                {(communityData?.average_overall || 0) * 100}%
              </span>
              <span className="text-emerald-500 font-bold text-xl">Cobertura</span>
            </div>
            <p className="text-slate-400 text-xs mt-4 max-w-xs uppercase leading-relaxed font-medium">
              {communityData?.community_narrative || "Calculando síntesis vital de la cohorte..."}
            </p>
          </div>
          
          <div className="flex-1 w-full">
            {communityData && <SDVTermometer scores={communityData.dimensions} size="lg" />}
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass p-8 rounded-3xl border border-slate-800 bg-rose-500/5 flex flex-col justify-between"
        >
          <div>
            <div className="w-12 h-12 rounded-2xl bg-rose-500/20 flex items-center justify-center mb-6">
              <AlertTriangle className="w-6 h-6 text-rose-500" />
            </div>
            <h3 className="text-lg font-bold text-white mb-2">Puntos Críticos</h3>
            <p className="text-slate-400 text-xs uppercase font-medium leading-relaxed">
              Dimensiones con cobertura inferior al 70% requieren intervención inmediata de la comunidad.
            </p>
          </div>
          
          <div className="mt-6 space-y-2">
            {communityData && Object.entries(communityData.dimensions)
              .filter(([, score]) => score < 0.7)
              .map(([dim, score]) => (
                <div key={dim} className="flex items-center justify-between p-3 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="text-[10px] font-bold uppercase text-slate-300">{dim}</span>
                  <span className="text-[10px] font-bold text-rose-500">{(score * 100).toFixed(0)}%</span>
                </div>
              ))
            }
            {communityData && Object.entries(communityData.dimensions).every(([, s]) => s >= 0.7) && (
                <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-center">
                    <span className="text-[10px] font-bold uppercase text-emerald-500">Sin violaciones críticas</span>
                </div>
            )}
          </div>
        </motion.div>
      </div>

      {/* Search and List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Users className="w-5 h-5 text-emerald-500" />
                Dignidad por Participante
            </h2>
            <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input 
                    type="text" 
                    placeholder="BUSCAR PARTICIPANTE..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="pl-10 pr-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-[10px] font-bold text-white focus:outline-none focus:border-emerald-500 transition-all w-64"
                />
            </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredParticipants.map((p, idx) => (
                <motion.div 
                    key={p.participant_id}
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: idx * 0.05 }}
                    className="glass p-6 rounded-3xl border border-slate-800 hover:border-slate-700 transition-all group"
                >
                    <div className="flex items-center justify-between mb-6">
                        <div className="flex items-center gap-3">
                            <div className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold text-sm ${
                                p.average_score < 0.7 ? "bg-rose-500/20 text-rose-500" : "bg-emerald-500/20 text-emerald-500"
                            }`}>
                                {p.participant_name.substring(0, 2).toUpperCase()}
                            </div>
                            <div>
                                <h4 className="text-sm font-bold text-white group-hover:text-emerald-400 transition-colors">
                                    {p.participant_name}
                                </h4>
                                <span className="text-[9px] font-black uppercase text-slate-500 tracking-widest">
                                    ID: {p.participant_id.toString().padStart(4, '0')}
                                </span>
                            </div>
                        </div>
                        <div className="text-right">
                            <div className={`text-xl font-black ${
                                p.average_score < 0.7 ? "text-rose-500" : "text-emerald-500"
                            }`}>
                                {(p.average_score * 100).toFixed(0)}%
                            </div>
                            <div className="text-[9px] font-bold uppercase text-slate-500">Índice SDV</div>
                        </div>
                    </div>

                    <SDVTermometer scores={p.sdv_scores} size="sm" showLabels={false} />
                    
                    <div className="mt-4 flex items-center justify-between">
                        <div className="flex gap-1">
                            {Object.entries(p.sdv_scores).map(([dim, score]) => (
                                score < 0.7 && (
                                    <div key={dim} className="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse" title={`${dim}: ${(score*100).toFixed(0)}%`} />
                                )
                            ))}
                        </div>
                        <button 
                            onClick={() => openAnalysis(p)}
                            className="text-[9px] font-black uppercase tracking-widest text-slate-400 hover:text-white flex items-center gap-1 transition-colors"
                        >
                            Ver Análisis Completo
                            <ChevronRight className="w-3 h-3" />
                        </button>
                    </div>
                </motion.div>
            ))}
        </div>
      </div>

      {/* Legend / Info */}
      <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 flex items-start gap-4">
        <Info className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" />
        <div>
            <h4 className="text-xs font-bold text-slate-300 uppercase mb-2">Metodología de Estimación SDV</h4>
            <p className="text-[10px] text-slate-500 uppercase leading-relaxed font-medium">
                Este panel muestra una estimación cualitativa basada en los formularios registrados. <br />
                <span className="text-rose-500/80">Rojo (0-49%):</span> Violación probable de derechos fundamentales. <br />
                <span className="text-amber-500/80">Ámbar (50-89%):</span> Vulnerabilidad o riesgo de insostenibilidad vital. <br />
                <span className="text-emerald-500/80">Verde (90-100%):</span> Nivel de dignidad garantizado según estándares Maxocracia.
            </p>
        </div>
      </div>

      {/* Analysis Modal */}
      {selectedParticipant && (
        <SDVAnalysisModal 
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          participantName={selectedParticipant.participant_name}
          scores={selectedParticipant.sdv_scores}
          narratives={selectedParticipant.narratives}
        />
      )}
    </div>
  );
}
