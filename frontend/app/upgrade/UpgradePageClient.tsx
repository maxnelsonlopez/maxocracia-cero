"""
Cliente de Upgrade - Lógica interactiva
========================================

Componente cliente que maneja:
- Selección de tier
- Cálculo PPP
- Integración con Stripe Checkout
- Gestión de estado de suscripción

Autor: Kimi (Moonshot AI)
"""

"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Check, 
  X, 
  Shield, 
  Zap, 
  Users, 
  Heart,
  Globe,
  Calculator,
  Sparkles,
  ArrowRight,
  Loader2
} from "lucide-react";

// Tipos
interface TierConfig {
  id: string;
  name: string;
  description: string;
  basePrice: number;
  benefits: string[];
  limitations?: string[];
  icon: React.ReactNode;
  popular?: boolean;
}

interface PPPData {
  country: string;
  code: string;
  factor: number;
  adjustedPrice: number;
}

// Configuración de tiers
const TIERS: TierConfig[] = [
  {
    id: "free",
    name: "Free",
    description: "Acceso básico a la filosofía Maxocracia",
    basePrice: 0,
    benefits: [
      "Acceso completo al libro (18 capítulos)",
      "Calculadora VHV básica (10 cálculos/día)",
      "Nexus Simulator - modo limitado",
      "Participación en GitHub Discussions",
    ],
    limitations: [
      "Sin soporte prioritario",
      "Sin acceso anticipado a funciones",
    ],
    icon: <Heart className="w-6 h-6" />,
  },
  {
    id: "contributor",
    name: "Contributor",
    description: "Apoya la sostenibilidad del proyecto",
    basePrice: 25,
    benefits: [
      "Todo lo del plan Free",
      "Dashboard avanzado con métricas",
      "Soporte prioritario (24h respuesta)",
      "Acceso anticipado a funciones",
      "Badge 'Contribuidor' en perfil",
      "Sesiones grupales mensuales",
      "API: 1000 cálculos/día",
    ],
    icon: <Zap className="w-6 h-6" />,
    popular: true,
  },
  {
    id: "enterprise",
    name: "Enterprise",
    description: "Para organizaciones que implementan Maxocracia",
    basePrice: 200,
    benefits: [
      "Todo lo del plan Contributor",
      "Consultoría de implementación",
      "Auditoría VHV personalizada",
      "White-label de MaxoContracts",
      "Soporte dedicado (4h respuesta)",
      "API: Llamadas ilimitadas",
      "SLA garantizado",
    ],
    icon: <Shield className="w-6 h-6" />,
  },
];

// Países con ajuste PPP
const PPP_COUNTRIES = [
  { code: "CO", name: "Colombia", factor: 0.35 },
  { code: "AR", name: "Argentina", factor: 0.25 },
  { code: "VE", name: "Venezuela", factor: 0.15 },
  { code: "MX", name: "México", factor: 0.45 },
  { code: "BR", name: "Brasil", factor: 0.40 },
  { code: "PE", name: "Perú", factor: 0.35 },
  { code: "CL", name: "Chile", factor: 0.50 },
  { code: "US", name: "Estados Unidos", factor: 1.00 },
  { code: "CA", name: "Canadá", factor: 1.00 },
  { code: "GB", name: "Reino Unido", factor: 0.95 },
  { code: "DE", name: "Alemania", factor: 0.90 },
  { code: "ES", name: "España", factor: 0.70 },
  { code: "FR", name: "Francia", factor: 0.90 },
];

export default function UpgradePageClient() {
  const [selectedTier, setSelectedTier] = useState<string>("contributor");
  const [countryCode, setCountryCode] = useState<string>("CO");
  const [monthlyIncome, setMonthlyIncome] = useState<number | "">("");
  const [isLoading, setIsLoading] = useState(false);
  const [stripeConfigured, setStripeConfigured] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  // Verificar configuración de Stripe al cargar
  useEffect(() => {
    fetch("http://localhost:5001/stripe/config")
      .then((res) => res.json())
      .then((data) => {
        setStripeConfigured(data.stripe_configured);
      })
      .catch(() => {
        setStripeConfigured(false);
      });
  }, []);

  // Calcular precio ajustado
  const calculatePrice = (tierId: string, country: string, income: number | ""): PPPData => {
    const tier = TIERS.find((t) => t.id === tierId);
    if (!tier) return { country: "", code: "", factor: 1, adjustedPrice: 0 };

    const countryData = PPP_COUNTRIES.find((c) => c.code === country);
    const factor = countryData?.factor || 0.60;
    
    let adjustedPrice = tier.basePrice * factor;

    // Ajuste por ingreso (honor system)
    if (income && typeof income === "number") {
      if (income < 500) adjustedPrice *= 0.5;
      else if (income < 1000) adjustedPrice *= 0.7;
      else if (income > 5000) adjustedPrice *= 1.2;
    }

    return {
      country: countryData?.name || "Otro",
      code: country,
      factor,
      adjustedPrice: Math.round(adjustedPrice * 100) / 100,
    };
  };

  const currentPPP = calculatePrice(selectedTier, countryCode, monthlyIncome);
  const selectedTierData = TIERS.find((t) => t.id === selectedTier);

  // Iniciar checkout con Stripe
  const handleSubscribe = async () => {
    if (!stripeConfigured) {
      setError("Stripe no está configurado. Contacta al administrador.");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Obtener token de autenticación (del localStorage o cookie)
      const token = localStorage.getItem("access_token");
      if (!token) {
        setError("Debes iniciar sesión para suscribirte.");
        setIsLoading(false);
        return;
      }

      // Crear sesión de checkout
      const response = await fetch(
        "http://localhost:5001/stripe/create-checkout-session",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            tier: selectedTier,
            country_code: countryCode,
            success_url: `${window.location.origin}/upgrade?success=true`,
            cancel_url: `${window.location.origin}/upgrade?canceled=true`,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Error al crear sesión de pago");
      }

      // Redirigir a Stripe Checkout
      if (data.url) {
        window.location.href = data.url;
      } else {
        throw new Error("No se recibió URL de checkout");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
      setIsLoading(false);
    }
  };

  // Verificar parámetros de URL (success/canceled)
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get("success") === "true") {
      setSuccess(true);
    }
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="max-w-7xl mx-auto px-4 py-16 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 text-sm font-medium mb-4">
              <Sparkles className="w-4 h-4" />
              Sostenibilidad Ética
            </span>
            <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4">
              Contribuidor Consciente
            </h1>
            <p className="text-xl text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
              Tu contribución mantiene vivo el proyecto. Precios ajustados por
              <span className="text-emerald-600 dark:text-emerald-400 font-semibold">
                {" "}paridad de poder adquisitivo
              </span>
              . Sin dark patterns, cancelación libre.
            </p>
          </motion.div>
        </div>

        {/* Mensaje de éxito */}
        <AnimatePresence>
          {success && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="mb-8"
            >
              <div className="bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl p-6 text-center">
                <div className="w-12 h-12 bg-emerald-100 dark:bg-emerald-800 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Check className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
                </div>
                <h3 className="text-lg font-semibold text-emerald-900 dark:text-emerald-100 mb-2">
                  ¡Gracias por contribuir!
                </h3>
                <p className="text-emerald-700 dark:text-emerald-300">
                  Tu suscripción ha sido activada. Revisa tu email para confirmación.
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Error */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="mb-8"
            >
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-4 text-center">
                <p className="text-red-700 dark:text-red-300">{error}</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Calculadora PPP */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="mb-12"
        >
          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-lg p-6 md:p-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-emerald-100 dark:bg-emerald-900/30 rounded-lg flex items-center justify-center">
                <Calculator className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
                  Calculadora de Precio Justo
                </h2>
                <p className="text-sm text-slate-500 dark:text-slate-400">
                  Basada en el Axioma T2: Igualdad Temporal Fundamental
                </p>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {/* Selector de país */}
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                  <Globe className="w-4 h-4 inline mr-1" />
                  País
                </label>
                <select
                  value={countryCode}
                  onChange={(e) => setCountryCode(e.target.value)}
                  className="w-full px-4 py-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                >
                  {PPP_COUNTRIES.map((c) => (
                    <option key={c.code} value={c.code}>
                      {c.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Ingreso mensual (honor system) */}
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                  Ingreso mensual (USD, opcional)
                  <span className="text-xs text-slate-400 block font-normal">
                    Sistema de honor - sin verificación
                  </span>
                </label>
                <input
                  type="number"
                  placeholder="Ej: 800"
                  value={monthlyIncome}
                  onChange={(e) =>
                    setMonthlyIncome(e.target.value ? parseInt(e.target.value) : "")
                  }
                  className="w-full px-4 py-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                />
              </div>
            </div>

            {/* Resultado del cálculo */}
            <div className="mt-6 p-4 bg-slate-50 dark:bg-slate-700/50 rounded-xl">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <p className="text-sm text-slate-500 dark:text-slate-400">
                    Precio base (EE.UU.):{" "}
                    <span className="line-through">
                      ${selectedTierData?.basePrice}/mes
                    </span>
                  </p>
                  <p className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">
                    ${currentPPP.adjustedPrice}/mes
                  </p>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    Ajuste PPP: {(currentPPP.factor * 100).toFixed(0)}% ·{" "}
                    {currentPPP.country}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-slate-500 dark:text-slate-400">
                    Ahorro vs. precio base:
                  </p>
                  <p className="text-lg font-semibold text-emerald-600 dark:text-emerald-400">
                    ${(selectedTierData?.basePrice || 0) - currentPPP.adjustedPrice}/mes
                  </p>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Grid de tiers */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {TIERS.map((tier, index) => {
            const tierPPP = calculatePrice(tier.id, countryCode, monthlyIncome);
            const isSelected = selectedTier === tier.id;

            return (
              <motion.div
                key={tier.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.1, duration: 0.5 }}
                onClick={() => setSelectedTier(tier.id)}
                className={`
                  relative rounded-2xl p-6 cursor-pointer transition-all duration-300
                  ${
                    isSelected
                      ? "ring-2 ring-emerald-500 bg-white dark:bg-slate-800 shadow-xl scale-105"
                      : "bg-white dark:bg-slate-800 shadow-lg hover:shadow-xl border border-slate-100 dark:border-slate-700"
                  }
                  ${tier.popular && !isSelected ? "ring-2 ring-emerald-200 dark:ring-emerald-900/30" : ""}
                `}
              >
                {/* Badge popular */}
                {tier.popular && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                    <span className="bg-emerald-500 text-white text-xs font-semibold px-3 py-1 rounded-full">
                      Más popular
                    </span>
                  </div>
                )}

                {/* Header del tier */}
                <div className="text-center mb-6">
                  <div
                    className={`
                    w-14 h-14 rounded-xl flex items-center justify-center mx-auto mb-4
                    ${
                      isSelected
                        ? "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400"
                        : "bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400"
                    }
                  `}
                  >
                    {tier.icon}
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-1">
                    {tier.name}
                  </h3>
                  <p className="text-sm text-slate-500 dark:text-slate-400">
                    {tier.description}
                  </p>
                </div>

                {/* Precio */}
                <div className="text-center mb-6">
                  {tier.id === "free" ? (
                    <span className="text-3xl font-bold text-slate-900 dark:text-white">
                      Gratis
                    </span>
                  ) : (
                    <>
                      <span className="text-sm text-slate-400 line-through block">
                        ${tier.basePrice}/mes
                      </span>
                      <span className="text-3xl font-bold text-slate-900 dark:text-white">
                        ${tierPPP.adjustedPrice}
                      </span>
                      <span className="text-slate-500 dark:text-slate-400">/mes</span>
                    </>
                  )}
                </div>

                {/* Beneficios */}
                <ul className="space-y-3 mb-6">
                  {tier.benefits.map((benefit, i) => (
                    <li key={i} className="flex items-start gap-3">
                      <Check className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" />
                      <span className="text-sm text-slate-600 dark:text-slate-300">
                        {benefit}
                      </span>
                    </li>
                  ))}
                  {tier.limitations?.map((limitation, i) => (
                    <li key={`limit-${i}`} className="flex items-start gap-3 opacity-50">
                      <X className="w-5 h-5 text-slate-400 flex-shrink-0 mt-0.5" />
                      <span className="text-sm text-slate-500 dark:text-slate-400">
                        {limitation}
                      </span>
                    </li>
                  ))}
                </ul>

                {/* Botón */}
                {tier.id === "free" ? (
                  <button
                    disabled
                    className="w-full py-3 rounded-lg font-medium bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400 cursor-default"
                  >
                    Plan actual
                  </button>
                ) : (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleSubscribe();
                    }}
                    disabled={isLoading || !stripeConfigured}
                    className={`
                      w-full py-3 rounded-lg font-medium flex items-center justify-center gap-2
                      transition-all duration-200
                      ${
                        isSelected
                          ? "bg-emerald-500 hover:bg-emerald-600 text-white shadow-lg shadow-emerald-500/25"
                          : "bg-slate-900 dark:bg-white text-white dark:text-slate-900 hover:bg-slate-800 dark:hover:bg-slate-100"
                      }
                      ${isLoading || !stripeConfigured ? "opacity-50 cursor-not-allowed" : ""}
                    `}
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        Procesando...
                      </>
                    ) : (
                      <>
                        Suscribirse
                        <ArrowRight className="w-4 h-4" />
                      </>
                    )}
                  </button>
                )}
              </motion.div>
            );
          })}
        </div>

        {/* Sección de transparencia */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="bg-slate-900 dark:bg-black rounded-2xl p-8 text-center"
        >
          <div className="max-w-3xl mx-auto">
            <h3 className="text-xl font-semibold text-white mb-4">
              Principios No Negociables
            </h3>
            <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-6 text-left">
              <div>
                <div className="w-10 h-10 bg-emerald-500/20 rounded-lg flex items-center justify-center mb-3">
                  <Globe className="w-5 h-5 text-emerald-400" />
                </div>
                <h4 className="text-white font-medium mb-1">Transparencia Radical</h4>
                <p className="text-slate-400 text-sm">
                  Todos los ingresos son públicos y auditables
                </p>
              </div>
              <div>
                <div className="w-10 h-10 bg-emerald-500/20 rounded-lg flex items-center justify-center mb-3">
                  <Users className="w-5 h-5 text-emerald-400" />
                </div>
                <h4 className="text-white font-medium mb-1">Igualdad Temporal</h4>
                <p className="text-slate-400 text-sm">
                  El tiempo de cada persona vale igual (PPP)
                </p>
              </div>
              <div>
                <div className="w-10 h-10 bg-emerald-500/20 rounded-lg flex items-center justify-center mb-3">
                  <Heart className="w-5 h-5 text-emerald-400" />
                </div>
                <h4 className="text-white font-medium mb-1">No Explotación</h4>
                <p className="text-slate-400 text-sm">
                  Sin dark patterns, cancelación libre anytime
                </p>
              </div>
              <div>
                <div className="w-10 h-10 bg-emerald-500/20 rounded-lg flex items-center justify-center mb-3">
                  <Sparkles className="w-5 h-5 text-emerald-400" />
                </div>
                <h4 className="text-white font-medium mb-1">Honor System</h4>
                <p className="text-slate-400 text-sm">
                  Confiamos en tu autoreporte de ingresos
                </p>
              </div>
            </div>

            <div className="mt-8 pt-8 border-t border-slate-800">
              <p className="text-slate-400 text-sm">
                ¿Preguntas? Revisa nuestro{" "}
                <a href="http://localhost:5001/subscriptions/transparency-report" target="_blank" rel="noopener noreferrer" className="text-emerald-400 hover:underline">
                  reporte de transparencia público
                </a>{" "}
                o{" "}
                <a href="#" className="text-emerald-400 hover:underline">
                  contacta al equipo
                </a>
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
