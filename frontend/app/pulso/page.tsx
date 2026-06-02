/*
 * Pulso Vital — El Latido de la Cohorte Cero
 * ============================================
 *
 * Dashboard de visualización del Suelo de Dignidad Vital (SDV)
 * comunitario. Muestra las 7 dimensiones de dignidad, narrativas
 * vitales, brechas de cobertura y alertas de Crímenes de Coherencia.
 *
 * Autor: Claude Opus (Anthropic)
 * Fecha: Mayo 2026
 */

"use client";

import { useState, useEffect, useMemo } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import {
  Activity,
  AlertTriangle,
  Home,
  Apple,
  Droplets,
  Heart,
  GraduationCap,
  Briefcase,
  Users,
  Shield,
  Loader2,
  LogIn,
  BarChart3,
  ArrowRight,
  Clock,
  Handshake,
  ClipboardList,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { apiFetch } from "../lib/api";

// ═══════════════════════════════════════════════════════════════
// Types
// ═══════════════════════════════════════════════════════════════

interface SDVDimensions {
  vivienda: number;
  alimentacion: number;
  agua: number;
  salud: number;
  educacion: number;
  trabajo: number;
  vinculos: number;
}

interface GapData {
  dimension: string;
  dimension_label: string;
  participants_needing: number;
  participants_offering: number;
  coverage_ratio: number;
  gap_severity: "critical" | "warning" | "ok";
}

interface UrgentNeed {
  participant_id: number;
  participant_name: string;
  city: string;
  neighborhood: string;
  need_description: string;
  need_urgency: string;
  need_categories: string[];
  need_dimensions: string[];
  days_without_exchange: number;
  latest_need_level: number;
  is_coherence_crime: boolean;
  top_matches: Array<{
    offerer_id: number;
    offerer_name: string;
    compatibility_score: number;
  }>;
}

interface PulseData {
  sdv: {
    average_overall: number;
    dimensions: SDVDimensions;
    participant_count: number;
    community_narrative: string;
    narratives: Record<string, string>;
  };
  gaps: {
    all: GapData[];
    critical: GapData[];
    warnings: GapData[];
    covered: GapData[];
    critical_count: number;
  };
  alerts: {
    coherence_crimes: UrgentNeed[];
    warnings: UrgentNeed[];
    total_urgent: number;
    crimes_count: number;
    system_alert: boolean;
  };
  stats: {
    total_participants: number;
    active_participants: number;
    total_exchanges: number;
    total_uth_hours: number;
    [key: string]: unknown;
  };
  timestamp: string;
}

// ═══════════════════════════════════════════════════════════════
// Constants
// ═══════════════════════════════════════════════════════════════

const DIMENSIONS = [
  { key: "vivienda", label: "Vivienda", Icon: Home },
  { key: "alimentacion", label: "Alimentación", Icon: Apple },
  { key: "agua", label: "Agua", Icon: Droplets },
  { key: "salud", label: "Salud", Icon: Heart },
  { key: "educacion", label: "Educación", Icon: GraduationCap },
  { key: "trabajo", label: "Trabajo", Icon: Briefcase },
  { key: "vinculos", label: "Vínculos", Icon: Users },
] as const;

type DimensionKey = (typeof DIMENSIONS)[number]["key"];

function scoreColor(s: number) {
  if (s >= 0.8) return { bg: "bg-emerald-500", text: "text-emerald-400", border: "border-emerald-500", stroke: "#34d399" };
  if (s >= 0.5) return { bg: "bg-amber-500", text: "text-amber-400", border: "border-amber-500", stroke: "#fbbf24" };
  return { bg: "bg-rose-500", text: "text-rose-400", border: "border-rose-500", stroke: "#fb7185" };
}

function scoreLabel(s: number) {
  if (s >= 0.9) return "Plenitud";
  if (s >= 0.7) return "Estable";
  if (s >= 0.5) return "Alerta";
  return "Crítico";
}

// ═══════════════════════════════════════════════════════════════
// SVG Radar Chart
// ═══════════════════════════════════════════════════════════════

function SDVRadarChart({ dimensions }: { dimensions: SDVDimensions }) {
  const cx = 160, cy = 160, maxR = 115;
  const n = DIMENSIONS.length;

  const angle = (i: number) => (2 * Math.PI * i) / n - Math.PI / 2;

  // Concentric heptagon rings
  const ring = (fraction: number) => {
    const r = maxR * fraction;
    const pts = Array.from({ length: n }, (_, i) => {
      const a = angle(i);
      return `${cx + r * Math.cos(a)},${cy + r * Math.sin(a)}`;
    }).join(" ");
    return pts;
  };

  // Score polygon points
  const scorePoints = useMemo(() => {
    const keys = DIMENSIONS.map((d) => d.key);
    return keys
      .map((k, i) => {
        const s = dimensions[k as DimensionKey] ?? 1;
        const r = maxR * s;
        const a = angle(i);
        return `${cx + r * Math.cos(a)},${cy + r * Math.sin(a)}`;
      })
      .join(" ");
  }, [dimensions]);

  // Individual score positions for dots
  const scoreDots = DIMENSIONS.map((d, i) => {
    const s = dimensions[d.key as DimensionKey] ?? 1;
    const r = maxR * s;
    const a = angle(i);
    return { x: cx + r * Math.cos(a), y: cy + r * Math.sin(a), score: s, dim: d };
  });

  // Label positions (outside the chart)
  const labelPositions = DIMENSIONS.map((d, i) => {
    const a = angle(i);
    const lr = maxR + 32;
    return { x: cx + lr * Math.cos(a), y: cy + lr * Math.sin(a), dim: d };
  });

  return (
    <div className="flex items-center justify-center">
      <svg viewBox="0 0 320 320" className="w-full max-w-[340px]">
        <defs>
          <radialGradient id="radarFill" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#34d399" stopOpacity="0.25" />
            <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.08" />
          </radialGradient>
        </defs>

        {/* Concentric rings */}
        {[0.25, 0.5, 0.75, 1.0].map((f) => (
          <polygon
            key={f}
            points={ring(f)}
            fill="none"
            stroke="currentColor"
            className="text-slate-800/40"
            strokeWidth={f === 1 ? 1 : 0.5}
          />
        ))}

        {/* Axis lines */}
        {DIMENSIONS.map((_, i) => {
          const a = angle(i);
          return (
            <line
              key={i}
              x1={cx}
              y1={cy}
              x2={cx + maxR * Math.cos(a)}
              y2={cy + maxR * Math.sin(a)}
              stroke="currentColor"
              className="text-slate-800/30"
              strokeWidth={0.5}
            />
          );
        })}

        {/* Score polygon */}
        <motion.polygon
          points={scorePoints}
          fill="url(#radarFill)"
          stroke="#34d399"
          strokeWidth={2}
          strokeLinejoin="round"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 0.5 }}
        />

        {/* Score dots */}
        {scoreDots.map(({ x, y, score, dim }, i) => (
          <motion.circle
            key={dim.key}
            cx={x}
            cy={y}
            r={4}
            fill={scoreColor(score).stroke}
            stroke="#020617"
            strokeWidth={2}
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.6 + i * 0.08, type: "spring" }}
          />
        ))}

        {/* Labels */}
        {labelPositions.map(({ x, y, dim }) => {
          const score = dimensions[dim.key as DimensionKey] ?? 1;
          const colors = scoreColor(score);
          return (
            <g key={dim.key}>
              <text
                x={x}
                y={y - 4}
                textAnchor="middle"
                className="fill-slate-400"
                fontSize="9"
                fontWeight="600"
              >
                {dim.label}
              </text>
              <text
                x={x}
                y={y + 9}
                textAnchor="middle"
                className={colors.text === "text-emerald-400" ? "fill-emerald-400" : colors.text === "text-amber-400" ? "fill-amber-400" : "fill-rose-400"}
                fontSize="10"
                fontWeight="700"
              >
                {(score * 100).toFixed(0)}%
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// Wellness Ring
// ═══════════════════════════════════════════════════════════════

function WellnessRing({ score }: { score: number }) {
  const radius = 78;
  const circumference = 2 * Math.PI * radius;
  const progress = circumference * (1 - score);
  const colors = scoreColor(score);
  const pct = Math.round(score * 100);

  return (
    <div className="relative flex items-center justify-center">
      <svg viewBox="0 0 200 200" className="w-48 h-48">
        {/* Background ring */}
        <circle
          cx="100"
          cy="100"
          r={radius}
          fill="none"
          stroke="currentColor"
          className="text-slate-800/60"
          strokeWidth="10"
        />
        {/* Progress ring */}
        <motion.circle
          cx="100"
          cy="100"
          r={radius}
          fill="none"
          stroke={colors.stroke}
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: progress }}
          transition={{ duration: 1.5, ease: "easeOut", delay: 0.3 }}
          transform="rotate(-90 100 100)"
        />
        {/* Glow overlay */}
        <motion.circle
          cx="100"
          cy="100"
          r={radius}
          fill="none"
          stroke={colors.stroke}
          strokeWidth="14"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: progress }}
          transition={{ duration: 1.5, ease: "easeOut", delay: 0.3 }}
          transform="rotate(-90 100 100)"
          opacity={0.15}
          className="blur-sm"
        />
      </svg>
      {/* Center content */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.span
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.8 }}
          className={`text-5xl font-black tabular-nums ${colors.text}`}
        >
          {pct}
        </motion.span>
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="text-xs font-bold uppercase tracking-widest text-slate-500 mt-1"
        >
          {scoreLabel(score)}
        </motion.span>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// Narrativa Vital Card
// ═══════════════════════════════════════════════════════════════

function NarrativaCard({
  dimension,
  score,
  narrative,
  delay,
}: {
  dimension: (typeof DIMENSIONS)[number];
  score: number;
  narrative: string;
  delay: number;
}) {
  const colors = scoreColor(score);
  const pct = Math.round(score * 100);
  const { Icon } = dimension;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5 }}
      className={`glass-card p-5 border-l-4 ${colors.border} hover:shadow-lg hover:shadow-${colors.stroke}/5 transition-shadow duration-300`}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2.5">
          <div className={`w-8 h-8 rounded-lg ${colors.bg}/15 flex items-center justify-center`}>
            <Icon size={16} className={colors.text} />
          </div>
          <span className="font-semibold text-sm text-white">{dimension.label}</span>
        </div>
        <span className={`text-sm font-bold tabular-nums ${colors.text}`}>{pct}%</span>
      </div>

      {/* Progress bar */}
      <div className="w-full h-1.5 bg-slate-800 rounded-full mb-3 overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${colors.bg}`}
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ delay: delay + 0.2, duration: 0.8, ease: "easeOut" }}
        />
      </div>

      {/* Narrative */}
      <p className="text-xs text-slate-400 leading-relaxed">{narrative}</p>
    </motion.div>
  );
}

// ═══════════════════════════════════════════════════════════════
// Coverage Gap Bar
// ═══════════════════════════════════════════════════════════════

function GapBar({ gap, delay }: { gap: GapData; delay: number }) {
  const severity = gap.gap_severity;
  const barColor =
    severity === "ok" ? "bg-emerald-500" :
    severity === "warning" ? "bg-amber-500" : "bg-rose-500";
  const dotColor =
    severity === "ok" ? "bg-emerald-400" :
    severity === "warning" ? "bg-amber-400" : "bg-rose-400";
  const ratio = Math.min(gap.coverage_ratio, 1);
  const pct = Math.round(ratio * 100);

  return (
    <motion.div
      initial={{ opacity: 0, x: -12 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay }}
      className="flex items-center gap-4"
    >
      <div className="w-28 shrink-0 flex items-center gap-2">
        <div className={`w-2 h-2 rounded-full ${dotColor}`} />
        <span className="text-xs font-medium text-slate-300 truncate">
          {gap.dimension_label}
        </span>
      </div>

      <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${barColor}`}
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ delay: delay + 0.15, duration: 0.7, ease: "easeOut" }}
        />
      </div>

      <div className="w-20 shrink-0 text-right">
        <span className="text-[10px] text-slate-500 tabular-nums">
          {gap.participants_offering}/{gap.participants_needing + gap.participants_offering}
        </span>
      </div>
    </motion.div>
  );
}

// ═══════════════════════════════════════════════════════════════
// Gap Analysis Section
// ═══════════════════════════════════════════════════════════════

function GapAnalysis({ gaps }: { gaps: GapData[] }) {
  return (
    <div className="glass-card p-6">
      <div className="flex items-center gap-3 mb-5">
        <div className="w-8 h-8 rounded-lg bg-amber-500/20 flex items-center justify-center text-amber-400 border border-amber-500/30">
          <BarChart3 size={16} />
        </div>
        <div>
          <h2 className="text-base font-bold text-white">Brechas de Cobertura</h2>
          <p className="text-[10px] text-slate-500">Capacidad de la red para cubrir cada dimensión</p>
        </div>
      </div>
      <div className="space-y-3">
        {gaps.map((g, i) => (
          <GapBar key={g.dimension} gap={g} delay={0.8 + i * 0.06} />
        ))}
      </div>
      <div className="mt-4 flex items-center gap-6 text-[10px] text-slate-600">
        <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-emerald-400" /> Cubierto</span>
        <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-amber-400" /> Alerta</span>
        <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-rose-400" /> Crítico</span>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// Coherence Crime Banner
// ═══════════════════════════════════════════════════════════════

function CoherenceCrimeBanner({ crimes }: { crimes: UrgentNeed[] }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-8 rounded-2xl border-2 border-rose-500/40 bg-rose-500/5 backdrop-blur-lg p-5 relative overflow-hidden"
    >
      {/* Pulsing glow */}
      <motion.div
        animate={{ opacity: [0.05, 0.15, 0.05] }}
        transition={{ duration: 3, repeat: Infinity }}
        className="absolute inset-0 bg-rose-500 rounded-2xl"
      />

      <div className="relative z-10">
        <div className="flex items-center gap-3 mb-3">
          <motion.div
            animate={{ scale: [1, 1.15, 1] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          >
            <AlertTriangle className="w-6 h-6 text-rose-400" />
          </motion.div>
          <div>
            <h3 className="font-bold text-rose-300 text-sm">
              ⚠️ Crimen de Coherencia Detectado
            </h3>
            <p className="text-[10px] text-rose-400/70">
              La comunidad tiene la obligación ética de actuar (Axioma T10: Responsabilidad Temporal Colectiva)
            </p>
          </div>
        </div>
        <div className="space-y-2">
          {crimes.map((c) => (
            <div key={c.participant_id} className="flex items-center gap-3 text-xs text-rose-200/80">
              <span className="font-semibold">{c.participant_name}</span>
              <span className="text-rose-400/50">·</span>
              <span>{c.need_description}</span>
              <span className="text-rose-400/50">·</span>
              <span className="flex items-center gap-1">
                <Clock size={10} />
                {c.days_without_exchange}d sin apoyo
              </span>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

// ═══════════════════════════════════════════════════════════════
// Urgent Needs Panel
// ═══════════════════════════════════════════════════════════════

function UrgentNeedsPanel({ crimes, warnings }: { crimes: UrgentNeed[]; warnings: UrgentNeed[] }) {
  const all = [...crimes, ...warnings];

  return (
    <div className="glass-card p-6">
      <div className="flex items-center gap-3 mb-5">
        <div className="w-8 h-8 rounded-lg bg-rose-500/20 flex items-center justify-center text-rose-400 border border-rose-500/30">
          <AlertTriangle size={16} />
        </div>
        <div>
          <h2 className="text-base font-bold text-white">Necesidades Urgentes</h2>
          <p className="text-[10px] text-slate-500">
            {crimes.length} crímenes de coherencia · {warnings.length} alertas activas
          </p>
        </div>
      </div>

      <div className="space-y-3">
        {all.map((need, i) => (
          <motion.div
            key={need.participant_id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.0 + i * 0.08 }}
            className={`p-4 rounded-xl border ${
              need.is_coherence_crime
                ? "border-rose-500/30 bg-rose-500/5"
                : "border-amber-500/20 bg-amber-500/5"
            }`}
          >
            <div className="flex items-start justify-between mb-2">
              <div>
                <span className="font-semibold text-sm text-white">{need.participant_name}</span>
                {need.city && (
                  <span className="text-[10px] text-slate-500 ml-2">{need.city}</span>
                )}
              </div>
              <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${
                need.is_coherence_crime
                  ? "bg-rose-500/20 text-rose-400"
                  : "bg-amber-500/20 text-amber-400"
              }`}>
                {need.is_coherence_crime ? "Crimen" : need.need_urgency}
              </span>
            </div>
            <p className="text-xs text-slate-400 mb-2">{need.need_description}</p>
            <div className="flex items-center gap-4 text-[10px] text-slate-500">
              <span className="flex items-center gap-1">
                <Clock size={10} />
                {need.days_without_exchange}d sin intercambio
              </span>
              {need.top_matches.length > 0 && (
                <span className="flex items-center gap-1">
                  <Handshake size={10} />
                  {need.top_matches.length} match{need.top_matches.length !== 1 ? "es" : ""} sugerido{need.top_matches.length !== 1 ? "s" : ""}
                </span>
              )}
            </div>
            {/* Top matches */}
            {need.top_matches.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-1.5">
                {need.top_matches.slice(0, 3).map((m) => (
                  <span key={m.offerer_id} className="inline-flex items-center gap-1 px-2 py-0.5 bg-slate-800/80 rounded-md text-[10px] text-emerald-400">
                    {m.offerer_name}
                    <span className="text-slate-600">{Math.round(m.compatibility_score * 100)}%</span>
                  </span>
                ))}
              </div>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// Quick Stat Row
// ═══════════════════════════════════════════════════════════════

function StatRow({ label, value, suffix }: { label: string; value: number; suffix?: string }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-xs text-slate-500">{label}</span>
      <span className="text-sm font-bold text-white tabular-nums">
        {typeof value === "number" && !Number.isInteger(value) ? value.toFixed(1) : value}
        {suffix && <span className="text-slate-500 text-xs ml-0.5">{suffix}</span>}
      </span>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// Status Indicator
// ═══════════════════════════════════════════════════════════════

function StatusIndicator({
  label,
  count,
  severity,
}: {
  label: string;
  count: number;
  severity: "ok" | "warning" | "critical";
}) {
  const dot =
    severity === "ok" ? "bg-emerald-400" :
    severity === "warning" ? "bg-amber-400" : "bg-rose-400";
  const countColor =
    severity === "ok" ? "text-emerald-400" :
    severity === "warning" ? "text-amber-400" : "text-rose-400";

  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2">
        <div className={`w-2 h-2 rounded-full ${dot}`} />
        <span className="text-xs text-slate-500">{label}</span>
      </div>
      <span className={`text-sm font-bold tabular-nums ${countColor}`}>{count}</span>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// State Screens
// ═══════════════════════════════════════════════════════════════

function LoadingState() {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex flex-col items-center gap-4"
      >
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
        >
          <Loader2 size={40} className="text-violet-400" />
        </motion.div>
        <p className="text-slate-400 text-sm">Leyendo el pulso vital de la comunidad...</p>
      </motion.div>
    </div>
  );
}

function UnauthenticatedState() {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass-card p-10 max-w-md text-center"
      >
        <div className="w-16 h-16 rounded-2xl bg-violet-500/20 flex items-center justify-center text-violet-400 border border-violet-500/30 mx-auto mb-6">
          <Activity size={32} />
        </div>
        <h2 className="text-2xl font-bold text-white mb-3">Pulso Vital</h2>
        <p className="text-slate-400 text-sm mb-6 leading-relaxed">
          Inicia sesión para ver el estado de dignidad vital de la Cohorte Cero
          en tiempo real. Cada dimensión cuenta una historia.
        </p>
        <Link
          href="/login"
          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-emerald-500 text-white font-bold hover:bg-emerald-600 transition-all shadow-lg shadow-emerald-500/20"
        >
          <LogIn size={18} />
          Iniciar Sesión
        </Link>
      </motion.div>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass-card p-10 max-w-md text-center"
      >
        <div className="w-16 h-16 rounded-2xl bg-cyan-500/20 flex items-center justify-center text-cyan-400 border border-cyan-500/30 mx-auto mb-6">
          <Users size={32} />
        </div>
        <h2 className="text-2xl font-bold text-white mb-3">Sin datos aún</h2>
        <p className="text-slate-400 text-sm mb-6 leading-relaxed">
          La Cohorte Cero aún no tiene participantes registrados. El Pulso Vital
          se activará cuando la comunidad empiece a latir.
        </p>
        <Link
          href="/forms/cero"
          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-emerald-500 text-white font-bold hover:bg-emerald-600 transition-all shadow-lg shadow-emerald-500/20"
        >
          <ClipboardList size={18} />
          Registrar Participante
          <ArrowRight size={16} />
        </Link>
      </motion.div>
    </div>
  );
}

function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass-card p-10 max-w-md text-center"
      >
        <div className="w-16 h-16 rounded-2xl bg-rose-500/20 flex items-center justify-center text-rose-400 border border-rose-500/30 mx-auto mb-6">
          <AlertTriangle size={32} />
        </div>
        <h2 className="text-2xl font-bold text-white mb-3">Error</h2>
        <p className="text-rose-400 text-sm mb-6">{message}</p>
        {onRetry && (
          <button
            onClick={onRetry}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-slate-800 text-white font-medium hover:bg-slate-700 transition-all"
          >
            Reintentar
          </button>
        )}
      </motion.div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// Main Page Component
// ═══════════════════════════════════════════════════════════════

export default function PulsoVitalPage() {
  const { isAuthenticated } = useAuth();
  const [pulseData, setPulseData] = useState<PulseData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPulse = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch("/forms/pulse");
      if (!res.ok) throw new Error("Error cargando el Pulso Vital");
      const data = await res.json();
      setPulseData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!isAuthenticated) {
      setLoading(false);
      return;
    }
    fetchPulse();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated]);

  // === State screens ===
  if (!isAuthenticated) return <UnauthenticatedState />;
  if (loading) return <LoadingState />;
  if (error) return <ErrorState message={error} onRetry={fetchPulse} />;
  if (!pulseData || pulseData.sdv.participant_count === 0) return <EmptyState />;

  const { sdv, gaps, alerts, stats } = pulseData;
  const overallScore = sdv.average_overall;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {/* Ambient background glow */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] rounded-full blur-[200px] opacity-[0.04] bg-violet-500" />
        <div className="absolute bottom-0 right-0 w-[400px] h-[400px] rounded-full blur-[180px] opacity-[0.03] bg-emerald-500" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
        {/* ── Header ── */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-10"
        >
          <div className="flex items-center gap-4 mb-2">
            <div className="relative">
              <div className="w-12 h-12 rounded-2xl bg-violet-500/20 flex items-center justify-center text-violet-400 border border-violet-500/30 shadow-lg shadow-violet-500/10">
                <Activity size={28} />
              </div>
              {/* Pulsing heartbeat dot */}
              <motion.div
                animate={{ scale: [1, 1.6, 1], opacity: [1, 0.4, 1] }}
                transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                className="absolute -top-1 -right-1 w-3 h-3 rounded-full bg-emerald-400 border-2 border-slate-950"
              />
            </div>
            <div>
              <h1 className="text-3xl md:text-4xl font-bold tracking-tight">
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-violet-400 via-emerald-400 to-cyan-400">
                  Pulso Vital
                </span>
              </h1>
              <p className="text-slate-400 text-sm">
                El latido de la Cohorte Cero — Suelo de Dignidad Vital en tiempo real
              </p>
            </div>
          </div>
        </motion.header>

        {/* ── Alert Banner ── */}
        {alerts.system_alert && (
          <CoherenceCrimeBanner crimes={alerts.coherence_crimes} />
        )}

        {/* ── Main Grid ── */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8">
          {/* Wellness Ring */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
            className="lg:col-span-4"
          >
            <div className="glass-card p-6 h-full flex flex-col items-center justify-center">
              <h2 className="text-xs font-bold uppercase tracking-[0.2em] text-slate-500 mb-6">
                Bienestar Comunitario
              </h2>
              <WellnessRing score={overallScore} />
              <p className="text-center text-sm text-slate-400 mt-6 max-w-xs leading-relaxed">
                {sdv.community_narrative}
              </p>
              <div className="mt-4 flex items-center gap-2 text-xs text-slate-500">
                <Users size={14} />
                <span>
                  {sdv.participant_count} participante{sdv.participant_count !== 1 ? "s" : ""} activo{sdv.participant_count !== 1 ? "s" : ""}
                </span>
              </div>
            </div>
          </motion.div>

          {/* Radar Chart */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="lg:col-span-5"
          >
            <div className="glass-card p-6 h-full">
              <h2 className="text-xs font-bold uppercase tracking-[0.2em] text-slate-500 mb-4">
                Las 7 Dimensiones de Dignidad
              </h2>
              <SDVRadarChart dimensions={sdv.dimensions} />
            </div>
          </motion.div>

          {/* Quick Stats + System Status */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
            className="lg:col-span-3"
          >
            <div className="space-y-4 h-full flex flex-col">
              <div className="glass-card p-5">
                <h2 className="text-xs font-bold uppercase tracking-[0.2em] text-slate-500 mb-4">
                  Actividad
                </h2>
                <div className="space-y-3">
                  <StatRow label="Participantes" value={stats.total_participants ?? 0} />
                  <StatRow label="Intercambios" value={stats.total_exchanges ?? 0} />
                  <StatRow label="UTH Movilizadas" value={stats.total_uth_hours ?? 0} suffix="h" />
                </div>
              </div>

              <div className="glass-card p-5 flex-1">
                <h2 className="text-xs font-bold uppercase tracking-[0.2em] text-slate-500 mb-4">
                  Estado del Sistema
                </h2>
                <div className="space-y-3">
                  <StatusIndicator
                    label="Crímenes de Coherencia"
                    count={alerts.crimes_count}
                    severity={alerts.crimes_count > 0 ? "critical" : "ok"}
                  />
                  <StatusIndicator
                    label="Alertas Activas"
                    count={alerts.total_urgent}
                    severity={alerts.total_urgent > 0 ? "warning" : "ok"}
                  />
                  <StatusIndicator
                    label="Brechas Críticas"
                    count={gaps.critical_count}
                    severity={gaps.critical_count > 0 ? "warning" : "ok"}
                  />
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* ── Narrativa Vital ── */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-8"
        >
          <div className="flex items-center gap-3 mb-6">
            <div className="w-8 h-8 rounded-lg bg-cyan-500/20 flex items-center justify-center text-cyan-400 border border-cyan-500/30">
              <Shield size={18} />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">Narrativa Vital</h2>
              <p className="text-xs text-slate-500">
                Cada dimensión cuenta una historia de dignidad humana
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {DIMENSIONS.map((dim, i) => (
              <NarrativaCard
                key={dim.key}
                dimension={dim}
                score={sdv.dimensions[dim.key as DimensionKey] ?? 1}
                narrative={sdv.narratives[dim.key] || "Sin datos suficientes para generar narrativa."}
                delay={0.5 + i * 0.08}
              />
            ))}
          </div>
        </motion.section>

        {/* ── Coverage Gaps ── */}
        {gaps.all.length > 0 && (
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="mb-8"
          >
            <GapAnalysis gaps={gaps.all} />
          </motion.section>
        )}

        {/* ── Urgent Needs ── */}
        {alerts.total_urgent > 0 && (
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.0 }}
            className="mb-8"
          >
            <UrgentNeedsPanel
              crimes={alerts.coherence_crimes}
              warnings={alerts.warnings}
            />
          </motion.section>
        )}

        {/* ── Footer ── */}
        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2 }}
          className="mt-16 pb-8 text-center text-xs text-slate-600 space-y-1"
        >
          <p>Pulso Vital — Contribución de Claude Opus (Anthropic) para la Maxocracia</p>
          <p className="italic">Cada segundo de vida consciente es irrepetible. Axioma T0.</p>
        </motion.footer>
      </div>
    </div>
  );
}
