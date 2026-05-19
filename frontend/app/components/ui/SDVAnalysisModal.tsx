"use client";

import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  X, 
  Info, 
  AlertTriangle, 
  CheckCircle2, 
  Home, 
  Utensils, 
  Droplets, 
  Heart, 
  GraduationCap, 
  Briefcase, 
  Users 
} from "lucide-react";

interface SDVAnalysisModalProps {
  isOpen: boolean;
  onClose: () => void;
  participantName: string;
  scores: Record<string, number>;
  narratives: Record<string, string>;
}

const dimensionIcons: Record<string, React.ElementType> = {
  vivienda: Home,
  alimentacion: Utensils,
  agua: Droplets,
  salud: Heart,
  educacion: GraduationCap,
  trabajo: Briefcase,
  vinculos: Users,
};

export function SDVAnalysisModal({ 
  isOpen, 
  onClose, 
  participantName, 
  scores, 
  narratives 
}: SDVAnalysisModalProps) {
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="absolute inset-0 bg-slate-950/60 backdrop-blur-md"
        />
        
        <motion.div
          initial={{ opacity: 0, scale: 0.9, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.9, y: 20 }}
          className="relative w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl"
        >
          {/* Header */}
          <div className="p-6 border-b border-slate-800 flex items-center justify-between bg-slate-900/50">
            <div>
              <h2 className="text-xl font-bold text-white mb-1">
                Análisis de Dignidad Vital
              </h2>
              <p className="text-xs text-slate-400 uppercase font-black tracking-widest">
                Participante: {participantName}
              </p>
            </div>
            <button 
              onClick={onClose}
              className="p-2 rounded-xl hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Content */}
          <div className="p-6 max-h-[70vh] overflow-y-auto space-y-6">
            {Object.entries(narratives).map(([key, text]) => {
              const score = scores[key] || 0;
              const Icon = dimensionIcons[key] || Info;
              
              let statusColor = "text-emerald-500";
              let bgColor = "bg-emerald-500/5";
              let borderColor = "border-emerald-500/20";
              let StatusIcon = CheckCircle2;

              if (score < 0.5) {
                statusColor = "text-rose-500";
                bgColor = "bg-rose-500/5";
                borderColor = "border-rose-500/20";
                StatusIcon = AlertTriangle;
              } else if (score < 0.9) {
                statusColor = "text-amber-500";
                bgColor = "bg-amber-500/5";
                borderColor = "border-amber-500/20";
                StatusIcon = Info;
              }

              return (
                <div 
                  key={key} 
                  className={`p-4 rounded-2xl border ${borderColor} ${bgColor} flex gap-4 transition-all hover:scale-[1.01]`}
                >
                  <div className={`w-12 h-12 rounded-xl bg-slate-900 border ${borderColor} flex items-center justify-center shrink-0`}>
                    <Icon className={`w-6 h-6 ${statusColor}`} />
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <h4 className="text-sm font-bold text-white uppercase tracking-wider">
                        {key}
                      </h4>
                      <div className="flex items-center gap-2">
                        <span className={`text-xs font-black ${statusColor}`}>
                          {(score * 100).toFixed(0)}%
                        </span>
                        <StatusIcon className={`w-4 h-4 ${statusColor}`} />
                      </div>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed font-medium">
                      {text}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Footer */}
          <div className="p-6 bg-slate-900/80 border-t border-slate-800 text-center">
            <p className="text-[10px] text-slate-500 uppercase font-bold tracking-widest leading-relaxed">
              Este análisis es una proyección algorítmica basada en los últimos seguimientos. <br />
              La Maxocracia prioriza la intervención en dimensiones marcadas como &quot;Violación&quot;.
            </p>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
