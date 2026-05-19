"use client";

import React, { useEffect, useState, useCallback } from "react";
import { apiFetch } from "../../lib/api";
import Link from "next/link";
import {
    AlertTriangle,
    CheckCircle2,
    Clock,
    Users,
    ArrowRight,
    MessageCircle,
    Phone,
    Zap,
    Activity,
    BarChart3,
    ShieldAlert,
    RefreshCw,
    MapPin,
    Tag,
    Heart,
} from "lucide-react";

// ─── Tipos ────────────────────────────────────────────────────────

interface MatchResult {
    offerer_id: number;
    offerer_name: string;
    offerer_city: string;
    offerer_neighborhood: string;
    offerer_phone_whatsapp: string | null;
    offerer_telegram: string | null;
    matched_categories: string[];
    offerer_description: string;
    offerer_dimensions: string[];
    compatibility_score: number;
    same_city: boolean;
    same_neighborhood: boolean;
    recently_exchanged: boolean;
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
    latest_need_level: number | null;
    is_coherence_crime: boolean;
    top_matches: MatchResult[];
}

interface CommunityGap {
    dimension: string;
    dimension_label: string;
    participants_needing: number;
    participants_offering: number;
    coverage_ratio: number;
    gap_severity: "critical" | "warning" | "ok";
}

interface MatchingData {
    coherence_crimes: UrgentNeed[];
    warnings: UrgentNeed[];
    total_urgent: number;
    crimes_count: number;
    system_alert: boolean;
}

interface GapsData {
    gaps: CommunityGap[];
    critical: CommunityGap[];
    warnings: CommunityGap[];
    covered: CommunityGap[];
    critical_count: number;
}

// ─── Helpers ──────────────────────────────────────────────────────

const CATEGORY_LABELS: Record<string, string> = {
    objeto: "Objeto físico",
    alimentacion: "Alimentación",
    habilidad: "Habilidad",
    conocimiento: "Conocimiento",
    transporte: "Transporte",
    tiempo: "Tiempo / Apoyo",
    espacio: "Espacio",
    apoyo_economico: "Apoyo económico",
};

const categoryLabel = (c: string) =>
    CATEGORY_LABELS[c] || c.replace(/_/g, " ");

const scoreColor = (score: number) => {
    if (score >= 0.75) return "text-emerald-400";
    if (score >= 0.5) return "text-amber-400";
    return "text-rose-400";
};

const scoreBg = (score: number) => {
    if (score >= 0.75) return "bg-emerald-500/10 border-emerald-500/20";
    if (score >= 0.5) return "bg-amber-500/10 border-amber-500/20";
    return "bg-rose-500/10 border-rose-500/20";
};

// apiFetch del módulo centralizado maneja el token mc_access_token automáticamente

// ─── Componentes ──────────────────────────────────────────────────

function CoherenceCrimeBanner({ count }: { count: number }) {
    if (count === 0) return null;
    return (
        <div className="relative overflow-hidden rounded-2xl border border-rose-500/40 bg-rose-950/40 backdrop-blur-xl p-6 animate-pulse-slow">
            <div className="absolute inset-0 bg-rose-500/5 pointer-events-none" />
            <div className="flex items-start gap-4">
                <ShieldAlert className="w-8 h-8 text-rose-400 shrink-0 mt-0.5 animate-pulse" />
                <div>
                    <h2 className="text-rose-300 font-black text-lg uppercase tracking-wider mb-1">
                        🔴 ALERTA: {count} Crimen{count > 1 ? "es" : ""} de Coherencia Detectado{count > 1 ? "s" : ""}
                    </h2>
                    <p className="text-rose-200/70 text-sm leading-relaxed">
                        El VHV reporta violaciones sistemáticas del Suelo de Dignidad Vital.
                        La resolución de estas situaciones es <strong>responsabilidad urgente y colectiva</strong> de
                        todos los miembros activos de la Maxocracia. Deben ser atendidas antes de
                        cualquier otro intercambio. El sistema está bajo protocolo de emergencia ética.
                    </p>
                </div>
            </div>
        </div>
    );
}

function MatchCard({ match }: { match: MatchResult }) {
    return (
        <div
            className={`rounded-xl border p-4 transition-all hover:scale-[1.01] ${scoreBg(match.compatibility_score)}`}
        >
            <div className="flex items-start justify-between gap-2 mb-3">
                <div>
                    <p className="font-bold text-white text-sm">{match.offerer_name}</p>
                    <div className="flex items-center gap-1 text-slate-400 text-xs mt-0.5">
                        <MapPin className="w-3 h-3" />
                        <span>
                            {match.offerer_neighborhood}
                            {match.same_neighborhood && (
                                <span className="ml-1 text-emerald-400 font-semibold">(mismo barrio)</span>
                            )}
                        </span>
                    </div>
                </div>
                <span
                    className={`text-xs font-black px-2 py-1 rounded-lg border ${scoreBg(match.compatibility_score)} ${scoreColor(match.compatibility_score)}`}
                >
                    {Math.round(match.compatibility_score * 100)}%
                </span>
            </div>

            <p className="text-slate-300 text-xs leading-relaxed line-clamp-2 mb-3">
                {match.offerer_description}
            </p>

            <div className="flex flex-wrap gap-1 mb-3">
                {match.matched_categories.map((c) => (
                    <span
                        key={c}
                        className="text-[10px] px-2 py-0.5 rounded-full bg-slate-700/60 text-slate-300 border border-slate-600/40 flex items-center gap-1"
                    >
                        <Tag className="w-2.5 h-2.5" />
                        {categoryLabel(c)}
                    </span>
                ))}
            </div>

            <div className="flex items-center gap-2">
                {match.offerer_phone_whatsapp && (
                    <a
                        href={`https://wa.me/${match.offerer_phone_whatsapp.replace(/\D/g, "")}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-1.5 text-[10px] px-3 py-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/20 text-emerald-400 font-semibold transition-colors"
                    >
                        <Phone className="w-3 h-3" />
                        WhatsApp
                    </a>
                )}
                {match.offerer_telegram && (
                    <a
                        href={`https://t.me/${match.offerer_telegram.replace("@", "")}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-1.5 text-[10px] px-3 py-1.5 rounded-lg bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/20 text-blue-400 font-semibold transition-colors"
                    >
                        <MessageCircle className="w-3 h-3" />
                        Telegram
                    </a>
                )}
                <Link
                    href={`/forms/exchange?receiver=${match.offerer_id}`}
                    className="ml-auto flex items-center gap-1 text-[10px] text-slate-400 hover:text-white transition-colors"
                >
                    Registrar intercambio
                    <ArrowRight className="w-3 h-3" />
                </Link>
            </div>
        </div>
    );
}

function UrgentNeedCard({ need }: { need: UrgentNeed }) {
    const isCrime = need.is_coherence_crime;

    return (
        <div
            className={`rounded-2xl border p-6 transition-all ${
                isCrime
                    ? "border-rose-500/40 bg-rose-950/20"
                    : "border-amber-500/20 bg-slate-900/50"
            } backdrop-blur-xl`}
        >
            {/* Header */}
            <div className="flex items-start justify-between gap-3 mb-4">
                <div>
                    <div className="flex items-center gap-2 mb-1">
                        {isCrime ? (
                            <ShieldAlert className="w-4 h-4 text-rose-400 animate-pulse" />
                        ) : (
                            <AlertTriangle className="w-4 h-4 text-amber-400" />
                        )}
                        <span className="font-bold text-white">{need.participant_name}</span>
                        {isCrime && (
                            <span className="text-[9px] px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 border border-rose-500/30 font-black uppercase">
                                CRIMEN DE COHERENCIA
                            </span>
                        )}
                    </div>
                    <div className="flex items-center gap-1 text-xs text-slate-400">
                        <MapPin className="w-3 h-3" />
                        {need.neighborhood}, {need.city}
                    </div>
                </div>
                <div className="text-right shrink-0">
                    <div className={`text-lg font-black ${isCrime ? "text-rose-400" : "text-amber-400"}`}>
                        {need.days_without_exchange === 9999 ? "∞" : need.days_without_exchange}d
                    </div>
                    <div className="text-[10px] text-slate-500 uppercase">sin intercambio</div>
                </div>
            </div>

            {/* Descripción de necesidad */}
            <p className="text-sm text-slate-300 leading-relaxed mb-4 pl-2 border-l-2 border-slate-600">
                {need.need_description}
            </p>

            {/* Categorías necesarias */}
            {need.need_categories.length > 0 && (
                <div className="flex flex-wrap gap-1 mb-4">
                    {need.need_categories.map((c) => (
                        <span
                            key={c}
                            className={`text-[10px] px-2 py-0.5 rounded-full border flex items-center gap-1 ${
                                isCrime
                                    ? "bg-rose-500/10 border-rose-500/20 text-rose-300"
                                    : "bg-amber-500/10 border-amber-500/20 text-amber-300"
                            }`}
                        >
                            <Heart className="w-2.5 h-2.5" />
                            {categoryLabel(c)}
                        </span>
                    ))}
                </div>
            )}

            {/* Matches sugeridos */}
            {need.top_matches.length > 0 ? (
                <div>
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                        <Zap className="w-3.5 h-3.5 text-emerald-500" />
                        Personas que pueden ayudar
                    </h4>
                    <div className="space-y-3">
                        {need.top_matches.map((m) => (
                            <MatchCard key={m.offerer_id} match={m} />
                        ))}
                    </div>
                </div>
            ) : (
                <div className="text-center py-4 rounded-xl bg-slate-800/30 border border-slate-700/30">
                    <Users className="w-6 h-6 text-slate-600 mx-auto mb-1" />
                    <p className="text-xs text-slate-500">
                        Sin matches disponibles en la red actual.
                        <br />
                        Considera incorporar nuevos participantes.
                    </p>
                </div>
            )}
        </div>
    );
}

function GapBar({ gap }: { gap: CommunityGap }) {
    const pct = Math.min(gap.coverage_ratio * 100, 100);
    const barColor =
        gap.gap_severity === "critical"
            ? "bg-rose-500"
            : gap.gap_severity === "warning"
            ? "bg-amber-500"
            : "bg-emerald-500";

    return (
        <div className="space-y-1.5">
            <div className="flex justify-between items-center text-xs">
                <span className="text-slate-300 font-medium">{gap.dimension_label}</span>
                <div className="flex items-center gap-3 text-slate-400">
                    <span>Necesitan: <strong className="text-white">{gap.participants_needing}</strong></span>
                    <span>Ofrecen: <strong className="text-white">{gap.participants_offering}</strong></span>
                    <span
                        className={`font-black ${
                            gap.gap_severity === "critical"
                                ? "text-rose-400"
                                : gap.gap_severity === "warning"
                                ? "text-amber-400"
                                : "text-emerald-400"
                        }`}
                    >
                        {Math.round(gap.coverage_ratio * 100)}%
                    </span>
                </div>
            </div>
            <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                <div
                    className={`h-full rounded-full transition-all duration-700 ${barColor}`}
                    style={{ width: `${pct}%` }}
                />
            </div>
        </div>
    );
}

// ─── Página principal ─────────────────────────────────────────────

export default function MatchingPage() {
    const [matching, setMatching] = useState<MatchingData | null>(null);
    const [gaps, setGaps] = useState<GapsData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [lastRefresh, setLastRefresh] = useState(new Date());

    const fetchData = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const [urgentRes, gapsRes] = await Promise.all([
                apiFetch("/forms/matching/urgent?top_matches=3"),
                apiFetch("/forms/matching/gaps"),
            ]);

            if (!urgentRes.ok) throw new Error("Error al obtener necesidades urgentes");
            if (!gapsRes.ok) throw new Error("Error al obtener brechas comunitarias");

            const [urgentData, gapsData] = await Promise.all([
                urgentRes.json(),
                gapsRes.json(),
            ]);

            setMatching(urgentData);
            setGaps(gapsData);
            setLastRefresh(new Date());
        } catch (err) {
            setError(err instanceof Error ? err.message : "Error desconocido");
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const allUrgent = [
        ...(matching?.coherence_crimes || []),
        ...(matching?.warnings || []),
    ];

    return (
        <div className="space-y-8 pb-16">
            {/* Header */}
            <div className="flex items-start justify-between">
                <div>
                    <h2 className="text-xl font-black text-white uppercase tracking-wider flex items-center gap-3">
                        <Activity className="w-5 h-5 text-emerald-500" />
                        Motor de Matching — Cohorte Cero
                    </h2>
                    <p className="text-slate-400 text-sm mt-1">
                        Emparejamiento de ofertas y necesidades para garantizar la cobertura del SDV.
                    </p>
                </div>
                <button
                    onClick={fetchData}
                    disabled={loading}
                    className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 border border-slate-700 text-slate-300 hover:text-white hover:border-slate-500 text-sm transition-all disabled:opacity-50"
                >
                    <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
                    Actualizar
                </button>
            </div>

            {/* Última actualización */}
            <p className="text-xs text-slate-500 -mt-6 flex items-center gap-1">
                <Clock className="w-3 h-3" />
                Última actualización: {lastRefresh.toLocaleTimeString("es-CO")}
            </p>

            {/* Error */}
            {error && (
                <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm flex items-center gap-3">
                    <AlertTriangle className="w-5 h-5 shrink-0" />
                    {error}
                </div>
            )}

            {/* Skeleton */}
            {loading && !matching && (
                <div className="space-y-4 animate-pulse">
                    {[...Array(3)].map((_, i) => (
                        <div key={i} className="h-48 bg-slate-900/50 rounded-2xl border border-slate-800" />
                    ))}
                </div>
            )}

            {!loading && matching && (
                <>
                    {/* Banner de Crímenes de Coherencia */}
                    <CoherenceCrimeBanner count={matching.crimes_count} />

                    {/* KPIs */}
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        <div className="rounded-2xl border border-rose-500/20 bg-rose-500/5 p-5 text-center">
                            <div className="text-3xl font-black text-rose-400 mb-1">
                                {matching.crimes_count}
                            </div>
                            <div className="text-xs text-slate-400 uppercase font-bold tracking-wider">
                                Crímenes de Coherencia
                            </div>
                        </div>
                        <div className="rounded-2xl border border-amber-500/20 bg-amber-500/5 p-5 text-center">
                            <div className="text-3xl font-black text-amber-400 mb-1">
                                {matching.warnings?.length || 0}
                            </div>
                            <div className="text-xs text-slate-400 uppercase font-bold tracking-wider">
                                Necesidades Urgentes
                            </div>
                        </div>
                        <div className="rounded-2xl border border-slate-700 bg-slate-900/50 p-5 text-center">
                            <div className="text-3xl font-black text-white mb-1">
                                {gaps?.critical_count || 0}
                            </div>
                            <div className="text-xs text-slate-400 uppercase font-bold tracking-wider">
                                Brechas Críticas en Red
                            </div>
                        </div>
                    </div>

                    {/* Necesidades urgentes */}
                    <section>
                        <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
                            <AlertTriangle className="w-4 h-4 text-amber-500" />
                            Necesidades Sin Resolver
                            {allUrgent.length > 0 && (
                                <span className="px-2 py-0.5 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-black">
                                    {allUrgent.length}
                                </span>
                            )}
                        </h3>

                        {allUrgent.length === 0 ? (
                            <div className="text-center py-16 rounded-2xl border border-slate-800 bg-slate-900/30">
                                <CheckCircle2 className="w-12 h-12 text-emerald-500/20 mx-auto mb-3" />
                                <p className="text-slate-400 font-bold uppercase text-sm">
                                    Todas las necesidades urgentes están siendo atendidas
                                </p>
                                <p className="text-slate-600 text-xs mt-1">
                                    El SDV de la comunidad está protegido.
                                </p>
                            </div>
                        ) : (
                            <div className="space-y-6">
                                {allUrgent.map((need) => (
                                    <UrgentNeedCard key={need.participant_id} need={need} />
                                ))}
                            </div>
                        )}
                    </section>

                    {/* Brechas comunitarias */}
                    {gaps && (
                        <section>
                            <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
                                <BarChart3 className="w-4 h-4 text-blue-500" />
                                Cobertura de Dimensiones en la Red
                            </h3>

                            <div className="rounded-2xl border border-slate-800 bg-slate-900/50 backdrop-blur-xl p-6 space-y-5">
                                <p className="text-xs text-slate-500">
                                    Porcentaje de cobertura: cuántas personas ofrecen cada dimensión
                                    respecto a cuántas la necesitan. Bajo el 100% hay déficit.
                                </p>
                                {gaps.gaps.length === 0 ? (
                                    <p className="text-center text-slate-500 text-sm py-8">
                                        Sin datos de dimensiones suficientes aún.
                                    </p>
                                ) : (
                                    <div className="space-y-4">
                                        {gaps.gaps.map((g) => (
                                            <GapBar key={g.dimension} gap={g} />
                                        ))}
                                    </div>
                                )}
                            </div>
                        </section>
                    )}
                </>
            )}
        </div>
    );
}
