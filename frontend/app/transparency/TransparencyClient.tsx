"use client";

import React, { useEffect, useState } from "react";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    Title,
    Tooltip,
    Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";
import {
    ShieldCheck,
    Wallet,
    TrendingUp,
    Landmark,
    RefreshCw,
    FileJson,
    AlertTriangle,
} from "lucide-react";
import { apiFetch } from "../lib/api";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);

interface TransparencyReport {
    report_type: string;
    principles: string[];
    subscription_stats: Array<{ tier: string; count: number; month: string }>;
    estimated_revenue_by_month: Record<string, number>;
    operational_costs: {
        hosting_servers: number;
        database: number;
        bandwidth: number;
        development_volunteer: number;
        legal_accounting: number;
        total_monthly_usd: number;
    };
    surplus_strategy: string;
    last_updated: string;
    auditable: boolean;
    blockchain_anchor: string | null;
}

const COST_LABELS: Record<string, string> = {
    hosting_servers: "Servidores",
    database: "Base de datos",
    bandwidth: "Ancho de banda",
    development_volunteer: "Desarrollo (voluntario)",
    legal_accounting: "Legal y contable",
};

const PRINCIPLES_ES: Record<string, string> = {
    "All financial flows are public": "Todos los flujos financieros son públicos",
    "No hidden costs": "Sin costos ocultos",
    "No profit maximization": "Sin maximización de lucro",
    "Surplus reinvested in open source": "Excedentes reinvertidos en open source",
};

const CHART_THEME = {
    grid: "rgba(51, 65, 85, 0.2)",
    ticks: "#64748b",
};

export default function TransparencyClient() {
    const [report, setReport] = useState<TransparencyReport | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        apiFetch("/subscriptions/transparency-report")
            .then((res) => {
                if (!res.ok) throw new Error("Error al obtener el reporte");
                return res.json();
            })
            .then((data: TransparencyReport) => setReport(data))
            .catch((err) => setError(err instanceof Error ? err.message : "Error desconocido"))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return (
        <div className="min-h-screen flex items-center justify-center">
            <div className="animate-pulse flex items-center gap-3 text-slate-500">
                <RefreshCw className="w-5 h-5 animate-spin" />
                <span>Cargando reporte de transparencia…</span>
            </div>
        </div>
    );

    if (error || !report) return (
        <div className="min-h-screen flex items-center justify-center p-8">
            <div className="p-8 bg-rose-500/10 border border-rose-500/20 rounded-2xl flex items-center gap-4 text-rose-500 max-w-lg">
                <AlertTriangle className="w-6 h-6" />
                <div>
                    <h3 className="font-bold uppercase tracking-wider">Reporte no disponible</h3>
                    <p className="text-sm opacity-80">{error || "Sin datos"}. El endpoint público sigue siendo accesible en /subscriptions/transparency-report.</p>
                </div>
            </div>
        </div>
    );

    const { operational_costs: costs, estimated_revenue_by_month: revenue, principles, surplus_strategy, last_updated, auditable } = report;

    const revenueMonths = Object.entries(revenue).sort(([a], [b]) => a.localeCompare(b));
    const totalRevenue = revenueMonths.reduce((acc, [, v]) => acc + v, 0);
    const surplus = totalRevenue - costs.total_monthly_usd;

    const costEntries = Object.entries(costs).filter(([k]) => k !== "total_monthly_usd");
    const maxCost = Math.max(...costEntries.map(([, v]) => v), 1);

    const revenueChartData = {
        labels: revenueMonths.length ? revenueMonths.map(([m]) => m) : ["Sin ingresos aún"],
        datasets: [{
            label: "Ingresos estimados (USD)",
            data: revenueMonths.length ? revenueMonths.map(([, v]) => v) : [0],
            backgroundColor: "rgba(16, 185, 129, 0.7)",
            borderRadius: 8,
            borderColor: "#0f172a",
            borderWidth: 1,
        }],
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
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
        <div className="min-h-screen pt-24 pb-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-8">
            {/* Header */}
            <div className="text-center space-y-3">
                <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold uppercase tracking-wider">
                    <ShieldCheck className="w-3.5 h-3.5" />
                    Axioma T13 · Transparencia Radical
                </div>
                <h1 className="text-4xl font-black text-white tracking-tight">Reporte de Transparencia</h1>
                <p className="text-slate-400 max-w-2xl mx-auto">
                    La Maxocracia no pide confianza ciega: hace visible lo invisible.
                    Cada flujo financiero de este proyecto es público y auditable por cualquiera.
                </p>
                <p className="text-xs text-slate-500">
                    Actualizado: {new Date(last_updated).toLocaleString("es-CO")} ·{" "}
                    {auditable ? "Auditable" : "No auditable"}
                </p>
            </div>

            {/* KPIs */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="p-6 bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl">
                    <div className="flex items-center gap-2 text-slate-400 mb-3">
                        <Landmark className="w-4 h-4" />
                        <span className="text-xs font-bold uppercase tracking-wider">Costo mensual</span>
                    </div>
                    <div className="text-3xl font-black text-white">${costs.total_monthly_usd} USD</div>
                </div>
                <div className="p-6 bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl">
                    <div className="flex items-center gap-2 text-slate-400 mb-3">
                        <Wallet className="w-4 h-4" />
                        <span className="text-xs font-bold uppercase tracking-wider">Ingresos acumulados</span>
                    </div>
                    <div className="text-3xl font-black text-emerald-400">${totalRevenue} USD</div>
                </div>
                <div className="p-6 bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl">
                    <div className="flex items-center gap-2 text-slate-400 mb-3">
                        <TrendingUp className="w-4 h-4" />
                        <span className="text-xs font-bold uppercase tracking-wider">Superávit neto</span>
                    </div>
                    <div className={`text-3xl font-black ${surplus >= 0 ? "text-emerald-400" : "text-amber-400"}`}>
                        ${surplus} USD
                    </div>
                </div>
                <div className="p-6 bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl">
                    <div className="flex items-center gap-2 text-slate-400 mb-3">
                        <ShieldCheck className="w-4 h-4" />
                        <span className="text-xs font-bold uppercase tracking-wider">Ancla blockchain</span>
                    </div>
                    <div className="text-3xl font-black text-white">
                        {report.blockchain_anchor ? "Activa" : "Pendiente"}
                    </div>
                </div>
            </div>

            {/* Costos e ingresos */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-6">Costos operativos mensuales</h3>
                    <div className="space-y-4">
                        {costEntries.map(([key, value]) => (
                            <div key={key}>
                                <div className="flex justify-between text-xs mb-1">
                                    <span className="text-slate-400">{COST_LABELS[key] || key}</span>
                                    <span className="font-bold text-white">${value} USD</span>
                                </div>
                                <div className="h-2.5 rounded-full bg-slate-800 overflow-hidden">
                                    <div
                                        className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-blue-500 transition-all duration-700"
                                        style={{ width: `${(value / maxCost) * 100}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                        <div className="pt-3 border-t border-slate-800 flex justify-between text-sm">
                            <span className="text-slate-400 font-semibold">Total mensual</span>
                            <span className="font-black text-white">${costs.total_monthly_usd} USD</span>
                        </div>
                    </div>
                </div>

                <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-6">Ingresos estimados por mes</h3>
                    <div className="h-[260px]">
                        <Bar data={revenueChartData} options={chartOptions} />
                    </div>
                    {revenueMonths.length === 0 && (
                        <p className="mt-3 text-xs text-slate-500">
                            Aún no hay contribuciones registradas. Cada contribución de la comunidad se hace visible aquí automáticamente.
                        </p>
                    )}
                </div>
            </div>

            {/* Principios y estrategia */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-6">Principios del reporte</h3>
                    <ul className="space-y-3">
                        {principles.map((p) => (
                            <li key={p} className="flex items-start gap-3 px-4 py-3 rounded-xl bg-slate-800/50 border border-slate-700/50">
                                <ShieldCheck className="w-4 h-4 text-emerald-500 mt-0.5 shrink-0" />
                                <div>
                                    <div className="text-sm text-slate-200 font-medium">{PRINCIPLES_ES[p] || p}</div>
                                    <div className="text-[10px] text-slate-500 italic">{p}</div>
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>

                <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-6">Estrategia de excedentes</h3>
                    <p className="text-sm text-slate-300 leading-relaxed mb-4">
                        {surplus_strategy}
                    </p>
                    <div className="p-4 rounded-xl bg-emerald-500/5 border border-emerald-500/20">
                        <p className="text-xs text-emerald-400/90 leading-relaxed">
                            <strong>Nota:</strong> este reporte no contiene datos personales de contribuyentes.
                            La transparencia se aplica a los sistemas, no a las personas (Axioma 6: la revelación responsable y la Capa de Ternura protegen lo inefable).
                        </p>
                    </div>
                    <a
                        href="/subscriptions/transparency-report"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="mt-4 inline-flex items-center gap-2 text-xs text-slate-400 hover:text-emerald-400 transition-colors"
                    >
                        <FileJson className="w-3.5 h-3.5" />
                        Ver datos crudos (JSON del endpoint)
                    </a>
                </div>
            </div>
        </div>
    );
}
