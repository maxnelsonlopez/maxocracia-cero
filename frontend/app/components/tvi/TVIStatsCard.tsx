"use client";

import React from "react";
import { motion } from "framer-motion";
import { Clock, Users, Activity, TrendingUp } from "lucide-react";

interface TVIStatsCardProps {
  label: string;
  value: string | number;
  subValue?: string;
  icon: "clock" | "users" | "activity" | "trend";
  color?: "blue" | "emerald" | "amber" | "rose" | "indigo";
}

const colorMap = {
  blue: "bg-blue-500/20 text-blue-400 border-blue-500/30",
  emerald: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
  amber: "bg-amber-500/20 text-amber-400 border-amber-500/30",
  rose: "bg-rose-500/20 text-rose-400 border-rose-500/30",
  indigo: "bg-indigo-500/20 text-indigo-400 border-indigo-500/30",
};

const iconMap = {
  clock: Clock,
  users: Users,
  activity: Activity,
  trend: TrendingUp,
};

export default function TVIStatsCard({ label, value, subValue, icon, color = "blue" }: TVIStatsCardProps) {
  const Icon = iconMap[icon];
  const colorStyles = colorMap[color];

  return (
    <motion.div
      whileHover={{ y: -5 }}
      className="p-6 bg-slate-900/50 backdrop-blur-md border border-slate-800 rounded-2xl flex flex-col gap-4 shadow-xl"
    >
      <div className="flex items-center justify-between">
        <div className={`p-3 rounded-xl border ${colorStyles}`}>
          <Icon size={24} />
        </div>
        {subValue && (
          <span className="text-xs font-medium px-2 py-1 bg-slate-800 rounded-full text-slate-400 border border-slate-700">
            {subValue}
          </span>
        )}
      </div>
      
      <div>
        <h4 className="text-sm font-medium text-slate-400 mb-1">{label}</h4>
        <div className="text-3xl font-bold text-slate-100 tracking-tight">
          {value}
        </div>
      </div>
    </motion.div>
  );
}
