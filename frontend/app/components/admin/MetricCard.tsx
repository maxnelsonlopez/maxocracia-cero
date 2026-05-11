"use client";

import React from "react";
import { LucideIcon, TrendingUp, TrendingDown, Minus } from "lucide-react";
import { motion } from "framer-motion";

interface MetricCardProps {
    label: string;
    value: string | number;
    icon: LucideIcon;
    trend?: {
        value: string;
        direction: "up" | "down" | "neutral";
    };
    color?: "blue" | "emerald" | "amber" | "purple" | "rose";
    delay?: number;
}

const colorMap = {
    blue: "text-blue-400 bg-blue-500/10 border-blue-500/20",
    emerald: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
    amber: "text-amber-400 bg-amber-500/10 border-amber-500/20",
    purple: "text-purple-400 bg-purple-500/10 border-purple-500/20",
    rose: "text-rose-400 bg-rose-500/10 border-rose-500/20",
};

export default function MetricCard({ 
    label, 
    value, 
    icon: Icon, 
    trend, 
    color = "blue",
    delay = 0 
}: MetricCardProps) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay }}
            className="p-6 bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl hover:border-slate-700 transition-all group relative overflow-hidden"
        >
            {/* Background Glow */}
            <div className={`absolute -right-4 -top-4 w-24 h-24 blur-3xl opacity-10 rounded-full bg-${color}-500`} />

            <div className="flex items-center justify-between mb-4">
                <div className={`p-2.5 rounded-xl border ${colorMap[color]} group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className="w-5 h-5" />
                </div>
                {trend && (
                    <div className={`flex items-center gap-1 text-[10px] font-bold px-2 py-1 rounded-full border ${
                        trend.direction === "up" ? "text-emerald-400 bg-emerald-500/10 border-emerald-500/20" :
                        trend.direction === "down" ? "text-rose-400 bg-rose-500/10 border-rose-500/20" :
                        "text-slate-400 bg-slate-500/10 border-slate-500/20"
                    }`}>
                        {trend.direction === "up" && <TrendingUp className="w-3 h-3" />}
                        {trend.direction === "down" && <TrendingDown className="w-3 h-3" />}
                        {trend.direction === "neutral" && <Minus className="w-3 h-3" />}
                        {trend.value}
                    </div>
                )}
            </div>

            <div className="relative">
                <div className="text-3xl font-bold text-white tracking-tight mb-1">{value}</div>
                <div className="text-xs text-slate-400 font-medium uppercase tracking-wider">{label}</div>
            </div>
        </motion.div>
    );
}
