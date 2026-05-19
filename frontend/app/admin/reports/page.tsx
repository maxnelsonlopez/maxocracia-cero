"use client";

import React, { useEffect, useState } from "react";
import { apiFetch } from "../../lib/api";
import { 
    BarChart3, 
    Target, 
    Zap, 
    Clock, 
    ShieldCheck,
    ArrowUpRight
} from "lucide-react";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

interface ReportData {
    categories: {
        exchange_types: Record<string, number>;
        top_offered_categories: Record<string, number>;
        top_needed_categories: Record<string, number>;
        match_rate: number;
    };
    resolution: {
        avg_resolution_score: number;
        resolution_by_urgency: Record<string, number>;
        avg_days_to_resolve: number;
        success_rate_by_category: Record<string, number>;
    };
}

export default function ReportsPage() {
    const [data, setData] = useState<ReportData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchData() {
            try {
                const [catRes, resRes] = await Promise.all([
                    apiFetch("/forms/dashboard/categories"),
                    apiFetch("/forms/dashboard/resolution")
                ]);

                if (catRes.ok && resRes.ok) {
                    const categories = await catRes.json();
                    const resolution = await resRes.json();
                    setData({ categories, resolution });
                }
            } catch (err) {
                console.error("Error fetching reports:", err);
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    const barOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: 'rgba(15, 23, 42, 0.9)',
                padding: 12,
                titleFont: { size: 10 },
                bodyFont: { size: 12 }
            }
        },
        scales: {
            x: { grid: { display: false }, ticks: { color: '#64748b', font: { size: 10 } } },
            y: { grid: { color: 'rgba(51, 65, 85, 0.2)' }, ticks: { color: '#64748b', font: { size: 10 } } }
        }
    };

    const categoryData = {
        labels: Object.keys(data?.categories.exchange_types || {}),
        datasets: [{
            data: Object.values(data?.categories.exchange_types || {}),
            backgroundColor: 'rgba(16, 185, 129, 0.6)',
            borderRadius: 8,
            hoverBackgroundColor: 'rgba(16, 185, 129, 0.8)',
        }]
    };

    if (loading) return (
        <div className="flex items-center justify-center h-[calc(100vh-200px)]">
            <div className="flex flex-col items-center gap-4">
                <div className="w-12 h-12 border-4 border-purple-500/20 border-t-purple-500 rounded-full animate-spin" />
                <p className="text-xs text-slate-500 font-bold uppercase tracking-widest">Generando Informes de Impacto...</p>
            </div>
        </div>
    );

    return (
        <div className="space-y-8 pb-12">
            {/* Impact KPIs */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <ImpactCard 
                    label="Tasa de Match"
                    value={`${data?.categories.match_rate}%`}
                    icon={Target}
                    desc="Necesidades con oferta disponible"
                    color="emerald"
                />
                <ImpactCard 
                    label="Efectividad"
                    value={`${data?.resolution.avg_resolution_score}/10`}
                    icon={Zap}
                    desc="Puntaje promedio de resolución"
                    color="amber"
                />
                <ImpactCard 
                    label="Tiempo de Respuesta"
                    value={`${data?.resolution.avg_days_to_resolve}d`}
                    icon={Clock}
                    desc="Promedio desde intercambio a cierre"
                    color="blue"
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Category Breakdown Chart */}
                <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-3xl p-8">
                    <div className="flex items-center justify-between mb-8">
                        <div>
                            <h3 className="text-lg font-bold text-white">Distribución por Categoría</h3>
                            <p className="text-xs text-slate-500">Volumen de intercambios registrados</p>
                        </div>
                        <BarChart3 className="w-5 h-5 text-slate-600" />
                    </div>
                    <div className="h-[300px]">
                        <Bar data={categoryData} options={barOptions} />
                    </div>
                </div>

                {/* Success Rate Table */}
                <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-3xl p-8">
                    <div className="flex items-center justify-between mb-8">
                        <div>
                            <h3 className="text-lg font-bold text-white">Tasa de Éxito por Sector</h3>
                            <p className="text-xs text-slate-500">Resolución efectiva (score &gt;= 7)</p>
                        </div>
                        <ShieldCheck className="w-5 h-5 text-emerald-500" />
                    </div>
                    <div className="space-y-6">
                        {Object.entries(data?.resolution.success_rate_by_category || {}).map(([cat, rate]) => (
                            <div key={cat} className="space-y-2">
                                <div className="flex justify-between text-xs">
                                    <span className="font-bold text-slate-400 uppercase">{cat}</span>
                                    <span className="font-black text-white">{rate}%</span>
                                </div>
                                <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                                    <div 
                                        className="h-full bg-emerald-500" 
                                        style={{ width: `${rate}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Critical Needs Analysis */}
            <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-3xl p-8">
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h3 className="text-lg font-bold text-white">Brechas de Necesidad</h3>
                        <p className="text-xs text-slate-500">Categorías con más demanda no resuelta</p>
                    </div>
                    <button className="px-4 py-2 bg-slate-800 border border-slate-700 rounded-xl text-xs font-bold text-white hover:bg-slate-700 transition-colors flex items-center gap-2">
                        Exportar CSV
                        <ArrowUpRight className="w-4 h-4" />
                    </button>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                    <div>
                        <h4 className="text-[10px] font-black text-rose-500 uppercase tracking-widest mb-4">Top Necesidades (Demanda)</h4>
                        <div className="space-y-4">
                            {Object.entries(data?.categories.top_needed_categories || {}).map(([cat, count], i) => (
                                <div key={cat} className="flex items-center gap-4">
                                    <span className="text-xs font-black text-slate-700 w-4">{i+1}</span>
                                    <div className="flex-1 text-sm font-bold text-slate-300">{cat}</div>
                                    <div className="px-3 py-1 bg-rose-500/10 text-rose-400 rounded-lg text-xs font-black">{count} pts</div>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div>
                        <h4 className="text-[10px] font-black text-emerald-500 uppercase tracking-widest mb-4">Top Ofertas (Recursos)</h4>
                        <div className="space-y-4">
                            {Object.entries(data?.categories.top_offered_categories || {}).map(([cat, count], i) => (
                                <div key={cat} className="flex items-center gap-4">
                                    <span className="text-xs font-black text-slate-700 w-4">{i+1}</span>
                                    <div className="flex-1 text-sm font-bold text-slate-300">{cat}</div>
                                    <div className="px-3 py-1 bg-emerald-500/10 text-emerald-400 rounded-lg text-xs font-black">{count} pts</div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

interface ImpactCardProps {
    label: string;
    value: string;
    icon: React.ComponentType<{ className?: string }>;
    desc: string;
    color: "emerald" | "amber" | "blue";
}

function ImpactCard({ label, value, icon: Icon, desc, color }: ImpactCardProps) {
    const colors: Record<"emerald" | "amber" | "blue", string> = {
        emerald: "text-emerald-500 bg-emerald-500/10 border-emerald-500/20",
        amber: "text-amber-500 bg-amber-500/10 border-amber-500/20",
        blue: "text-blue-500 bg-blue-500/10 border-blue-500/20"
    };

    return (
        <div className="p-8 bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-3xl hover:border-slate-700 transition-all group">
            <div className={`p-3 w-fit rounded-2xl border mb-6 ${colors[color]}`}>
                <Icon className="w-6 h-6" />
            </div>
            <div className="text-4xl font-black text-white mb-2 tracking-tight">{value}</div>
            <div className="text-sm font-bold text-slate-200 mb-1">{label}</div>
            <p className="text-xs text-slate-500 leading-relaxed">{desc}</p>
        </div>
    );
}
