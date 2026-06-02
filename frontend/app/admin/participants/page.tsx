"use client";

import React, { useEffect, useState } from "react";
import { apiFetch } from "../../lib/api";
import {
  Search,
  Filter,
  CheckCircle2,
  XCircle,
  Clock,
  Edit,
  Trash2,
  MapPin,
  AlertTriangle,
  Heart,
  Plus,
  X
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface Participant {
  id: number;
  name: string;
  email: string;
  city: string;
  neighborhood: string;
  phone_call?: string;
  phone_whatsapp?: string;
  telegram_handle?: string;
  referred_by?: string;
  personal_values?: string;
  offer_description: string;
  need_description: string;
  need_urgency: string;
  offer_categories: string[];
  need_categories: string[];
  offer_human_dimensions: string[];
  need_human_dimensions: string[];
  status: "active" | "paused" | "inactive";
  consent_given?: boolean;
}

const CATEGORY_OPTIONS = [
  { value: "objeto", label: "Objeto físico" },
  { value: "alimentacion", label: "Alimentación" },
  { value: "habilidad", label: "Habilidad" },
  { value: "conocimiento", label: "Conocimiento" },
  { value: "transporte", label: "Transporte" },
  { value: "tiempo", label: "Tiempo / Apoyo" },
  { value: "espacio", label: "Espacio" },
  { value: "apoyo_economico", label: "Apoyo económico" }
];

const DIMENSION_OPTIONS = [
  { value: "crecimiento_aprendizaje", label: "Crecimiento y Aprendizaje" },
  { value: "bienestar_descanso", label: "Bienestar y Descanso" },
  { value: "seguridad_estabilidad", label: "Seguridad y Estabilidad" },
  { value: "autoestima_autonomia", label: "Autoestima y Autonomía" },
  { value: "conexion_social", label: "Conexión Social" },
  { value: "prosperidad_recursos", label: "Prosperidad y Recursos" },
  { value: "placer_goce", label: "Placer y Goce" },
  { value: "intimidad_vinculos", label: "Intimidad y Vínculos" }
];

const CATEGORY_LABELS: Record<string, string> = {
  objeto: "Objeto físico",
  alimentacion: "Alimentación",
  habilidad: "Habilidad",
  conocimiento: "Conocimiento",
  transporte: "Transporte",
  tiempo: "Tiempo / Apoyo",
  espacio: "Espacio",
  apoyo_economico: "Apoyo económico",
};

const categoryLabel = (c: string) => CATEGORY_LABELS[c] || c.replace(/_/g, " ");

export default function AdminParticipants() {
  const [participants, setParticipants] = useState<Participant[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Search & Filter State
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [urgencyFilter, setUrgencyFilter] = useState<string>("all");
  const [limit, setLimit] = useState(50);
  const [offset, setOffset] = useState(0);

  // Edit modal state
  const [selectedParticipant, setSelectedParticipant] = useState<Participant | null>(null);
  const [activeTab, setActiveTab] = useState<"contact" | "needs" | "offers">("contact");
  const [saving, setSaving] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);
  const [modalSuccess, setModalSuccess] = useState(false);

  // Delete confirmation state
  const [participantToDelete, setParticipantToDelete] = useState<Participant | null>(null);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    fetchParticipants();
  }, [search, statusFilter, limit, offset]);

  async function fetchParticipants() {
    try {
      setLoading(true);
      let url = `/forms/participants?limit=${limit}&offset=${offset}`;
      if (statusFilter !== "all") {
        url += `&status=${statusFilter}`;
      }
      if (search.trim()) {
        url += `&search=${encodeURIComponent(search)}`;
      }
      const res = await apiFetch(url);
      if (!res.ok) throw new Error("Error cargando participantes de la red");
      const data = await res.json();
      setParticipants(data.participants || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setLoading(false);
    }
  }

  const handleEditClick = (p: Participant) => {
    setSelectedParticipant({
      ...p,
      phone_call: p.phone_call || "",
      phone_whatsapp: p.phone_whatsapp || "",
      telegram_handle: p.telegram_handle || "",
      personal_values: p.personal_values || "",
      offer_categories: p.offer_categories || [],
      need_categories: p.need_categories || [],
      offer_human_dimensions: p.offer_human_dimensions || [],
      need_human_dimensions: p.need_human_dimensions || []
    });
    setActiveTab("contact");
    setModalError(null);
    setModalSuccess(false);
  };

  const handleSaveParticipant = async () => {
    if (!selectedParticipant) return;
    setSaving(true);
    setModalError(null);

    // Basic Validation
    if (
      !selectedParticipant.name ||
      !selectedParticipant.email ||
      !selectedParticipant.city ||
      !selectedParticipant.neighborhood ||
      !selectedParticipant.need_description ||
      !selectedParticipant.offer_description
    ) {
      setModalError("Por favor completa todos los campos requeridos (*)");
      setSaving(false);
      return;
    }

    try {
      const res = await apiFetch(`/forms/participants/${selectedParticipant.id}`, {
        method: "PUT",
        body: JSON.stringify(selectedParticipant)
      });

      if (res.ok) {
        setModalSuccess(true);
        await fetchParticipants();
        setTimeout(() => {
          setSelectedParticipant(null);
          setModalSuccess(false);
        }, 1500);
      } else {
        const errData = await res.json();
        setModalError(errData.error || "Error al actualizar participante");
      }
    } catch (err) {
      console.error(err);
      setModalError("Error de red al actualizar participante");
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteClick = (p: Participant) => {
    setParticipantToDelete(p);
  };

  const confirmDeleteParticipant = async () => {
    if (!participantToDelete) return;
    setDeleting(true);
    try {
      const res = await apiFetch(`/forms/participants/${participantToDelete.id}`, {
        method: "DELETE"
      });

      if (res.ok) {
        setParticipantToDelete(null);
        await fetchParticipants();
      } else {
        const errData = await res.json();
        alert(errData.error || "No se pudo eliminar al participante");
      }
    } catch (err) {
      console.error(err);
      alert("Error de red al intentar eliminar");
    } finally {
      setDeleting(false);
    }
  };

  // Filter participants further in frontend if needed (e.g. urgency filter)
  const displayedParticipants = participants.filter(p => {
    if (urgencyFilter !== "all" && p.need_urgency !== urgencyFilter) {
      return false;
    }
    return true;
  });

  return (
    <div className="space-y-6">
      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-450 text-xs font-semibold text-center">
          ⚠️ {error}
        </div>
      )}

      {/* Header Actions */}
      <div className="flex flex-col lg:flex-row gap-4 justify-between items-center bg-slate-900/50 p-4 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="relative w-full lg:w-96">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Buscar por nombre, email o barrio..."
            className="w-full bg-slate-950 border border-slate-850 rounded-xl py-2.5 pl-10 pr-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-all"
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setOffset(0);
            }}
          />
        </div>
        
        <div className="flex flex-wrap gap-2 w-full lg:w-auto justify-end">
          {/* Status Filter */}
          <div className="flex items-center bg-slate-950 border border-slate-850 rounded-xl px-3 py-1">
            <span className="text-xs text-slate-500 mr-2">Estado:</span>
            <select
              className="bg-transparent text-xs text-slate-300 focus:outline-none py-1 cursor-pointer font-medium"
              value={statusFilter}
              onChange={(e) => {
                setStatusFilter(e.target.value);
                setOffset(0);
              }}
            >
              <option value="all" className="bg-slate-950 text-slate-300">Todos</option>
              <option value="active" className="bg-slate-950 text-slate-300">Activo</option>
              <option value="paused" className="bg-slate-950 text-slate-300">Pausado</option>
              <option value="inactive" className="bg-slate-950 text-slate-300">Inactivo</option>
            </select>
          </div>

          {/* Urgency Filter */}
          <div className="flex items-center bg-slate-950 border border-slate-850 rounded-xl px-3 py-1">
            <span className="text-xs text-slate-500 mr-2">Urgencia:</span>
            <select
              className="bg-transparent text-xs text-slate-300 focus:outline-none py-1 cursor-pointer font-medium"
              value={urgencyFilter}
              onChange={(e) => {
                setUrgencyFilter(e.target.value);
              }}
            >
              <option value="all" className="bg-slate-950 text-slate-300">Todos</option>
              <option value="Alta" className="bg-slate-950 text-rose-450">Alta</option>
              <option value="Media" className="bg-slate-950 text-amber-400">Media</option>
              <option value="Baja" className="bg-slate-950 text-emerald-400">Baja</option>
            </select>
          </div>

          {/* Register Button */}
          <a
            href="/forms/cero"
            className="flex items-center gap-2 px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 rounded-xl text-xs font-bold transition-all hover:scale-[1.02]"
          >
            <Plus className="w-4 h-4" />
            Registrar Participante
          </a>
        </div>
      </div>

      {/* Participants Table */}
      <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-800/40 text-slate-450 uppercase text-[10px] font-bold tracking-wider border-b border-slate-850">
              <tr>
                <th className="px-6 py-4">Participante / Ubicación</th>
                <th className="px-6 py-4">Necesidad / Urgencia</th>
                <th className="px-6 py-4">Oferta Comunidad</th>
                <th className="px-6 py-4">Estado</th>
                <th className="px-6 py-4 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-850">
              {loading ? (
                <tr>
                  <td colSpan={5} className="px-6 py-12 text-center text-slate-500 font-medium">
                    Cargando red de apoyo...
                  </td>
                </tr>
              ) : displayedParticipants.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-12 text-center text-slate-500 font-medium">
                    No se encontraron participantes.
                  </td>
                </tr>
              ) : (
                displayedParticipants.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-800/20 transition-colors group">
                    <td className="px-6 py-4">
                      <div className="flex flex-col">
                        <span className="font-extrabold text-white text-sm">{p.name}</span>
                        <span className="text-xs text-slate-450">{p.email}</span>
                        <span className="text-[10px] text-slate-500 flex items-center gap-1 mt-1">
                          <MapPin className="w-3 h-3 text-slate-600" />
                          {p.neighborhood}, {p.city}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="space-y-1 max-w-xs">
                        <div className="flex items-center gap-2">
                          <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded-full ${
                            p.need_urgency === "Alta" ? "bg-rose-500/20 text-rose-450 border border-rose-500/30" :
                            p.need_urgency === "Media" ? "bg-amber-500/20 text-amber-400 border border-amber-500/30" :
                            "bg-emerald-500/20 text-emerald-450 border border-emerald-500/30"
                          }`}>
                            {p.need_urgency}
                          </span>
                        </div>
                        <p className="text-xs text-slate-350 line-clamp-2">"{p.need_description}"</p>
                        <div className="flex flex-wrap gap-1">
                          {p.need_categories?.map((cat, i) => (
                            <span key={i} className="text-[8px] bg-slate-950 text-slate-500 border border-slate-900 px-1 py-0.5 rounded">
                              {categoryLabel(cat)}
                            </span>
                          ))}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="space-y-1 max-w-xs">
                        <p className="text-xs text-slate-350 line-clamp-2">"{p.offer_description}"</p>
                        <div className="flex flex-wrap gap-1">
                          {p.offer_categories?.map((cat, i) => (
                            <span key={i} className="text-[8px] bg-slate-950 text-slate-500 border border-slate-900 px-1 py-0.5 rounded">
                              {categoryLabel(cat)}
                            </span>
                          ))}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      {p.status === "active" ? (
                        <span className="flex items-center gap-1.5 w-fit text-[10px] font-black uppercase py-0.5 px-2.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                          <CheckCircle2 className="w-3 h-3" /> Activo
                        </span>
                      ) : p.status === "paused" ? (
                        <span className="flex items-center gap-1.5 w-fit text-[10px] font-black uppercase py-0.5 px-2.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">
                          <Clock className="w-3 h-3" /> Pausado
                        </span>
                      ) : (
                        <span className="flex items-center gap-1.5 w-fit text-[10px] font-black uppercase py-0.5 px-2.5 rounded-full bg-slate-800 text-slate-500 border border-slate-700">
                          <XCircle className="w-3 h-3" /> Inactivo
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={() => handleEditClick(p)}
                          className="p-2 text-slate-400 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-xl transition-all"
                          title="Editar Participante"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDeleteClick(p)}
                          className="p-2 text-slate-400 hover:text-rose-500 hover:bg-rose-500/10 rounded-xl transition-all"
                          title="Eliminar Participante"
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

      {/* Admin Edit Modal */}
      <AnimatePresence>
        {selectedParticipant && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedParticipant(null)}
              className="absolute inset-0"
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="bg-slate-900 border border-slate-850 rounded-3xl w-full max-w-3xl overflow-hidden shadow-2xl relative z-10 flex flex-col max-h-[90vh]"
            >
              <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-emerald-500/0 via-emerald-500 to-emerald-500/0" />
              
              {/* Modal Header */}
              <div className="flex items-center justify-between p-6 border-b border-slate-850">
                <div>
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <Edit className="w-5 h-5 text-emerald-400" />
                    Editar Ficha de Participante (Admin)
                  </h3>
                  <p className="text-xs text-slate-400 mt-1">
                    Control administrativo completo del participante #{selectedParticipant.id}
                  </p>
                </div>
                <button
                  onClick={() => setSelectedParticipant(null)}
                  className="p-2 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Tabs Navigation */}
              <div className="flex border-b border-slate-850 bg-slate-950/20 px-6">
                {(["contact", "needs", "offers"] as const).map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`py-3 px-4 text-xs font-bold uppercase tracking-wider border-b-2 transition-all relative ${
                      activeTab === tab
                        ? "border-emerald-500 text-emerald-400"
                        : "border-transparent text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    {tab === "contact" && "Contacto e Identidad"}
                    {tab === "needs" && "Necesidades"}
                    {tab === "offers" && "Ofertas"}
                  </button>
                ))}
              </div>

              {/* Modal Body */}
              <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {modalError && (
                  <div className="p-4 bg-rose-500/10 border border-rose-500/20 rounded-xl text-rose-450 text-xs font-medium flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 shrink-0" />
                    {modalError}
                  </div>
                )}

                {modalSuccess && (
                  <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400 text-xs font-medium flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 shrink-0" />
                    ¡Participante actualizado exitosamente!
                  </div>
                )}

                {activeTab === "contact" && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Nombre Completo *</label>
                      <input
                        type="text"
                        value={selectedParticipant.name || ""}
                        onChange={(e) => setSelectedParticipant({ ...selectedParticipant, name: e.target.value })}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Correo Electrónico *</label>
                      <input
                        type="email"
                        value={selectedParticipant.email || ""}
                        onChange={(e) => setSelectedParticipant({ ...selectedParticipant, email: e.target.value })}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Teléfono de Llamadas</label>
                      <input
                        type="text"
                        value={selectedParticipant.phone_call || ""}
                        onChange={(e) => setSelectedParticipant({ ...selectedParticipant, phone_call: e.target.value })}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">WhatsApp</label>
                      <input
                        type="text"
                        value={selectedParticipant.phone_whatsapp || ""}
                        onChange={(e) => setSelectedParticipant({ ...selectedParticipant, phone_whatsapp: e.target.value })}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Telegram</label>
                      <input
                        type="text"
                        value={selectedParticipant.telegram_handle || ""}
                        onChange={(e) => setSelectedParticipant({ ...selectedParticipant, telegram_handle: e.target.value })}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Referido Por</label>
                      <input
                        type="text"
                        value={selectedParticipant.referred_by || ""}
                        onChange={(e) => setSelectedParticipant({ ...selectedParticipant, referred_by: e.target.value })}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Ciudad *</label>
                      <input
                        type="text"
                        value={selectedParticipant.city || ""}
                        onChange={(e) => setSelectedParticipant({ ...selectedParticipant, city: e.target.value })}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Barrio / Sector *</label>
                      <input
                        type="text"
                        value={selectedParticipant.neighborhood || ""}
                        onChange={(e) => setSelectedParticipant({ ...selectedParticipant, neighborhood: e.target.value })}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Estado en la Red</label>
                      <select
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors"
                        value={selectedParticipant.status}
                        onChange={(e) => setSelectedParticipant({ ...selectedParticipant, status: e.target.value as any })}
                      >
                        <option value="active">Activo</option>
                        <option value="paused">Pausado</option>
                        <option value="inactive">Inactivo</option>
                      </select>
                    </div>
                    <div className="space-y-1.5 flex items-center pt-6">
                      <label className="flex items-center gap-2 cursor-pointer text-xs font-bold text-slate-400 uppercase tracking-wider">
                        <input
                          type="checkbox"
                          checked={selectedParticipant.consent_given || false}
                          onChange={(e) => setSelectedParticipant({ ...selectedParticipant, consent_given: e.target.checked })}
                          className="w-4 h-4 rounded border-slate-850 bg-slate-950 text-emerald-500 focus:ring-emerald-500/50"
                        />
                        Consentimiento Informado
                      </label>
                    </div>
                    <div className="space-y-1.5 md:col-span-2">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Valores Clave</label>
                      <textarea
                        rows={2}
                        value={selectedParticipant.personal_values || ""}
                        onChange={(e) => setSelectedParticipant({ ...selectedParticipant, personal_values: e.target.value })}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors resize-none"
                      />
                    </div>
                  </div>
                )}

                {activeTab === "needs" && (
                  <div className="space-y-5">
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Nivel de Urgencia</label>
                      <div className="grid grid-cols-3 gap-3">
                        {(["Baja", "Media", "Alta"] as const).map((urgency) => (
                          <button
                            key={urgency}
                            type="button"
                            onClick={() => setSelectedParticipant({ ...selectedParticipant, need_urgency: urgency })}
                            className={`py-3 px-4 rounded-xl border text-sm font-bold uppercase transition-all flex items-center justify-center gap-2 ${
                              selectedParticipant.need_urgency === urgency
                                ? urgency === "Alta"
                                  ? "bg-rose-500/20 border-rose-500 text-rose-450"
                                  : urgency === "Media"
                                  ? "bg-amber-500/20 border-amber-500 text-amber-400"
                                  : "bg-emerald-500/20 border-emerald-500 text-emerald-400"
                                : "bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700"
                            }`}
                          >
                            <span className={`w-2 h-2 rounded-full ${
                              urgency === "Alta" ? "bg-rose-500" : urgency === "Media" ? "bg-amber-500" : "bg-emerald-500"
                            }`} />
                            {urgency}
                          </button>
                        ))}
                      </div>
                    </div>

                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Descripción de Necesidad *</label>
                      <textarea
                        rows={3}
                        value={selectedParticipant.need_description || ""}
                        onChange={(e) => setSelectedParticipant({ ...selectedParticipant, need_description: e.target.value })}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors resize-none"
                      />
                    </div>

                    <div className="space-y-2">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider block">Categorías de Necesidad</label>
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                        {CATEGORY_OPTIONS.map((opt) => {
                          const isChecked = selectedParticipant.need_categories?.includes(opt.value);
                          return (
                            <button
                              key={opt.value}
                              type="button"
                              onClick={() => {
                                const cats = selectedParticipant.need_categories || [];
                                const nextCats = isChecked
                                  ? cats.filter((c) => c !== opt.value)
                                  : [...cats, opt.value];
                                setSelectedParticipant({ ...selectedParticipant, need_categories: nextCats });
                              }}
                              className={`p-2.5 rounded-xl border text-xs font-medium text-left transition-all ${
                                isChecked
                                  ? "bg-emerald-500/10 border-emerald-500/40 text-emerald-400"
                                  : "bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700"
                              }`}
                            >
                              {opt.label}
                            </button>
                          );
                        })}
                      </div>
                    </div>

                    <div className="space-y-2">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider block">Dimensiones de la Dignidad Humana (SDV) Impactadas</label>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {DIMENSION_OPTIONS.map((opt) => {
                          const isChecked = selectedParticipant.need_human_dimensions?.includes(opt.value);
                          return (
                            <button
                              key={opt.value}
                              type="button"
                              onClick={() => {
                                const dims = selectedParticipant.need_human_dimensions || [];
                                const nextDims = isChecked
                                  ? dims.filter((d) => d !== opt.value)
                                  : [...dims, opt.value];
                                setSelectedParticipant({ ...selectedParticipant, need_human_dimensions: nextDims });
                              }}
                              className={`p-3 rounded-xl border text-xs font-medium text-left transition-all flex items-center justify-between ${
                                isChecked
                                  ? "bg-emerald-500/10 border-emerald-500/40 text-emerald-400"
                                  : "bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700"
                              }`}
                            >
                              <span>{opt.label}</span>
                              {isChecked && <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />}
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === "offers" && (
                  <div className="space-y-5">
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Descripción de Oferta *</label>
                      <textarea
                        rows={3}
                        value={selectedParticipant.offer_description || ""}
                        onChange={(e) => setSelectedParticipant({ ...selectedParticipant, offer_description: e.target.value })}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors resize-none"
                      />
                    </div>

                    <div className="space-y-2">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider block">Categorías de Oferta</label>
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                        {CATEGORY_OPTIONS.map((opt) => {
                          const isChecked = selectedParticipant.offer_categories?.includes(opt.value);
                          return (
                            <button
                              key={opt.value}
                              type="button"
                              onClick={() => {
                                const cats = selectedParticipant.offer_categories || [];
                                const nextCats = isChecked
                                  ? cats.filter((c) => c !== opt.value)
                                  : [...cats, opt.value];
                                setSelectedParticipant({ ...selectedParticipant, offer_categories: nextCats });
                              }}
                              className={`p-2.5 rounded-xl border text-xs font-medium text-left transition-all ${
                                isChecked
                                  ? "bg-emerald-500/10 border-emerald-500/40 text-emerald-400"
                                  : "bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700"
                              }`}
                            >
                              {opt.label}
                            </button>
                          );
                        })}
                      </div>
                    </div>

                    <div className="space-y-2">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider block">Dimensiones de la Dignidad Humana (SDV) Vinculadas</label>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {DIMENSION_OPTIONS.map((opt) => {
                          const isChecked = selectedParticipant.offer_human_dimensions?.includes(opt.value);
                          return (
                            <button
                              key={opt.value}
                              type="button"
                              onClick={() => {
                                const dims = selectedParticipant.offer_human_dimensions || [];
                                const nextDims = isChecked
                                  ? dims.filter((d) => d !== opt.value)
                                  : [...dims, opt.value];
                                setSelectedParticipant({ ...selectedParticipant, offer_human_dimensions: nextDims });
                              }}
                              className={`p-3 rounded-xl border text-xs font-medium text-left transition-all flex items-center justify-between ${
                                isChecked
                                  ? "bg-emerald-500/10 border-emerald-500/40 text-emerald-400"
                                  : "bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700"
                              }`}
                            >
                              <span>{opt.label}</span>
                              {isChecked && <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />}
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Modal Footer */}
              <div className="p-6 border-t border-slate-850 bg-slate-950/20 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setSelectedParticipant(null)}
                  className="px-5 py-2.5 bg-slate-950 hover:bg-slate-900 border border-slate-800 rounded-xl text-slate-350 hover:text-white transition-all text-xs font-bold"
                >
                  Cancelar
                </button>
                <button
                  type="button"
                  onClick={handleSaveParticipant}
                  disabled={saving}
                  className="px-6 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 rounded-xl font-bold transition-all text-xs active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  {saving ? (
                    <>
                      <div className="w-3.5 h-3.5 border-2 border-slate-950/20 border-t-slate-950 rounded-full animate-spin" />
                      Guardando...
                    </>
                  ) : (
                    "Guardar Cambios"
                  )}
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* Delete Confirmation Modal */}
      <AnimatePresence>
        {participantToDelete && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setParticipantToDelete(null)}
              className="absolute inset-0"
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-slate-900 border border-rose-500/30 rounded-3xl w-full max-w-md p-6 relative z-10 space-y-4 shadow-2xl"
            >
              <div className="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-500">
                <AlertTriangle className="w-6 h-6 animate-pulse" />
              </div>
              <div>
                <h4 className="text-lg font-bold text-white">¿Eliminar Participante?</h4>
                <p className="text-sm text-slate-400 mt-2 leading-relaxed">
                  ¿Estás seguro de que deseas eliminar permanentemente a <span className="text-white font-semibold">{participantToDelete.name}</span> de la Red de Apoyo? 
                  Esta acción es irreversible y eliminará todos sus registros de seguimiento en cascada.
                </p>
              </div>
              <div className="flex items-center gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setParticipantToDelete(null)}
                  className="flex-1 py-2.5 bg-slate-950 hover:bg-slate-900 border border-slate-800 rounded-xl text-slate-350 hover:text-white transition-all text-xs font-bold"
                >
                  Cancelar
                </button>
                <button
                  type="button"
                  onClick={confirmDeleteParticipant}
                  disabled={deleting}
                  className="flex-1 py-2.5 bg-rose-600 hover:bg-rose-500 disabled:opacity-50 text-white rounded-xl font-bold transition-all text-xs flex items-center justify-center gap-2"
                >
                  {deleting ? (
                    <>
                      <div className="w-3.5 h-3.5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                      Eliminando...
                    </>
                  ) : (
                    "Sí, eliminar"
                  )}
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
