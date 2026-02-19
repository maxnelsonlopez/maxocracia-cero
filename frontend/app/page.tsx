"""
Landing Page - Maxocracia
==========================

Página principal que sirve como portal al ecosistema:
- Hero impactante con valor proposición
- Demo interactiva del VHV
- Features principales
- CTA a suscripción
- Stats del proyecto

Autor: Kimi (Moonshot AI)
"""

import { Metadata } from "next";
import { HeroSection } from "./sections/HeroSection";
import { VHVPreview } from "./sections/VHVPreview";
import { FeaturesGrid } from "./sections/FeaturesGrid";
import { StatsSection } from "./sections/StatsSection";
import { CTASection } from "./sections/CTASection";

export const metadata: Metadata = {
  title: "Maxocracia - Sistema Operativo para una Civilización Coherente",
  description: "Reemplaza la contabilidad del dinero por la contabilidad de la vida. El tiempo vital es el recurso más escaso del universo.",
};

export default function HomePage() {
  return (
    <div className="relative">
      {/* Background gradient */}
      <div className="fixed inset-0 bg-slate-950 -z-10">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl" />
      </div>

      <HeroSection />
      <VHVPreview />
      <FeaturesGrid />
      <StatsSection />
      <CTASection />
    </div>
  );
}
