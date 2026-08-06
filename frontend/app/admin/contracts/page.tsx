"use client";

import React, { useEffect, useState } from "react";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    Title,
    Tooltip,
    Legend,
    Filler,
} from "chart.js";
import { Line, Bar, Doughnut } from "react-chartjs-2";
import {
    FileCheck2,
    Activity,
    HeartHandshake,
    ShieldAlert,
    Gauge,
    Zap,
    ShieldCheck,
    AlertTriangle,
    ListChecks,
    Target,
} from "lucide-react";
import { apiFetch } from "../../lib/api";
import MetricCard from "@/app/components/admin/MetricCard";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

interface GammaAlert {
    contract_id: string;
    contract_state: string;
    participant_id: string;
    gamma: number;
}

interface SDVViolation {
    contract_id: string;
    contract_state: string;
    participant_id: string;
    status: Record<string, number> | string;
}

interface ContractStats {
    summary: {
        total: number;
        by_state: Record<string, number>;
    };
    gamma: {
        sample_count: number;
        avg: number | null;
        min: number | null;
        max: number | null;
        distribution: {
            lt_05: number;
            "05_08": number;
            "08_10": number;
            "10_12": number;
            gte_12: number;
        };
        alerts: GammaAlert[];
    };
    sdv: {
        violations_count: number;
        violations: SDVViolation[];
    };
    nps: {
        score: number | null;
        responses_count: number;
        distribution: {
            detractors: number;
            passives: number;
            promoters: number;
        };
        responses: Array<{
            contract_id: string;
            participant_id: string;
            score: number;
            comment: string | null;
        }>;
    };
    trends: {
        labels: string[];
        created: number[];
        activated: number[];
    };
    categories: Record<string, number>;
    vhv: {
        t: number;
        v: number;
        r: number;
    };
}

interface ContractListItem {
    contract_id: string;
    state: string;
}

const STATE_LABELS: Record<string, string> = {
    draft: "Borrador",
    pending: "Pendiente",
    active: "Activo",
    executed: "Ejecutado",
    retracted: "Retractado",
    expired: "Expirado",
};

const STATE_COLORS: Record<string, string> = {
    draft: "rgb(148, 163, 184)",
    pending: "rgb(245, 158, 11)",
    active: "rgb(16, 185, 129)",
    executed: "rgb(59, 130, 246)",
    retracted: "rgb(244, 63, 94)",
    expired: "rgb(100, 116, 139)",
};

const CATEGORY_META: Record<string, { target: number; label: string }> = {
    aseo: { target: 20, label: "Aseo compartido" },
    prestamo: { target: 15, label: "Préstamos sin usura" },
    comida: { target: 15, label: "Comidas colaborativas" },
};

const CHART_THEME = {
    grid: "rgba(51, 65, 85, 0.2)",
    ticks: "#64748b",
};

export default function ContractsDashboard() {
    const [stats, setStats] = useState<ContractStats | null>(null);
    const [contracts, setContracts] = useState<ContractListItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Formulario NPS
    const [npsContract, setNpsContract] = useState("");
    const [npsParticipant, setNpsParticipant] = useState("");
    const [npsScore, setNpsScore] = useState("");
    const [npsComment, setNpsComment] = useState("");
    const [npsSaving, setNpsSaving] = useState(false);
    const [npsFeedback, setNpsFeedback] = useState<string | null>(null);

    async function fetchData() {
        try {
            const [statsRes, listRes] = await Promise.all([
                apiFetch("/contracts/stats"),
                apiFetch("/contracts/"),
            ]);
            if (!statsRes.ok) throw new Error("Error al obtener métricas de contratos");
            const statsData: ContractStats = await statsRes.json();
            const listData = await listRes.json();
            setStats(statsData);
            setContracts(listData.contracts || []);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Error desconocido");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        fetchData();
    }, []);

    async function submitNps(e: React.FormEvent) {
        e.preventDefault();
        setNpsFeedback(null);
        if (!npsContract || !npsParticipant || !npsScore) {
            setNpsFeedback("Completa contrato, participante y puntuación.");
            return;
        }
        setNpsSaving(true);
        try {
            const res = await apiFetch(`/contracts/${npsContract}/nps`, {
                method: "POST",
                body: JSON.stringify({
                    participant_id: npsParticipant,
                    score: Number(npsScore),
                    comment: npsComment || undefined,
                }),
            });
            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.error || "Error al registrar NPS");
            }
            setNpsFeedback("Puntuación NPS registrada.");
            setNpsParticipant("");
            setNpsScore("");
            setNpsComment("");
            fetchData();
        } catch (err) {
            setNpsFeedback(err instanceof Error ? err.message : "Error desconocido");
        } finally {
            setNpsSaving(false);
        }
    }

    if (loading) return (
        <div className="space-y-8 animate-pulse">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[...Array(4)].map((_, i) => (
                    <div key={i} className="h-32 bg-slate-900/50 rounded-2xl border border-slate-800" />
                ))}
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="h-[300px] bg-slate-900/50 rounded-2xl border border-slate-800" />
                <div className="h-[300px] bg-slate-900/50 rounded-2xl border border-slate-800" />
            </div>
        </div>
    );

    if (error || !stats) return (
        <div className="p-8 bg-rose-500/10 border border-rose-500/20 rounded-2xl flex items-center gap-4 text-rose-500">
            <AlertTriangle className="w-6 h-6" />
            <div>
                <h3 className="font-bold uppercase tracking-wider">Fallo de Sincronización</h3>
                <p className="text-sm opacity-80">{error || "Sin datos de contratos"}. Verifica tus credenciales de Administrador.</p>
            </div>
        </div>
    );

    const { summary, gamma, sdv, nps, trends, categories, vhv } = stats;

    const stateEntries = Object.entries(summary.by_state);
    const stateData = {
        labels: stateEntries.map(([s]) => STATE_LABELS[s] || s),
        datasets: [{
            data: stateEntries.map(([, n]) => n),
            backgroundColor: stateEntries.map(([s]) => STATE_COLORS[s] || "rgb(148, 163, 184)"),
            borderColor: "#0f172a",
            borderWidth: 2,
        }],
    };

    const gammaBuckets = [
        { label: "< 0.5", value: gamma.distribution.lt_05, color: "rgb(244, 63, 94)" },
        { label: "0.5-0.8", value: gamma.distribution["05_08"], color: "rgb(249, 115, 22)" },
        { label: "0.8-1.0", value: gamma.distribution["08_10"], color: "rgb(245, 158, 11)" },
        { label: "1.0-1.2", value: gamma.distribution["10_12"], color: "rgb(16, 185, 129)" },
        { label: "≥ 1.2", value: gamma.distribution.gte_12, color: "rgb(59, 130, 246)" },
    ];
    const gammaChartData = {
        labels: gammaBuckets.map((b) => b.label),
        datasets: [{
            label: "Participantes",
            data: gammaBuckets.map((b) => b.value),
            backgroundColor: gammaBuckets.map((b) => b.color),
            borderRadius: 6,
            borderColor: "#0f172a",
            borderWidth: 1,
        }],
    };

    const trendChartData = {
        labels: trends.labels,
        datasets: [
            {
                label: "Creados",
                data: trends.created,
                borderColor: "rgb(16, 185, 129)",
                backgroundColor: "rgba(16, 185, 129, 0.1)",
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 3,
            },
            {
                label: "Activados",
                data: trends.activated,
                borderColor: "rgb(59, 130, 246)",
                backgroundColor: "rgba(59, 130, 246, 0.1)",
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 3,
            },
        ],
    };

    const categoryEntries = Object.entries(categories);
    const cohortProgress = categoryEntries.reduce((acc, [k, n]) => acc + Math.min(n, CATEGORY_META[k]?.target || n), 0);
    const cohortTarget = Object.values(CATEGORY_META).reduce((a, c) => a + c.target, 0);

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: { color: "#94a3b8", boxWidth: 12, boxHeight: 12 },
            },
            tooltip: {
                backgroundColor: "rgba(15, 23, 42, 0.9)",
                titleColor: "#fff",
                bodyColor: "#94a3b8",
                borderColor: "rgba(51, 65, 85, 0.5)",
                borderWidth: 1,
            },
        },
        scales: {
            x: {
                grid: { display: false },
                ticks: { color: CHART_THEME.ticks, font: { size: 10 } },
            },
            y: {
                grid: { color: CHART_THEME.grid, drawBorder: false },
                ticks: { color: CHART_THEME.ticks, font: { size: 10 }, maxTicksLimit: 5 },
            },
        },
    };

    return (
        <div className="space-y-8 pb-12">
            {/* KPIs */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard
                    label="Contratos Totales"
                    value={summary.total}
                    icon={FileCheck2}
                    color="blue"
                    delay={0}
                />
                <MetricCard
                    label="γ Promedio (Bienestar)"
                    value={gamma.avg !== null ? gamma.avg.toFixed(2) : "—"}
                    icon={Gauge}
                    color="emerald"
                    delay={0.1}
                />
                <MetricCard
                    label="NPS"
                    value={nps.score !== null ? nps.score.toFixed(1) : "—"}
                    icon={HeartHandshake}
                    color={nps.score !== null && nps.score >= 50 ? "emerald" : "amber"}
                    delay={0.2}
                />
                <MetricCard
                    label="Violaciones SDV"
                    value={sdv.violations_count}
                    icon={ShieldAlert}
                    color={sdv.violations_count > 0 ? "rose" : "emerald"}
                    delay={0.3}
                />
            </div>

            {/* Estado + Tendencias */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-6">Distribución por Estado</h3>
                    <div className="h-[220px] relative">
                        <Doughnut data={stateData} options={{ ...chartOptions, plugins: { ...chartOptions.plugins, legend: { position: "right", labels: { color: "#94a3b8", boxWidth: 10, boxHeight: 10 } } } }} />
                    </div>
                    <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
                        {stateEntries.map(([s, n]) => (
                            <div key={s} className="flex items-center justify-between px-3 py-1.5 rounded-lg bg-slate-800/50 border border-slate-700/50">
                                <span className="text-slate-400">{STATE_LABELS[s] || s}</span>
                                <span className="font-bold text-white">{n}</span>
                            </div>
                        ))}
                        {stateEntries.length === 0 && (
                            <div className="col-span-2 text-center text-slate-500 py-4">Sin contratos aún</div>
                        )}
                    </div>
                </div>

                <div className="lg:col-span-2 bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-6">Actividad Semanal (8 semanas)</h3>
                    <div className="h-[280px]">
                        <Line data={trendChartData} options={chartOptions} />
                    </div>
                </div>
            </div>

            {/* Gamma + SDV */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider">Distribución de γ</h3>
                        <span className="text-[10px] text-slate-500 uppercase">Invariante 1: γ ≥ 1.0</span>
                    </div>
                    <div className="h-[220px]">
                        <Bar data={gammaChartData} options={{ ...chartOptions, plugins: { ...chartOptions.plugins, legend: { display: false } } }} />
                    </div>

                    {gamma.alerts.length > 0 && (
                        <div className="mt-5">
                            <h4 className="text-xs font-bold text-rose-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                                <Zap className="w-3.5 h-3.5" /> Alertas γ &lt; 1.0 ({gamma.alerts.length})
                            </h4>
                            <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
                                {gamma.alerts.map((a) => (
                                    <div key={`${a.contract_id}-${a.participant_id}`} className="flex items-center justify-between px-3 py-2 rounded-lg bg-rose-500/10 border border-rose-500/20">
                                        <div>
                                            <div className="text-xs font-semibold text-rose-300">{a.contract_id}</div>
                                            <div className="text-[10px] text-slate-500">{a.participant_id} · {a.contract_state}</div>
                                        </div>
                                        <span className="text-sm font-black text-rose-400">{a.gamma.toFixed(2)}</span>
                                    </div>
                                ))}
                            </div>
                            <p className="mt-3 text-[10px] text-slate-500 leading-relaxed">
                                Según el Invariante 1, si γ cae por debajo de 1.0 el contrato debe activar el protocolo de retractación ética (Capa de Ternura, Cap. 17).
                            </p>
                        </div>
                    )}
                </div>

                <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider">Violaciones SDV</h3>
                        <span className="text-[10px] text-slate-500 uppercase">Suelo de Dignidad Vital</span>
                    </div>

                    {sdv.violations.length === 0 ? (
                        <div className="flex flex-col items-center justify-center h-[220px] gap-3 text-center">
                            <ShieldCheck className="w-10 h-10 text-emerald-500/60" />
                            <p className="text-sm text-slate-400">Sin violaciones registradas.<br />La dignidad vital está protegida.</p>
                        </div>
                    ) : (
                        <div className="space-y-2 max-h-[280px] overflow-y-auto pr-1">
                            {sdv.violations.map((v, i) => (
                                <div key={i} className="px-3 py-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20">
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <div className="text-xs font-semibold text-amber-300">{v.contract_id}</div>
                                            <div className="text-[10px] text-slate-500">{v.participant_id} · {v.contract_state}</div>
                                        </div>
                                        <AlertTriangle className="w-4 h-4 text-amber-400" />
                                    </div>
                                    {typeof v.status === "object" && v.status !== null && (
                                        <div className="mt-2 grid grid-cols-2 gap-1">
                                            {Object.entries(v.status).map(([dim, val]) => (
                                                <div key={dim} className="flex justify-between text-[10px]">
                                                    <span className="text-slate-500">{dim}</span>
                                                    <span className={Number(val) < 0.5 ? "text-rose-400 font-bold" : "text-slate-400"}>
                                                        {Number(val).toFixed(2)}
                                                    </span>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* NPS + Categorías */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider">NPS de la Cohorte</h3>
                        <span className="text-2xl font-black text-white">
                            {nps.score !== null ? nps.score.toFixed(1) : "—"}
                        </span>
                    </div>

                    <div className="space-y-3 mb-6">
                        {[
                            { label: "Promotores (9-10)", value: nps.distribution.promoters, color: "bg-emerald-500" },
                            { label: "Pasivos (7-8)", value: nps.distribution.passives, color: "bg-amber-500" },
                            { label: "Detractores (0-6)", value: nps.distribution.detractors, color: "bg-rose-500" },
                        ].map((seg) => (
                            <div key={seg.label}>
                                <div className="flex justify-between text-xs mb-1">
                                    <span className="text-slate-400">{seg.label}</span>
                                    <span className="font-bold text-white">{seg.value}</span>
                                </div>
                                <div className="h-2 rounded-full bg-slate-800 overflow-hidden">
                                    <div
                                        className={`h-full rounded-full ${seg.color} transition-all duration-700`}
                                        style={{ width: `${nps.responses_count > 0 ? (seg.value / nps.responses_count) * 100 : 0}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>

                    <form onSubmit={submitNps} className="space-y-3 p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
                        <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Registrar respuesta NPS</h4>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            <select
                                value={npsContract}
                                onChange={(e) => setNpsContract(e.target.value)}
                                className="px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-sm text-slate-200 outline-none focus:border-emerald-500/50"
                            >
                                <option value="">Contrato…</option>
                                {contracts.map((c) => (
                                    <option key={c.contract_id} value={c.contract_id}>
                                        {c.contract_id} ({c.state})
                                    </option>
                                ))}
                            </select>
                            <input
                                type="text"
                                value={npsParticipant}
                                onChange={(e) => setNpsParticipant(e.target.value)}
                                placeholder="participante (user-3)"
                                className="px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-sm text-slate-200 outline-none focus:border-emerald-500/50"
                            />
                            <input
                                type="number"
                                min={0}
                                max={10}
                                value={npsScore}
                                onChange={(e) => setNpsScore(e.target.value)}
                                placeholder="Puntuación 0-10"
                                className="px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-sm text-slate-200 outline-none focus:border-emerald-500/50"
                            />
                            <input
                                type="text"
                                value={npsComment}
                                onChange={(e) => setNpsComment(e.target.value)}
                                placeholder="Comentario (opcional)"
                                className="px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-sm text-slate-200 outline-none focus:border-emerald-500/50"
                            />
                        </div>
                        <button
                            type="submit"
                            disabled={npsSaving}
                            className="w-full px-4 py-2.5 rounded-xl text-sm font-bold bg-emerald-500 text-white hover:bg-emerald-600 transition-all disabled:opacity-50"
                        >
                            {npsSaving ? "Guardando…" : "Registrar puntuación"}
                        </button>
                        {npsFeedback && (
                            <p className={`text-xs ${npsFeedback.includes("registrada") ? "text-emerald-400" : "text-rose-400"}`}>
                                {npsFeedback}
                            </p>
                        )}
                    </form>
                </div>

                <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-2">
                        <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider">Progreso Cohorte Cero</h3>
                        <Target className="w-4 h-4 text-emerald-500" />
                    </div>
                    <p className="text-[10px] text-slate-500 mb-6">
                        Meta de validación: 50 contratos (20 aseo · 15 préstamos · 15 comidas)
                    </p>

                    <div className="mb-6">
                        <div className="flex justify-between text-xs mb-1">
                            <span className="text-slate-400">Contratos con categoría</span>
                            <span className="font-bold text-white">{cohortProgress} / {cohortTarget}</span>
                        </div>
                        <div className="h-3 rounded-full bg-slate-800 overflow-hidden">
                            <div
                                className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-blue-500 transition-all duration-700"
                                style={{ width: `${(cohortProgress / cohortTarget) * 100}%` }}
                            />
                        </div>
                    </div>

                    <div className="space-y-4">
                        {Object.entries(CATEGORY_META).map(([key, meta]) => {
                            const current = categories[key] || 0;
                            const pct = Math.min(100, (current / meta.target) * 100);
                            return (
                                <div key={key}>
                                    <div className="flex justify-between text-xs mb-1">
                                        <span className="text-slate-400">{meta.label}</span>
                                        <span className="font-bold text-white">{current} / {meta.target}</span>
                                    </div>
                                    <div className="h-2 rounded-full bg-slate-800 overflow-hidden">
                                        <div
                                            className={`h-full rounded-full transition-all duration-700 ${pct >= 100 ? "bg-emerald-500" : "bg-blue-500"}`}
                                            style={{ width: `${pct}%` }}
                                        />
                                    </div>
                                </div>
                            );
                        })}
                    </div>

                    <div className="mt-6 p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
                        <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-3 flex items-center gap-2">
                            <ListChecks className="w-3.5 h-3.5 text-emerald-500" /> Huella Vital Agregada (VHV)
                        </h4>
                        <div className="grid grid-cols-3 gap-2 text-center">
                            <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-700/50">
                                <div className="text-lg font-black text-blue-400">{vhv.t.toFixed(1)}</div>
                                <div className="text-[10px] text-slate-500 uppercase">Tiempo (h)</div>
                            </div>
                            <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-700/50">
                                <div className="text-lg font-black text-rose-400">{vhv.v.toFixed(1)}</div>
                                <div className="text-[10px] text-slate-500 uppercase">Vida (UCV)</div>
                            </div>
                            <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-700/50">
                                <div className="text-lg font-black text-amber-400">{vhv.r.toFixed(1)}</div>
                                <div className="text-[10px] text-slate-500 uppercase">Recursos</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="flex items-center gap-2 text-[10px] text-slate-600">
                <Activity className="w-3 h-3" />
                Los datos provienen del registro inmutable (T13): maxo_contracts, participantes, eventos y respuestas NPS.
            </div>
        </div>
    );
}
