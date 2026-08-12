"use client";

import React, { useEffect, useState } from "react";
import { apiFetch } from "../../lib/api";
import {
  Search,
  ClipboardList,
  CalendarDays,
  Flag,
  ArrowRight,
  User,
  Pencil,
  Trash2,
  X,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

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

  const [editing, setEditing] = useState<FollowUp | null>(null);
  const [form, setForm] = useState({
    follow_up_date: "",
    follow_up_type: "routine_check",
    current_situation: "",
    situation_change: "same",
    need_level: "",
    follow_up_priority: "low",
    next_follow_up_date: "",
  });
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState<FollowUp | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

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

  const openEdit = (f: FollowUp) => {
    setActionError(null);
    setForm({
      follow_up_date: f.follow_up_date || "",
      follow_up_type: f.follow_up_type || "routine_check",
      current_situation: f.current_situation || "",
      situation_change: f.situation_change || "same",
      need_level: f.need_level !== undefined && f.need_level !== null ? String(f.need_level) : "",
      follow_up_priority: f.follow_up_priority || "low",
      next_follow_up_date: f.next_follow_up_date || "",
    });
    setEditing(f);
  };

  const handleSaveEdit = async () => {
    if (!editing) return;
    setSaving(true);
    setActionError(null);
    try {
      const payload: Record<string, unknown> = {};
      if (form.follow_up_date.trim()) payload.follow_up_date = form.follow_up_date.trim();
      if (form.follow_up_type) payload.follow_up_type = form.follow_up_type;
      if (form.current_situation.trim()) payload.current_situation = form.current_situation.trim();
      if (form.situation_change) payload.situation_change = form.situation_change;
      if (form.need_level.trim() !== "") payload.need_level = parseInt(form.need_level, 10);
      if (form.follow_up_priority) payload.follow_up_priority = form.follow_up_priority;
      if (form.next_follow_up_date.trim())
        payload.next_follow_up_date = form.next_follow_up_date.trim();

      const res = await apiFetch(`/forms/follow-ups/${editing.id}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Error actualizando seguimiento");
      }
      setEditing(null);
      await fetchFollowUps();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!deleting) return;
    setDeleteLoading(true);
    setActionError(null);
    try {
      const res = await apiFetch(`/forms/follow-ups/${deleting.id}`, { method: "DELETE" });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Error eliminando seguimiento");
      }
      setDeleting(null);
      await fetchFollowUps();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setDeleteLoading(false);
    }
  };

  return (
    <div className="space-y-6">
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
                <th className="px-6 py-4 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-850">
              {loading ? (
                <tr>
                  <td colSpan={7} className="px-6 py-12 text-center text-slate-500 font-medium">
                    Cargando seguimientos...
                  </td>
                </tr>
              ) : displayed.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-6 py-12 text-center text-slate-500 font-medium">
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
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-1.5">
                        <button
                          onClick={() => openEdit(f)}
                          className="p-2 text-slate-400 hover:text-sky-400 hover:bg-sky-500/10 rounded-xl transition-all"
                          title="Editar seguimiento"
                        >
                          <Pencil className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => {
                            setActionError(null);
                            setDeleting(f);
                          }}
                          className="p-2 text-slate-400 hover:text-rose-450 hover:bg-rose-500/10 rounded-xl transition-all"
                          title="Eliminar seguimiento"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      <AnimatePresence>
        {editing && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setEditing(null)}
              className="absolute inset-0"
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="bg-slate-900 border border-slate-850 rounded-3xl w-full max-w-lg overflow-hidden shadow-2xl relative z-10 flex flex-col max-h-[90vh]"
            >
              <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-sky-500/0 via-sky-500 to-sky-500/0" />
              <div className="flex items-center justify-between p-6 border-b border-slate-850">
                <div>
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <ClipboardList className="w-5 h-5 text-sky-400" />
                    Editar seguimiento #{editing.id}
                  </h3>
                  <p className="text-xs text-slate-400 mt-1">
                    Participante #{editing.participant_id ?? "?"} · Los campos vacíos se conservan
                  </p>
                </div>
                <button
                  onClick={() => setEditing(null)}
                  className="p-2 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {actionError && (
                  <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-450 text-xs font-semibold">
                    {actionError}
                  </div>
                )}

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[10px] font-black uppercase tracking-wider text-slate-500 mb-1">
                      Fecha del seguimiento
                    </label>
                    <input
                      type="date"
                      value={form.follow_up_date}
                      onChange={(e) => setForm({ ...form, follow_up_date: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500 transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] font-black uppercase tracking-wider text-slate-500 mb-1">
                      Tipo
                    </label>
                    <select
                      value={form.follow_up_type}
                      onChange={(e) => setForm({ ...form, follow_up_type: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500 cursor-pointer"
                    >
                      {Object.entries(TYPE_LABELS).map(([value, label]) => (
                        <option key={value} value={value} className="bg-slate-950">{label}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-[10px] font-black uppercase tracking-wider text-slate-500 mb-1">
                    Situación actual
                  </label>
                  <textarea
                    value={form.current_situation}
                    onChange={(e) => setForm({ ...form, current_situation: e.target.value })}
                    rows={3}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-sky-500 transition-all resize-none"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[10px] font-black uppercase tracking-wider text-slate-500 mb-1">
                      Cambio de situación
                    </label>
                    <select
                      value={form.situation_change}
                      onChange={(e) => setForm({ ...form, situation_change: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500 cursor-pointer"
                    >
                      {Object.entries(CHANGE_LABELS).map(([value, label]) => (
                        <option key={value} value={value} className="bg-slate-950">{label}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-[10px] font-black uppercase tracking-wider text-slate-500 mb-1">
                      Nivel de necesidad (1-5)
                    </label>
                    <input
                      type="number"
                      min="1"
                      max="5"
                      value={form.need_level}
                      onChange={(e) => setForm({ ...form, need_level: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500 transition-all"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[10px] font-black uppercase tracking-wider text-slate-500 mb-1">
                      Prioridad
                    </label>
                    <select
                      value={form.follow_up_priority}
                      onChange={(e) => setForm({ ...form, follow_up_priority: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500 cursor-pointer"
                    >
                      {Object.entries(PRIORITY_LABELS).map(([value, label]) => (
                        <option key={value} value={value} className="bg-slate-950">{label}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-[10px] font-black uppercase tracking-wider text-slate-500 mb-1">
                      Próximo seguimiento
                    </label>
                    <input
                      type="date"
                      value={form.next_follow_up_date}
                      onChange={(e) => setForm({ ...form, next_follow_up_date: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500 transition-all"
                    />
                  </div>
                </div>
              </div>

              <div className="p-6 border-t border-slate-850 bg-slate-950/20 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setEditing(null)}
                  className="px-5 py-2.5 bg-slate-950 hover:bg-slate-900 border border-slate-800 rounded-xl text-slate-350 hover:text-white transition-all text-xs font-bold"
                >
                  Cancelar
                </button>
                <button
                  type="button"
                  onClick={handleSaveEdit}
                  disabled={saving}
                  className="px-5 py-2.5 bg-sky-500 hover:bg-sky-400 text-slate-950 rounded-xl text-xs font-bold transition-all hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {saving ? "Guardando..." : "Guardar cambios"}
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {deleting && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setDeleting(null)}
              className="absolute inset-0"
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="bg-slate-900 border border-slate-850 rounded-3xl w-full max-w-md overflow-hidden shadow-2xl relative z-10"
            >
              <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-rose-500/0 via-rose-500 to-rose-500/0" />
              <div className="p-6">
                {actionError && (
                  <div className="mb-4 p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-450 text-xs font-semibold">
                    {actionError}
                  </div>
                )}
                <div className="flex items-start gap-4">
                  <div className="p-3 rounded-2xl bg-rose-500/10 border border-rose-500/20">
                    <Trash2 className="w-6 h-6 text-rose-450" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-white">Eliminar seguimiento</h3>
                    <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                      ¿Seguro que quieres eliminar el seguimiento{" "}
                      <span className="text-white font-semibold">#{deleting.id}</span> del
                      participante <span className="text-white font-semibold">#{deleting.participant_id ?? "?"}</span>?
                      Esta acción no se puede deshacer.
                    </p>
                  </div>
                </div>
              </div>
              <div className="p-6 border-t border-slate-850 bg-slate-950/20 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setDeleting(null)}
                  className="px-5 py-2.5 bg-slate-950 hover:bg-slate-900 border border-slate-800 rounded-xl text-slate-350 hover:text-white transition-all text-xs font-bold"
                >
                  Cancelar
                </button>
                <button
                  type="button"
                  onClick={handleDelete}
                  disabled={deleteLoading}
                  className="px-5 py-2.5 bg-rose-500 hover:bg-rose-400 text-slate-950 rounded-xl text-xs font-bold transition-all hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {deleteLoading ? "Eliminando..." : "Eliminar"}
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
