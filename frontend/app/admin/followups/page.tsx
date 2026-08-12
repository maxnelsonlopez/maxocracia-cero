"use client";

import React, { useEffect, useState } from "react";
import { apiFetch } from "../../lib/api";
import {
  Search,
  ClipboardList,
  AlertTriangle,
  CalendarDays,
  Flag,
  ArrowRight,
  User,
} from "lucide-react";

interface FollowUp {
  id: number;
  follow_up_date?: string;
  participant_id?: number;
  related_interchange_id?: number;
  follow_up_type?: string;
  current_situation?: string;
  need_level?: number;
  situation_change?: string;
  active_interchanges_status?: string;
  new_needs_detected?: string[];
  new_offers_detected?: string[];
  emotional_state?: string;
  actions_required?: string[];
  follow_up_priority?: string;
  next_follow_up_date?: string;
  facilitator_notes?: string;
  learnings?: string;
  created_at?: string;
}

const TYPE_LABELS: Record<string, string> = {
  verification_completed: "Verificación completada",
  update_in_progress: "Actualización en curso",
  situation_evolution: "Evolución de situación",
  new_urgent_need: "Nueva necesidad urgente",
  need_resolved: "Necesidad resuelta",
  spontaneous_feedback: "Retroalimentación espontánea",
  routine_check: "Chequeo rutinario",
};

const CHANGE_LABELS: Record<string, string> = {
  improved_significantly: "Mejoró mucho",
  improved_slightly: "Mejoró algo",
  same: "Igual",
  worsened_slightly: "Empeoró algo",
  worsened_significantly: "Empeoró mucho",
  first_evaluation: "Primera evaluación",
};

const PRIORITY_STYLE: Record<string, string> = {
  high: "bg-rose-500/20 text-rose-450 border border-rose-500/30",
  medium: "bg-amber-500/20 text-amber-400 border border-amber-500/30",
  low: "bg-emerald-500/20 text-emerald-450 border border-emerald-500/30",
  closed: "bg-slate-800 text-slate-500 border border-slate-700",
};

const PRIORITY_LABELS: Record<string, string> = {
  high: "Alta",
  medium: "Media",
  low: "Baja",
  closed: "Cerrada",
};

function needLevelBadge(level?: number) {
  if (!level) return null;
  const color =
    level >= 4
      ? "bg-rose-500/20 text-rose-450 border-rose-500/30"
      : level === 3
      ? "bg-amber-500/20 text-amber-400 border-amber-500/30"
      : "bg-emerald-500/20 text-emerald-450 border-emerald-500/30";
  return (
    <span className={`inline-block text-[9px] font-black uppercase px-2 py-0.5 rounded-full border ${color}`}>
      Nivel {level}/5
    </span>
  );
}

export default function AdminFollowUps() {
  const [followUps, setFollowUps] = useState<FollowUp[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [search, setSearch] = useState("");
  const [priorityFilter, setPriorityFilter] = useState<string>("all");
  const [offset, setOffset] = useState(0);
  const limit = 50;

  useEffect(() => {
    fetchFollowUps();
  }, [priorityFilter, offset]);

  async function fetchFollowUps() {
    try {
      setLoading(true);
      let url = `/forms/follow-ups?limit=${limit}&offset=${offset}`;
      if (priorityFilter !== "all") {
        url += `&priority=${encodeURIComponent(priorityFilter)}`;
      }
      const res = await apiFetch(url);
      if (!res.ok) throw new Error("Error cargando seguimientos");
      const data = await res.json();
      setFollowUps(data.follow_ups || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setLoading(false);
    }
  }

  const displayed = followUps.filter((f) => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return (
      String(f.id).includes(q) ||
      String(f.participant_id ?? "").includes(q) ||
      (f.current_situation || "").toLowerCase().includes(q) ||
      (TYPE_LABELS[f.follow_up_type || ""] || "").toLowerCase().includes(q)
    );
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 text-[11px] font-semibold w-fit">
        <AlertTriangle className="w-3.5 h-3.5" />
        Modo solo lectura: el backend no expone PUT/DELETE para seguimientos (gap RF-G4)
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-450 text-xs font-semibold text-center">
          {error}
        </div>
      )}

      <div className="flex flex-col lg:flex-row gap-4 justify-between items-center bg-slate-900/50 p-4 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="relative w-full lg:w-96">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Buscar por participante, situación o ID..."
            className="w-full bg-slate-950 border border-slate-850 rounded-xl py-2.5 pl-10 pr-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-all"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <div className="flex flex-wrap gap-2 w-full lg:w-auto justify-end items-center">
          <div className="flex items-center bg-slate-950 border border-slate-850 rounded-xl px-3 py-1">
            <span className="text-xs text-slate-500 mr-2">Prioridad:</span>
            <select
              className="bg-transparent text-xs text-slate-300 focus:outline-none py-1 cursor-pointer font-medium"
              value={priorityFilter}
              onChange={(e) => {
                setPriorityFilter(e.target.value);
                setOffset(0);
              }}
            >
              <option value="all" className="bg-slate-950 text-slate-300">Todas</option>
              <option value="high" className="bg-slate-950 text-rose-450">Alta</option>
              <option value="medium" className="bg-slate-950 text-amber-400">Media</option>
              <option value="low" className="bg-slate-950 text-emerald-400">Baja</option>
              <option value="closed" className="bg-slate-950 text-slate-400">Cerrada</option>
            </select>
          </div>

          <div className="flex items-center gap-1.5">
            <button
              onClick={() => setOffset(Math.max(0, offset - limit))}
              disabled={offset === 0}
              className="px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs font-bold text-slate-300 hover:border-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            >
              Anterior
            </button>
            <button
              onClick={() => setOffset(offset + limit)}
              disabled={followUps.length < limit}
              className="px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs font-bold text-slate-300 hover:border-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            >
              Siguiente
            </button>
          </div>
        </div>
      </div>

      <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-800/40 text-slate-450 uppercase text-[10px] font-bold tracking-wider border-b border-slate-850">
              <tr>
                <th className="px-6 py-4">Fecha / Participante</th>
                <th className="px-6 py-4">Resultado</th>
                <th className="px-6 py-4">Situación</th>
                <th className="px-6 py-4">Nivel</th>
                <th className="px-6 py-4">Prioridad</th>
                <th className="px-6 py-4">Próximo Seguimiento</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-850">
              {loading ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-slate-500 font-medium">
                    Cargando seguimientos...
                  </td>
                </tr>
              ) : displayed.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-slate-500 font-medium">
                    No se encontraron seguimientos.
                  </td>
                </tr>
              ) : (
                displayed.map((f) => (
                  <tr key={f.id} className="hover:bg-slate-800/20 transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex flex-col">
                        <span className="text-xs text-slate-500 flex items-center gap-1">
                          <CalendarDays className="w-3 h-3 text-slate-600" />
                          {f.follow_up_date || "—"}
                        </span>
                        <span className="font-extrabold text-white text-sm mt-1 flex items-center gap-1">
                          <User className="w-3.5 h-3.5 text-emerald-500" />
                          Participante #{f.participant_id ?? "?"}
                        </span>
                        {f.related_interchange_id && (
                          <span className="text-[10px] text-slate-500">
                            Intercambio relacionado: #{f.related_interchange_id}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="space-y-1">
                        <span className="text-[10px] font-black uppercase px-2 py-0.5 rounded-full bg-slate-950 text-slate-400 border border-slate-800 w-fit">
                          {TYPE_LABELS[f.follow_up_type || ""] || f.follow_up_type || "—"}
                        </span>
                        {f.situation_change && (
                          <span className="block text-[10px] text-slate-500 flex items-center gap-1">
                            <ArrowRight className="w-3 h-3 text-slate-600" />
                            {CHANGE_LABELS[f.situation_change] || f.situation_change.replace(/_/g, " ")}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 max-w-sm">
                      <p className="text-xs text-slate-350 line-clamp-2">
                        {f.current_situation || "—"}
                      </p>
                      {f.new_needs_detected && f.new_needs_detected.length > 0 && (
                        <span className="inline-block mt-1 text-[8px] bg-rose-500/10 text-rose-450 border border-rose-500/20 px-1.5 py-0.5 rounded uppercase font-bold">
                          Nuevas necesidades detectadas
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4">{needLevelBadge(f.need_level)}</td>
                    <td className="px-6 py-4">
                      <span className={`inline-block text-[9px] font-black uppercase px-2 py-0.5 rounded-full ${
                        PRIORITY_STYLE[f.follow_up_priority || ""] || "bg-slate-800 text-slate-400"
                      }`}>
                        {PRIORITY_LABELS[f.follow_up_priority || ""] || f.follow_up_priority || "—"}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-xs text-slate-400 flex items-center gap-1">
                        <Flag className="w-3 h-3 text-slate-600" />
                        {f.next_follow_up_date || "—"}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
