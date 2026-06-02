"use client";

import React, { useEffect, useState, useRef } from "react";
import { apiFetch } from "../lib/api";
import Link from "next/link";
import {
  AlertTriangle,
  CheckCircle2,
  Clock,
  Users,
  ArrowRight,
  MessageCircle,
  Phone,
  Zap,
  Activity,
  BarChart3,
  ShieldAlert,
  RefreshCw,
  MapPin,
  Tag,
  Heart,
  Send,
  Sparkles,
  Bot,
  Plus,
  Trash2,
  X
} from "lucide-react";

// Types
interface MatchResult {
  offerer_id: number;
  offerer_name: string;
  offerer_city: string;
  offerer_neighborhood: string;
  offerer_phone_whatsapp: string | null;
  offerer_telegram: string | null;
  matched_categories: string[];
  offerer_description: string;
  offerer_dimensions: string[];
  compatibility_score: number;
  same_city: boolean;
  same_neighborhood: boolean;
  recently_exchanged: boolean;
}

interface Participant {
  id: number;
  name: string;
  email: string;
  city: string;
  neighborhood: string;
  offer_description: string;
  need_description: string;
  need_urgency: string;
  offer_categories: string[];
  need_categories: string[];
  offer_human_dimensions: string[];
  need_human_dimensions: string[];
  phone_call?: string;
  phone_whatsapp?: string;
  telegram_handle?: string;
  personal_values?: string;
}

interface UrgentNeed {
  participant_id: number;
  participant_name: string;
  city: string;
  neighborhood: string;
  need_description: string;
  need_urgency: string;
  need_categories: string[];
  need_dimensions: string[];
  days_without_exchange: number;
  latest_need_level: number | null;
  is_coherence_crime: boolean;
  top_matches: MatchResult[];
  phone_whatsapp?: string | null;
  telegram?: string | null;
}

interface CommunityGap {
  dimension: string;
  dimension_label: string;
  participants_needing: number;
  participants_offering: number;
  coverage_ratio: number;
  gap_severity: "critical" | "warning" | "ok";
}

interface ChatMessage {
  sender: "user" | "oracle";
  text: string;
  prefill?: {
    giver_id: number | null;
    giver_name: string | null;
    receiver_id: number | null;
    receiver_name: string | null;
    type: string;
    description: string;
    urgency: string;
    uth_hours: number | null;
  };
}

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

const OFFER_CATEGORIES = [
  { label: "Objeto", value: "objeto", emoji: "📦" },
  { label: "Alimentación", value: "alimentacion", emoji: "🍽" },
  { label: "Habilidad / Servicio", value: "habilidad", emoji: "🛠" },
  { label: "Conocimiento / Consejo", value: "conocimiento", emoji: "📚" },
  { label: "Transporte / Acompañamiento", value: "transporte", emoji: "🚗" },
  { label: "Tiempo y Compañía", value: "tiempo", emoji: "⏰" },
  { label: "Espacio", value: "espacio", emoji: "🏠" },
  { label: "Apoyo Económico", value: "apoyo_economico", emoji: "💰" },
];

const NEED_CATEGORIES = [
  { label: "Objeto", value: "objeto", emoji: "📦" },
  { label: "Alimentación", value: "alimentacion", emoji: "🍽" },
  { label: "Habilidad / Servicio", value: "habilidad", emoji: "🛠" },
];

const HUMAN_DIMENSIONS = [
  { label: "Educación / Aprendizaje", value: "crecimiento_aprendizaje" },
  { label: "Bienestar y Descanso", value: "bienestar_descanso" },
  { label: "Seguridad y Estabilidad", value: "seguridad_estabilidad" },
  { label: "Autonomía / Autoestima", value: "autoestima_autonomia" },
  { label: "Conexión Social", value: "conexion_social" },
  { label: "Recursos / Subsistencia", value: "prosperidad_recursos" },
  { label: "Placer y Goce", value: "placer_goce" },
  { label: "Vínculos Íntimos", value: "intimidad_vinculos" },
];

export default function PlazaDeApoyoPage() {
  const [loading, setLoading] = useState(true);
  const [profileStatus, setProfileStatus] = useState<"ok" | "no_profile" | "error">("ok");
  const [myProfile, setMyProfile] = useState<Participant | null>(null);
  const [seekerMatches, setSeekerMatches] = useState<MatchResult[]>([]);
  const [offererMatches, setOffererMatches] = useState<MatchResult[]>([]);
  const [urgentNeeds, setUrgentNeeds] = useState<UrgentNeed[]>([]);
  const [sdvGaps, setSdvGaps] = useState<CommunityGap[]>([]);
  
  // Chat state
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      sender: "oracle",
      text: "¡Hola! Soy el Oráculo Sintético. ¿Te gustaría reportar un intercambio de ayuda hoy? Cuéntame lo que pasó (ej. 'Max Nelson ayudó a Nelson Lopez con 2 horas de diseño') y yo me encargo de prepararte el formulario rápido."
    }
  ]);
  const [chatInput, setChatInput] = useState("");
  const [sendingChat, setSendingChat] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);
  const [registerStatus, setRegisterStatus] = useState<{ id: string; status: "success" | "error" | "submitting" | null }>({ id: "", status: null });

  // Profile edit modal state
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<"general" | "needs" | "offers">("general");

  // Form states for general info
  const [editName, setEditName] = useState("");
  const [editCity, setEditCity] = useState("");
  const [editNeighborhood, setEditNeighborhood] = useState("");
  const [editPhoneCall, setEditPhoneCall] = useState("");
  const [editPhoneWhatsapp, setEditPhoneWhatsapp] = useState("");
  const [editTelegramHandle, setEditTelegramHandle] = useState("");
  const [editPersonalValues, setEditPersonalValues] = useState("");

  // Primary need/offer form states
  const [editNeedDesc, setEditNeedDesc] = useState("");
  const [editNeedUrgency, setEditNeedUrgency] = useState("Media");
  const [editNeedCats, setEditNeedCats] = useState<string[]>([]);
  const [editNeedDims, setEditNeedDims] = useState<string[]>([]);

  const [editOfferDesc, setEditOfferDesc] = useState("");
  const [editOfferCats, setEditOfferCats] = useState<string[]>([]);
  const [editOfferDims, setEditOfferDims] = useState<string[]>([]);

  // Secondary lists state
  const [secondaryOffers, setSecondaryOffers] = useState<any[]>([]);
  const [secondaryNeeds, setSecondaryNeeds] = useState<any[]>([]);

  // Secondary need form state
  const [showAddNeedForm, setShowAddNeedForm] = useState(false);
  const [editingNeedId, setEditingNeedId] = useState<number | null>(null);
  const [secNeedDesc, setSecNeedDesc] = useState("");
  const [secNeedUrgency, setSecNeedUrgency] = useState("Media");
  const [secNeedCats, setSecNeedCats] = useState<string[]>([]);
  const [secNeedDims, setSecNeedDims] = useState<string[]>([]);

  // Secondary offer form state
  const [showAddOfferForm, setShowAddOfferForm] = useState(false);
  const [editingOfferId, setEditingOfferId] = useState<number | null>(null);
  const [secOfferDesc, setSecOfferDesc] = useState("");
  const [secOfferCats, setSecOfferCats] = useState<string[]>([]);
  const [secOfferDims, setSecOfferDims] = useState<string[]>([]);

  const resetSecondaryNeedForm = () => {
    setShowAddNeedForm(false);
    setEditingNeedId(null);
    setSecNeedDesc("");
    setSecNeedUrgency("Media");
    setSecNeedCats([]);
    setSecNeedDims([]);
  };

  const resetSecondaryOfferForm = () => {
    setShowAddOfferForm(false);
    setEditingOfferId(null);
    setSecOfferDesc("");
    setSecOfferCats([]);
    setSecOfferDims([]);
  };

  const openEditModal = () => {
    if (!myProfile) return;
    setEditName(myProfile.name || "");
    setEditCity(myProfile.city || "");
    setEditNeighborhood(myProfile.neighborhood || "");
    setEditPhoneCall(myProfile.phone_call || "");
    setEditPhoneWhatsapp(myProfile.phone_whatsapp || "");
    setEditTelegramHandle(myProfile.telegram_handle || "");
    setEditPersonalValues(myProfile.personal_values || "");

    setEditNeedDesc(myProfile.need_description || "");
    setEditNeedUrgency(myProfile.need_urgency || "Media");
    setEditNeedCats(myProfile.need_categories || []);
    setEditNeedDims(myProfile.need_human_dimensions || []);

    setEditOfferDesc(myProfile.offer_description || "");
    setEditOfferCats(myProfile.offer_categories || []);
    setEditOfferDims(myProfile.offer_human_dimensions || []);

    setActiveTab("general");
    setIsEditModalOpen(true);

    resetSecondaryNeedForm();
    resetSecondaryOfferForm();
  };

  const fetchData = async () => {
    try {
      // 1. Fetch personal profile and P2P matches
      const resMe = await apiFetch("/forms/matching/me");
      if (resMe.ok) {
        const dataMe = await resMe.json();
        if (dataMe.status === "no_profile") {
          setProfileStatus("no_profile");
        } else {
          setProfileStatus("ok");
          setMyProfile(dataMe.participant);
          setSeekerMatches(dataMe.seeker_matches || []);
          setOffererMatches(dataMe.offerer_matches || []);

          // Fetch secondary offers and needs
          const pid = dataMe.participant.id;
          const [resSecOffers, resSecNeeds] = await Promise.all([
            apiFetch(`/forms/participants/${pid}/offers`),
            apiFetch(`/forms/participants/${pid}/needs`)
          ]);
          
          if (resSecOffers.ok) {
            const dataSecOffers = await resSecOffers.json();
            setSecondaryOffers(dataSecOffers.offers || []);
          }
          if (resSecNeeds.ok) {
            const dataSecNeeds = await resSecNeeds.json();
            setSecondaryNeeds(dataSecNeeds.needs || []);
          }
        }
      } else {
        setProfileStatus("error");
      }

      // 2. Fetch community urgent needs
      const resUrgent = await apiFetch("/forms/matching/urgent?days_threshold=0");
      if (resUrgent.ok) {
        const dataUrgent = await resUrgent.json();
        // Combine crimes and warnings for community wall
        const allUrgent = [
          ...(dataUrgent.coherence_crimes || []),
          ...(dataUrgent.warnings || [])
        ];
        setUrgentNeeds(allUrgent);
      }

      // 3. Fetch community gaps
      const resGaps = await apiFetch("/forms/matching/gaps");
      if (resGaps.ok) {
        const dataGaps = await resGaps.json();
        setSdvGaps(dataGaps.gaps || []);
      }
    } catch (err) {
      console.error("Error fetching matching plaza data:", err);
      setProfileStatus("error");
    } finally {
      setLoading(false);
    }
  };

  const handleSaveProfile = async () => {
    if (!myProfile) return;
    try {
      const payload = {
        name: editName,
        city: editCity,
        neighborhood: editNeighborhood,
        phone_call: editPhoneCall,
        phone_whatsapp: editPhoneWhatsapp,
        telegram_handle: editTelegramHandle,
        personal_values: editPersonalValues,
        need_description: editNeedDesc,
        need_urgency: editNeedUrgency,
        need_categories: editNeedCats,
        need_human_dimensions: editNeedDims,
        offer_description: editOfferDesc,
        offer_categories: editOfferCats,
        offer_human_dimensions: editOfferDims,
      };

      const res = await apiFetch(`/forms/participants/${myProfile.id}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        setIsEditModalOpen(false);
        fetchData();
      } else {
        const errorData = await res.json();
        alert(`Error al guardar el perfil: ${errorData.error || "Ocurrió un error."}`);
      }
    } catch (err) {
      console.error(err);
      alert("Error de red al guardar el perfil.");
    }
  };

  const handleSaveSecondaryNeed = async () => {
    if (!myProfile) return;
    if (!secNeedDesc.trim()) {
      alert("La descripción es obligatoria.");
      return;
    }
    if (secNeedCats.length === 0) {
      alert("Debe seleccionar al menos una categoría.");
      return;
    }

    const payload = {
      description: secNeedDesc,
      urgency: secNeedUrgency,
      categories: secNeedCats,
      human_dimensions: secNeedDims,
    };

    try {
      let res;
      if (editingNeedId) {
        res = await apiFetch(`/forms/needs/${editingNeedId}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
      } else {
        res = await apiFetch(`/forms/participants/${myProfile.id}/needs`, {
          method: "POST",
          body: JSON.stringify(payload),
        });
      }

      if (res.ok) {
        resetSecondaryNeedForm();
        fetchData();
      } else {
        const errorData = await res.json();
        alert(`Error al guardar la necesidad: ${errorData.error || "Ocurrió un error."}`);
      }
    } catch (err) {
      console.error(err);
      alert("Error de red al guardar la necesidad.");
    }
  };

  const handleDeleteSecondaryNeed = async (id: number) => {
    if (!confirm("¿Está seguro de que desea eliminar esta necesidad secundaria?")) return;
    try {
      const res = await apiFetch(`/forms/needs/${id}`, {
        method: "DELETE",
      });

      if (res.ok) {
        fetchData();
      } else {
        const errorData = await res.json();
        alert(`Error al eliminar: ${errorData.error || "Ocurrió un error."}`);
      }
    } catch (err) {
      console.error(err);
      alert("Error de red al eliminar la necesidad.");
    }
  };

  const handleEditSecondaryNeed = (need: any) => {
    setEditingNeedId(need.id);
    setSecNeedDesc(need.description || "");
    setSecNeedUrgency(need.urgency || "Media");
    const cats = Array.isArray(need.categories) 
      ? need.categories 
      : (typeof need.categories === "string" ? JSON.parse(need.categories) : []);
    const dims = Array.isArray(need.human_dimensions) 
      ? need.human_dimensions 
      : (typeof need.human_dimensions === "string" ? JSON.parse(need.human_dimensions) : []);
    setSecNeedCats(cats);
    setSecNeedDims(dims);
    setShowAddNeedForm(true);
  };

  const handleSaveSecondaryOffer = async () => {
    if (!myProfile) return;
    if (!secOfferDesc.trim()) {
      alert("La descripción es obligatoria.");
      return;
    }
    if (secOfferCats.length === 0) {
      alert("Debe seleccionar al menos una categoría.");
      return;
    }

    const payload = {
      description: secOfferDesc,
      categories: secOfferCats,
      human_dimensions: secOfferDims,
    };

    try {
      let res;
      if (editingOfferId) {
        res = await apiFetch(`/forms/offers/${editingOfferId}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
      } else {
        res = await apiFetch(`/forms/participants/${myProfile.id}/offers`, {
          method: "POST",
          body: JSON.stringify(payload),
        });
      }

      if (res.ok) {
        resetSecondaryOfferForm();
        fetchData();
      } else {
        const errorData = await res.json();
        alert(`Error al guardar la oferta: ${errorData.error || "Ocurrió un error."}`);
      }
    } catch (err) {
      console.error(err);
      alert("Error de red al guardar la oferta.");
    }
  };

  const handleDeleteSecondaryOffer = async (id: number) => {
    if (!confirm("¿Está seguro de que desea eliminar esta oferta secundaria?")) return;
    try {
      const res = await apiFetch(`/forms/offers/${id}`, {
        method: "DELETE",
      });

      if (res.ok) {
        fetchData();
      } else {
        const errorData = await res.json();
        alert(`Error al eliminar: ${errorData.error || "Ocurrió un error."}`);
      }
    } catch (err) {
      console.error(err);
      alert("Error de red al eliminar la oferta.");
    }
  };

  const handleEditSecondaryOffer = (offer: any) => {
    setEditingOfferId(offer.id);
    setSecOfferDesc(offer.description || "");
    const cats = Array.isArray(offer.categories) 
      ? offer.categories 
      : (typeof offer.categories === "string" ? JSON.parse(offer.categories) : []);
    const dims = Array.isArray(offer.human_dimensions) 
      ? offer.human_dimensions 
      : (typeof offer.human_dimensions === "string" ? JSON.parse(offer.human_dimensions) : []);
    setSecOfferCats(cats);
    setSecOfferDims(dims);
    setShowAddOfferForm(true);
  };

  const handleDeleteProfile = async () => {
    if (!myProfile) return;
    if (!confirm("⚠️ ¡ADVERTENCIA CRÍTICA!\n\n¿Estás completamente seguro de que deseas darte de baja de la Red de Apoyo de la Maxocracia? Esta acción eliminará permanentemente tu perfil, todas tus ofertas y necesidades, y tu historial de coincidencias. Esto es irreversible.")) {
      return;
    }
    if (!confirm("Confirmación final: ¿Realmente deseas eliminar todos tus datos de la Red de Apoyo?")) {
      return;
    }

    try {
      const res = await apiFetch(`/forms/participants/${myProfile.id}`, {
        method: "DELETE",
      });

      if (res.ok) {
        setIsEditModalOpen(false);
        window.location.href = "/forms/cero";
      } else {
        const errorData = await res.json();
        alert(`Error al dar de baja el perfil: ${errorData.error || "Ocurrió un error."}`);
      }
    } catch (err) {
      console.error(err);
      alert("Error de red al dar de baja el perfil.");
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  const handleSendChat = async () => {
    if (!chatInput.trim() || sendingChat) return;
    const userText = chatInput.trim();
    setChatInput("");
    setChatMessages(prev => [...prev, { sender: "user", text: userText }]);
    setSendingChat(true);

    try {
      const res = await apiFetch("/forms/oracle/chat", {
        method: "POST",
        body: JSON.stringify({ message: userText })
      });
      if (res.ok) {
        const data = await res.json();
        setChatMessages(prev => [...prev, {
          sender: "oracle",
          text: data.reply,
          prefill: data.prefill || undefined
        }]);
      } else {
        setChatMessages(prev => [...prev, {
          sender: "oracle",
          text: "Lo siento, tuve un problema para procesar tu mensaje. ¿Podrías volver a intentarlo?"
        }]);
      }
    } catch (err) {
      setChatMessages(prev => [...prev, {
        sender: "oracle",
        text: "Error de conexión con el Oráculo Sintético."
      }]);
    } finally {
      setSendingChat(false);
    }
  };

  const handleRegisterExpress = async (prefill: any, messageIndex: number) => {
    const key = `msg-${messageIndex}`;
    setRegisterStatus({ id: key, status: "submitting" });
    
    // Generate a unique interchange ID
    const interchange_id = `INT-${Date.now().toString().slice(-6)}-${Math.floor(Math.random() * 1000)}`;
    const date = new Date().toISOString().split("T")[0];

    try {
      const payload = {
        date,
        interchange_id,
        giver_id: prefill.giver_id,
        receiver_id: prefill.receiver_id,
        type: [prefill.type || "habilidad"],
        description: prefill.description,
        urgency: prefill.urgency || "Media",
        uth_hours: prefill.uth_hours || 1.0,
        economic_value: 0,
        urf_description: "Registrado por el Oráculo Sintético",
        impact_resolution_score: 5,
        reciprocity_status: "Completada",
        human_dimension: [],
        coordination_method: "WhatsApp",
        requires_followup: 0,
        followup_scheduled_date: "",
        facilitator_notes: "Registro rápido Express vía Oráculo Sintético."
      };

      const res = await apiFetch("/forms/exchange", {
        method: "POST",
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        setRegisterStatus({ id: key, status: "success" });
        // Refresh matching statistics & profiles
        fetchData();
        // Append success message to chat
        setTimeout(() => {
          setChatMessages(prev => [...prev, {
            sender: "oracle",
            text: `✅ ¡Intercambio registrado con éxito! Código: ${interchange_id}. Se han sumado ${prefill.uth_hours} UTH de emisor a receptor.`
          }]);
        }, 500);
      } else {
        const errorData = await res.json();
        setRegisterStatus({ id: key, status: "error" });
        alert(`Error al registrar intercambio: ${errorData.error || "Ocurrió un error."}`);
      }
    } catch (err) {
      setRegisterStatus({ id: key, status: "error" });
      console.error(err);
      alert("Error de red al registrar intercambio.");
    }
  };

  const getContactLink = (match: MatchResult, type: "wa" | "tg", direction: "seeker" | "offerer") => {
    const text = direction === "seeker" 
      ? `Hola ${match.offerer_name}, te vi en la Plaza de Apoyo de la Cohorte Cero. Veo que puedes ayudar con '${match.offerer_description.substring(0, 45)}...'. ¿Te queda bien que conversemos?`
      : `Hola ${match.offerer_name}, te vi en la Plaza de Apoyo de la Cohorte Cero. Veo que necesitas ayuda con '${match.offerer_description.substring(0, 45)}...'. ¿Te gustaría que te eche una mano?`;
      
    if (type === "wa" && match.offerer_phone_whatsapp) {
      // Clean phone: replace symbols
      const cleanPhone = match.offerer_phone_whatsapp.replace(/[^\d+]/g, "");
      return `https://wa.me/${cleanPhone}?text=${encodeURIComponent(text)}`;
    }
    if (type === "tg" && match.offerer_telegram) {
      const cleanHandle = match.offerer_telegram.replace("@", "");
      return `https://t.me/${cleanHandle}`;
    }
    return "#";
  };

  const getWallNeedContactLink = (need: UrgentNeed, type: "wa" | "tg") => {
    const text = `Hola ${need.participant_name}, te vi en el Muro de Necesidades Colectivas de la Cohorte Cero. Veo que necesitas ayuda con '${need.need_description.substring(0, 45)}...'. ¿Te gustaría que te eche una mano?`;
      
    if (type === "wa" && need.phone_whatsapp) {
      const cleanPhone = need.phone_whatsapp.replace(/[^\d+]/g, "");
      return `https://wa.me/${cleanPhone}?text=${encodeURIComponent(text)}`;
    }
    if (type === "tg" && need.telegram) {
      const cleanHandle = need.telegram.replace("@", "");
      return `https://t.me/${cleanHandle}`;
    }
    return "#";
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex flex-col items-center justify-center p-6">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-emerald-500/20 border-t-emerald-500 rounded-full animate-spin" />
          <p className="text-slate-400 font-medium text-sm animate-pulse">Abriendo la Plaza de Apoyo...</p>
        </div>
      </div>
    );
  }

  if (profileStatus === "no_profile") {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-6">
        <div className="max-w-md w-full bg-slate-900/60 backdrop-blur-2xl border border-slate-800/80 rounded-3xl p-8 shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-emerald-500/0 via-emerald-500 to-emerald-500/0" />
          <div className="w-16 h-16 bg-emerald-500/10 rounded-2xl flex items-center justify-center border border-emerald-500/20 mb-6">
            <Users className="w-8 h-8 text-emerald-400" />
          </div>
          <h2 className="text-2xl font-bold text-white mb-3">Formulario CERO Requerido</h2>
          <p className="text-slate-400 text-sm leading-relaxed mb-8">
            Para entrar a la Plaza de Apoyo Peer-to-Peer, primero debes registrar tus ofertas y necesidades en la Cohorte Cero usando tu correo electrónico.
          </p>
          <Link
            href="/forms/cero"
            className="w-full py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-xl transition-all shadow-lg shadow-emerald-500/10 flex items-center justify-center gap-2 group"
          >
            Completar Formulario CERO
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>
      </div>
    );
  }

  if (profileStatus === "error") {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-6">
        <div className="max-w-md w-full text-center">
          <AlertTriangle className="w-16 h-16 text-rose-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-white mb-2">Error de Conexión</h2>
          <p className="text-slate-400 text-sm mb-6">No pudimos cargar la Plaza de Apoyo. Por favor verifica tu sesión o recarga la página.</p>
          <button onClick={fetchData} className="px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-xl transition-colors">
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  // Determine thermometer severity background
  const getSeverityBg = (severity: string) => {
    if (severity === "critical") return "bg-rose-500";
    if (severity === "warning") return "bg-amber-500";
    return "bg-emerald-500";
  };

  const getSeverityTextColor = (severity: string) => {
    if (severity === "critical") return "text-rose-400";
    if (severity === "warning") return "text-amber-400";
    return "text-emerald-400";
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4 sm:p-6 lg:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-slate-900">
          <div>
            <div className="flex items-center gap-2 text-emerald-400 font-semibold text-sm mb-1">
              <Sparkles className="w-4 h-4 animate-pulse" />
              <span>Cohorte Cero P2P</span>
            </div>
            <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl">
              Plaza de Apoyo Comunitario
            </h1>
            <p className="text-slate-400 text-sm sm:text-base mt-2 max-w-2xl">
              Bienvenido, <span className="text-emerald-400 font-bold">{myProfile?.name}</span>. 
              Este es tu centro comunitario de ayuda mutua, donde las necesidades encuentran soluciones en tiempo real.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <Link
              href="/forms/exchange"
              className="px-5 py-3 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/20 font-bold text-sm transition-all"
            >
              Registrar Intercambio (Wizard)
            </Link>
            <button
              onClick={fetchData}
              className="p-3 bg-slate-900 border border-slate-800 rounded-xl hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
              title="Actualizar datos"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Profile Card */}
        <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-900 rounded-3xl p-6 relative overflow-hidden transition-all duration-350 shadow-lg">
          <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-6">
            
            {/* Left/Main Side: Avatar + Details */}
            <div className="flex-1 space-y-6">
              
              {/* Profile Title & Subtitle */}
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-emerald-500/10 rounded-2xl flex items-center justify-center border border-emerald-500/20 shadow-md">
                  <Users className="w-6 h-6 text-emerald-400" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white tracking-wide">Mi Perfil en la Red de Apoyo</h2>
                  <p className="text-xs text-slate-500 mt-0.5">Gestiona tus necesidades, ofertas y datos de contacto públicos en la comunidad.</p>
                </div>
              </div>
              
              {/* Info Row: Location, Contact, Key Values */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm border-t border-slate-900 pt-4">
                
                {/* Location */}
                <div className="space-y-1">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block">Ubicación</span>
                  <div className="flex items-center gap-1.5 text-slate-300">
                    <MapPin className="w-4 h-4 text-emerald-500" />
                    <span>{myProfile?.neighborhood || "Sin barrio"}, {myProfile?.city || "Sin ciudad"}</span>
                  </div>
                </div>

                {/* Public Contact */}
                <div className="space-y-1">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block">Contacto Público</span>
                  <div className="space-y-0.5 text-slate-300">
                    {myProfile?.phone_whatsapp && (
                      <div className="text-xs">
                        WhatsApp: <span className="font-semibold text-emerald-400">{myProfile.phone_whatsapp}</span>
                      </div>
                    )}
                    {myProfile?.telegram_handle && (
                      <div className="text-xs">
                        Telegram: <span className="font-semibold text-sky-400">{myProfile.telegram_handle}</span>
                      </div>
                    )}
                    {!myProfile?.phone_whatsapp && !myProfile?.telegram_handle && (
                      <span className="text-slate-500 italic">No proporcionado</span>
                    )}
                  </div>
                </div>

                {/* Key Values */}
                <div className="space-y-1">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block">Mis Valores Clave</span>
                  <p className="text-xs text-slate-400 italic leading-relaxed">
                    {myProfile?.personal_values ? `"${myProfile.personal_values}"` : "No definidos"}
                  </p>
                </div>

              </div>
              
              {/* Grid: Primary Need vs Primary Offer */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-slate-900">
                
                {/* Primary Need */}
                <div className="bg-slate-950/40 border border-slate-900/60 rounded-2xl p-4 space-y-3 relative">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-rose-450">Mi Necesidad Activa</span>
                    <span className={`text-[9px] font-bold uppercase px-2 py-0.5 rounded-full ${
                      myProfile?.need_urgency === "Alta" ? "bg-rose-500/20 text-rose-400" :
                      myProfile?.need_urgency === "Media" ? "bg-amber-500/20 text-amber-400" :
                      "bg-emerald-500/20 text-emerald-400"
                    }`}>
                      Urgencia {myProfile?.need_urgency || "Media"}
                    </span>
                  </div>
                  <p className="text-slate-300 text-xs italic leading-relaxed">
                    {myProfile?.need_description ? `"${myProfile.need_description}"` : "No declarada"}
                  </p>
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {myProfile?.need_categories?.map((cat, i) => (
                      <span key={i} className="px-2 py-0.5 bg-slate-900 text-slate-400 text-[10px] rounded font-medium">
                        {categoryLabel(cat)}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Primary Offer */}
                <div className="bg-slate-950/40 border border-slate-900/60 rounded-2xl p-4 space-y-3 relative">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-400">Mi Oferta a la Comunidad</span>
                    <span className="text-[9px] font-bold uppercase px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center gap-1">
                      <Heart className="w-2.5 h-2.5 text-rose-500 fill-rose-500" />
                      Solidario
                    </span>
                  </div>
                  <p className="text-slate-300 text-xs italic leading-relaxed">
                    {myProfile?.offer_description ? `"${myProfile.offer_description}"` : "No declarada"}
                  </p>
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {myProfile?.offer_categories?.map((cat, i) => (
                      <span key={i} className="px-2 py-0.5 bg-slate-900 text-slate-400 text-[10px] rounded font-medium">
                        {categoryLabel(cat)}
                      </span>
                    ))}
                  </div>
                </div>

              </div>

            </div>

            {/* Right Side: Edit Button */}
            <div className="shrink-0 pt-2 lg:pt-0">
              <button
                onClick={openEditModal}
                className="px-5 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-sm transition-all shadow-md shadow-emerald-500/10 flex items-center gap-2 active:scale-95 group"
              >
                <svg className="w-4 h-4 transition-transform group-hover:rotate-12" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="3">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                </svg>
                Editar mi Perfil
              </button>
            </div>

          </div>
        </div>

        {/* Section 1: Community Wall & SDV Thermometer */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Muro de la Comunidad */}
          <div className="lg:col-span-7 space-y-6">
            <div className="flex items-center gap-2 mb-2">
              <Activity className="w-5 h-5 text-emerald-400" />
              <h2 className="text-xl font-bold uppercase tracking-wider text-slate-300">Muro de Necesidades Colectivas</h2>
            </div>

            {urgentNeeds.length === 0 ? (
              <div className="bg-slate-900/20 border border-slate-900 rounded-2xl p-8 text-center text-slate-500">
                No hay alertas ni necesidades urgentes reportadas en este momento. ¡La coherencia es plena!
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-4 max-h-[450px] overflow-y-auto pr-2 custom-scrollbar">
                {urgentNeeds.map((need, idx) => {
                  const isMyOwnNeed = need.participant_id === myProfile?.id;
                  return (
                    <div
                      key={idx}
                      className={`rounded-2xl border p-5 backdrop-blur-md relative overflow-hidden transition-all hover:translate-y-[-2px] ${
                        need.is_coherence_crime
                          ? "border-rose-500/30 bg-rose-950/15"
                          : "border-slate-800/80 bg-slate-900/40"
                      }`}
                    >
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <div className="flex items-center gap-2 flex-wrap mb-2">
                            <span className="font-extrabold text-white text-sm">{need.participant_name}</span>
                            <span className="text-slate-500 text-[10px]">•</span>
                            <span className="text-slate-400 text-xs flex items-center gap-1">
                              <MapPin className="w-3 h-3 text-slate-500" />
                              {need.neighborhood}, {need.city}
                            </span>
                            {need.is_coherence_crime && (
                              <span className="px-2 py-0.5 rounded-full text-[9px] font-black uppercase bg-rose-500 text-white animate-pulse">
                                CRIMEN DE COHERENCIA
                              </span>
                            )}
                          </div>
                          <p className="text-slate-300 text-sm leading-relaxed mb-4">{need.need_description}</p>
                          
                          <div className="flex items-center gap-2 flex-wrap">
                            {need.need_categories.map((cat, i) => (
                              <span key={i} className="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-450 text-xs font-semibold">
                                {categoryLabel(cat)}
                              </span>
                            ))}
                          </div>
                        </div>

                        <div className="flex flex-col items-end shrink-0">
                          <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded-lg ${
                            need.is_coherence_crime ? "bg-rose-500/20 text-rose-400" : "bg-amber-500/20 text-amber-400"
                          }`}>
                            {need.need_urgency}
                          </span>
                          <span className="text-slate-500 text-[10px] mt-2">
                            Hace {need.days_without_exchange} días
                          </span>
                        </div>
                      </div>

                      {/* Actions Footer inside the card */}
                      <div className="flex items-center justify-between mt-4 pt-3 border-t border-slate-900/60">
                        {isMyOwnNeed ? (
                          <span className="text-[10px] font-bold text-emerald-400 flex items-center gap-1 bg-emerald-500/10 px-2 py-0.5 rounded-full">
                            <CheckCircle2 className="w-3 h-3" />
                            Tu necesidad publicada
                          </span>
                        ) : (
                          <>
                            <div className="flex items-center gap-1.5">
                              {need.phone_whatsapp && (
                                <a
                                  href={getWallNeedContactLink(need, "wa")}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="p-2 rounded-xl bg-slate-950 border border-slate-900 text-emerald-400 hover:bg-slate-900 hover:text-emerald-300 transition-all"
                                  title="Contactar vía WhatsApp"
                                >
                                  <MessageCircle className="w-3.5 h-3.5" />
                                </a>
                              )}
                              {need.telegram && (
                                <a
                                  href={getWallNeedContactLink(need, "tg")}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="p-2 rounded-xl bg-slate-950 border border-slate-900 text-sky-400 hover:bg-slate-900 hover:text-sky-300 transition-all"
                                  title="Contactar vía Telegram"
                                >
                                  <Phone className="w-3.5 h-3.5" />
                                </a>
                              )}
                              {!need.phone_whatsapp && !need.telegram && (
                                <span className="text-[10px] text-slate-500 italic">Contacto privado</span>
                              )}
                            </div>
                            
                            {/* Ofrecer Ayuda Button */}
                            <Link
                              href={`/forms/exchange?giver_id=${myProfile?.id}&receiver_id=${need.participant_id}&type=${need.need_categories[0] || ""}&description=${encodeURIComponent("Ayuda con: " + need.need_description.substring(0, 50))}&urgency=${need.need_urgency}`}
                              className="px-3 py-1.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-bold rounded-lg transition-all flex items-center gap-1 active:scale-95 shadow-md shadow-emerald-500/5"
                            >
                              <Zap className="w-3 h-3 text-slate-950 fill-slate-950" />
                              Ofrecer Ayuda
                            </Link>
                          </>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Termómetro de Dignidad Vital (SDV) */}
          <div className="lg:col-span-5 bg-slate-900/40 backdrop-blur-xl border border-slate-900 rounded-3xl p-6 space-y-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-emerald-400" />
                <h2 className="text-xl font-bold uppercase tracking-wider text-slate-300">Termómetro SDV</h2>
              </div>
              <span className="text-xs text-slate-500">8 Dimensiones</span>
            </div>

            <div className="space-y-4 max-h-[380px] overflow-y-auto pr-1 custom-scrollbar">
              {sdvGaps.length === 0 ? (
                <p className="text-slate-500 text-sm">Cargando dimensiones del SDV...</p>
              ) : (
                sdvGaps.map((gap, idx) => (
                  <div key={idx} className="space-y-1.5">
                    <div className="flex items-center justify-between text-xs sm:text-sm">
                      <span className="font-semibold text-slate-200">{gap.dimension_label}</span>
                      <span className={`font-black ${getSeverityTextColor(gap.gap_severity)}`}>
                        Ratio: {gap.coverage_ratio >= 99 ? "1.00" : gap.coverage_ratio.toFixed(2)}
                      </span>
                    </div>
                    <div className="w-full h-2.5 bg-slate-950 rounded-full overflow-hidden border border-slate-800/30">
                      <div
                        className={`h-full rounded-full transition-all duration-500 ${getSeverityBg(gap.gap_severity)}`}
                        style={{ width: `${Math.min(gap.coverage_ratio * 100, 100)}%` }}
                      />
                    </div>
                    <div className="flex items-center justify-between text-[10px] text-slate-500">
                      <span>{gap.participants_offering} ofertas</span>
                      <span>{gap.participants_needing} necesitan</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Section 2: Personal Matches Grid */}
        <div className="space-y-6">
          <div className="flex items-center gap-2">
            <Users className="w-5 h-5 text-emerald-400" />
            <h2 className="text-xl font-bold uppercase tracking-wider text-slate-300">Mis Conexiones P2P Directas</h2>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            {/* Quién me puede ayudar */}
            <div className="bg-slate-900/30 border border-slate-900 rounded-3xl p-6 space-y-6">
              <div className="flex items-center justify-between border-b border-slate-900 pb-4">
                <h3 className="font-extrabold text-lg text-emerald-400 flex items-center gap-2">
                  <Zap className="w-4 h-4 text-emerald-400" />
                  ¿Quién puede ayudarme?
                </h3>
                <span className="text-xs text-slate-500">Coinciden con mis necesidades</span>
              </div>

              {seekerMatches.length === 0 ? (
                <div className="p-8 text-center text-slate-650 text-sm">
                  No hay oferentes registrados que coincidan con tus necesidades declaradas.
                </div>
              ) : (
                <div className="space-y-4 max-h-[350px] overflow-y-auto pr-1 custom-scrollbar">
                  {seekerMatches.map((match, idx) => (
                    <div key={idx} className="bg-slate-950/60 border border-slate-800/60 rounded-2xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div className="space-y-2">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="font-bold text-white text-sm">{match.offerer_name}</span>
                          <span className="text-xs text-slate-500 flex items-center gap-0.5">
                            <MapPin className="w-3 h-3 text-slate-600" />
                            {match.offerer_neighborhood}
                          </span>
                        </div>
                        <p className="text-xs text-slate-400 leading-normal">{match.offerer_description}</p>
                        <div className="flex flex-wrap gap-1.5">
                          {match.matched_categories.map((cat, i) => (
                            <span key={i} className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 text-[10px] rounded-md font-semibold border border-emerald-500/20">
                              {categoryLabel(cat)}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div className="flex items-center gap-2 shrink-0 sm:self-center">
                        {match.offerer_phone_whatsapp && (
                          <a
                            href={getContactLink(match, "wa", "seeker")}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-emerald-400 hover:bg-slate-850 transition-colors"
                            title="Contactar vía WhatsApp"
                          >
                            <MessageCircle className="w-4 h-4" />
                          </a>
                        )}
                        {match.offerer_telegram && (
                          <a
                            href={getContactLink(match, "tg", "seeker")}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-sky-400 hover:bg-slate-850 transition-colors"
                            title="Contactar vía Telegram"
                          >
                            <Phone className="w-4 h-4" />
                          </a>
                        )}
                        <Link
                          href={`/forms/exchange?giver_id=${match.offerer_id}&receiver_id=${myProfile?.id}&type=${match.matched_categories[0] || ""}`}
                          className="px-3.5 py-2.5 rounded-xl bg-emerald-500 text-slate-950 font-bold text-xs hover:bg-emerald-400 transition-all"
                        >
                          Registrar
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* A quién puedo ayudar */}
            <div className="bg-slate-900/30 border border-slate-900 rounded-3xl p-6 space-y-6">
              <div className="flex items-center justify-between border-b border-slate-900 pb-4">
                <h3 className="font-extrabold text-lg text-emerald-400 flex items-center gap-2">
                  <Heart className="w-4 h-4 text-emerald-400" />
                  ¿A quién puedo ayudar?
                </h3>
                <span className="text-xs text-slate-500">Necesitan lo que yo ofrezco</span>
              </div>

              {offererMatches.length === 0 ? (
                <div className="p-8 text-center text-slate-650 text-sm">
                  No hay participantes cuyas necesidades coincidan con lo que ofreces.
                </div>
              ) : (
                <div className="space-y-4 max-h-[350px] overflow-y-auto pr-1 custom-scrollbar">
                  {offererMatches.map((match, idx) => (
                    <div key={idx} className="bg-slate-950/60 border border-slate-800/60 rounded-2xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div className="space-y-2">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="font-bold text-white text-sm">{match.offerer_name}</span>
                          <span className="text-xs text-slate-500 flex items-center gap-0.5">
                            <MapPin className="w-3 h-3 text-slate-600" />
                            {match.offerer_neighborhood}
                          </span>
                        </div>
                        <p className="text-xs text-slate-400 leading-normal">{match.offerer_description}</p>
                        <div className="flex flex-wrap gap-1.5">
                          {match.matched_categories.map((cat, i) => (
                            <span key={i} className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 text-[10px] rounded-md font-semibold border border-emerald-500/20">
                              {categoryLabel(cat)}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div className="flex items-center gap-2 shrink-0 sm:self-center">
                        {match.offerer_phone_whatsapp && (
                          <a
                            href={getContactLink(match, "wa", "offerer")}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-emerald-400 hover:bg-slate-850 transition-colors"
                            title="Contactar vía WhatsApp"
                          >
                            <MessageCircle className="w-4 h-4" />
                          </a>
                        )}
                        {match.offerer_telegram && (
                          <a
                            href={getContactLink(match, "tg", "offerer")}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-sky-400 hover:bg-slate-850 transition-colors"
                            title="Contactar vía Telegram"
                          >
                            <Phone className="w-4 h-4" />
                          </a>
                        )}
                        <Link
                          href={`/forms/exchange?giver_id=${myProfile?.id}&receiver_id=${match.offerer_id}&type=${match.matched_categories[0] || ""}`}
                          className="px-3.5 py-2.5 rounded-xl bg-emerald-500 text-slate-950 font-bold text-xs hover:bg-emerald-400 transition-all"
                        >
                          Registrar
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Section 3: Synthetic Oracle Chatbot */}
        <div className="grid grid-cols-1 gap-6 bg-slate-900/25 border border-slate-900 rounded-3xl p-6 sm:p-8">
          <div className="flex items-center gap-3 border-b border-slate-900 pb-5 mb-4">
            <div className="w-10 h-10 bg-emerald-500/10 rounded-xl border border-emerald-500/20 flex items-center justify-center">
              <Bot className="w-5 h-5 text-emerald-400" />
            </div>
            <div>
              <h3 className="font-extrabold text-lg text-white">Oráculo Sintético Dinámico</h3>
              <p className="text-xs text-slate-500">Gestión de datos conversacional asistida por IA</p>
            </div>
          </div>

          <div className="flex flex-col h-[400px] bg-slate-950/80 border border-slate-900 rounded-2xl overflow-hidden shadow-inner">
            
            {/* Messages body */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
              {chatMessages.map((msg, index) => (
                <div key={index} className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
                  <div className={`max-w-[85%] rounded-2xl p-4 text-sm leading-relaxed ${
                    msg.sender === "user" 
                      ? "bg-emerald-500 text-slate-950 font-medium rounded-tr-none" 
                      : "bg-slate-900 text-slate-200 border border-slate-800 rounded-tl-none space-y-4"
                  }`}>
                    <p>{msg.text}</p>
                    
                    {/* Render Express Registration Prefill Card */}
                    {msg.prefill && (
                      <div className="p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-3">
                        <div className="flex items-center gap-1.5 text-xs text-emerald-400 font-bold uppercase tracking-wider">
                          <Zap className="w-3.5 h-3.5 animate-pulse" />
                          <span>Intercambio Detectado</span>
                        </div>
                        <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-xs border-t border-slate-900 pt-2.5 text-slate-400">
                          <div>
                            <span className="block text-[10px] text-slate-500">Emisor (Dador):</span>
                            <span className="font-semibold text-slate-300">{msg.prefill.giver_name || "Desconocido"}</span>
                          </div>
                          <div>
                            <span className="block text-[10px] text-slate-500">Receptor (Buscador):</span>
                            <span className="font-semibold text-slate-300">{msg.prefill.receiver_name || "Desconocido"}</span>
                          </div>
                          <div className="col-span-2">
                            <span className="block text-[10px] text-slate-500">Detalles:</span>
                            <span className="font-semibold text-slate-300 italic">"{msg.prefill.description}"</span>
                          </div>
                          <div>
                            <span className="block text-[10px] text-slate-500">Horas (UTH):</span>
                            <span className="font-semibold text-emerald-400">{msg.prefill.uth_hours} hrs</span>
                          </div>
                          <div>
                            <span className="block text-[10px] text-slate-500">Urgencia:</span>
                            <span className="font-semibold text-slate-300">{msg.prefill.urgency}</span>
                          </div>
                        </div>

                        {registerStatus.id === `msg-${index}` && registerStatus.status === "success" ? (
                          <div className="py-2.5 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-center text-xs text-emerald-400 font-semibold flex items-center justify-center gap-2">
                            <CheckCircle2 className="w-4 h-4" />
                            Registrado Exitosamente
                          </div>
                        ) : (
                          <button
                            onClick={() => handleRegisterExpress(msg.prefill, index)}
                            disabled={!msg.prefill.giver_id || !msg.prefill.receiver_id || (registerStatus.id === `msg-${index}` && registerStatus.status === "submitting")}
                            className="w-full py-2.5 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 disabled:cursor-not-allowed text-slate-950 font-bold text-xs rounded-lg transition-all shadow-md shadow-emerald-500/10 active:scale-95 flex items-center justify-center gap-2"
                          >
                            {registerStatus.id === `msg-${index}` && registerStatus.status === "submitting" ? (
                              <>
                                <div className="w-3.5 h-3.5 border-2 border-slate-950/20 border-t-slate-950 rounded-full animate-spin" />
                                Registrando...
                              </>
                            ) : (
                              <>
                                Registrar Intercambio Express
                              </>
                            )}
                          </button>
                        )}
                        {(!msg.prefill.giver_id || !msg.prefill.receiver_id) && (
                          <p className="text-[10px] text-rose-450 leading-normal">
                            ⚠️ No se pudieron asociar los nombres de los participantes con registros reales en la Cohorte Cero. Por favor especifica nombres completos o registrados.
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {sendingChat && (
                <div className="flex justify-start">
                  <div className="bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-none p-4 flex items-center gap-2">
                    <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-bounce" />
                    <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-bounce delay-100" />
                    <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-bounce delay-200" />
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>

            {/* Input form */}
            <form 
              onSubmit={(e) => { e.preventDefault(); handleSendChat(); }}
              className="flex items-center gap-2 p-3 bg-slate-900 border-t border-slate-900"
            >
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                placeholder="Escribe un mensaje al Oráculo..."
                className="flex-1 px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-sm focus:outline-none focus:border-emerald-500 text-white placeholder-slate-500 transition-colors"
              />
              <button
                type="submit"
                disabled={!chatInput.trim() || sendingChat}
                className="p-3 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl text-slate-950 transition-all font-bold active:scale-95"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </div>

      </div>

      {/* Modal de Edición de Perfil */}
      {isEditModalOpen && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-md flex items-center justify-center z-50 p-4 animate-in fade-in duration-200">
          <div className="bg-slate-900 border border-slate-850 rounded-3xl w-full max-w-3xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200">
            
            {/* Modal Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-900">
              <div className="flex items-center gap-2">
                <Users className="w-5 h-5 text-emerald-400" />
                <h3 className="text-lg font-bold text-white">Editar Perfil en la Red de Apoyo</h3>
              </div>
              <button
                onClick={() => setIsEditModalOpen(false)}
                className="p-1 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Tabs */}
            <div className="flex gap-4 px-6 border-b border-slate-800 bg-slate-900/60 overflow-x-auto">
              <button
                onClick={() => setActiveTab("general")}
                className={`py-3 text-xs uppercase tracking-wider font-extrabold border-b-2 transition-all shrink-0 ${
                  activeTab === "general"
                    ? "border-emerald-500 text-emerald-400"
                    : "border-transparent text-slate-400 hover:text-white"
                }`}
              >
                Datos Generales
              </button>
              <button
                onClick={() => setActiveTab("needs")}
                className={`py-3 text-xs uppercase tracking-wider font-extrabold border-b-2 transition-all shrink-0 ${
                  activeTab === "needs"
                    ? "border-emerald-500 text-emerald-400"
                    : "border-transparent text-slate-400 hover:text-white"
                }`}
              >
                Mis Necesidades
              </button>
              <button
                onClick={() => setActiveTab("offers")}
                className={`py-3 text-xs uppercase tracking-wider font-extrabold border-b-2 transition-all shrink-0 ${
                  activeTab === "offers"
                    ? "border-emerald-500 text-emerald-400"
                    : "border-transparent text-slate-400 hover:text-white"
                }`}
              >
                Mis Ofertas
              </button>
            </div>

            {/* Modal Content Scroll Area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-950/20 custom-scrollbar">
              
              {/* TAB 1: General Info */}
              {activeTab === "general" && (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    
                    {/* Nombre */}
                    <div className="space-y-1">
                      <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Nombre Completo</label>
                      <input
                        type="text"
                        value={editName}
                        onChange={(e) => setEditName(e.target.value)}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm focus:outline-none focus:border-emerald-500 text-white placeholder-slate-600 transition-colors"
                        placeholder="Tu nombre completo"
                      />
                    </div>

                    {/* WhatsApp */}
                    <div className="space-y-1">
                      <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">WhatsApp (Ej: +573115746208)</label>
                      <input
                        type="text"
                        value={editPhoneWhatsapp}
                        onChange={(e) => setEditPhoneWhatsapp(e.target.value)}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm focus:outline-none focus:border-emerald-500 text-white placeholder-slate-600 transition-colors"
                        placeholder="+57..."
                      />
                    </div>

                    {/* Telegram */}
                    <div className="space-y-1">
                      <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Telegram Username (Ej: @max)</label>
                      <input
                        type="text"
                        value={editTelegramHandle}
                        onChange={(e) => setEditTelegramHandle(e.target.value)}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm focus:outline-none focus:border-emerald-500 text-white placeholder-slate-600 transition-colors"
                        placeholder="@username"
                      />
                    </div>

                    {/* Teléfono de Llamadas */}
                    <div className="space-y-1">
                      <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Teléfono de Llamadas (Opcional)</label>
                      <input
                        type="text"
                        value={editPhoneCall}
                        onChange={(e) => setEditPhoneCall(e.target.value)}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm focus:outline-none focus:border-emerald-500 text-white placeholder-slate-600 transition-colors"
                        placeholder="Número de celular"
                      />
                    </div>

                    {/* Barrio */}
                    <div className="space-y-1">
                      <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Barrio</label>
                      <input
                        type="text"
                        value={editNeighborhood}
                        onChange={(e) => setEditNeighborhood(e.target.value)}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm focus:outline-none focus:border-emerald-500 text-white placeholder-slate-600 transition-colors"
                        placeholder="Ej: Santa Lucía"
                      />
                    </div>

                    {/* Ciudad */}
                    <div className="space-y-1">
                      <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Ciudad</label>
                      <input
                        type="text"
                        value={editCity}
                        onChange={(e) => setEditCity(e.target.value)}
                        className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm focus:outline-none focus:border-emerald-500 text-white placeholder-slate-600 transition-colors"
                        placeholder="Ej: Bogotá"
                      />
                    </div>

                  </div>

                  {/* Valores Clave */}
                  <div className="space-y-1">
                    <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Tus Valores Clave</label>
                    <textarea
                      value={editPersonalValues}
                      onChange={(e) => setEditPersonalValues(e.target.value)}
                      rows={3}
                      className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-sm focus:outline-none focus:border-emerald-500 text-white placeholder-slate-600 transition-colors resize-none"
                      placeholder="Ej: Honestidad, Solidaridad, Autonomía..."
                    />
                  </div>

                </div>
              )}

              {/* TAB 2: Mis Necesidades (Primary + Secondary) */}
              {activeTab === "needs" && (
                <div className="space-y-8">
                  
                  {/* Necesidad Principal */}
                  <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-5 space-y-4">
                    <div className="flex items-center gap-1 text-xs font-extrabold uppercase text-emerald-400">
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>Necesidad Principal Activa</span>
                    </div>

                    <div className="space-y-1">
                      <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Descripción de la Necesidad</label>
                      <textarea
                        value={editNeedDesc}
                        onChange={(e) => setEditNeedDesc(e.target.value)}
                        rows={3}
                        className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-sm focus:outline-none focus:border-emerald-500 text-white placeholder-slate-650 transition-colors resize-none"
                        placeholder="¿Qué necesitas ayuda para resolver?"
                      />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {/* Urgencia */}
                      <div className="space-y-2">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">Urgencia</span>
                        <div className="flex items-center gap-3">
                          {["Alta", "Media", "Baja"].map((urg) => (
                            <button
                              key={urg}
                              type="button"
                              onClick={() => setEditNeedUrgency(urg)}
                              className={`flex-1 py-2 px-3 border rounded-xl font-bold text-xs transition-all ${
                                editNeedUrgency === urg
                                  ? urg === "Alta"
                                    ? "bg-rose-500/20 border-rose-500 text-rose-400"
                                    : urg === "Media"
                                    ? "bg-amber-500/20 border-amber-500 text-amber-400"
                                    : "bg-emerald-500/20 border-emerald-500 text-emerald-400"
                                  : "bg-slate-950 border-slate-800 text-slate-400 hover:text-white"
                              }`}
                            >
                              {urg}
                            </button>
                          ))}
                        </div>
                      </div>

                      {/* Categorías */}
                      <div className="space-y-2">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">Categorías</span>
                        <div className="flex flex-wrap gap-2">
                          {NEED_CATEGORIES.map((cat) => {
                            const isSelected = editNeedCats.includes(cat.value);
                            return (
                              <button
                                key={cat.value}
                                type="button"
                                onClick={() => {
                                  if (isSelected) {
                                    setEditNeedCats(editNeedCats.filter((x) => x !== cat.value));
                                  } else {
                                    setEditNeedCats([...editNeedCats, cat.value]);
                                  }
                                }}
                                className={`py-1.5 px-3 border rounded-xl font-bold text-xs flex items-center gap-1.5 transition-all ${
                                  isSelected
                                    ? "bg-emerald-500 border-emerald-500 text-slate-950"
                                    : "bg-slate-950 border-slate-800 text-slate-400 hover:text-white"
                                }`}
                              >
                                <span>{cat.emoji}</span>
                                <span>{cat.label}</span>
                              </button>
                            );
                          })}
                        </div>
                      </div>
                    </div>

                    {/* Dimensiones Humanas del SDV */}
                    <div className="space-y-2">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">Dimensiones de Dignidad Humana Asignadas</span>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {HUMAN_DIMENSIONS.map((dim) => {
                          const isSelected = editNeedDims.includes(dim.value);
                          return (
                            <button
                              key={dim.value}
                              type="button"
                              onClick={() => {
                                if (isSelected) {
                                  setEditNeedDims(editNeedDims.filter((x) => x !== dim.value));
                                } else {
                                  setEditNeedDims([...editNeedDims, dim.value]);
                                }
                              }}
                              className={`py-2 px-3 border rounded-xl font-bold text-left text-xs transition-all flex items-center justify-between ${
                                isSelected
                                  ? "bg-emerald-500/10 border-emerald-500 text-emerald-400"
                                  : "bg-slate-950 border-slate-800 text-slate-400 hover:text-white"
                              }`}
                            >
                              <span>{dim.label}</span>
                              {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />}
                            </button>
                          );
                        })}
                      </div>
                    </div>

                  </div>

                  {/* Necesidades Secundarias */}
                  <div className="space-y-4 pt-4 border-t border-slate-800">
                    <div className="flex items-center justify-between">
                      <h4 className="font-bold text-sm text-slate-300 uppercase tracking-wider">Necesidades Secundarias de Apoyo</h4>
                      {!showAddNeedForm && (
                        <button
                          onClick={() => {
                            resetSecondaryNeedForm();
                            setShowAddNeedForm(true);
                          }}
                          className="px-3 py-1.5 bg-slate-900 hover:bg-slate-850 border border-slate-800 text-emerald-400 hover:text-emerald-300 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5"
                        >
                          <Plus className="w-3.5 h-3.5" />
                          Agregar Necesidad
                        </button>
                      )}
                    </div>

                    {/* Formulario de Agregar/Editar Necesidad Secundaria */}
                    {showAddNeedForm && (
                      <div className="bg-slate-950/60 border border-slate-800 rounded-2xl p-4 space-y-4 animate-in slide-in-from-top-2 duration-200">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-black text-emerald-400 uppercase tracking-widest">
                            {editingNeedId ? "✏️ Editar Necesidad Secundaria" : "⚡ Nueva Necesidad Secundaria"}
                          </span>
                          <button
                            onClick={resetSecondaryNeedForm}
                            className="p-1 text-slate-500 hover:text-white transition-colors"
                          >
                            <X className="w-4 h-4" />
                          </button>
                        </div>

                        <div className="space-y-1">
                          <label className="text-[9px] font-bold uppercase tracking-wider text-slate-500">Descripción de la necesidad</label>
                          <textarea
                            value={secNeedDesc}
                            onChange={(e) => setSecNeedDesc(e.target.value)}
                            rows={2}
                            className="w-full px-4 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-emerald-500 text-white placeholder-slate-650 transition-colors resize-none"
                            placeholder="Ej: Ayuda para pintar la sala..."
                          />
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {/* Urgencia */}
                          <div className="space-y-2">
                            <span className="text-[9px] font-bold uppercase tracking-wider text-slate-500 block">Urgencia</span>
                            <div className="flex items-center gap-2">
                              {["Alta", "Media", "Baja"].map((urg) => (
                                <button
                                  key={urg}
                                  type="button"
                                  onClick={() => setSecNeedUrgency(urg)}
                                  className={`flex-1 py-1.5 px-2 border rounded-lg font-bold text-[10px] transition-all ${
                                    secNeedUrgency === urg
                                      ? urg === "Alta"
                                        ? "bg-rose-500/20 border-rose-500 text-rose-400"
                                        : urg === "Media"
                                        ? "bg-amber-500/20 border-amber-500 text-amber-400"
                                        : "bg-emerald-500/20 border-emerald-500 text-emerald-400"
                                      : "bg-slate-905 border-slate-800 text-slate-450 hover:text-white"
                                  }`}
                                >
                                  {urg}
                                </button>
                              ))}
                            </div>
                          </div>

                          {/* Categorías */}
                          <div className="space-y-2">
                            <span className="text-[9px] font-bold uppercase tracking-wider text-slate-500 block">Categorías</span>
                            <div className="flex flex-wrap gap-1.5">
                              {NEED_CATEGORIES.map((cat) => {
                                const isSelected = secNeedCats.includes(cat.value);
                                return (
                                  <button
                                    key={cat.value}
                                    type="button"
                                    onClick={() => {
                                      if (isSelected) {
                                        setSecNeedCats(secNeedCats.filter((x) => x !== cat.value));
                                      } else {
                                        setSecNeedCats([...secNeedCats, cat.value]);
                                      }
                                    }}
                                    className={`py-1 px-2 border rounded-lg font-bold text-[10px] flex items-center gap-1 transition-all ${
                                      isSelected
                                        ? "bg-emerald-500 border-emerald-500 text-slate-950"
                                        : "bg-slate-900 border-slate-800 text-slate-450 hover:text-white"
                                    }`}
                                  >
                                    <span>{cat.emoji}</span>
                                    <span>{cat.label}</span>
                                  </button>
                                );
                              })}
                            </div>
                          </div>
                        </div>

                        {/* Dimensiones Humanas */}
                        <div className="space-y-2">
                          <span className="text-[9px] font-bold uppercase tracking-wider text-slate-500 block">Dimensiones de Dignidad Humana</span>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
                            {HUMAN_DIMENSIONS.map((dim) => {
                              const isSelected = secNeedDims.includes(dim.value);
                              return (
                                <button
                                  key={dim.value}
                                  type="button"
                                  onClick={() => {
                                    if (isSelected) {
                                      setSecNeedDims(secNeedDims.filter((x) => x !== dim.value));
                                    } else {
                                      setSecNeedDims([...secNeedDims, dim.value]);
                                    }
                                  }}
                                  className={`py-1.5 px-2.5 border rounded-lg font-semibold text-left text-[10px] transition-all flex items-center justify-between ${
                                    isSelected
                                      ? "bg-emerald-500/10 border-emerald-500 text-emerald-400"
                                      : "bg-slate-900 border-slate-800 text-slate-450 hover:text-white"
                                  }`}
                                >
                                  <span>{dim.label}</span>
                                  {isSelected && <CheckCircle2 className="w-3 h-3 text-emerald-400" />}
                                </button>
                              );
                            })}
                          </div>
                        </div>

                        <div className="flex justify-end gap-2 pt-2 border-t border-slate-805">
                          <button
                            type="button"
                            onClick={resetSecondaryNeedForm}
                            className="px-3 py-1.5 bg-slate-900 hover:bg-slate-850 rounded-lg text-[11px] text-slate-400 font-bold transition-all"
                          >
                            Cancelar
                          </button>
                          <button
                            type="button"
                            onClick={handleSaveSecondaryNeed}
                            className="px-3 py-1.5 bg-emerald-500 hover:bg-emerald-400 rounded-lg text-[11px] text-slate-950 font-extrabold transition-all"
                          >
                            {editingNeedId ? "Actualizar" : "Agregar"}
                          </button>
                        </div>
                      </div>
                    )}

                    {/* Listado de Necesidades Secundarias */}
                    <div className="space-y-2">
                      {secondaryNeeds.length === 0 ? (
                        <p className="text-xs text-slate-500 italic text-center py-4 bg-slate-900/10 rounded-xl border border-dashed border-slate-800/40">
                          No tienes necesidades secundarias declaradas.
                        </p>
                      ) : (
                        secondaryNeeds.map((need) => (
                          <div
                            key={need.id}
                            className="bg-slate-950/40 border border-slate-900 rounded-xl p-3 flex items-start justify-between gap-4 transition-all hover:border-slate-800"
                          >
                            <div className="space-y-1.5 flex-1">
                              <div className="flex items-center gap-2 flex-wrap">
                                <span className={`text-[9px] font-black uppercase tracking-wider px-1.5 py-0.5 rounded ${
                                  need.urgency === "Alta" ? "bg-rose-500/20 text-rose-400" :
                                  need.urgency === "Media" ? "bg-amber-500/20 text-amber-400" :
                                  "bg-emerald-500/20 text-emerald-400"
                                }`}>
                                  {need.urgency}
                                </span>
                                {need.categories?.map((cat: string) => (
                                  <span key={cat} className="text-[9px] font-semibold text-slate-400 bg-slate-900 px-1.5 py-0.5 rounded">
                                    {categoryLabel(cat)}
                                  </span>
                                ))}
                              </div>
                              <p className="text-xs text-slate-300 leading-relaxed font-medium">"{need.description}"</p>
                              {need.human_dimensions && need.human_dimensions.length > 0 && (
                                <div className="flex flex-wrap gap-1">
                                  {need.human_dimensions.map((dim: string) => (
                                    <span key={dim} className="text-[8px] font-medium text-emerald-450/80 bg-emerald-500/5 px-1.5 py-0.2 rounded border border-emerald-500/10">
                                      {HUMAN_DIMENSIONS.find(d => d.value === dim)?.label || dim}
                                    </span>
                                  ))}
                                </div>
                              )}
                            </div>

                            <div className="flex items-center gap-1.5 shrink-0">
                              <button
                                onClick={() => handleEditSecondaryNeed(need)}
                                className="p-1.5 hover:bg-slate-800 text-slate-400 hover:text-white rounded-lg transition-colors"
                                title="Editar"
                              >
                                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                                </svg>
                              </button>
                              <button
                                onClick={() => handleDeleteSecondaryNeed(need.id)}
                                className="p-1.5 hover:bg-slate-800 text-rose-500 hover:text-rose-400 rounded-lg transition-colors"
                                title="Eliminar"
                              >
                                <Trash2 className="w-3.5 h-3.5" />
                              </button>
                            </div>
                          </div>
                        ))
                      )}
                    </div>

                  </div>

                </div>
              )}

              {/* TAB 3: Mis Ofertas (Primary + Secondary) */}
              {activeTab === "offers" && (
                <div className="space-y-8">
                  
                  {/* Oferta Principal */}
                  <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-5 space-y-4">
                    <div className="flex items-center gap-1 text-xs font-extrabold uppercase text-emerald-400">
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>Oferta Principal a la Comunidad</span>
                    </div>

                    <div className="space-y-1">
                      <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Descripción de la Oferta</label>
                      <textarea
                        value={editOfferDesc}
                        onChange={(e) => setEditOfferDesc(e.target.value)}
                        rows={3}
                        className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-sm focus:outline-none focus:border-emerald-500 text-white placeholder-slate-650 transition-colors resize-none"
                        placeholder="¿Qué habilidades, recursos o tiempo puedes ofrecer?"
                      />
                    </div>

                    {/* Categorías */}
                    <div className="space-y-2">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">Categorías de la Oferta</span>
                      <div className="flex flex-wrap gap-2">
                        {OFFER_CATEGORIES.map((cat) => {
                          const isSelected = editOfferCats.includes(cat.value);
                          return (
                            <button
                              key={cat.value}
                              type="button"
                              onClick={() => {
                                  if (isSelected) {
                                    setEditOfferCats(editOfferCats.filter((x) => x !== cat.value));
                                  } else {
                                    setEditOfferCats([...editOfferCats, cat.value]);
                                  }
                              }}
                              className={`py-1.5 px-3 border rounded-xl font-bold text-xs flex items-center gap-1.5 transition-all ${
                                isSelected
                                  ? "bg-emerald-500 border-emerald-500 text-slate-950"
                                  : "bg-slate-950 border-slate-800 text-slate-400 hover:text-white"
                              }`}
                            >
                              <span>{cat.emoji}</span>
                              <span>{cat.label}</span>
                            </button>
                          );
                        })}
                      </div>
                    </div>

                    {/* Dimensiones Humanas del SDV */}
                    <div className="space-y-2">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">Dimensiones de Dignidad Humana Impactadas</span>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {HUMAN_DIMENSIONS.map((dim) => {
                          const isSelected = editOfferDims.includes(dim.value);
                          return (
                            <button
                              key={dim.value}
                              type="button"
                              onClick={() => {
                                if (isSelected) {
                                  setEditOfferDims(editOfferDims.filter((x) => x !== dim.value));
                                } else {
                                  setEditOfferDims([...editOfferDims, dim.value]);
                                }
                              }}
                              className={`py-2 px-3 border rounded-xl font-bold text-left text-xs transition-all flex items-center justify-between ${
                                isSelected
                                  ? "bg-emerald-500/10 border-emerald-500 text-emerald-400"
                                  : "bg-slate-950 border-slate-800 text-slate-400 hover:text-white"
                              }`}
                            >
                              <span>{dim.label}</span>
                              {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />}
                            </button>
                          );
                        })}
                      </div>
                    </div>

                  </div>

                  {/* Ofertas Secundarias */}
                  <div className="space-y-4 pt-4 border-t border-slate-800">
                    <div className="flex items-center justify-between">
                      <h4 className="font-bold text-sm text-slate-300 uppercase tracking-wider">Ofertas Secundarias de Apoyo</h4>
                      {!showAddOfferForm && (
                        <button
                          onClick={() => {
                            resetSecondaryOfferForm();
                            setShowAddOfferForm(true);
                          }}
                          className="px-3 py-1.5 bg-slate-900 hover:bg-slate-850 border border-slate-800 text-emerald-400 hover:text-emerald-300 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5"
                        >
                          <Plus className="w-3.5 h-3.5" />
                          Agregar Oferta
                        </button>
                      )}
                    </div>

                    {/* Formulario de Agregar/Editar Oferta Secundaria */}
                    {showAddOfferForm && (
                      <div className="bg-slate-950/60 border border-slate-800 rounded-2xl p-4 space-y-4 animate-in slide-in-from-top-2 duration-200">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-black text-emerald-400 uppercase tracking-widest">
                            {editingOfferId ? "✏️ Editar Oferta Secundaria" : "⚡ Nueva Oferta Secundaria"}
                          </span>
                          <button
                            onClick={resetSecondaryOfferForm}
                            className="p-1 text-slate-500 hover:text-white transition-colors"
                          >
                            <X className="w-4 h-4" />
                          </button>
                        </div>

                        <div className="space-y-1">
                          <label className="text-[9px] font-bold uppercase tracking-wider text-slate-500">Descripción de la oferta</label>
                          <textarea
                            value={secOfferDesc}
                            onChange={(e) => setSecOfferDesc(e.target.value)}
                            rows={2}
                            className="w-full px-4 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-xs focus:outline-none focus:border-emerald-500 text-white placeholder-slate-650 transition-colors resize-none"
                            placeholder="Ej: Ofrezco asesorías en contabilidad los sábados..."
                          />
                        </div>

                        {/* Categorías */}
                        <div className="space-y-2">
                          <span className="text-[9px] font-bold uppercase tracking-wider text-slate-500 block">Categorías</span>
                          <div className="flex flex-wrap gap-1.5">
                            {OFFER_CATEGORIES.map((cat) => {
                              const isSelected = secOfferCats.includes(cat.value);
                              return (
                                <button
                                  key={cat.value}
                                  type="button"
                                  onClick={() => {
                                    if (isSelected) {
                                      setSecOfferCats(secOfferCats.filter((x) => x !== cat.value));
                                    } else {
                                      setSecOfferCats([...secOfferCats, cat.value]);
                                    }
                                  }}
                                  className={`py-1 px-2 border rounded-lg font-bold text-[10px] flex items-center gap-1 transition-all ${
                                    isSelected
                                      ? "bg-emerald-500 border-emerald-500 text-slate-950"
                                      : "bg-slate-900 border-slate-800 text-slate-450 hover:text-white"
                                  }`}
                                >
                                  <span>{cat.emoji}</span>
                                  <span>{cat.label}</span>
                                </button>
                              );
                            })}
                          </div>
                        </div>

                        {/* Dimensiones Humanas */}
                        <div className="space-y-2">
                          <span className="text-[9px] font-bold uppercase tracking-wider text-slate-500 block">Dimensiones de Dignidad Humana</span>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
                            {HUMAN_DIMENSIONS.map((dim) => {
                              const isSelected = secOfferDims.includes(dim.value);
                              return (
                                <button
                                  key={dim.value}
                                  type="button"
                                  onClick={() => {
                                    if (isSelected) {
                                      setSecOfferDims(secOfferDims.filter((x) => x !== dim.value));
                                    } else {
                                      setSecOfferDims([...secOfferDims, dim.value]);
                                    }
                                  }}
                                  className={`py-1.5 px-2.5 border rounded-lg font-semibold text-left text-[10px] transition-all flex items-center justify-between ${
                                    isSelected
                                      ? "bg-emerald-500/10 border-emerald-500 text-emerald-400"
                                      : "bg-slate-900 border-slate-800 text-slate-450 hover:text-white"
                                  }`}
                                >
                                  <span>{dim.label}</span>
                                  {isSelected && <CheckCircle2 className="w-3 h-3 text-emerald-400" />}
                                </button>
                              );
                            })}
                          </div>
                        </div>

                        <div className="flex justify-end gap-2 pt-2 border-t border-slate-805">
                          <button
                            type="button"
                            onClick={resetSecondaryOfferForm}
                            className="px-3 py-1.5 bg-slate-900 hover:bg-slate-850 rounded-lg text-[11px] text-slate-400 font-bold transition-all"
                          >
                            Cancelar
                          </button>
                          <button
                            type="button"
                            onClick={handleSaveSecondaryOffer}
                            className="px-3 py-1.5 bg-emerald-500 hover:bg-emerald-400 rounded-lg text-[11px] text-slate-950 font-extrabold transition-all"
                          >
                            {editingOfferId ? "Actualizar" : "Agregar"}
                          </button>
                        </div>
                      </div>
                    )}

                    {/* Listado de Ofertas Secundarias */}
                    <div className="space-y-2">
                      {secondaryOffers.length === 0 ? (
                        <p className="text-xs text-slate-500 italic text-center py-4 bg-slate-900/10 rounded-xl border border-dashed border-slate-800/40">
                          No tienes ofertas secundarias declaradas.
                        </p>
                      ) : (
                        secondaryOffers.map((offer) => (
                          <div
                            key={offer.id}
                            className="bg-slate-950/40 border border-slate-900 rounded-xl p-3 flex items-start justify-between gap-4 transition-all hover:border-slate-800"
                          >
                            <div className="space-y-1.5 flex-1">
                              <div className="flex items-center gap-2 flex-wrap">
                                {offer.categories?.map((cat: string) => (
                                  <span key={cat} className="text-[9px] font-semibold text-slate-400 bg-slate-900 px-1.5 py-0.5 rounded">
                                    {categoryLabel(cat)}
                                  </span>
                                ))}
                              </div>
                              <p className="text-xs text-slate-300 leading-relaxed font-medium">"{offer.description}"</p>
                              {offer.human_dimensions && offer.human_dimensions.length > 0 && (
                                <div className="flex flex-wrap gap-1">
                                  {offer.human_dimensions.map((dim: string) => (
                                    <span key={dim} className="text-[8px] font-medium text-emerald-455 bg-emerald-500/5 px-1.5 py-0.2 rounded border border-emerald-500/10">
                                      {HUMAN_DIMENSIONS.find(d => d.value === dim)?.label || dim}
                                    </span>
                                  ))}
                                </div>
                              )}
                            </div>

                            <div className="flex items-center gap-1.5 shrink-0">
                              <button
                                onClick={() => handleEditSecondaryOffer(offer)}
                                className="p-1.5 hover:bg-slate-800 text-slate-400 hover:text-white rounded-lg transition-colors"
                                title="Editar"
                              >
                                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                                </svg>
                              </button>
                              <button
                                onClick={() => handleDeleteSecondaryOffer(offer.id)}
                                className="p-1.5 hover:bg-slate-800 text-rose-500 hover:text-rose-400 rounded-lg transition-colors"
                                title="Eliminar"
                              >
                                <Trash2 className="w-3.5 h-3.5" />
                              </button>
                            </div>
                          </div>
                        ))
                      )}
                    </div>

                  </div>

                </div>
              )}

            </div>

            {/* Modal Footer */}
            <div className="px-6 py-4 border-t border-slate-800 bg-slate-900 flex items-center justify-between">
              <div>
                <button
                  onClick={handleDeleteProfile}
                  className="px-4 py-2 border border-rose-500/30 text-rose-500 hover:bg-rose-500/10 rounded-xl text-xs font-black transition-all"
                >
                  Darme de baja de la Red
                </button>
              </div>
              <div className="flex gap-3">
                <button
                  onClick={() => setIsEditModalOpen(false)}
                  className="px-5 py-2.5 bg-slate-800 hover:bg-slate-705 text-white rounded-xl text-xs font-bold transition-all"
                >
                  Cancelar
                </button>
                <button
                  onClick={handleSaveProfile}
                  className="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 rounded-xl text-xs font-black transition-all shadow-md shadow-emerald-500/10"
                >
                  Guardar Cambios
                </button>
              </div>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}
