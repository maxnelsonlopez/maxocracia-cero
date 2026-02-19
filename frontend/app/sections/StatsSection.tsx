"""
Stats Section - Landing Page
=============================

Métricas del proyecto con animaciones:
- Tests pasando
- Líneas de código
- Capítulos del libro
- Miembros cohorte

Autor: Kimi (Moonshot AI)
"""

"use client";

import { motion, useInView } from "framer-motion";
import { useRef, useEffect, useState } from "react";
import { 
  CheckCircle2, 
  Code2, 
  BookOpen, 
  Users,
  GitBranch,
  FileText
} from "lucide-react";

const stats = [
  {
    icon: CheckCircle2,
    value: 295,
    suffix: "",
    label: "Tests Pasando",
    description: "Cobertura ~85%",
    color: "text-emerald-400",
  },
  {
    icon: Code2,
    value: 7881,
    suffix: "+",
    label: "Líneas de Código",
    description: "Python + TypeScript",
    color: "text-blue-400",
  },
  {
    icon: BookOpen,
    value: 18,
    suffix: "",
    label: "Capítulos",
    description: "Edición 3 Dinámica",
    color: "text-amber-400",
  },
  {
    icon: Users,
    value: 11,
    suffix: "",
    label: "Cohorte Cero",
    description: "Bogotá, Colombia",
    color: "text-purple-400",
  },
];

const additionalStats = [
  { label: "Commits", value: "50+", icon: GitBranch },
  { label: "Documentos", value: "86", icon: FileText },
  { label: "Calificación", value: "A+", icon: CheckCircle2 },
];

export function StatsSection() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true });

  return (
    <section ref={ref} className="py-24 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Progreso medible
          </h2>
          <p className="text-slate-400 max-w-2xl mx-auto">
            Transparencia radical incluye mostrar el trabajo realizado. 
            Todas las métricas son verificables en el repositorio.
          </p>
        </div>

        {/* Main Stats */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {stats.map((stat, index) => (
            <StatCard
              key={stat.label}
              {...stat}
              index={index}
              isInView={isInView}
            />
          ))}
        </div>

        {/* Additional Stats Bar */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="flex flex-wrap justify-center gap-8 p-6 bg-slate-900/50 border border-slate-800 rounded-2xl"
        >
          {additionalStats.map((stat) => (
            <div key={stat.label} className="flex items-center gap-3">
              <stat.icon className="w-5 h-5 text-slate-500" />
              <div>
                <p className="text-2xl font-bold text-white">{stat.value}</p>
                <p className="text-xs text-slate-400">{stat.label}</p>
              </div>
            </div>
          ))}
        </motion.div>

        {/* Auditoría Badge */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mt-12 text-center"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-500/10 border border-emerald-500/20 rounded-full">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span className="text-sm text-emerald-400">
              Auditoría A+ (9.2/10) — Febrero 2026
            </span>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

interface StatCardProps {
  icon: React.ElementType;
  value: number;
  suffix: string;
  label: string;
  description: string;
  color: string;
  index: number;
  isInView: boolean;
}

function StatCard({ 
  icon: Icon, 
  value, 
  suffix, 
  label, 
  description,
  color,
  index,
  isInView
}: StatCardProps) {
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    if (!isInView) return;

    const duration = 2000;
    const steps = 60;
    const increment = value / steps;
    let current = 0;

    const timer = setInterval(() => {
      current += increment;
      if (current >= value) {
        setDisplayValue(value);
        clearInterval(timer);
      } else {
        setDisplayValue(Math.floor(current));
      }
    }, duration / steps);

    return () => clearInterval(timer);
  }, [isInView, value]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ delay: index * 0.1 }}
      className="p-6 bg-slate-900 border border-slate-800 rounded-2xl text-center hover:border-slate-700 transition-colors"
    >
      <div className={`w-12 h-12 bg-slate-800 rounded-xl flex items-center justify-center mx-auto mb-4 ${color}`}>
        <Icon className="w-6 h-6" />
      </div>
      <div className="text-4xl font-bold text-white mb-1">
        {displayValue.toLocaleString()}{suffix}
      </div>
      <div className="font-medium text-slate-300 mb-1">{label}</div>
      <div className="text-sm text-slate-500">{description}</div>
    </motion.div>
  );
}
