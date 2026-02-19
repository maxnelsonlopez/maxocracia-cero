"""
Hero Section - Maxocracia Landing
==================================

Sección hero con:
- Headline impactante
- Subtítulo explicativo
- CTAs principales
- Elementos visuales animados

Autor: Kimi (Moonshot AI)
"""

"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { 
  ArrowRight, 
  Play, 
  Sparkles,
  Clock,
  Heart,
  Scale
} from "lucide-react";

export function HeroSection() {
  return (
    <section className="relative min-h-[90vh] flex items-center justify-center px-4 sm:px-6 lg:px-8 overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          animate={{ 
            rotate: 360,
            scale: [1, 1.1, 1]
          }}
          transition={{ 
            rotate: { duration: 60, repeat: Infinity, ease: "linear" },
            scale: { duration: 8, repeat: Infinity, ease: "easeInOut" }
          }}
          className="absolute -top-1/2 -right-1/2 w-[1000px] h-[1000px] border border-slate-800/30 rounded-full"
        />
        <motion.div
          animate={{ rotate: -360 }}
          transition={{ duration: 80, repeat: Infinity, ease: "linear" }}
          className="absolute -bottom-1/2 -left-1/2 w-[800px] h-[800px] border border-slate-800/20 rounded-full"
        />
      </div>

      <div className="relative max-w-5xl mx-auto text-center">
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Link
            href="/upgrade"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-sm font-medium mb-8 hover:bg-emerald-500/20 transition-colors"
          >
            <Sparkles className="w-4 h-4" />
            <span>Fase 2: Sostenibilidad Económica</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </motion.div>

        {/* Main Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.5 }}
          className="text-5xl sm:text-6xl lg:text-7xl font-bold text-white mb-6 leading-tight"
        >
          La economía del{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
            tiempo vital
          </span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="text-xl text-slate-400 mb-8 max-w-2xl mx-auto leading-relaxed"
        >
          Maxocracia propone reemplazar la contabilidad basada en dinero fiduciario 
          por una <strong className="text-slate-200">contabilidad de la vida</strong>. 
          Tu tiempo consciente es el recurso más escaso del universo.
        </motion.p>

        {/* CTAs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16"
        >
          <Link
            href="/upgrade"
            className="group flex items-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold rounded-xl transition-all hover:scale-105 hover:shadow-lg hover:shadow-emerald-500/25"
          >
            <Heart className="w-5 h-5" />
            Contribuir al proyecto
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
          
          <a
            href="https://github.com/maxnelsonlopez/maxocracia-cero/blob/main/docs/book/edicion_3_dinamica/libro_completo_310126.md"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-8 py-4 bg-slate-800/50 hover:bg-slate-800 text-white font-medium rounded-xl border border-slate-700 transition-all"
          >
            <Play className="w-5 h-5" />
            Leer el libro (18 capítulos)
          </a>
        </motion.div>

        {/* Key concepts */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.5 }}
          className="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-3xl mx-auto"
        >
          <ConceptCard
            icon={Clock}
            title="TVI"
            description="Tiempo Vital Indexado. Cada segundo como NFT existencial."
          />
          <ConceptCard
            icon={Scale}
            title="VHV"
            description="Vector de Huella Vital. [T, V, R] = Tiempo, Vidas, Recursos."
          />
          <ConceptCard
            icon={Heart}
            title="Maxo"
            description="Moneda anclada al costo vital real, no a la deuda."
          />
        </motion.div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1, duration: 0.5 }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
      >
        <motion.div
          animate={{ y: [0, 8, 0] }}
          transition={{ duration: 1.5, repeat: Infinity }}
          className="w-6 h-10 border-2 border-slate-700 rounded-full flex items-start justify-center p-2"
        >
          <div className="w-1 h-2 bg-slate-500 rounded-full" />
        </motion.div>
      </motion.div>
    </section>
  );
}

function ConceptCard({ 
  icon: Icon, 
  title, 
  description 
}: { 
  icon: React.ElementType; 
  title: string; 
  description: string;
}) {
  return (
    <div className="p-6 bg-slate-900/50 backdrop-blur-sm border border-slate-800 rounded-2xl hover:border-slate-700 transition-colors">
      <div className="w-10 h-10 bg-emerald-500/10 rounded-lg flex items-center justify-center mb-4">
        <Icon className="w-5 h-5 text-emerald-400" />
      </div>
      <h3 className="font-semibold text-white mb-2">{title}</h3>
      <p className="text-sm text-slate-400">{description}</p>
    </div>
  );
}
