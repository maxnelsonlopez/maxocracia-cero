"use client";

import { motion } from "framer-motion";
import { 
  Home, 
  Utensils, 
  Droplets, 
  Heart, 
  GraduationCap, 
  Briefcase, 
  Users 
} from "lucide-react";

interface SDVScores {
  vivienda: number;
  alimentacion: number;
  agua: number;
  salud: number;
  educacion: number;
  trabajo: number;
  vinculos: number;
}

interface SDVTermometerProps {
  scores: SDVScores;
  size?: "sm" | "md" | "lg";
  showLabels?: boolean;
}

const dimensions = [
  { key: "vivienda", label: "Vivienda", icon: Home },
  { key: "alimentacion", label: "Alimentación", icon: Utensils },
  { key: "agua", label: "Agua", icon: Droplets },
  { key: "salud", label: "Salud", icon: Heart },
  { key: "educacion", label: "Educación", icon: GraduationCap },
  { key: "trabajo", label: "Trabajo", icon: Briefcase },
  { key: "vinculos", label: "Vínculos", icon: Users },
];

export function SDVTermometer({ scores, size = "md", showLabels = true }: SDVTermometerProps) {
  const getBarColor = (score: number) => {
    if (score >= 0.9) return "bg-emerald-500";
    if (score >= 0.7) return "bg-amber-500";
    if (score >= 0.5) return "bg-orange-500";
    return "bg-rose-500";
  };

  const getGlowColor = (score: number) => {
    if (score >= 0.9) return "shadow-emerald-500/40";
    if (score >= 0.7) return "shadow-amber-500/40";
    if (score >= 0.5) return "shadow-orange-500/40";
    return "shadow-rose-500/40";
  };

  const getHeight = () => {
    if (size === "sm") return "h-24";
    if (size === "lg") return "h-48";
    return "h-36";
  };

  const getWidth = () => {
    if (size === "sm") return "w-3";
    if (size === "lg") return "w-6";
    return "w-4";
  };

  return (
    <div className="flex items-end justify-between gap-2 md:gap-4 p-4 glass rounded-2xl border border-slate-800">
      {dimensions.map((dim, idx) => {
        const score = scores[dim.key as keyof SDVScores] || 0;
        const Icon = dim.icon;
        
        return (
          <div key={dim.key} className="flex flex-col items-center gap-3">
            {/* Bar Container */}
            <div className={`relative ${getHeight()} ${getWidth()} bg-slate-900/50 rounded-full overflow-hidden border border-slate-800/50`}>
              {/* Fill */}
              <motion.div
                initial={{ height: 0 }}
                animate={{ height: `${score * 100}%` }}
                transition={{ duration: 1, delay: idx * 0.1, ease: "easeOut" }}
                className={`absolute bottom-0 left-0 right-0 ${getBarColor(score)} shadow-[0_0_15px_rgba(0,0,0,0.5)] ${getGlowColor(score)} shadow-lg`}
              />
            </div>
            
            {/* Icon & Label */}
            <div className="flex flex-col items-center gap-1">
              <div className={`p-1.5 rounded-lg bg-slate-900 border border-slate-800 ${score < 0.5 ? "text-rose-400" : "text-slate-400"}`}>
                <Icon className={size === "sm" ? "w-3 h-3" : "w-4 h-4"} />
              </div>
              {showLabels && (
                <span className="text-[9px] font-bold uppercase tracking-tighter text-slate-500 hidden md:block">
                  {dim.label}
                </span>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
