"""
Página de Upgrade - Contribuidor Consciente
============================================

Página de suscripción ética que respeta los principios de Maxocracia:
- Transparencia radical (precios públicos, costos visibles)
- Igualdad temporal (ajuste PPP)
- No-explotación (honor system, sin coerción)

Autor: Kimi (Moonshot AI)
Fecha: Febrero 2026
"""

import { Metadata } from "next";
import UpgradePageClient from "./UpgradePageClient";

export const metadata: Metadata = {
  title: "Contribuidor Consciente - Maxocracia",
  description: "Contribuye a la sostenibilidad de Maxocracia. Precios ajustados por paridad de poder adquisitivo (PPP). Transparencia radical.",
};

export default function UpgradePage() {
  return <UpgradePageClient />;
}
