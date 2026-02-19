"""
Features Grid Section - Landing Page
=====================================

Grid de características principales del proyecto:
- 4 capas de Maxocracia
- Features con iconos
- Hover effects

Autor: Kimi (Moonshot AI)
"""

"use client";

import { motion } from "framer-motion";
import { 
  BookOpen, 
  Coins, 
  Home, 
  Shield,
  Zap,
  Users,
  Globe,
  Lock
} from "lucide-react";
import Link from "next/link";

const features = [
  {
    icon: BookOpen,
    title: "Teoría Fundacional",
    description: "18 capítulos que establecen los axiomas matemáticos y filosóficos del sistema. Victoria Sintética como pilar lógico.",
    status: "Completado",
    statusColor: "text-emerald-400 bg-emerald-400/10",
    href: "https://github.com/maxnelsonlopez/maxocracia-cero/blob/main/docs/book/edicion_3_dinamica/libro_completo_310126.md",
    external: true,
  },
  {
    icon: Coins,
    title: "Economía VHV",
    description: "Calculadora de Vector de Huella Vital, sistema TVI con detección de overlap, y API REST completa.",
    status: "Operativo",
    statusColor: "text-emerald-400 bg-emerald-400/10",
    href: "http://localhost:5001/vhv-calculator.html",
    external: true,
  },
  {
    icon: Home,
    title: "MicroMaxocracia",
    description: "Manual de equidad doméstica con el Modelo de 3 Cuentas (CDD, CEH, TED). Próximo: apps para 30 hogares piloto.",
    status: "Documentado",
    statusColor: "text-blue-400 bg-blue-400/10",
    href: "#",
    external: false,
  },
  {
    icon: Shield,
    title: "MaxoContracts",
    description: "Contratos inteligentes éticos con oráculo sintético. 5 bloques modulares implementados en Python + API REST.",
    status: "MVP Listo",
    statusColor: "text-amber-400 bg-amber-400/10",
    href: "/contracts/builder",
    external: false,
  },
];

const principles = [
  {
    icon: Zap,
    title: "Igualdad Temporal",
    description: "El tiempo de cada persona vale igual. Precios ajustados por PPP.",
  },
  {
    icon: Users,
    title: "No Explotación",
    description: "Sin dark patterns. Cancelación libre. Honor system.",
  },
  {
    icon: Globe,
    title: "Transparencia Radical",
    description: "Todos los flujos financieros públicos y auditables.",
  },
  {
    icon: Lock,
    title: "Privacidad",
    description: "Datos personales nunca vendidos. Código open source.",
  },
];

export function FeaturesGrid() {
  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 bg-slate-900/30">
      <div className="max-w-6xl mx-auto">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Cuatro capas de coherencia
          </h2>
          <p className="text-slate-400 max-w-2xl mx-auto">
            Maxocracia no es solo teoría. Es un sistema operativo completo 
            que implementa la contabilidad de la vida en 4 niveles.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 gap-6 mb-20">
          {features.map((feature, index) => (
            <FeatureCard key={feature.title} {...feature} index={index} />
          ))}
        </div>

        {/* Principles Section */}
        <div className="text-center mb-12">
          <h3 className="text-2xl font-bold text-white mb-4">
            Principios No Negociables
          </h3>
          <p className="text-slate-400">
            Cada decisión técnica y económica respeta estos axiomas.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {principles.map((principle, index) => (
            <PrincipleCard key={principle.title} {...principle} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
}

interface FeatureCardProps {
  icon: React.ElementType;
  title: string;
  description: string;
  status: string;
  statusColor: string;
  href: string;
  external?: boolean;
  index: number;
}

function FeatureCard({ 
  icon: Icon, 
  title, 
  description, 
  status, 
  statusColor,
  href,
  external,
  index
}: FeatureCardProps) {
  const CardContent = (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.1 }}
      className="group h-full p-6 bg-slate-900 border border-slate-800 rounded-2xl hover:border-slate-700 transition-all hover:shadow-lg hover:shadow-slate-900/50"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="w-12 h-12 bg-slate-800 rounded-xl flex items-center justify-center group-hover:bg-emerald-500/10 transition-colors">
          <Icon className="w-6 h-6 text-emerald-400" />
        </div>
        <span className={`px-2 py-1 rounded text-xs font-medium ${statusColor}`}>
          {status}
        </span>
      </div>
      
      <h3 className="text-xl font-semibold text-white mb-2 group-hover:text-emerald-400 transition-colors">
        {title}
      </h3>
      <p className="text-slate-400 text-sm leading-relaxed">
        {description}
      </p>
    </motion.div>
  );

  if (external) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" className="block h-full">
        {CardContent}
      </a>
    );
  }

  return (
    <Link href={href} className="block h-full">
      {CardContent}
    </Link>
  );
}

interface PrincipleCardProps {
  icon: React.ElementType;
  title: string;
  description: string;
  index: number;
}

function PrincipleCard({ 
  icon: Icon, 
  title, 
  description,
  index
}: PrincipleCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.1 }}
      className="p-4 bg-slate-900/50 border border-slate-800 rounded-xl text-center hover:bg-slate-800/50 transition-colors"
    >
      <div className="w-10 h-10 bg-slate-800 rounded-lg flex items-center justify-center mx-auto mb-3">
        <Icon className="w-5 h-5 text-emerald-400" />
      </div>
      <h4 className="font-medium text-white mb-1">{title}</h4>
      <p className="text-xs text-slate-400">{description}</p>
    </motion.div>
  );
}
