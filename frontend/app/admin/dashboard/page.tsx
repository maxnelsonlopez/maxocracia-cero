"use client";

import React, { useEffect, useState } from "react";
import {
    Users,
    DollarSign,
    TrendingUp,
    Target,
    AlertCircle,
    Clock,
    CheckCircle2,
    Activity,
    HandHelping,
    Zap,
    BarChart3
} from "lucide-react";
import MetricCard from "@/app/components/admin/MetricCard";
import TrendChart from "@/app/components/admin/TrendChart";

interface DashboardData {
    financials: {
        total_users: number;
        active_contributors: number;
        mrr_usd_estimated: number;
        surplus: number;
        tiers_breakdown: Array<{ tier: string, count: number }>;
    };
    operational: {
        total_participants: number;
        total_exchanges: number;
        uth_mobilized: number;
        resolution_rate: number;
        urgency_distribution: Record<string, number>;
    };
    trends: {
        dates: string[];
        exchanges: number[];
        uth: number[];
    };
    alerts: Array<{
        id: number;
        participant_name: string;
        follow_up_priority: string;
        follow_up_reason: string;
        date: string;
    }>;
}

export default function AdminDashboard() {
    const [data, setData] = useState<DashboardData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function fetchAllData() {
            try {
                const token = localStorage.getItem("mc_token");
                const headers = { "Authorization": `Bearer ${token}` };

                const [finRes, opRes, trendRes, alertRes] = await Promise.all([
                    fetch("/subscriptions/admin/stats", { headers }),
                    fetch("/forms/dashboard/stats", { headers }),
                    fetch("/forms/dashboard/trends", { headers }),
                    fetch("/forms/dashboard/alerts", { headers })
                ]);

                if (!finRes.ok || !opRes.ok) throw new Error("Error al obtener datos del servidor");

                const financials = await finRes.json();
                const operational = await opRes.json();
                const trends = await trendRes.json();
                const alertsData = await alertRes.json();

                setData({
                    financials,
                    operational,
                    trends: {
                        dates: trends.map((t: any) => t.date),
                        exchanges: trends.map((t: any) => t.exchanges),
                        uth: trends.map((t: any) => t.uth)
                    },
                    alerts: alertsData.alerts || []
                });
            } catch (err) {
                setError(err instanceof Error ? err.message : "Error desconocido");
            } finally {
                setLoading(false);
            }
        }

        fetchAllData();
    }, []);

    if (loading) return (
        <div className="space-y-8 animate-pulse">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[...Array(4)].map((_, i) => (
                    <div key={i} className="h-32 bg-slate-900/50 rounded-2xl border border-slate-800" />
                ))}
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="h-[350px] bg-slate-900/50 rounded-2xl border border-slate-800" />
                <div className="h-[350px] bg-slate-900/50 rounded-2xl border border-slate-800" />
            </div>
        </div>
    );

    if (error) return (
        <div className="p-8 bg-rose-500/10 border border-rose-500/20 rounded-2xl flex items-center gap-4 text-rose-500">
            <AlertCircle className="w-6 h-6" />
            <div>
                <h3 className="font-bold uppercase tracking-wider">Fallo de Sincronización</h3>
                <p className="text-sm opacity-80">{error}. Verifica tus credenciales de Administrador.</p>
            </div>
        </div>
    );

    return (
        <div className="space-y-8 pb-12">
            {/* Main Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard
                    label="UTH Movilizado"
                    value={data?.operational.uth_mobilized || 0}
                    icon={Zap}
                    trend={{ value: "+12.5%", direction: "up" }}
                    color="amber"
                    delay={0.1}
                />
                <MetricCard
                    label="Participantes Red"
                    value={data?.operational.total_participants || 0}
                    icon={Users}
                    trend={{ value: "+4", direction: "up" }}
                    color="blue"
                    delay={0.2}
                />
                <MetricCard
                    label="Intercambios"
                    value={data?.operational.total_exchanges || 0}
                    icon={HandHelping}
                    trend={{ value: "Estable", direction: "neutral" }}
                    color="purple"
                    delay={0.3}
                />
                <MetricCard
                    label="Resolución"
                    value={`${data?.operational.resolution_rate || 0}%`}
                    icon={CheckCircle2}
                    trend={{ value: "+2%", direction: "up" }}
                    color="emerald"
                    delay={0.4}
                />
            </div>

            {/* Financial & Trend Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 space-y-8">
                    {/* Activity Chart */}
                    <TrendChart
                        title="Actividad de Intercambio (30 días)"
                        labels={data?.trends.dates || []}
                        data={data?.trends.exchanges || []}
                        label="Intercambios"
                        color="rgb(139, 92, 246)" // Purple 500
                    />

                    {/* Secondary Stats Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
                            <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-6 flex items-center gap-2">
                                <DollarSign className="w-4 h-4 text-emerald-500" />
                                Salud Financiera
                            </h3>
                            <div className="space-y-6">
                                <div>
                                    <div className="flex justify-between text-xs mb-2">
                                        <span className="text-slate-400">MRR Estimado</span>
                                        <span className="text-white font-bold">${data?.financials.mrr_usd_estimated}</span>
                                    </div>
                                    <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                                        <div className="h-full bg-emerald-500 w-[75%]" />
                                    </div>
                                </div>
                                <div>
                                    <div className="flex justify-between text-xs mb-2">
                                        <span className="text-slate-400">Excedente Ético</span>
                                        <span className="text-white font-bold">${data?.financials.surplus}</span>
                                    </div>
                                    <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                                        <div className="h-full bg-blue-500 w-[40%]" />
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
                            <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-6 flex items-center gap-2">
                                <BarChart3 className="w-4 h-4 text-amber-500" />
                                Urgencia en Red
                            </h3>
                            <div className="space-y-4">
                                {Object.entries(data?.operational.urgency_distribution || {}).map(([level, count]) => (
                                    <div key={level} className="flex items-center justify-between text-xs">
                                        <span className="capitalize text-slate-400">{level}</span>
                                        <span className={`font-bold ${
                                            level === 'Alta' ? 'text-rose-400' : 
                                            level === 'Media' ? 'text-amber-400' : 'text-emerald-400'
                                        }`}>{count}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Sidebar: Alerts & Tiers */}
                <div className="space-y-8">
                    {/* Critical Alerts */}
                    <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
                        <h3 className="text-sm font-bold text-white mb-6 flex items-center gap-2">
                            <Activity className="w-4 h-4 text-rose-500 animate-pulse" />
                            Alertas de Seguimiento
                        </h3>
                        <div className="space-y-4">
                            {data?.alerts.length === 0 ? (
                                <div className="text-center py-8">
                                    <CheckCircle2 className="w-8 h-8 text-emerald-500/20 mx-auto mb-2" />
                                    <p className="text-xs text-slate-500 uppercase font-bold">Todo en orden</p>
                                </div>
                            ) : (
                                data?.alerts.map((alert) => (
                                    <div key={alert.id} className="p-3 rounded-xl bg-slate-800/30 border border-slate-700/30 hover:border-slate-600 transition-colors cursor-pointer group">
                                        <div className="flex justify-between items-start mb-1">
                                            <span className="text-xs font-bold text-white truncate max-w-[120px]">{alert.participant_name}</span>
                                            <span className={`text-[10px] px-1.5 py-0.5 rounded uppercase font-black ${
                                                alert.follow_up_priority === 'Alta' ? 'bg-rose-500/20 text-rose-400' : 'bg-amber-500/20 text-amber-400'
                                            }`}>
                                                {alert.follow_up_priority}
                                            </span>
                                        </div>
                                        <p className="text-[10px] text-slate-400 line-clamp-2 leading-relaxed">
                                            {alert.follow_up_reason}
                                        </p>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>

                    {/* Distribution Tiers */}
                    <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-6">
                        <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-6">Distribución Contribuidores</h3>
                        <div className="space-y-4">
                            {data?.financials.tiers_breakdown.map((t) => (
                                <div key={t.tier} className="space-y-1.5">
                                    <div className="flex justify-between text-[10px] uppercase font-bold text-slate-500">
                                        <span>Tier {t.tier}</span>
                                        <span>{t.count}</span>
                                    </div>
                                    <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                                        <div 
                                            className="h-full bg-purple-500" 
                                            style={{ width: `${(t.count / (data.financials.active_contributors || 1)) * 100}%` }}
                                        />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
