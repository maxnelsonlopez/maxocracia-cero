"use client";

import React, { useEffect, useState } from "react";
import { apiFetch } from "../../lib/api";
import {
  Search,
  Repeat,
  Eye,
  X,
  Timer,
  Gauge,
  CalendarDays,
  Users,
  FileText,
  Pencil,
  Trash2,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface Interchange {
  id: number;
  interchange_id?: string;
  date?: string;
  giver_id?: number;
  receiver_id?: number;
  type?: string;
  description?: string;
  urgency?: string;
  uth_hours?: number;
  uvc_score?: number;
  urf_units?: number;
  urf_description?: string;
  economic_value_approx?: string;
  vhv_time_seconds?: number;
  vhv_lives?: number;
  vhv_resources_json?: string;
  impact_resolution_score?: number;
  reciprocity_status?: string;
  human_dimension_attended?: string;
  coordination_method?: string;
  requires_followup?: number;
  followup_scheduled_date?: string;
  facilitator_notes?: string;
  created_at?: string;
}

const URGENCY_STYLE: Record<string, string> = {
  Alta: "bg-rose-500/20 text-rose-450 border border-rose-500/30",
  Media: "bg-amber-500/20 text-amber-400 border border-amber-500/30",
  Baja: "bg-emerald-500/20 text-emerald-450 border border-emerald-500/30",
};

interface ExchangeForm {
  date: string;
  type: string;
  description: string;
  urgency: string;
  uth_hours: string;
  impact_resolution_score: string;
}

export default function AdminInterchanges() {
  const [interchanges, setInterchanges] = useState<Interchange[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [search, setSearch] = useState("");
  const [urgencyFilter, setUrgencyFilter] = useState<string>("all");
  const [offset, setOffset] = useState(0);
  const limit = 50;

  const [selected, setSelected] = useState<Interchange | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  const [editing, setEditing] = useState<Interchange | null>(null);
  const [form, setForm] = useState<ExchangeForm>({
    date: "",
    type: "",
    description: "",
    urgency: "Media",
    uth_hours: "",
    impact_resolution_score: "",
  });
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState<Interchange | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  useEffect(() => {
    fetchInterchanges();
  }, [urgencyFilter, offset]);

  async function fetchInterchanges() {
    try {
      setLoading(true);
      let url = `/forms/exchanges?limit=${limit}&offset=${offset}`;
      if (urgencyFilter !== "all") {
        url += `&urgency=${encodeURIComponent(urgencyFilter)}`;
      }
      const res = await apiFetch(url);
      if (!res.ok) throw new Error("Error cargando intercambios");
      const data = await res.json();
      setInterchanges(data.exchanges || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setLoading(false);
    }
  }

  const displayed = interchanges.filter((ex) => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return (
      String(ex.id).includes(q) ||
      (ex.interchange_id || "").toLowerCase().includes(q) ||
      (ex.description || "").toLowerCase().includes(q) ||
      (ex.type || "").toLowerCase().includes(q)
    );
  });

  const handleDetail = async (ex: Interchange) => {
    setSelected(ex);
    setDetailLoading(true);
    try {
      const res = await apiFetch(`/forms/exchanges/${ex.id}`);
      if (res.ok) {
        const data = await res.json();
        setSelected(data);
      }
    } catch {
      setDetailLoading(false);
      setSelected(ex);
      return;
    } finally {
      setDetailLoading(false);
    }
  };

  const openEdit = (ex: Interchange) => {
    setActionError(null);
    setForm({
      date: ex.date || "",
      type: ex.type || "",
      description: ex.description || "",
      urgency: ex.urgency || "Media",
      uth_hours: ex.uth_hours !== undefined && ex.uth_hours !== null ? String(ex.uth_hours) : "",
      impact_resolution_score:
        ex.impact_resolution_score !== undefined && ex.impact_resolution_score !== null
          ? String(ex.impact_resolution_score)
          : "",
    });
    setEditing(ex);
  };

  const handleSaveEdit = async () => {
    if (!editing) return;
    setSaving(true);
    setActionError(null);
    try {
      const payload: Record<string, unknown> = {};
      if (form.date.trim()) payload.date = form.date.trim();
      if (form.type.trim()) payload.type = form.type.trim();
      if (form.description.trim()) payload.description = form.description.trim();
      if (form.urgency) payload.urgency = form.urgency;
      if (form.uth_hours.trim() !== "") payload.uth_hours = parseFloat(form.uth_hours);
      if (form.impact_resolution_score.trim() !== "")
        payload.impact_resolution_score = parseInt(form.impact_resolution_score, 10);

      const res = await apiFetch(`/forms/exchanges/${editing.id}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Error actualizando intercambio");
      }
      setEditing(null);
      await fetchInterchanges();
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
      const res = await apiFetch(`/forms/exchanges/${deleting.id}`, { method: "DELETE" });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Error eliminando intercambio");
      }
      setDeleting(null);
      await fetchInterchanges();
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
            placeholder="Buscar por descripción, tipo o ID..."
            className="w-full bg-slate-950 border border-slate-850 rounded-xl py-2.5 pl-10 pr-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-all"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <div className="flex flex-wrap gap-2 w-full lg:w-auto justify-end items-center">
          <div className="flex items-center bg-slate-950 border border-slate-850 rounded-xl px-3 py-1">
            <span className="text-xs text-slate-500 mr-2">Urgencia:</span>
            <select
              className="bg-transparent text-xs text-slate-300 focus:outline-none py-1 cursor-pointer font-medium"
              value={urgencyFilter}
              onChange={(e) => {
                setUrgencyFilter(e.target.value);
                setOffset(0);
              }}
            >
              <option value="all" className="bg-slate-950 text-slate-300">Todas</option>
              <option value="Alta" className="bg-slate-950 text-rose-450">Alta</option>
              <option value="Media" className="bg-slate-950 text-amber-400">Media</option>
              <option value="Baja" className="bg-slate-950 text-emerald-400">Baja</option>
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
              disabled={interchanges.length < limit}
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
                <th className="px-6 py-4">Intercambio / Fecha</th>
                <th className="px-6 py-4">Partes</th>
                <th className="px-6 py-4">Descripción</th>
                <th className="px-6 py-4">Categoría</th>
                <th className="px-6 py-4">Horas UTH</th>
                <th className="px-6 py-4">Score Impacto</th>
                <th className="px-6 py-4">Estado</th>
                <th className="px-6 py-4 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-850">
              {loading ? (
                <tr>
                  <td colSpan={8} className="px-6 py-12 text-center text-slate-500 font-medium">
                    Cargando intercambios...
                  </td>
                </tr>
              ) : displayed.length === 0 ? (
                <tr>
                  <td colSpan={8} className="px-6 py-12 text-center text-slate-500 font-medium">
                    No se encontraron intercambios.
                  </td>
                </tr>
              ) : (
                displayed.map((ex) => (
                  <tr key={ex.id} className="hover:bg-slate-800/20 transition-colors group">
                    <td className="px-6 py-4">
                      <div className="flex flex-col">
                        <span className="font-extrabold text-white text-sm">
                          {ex.interchange_id || `#${ex.id}`}
                        </span>
                        <span className="text-[10px] text-slate-500 flex items-center gap-1 mt-1">
                          <CalendarDays className="w-3 h-3 text-slate-600" />
                          {ex.date || "—"}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-col gap-0.5 text-xs">
                        <span className="text-slate-300 flex items-center gap-1">
                          <Users className="w-3 h-3 text-emerald-500" />
                          Da: <span className="text-emerald-400 font-semibold">#{ex.giver_id ?? "?"}</span>
                        </span>
                        <span className="text-slate-300 flex items-center gap-1">
                          <Repeat className="w-3 h-3 text-amber-400" />
                          Recibe: <span className="text-amber-400 font-semibold">#{ex.receiver_id ?? "?"}</span>
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 max-w-xs">
                      <div className="space-y-1">
                        <span className="text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-slate-950 text-slate-500 border border-slate-900 w-fit">
                          {ex.type || "intercambio"}
                        </span>
                        <p className="text-xs text-slate-350 line-clamp-2">
                          {(ex.description || "").slice(0, 120) || "—"}
                        </p>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-[10px] bg-slate-950 text-slate-500 border border-slate-900 px-2 py-0.5 rounded">
                        {(ex.human_dimension_attended || "—").replace(/_/g, " ")}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-xs font-bold text-white flex items-center gap-1">
                        <Timer className="w-3.5 h-3.5 text-emerald-400" />
                        {ex.uth_hours ?? 0} h
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-xs font-bold text-white flex items-center gap-1">
                        <Gauge className="w-3.5 h-3.5 text-sky-400" />
                        {ex.impact_resolution_score ?? 0}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="space-y-1">
                        <span className="text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-slate-950 text-slate-400 border border-slate-800">
                          {ex.reciprocity_status || "sin estado"}
                        </span>
                        {ex.requires_followup === 1 && (
                          <span className="block text-[8px] font-black uppercase px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 w-fit">
                            Requiere seguimiento
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={() => handleDetail(ex)}
                          className="p-2 text-slate-400 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-xl transition-all"
                          title="Ver detalle del intercambio"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => openEdit(ex)}
                          className="p-2 text-slate-400 hover:text-sky-400 hover:bg-sky-500/10 rounded-xl transition-all"
                          title="Editar intercambio"
                        >
                          <Pencil className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => {
                            setActionError(null);
                            setDeleting(ex);
                          }}
                          className="p-2 text-slate-400 hover:text-rose-450 hover:bg-rose-500/10 rounded-xl transition-all"
                          title="Eliminar intercambio"
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
        {selected && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelected(null)}
              className="absolute inset-0"
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="bg-slate-900 border border-slate-850 rounded-3xl w-full max-w-2xl overflow-hidden shadow-2xl relative z-10 flex flex-col max-h-[90vh]"
            >
              <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-emerald-500/0 via-emerald-500 to-emerald-500/0" />
              <div className="flex items-center justify-between p-6 border-b border-slate-850">
                <div>
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <Repeat className="w-5 h-5 text-emerald-400" />
                    Intercambio {selected.interchange_id || `#${selected.id}`}
                  </h3>
                  <p className="text-xs text-slate-400 mt-1">
                    Registrado el {selected.created_at || selected.date || "—"}
                  </p>
                </div>
                <button
                  onClick={() => setSelected(null)}
                  className="p-2 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {detailLoading ? (
                  <div className="py-10 text-center text-slate-500 text-xs font-medium">
                    Cargando detalle completo...
                  </div>
                ) : (
                  <>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                      <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                        <p className="text-[9px] font-black uppercase tracking-wider text-slate-500">Fecha</p>
                        <p className="text-sm font-bold text-white mt-1">{selected.date || "—"}</p>
                      </div>
                      <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                        <p className="text-[9px] font-black uppercase tracking-wider text-slate-500">Tipo</p>
                        <p className="text-sm font-bold text-white mt-1">{selected.type || "—"}</p>
                      </div>
                      <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                        <p className="text-[9px] font-black uppercase tracking-wider text-slate-500">Urgencia</p>
                        <span className={`inline-block mt-1 text-[10px] font-black uppercase px-2 py-0.5 rounded-full ${
                          URGENCY_STYLE[selected.urgency || ""] || "bg-slate-800 text-slate-400"
                        }`}>
                          {selected.urgency || "—"}
                        </span>
                      </div>
                      <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                        <p className="text-[9px] font-black uppercase tracking-wider text-slate-500">Giver</p>
                        <p className="text-sm font-bold text-emerald-400 mt-1">#{selected.giver_id ?? "?"}</p>
                      </div>
                      <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                        <p className="text-[9px] font-black uppercase tracking-wider text-slate-500">Receiver</p>
                        <p className="text-sm font-bold text-amber-400 mt-1">#{selected.receiver_id ?? "?"}</p>
                      </div>
                      <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                        <p className="text-[9px] font-black uppercase tracking-wider text-slate-500">Estado</p>
                        <p className="text-sm font-bold text-white mt-1">{selected.reciprocity_status || "—"}</p>
                      </div>
                      <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                        <p className="text-[9px] font-black uppercase tracking-wider text-slate-500">Horas UTH</p>
                        <p className="text-sm font-bold text-white mt-1">{selected.uth_hours ?? 0}</p>
                      </div>
                      <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                        <p className="text-[9px] font-black uppercase tracking-wider text-slate-500">Score Impacto</p>
                        <p className="text-sm font-bold text-white mt-1">{selected.impact_resolution_score ?? 0}</p>
                      </div>
                      <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                        <p className="text-[9px] font-black uppercase tracking-wider text-slate-500">UVC / URF</p>
                        <p className="text-sm font-bold text-white mt-1">
                          {selected.uvc_score ?? 0} / {selected.urf_units ?? 0}
                        </p>
                      </div>
                    </div>

                    <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                      <p className="text-[9px] font-black uppercase tracking-wider text-slate-500 flex items-center gap-1">
                        <FileText className="w-3 h-3" /> Descripción
                      </p>
                      <p className="text-sm text-slate-300 mt-2 leading-relaxed">
                        {selected.description || "Sin descripción"}
                      </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                        <p className="text-[9px] font-black uppercase tracking-wider text-slate-500">
                          Dimensión Humana Atendida
                        </p>
                        <p className="text-sm text-slate-300 mt-1">
                          {(selected.human_dimension_attended || "—").replace(/_/g, " ")}
                        </p>
                      </div>
                      <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                        <p className="text-[9px] font-black uppercase tracking-wider text-slate-500">
                          Coordinación
                        </p>
                        <p className="text-sm text-slate-300 mt-1">
                          {(selected.coordination_method || "—").replace(/_/g, " ")}
                        </p>
                      </div>
                      <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                        <p className="text-[9px] font-black uppercase tracking-wider text-slate-500">
                          Valor Económico Aprox.
                        </p>
                        <p className="text-sm text-slate-300 mt-1">{selected.economic_value_approx || "—"}</p>
                      </div>
                      <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                        <p className="text-[9px] font-black uppercase tracking-wider text-slate-500">
                          Requiere Seguimiento
                        </p>
                        <p className="text-sm text-slate-300 mt-1">
                          {selected.requires_followup === 1
                            ? `Sí (${selected.followup_scheduled_date || "sin fecha"})`
                            : "No"}
                        </p>
                      </div>
                    </div>

                    {selected.facilitator_notes && (
                      <div className="p-4 rounded-xl bg-amber-500/5 border border-amber-500/20">
                        <p className="text-[9px] font-black uppercase tracking-wider text-amber-400">
                          Notas del Facilitador
                        </p>
                        <p className="text-sm text-slate-300 mt-2 leading-relaxed">{selected.facilitator_notes}</p>
                      </div>
                    )}
                  </>
                )}
              </div>

              <div className="p-6 border-t border-slate-850 bg-slate-950/20 flex justify-end">
                <button
                  type="button"
                  onClick={() => setSelected(null)}
                  className="px-5 py-2.5 bg-slate-950 hover:bg-slate-900 border border-slate-800 rounded-xl text-slate-350 hover:text-white transition-all text-xs font-bold"
                >
                  Cerrar
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

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
                    <Pencil className="w-5 h-5 text-sky-400" />
                    Editar intercambio {editing.interchange_id || `#${editing.id}`}
                  </h3>
                  <p className="text-xs text-slate-400 mt-1">
                    Los campos vacíos se conservan sin cambios
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
                      Fecha
                    </label>
                    <input
                      type="date"
                      value={form.date}
                      onChange={(e) => setForm({ ...form, date: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500 transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] font-black uppercase tracking-wider text-slate-500 mb-1">
                      Tipo
                    </label>
                    <input
                      type="text"
                      value={form.type}
                      onChange={(e) => setForm({ ...form, type: e.target.value })}
                      placeholder="UTH, alimento..."
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-sky-500 transition-all"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-[10px] font-black uppercase tracking-wider text-slate-500 mb-1">
                    Descripción
                  </label>
                  <textarea
                    value={form.description}
                    onChange={(e) => setForm({ ...form, description: e.target.value })}
                    rows={3}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-sky-500 transition-all resize-none"
                  />
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-[10px] font-black uppercase tracking-wider text-slate-500 mb-1">
                      Urgencia
                    </label>
                    <select
                      value={form.urgency}
                      onChange={(e) => setForm({ ...form, urgency: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500 cursor-pointer"
                    >
                      <option value="Alta" className="bg-slate-950">Alta</option>
                      <option value="Media" className="bg-slate-950">Media</option>
                      <option value="Baja" className="bg-slate-950">Baja</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[10px] font-black uppercase tracking-wider text-slate-500 mb-1">
                      Horas UTH
                    </label>
                    <input
                      type="number"
                      min="0"
                      step="0.5"
                      value={form.uth_hours}
                      onChange={(e) => setForm({ ...form, uth_hours: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500 transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] font-black uppercase tracking-wider text-slate-500 mb-1">
                      Score Impacto
                    </label>
                    <input
                      type="number"
                      min="0"
                      step="1"
                      value={form.impact_resolution_score}
                      onChange={(e) =>
                        setForm({ ...form, impact_resolution_score: e.target.value })
                      }
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
                    <h3 className="text-lg font-bold text-white">Eliminar intercambio</h3>
                    <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                      ¿Seguro que quieres eliminar el intercambio{" "}
                      <span className="text-white font-semibold">
                        {deleting.interchange_id || `#${deleting.id}`}
                      </span>
                      ? Esta acción no se puede deshacer.
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
