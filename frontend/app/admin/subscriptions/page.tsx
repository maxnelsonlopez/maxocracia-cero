"use client";

import React, { useEffect, useState } from "react";
import { 
  CreditCard, 
  TrendingUp, 
  Users, 
  DollarSign, 
  AlertCircle, 
  Search,
  Sparkles,
  RefreshCw
} from "lucide-react";
import { motion } from "framer-motion";
import { apiFetch } from "../../lib/api";

interface SubUser {
  id: number;
  email: string;
  name: string;
  alias?: string;
  tier: string;
  sub_status?: string;
  expires_at?: string | null;
  payment_method?: string;
}

interface AdminStats {
  total_users: number;
  active_contributors: number;
  mrr_usd_estimated: number;
  tiers_breakdown: { tier: string; count: number }[];
  operational_costs: number;
  surplus: number;
}

export default function AdminSubscriptions() {
  const [users, setUsers] = useState<SubUser[]>([]);
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = () => {
    setLoading(true);
    setError(null);
    Promise.all([
      apiFetch("/subscriptions/admin/users").then((r) => {
        if (!r.ok) throw new Error(`users: ${r.status}`);
        return r.json();
      }),
      apiFetch("/subscriptions/admin/stats").then((r) => {
        if (!r.ok) throw new Error(`stats: ${r.status}`);
        return r.json();
      }),
    ])
      .then(([u, s]) => {
        setUsers(u);
        setStats(s);
      })
      .catch((e: unknown) => {
        setError(e instanceof Error ? e.message : "Error al cargar suscripciones.");
      })
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const filtered = users.filter((u) =>
    (u.name || "").toLowerCase().includes(query.toLowerCase()) ||
    (u.email || "").toLowerCase().includes(query.toLowerCase())
  );

  const tierColor: Record<string, string> = {
    enterprise: "bg-amber-500/10 text-amber-400 border-amber-500/20",
    contributor: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    free: "bg-slate-700/20 text-slate-400 border-slate-700",
  };

  const mrr = stats?.mrr_usd_estimated ?? 0;
  const surplus = stats?.surplus ?? 0;

  return (
    <div className="space-y-8 max-w-6xl">
      {/* Encabezado */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
          <CreditCard className="w-5 h-5 text-emerald-400" />
          Sostenibilidad Económica — Suscripciones
        </h3>
        <p className="text-xs text-slate-400 leading-relaxed">
          Datos reales de la Fase 2 (Sostenibilidad Económica): contribuidores activos por tier,
          MRR estimado y excedente sobre costos operativos. Todo cálculo auditable (T13).
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-semibold flex items-center gap-2">
          <AlertCircle className="w-4 h-4" />
          {error} — verifica que el backend esté activo y que la sesión sea de administrador.
        </div>
      )}

      {/* KPIs reales */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard icon={<Users className="w-5 h-5" />} label="Usuarios totales" value={stats ? String(stats.total_users) : "—"} sub="registrados en el sistema" />
        <KpiCard icon={<Sparkles className="w-5 h-5" />} label="Contribuidores activos" value={stats ? String(stats.active_contributors) : "—"} sub="suscripciones vigentes" />
        <KpiCard icon={<DollarSign className="w-5 h-5" />} label="MRR estimado" value={stats ? `$${mrr.toFixed(2)}` : "—"} sub="ingreso mensual recurrente" />
        <KpiCard icon={<TrendingUp className="w-5 h-5" />} label="Excedente" value={stats ? `$${surplus.toFixed(2)}` : "—"} sub={stats ? `costos operativos $${stats.operational_costs.toFixed(2)}` : "—"} positive={surplus >= 0} />
      </div>

      {/* Desglose por tier */}
      {stats && stats.tiers_breakdown.length > 0 && (
        <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
          <h4 className="font-semibold text-white text-sm mb-4">Desglose por tier</h4>
          <div className="flex flex-wrap gap-3">
            {stats.tiers_breakdown.map((t) => (
              <span key={t.tier} className={`px-3 py-1.5 rounded-lg text-xs font-semibold border ${tierColor[t.tier] || "bg-slate-700/20 text-slate-400 border-slate-700"}`}>
                {t.tier}: {t.count}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Tabla de usuarios */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h4 className="font-semibold text-white text-sm">Usuarios y estado de suscripción</h4>
          <div className="flex items-center gap-2">
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Buscar..."
                className="pl-9 pr-3 py-2 text-xs rounded-lg bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500 text-white placeholder:text-slate-600"
              />
            </div>
            <button onClick={load} disabled={loading} className="p-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-400 hover:text-white transition-colors">
              <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            </button>
          </div>
        </div>

        {loading ? (
          <div className="text-center py-12 text-xs text-slate-500">Cargando datos reales...</div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-12 text-xs text-slate-500">
            {users.length === 0 ? "Sin usuarios con suscripciones registradas." : "Sin resultados para la búsqueda."}
          </div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-slate-800">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950/60 text-slate-500">
                <tr>
                  <th className="px-4 py-3 font-semibold">Nombre</th>
                  <th className="px-4 py-3 font-semibold">Email</th>
                  <th className="px-4 py-3 font-semibold">Tier</th>
                  <th className="px-4 py-3 font-semibold">Estado</th>
                  <th className="px-4 py-3 font-semibold">Vence</th>
                  <th className="px-4 py-3 font-semibold">Método</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {filtered.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-900/40">
                    <td className="px-4 py-3 text-slate-300 font-medium">{u.name || u.alias || "—"}</td>
                    <td className="px-4 py-3 text-slate-400">{u.email}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold border ${tierColor[u.tier] || "bg-slate-700/20 text-slate-400 border-slate-700"}`}>
                        {u.tier || "free"}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-slate-400">{u.sub_status || "sin suscripción"}</td>
                    <td className="px-4 py-3 text-slate-400">{u.expires_at ? new Date(u.expires_at).toLocaleDateString() : "—"}</td>
                    <td className="px-4 py-3 text-slate-500">{u.payment_method || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

function KpiCard({ icon, label, value, sub, positive = true }: { icon: React.ReactNode; label: string; value: string; sub: string; positive?: boolean }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-slate-900/50 border border-slate-800 rounded-2xl p-5"
    >
      <div className="flex items-center gap-2 text-slate-500 mb-3">
        <span className="text-emerald-400">{icon}</span>
        <span className="text-[10px] font-semibold uppercase tracking-wider">{label}</span>
      </div>
      <p className={`text-2xl font-bold ${positive ? "text-white" : "text-red-400"}`}>{value}</p>
      <p className="text-[10px] text-slate-500 mt-1">{sub}</p>
    </motion.div>
  );
}
