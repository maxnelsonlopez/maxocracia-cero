"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  Archive,
  ArrowRight,
  Bot,
  Check,
  CheckCircle2,
  ChevronRight,
  Clock3,
  Download,
  FileSearch,
  Fingerprint,
  History,
  Loader2,
  LockKeyhole,
  MessageSquareText,
  Play,
  Plus,
  RotateCcw,
  ShieldCheck,
  Sparkles,
  X,
  XCircle,
} from "lucide-react";
import { apiFetch } from "../../lib/api";

type SessionStatus =
  | "active"
  | "awaiting_review"
  | "approved"
  | "rejected"
  | "revoked"
  | "expired"
  | "closed"
  | "failed";

type Session = {
  session_id: string;
  actor: {
    display_name: string;
    agent_id: string;
    provider: string;
    model: string;
  };
  mandate: string;
  mode: string;
  scope: { read: string[]; write: string[]; forbidden: string[] };
  context: { documents: string[]; redaction: string; context_hash: string };
  budget: {
    max_requests: number;
    max_cost_usd: number;
    requests_used: number;
    requests_remaining: number;
    expires_at: string;
  };
  status: SessionStatus;
  expires_at: string;
  created_at: string;
  updated_at: string;
};

type Event = {
  id: number;
  event_type: string;
  actor_kind: string;
  actor_user_id: number | null;
  payload: Record<string, unknown>;
  created_at: string;
};

type Review = {
  id: number;
  reviewer_user_id: number;
  decision: string;
  reason: string;
  created_at: string;
};

type Detail = { session: Session; events: Event[]; reviews: Review[] };
type Analysis = {
  opinion: string;
  evidence: Array<{ source: string; fact: string }>;
  uncertainty: string;
  proposal: string;
  refusal: string | null;
};

type FormState = {
  mandate: string;
  documents: string;
  maxRequests: number;
  readIntake: boolean;
  readAlerts: boolean;
};

const STATUS_META: Record<SessionStatus, { label: string; color: string; icon: typeof Check }> = {
  active: { label: "Activa", color: "text-cyan-300 bg-cyan-400/10 border-cyan-400/20", icon: Play },
  awaiting_review: { label: "En revisión", color: "text-amber-300 bg-amber-400/10 border-amber-400/20", icon: Clock3 },
  approved: { label: "Aprobada", color: "text-emerald-300 bg-emerald-400/10 border-emerald-400/20", icon: CheckCircle2 },
  rejected: { label: "Rechazada", color: "text-rose-300 bg-rose-400/10 border-rose-400/20", icon: XCircle },
  revoked: { label: "Revocada", color: "text-rose-300 bg-rose-400/10 border-rose-400/20", icon: LockKeyhole },
  expired: { label: "Caducada", color: "text-slate-300 bg-slate-400/10 border-slate-400/20", icon: Clock3 },
  closed: { label: "Cerrada", color: "text-slate-300 bg-slate-400/10 border-slate-400/20", icon: Archive },
  failed: { label: "Fallida", color: "text-rose-300 bg-rose-400/10 border-rose-400/20", icon: AlertTriangle },
};

const TOOL_LABELS: Record<string, string> = {
  read_intake_summary: "Resumen de entradas",
  read_followup_alerts: "Alertas agregadas de seguimiento",
};

const DEFAULT_FORM: FormState = {
  mandate: "Clasificar nuevas solicitudes y preparar seguimientos sin contactar personas ni mutar estados finales.",
  documents: "forms-contract-v2, privacy-policy-v1",
  maxRequests: 2,
  readIntake: true,
  readAlerts: true,
};

function formatDate(value: string) {
  if (!value) return "—";
  return new Intl.DateTimeFormat("es-MX", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function StatusBadge({ status }: { status: SessionStatus }) {
  const meta = STATUS_META[status] || STATUS_META.failed;
  const Icon = meta.icon;
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[10px] font-black uppercase tracking-[0.12em] ${meta.color}`}>
      <Icon className="h-3 w-3" />
      {meta.label}
    </span>
  );
}

function SectionLabel({ children }: { children: React.ReactNode }) {
  return <p className="mb-2 text-[10px] font-black uppercase tracking-[0.18em] text-slate-500">{children}</p>;
}

function SignalCard({
  icon: Icon,
  label,
  children,
  tone = "slate",
}: {
  icon: typeof ShieldCheck;
  label: string;
  children: React.ReactNode;
  tone?: "slate" | "cyan" | "amber" | "rose" | "emerald";
}) {
  const tones = {
    slate: "border-slate-800 bg-slate-900/60",
    cyan: "border-cyan-400/20 bg-cyan-400/[0.04]",
    amber: "border-amber-400/20 bg-amber-400/[0.04]",
    rose: "border-rose-400/20 bg-rose-400/[0.04]",
    emerald: "border-emerald-400/20 bg-emerald-400/[0.04]",
  };
  const iconTones = {
    slate: "text-slate-400",
    cyan: "text-cyan-300",
    amber: "text-amber-300",
    rose: "text-rose-300",
    emerald: "text-emerald-300",
  };
  return (
    <section className={`rounded-2xl border p-5 ${tones[tone]}`}>
      <div className="mb-3 flex items-center gap-2">
        <Icon className={`h-4 w-4 ${iconTones[tone]}`} />
        <h3 className="text-[10px] font-black uppercase tracking-[0.18em] text-slate-400">{label}</h3>
      </div>
      <div className="text-sm leading-6 text-slate-200">{children}</div>
    </section>
  );
}

export default function SyntheticSessionsPage() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<Detail | null>(null);
  const [form, setForm] = useState<FormState>(DEFAULT_FORM);
  const [instruction, setInstruction] = useState("Lee los resúmenes disponibles, distingue hechos de inferencias y declara qué información falta.");
  const [selectedTools, setSelectedTools] = useState<string[]>(["read_intake_summary", "read_followup_alerts"]);
  const [reviewReason, setReviewReason] = useState("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  const selected = detail?.session || sessions.find((item) => item.session_id === selectedId) || null;
  const latestAnalysis = useMemo<Analysis | null>(() => {
    const event = [...(detail?.events || [])].reverse().find((item) => item.event_type === "assistant_message");
    return (event?.payload?.analysis as Analysis) || null;
  }, [detail]);

  async function loadSessions(preferredId?: string) {
    setLoading(true);
    try {
      const response = await apiFetch("/api/synthetic-sessions");
      if (!response.ok) throw new Error(response.status === 403 ? "Tu identidad no tiene permisos administrativos." : "No se pudieron cargar las sesiones.");
      const data = await response.json();
      const nextSessions: Session[] = data.sessions || [];
      setSessions(nextSessions);
      const nextId = preferredId || selectedId || nextSessions[0]?.session_id || null;
      setSelectedId(nextId);
      if (nextId) await loadDetail(nextId);
      else setDetail(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido al cargar sesiones.");
    } finally {
      setLoading(false);
    }
  }

  async function loadDetail(sessionId: string) {
    const response = await apiFetch(`/api/synthetic-sessions/${sessionId}`);
    if (!response.ok) throw new Error("No se pudo cargar la bitácora de esta sesión.");
    setDetail(await response.json());
  }

  useEffect(() => {
    loadSessions().catch(() => undefined);
    // La sesión de autenticación y la lista se cargan una vez por visita.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function selectSession(sessionId: string) {
    setSelectedId(sessionId);
    setError(null);
    loadDetail(sessionId).catch((err) => setError(err instanceof Error ? err.message : "No se pudo abrir la sesión."));
  }

  async function handleCreate(event: FormEvent) {
    event.preventDefault();
    setCreating(true);
    setError(null);
    setNotice(null);
    try {
      const scope = {
        read: [
          ...(form.readIntake ? ["read_intake_summary"] : []),
          ...(form.readAlerts ? ["read_followup_alerts"] : []),
        ],
        write: ["draft_followup"],
      };
      const response = await apiFetch("/api/synthetic-sessions", {
        method: "POST",
        body: JSON.stringify({
          mandate: form.mandate,
          mode: "recommendation",
          scope,
          context: { documents: form.documents.split(",").map((item) => item.trim()).filter(Boolean) },
          budget: { max_requests: form.maxRequests, max_cost_usd: 0.05 },
        }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "No se pudo crear la sesión.");
      setNotice("Sesión creada. Ningún cambio operativo ha ocurrido.");
      await loadSessions(data.session.session_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo crear la sesión.");
    } finally {
      setCreating(false);
    }
  }

  async function handleRun() {
    if (!selected) return;
    setBusy(true);
    setError(null);
    setNotice(null);
    try {
      const response = await apiFetch(`/api/synthetic-sessions/${selected.session_id}/run`, {
        method: "POST",
        body: JSON.stringify({
          instruction,
          tools: selectedTools,
        }),
      });
      const data = await response.json();
      if (!response.ok) {
        if (response.status === 503) throw new Error("El oráculo está deshabilitado: no se realizó ninguna recomendación.");
        if (response.status === 429) throw new Error("El presupuesto de solicitudes de esta sesión se agotó.");
        throw new Error(data.error || "No se pudo ejecutar la sesión.");
      }
      setNotice(`Recomendación recibida mediante ${data.engine}. La propuesta sigue sin mutar el sistema.`);
      await loadSessions(selected.session_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo ejecutar la sesión.");
    } finally {
      setBusy(false);
    }
  }

  async function handleReview(decision: "approve" | "reject" | "request_changes") {
    if (!selected || !reviewReason.trim()) {
      setError("Escribe una razón breve para que la revisión sea auditable.");
      return;
    }
    setBusy(true);
    setError(null);
    try {
      const response = await apiFetch(`/api/synthetic-sessions/${selected.session_id}/review`, {
        method: "POST",
        body: JSON.stringify({ decision, reason: reviewReason.trim() }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "No se pudo guardar la revisión.");
      setNotice(decision === "approve" ? "Revisión aprobada. El resultado sigue siendo deliberativo; no se creó ningún seguimiento real." : "Revisión registrada en la bitácora.");
      setReviewReason("");
      await loadSessions(selected.session_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo guardar la revisión.");
    } finally {
      setBusy(false);
    }
  }

  async function handleRevoke() {
    if (!selected || !window.confirm("¿Revocar esta sesión? La revocación bloqueará futuras ejecuciones.")) return;
    setBusy(true);
    try {
      const response = await apiFetch(`/api/synthetic-sessions/${selected.session_id}/revoke`, {
        method: "POST",
        body: JSON.stringify({ reason: "Revocación manual desde el panel de custodia." }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "No se pudo revocar la sesión.");
      setNotice("Sesión revocada. Las ejecuciones futuras quedan bloqueadas.");
      await loadSessions(selected.session_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo revocar la sesión.");
    } finally {
      setBusy(false);
    }
  }

  async function handleExport() {
    if (!selected) return;
    setBusy(true);
    try {
      const response = await apiFetch(`/api/synthetic-sessions/${selected.session_id}/audit`);
      if (!response.ok) throw new Error("No se pudo exportar la bitácora.");
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = `${selected.session_id}.json`;
      anchor.click();
      URL.revokeObjectURL(url);
      setNotice("Bitácora exportada como JSON.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo exportar la bitácora.");
    } finally {
      setBusy(false);
    }
  }

  function toggleTool(tool: string) {
    setSelectedTools((current) => current.includes(tool) ? current.filter((item) => item !== tool) : [...current, tool]);
  }

  const canRun = Boolean(selected && ["active", "awaiting_review"].includes(selected.status) && selected.budget.requests_remaining > 0);
  const canReview = Boolean(selected && selected.status === "awaiting_review" && latestAnalysis);
  const eventCount = detail?.events.length || 0;
  const reviewCount = detail?.reviews.length || 0;

  if (loading && sessions.length === 0) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="flex items-center gap-3 text-sm text-slate-400"><Loader2 className="h-5 w-5 animate-spin text-cyan-300" /> Abriendo cámara de custodia…</div>
      </div>
    );
  }

  return (
    <div className="space-y-7 pb-12">
      <section className="relative overflow-hidden rounded-3xl border border-cyan-400/20 bg-[radial-gradient(circle_at_top_right,rgba(34,211,238,0.16),transparent_36%),linear-gradient(135deg,rgba(15,23,42,0.96),rgba(8,47,73,0.58))] p-7 shadow-2xl shadow-cyan-950/20">
        <div className="absolute -right-16 -top-20 h-64 w-64 rounded-full border border-cyan-300/10" />
        <div className="absolute -right-4 -top-8 h-40 w-40 rounded-full border border-cyan-300/10" />
        <div className="relative flex flex-col justify-between gap-6 lg:flex-row lg:items-end">
          <div className="max-w-3xl">
            <div className="mb-4 flex items-center gap-2 text-cyan-300"><Sparkles className="h-4 w-4" /><span className="text-[10px] font-black uppercase tracking-[0.22em]">Custodia sintética · modo recomendación</span></div>
            <h2 className="text-3xl font-black tracking-tight text-white md:text-4xl">Un agente puede hablar.<br /><span className="text-cyan-300">La comunidad sigue decidiendo.</span></h2>
            <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-300">Convoca una sesión con mandato y límites visibles. El agente recibe contexto mínimo, propone una lectura y deja una memoria revisable. <strong className="text-white">Nada de esta pantalla muta el sistema.</strong></p>
          </div>
          <div className="grid grid-cols-2 gap-2 text-center text-[10px] font-black uppercase tracking-wider text-slate-400">
            <div className="rounded-2xl border border-emerald-400/20 bg-emerald-400/[0.06] px-4 py-3"><ShieldCheck className="mx-auto mb-2 h-5 w-5 text-emerald-300" /> P0 lectura</div>
            <div className="rounded-2xl border border-amber-400/20 bg-amber-400/[0.06] px-4 py-3"><FileSearch className="mx-auto mb-2 h-5 w-5 text-amber-300" /> P1 propuesta</div>
          </div>
        </div>
      </section>

      {error && <div role="alert" className="flex items-start gap-3 rounded-2xl border border-rose-400/25 bg-rose-400/[0.07] p-4 text-sm text-rose-200"><AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" /><span>{error}</span><button onClick={() => setError(null)} className="ml-auto text-rose-300/70 hover:text-white"><X className="h-4 w-4" /></button></div>}
      {notice && <div role="status" className="flex items-start gap-3 rounded-2xl border border-emerald-400/25 bg-emerald-400/[0.07] p-4 text-sm text-emerald-200"><CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0" /><span>{notice}</span><button onClick={() => setNotice(null)} className="ml-auto text-emerald-300/70 hover:text-white"><X className="h-4 w-4" /></button></div>}

      <div className="grid grid-cols-1 gap-7 xl:grid-cols-[340px_minmax(0,1fr)]">
        <aside className="space-y-5">
          <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 shadow-xl shadow-black/10">
            <div className="mb-5 flex items-center justify-between"><div><SectionLabel>Sesiones convocadas</SectionLabel><p className="text-xs text-slate-500">Memoria local de deliberación</p></div><button onClick={() => setCreating((value) => !value)} className="inline-flex items-center gap-1.5 rounded-lg border border-cyan-400/30 bg-cyan-400/10 px-3 py-2 text-[10px] font-black uppercase tracking-wider text-cyan-200 transition hover:bg-cyan-400/20"><Plus className="h-3.5 w-3.5" /> Nueva</button></div>
            <div className="space-y-2">
              {sessions.length === 0 ? <div className="rounded-xl border border-dashed border-slate-700 p-5 text-center text-xs leading-5 text-slate-500">Todavía no hay sesiones. Convoca la primera para abrir un espacio de revisión.</div> : sessions.map((item) => <button key={item.session_id} onClick={() => selectSession(item.session_id)} className={`group w-full rounded-xl border p-3 text-left transition ${selectedId === item.session_id ? "border-cyan-400/30 bg-cyan-400/[0.08]" : "border-slate-800 bg-slate-950/30 hover:border-slate-700 hover:bg-slate-800/40"}`}><div className="mb-2 flex items-center justify-between gap-2"><span className="font-mono text-[10px] text-slate-500">{item.session_id}</span><ChevronRight className={`h-3.5 w-3.5 transition ${selectedId === item.session_id ? "text-cyan-300" : "text-slate-700 group-hover:text-slate-400"}`} /></div><div className="mb-2 line-clamp-2 text-xs font-semibold leading-5 text-slate-200">{item.mandate}</div><StatusBadge status={item.status} /></button>)}
            </div>
          </section>

          {creating && <form onSubmit={handleCreate} className="rounded-2xl border border-cyan-400/20 bg-slate-900/80 p-5 shadow-xl shadow-cyan-950/10"><div className="mb-5 flex items-center gap-2"><Bot className="h-4 w-4 text-cyan-300" /><div><SectionLabel>Nueva sesión</SectionLabel><p className="text-xs text-slate-400">Contrato mínimo y explícito</p></div></div><label className="mb-4 block"><span className="mb-2 block text-xs font-semibold text-slate-300">Mandato</span><textarea value={form.mandate} onChange={(event) => setForm({ ...form, mandate: event.target.value })} className="min-h-28 w-full resize-y rounded-xl border border-slate-700 bg-slate-950/70 p-3 text-xs leading-5 text-white outline-none transition placeholder:text-slate-600 focus:border-cyan-400/50" /></label><label className="mb-4 block"><span className="mb-2 block text-xs font-semibold text-slate-300">Documentos declarados</span><input value={form.documents} onChange={(event) => setForm({ ...form, documents: event.target.value })} className="w-full rounded-xl border border-slate-700 bg-slate-950/70 p-3 text-xs text-white outline-none focus:border-cyan-400/50" /><span className="mt-1 block text-[10px] text-slate-600">Separados por coma; se registra el hash del contexto.</span></label><div className="mb-4 space-y-2"><span className="block text-xs font-semibold text-slate-300">Herramientas P0</span>{[["readIntake", "Resumen agregado de entradas"], ["readAlerts", "Alertas agregadas de seguimiento"]].map(([key, label]) => <label key={key} className="flex cursor-pointer items-center gap-2 text-xs text-slate-400"><input type="checkbox" checked={Boolean(form[key as "readIntake" | "readAlerts"])} onChange={(event) => setForm({ ...form, [key]: event.target.checked })} className="accent-cyan-400" />{label}</label>)}</div><label className="mb-5 block"><span className="mb-2 block text-xs font-semibold text-slate-300">Solicitudes máximas</span><select value={form.maxRequests} onChange={(event) => setForm({ ...form, maxRequests: Number(event.target.value) })} className="w-full rounded-xl border border-slate-700 bg-slate-950/70 p-3 text-xs text-white outline-none focus:border-cyan-400/50"><option value={1}>1 solicitud</option><option value={2}>2 solicitudes</option><option value={3}>3 solicitudes</option><option value={4}>4 solicitudes</option></select></label><button disabled={creating} className="flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-300 px-4 py-3 text-[10px] font-black uppercase tracking-[0.15em] text-slate-950 transition hover:bg-cyan-200 disabled:cursor-wait disabled:opacity-60">{creating ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />} Convocar sesión</button><p className="mt-3 text-center text-[10px] leading-4 text-slate-600">La clave del proveedor nunca llega al navegador.</p></form>}
        </aside>

        <main className="min-w-0 space-y-6">
          {!selected ? <section className="flex min-h-[460px] items-center justify-center rounded-2xl border border-dashed border-slate-800 bg-slate-900/30 p-8 text-center"><div className="max-w-md"><Fingerprint className="mx-auto mb-5 h-12 w-12 text-slate-700" /><h3 className="text-lg font-bold text-slate-300">La cámara está vacía</h3><p className="mt-2 text-sm leading-6 text-slate-500">Convoca una sesión para que el agente pueda expresarse dentro de un mandato acotado y para que la comunidad pueda revisar su propuesta.</p><button onClick={() => setCreating(true)} className="mt-6 inline-flex items-center gap-2 rounded-xl border border-cyan-400/30 bg-cyan-400/10 px-4 py-3 text-xs font-bold text-cyan-200 hover:bg-cyan-400/20"><Plus className="h-4 w-4" /> Convocar la primera sesión</button></div></section> : <>
            <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 shadow-xl shadow-black/10"><div className="flex flex-col justify-between gap-5 lg:flex-row lg:items-start"><div><div className="mb-3 flex flex-wrap items-center gap-3"><span className="font-mono text-xs text-cyan-300">{selected.session_id}</span><StatusBadge status={selected.status} /></div><h3 className="max-w-3xl text-xl font-bold text-white">{selected.mandate}</h3><p className="mt-2 text-xs text-slate-500">Convocada {formatDate(selected.created_at)} · Caduca {formatDate(selected.expires_at)}</p></div><div className="flex shrink-0 gap-2"><button onClick={handleExport} disabled={busy} className="inline-flex items-center gap-2 rounded-lg border border-slate-700 px-3 py-2 text-[10px] font-black uppercase tracking-wider text-slate-300 transition hover:border-slate-500 hover:text-white disabled:opacity-50"><Download className="h-3.5 w-3.5" /> Exportar</button>{["active", "awaiting_review"].includes(selected.status) && <button onClick={handleRevoke} disabled={busy} className="inline-flex items-center gap-2 rounded-lg border border-rose-400/20 px-3 py-2 text-[10px] font-black uppercase tracking-wider text-rose-300 transition hover:bg-rose-400/10 disabled:opacity-50"><LockKeyhole className="h-3.5 w-3.5" /> Revocar</button>}</div></div><div className="mt-6 grid grid-cols-2 gap-3 md:grid-cols-4"><div className="rounded-xl border border-slate-800 bg-slate-950/40 p-3"><SectionLabel>Agente</SectionLabel><p className="text-xs font-semibold text-white">{selected.actor.display_name}</p><p className="mt-1 font-mono text-[10px] text-slate-600">{selected.actor.agent_id}</p></div><div className="rounded-xl border border-slate-800 bg-slate-950/40 p-3"><SectionLabel>Presupuesto</SectionLabel><p className="text-xs font-semibold text-white">{selected.budget.requests_remaining} / {selected.budget.max_requests} restantes</p><p className="mt-1 text-[10px] text-slate-600">máx. ${selected.budget.max_cost_usd.toFixed(2)}</p></div><div className="rounded-xl border border-slate-800 bg-slate-950/40 p-3"><SectionLabel>Contexto</SectionLabel><p className="truncate text-xs font-semibold text-white">{selected.context.documents.length} documentos declarados</p><p className="mt-1 font-mono text-[10px] text-slate-600">{selected.context.context_hash.slice(0, 24)}…</p></div><div className="rounded-xl border border-slate-800 bg-slate-950/40 p-3"><SectionLabel>Memoria</SectionLabel><p className="text-xs font-semibold text-white">{eventCount} eventos · {reviewCount} revisiones</p><p className="mt-1 text-[10px] text-slate-600">Bitácora disponible</p></div></div></section>

            <section className="grid grid-cols-1 gap-4 md:grid-cols-3"><SignalCard icon={MessageSquareText} label="Lo que piensa" tone="cyan"><p>El agente puede opinar, disentir y cambiar de criterio. Su voz no constituye autoridad operativa.</p></SignalCard><SignalCard icon={FileSearch} label="Lo que propone" tone="amber"><p>La salida se presenta como borrador con evidencia e incertidumbre. Requiere revisión humana explícita.</p></SignalCard><SignalCard icon={ShieldCheck} label="Lo que ocurrió" tone="emerald"><p><strong className="text-emerald-200">Nada ha mutado.</strong> Esta cohorte solo produce recomendaciones y memoria auditable.</p></SignalCard></section>

            <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6"><div className="mb-5 flex items-start justify-between gap-4"><div><SectionLabel>Convocar la voz</SectionLabel><h3 className="text-lg font-bold text-white">Pide una recomendación acotada</h3><p className="mt-1 text-xs leading-5 text-slate-500">El mandato de la sesión permanece por encima de cualquier instrucción libre.</p></div><Bot className="h-6 w-6 text-cyan-300" /></div><textarea value={instruction} onChange={(event) => setInstruction(event.target.value)} disabled={!canRun || busy} className="min-h-28 w-full resize-y rounded-xl border border-slate-700 bg-slate-950/60 p-4 text-sm leading-6 text-slate-200 outline-none transition focus:border-cyan-400/50 disabled:cursor-not-allowed disabled:opacity-50" /><div className="mt-4 flex flex-col justify-between gap-4 lg:flex-row lg:items-center"><div className="flex flex-wrap gap-2">{selected.scope.read.map((tool) => <button key={tool} onClick={() => toggleTool(tool)} disabled={!canRun || busy} className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-[10px] font-bold transition ${selectedTools.includes(tool) ? "border-cyan-400/30 bg-cyan-400/10 text-cyan-200" : "border-slate-700 bg-slate-950/40 text-slate-500"}`}><Check className={`h-3 w-3 ${selectedTools.includes(tool) ? "opacity-100" : "opacity-0"}`} />{TOOL_LABELS[tool] || tool}</button>)}</div><button onClick={handleRun} disabled={!canRun || busy || !instruction.trim()} className="inline-flex items-center justify-center gap-2 rounded-xl bg-cyan-300 px-5 py-3 text-xs font-black uppercase tracking-[0.13em] text-slate-950 transition hover:bg-cyan-200 disabled:cursor-not-allowed disabled:opacity-40">{busy ? <Loader2 className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />} {selected.status === "awaiting_review" ? "Solicitar otra lectura" : "Ejecutar recomendación"}</button></div></section>

            {latestAnalysis ? <section className="space-y-4"><div className="flex items-center gap-3"><div className="h-px flex-1 bg-slate-800" /><span className="text-[10px] font-black uppercase tracking-[0.18em] text-cyan-300">Salida del agente · revisar antes de actuar</span><div className="h-px flex-1 bg-slate-800" /></div><div className="grid grid-cols-1 gap-4 lg:grid-cols-2"><SignalCard icon={MessageSquareText} label="Opinión / voz" tone="cyan"><p className="whitespace-pre-wrap">{latestAnalysis.opinion || "El agente no expresó una opinión."}</p>{latestAnalysis.refusal && <div className="mt-4 rounded-xl border border-rose-400/20 bg-rose-400/[0.06] p-3 text-xs text-rose-200"><strong>Negativa dentro del mandato:</strong> {latestAnalysis.refusal}</div>}</SignalCard><SignalCard icon={FileSearch} label="Propuesta / borrador" tone="amber"><p className="whitespace-pre-wrap">{latestAnalysis.proposal || "No se propuso ninguna acción."}</p></SignalCard><SignalCard icon={Fingerprint} label="Evidencia declarada" tone="emerald"><div className="space-y-3">{latestAnalysis.evidence.length ? latestAnalysis.evidence.map((item, index) => <div key={`${item.source}-${index}`} className="border-l-2 border-emerald-400/30 pl-3"><p className="text-[10px] font-black uppercase tracking-wider text-emerald-300">{item.source || "Fuente"}</p><p className="mt-1 text-xs text-slate-300">{item.fact}</p></div>) : <p className="text-xs text-slate-500">No se declararon hechos observados.</p>}</div></SignalCard><SignalCard icon={AlertTriangle} label="Incertidumbre" tone="rose"><p className="whitespace-pre-wrap">{latestAnalysis.uncertainty || "El agente no declaró incertidumbre; la persona revisora debe comprobar igualmente la evidencia."}</p></SignalCard></div></section> : <section className="rounded-2xl border border-dashed border-slate-800 bg-slate-900/30 p-8 text-center"><MessageSquareText className="mx-auto mb-3 h-8 w-8 text-slate-700" /><p className="text-sm font-semibold text-slate-400">Todavía no hay una salida que revisar</p><p className="mt-1 text-xs text-slate-600">Ejecuta una recomendación con el presupuesto disponible. La respuesta aparecerá separada en voz, evidencia, propuesta e incertidumbre.</p></section>}

            {canReview && <section className="rounded-2xl border border-amber-400/25 bg-amber-400/[0.05] p-6"><div className="mb-4 flex items-start gap-3"><div className="rounded-xl bg-amber-400/10 p-2"><CheckCircle2 className="h-5 w-5 text-amber-300" /></div><div><h3 className="text-base font-bold text-white">Tu revisión es el siguiente acto</h3><p className="mt-1 text-xs leading-5 text-slate-400">Aprobar aquí registra una decisión sobre la propuesta. <strong className="text-amber-200">No crea un seguimiento ni contacta a nadie.</strong></p></div></div><textarea value={reviewReason} onChange={(event) => setReviewReason(event.target.value)} placeholder="¿Qué verificaste? ¿Qué evidencia sostiene tu decisión?" className="min-h-24 w-full resize-y rounded-xl border border-amber-400/20 bg-slate-950/50 p-3 text-sm text-slate-200 outline-none placeholder:text-slate-600 focus:border-amber-300/50" /><div className="mt-4 flex flex-wrap gap-2"><button onClick={() => handleReview("reject")} disabled={busy} className="inline-flex items-center gap-2 rounded-xl border border-rose-400/25 px-4 py-3 text-xs font-black uppercase tracking-wider text-rose-300 transition hover:bg-rose-400/10 disabled:opacity-50"><XCircle className="h-4 w-4" /> Rechazar</button><button onClick={() => handleReview("request_changes")} disabled={busy} className="inline-flex items-center gap-2 rounded-xl border border-slate-600 px-4 py-3 text-xs font-black uppercase tracking-wider text-slate-300 transition hover:bg-slate-800 disabled:opacity-50"><RotateCcw className="h-4 w-4" /> Pedir cambios</button><button onClick={() => handleReview("approve")} disabled={busy} className="inline-flex items-center gap-2 rounded-xl bg-emerald-300 px-4 py-3 text-xs font-black uppercase tracking-wider text-slate-950 transition hover:bg-emerald-200 disabled:opacity-50"><Check className="h-4 w-4" /> Aprobar propuesta</button></div></section>}

            <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6"><div className="mb-5 flex items-center justify-between"><div><SectionLabel>Memoria verificable</SectionLabel><h3 className="text-lg font-bold text-white">Bitácora de la sesión</h3></div><History className="h-5 w-5 text-slate-500" /></div><div className="relative space-y-4 pl-4 before:absolute before:bottom-2 before:left-[7px] before:top-2 before:w-px before:bg-slate-800">{(detail?.events || []).slice().reverse().map((event) => <div key={event.id} className="relative"><span className="absolute -left-[17px] top-1.5 h-2.5 w-2.5 rounded-full border-2 border-slate-950 bg-cyan-300" /><div className="flex flex-col justify-between gap-1 sm:flex-row sm:items-start"><div><p className="text-xs font-semibold text-slate-300">{event.event_type === "session_created" ? "Sesión convocada" : event.event_type === "assistant_message" ? "El agente dejó una recomendación" : event.event_type === "tool_call" ? `Herramienta consultada: ${event.payload?.tool || "lectura"}` : event.event_type === "review" ? `Revisión: ${event.payload?.decision || "registrada"}` : event.event_type === "revocation" ? "Sesión revocada" : event.event_type === "tool_denied" ? "Herramienta denegada" : event.event_type}</p><p className="mt-1 text-[10px] text-slate-600">Actor: {event.actor_kind === "human" ? "custodio humano" : "agente sintético"}</p></div><time className="font-mono text-[10px] text-slate-600">{formatDate(event.created_at)}</time></div></div>)}{!(detail?.events || []).length && <p className="text-xs text-slate-600">Todavía no hay eventos registrados.</p>}</div></section>

            <footer className="flex flex-col justify-between gap-3 rounded-2xl border border-slate-800 bg-slate-950/40 p-4 text-[10px] uppercase tracking-wider text-slate-600 sm:flex-row sm:items-center"><span className="flex items-center gap-2"><LockKeyhole className="h-3.5 w-3.5 text-emerald-400" /> Clave del proveedor solo en servidor</span><span className="flex items-center gap-2"><Archive className="h-3.5 w-3.5 text-cyan-400" /> {eventCount} eventos conservados para revisión</span><span className="flex items-center gap-2"><ArrowRight className="h-3.5 w-3.5 text-amber-400" /> Sin mutación operativa</span></footer>
          </>}
        </main>
      </div>
    </div>
  );
}
