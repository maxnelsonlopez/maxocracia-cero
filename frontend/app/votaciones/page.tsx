"use client";

import React, { useCallback, useEffect, useState } from "react";
import {
  Vote,
  Plus,
  ShieldCheck,
  AlertTriangle,
  Clock,
  Hash,
  CheckCircle2,
  XCircle,
  Scale,
  Users,
  Loader2,
  RefreshCw,
  Cpu,
  Sparkles,
} from "lucide-react";
import { motion } from "framer-motion";
import { apiFetch } from "../lib/api";
import ParlamentoParams from "./ParlamentoParams";
import ParlamentoEducativo from "./ParlamentoEducativo";

interface Proposal {
  id: number;
  title: string;
  description: string;
  category: "operational" | "critical" | "emergency";
  options: string[];
  quorum_ratio: number;
  majority_ratio: number;
  status: "open" | "closed";
  result: string | null;
  result_detail: Record<string, unknown> | null;
  created_by: number;
  reason: string;
  deadline: string | null;
  closed_at: string | null;
  created_at: string;
  votes?: { user_id: number; option: string; created_at: string }[];
  oracle_analysis?: {
    analysis: {
      vhv: { vitalTime: number; affectedLives: number; finiteResources: number; timeFactor: number; totalScore: number; confidence: number };
      axiomReport: { type: "TRUTH" | "TIME" | "LIFE" | "RESOURCES"; passed: boolean; score: number; reasoning: string }[];
      oracleOpinions: { role: string; verdict: string; analysis: string; confidence: number }[];
      model: string;
      engine: string;
    };
    model: string;
    created_at: string;
    updated_at: string;
  } | null;
}

const CATEGORY_META: Record<string, { label: string; color: string; quorum: number; majority: number; hint: string }> = {
  operational: { label: "Operativa", color: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20", quorum: 0.5, majority: 0.5, hint: "Aspectos operativos cotidianos" },
  critical: { label: "Crítica", color: "bg-amber-500/10 text-amber-400 border-amber-500/20", quorum: 0.6, majority: 0.75, hint: "Consenso del 75% (Cap 14)" },
  emergency: { label: "Emergencia", color: "bg-red-500/10 text-red-400 border-red-500/20", quorum: 0.4, majority: 0.6, hint: "Veto vital / coherencia" },
};

export default function VotacionesPage() {
  const [proposals, setProposals] = useState<Proposal[]>([]);
  const [stats, setStats] = useState<{ total_proposals: number; open_proposals: number; passed_proposals: number; total_votes: number; audit: string } | null>(null);
  const [tab, setTab] = useState<"abiertas" | "cerradas">("abiertas");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [myVotes, setMyVotes] = useState<Record<number, string>>({});
  const [delegations, setDelegations] = useState<{ delegator_user_id: number; delegatee_user_id: number }[]>([]);
  const [delegateInput, setDelegateInput] = useState("");

  const loadDelegations = useCallback(async () => {
    try {
      const res = await apiFetch("/voting/delegations");
      if (res.ok) setDelegations(await res.json());
    } catch {
      // silencioso: la delegación es auxiliar
    }
  }, []);

  useEffect(() => {
    loadDelegations();
  }, [loadDelegations]);

  const setDelegation = async () => {
    const uid = parseInt(delegateInput);
    if (!uid) return;
    setError(null);
    const res = await apiFetch("/voting/delegations", {
      method: "POST",
      body: JSON.stringify({ delegatee_user_id: uid }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      setError(err.error || "Error al delegar");
      return;
    }
    setDelegateInput("");
    loadDelegations();
  };

  const revokeDelegation = async () => {
    await apiFetch("/voting/delegations", { method: "DELETE" });
    loadDelegations();
  };

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [p, s] = await Promise.all([
        apiFetch("/voting/proposals").then((r) => (r.ok ? r.json() : [])),
        apiFetch("/voting/stats").then((r) => (r.ok ? r.json() : null)),
      ]);
      setProposals(p);
      setStats(s);
    } catch {
      setError("No se pudieron cargar las votaciones (¿backend activo?).");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const castVote = async (proposalId: number, option: string) => {
    setError(null);
    const res = await apiFetch(`/voting/proposals/${proposalId}/vote`, {
      method: "POST",
      body: JSON.stringify({ option }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      setError(err.error || "Error al votar");
      return;
    }
    setMyVotes((prev) => ({ ...prev, [proposalId]: option }));
    load();
  };

  const closed = proposals.filter((p) => p.status === "closed");
  const open = proposals.filter((p) => p.status === "open");

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-6xl mx-auto px-4 py-10 space-y-8">
        {/* Encabezado */}
        <div className="bg-gradient-to-r from-emerald-900/20 to-slate-900/80 backdrop-blur border border-emerald-500/30 rounded-2xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold flex items-center gap-3">
              <Vote className="text-emerald-400" />
              Gobernanza Comunitaria
            </h1>
            <p className="text-sm text-emerald-400/80 font-mono mt-1">
              Consenso Diverso (Cap. 14) — la Cohorte Cero decide los aspectos operativos
            </p>
            {stats && (
              <div className="flex flex-wrap gap-4 mt-3 text-xs font-mono text-slate-400">
                <span className="flex items-center gap-1"><Scale className="w-3 h-3" /> {stats.total_proposals} propuestas</span>
                <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {stats.open_proposals} abiertas</span>
                <span className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3" /> {stats.passed_proposals} aprobadas</span>
                <span className="flex items-center gap-1"><Users className="w-3 h-3" /> {stats.total_votes} votos</span>
                <span className="flex items-center gap-1 text-slate-600"><Hash className="w-3 h-3" /> audit {stats.audit}</span>
              </div>
            )}
          </div>
          <div className="flex items-center gap-3">
            <button onClick={load} className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-400 hover:text-white transition-colors">
              <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            </button>
            <button
              onClick={() => setShowModal(true)}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold transition-all shadow-lg shadow-emerald-500/20"
            >
              <Plus className="w-4 h-4" />
              Nueva Propuesta
            </button>
          </div>
        </div>

        {/* Delegación de voto (democracia líquida, T13) */}
        <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <p className="text-xs font-bold text-slate-300 flex items-center gap-1.5">
              <Users className="w-3.5 h-3.5 text-emerald-400" />
              Delegación de voto (democracia líquida)
            </p>
            <p className="text-[10px] text-slate-500 mt-0.5">
              Si no votas, tu voto sigue la opción de tu delegatario. El voto directo siempre manda. Registro público (T13).
            </p>
          </div>
          <div className="flex items-center gap-2">
            {delegations.length > 0 ? (
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-mono text-slate-400">
                  Delegado: usuario #{delegations[0].delegatee_user_id}
                </span>
                <button onClick={revokeDelegation} className="px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase border border-red-500/30 text-red-400 hover:bg-red-500/10 transition-all">
                  Revocar
                </button>
              </div>
            ) : (
              <>
                <input
                  value={delegateInput}
                  onChange={(e) => setDelegateInput(e.target.value)}
                  placeholder="ID de usuario delegatario"
                  className="w-40 px-3 py-1.5 text-xs rounded-lg bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500 text-white font-mono placeholder:text-slate-600"
                />
                <button onClick={setDelegation} className="px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase border border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/10 transition-all">
                  Delegar
                </button>
              </>
            )}
          </div>
        </div>

        {/* Parlamento de Parámetros (Cap. 11: la comunidad ajusta α, β, γ, δ) */}
        <ParlamentoParams />

        {/* Parlamento Educativo (M9: la comunidad vota el umbral del puente años↔índice) */}
        <ParlamentoEducativo />

        {error && (
          <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-semibold flex items-center gap-2">
            <AlertTriangle className="w-4 h-4" /> {error}
          </div>
        )}

        {/* Tabs */}
        <div className="flex gap-2">
          {(["abiertas", "cerradas"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all border ${
                tab === t
                  ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
                  : "text-slate-500 border-slate-800 hover:text-slate-300"
              }`}
            >
              {t === "abiertas" ? `Abiertas (${open.length})` : `TruthLedger — Cerradas (${closed.length})`}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-24 text-slate-500">
            <Loader2 className="w-5 h-5 animate-spin mr-2" /> Consultando el Consenso...
          </div>
        ) : tab === "abiertas" ? (
          open.length === 0 ? (
            <EmptyState text="No hay propuestas abiertas. La comunidad espera tu iniciativa." />
          ) : (
            <div className="space-y-4">
              {open.map((p) => (
                <OpenProposalCard key={p.id} proposal={p} myVote={myVotes[p.id]} onVote={(opt) => castVote(p.id, opt)} />
              ))}
            </div>
          )
        ) : closed.length === 0 ? (
          <EmptyState text="El TruthLedger está vacío. Las decisiones aprobadas quedarán registradas aquí (T13)." />
        ) : (
          <div className="space-y-4">
            {closed.map((p) => (
              <ClosedProposalCard key={p.id} proposal={p} />
            ))}
          </div>
        )}
      </div>

      {showModal && <NewProposalModal onClose={() => setShowModal(false)} onCreated={() => { setShowModal(false); load(); }} />}
    </div>
  );
}

function EmptyState({ text }: { text: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-slate-500 space-y-3 bg-slate-900/50 rounded-2xl border border-slate-800 border-dashed">
      <Vote size={48} className="opacity-20" />
      <p className="text-sm">{text}</p>
    </div>
  );
}

function formatNum(n: number): string {
  return n >= 1000000 ? `${(n / 1000000).toFixed(1)}M` : n >= 1000 ? `${(n / 1000).toFixed(1)}k` : String(Math.round(n));
}

function formatBig(n: number): string {
  return n >= 1000000000 ? `${(n / 1000000000).toFixed(1)}B` : `${(n / 1000000).toFixed(1)}M`;
}

function Metric({ label, value, accent }: { label: string; value: string; accent?: boolean }) {
  return (
    <div className={`p-2.5 rounded-lg border ${accent ? "border-cyan-500/30 bg-cyan-500/5" : "border-slate-800 bg-slate-900/40"}`}>
      <p className="text-[9px] uppercase tracking-wider text-slate-500">{label}</p>
      <p className={`font-mono font-bold text-sm ${accent ? "text-cyan-400" : "text-slate-200"}`}>{value}</p>
    </div>
  );
}

function CategoryBadge({ category }: { category: Proposal["category"] }) {
  const meta = CATEGORY_META[category];
  return (
    <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider border ${meta.color}`}>
      {meta.label}
      {category === "critical" && " · 75%"}
    </span>
  );
}

function OpenProposalCard({ proposal: p, myVote, onVote }: { proposal: Proposal; myVote?: string; onVote: (opt: string) => void }) {
  const [detail, setDetail] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState<Proposal["oracle_analysis"] | undefined>(undefined);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const votes = p.votes || [];
  const counts: Record<string, number> = {};
  for (const v of votes) counts[v.option] = (counts[v.option] || 0) + 1;
  const totalVotes = votes.length;

  const runAnalysis = async () => {
    setAnalyzing(true);
    setAnalysisError(null);
    try {
      const res = await apiFetch(`/voting/proposals/${p.id}/analyze`, { method: "POST", body: "{}" });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error === "oracle_disabled" ? "Oráculo deshabilitado: configura DeepSeek o habilita el modelo local" : err.error || "Error del oráculo");
      }
      const data = await res.json();
      setAnalysis(data.oracle_analysis);
    } catch (e: unknown) {
      setAnalysisError(e instanceof Error ? e.message : "Error del oráculo");
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="bg-slate-900/50 border border-slate-800 hover:border-emerald-500/40 rounded-2xl p-5 transition-all">
      <div className="flex items-start justify-between gap-4">
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <CategoryBadge category={p.category} />
            <span className="text-[10px] font-mono text-slate-500">#{p.id} · vence {p.deadline ? new Date(p.deadline).toLocaleDateString() : "—"}</span>
          </div>
          <h3 className="text-lg font-bold text-slate-100">{p.title}</h3>
          <p className="text-xs text-slate-400 leading-relaxed max-w-3xl">{p.description}</p>
          {p.reason && <p className="text-[10px] text-slate-500 italic">Motivo: {p.reason}</p>}
        </div>
        <button onClick={() => setDetail(!detail)} className="text-xs text-emerald-400 font-bold uppercase tracking-wider hover:text-emerald-300 shrink-0">
          {detail ? "Ocultar" : "Detalle (T13)"}
        </button>
      </div>

      <div className="mt-4 space-y-2.5">
        {p.options.map((opt) => {
          const n = counts[opt] || 0;
          const pct = totalVotes ? (n / totalVotes) * 100 : 0;
          const voted = myVote === opt;
          return (
            <div key={opt} className="flex items-center gap-3">
              <button
                onClick={() => onVote(opt)}
                disabled={!!myVote}
                className={`w-24 shrink-0 px-3 py-2 rounded-lg text-xs font-bold border transition-all ${
                  voted
                    ? "bg-emerald-500 text-slate-950 border-emerald-500"
                    : myVote
                    ? "bg-slate-950 text-slate-600 border-slate-800 cursor-not-allowed"
                    : "bg-slate-950 text-emerald-400 border-emerald-500/30 hover:bg-emerald-500/10"
                }`}
              >
                {voted ? "✓ Votado" : "Votar"}
              </button>
              <div className="flex-1">
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-300 font-medium">{opt}</span>
                  <span className="font-mono text-slate-500">{n} votos · {pct.toFixed(0)}%</span>
                </div>
                <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div className={`h-full rounded-full transition-all ${voted ? "bg-emerald-500" : "bg-emerald-500/40"}`} style={{ width: `${pct}%` }} />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-[10px] font-mono text-slate-500">
        <span>Quórum: {totalVotes} votos emitidos</span>
        <span className="flex items-center gap-3">
          <button
            onClick={runAnalysis}
            disabled={analyzing}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase tracking-wider border transition-all ${
              analysis
                ? "text-slate-500 border-slate-800 cursor-default"
                : "text-cyan-400 border-cyan-500/30 hover:bg-cyan-500/10"
            }`}
          >
            {analyzing ? <Loader2 className="w-3 h-3 animate-spin" /> : <Cpu className="w-3 h-3" />}
            {analysis ? "Analizada" : "Analizar con Oráculo"}
          </button>
          Mayoría: {(p.majority_ratio * 100).toFixed(0)}% · Quórum: {(p.quorum_ratio * 100).toFixed(0)}%
        </span>
      </div>

      {analysisError && <p className="mt-2 text-[10px] text-red-400 font-semibold">{analysisError}</p>}

      {analysis && (
        <div className="mt-4 p-4 bg-slate-950/60 border border-cyan-500/20 rounded-xl space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-[10px] font-black uppercase tracking-widest text-cyan-400 flex items-center gap-1.5">
              <Sparkles className="w-3 h-3" /> Informe del Oráculo Sintético
            </p>
            <span className={`px-2 py-0.5 rounded-full text-[9px] font-bold uppercase border ${
              analysis.analysis.engine === "deepseek"
                ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                : "bg-cyan-500/10 text-cyan-400 border-cyan-500/20"
            }`}>
              {analysis.analysis.engine === "deepseek" ? "Nube · DeepSeek" : "Local · Hub"}
            </span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
            <Metric label="TV (horas)" value={formatNum(analysis.analysis.vhv.vitalTime)} />
            <Metric label="VA (vidas)" value={formatNum(analysis.analysis.vhv.affectedLives)} />
            <Metric label="RF (0-1000)" value={formatNum(analysis.analysis.vhv.finiteResources)} />
            <Metric label="T-Factor" value={analysis.analysis.vhv.timeFactor.toFixed(1)} />
            <Metric label="VHV total" value={formatBig(analysis.analysis.vhv.totalScore)} accent />
          </div>

          <div className="flex flex-wrap gap-2">
            {analysis.analysis.axiomReport.map((a) => (
              <span
                key={a.type}
                title={a.reasoning}
                className={`px-2.5 py-1 rounded-lg text-[10px] font-bold border ${
                  a.passed
                    ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                    : "bg-red-500/10 text-red-400 border-red-500/20"
                }`}
              >
                {a.type} {a.score}/100 {a.passed ? "✓" : "✗"}
              </span>
            ))}
          </div>

          <div className="space-y-2">
            {analysis.analysis.oracleOpinions.map((o) => (
              <div key={o.role} className="flex items-start justify-between gap-3 text-xs">
                <div>
                  <p className="font-bold text-slate-300">{o.role}</p>
                  <p className="text-[10px] text-slate-500 leading-relaxed">{o.analysis}</p>
                </div>
                <span className={`shrink-0 px-2 py-0.5 rounded-full text-[9px] font-bold uppercase border ${
                  o.verdict === "Approve"
                    ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                    : o.verdict === "Reject"
                    ? "bg-red-500/10 text-red-400 border-red-500/20"
                    : "bg-amber-500/10 text-amber-400 border-amber-500/20"
                }`}>
                  {o.verdict} · {(o.confidence * 100).toFixed(0)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {detail && (
        <div className="mt-4 p-4 bg-slate-950/60 border border-slate-800 rounded-xl space-y-2">
          <p className="text-[10px] font-black uppercase tracking-widest text-slate-500">Registro público de votos (T13)</p>
          {votes.length === 0 ? (
            <p className="text-xs text-slate-600">Sin votos aún.</p>
          ) : (
            votes.map((v, i) => (
              <div key={i} className="flex justify-between text-xs font-mono">
                <span className="text-slate-400">usuario #{v.user_id}</span>
                <span className="text-emerald-400">{v.option}</span>
                <span className="text-slate-600">{new Date(v.created_at).toLocaleString()}</span>
              </div>
            ))
          )}
        </div>
      )}
    </motion.div>
  );
}

function ClosedProposalCard({ proposal: p }: { proposal: Proposal }) {
  const detail = p.result_detail as Record<string, unknown> | null;
  const passed = p.result === "passed";
  const votes = p.votes || [];
  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="bg-slate-900/90 border border-slate-800 hover:border-emerald-500/50 rounded-2xl p-5 transition-all relative overflow-hidden">
      <div className="absolute top-0 left-0 w-1 h-full bg-emerald-600" />
      <div className="flex flex-col md:flex-row justify-between items-start gap-4">
        <div>
          <div className="flex items-center gap-3">
            <CategoryBadge category={p.category} />
            {passed ? (
              <span className="flex items-center gap-1 text-emerald-400 text-[10px] font-bold uppercase"><CheckCircle2 className="w-3.5 h-3.5" /> Aprobada</span>
            ) : (
              <span className="flex items-center gap-1 text-red-400 text-[10px] font-bold uppercase"><XCircle className="w-3.5 h-3.5" /> {p.result === "quorum_not_met" ? "Sin quórum" : "Rechazada"}</span>
            )}
          </div>
          <h3 className="text-lg font-bold text-slate-200 mt-2">{p.title}</h3>
          <p className="text-xs text-slate-500 mt-1">{p.description}</p>
          <div className="flex items-center gap-4 mt-3 text-xs font-mono text-slate-500">
            <span className="flex items-center gap-1"><Users className="w-3 h-3" /> {votes.length} votos</span>
            {detail && typeof detail.quorum_actual === "number" && (
              <span className="flex items-center gap-1"><Scale className="w-3 h-3" /> quórum {(detail.quorum_actual as number * 100).toFixed(0)}%</span>
            )}
            {detail && typeof detail.winner === "string" && (
              <span className="flex items-center gap-1 text-emerald-400"><CheckCircle2 className="w-3 h-3" /> ganadora: {detail.winner}</span>
            )}
            {detail && typeof detail.weighted_fraction === "number" && detail.weighted_fraction !== detail.winner_fraction && (
              <span className="flex items-center gap-1 text-amber-400" title="Participación Inteligente (Cap. 14): el peso del voto crece con el TVI registrado">
                <Sparkles className="w-3 h-3" /> consenso ponderado {(detail.weighted_fraction as number * 100).toFixed(0)}%
              </span>
            )}
            <span className="flex items-center gap-1 text-slate-600"><Hash className="w-3 h-3" /> {p.closed_at ? new Date(p.closed_at).toLocaleDateString() : "—"}</span>
          </div>
        </div>
        <div className="text-right shrink-0">
          <p className="text-[10px] uppercase text-slate-500">Detalle de resultado</p>
          <pre className="text-[10px] font-mono text-emerald-400/80 bg-slate-950 p-2 rounded-lg mt-1 max-w-xs overflow-x-auto">
            {detail ? JSON.stringify(detail, null, 1) : "—"}
          </pre>
        </div>
      </div>
    </motion.div>
  );
}

function NewProposalModal({ onClose, onCreated }: { onClose: () => void; onCreated: () => void }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState<Proposal["category"]>("operational");
  const [options, setOptions] = useState<string[]>(["Si", "No"]);
  const [reason, setReason] = useState("");
  const [deadlineHours, setDeadlineHours] = useState(72);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async () => {
    setSaving(true);
    setError(null);
    try {
      const res = await apiFetch("/voting/proposals", {
        method: "POST",
        body: JSON.stringify({ title, description, category, options: options.filter((o) => o.trim()), reason, deadline_hours: deadlineHours }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error || "Error al crear la propuesta");
      }
      onCreated();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Error al crear");
      setSaving(false);
    }
  };

  const meta = CATEGORY_META[category];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4" onClick={onClose}>
      <motion.div
        initial={{ opacity: 0, scale: 0.96 }}
        animate={{ opacity: 1, scale: 1 }}
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-2xl bg-slate-900 border border-emerald-500/20 rounded-2xl p-6 space-y-5 max-h-[90vh] overflow-y-auto"
      >
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold flex items-center gap-2">
            <ShieldCheck className="text-emerald-400" />
            Nueva Propuesta Comunitaria
          </h2>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">×</button>
        </div>

        <div className="space-y-2">
          <label className="text-xs font-semibold text-slate-300">Título</label>
          <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="¿Qué decide la comunidad?" className="w-full px-3 py-2.5 text-sm rounded-xl bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500 text-white" />
        </div>

        <div className="space-y-2">
          <label className="text-xs font-semibold text-slate-300">Descripción</label>
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={3} placeholder="Contexto, impacto y fundamento axiomático..." className="w-full px-3 py-2.5 text-sm rounded-xl bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500 text-white" />
        </div>

        <div className="space-y-2">
          <label className="text-xs font-semibold text-slate-300">Categoría (define quórum y mayoría)</label>
          <div className="grid grid-cols-3 gap-2">
            {(Object.keys(CATEGORY_META) as Proposal["category"][]).map((c) => (
              <button
                key={c}
                onClick={() => setCategory(c)}
                className={`p-3 rounded-xl border text-left transition-all ${
                  category === c ? "border-emerald-500/50 bg-emerald-500/10" : "border-slate-800 hover:border-slate-600"
                }`}
              >
                <span className={`inline-block px-2 py-0.5 rounded-full text-[9px] font-bold uppercase border ${CATEGORY_META[c].color}`}>{CATEGORY_META[c].label}</span>
                <p className="text-[10px] text-slate-500 mt-1.5">{CATEGORY_META[c].hint}</p>
                <p className="text-[10px] font-mono text-emerald-400 mt-0.5">quórum {(CATEGORY_META[c].quorum * 100).toFixed(0)}% · mayoría {(CATEGORY_META[c].majority * 100).toFixed(0)}%</p>
              </button>
            ))}
          </div>
          <p className="text-[10px] text-slate-500">{meta.hint} — el consenso crítico requiere 75% (Cap 14).</p>
        </div>

        <div className="space-y-2">
          <label className="text-xs font-semibold text-slate-300">Opciones (2-8)</label>
          {options.map((opt, i) => (
            <div key={i} className="flex gap-2">
              <input
                value={opt}
                onChange={(e) => setOptions(options.map((o, j) => (j === i ? e.target.value : o)))}
                className="flex-1 px-3 py-2 text-sm rounded-xl bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500 text-white"
              />
              {options.length > 2 && (
                <button onClick={() => setOptions(options.filter((_, j) => j !== i))} className="px-3 rounded-xl border border-slate-800 text-slate-500 hover:text-red-400">×</button>
              )}
            </div>
          ))}
          {options.length < 8 && (
            <button onClick={() => setOptions([...options, ""])} className="text-xs text-emerald-400 font-bold hover:text-emerald-300">+ Añadir opción</button>
          )}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-300">Plazo (horas)</label>
            <input type="number" value={deadlineHours} min={1} max={720} onChange={(e) => setDeadlineHours(parseInt(e.target.value) || 72)} className="w-full px-3 py-2.5 text-sm rounded-xl bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500 text-white font-mono" />
          </div>
          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-300">Motivo (auditable, T13)</label>
            <input value={reason} onChange={(e) => setReason(e.target.value)} placeholder="¿Por qué ahora?" className="w-full px-3 py-2.5 text-sm rounded-xl bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500 text-white" />
          </div>
        </div>

        {error && <p className="text-xs text-red-400 font-semibold">{error}</p>}

        <div className="flex justify-end gap-3 pt-2">
          <button onClick={onClose} className="px-5 py-2.5 rounded-xl border border-slate-800 text-slate-400 hover:text-white text-sm">Cancelar</button>
          <button
            onClick={submit}
            disabled={saving || !title.trim() || !description.trim() || options.filter((o) => o.trim()).length < 2}
            className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-sm disabled:opacity-40 transition-all"
          >
            {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Vote className="w-4 h-4" />}
            Someter a la Comunidad
          </button>
        </div>
      </motion.div>
    </div>
  );
}
