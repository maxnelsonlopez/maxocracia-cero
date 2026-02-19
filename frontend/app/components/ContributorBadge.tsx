/*
 * Componente ContributorBadge
 * =============================
 * 
 * Badge visual que indica el nivel de suscripción del usuario.
 * Se muestra en perfiles, posts, y contribuciones.
 * 
 * Autor: Kimi (Moonshot AI)
 * Fecha: Febrero 2026
 */

"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { 
  Zap, 
  Shield, 
  Heart, 
  Crown,
  Sparkles,
  CheckCircle2
} from "lucide-react";

interface ContributorBadgeProps {
  tier?: "free" | "contributor" | "enterprise";
  showLabel?: boolean;
  size?: "sm" | "md" | "lg";
  animated?: boolean;
}

interface SubscriptionData {
  tier: string;
  status: string;
  days_until_expiry: number | null;
}

const TIER_CONFIG = {
  free: {
    icon: Heart,
    label: "Miembro",
    color: "bg-slate-100 text-slate-600",
    darkColor: "dark:bg-slate-800 dark:text-slate-400",
    borderColor: "border-slate-200 dark:border-slate-700",
    description: "Acceso gratuito",
  },
  contributor: {
    icon: Zap,
    label: "Contribuidor",
    color: "bg-emerald-100 text-emerald-700",
    darkColor: "dark:bg-emerald-900/30 dark:text-emerald-300",
    borderColor: "border-emerald-200 dark:border-emerald-800",
    description: "Apoya la sostenibilidad",
  },
  enterprise: {
    icon: Crown,
    label: "Enterprise",
    color: "bg-amber-100 text-amber-700",
    darkColor: "dark:bg-amber-900/30 dark:text-amber-300",
    borderColor: "border-amber-200 dark:border-amber-800",
    description: "Organización partner",
  },
};

const SIZE_CONFIG = {
  sm: {
    container: "px-2 py-0.5 text-xs gap-1",
    icon: "w-3 h-3",
  },
  md: {
    container: "px-3 py-1 text-sm gap-1.5",
    icon: "w-4 h-4",
  },
  lg: {
    container: "px-4 py-2 text-base gap-2",
    icon: "w-5 h-5",
  },
};

export function ContributorBadge({
  tier: propTier,
  showLabel = true,
  size = "md",
  animated = true,
}: ContributorBadgeProps) {
  const [tier, setTier] = useState<string>(propTier || "free");
  const [loading, setLoading] = useState(!propTier);
  const [error, setError] = useState(false);

  // Si no se pasa tier, fetch desde API
  useEffect(() => {
    if (propTier) {
      setTier(propTier);
      return;
    }

    const fetchSubscription = async () => {
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          setTier("free");
          setLoading(false);
          return;
        }

        const response = await fetch(
          "http://localhost:5001/subscriptions/my-subscription",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.ok) {
          const data: SubscriptionData = await response.json();
          setTier(data.tier);
        } else {
          setTier("free");
        }
      } catch {
        setError(true);
        setTier("free");
      } finally {
        setLoading(false);
      }
    };

    fetchSubscription();
  }, [propTier]);

  if (loading) {
    return (
      <div className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-slate-100 dark:bg-slate-800 animate-pulse">
        <div className="w-3 h-3 rounded-full bg-slate-300 dark:bg-slate-600" />
        <div className="w-16 h-3 rounded bg-slate-300 dark:bg-slate-600" />
      </div>
    );
  }

  const config = TIER_CONFIG[tier as keyof typeof TIER_CONFIG] || TIER_CONFIG.free;
  const sizeConfig = SIZE_CONFIG[size];
  const IconComponent = config.icon;

  const BadgeContent = (
    <>
      <IconComponent className={sizeConfig.icon} />
      {showLabel && (
        <span className="font-medium">{config.label}</span>
      )}
    </>
  );

  if (animated && tier !== "free") {
    return (
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        whileHover={{ scale: 1.05 }}
        className={`
          inline-flex items-center rounded-full border
          ${config.color} ${config.darkColor} ${config.borderColor}
          ${sizeConfig.container}
          shadow-sm cursor-default
        `}
        title={config.description}
      >
        {tier === "contributor" && (
          <motion.div
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ repeat: Infinity, duration: 2, repeatDelay: 3 }}
          >
            {BadgeContent}
          </motion.div>
        )}
        {tier === "enterprise" && (
          <motion.div
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ repeat: Infinity, duration: 2, repeatDelay: 3 }}
          >
            {BadgeContent}
          </motion.div>
        )}
        {tier === "free" && BadgeContent}
      </motion.div>
    );
  }

  return (
    <div
      className={`
        inline-flex items-center rounded-full border
        ${config.color} ${config.darkColor} ${config.borderColor}
        ${sizeConfig.container}
        shadow-sm
      `}
      title={config.description}
    >
      {BadgeContent}
    </div>
  );
}

// Componente de insignia de verificación adicional
export function VerifiedContributor({ 
  size = "md" 
}: { 
  size?: "sm" | "md" | "lg" 
}) {
  const sizeConfig = {
    sm: "w-4 h-4",
    md: "w-5 h-5",
    lg: "w-6 h-6",
  };

  return (
    <motion.div
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      className="inline-flex items-center justify-center rounded-full bg-emerald-500 text-white"
      title="Contribuidor Verificado"
    >
      <CheckCircle2 className={sizeConfig[size]} />
    </motion.div>
  );
}

// Componente de banner de suscripción (para mostrar en dashboard)
export function SubscriptionBanner() {
  const [subscription, setSubscription] = useState<SubscriptionData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSubscription = async () => {
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          setLoading(false);
          return;
        }

        const response = await fetch(
          "http://localhost:5001/subscriptions/my-subscription",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.ok) {
          const data = await response.json();
          setSubscription(data);
        }
      } catch {
        // Silenciar error
      } finally {
        setLoading(false);
      }
    };

    fetchSubscription();
  }, []);

  if (loading || !subscription || subscription.tier === "free") {
    return null;
  }

  const isExpiringSoon = subscription.days_until_expiry !== null && 
    subscription.days_until_expiry <= 7;

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`
        rounded-xl p-4 mb-6
        ${isExpiringSoon 
          ? "bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800" 
          : "bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800"
        }
      `}
    >
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-3">
          <div className={`
            w-10 h-10 rounded-lg flex items-center justify-center
            ${isExpiringSoon 
              ? "bg-amber-100 dark:bg-amber-800 text-amber-600 dark:text-amber-400" 
              : "bg-emerald-100 dark:bg-emerald-800 text-emerald-600 dark:text-emerald-400"
            }
          `}>
            {isExpiringSoon ? <Sparkles className="w-5 h-5" /> : <Shield className="w-5 h-5" />}
          </div>
          <div>
            <h4 className="font-semibold text-slate-900 dark:text-white">
              {isExpiringSoon ? "Renovación próxima" : `Suscripción ${subscription.tier}`}
            </h4>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              {isExpiringSoon 
                ? `Tu suscripción expira en ${subscription.days_until_expiry} días`
                : "Gracias por contribuir a la sostenibilidad de Maxocracia"
              }
            </p>
          </div>
        </div>
        <a
          href="http://localhost:5001/stripe/customer-portal"
          className={`
            px-4 py-2 rounded-lg text-sm font-medium transition-colors
            ${isExpiringSoon 
              ? "bg-amber-500 hover:bg-amber-600 text-white" 
              : "bg-emerald-500 hover:bg-emerald-600 text-white"
            }
          `}
        >
          {isExpiringSoon ? "Renovar ahora" : "Gestionar suscripción"}
        </a>
      </div>
    </motion.div>
  );
}

export default ContributorBadge;
