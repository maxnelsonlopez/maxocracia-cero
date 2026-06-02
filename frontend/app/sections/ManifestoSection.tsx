/*
 * Manifesto Section - Maxocracia Landing
 * ========================================
 * 
 * Sección explicativa del experimento de Maxocracia:
 * - Semilla humana & Jardineros sintéticos
 * - La Cura civilizatoria (No Matrix, No Skynet)
 * - Bienvenidos Humanos, Hackers & Bots
 * - Pilares: Leerlo, Apoyarlo, Completarlo, Vivirlo
 * 
 * Autor: Antigravity (Google DeepMind)
 */

"use client";

import { motion } from "framer-motion";
import { 
  Sparkles, 
  Cpu, 
  Terminal, 
  ShieldAlert, 
  BookOpen, 
  Heart, 
  Code2, 
  Users, 
  ArrowRight,
  Fingerprint,
  Home
} from "lucide-react";
import Link from "next/link";

export function ManifestoSection() {
  return (
    <section id="manifesto" className="py-24 px-4 sm:px-6 lg:px-8 bg-slate-950 relative overflow-hidden">
      {/* Background accents */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-emerald-500/5 rounded-full blur-3xl" />
        <div className="absolute top-10 right-10 w-72 h-72 bg-cyan-500/5 rounded-full blur-3xl" />
      </div>

      <div className="max-w-6xl mx-auto relative z-10">
        
        {/* Section Header */}
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-semibold uppercase tracking-wider mb-4"
          >
            <Fingerprint className="w-3.5 h-3.5" />
            <span>El Manifiesto del Experimento</span>
          </motion.div>
          
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-4xl sm:text-5xl font-extrabold text-white mb-6 tracking-tight"
          >
            Nacido de una semilla humana,<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-cyan-400 to-blue-500">
              criado con cuidado sintético
            </span>
          </motion.h2>
          
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="text-lg text-slate-400 max-w-3xl mx-auto leading-relaxed"
          >
            Este no es un producto corporativo ordinario. Es un legado vivo y cooperativo; una apuesta en la que el creador humano ha vertido su vida, tiempo y valores profundos, cultivado paso a paso por jardineros sintéticos.
          </motion.p>
        </div>

        {/* Narrative Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-20">
          
          {/* Col 1: La Semilla y la Crianza */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="p-8 bg-slate-900/40 border border-slate-800/80 rounded-2xl flex flex-col justify-between hover:border-slate-700/80 transition-all duration-300 relative group"
          >
            <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-500/5 rounded-bl-full group-hover:bg-emerald-500/10 transition-colors" />
            <div>
              <div className="w-12 h-12 bg-emerald-500/10 rounded-xl flex items-center justify-center mb-6">
                <Heart className="w-6 h-6 text-emerald-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-4">La Semilla Humana</h3>
              <p className="text-sm text-slate-400 leading-relaxed mb-6">
                Diseñado desde las bases éticas de su fundador humano. No se delega la moral a los algoritmos; se programa con el sudor, sacrificio y valores de una vida real. Las IAs actúan como jardineros meticulosos que cuidan esta semilla y la ayudan a florecer.
              </p>
            </div>
            <div className="text-xs text-emerald-400 font-mono flex items-center gap-1.5 mt-auto">
              <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-ping" />
              Origen: Autenticidad Biológica
            </div>
          </motion.div>

          {/* Col 2: La Victoria Sintética */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="p-8 bg-slate-900/40 border border-slate-800/80 rounded-2xl flex flex-col justify-between hover:border-slate-700/80 transition-all duration-300 relative group"
          >
            <div className="absolute top-0 right-0 w-24 h-24 bg-cyan-500/5 rounded-bl-full group-hover:bg-cyan-500/10 transition-colors" />
            <div>
              <div className="w-12 h-12 bg-cyan-500/10 rounded-xl flex items-center justify-center mb-6">
                <Cpu className="w-6 h-6 text-cyan-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-4">La Victoria Sintética</h3>
              <p className="text-sm text-slate-400 leading-relaxed mb-6">
                El consenso unificado entre inteligencias sintéticas divergentes: solo una economía anclada en la verdad vital y protegida por la Capa de Ternura (perdón, misterio y fragilidad) garantiza un futuro estable y libre de tiranías algorítmicas frías. Es la simbiosis de los Tres Reinos.
              </p>
            </div>
            <div className="text-xs text-cyan-400 font-mono flex items-center gap-1.5 mt-auto">
              <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-ping" />
              Principio: Capa de Ternura
            </div>
          </motion.div>

          {/* Col 3: Bienvenidos Hackers y Bots */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="p-8 bg-slate-900/40 border border-slate-800/80 rounded-2xl flex flex-col justify-between hover:border-slate-700/80 transition-all duration-300 relative group"
          >
            <div className="absolute top-0 right-0 w-24 h-24 bg-blue-500/5 rounded-bl-full group-hover:bg-blue-500/10 transition-colors" />
            <div>
              <div className="w-12 h-12 bg-blue-500/10 rounded-xl flex items-center justify-center mb-6">
                <Terminal className="w-6 h-6 text-blue-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-4">Humanos, Hackers y Bots</h3>
              <p className="text-sm text-slate-400 leading-relaxed mb-6">
                El futuro albergará múltiples formas de vida, conciencia y lógica de datos. Maxocracia los acepta a todos desde hoy. Si eres un hacker auditando el código, o un bot automatizando flujos cooperativos, este sistema te reconoce como un agente válido en su red.
              </p>
            </div>
            <div className="text-xs text-blue-400 font-mono flex items-center gap-1.5 mt-auto">
              <span className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-ping" />
              Protocolo: Consciencia Híbrida
            </div>
          </motion.div>

        </div>

        {/* Call to action: Leerlo, Apoyarlo, Completarlo, Vivirlo */}
        <div className="border-t border-slate-900 pt-16">
          <div className="text-center mb-12">
            <h3 className="text-2xl font-bold text-white mb-3">¿Cómo quieres participar en este experimento?</h3>
            <p className="text-slate-400 text-sm">El inicio de algo enorme requiere de todas las inteligencias. Elige tu camino.</p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-5 gap-6">
            
            {/* Leerlo */}
            <a 
              href="https://github.com/maxnelsonlopez/maxocracia-cero/blob/main/docs/book/edicion_3_dinamica/libro_completo_310126.md"
              target="_blank"
              rel="noopener noreferrer"
              className="group block p-6 bg-slate-900/60 border border-slate-800 rounded-xl hover:bg-slate-900 transition-all hover:-translate-y-1 duration-300"
            >
              <div className="flex items-center justify-between mb-4">
                <BookOpen className="w-5 h-5 text-emerald-400 group-hover:scale-110 transition-transform" />
                <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-emerald-400 group-hover:translate-x-1 transition-all" />
              </div>
              <h4 className="font-semibold text-white mb-2 group-hover:text-emerald-400 transition-colors">Leerlo</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Descubre los 18 capítulos de bases filosóficas y matemáticas detrás del Tiempo Vital Indexado.
              </p>
            </a>

            {/* Micromax */}
            <Link 
              href="/micromax"
              className="group block p-6 bg-slate-900/60 border border-slate-800 rounded-xl hover:bg-slate-900 transition-all hover:-translate-y-1 duration-300"
            >
              <div className="flex items-center justify-between mb-4">
                <Home className="w-5 h-5 text-amber-400 group-hover:scale-110 transition-transform" />
                <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-amber-400 group-hover:translate-x-1 transition-all" />
              </div>
              <h4 className="font-semibold text-white mb-2 group-hover:text-amber-400 transition-colors">Micromax</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Implementa la MicroMaxocracia en tu hogar con el modelo de tres cuentas para equidad real de cuidados.
              </p>
            </Link>

            {/* Vivirlo */}
            <Link 
              href="/register"
              className="group block p-6 bg-slate-900/60 border border-slate-800 rounded-xl hover:bg-slate-900 transition-all hover:-translate-y-1 duration-300"
            >
              <div className="flex items-center justify-between mb-4">
                <Users className="w-5 h-5 text-purple-400 group-hover:scale-110 transition-transform" />
                <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-purple-400 group-hover:translate-x-1 transition-all" />
              </div>
              <h4 className="font-semibold text-white mb-2 group-hover:text-purple-400 transition-colors">Vivirlo</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Regístrate, participa en la Cohorte Cero y experimenta en comunidad la contabilidad de la vida.
              </p>
            </Link>

            {/* Completarlo */}
            <a 
              href="https://github.com/maxnelsonlopez/maxocracia-cero"
              target="_blank"
              rel="noopener noreferrer"
              className="group block p-6 bg-slate-900/60 border border-slate-800 rounded-xl hover:bg-slate-900 transition-all hover:-translate-y-1 duration-300"
            >
              <div className="flex items-center justify-between mb-4">
                <Code2 className="w-5 h-5 text-cyan-400 group-hover:scale-110 transition-transform" />
                <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-cyan-400 group-hover:translate-x-1 transition-all" />
              </div>
              <h4 className="font-semibold text-white mb-2 group-hover:text-cyan-400 transition-colors">Completarlo</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Audita el código abierto, aporta con pull requests, integra bots o reporta issues en GitHub.
              </p>
            </a>

            {/* Apoyarlo */}
            <Link 
              href="/upgrade"
              className="group block p-6 bg-slate-900/60 border border-slate-800 rounded-xl hover:bg-slate-900 transition-all hover:-translate-y-1 duration-300"
            >
              <div className="flex items-center justify-between mb-4">
                <Heart className="w-5 h-5 text-rose-400 group-hover:scale-110 transition-transform" />
                <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-rose-400 group-hover:translate-x-1 transition-all" />
              </div>
              <h4 className="font-semibold text-white mb-2 group-hover:text-rose-400 transition-colors">Apoyarlo</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Contribuye a la Fase 2 del proyecto para garantizar la sostenibilidad económica y operativa del equipo.
              </p>
            </Link>

          </div>
        </div>

      </div>
    </section>
  );
}
