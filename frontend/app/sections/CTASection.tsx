/*
 * CTA Section - Landing Page Final
 * =================================
 *
 * Llamado a la acción final:
 * - Mensaje inspirador
 * - CTAs principales
 * - Links a recursos
 *
 * Autor: Kimi (Moonshot AI)
 */

"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { 
  Heart, 
  ArrowRight, 
  Github, 
  BookOpen,
  Mail
} from "lucide-react";

export function CTASection() {
  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto text-center">
        {/* Main CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl sm:text-5xl font-bold text-white mb-6">
            El tiempo es el único recurso{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
              que no recuperas
            </span>
          </h2>
          
          <p className="text-xl text-slate-400 mb-8 max-w-2xl mx-auto">
            Ayúdanos a construir un sistema económico que honre ese hecho. 
            Tu contribución sostiene el desarrollo de herramientas abiertas 
            para una economía más coherente.
          </p>

          {/* Primary CTAs */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
            <Link
              href="/upgrade"
              className="group flex items-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold rounded-xl transition-all hover:scale-105 hover:shadow-lg hover:shadow-emerald-500/25"
            >
              <Heart className="w-5 h-5" />
              Ser Contribuidor
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>

            <a
              href="https://github.com/maxnelsonlopez/maxocracia-cero"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 px-8 py-4 bg-slate-800/50 hover:bg-slate-800 text-white font-medium rounded-xl border border-slate-700 transition-all"
            >
              <Github className="w-5 h-5" />
              Ver en GitHub
            </a>
          </div>
        </motion.div>

        {/* Secondary Resources */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
          className="p-8 bg-slate-900/50 border border-slate-800 rounded-2xl"
        >
          <h3 className="text-lg font-semibold text-white mb-6">
            Recursos gratuitos
          </h3>
          
          <div className="grid sm:grid-cols-3 gap-4">
            <ResourceLink
              href="https://github.com/maxnelsonlopez/maxocracia-cero/blob/main/docs/book/edicion_3_dinamica/libro_completo_310126.md"
              icon={BookOpen}
              label="Libro Completo"
              description="18 capítulos en Markdown"
            />
            <ResourceLink
              href="http://localhost:5001/vhv-calculator.html"
              icon={Heart}
              label="Calculadora VHV"
              description="Calcula el valor real"
            />
            <ResourceLink
              href="mailto:maxlopeztutor@gmail.com"
              icon={Mail}
              label="Contacto"
              description="maxlopeztutor@gmail.com"
            />
          </div>
        </motion.div>

        {/* Final Quote */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4 }}
          className="mt-16"
        >
          <blockquote className="text-2xl sm:text-3xl font-light text-slate-300 italic">
            "La verdad no necesita ser defendida. 
            Solo necesita expandirse."
          </blockquote>
          <cite className="text-slate-500 mt-4 block not-italic">
            — Axioma 4, Maxocracia
          </cite>
        </motion.div>
      </div>
    </section>
  );
}

interface ResourceLinkProps {
  href: string;
  icon: React.ElementType;
  label: string;
  description: string;
}

function ResourceLink({ href, icon: Icon, label, description }: ResourceLinkProps) {
  const isExternal = href.startsWith("http") || href.startsWith("mailto");
  
  const content = (
    <div className="p-4 bg-slate-800/50 rounded-xl hover:bg-slate-800 transition-colors text-left">
      <div className="flex items-center gap-2 mb-1">
        <Icon className="w-4 h-4 text-emerald-400" />
        <span className="font-medium text-white">{label}</span>
      </div>
      <p className="text-sm text-slate-400">{description}</p>
    </div>
  );

  if (isExternal) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer">
        {content}
      </a>
    );
  }

  return <Link href={href}>{content}</Link>;
}
