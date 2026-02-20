"use client";

import React, { useEffect, useState } from "react";
import {
    Users,
    DollarSign,
    TrendingUp,
    Target,
    AlertCircle,
    Clock,
    CheckCircle2
} from "lucide-react";

interface AdminStats {
    total_users: number;
    active_contributors: number;
    mrr_usd_estimated: number;
    tiers_breakdown: Array<{ tier: string, count: number }>;
    operational_costs: number;
    surplus: number;
}

export default function AdminDashboard() {
    const [stats, setStats] = useState<AdminStats | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function fetchStats() {
            try {
                const token = localStorage.getItem("mc_token");
                const res = await fetch("/subscriptions/admin/stats", {
                    headers: {
                        "Authorization": `Bearer ${token}`
                    }
                });

                if (!res.ok) throw new Error("Acceso denegado o error de red");

                const data = await res.json();
                setStats(data);
            } catch (err) {
                setError(err instanceof Error ? err.message : "Error desconocido");
            } finally {
                setLoading(false);
            }
        }

        fetchStats();
    }, []);

    if (loading) return <div className="animate-pulse space-y-4">
        <div className="h-32 bg-slate-900 rounded-2xl border border-slate-800" />
        <div className="grid grid-cols-3 gap-4">
            <div className="h-40 bg-slate-900 rounded-2xl border border-slate-800" />
            <div className="h-40 bg-slate-900 rounded-2xl border border-slate-800" />
            <div className="h-40 bg-slate-900 rounded-2xl border border-slate-800" />
        </div>
    </div>;

    if (error) return (
        <div className="p-8 bg-red-500/10 border border-red-500/20 rounded-2xl flex items-center gap-4 text-red-500">
            <AlertCircle className="w-6 h-6" />
            <div>
                <h3 className="font-bold">Error de Autenticación</h3>
                <p className="text-sm opacity-80">{error}. Asegúrate de estar logueado como Admin.</p>
            </div>
        </div>
    );

    return (
        <div className="space-y-8">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    label="Usuarios Totales"
                    value={stats?.total_users || 0}
                    icon={Users}
                    trend="+5%"
                    color="blue"
                />
                <StatCard
                    label="Contribuidores"
                    value={stats?.active_contributors || 0}
                    icon={Target}
                    trend="+12%"
                    color="emerald"
                />
                <StatCard
                    label="MRR (Estimado)"
                    value={`$${stats?.mrr_usd_estimated || 0}`}
                    icon={DollarSign}
                    trend="+8%"
                    color="amber"
                />
                <StatCard
                    label="Excedente Ético"
                    value={`$${stats?.surplus || 0}`}
                    icon={TrendingUp}
                    trend="Estable"
                    color="purple"
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Tiers Breakdown */}
                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-lg font-bold text-white mb-6">Distribución por Tier</h3>
                    <div className="space-y-4">
                        {stats?.tiers_breakdown.map((t) => (
                            <div key={t.tier} className="flex items-center gap-4">
                                <div className="w-24 text-sm font-medium text-slate-400 capitalize">{t.tier}</div>
                                <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-emerald-500"
                                        style={{ width: `${(t.count / (stats.active_contributors || 1)) * 100}%` }}
                                    />
                                </div>
                                <div className="w-12 text-sm text-right font-bold text-white">{t.count}</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* System Alerts */}
                <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
                        <Activity className="w-5 h-5 text-emerald-500" />
                        Alertas de Verificación
                    </h3>
                    <div className="space-y-4">
                        <AlertItem
                            icon={Clock}
                            title="3 pagos Cripto pendientes"
                            desc="Validación de TX hash requerida."
                            type="warning"
                        />
                        <AlertItem
                            icon={CheckCircle2}
                            title="Sistema saludable"
                            desc="Latencia de API: 45ms"
                            type="success"
                        />
                    </div>
                </div>
            </div>
        </div>
    );
}

function StatCard({ label, value, icon: Icon, trend, color }: any) {
    const colorMap: any = {
        blue: "text-blue-500 bg-blue-500/10 border-blue-500/20",
        emerald: "text-emerald-500 bg-emerald-500/10 border-emerald-500/20",
        amber: "text-amber-500 bg-amber-500/10 border-amber-500/20",
        purple: "text-purple-500 bg-purple-500/10 border-purple-500/20",
    };

    return (
        <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl hover:border-slate-700 transition-colors group">
            <div className="flex items-center justify-between mb-4">
                <div className={`p-2 rounded-lg ${colorMap[color]}`}>
                    <Icon className="w-5 h-5" />
                </div>
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-500">{trend}</span>
            </div>
            <div className="text-2xl font-bold text-white mb-1">{value}</div>
            <div className="text-xs text-slate-400 font-medium">{label}</div>
        </div>
    );
}

function AlertItem({ icon: Icon, title, desc, type }: any) {
    const styles = type === 'warning' ? "text-amber-500 bg-amber-500/10" : "text-emerald-500 bg-emerald-500/10";
    return (
        <div className="flex gap-4">
            <div className={`p-2 rounded-lg h-fit ${styles}`}>
                <Icon className="w-4 h-4" />
            </div>
            <div>
                <div className="text-sm font-bold text-white">{title}</div>
                <div className="text-xs text-slate-500">{desc}</div>
            </div>
        </div>
    );
}

function Activity({ className }: { className?: string }) {
    return (
        <svg
            className={className}
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
        </svg>
    );
}
