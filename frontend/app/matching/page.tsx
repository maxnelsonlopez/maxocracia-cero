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
  Bot
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
                {urgentNeeds.map((need, idx) => (
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
                  </div>
                ))}
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
    </div>
  );
}
