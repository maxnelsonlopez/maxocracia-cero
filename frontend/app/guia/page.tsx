"use client";

import React, { useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Sparkles,
  Send,
  Loader2,
  AlertTriangle,
  ShieldCheck,
  User,
  Footprints,
  FileCheck2,
  Clock3,
  Star,
  FileText,
  Cpu,
  Scale,
  Compass,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { apiFetch } from "../lib/api";

const TRUST_LEVELS: Record<number, { label: string; color: string; hint: string }> = {
  0: { label: "N0 · Recién llegado", color: "bg-slate-500/10 text-slate-300 border-slate-500/30", hint: "Todos empiezan aquí: la voz se gana caminando el primer acuerdo." },
  1: { label: "N1 · Miembro con voz", color: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30", hint: "Tu voz cuenta en la gobernanza de la Cohorte (Cap. 15)." },
  2: { label: "N2 · Guardián", color: "bg-violet-500/10 text-violet-400 border-violet-500/30", hint: "Custodias el sentido del proyecto (Cap. 14.9)." },
};

interface Evidence {
  trust_level: number;
  contracts_created: number;
  contracts_signed: number;
  tvi_hours: number;
  reputation_score: number;
  reputation_reviews: number;
  has_cero_form: boolean;
}

interface TrustAssessment {
  ethic?: number;
  attitude?: number;
  aptitude?: number;
  suggested_trust_level?: number;
  reasoning?: string;
  honest_limits?: string;
  engine?: string;
  evidence?: Evidence;
}

interface DirectorAssessment {
  eligible?: boolean;
  ethic?: number;
  attitude?: number;
  aptitude?: number;
  reasoning?: string;
  honest_limits?: string;
  engine?: string;
  evidence?: Evidence;
  hint?: string;
}

interface ChatMsg {
  role: "user" | "guide";
  content: string;
  engine?: string;
}

const TABS: { id: "chat" | "evaluacion" | "candidatura"; label: string; icon: React.ElementType }[] = [
  { id: "chat", label: "Chat con el Guía", icon: Sparkles },
  { id: "evaluacion", label: "Mi evaluación", icon: Footprints },
  { id: "candidatura", label: "Candidatura a director", icon: ShieldCheck },
];

export default function GuiaPage() {
  const { isAuthenticated, isLoading } = useAuth();
  const [tab, setTab] = useState<"chat" | "evaluacion" | "candidatura">("chat");

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-violet-400" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="max-w-md w-full glass rounded-2xl border border-slate-800 p-8 text-center">
          <Compass className="w-12 h-12 text-violet-400 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-white mb-2">Guía de la Maxocracia</h1>
          <p className="text-slate-400 mb-6">
            El oráculo que recibe a los recién llegados: orientación, tu escalera de confianza
            y la evaluación de tu candidatura. Inicia sesión para hablar con el Guía.
          </p>
          <Link
            href="/login"
            className="inline-block px-6 py-3 rounded-xl bg-violet-500 text-white font-bold hover:bg-violet-600 transition-all"
          >
            Entrar
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-5xl mx-auto px-4 py-10 space-y-8">
        {/* Encabezado */}
        <div className="bg-gradient-to-r from-violet-900/20 to-slate-900/80 backdrop-blur border border-violet-500/30 rounded-2xl p-6">
          <h1 className="text-2xl font-bold flex items-center gap-3">
            <Compass className="text-violet-400" />
            Guía de la Maxocracia
          </h1>
          <p className="text-sm text-violet-400/80 font-mono mt-1">
            Cap. 13/15 — la voz que recibe a los recién llegados a la Cohorte Cero
          </p>
          <p className="text-xs text-slate-400 mt-2 max-w-2xl">
            Los oráculos sintéticos procesan, los humanos custodian el sentido. Pregunta, conoce tu
            lugar en la escalera de confianza y —si es tu vocación— presenta tu candidatura a director.
          </p>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 flex-wrap">
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all border ${
                tab === t.id
                  ? "bg-violet-500/10 text-violet-400 border-violet-500/30"
                  : "text-slate-500 border-slate-800 hover:text-slate-300"
              }`}
            >
              <t.icon className="w-3.5 h-3.5" />
              {t.label}
            </button>
          ))}
        </div>

        {tab === "chat" && <ChatTab />}
        {tab === "evaluacion" && <EvaluationTab />}
        {tab === "candidatura" && <CandidacyTab />}
      </div>
    </div>
  );
}

/* ============================ Pestaña 1: Chat ============================ */

function ChatTab() {
  const [messages, setMessages] = useState<ChatMsg[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const send = async () => {
    const text = input.trim();
    if (!text || sending) return;
    setError(null);
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setInput("");
    setSending(true);
    try {
      const res = await apiFetch("/guide/chat", { method: "POST", body: JSON.stringify({ message: text }) });
      const data = await res.json().catch(() => ({}));
      if (res.status === 503) {
        throw new Error(data.hint || "Oráculo deshabilitado");
      }
      if (!res.ok) {
        throw new Error(data.error || data.detail || "Error del oráculo");
      }
      setMessages((prev) => [...prev, { role: "guide", content: data.reply, engine: data.engine }]);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Error al hablar con el guía");
    } finally {
      setSending(false);
    }
  };

  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
      <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-4 flex flex-col max-h-[55vh] min-h-[320px]">
        {messages.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center text-slate-500 space-y-3 py-10">
            <Sparkles size={40} className="opacity-20" />
            <p className="text-sm max-w-sm text-center">
              Pregúntale al Guía: cómo empezar, qué es el TVI, cómo caminar tu primer acuerdo,
              qué significa la escalera de confianza...
            </p>
          </div>
        ) : (
          <div className="flex-1 space-y-3 overflow-y-auto pr-1">
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-[85%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                    m.role === "user"
                      ? "bg-violet-500/20 border border-violet-500/30 text-violet-100"
                      : "bg-slate-950 border border-slate-800 text-slate-300"
                  }`}
                >
                  <p className="whitespace-pre-wrap">{m.content}</p>
                  {m.role === "guide" && (
                    <div className="mt-2 flex items-center justify-between">
                      <span className="text-[9px] font-bold uppercase tracking-widest text-slate-500">
                        Guía de la Maxocracia
                      </span>
                      <EngineBadge engine={m.engine} />
                    </div>
                  )}
                </div>
              </div>
            ))}
            {sending && (
              <div className="flex justify-start">
                <div className="px-4 py-3 rounded-2xl bg-slate-950 border border-slate-800 flex items-center gap-2 text-xs text-slate-500">
                  <Loader2 className="w-3.5 h-3.5 animate-spin" /> El Guía está reflexionando...
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {error && (
        <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-semibold flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 shrink-0" /> {error}
        </div>
      )}

      <div className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Escribe tu pregunta al Guía..."
          className="flex-1 px-4 py-3 text-sm rounded-xl bg-slate-900/60 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-violet-500 text-white placeholder:text-slate-600"
        />
        <button
          onClick={send}
          disabled={sending || !input.trim()}
          className="flex items-center gap-2 px-5 py-3 rounded-xl bg-violet-500 hover:bg-violet-400 text-slate-950 font-semibold text-sm disabled:opacity-40 transition-all"
        >
          {sending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
          Enviar
        </button>
      </div>
    </motion.div>
  );
}

/* ========================= Pestaña 2: Evaluación ========================= */

function EvaluationTab() {
  const [statement, setStatement] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<TrustAssessment | null>(null);

  const evaluate = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await apiFetch("/guide/trust-assessment", {
        method: "POST",
        body: JSON.stringify({ statement: statement.trim() }),
      });
      const data = await res.json().catch(() => ({}));
      if (res.status === 503) {
        throw new Error(data.hint || "Oráculo deshabilitado");
      }
      if (!res.ok) {
        throw new Error(data.error || data.detail || "Error del oráculo");
      }
      setResult(data.assessment);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Error al evaluarte");
    } finally {
      setLoading(false);
    }
  };

  const level = result?.suggested_trust_level ?? 0;
  const levelMeta = TRUST_LEVELS[level] || TRUST_LEVELS[0];

  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
      <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-5 space-y-3">
        <p className="text-xs font-bold text-slate-300 flex items-center gap-1.5">
          <Footprints className="w-3.5 h-3.5 text-violet-400" />
          La escalera de confianza (Cap. 13/15)
        </p>
        <textarea
          value={statement}
          onChange={(e) => setStatement(e.target.value)}
          rows={3}
          placeholder="Cuéntale al Guía quién eres y qué buscas en la Cohorte (opcional, la evidencia T13 también cuenta)..."
          className="w-full px-3 py-2.5 text-sm rounded-xl bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-violet-500 text-white placeholder:text-slate-600"
        />
        <button
          onClick={evaluate}
          disabled={loading}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-violet-500 hover:bg-violet-400 text-slate-950 font-semibold text-sm disabled:opacity-40 transition-all"
        >
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Footprints className="w-4 h-4" />}
          Evaluarme
        </button>
        {error && (
          <p className="text-xs text-red-400 font-semibold flex items-center gap-1.5">
            <AlertTriangle className="w-3.5 h-3.5 shrink-0" /> {error}
          </p>
        )}
      </div>

      {result && (
        <div className="bg-slate-900/50 border border-violet-500/20 rounded-2xl p-5 space-y-5">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <span className={`px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider border ${levelMeta.color}`}>
                {levelMeta.label}
              </span>
              <p className="text-[10px] text-slate-500 max-w-xs">{levelMeta.hint}</p>
            </div>
            <EngineBadge engine={result.engine} />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <ScoreBar label="Ética" value={result.ethic ?? 0} color="bg-emerald-500" />
            <ScoreBar label="Actitud" value={result.attitude ?? 0} color="bg-amber-500" />
            <ScoreBar label="Aptitud" value={result.aptitude ?? 0} color="bg-violet-500" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl">
              <p className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-1.5">Razonamiento</p>
              <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap">{result.reasoning || "—"}</p>
            </div>
            <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl">
              <p className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-1.5">Límites honestos</p>
              <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap">{result.honest_limits || "—"}</p>
            </div>
          </div>

          {result.evidence && (
            <div className="space-y-2">
              <p className="text-[10px] font-black uppercase tracking-widest text-slate-500">
                Evidencia registrada (T13)
              </p>
              <EvidenceGrid evidence={result.evidence} />
            </div>
          )}
        </div>
      )}
    </motion.div>
  );
}

/* ====================== Pestaña 3: Candidatura ====================== */

function CandidacyTab() {
  const [statement, setStatement] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<DirectorAssessment | null>(null);

  const submit = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await apiFetch("/guide/director-candidacy", {
        method: "POST",
        body: JSON.stringify({ statement: statement.trim() }),
      });
      const data = await res.json().catch(() => ({}));
      if (res.status === 503) {
        throw new Error(data.hint || "Oráculo deshabilitado");
      }
      if (!res.ok) {
        throw new Error(data.error || data.detail || "Error del oráculo");
      }
      setResult(data.assessment);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Error al enviar la candidatura");
    } finally {
      setLoading(false);
    }
  };

  const eligible = !!result?.eligible;

  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
      <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-5 space-y-3">
        <p className="text-xs font-bold text-slate-300 flex items-center gap-1.5">
          <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
          Candidatura a director (Cap. 14.9)
        </p>
        <p className="text-[10px] text-slate-500">
          Ser director no es un privilegio sino una custodia. El Guía filtra con criterios éticos,
          de actitud y aptitud; la comunidad decide. Presenta tu declaración: por qué quieres custodiar.
        </p>
        <textarea
          value={statement}
          onChange={(e) => setStatement(e.target.value)}
          rows={4}
          placeholder="Declaración del candidato: ¿por qué quieres custodiar el sentido del proyecto?"
          className="w-full px-3 py-2.5 text-sm rounded-xl bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-amber-500 text-white placeholder:text-slate-600"
        />
        <button
          onClick={submit}
          disabled={loading || !statement.trim()}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold text-sm disabled:opacity-40 transition-all"
        >
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <ShieldCheck className="w-4 h-4" />}
          Enviar candidatura
        </button>
        {error && (
          <p className="text-xs text-red-400 font-semibold flex items-center gap-1.5">
            <AlertTriangle className="w-3.5 h-3.5 shrink-0" /> {error}
          </p>
        )}
      </div>

      {result && (
        <div className="bg-slate-900/50 border border-amber-500/20 rounded-2xl p-5 space-y-5">
          <div className="flex flex-wrap items-center justify-between gap-3">
            {eligible ? (
              <span className="flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider border bg-emerald-500/10 text-emerald-400 border-emerald-500/30">
                <ShieldCheck className="w-3.5 h-3.5" /> Elegible
              </span>
            ) : (
              <span className="flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider border bg-slate-500/10 text-slate-300 border-slate-500/30">
                No elegible · la escalera es un camino
              </span>
            )}
            <EngineBadge engine={result.engine} />
          </div>

          {!eligible && (
            <p className="text-xs text-amber-400/90 leading-relaxed">
              No es un cierre: el Guía recomienda, la comunidad decide. La escalera de confianza se
              camina con acciones verificables: firma contratos, registra TVI, gana reputación y
              vuelve a intentarlo cuando la evidencia hable.
            </p>
          )}

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <ScoreBar label="Ética" value={result.ethic ?? 0} color="bg-emerald-500" />
            <ScoreBar label="Actitud" value={result.attitude ?? 0} color="bg-amber-500" />
            <ScoreBar label="Aptitud" value={result.aptitude ?? 0} color="bg-violet-500" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl">
              <p className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-1.5">Razonamiento</p>
              <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap">{result.reasoning || "—"}</p>
            </div>
            <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl">
              <p className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-1.5">Límites honestos</p>
              <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap">{result.honest_limits || "—"}</p>
            </div>
          </div>

          <div className="p-4 bg-amber-500/5 border border-amber-500/20 rounded-xl flex items-start gap-2">
            <Scale className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <p className="text-xs text-amber-300/90 leading-relaxed">
              {result.hint || "El Guía recomienda, la comunidad decide: crea una propuesta critical (Cap. 14)."}
            </p>
          </div>

          {result.evidence && (
            <div className="space-y-2">
              <p className="text-[10px] font-black uppercase tracking-widest text-slate-500">
                Evidencia registrada (T13)
              </p>
              <EvidenceGrid evidence={result.evidence} />
            </div>
          )}
        </div>
      )}
    </motion.div>
  );
}

/* ========================= Componentes comunes ========================= */

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  const v = Math.max(0, Math.min(100, value));
  return (
    <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl">
      <div className="flex justify-between text-xs mb-2">
        <span className="text-slate-300 font-medium">{label}</span>
        <span className="font-mono text-slate-400">{Math.round(v)}/100</span>
      </div>
      <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full transition-all ${color}`} style={{ width: `${v}%` }} />
      </div>
    </div>
  );
}

function EvidenceGrid({ evidence }: { evidence: Evidence }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
      <EvidenceCard icon={<FileText className="w-3.5 h-3.5 text-violet-400" />} label="Contratos creados" value={String(evidence.contracts_created)} />
      <EvidenceCard icon={<FileCheck2 className="w-3.5 h-3.5 text-emerald-400" />} label="Contratos firmados" value={String(evidence.contracts_signed)} />
      <EvidenceCard icon={<Clock3 className="w-3.5 h-3.5 text-cyan-400" />} label="TVI registrado" value={`${evidence.tvi_hours} h`} />
      <EvidenceCard icon={<Star className="w-3.5 h-3.5 text-amber-400" />} label="Reputación" value={`${evidence.reputation_score} (${evidence.reputation_reviews} reseñas)`} />
      <EvidenceCard icon={<Scale className="w-3.5 h-3.5 text-slate-400" />} label="Nivel actual" value={`N${evidence.trust_level}`} />
      <EvidenceCard
        icon={<User className="w-3.5 h-3.5 text-emerald-400" />}
        label="Formulario CERO"
        value={evidence.has_cero_form ? "Completado" : "Pendiente"}
        accent={evidence.has_cero_form ? "text-emerald-400" : "text-slate-400"}
      />
    </div>
  );
}

function EvidenceCard({ icon, label, value, accent }: { icon: React.ReactNode; label: string; value: string; accent?: string }) {
  return (
    <div className="p-3 rounded-lg border border-slate-800 bg-slate-950/60 flex items-center gap-3">
      <div className="w-8 h-8 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-center shrink-0">{icon}</div>
      <div className="min-w-0">
        <p className="text-[9px] uppercase tracking-wider text-slate-500 truncate">{label}</p>
        <p className={`font-mono font-bold text-sm ${accent || "text-slate-200"}`}>{value}</p>
      </div>
    </div>
  );
}

function EngineBadge({ engine }: { engine?: string }) {
  if (!engine) return null;
  const cloud = engine === "deepseek";
  return (
    <span className={`px-2 py-0.5 rounded-full text-[9px] font-bold uppercase border ${
      cloud
        ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
        : "bg-cyan-500/10 text-cyan-400 border-cyan-500/20"
    }`}>
      <Cpu className="w-2.5 h-2.5 inline mr-1" />
      {cloud ? "Nube · DeepSeek" : "Local · Hub"}
    </span>
  );
}
