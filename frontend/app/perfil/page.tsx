"use client";

import React, { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import {
  Coins,
  ShieldCheck,
  Star,
  Boxes,
  Handshake,
  ArrowUpRight,
  ArrowDownLeft,
  Send,
  Plus,
  Loader2,
  AlertTriangle,
  User,
  GraduationCap,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { apiFetch } from "../lib/api";
import InfoTip from "../components/ui/InfoTip";

interface EduEvent {
  id: number;
  topic_slug: string;
  branch_slug: string;
  score: number | null;
  mentor_rounds: number;
  triada_approved: boolean;
  verified_at: string;
  t13_hash: string;
}

interface LedgerEntry {
  id: number;
  change_amount: number;
  reason: string | null;
  created_at: string;
}

interface ProtectionProfile {
  user_id: number;
  level: "standard" | "assisted" | "shielded";
  companion_user_id: number | null;
  declared_age: number | null;
  declared_education: string | null;
}

interface ProtectionCaps {
  contract_hours: number | null;
  weekly_hours: number | null;
  reflection_hours: number;
  requires_paraphrase: boolean;
  requires_oracle_review: boolean;
  requires_witness: boolean;
  oracle_required_for_creation: boolean;
}

interface ResourceItem {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  category: string | null;
  available: boolean;
  created_at: string;
}

interface Interchange {
  id: number;
  interchange_id: string | null;
  date: string | null;
  giver_id: number | null;
  receiver_id: number | null;
  type: string | null;
  description: string | null;
  uth_hours: number | null;
  uvc_score: number | null;
  impact_resolution_score: number | null;
  created_at: string;
}

const LEVEL_META: Record<string, { label: string; color: string; hint: string }> = {
  standard: { label: "Estándar", color: "bg-slate-500/10 text-slate-300 border-slate-500/30", hint: "Sin protecciones adicionales" },
  assisted: { label: "Asistido", color: "bg-amber-500/10 text-amber-400 border-amber-500/30", hint: "Paráfrasis oracular, revisión pre-firma, enfriamiento 24h" },
  shielded: { label: "Blindado", color: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30", hint: "Todo lo anterior + co-testigo humano, enfriamiento 72h" },
};

function fmtAmount(v: number) {
  return v.toLocaleString("es-ES", { maximumFractionDigits: 4 });
}

export default function PerfilPage() {
  const { user, isAuthenticated, isLoading } = useAuth();

  const [balance, setBalance] = useState<number | null>(null);
  const [ledger, setLedger] = useState<LedgerEntry[]>([]);
  const [protection, setProtection] = useState<{
    profile: ProtectionProfile;
    protection_level: string;
    caps: ProtectionCaps;
  } | null>(null);
  const [reputation, setReputation] = useState<{ score: number; reviews_count: number } | null>(null);
  const [resources, setResources] = useState<ResourceItem[]>([]);
  const [interchanges, setInterchanges] = useState<Interchange[]>([]);
  const [eduEvents, setEduEvents] = useState<EduEvent[]>([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [showTransfer, setShowTransfer] = useState(false);
  const [transferForm, setTransferForm] = useState({ to_user_id: "", amount: "", reason: "" });
  const [transferMsg, setTransferMsg] = useState<string | null>(null);

  const [showResource, setShowResource] = useState(false);
  const [resourceForm, setResourceForm] = useState({ title: "", description: "", category: "" });
  const [resourceMsg, setResourceMsg] = useState<string | null>(null);

  const [protectForm, setProtectForm] = useState({ level: "standard", companion_user_id: "", declared_age: "" });
  const [protectMsg, setProtectMsg] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!user) return;
    setLoading(true);
    setError(null);
    try {
      const [bal, led, prot, rep, res] = await Promise.all([
        apiFetch(`/maxo/${user.id}/balance`),
        apiFetch(`/maxo/${user.id}/ledger`),
        apiFetch("/protection/profile"),
        apiFetch(`/reputation/${user.id}`),
        apiFetch("/resources"),
      ]);
      if (bal.ok) setBalance((await bal.json()).balance);
      if (led.ok) {
        const d = await led.json();
        setLedger(d.entries || []);
      }
      if (prot.ok) setProtection(await prot.json());
      if (rep.ok) setReputation(await rep.json());
      if (res.ok) setResources(await res.json());
    } catch {
      setError("No se pudieron cargar algunos datos (¿backend activo?).");
    } finally {
      setLoading(false);
    }
  }, [user]);

  const loadInterchanges = useCallback(async () => {
    if (!user) return;
    try {
      const res = await apiFetch("/interchanges");
      if (res.ok) {
        const all: Interchange[] = await res.json();
        setInterchanges(all.filter((i) => i.giver_id === user.id || i.receiver_id === user.id));
      }
    } catch {
      // silencioso: los intercambios son auxiliares
    }
  }, [user]);

  useEffect(() => {
    load();
    loadInterchanges();
    // Evidencia educativa sincronizada desde el nodo del OEV (T13).
    apiFetch("/edu-bridge/events")
      .then(async (res) => {
        if (res.ok) {
          const data = await res.json();
          setEduEvents(data.events || []);
        }
      })
      .catch(() => setEduEvents([]));
  }, [load, loadInterchanges]);

  const doTransfer = async () => {
    if (!user) return;
    setTransferMsg(null);
    const to_id = parseInt(transferForm.to_user_id);
    const amount = parseFloat(transferForm.amount);
    if (!to_id || !amount || amount <= 0) {
      setTransferMsg("Indica un destinatario (id) y un monto positivo.");
      return;
    }
    const res = await apiFetch("/maxo/transfer", {
      method: "POST",
      body: JSON.stringify({ from_user_id: user.id, to_user_id: to_id, amount, reason: transferForm.reason }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      setTransferMsg(data.error || "Error en la transferencia.");
      return;
    }
    setTransferMsg(`Transferencia exitosa. Nuevo saldo: ${fmtAmount(data.new_balance)} Maxos.`);
    setTransferForm({ to_user_id: "", amount: "", reason: "" });
    load();
  };

  const doCreateResource = async () => {
    if (!user) return;
    setResourceMsg(null);
    if (!resourceForm.title.trim()) {
      setResourceMsg("El título del recurso es obligatorio.");
      return;
    }
    const res = await apiFetch("/resources", {
      method: "POST",
      body: JSON.stringify({ user_id: user.id, ...resourceForm }),
    });
    if (!res.ok) {
      setResourceMsg("Error al crear el recurso.");
      return;
    }
    setResourceMsg("Recurso ofrecido a la comunidad.");
    setResourceForm({ title: "", description: "", category: "" });
    load();
  };

  const doClaimResource = async (resId: number) => {
    if (!user) return;
    const res = await apiFetch(`/resources/${resId}/claim`, {
      method: "POST",
      body: JSON.stringify({ requester_id: user.id }),
    });
    if (res.ok) load();
  };

  const doSaveProtection = async () => {
    if (!user) return;
    setProtectMsg(null);
    const body: Record<string, unknown> = { level: protectForm.level };
    if (protectForm.companion_user_id.trim()) body.companion_user_id = parseInt(protectForm.companion_user_id);
    if (protectForm.declared_age.trim()) body.declared_age = parseInt(protectForm.declared_age);
    const res = await apiFetch("/protection/profile", { method: "POST", body: JSON.stringify(body) });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      setProtectMsg(data.error || "Error al guardar el perfil de protección.");
      return;
    }
    setProtectMsg("Perfil de protección actualizado.");
    load();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-emerald-400" />
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="max-w-md w-full glass rounded-2xl border border-slate-800 p-8 text-center">
          <User className="w-12 h-12 text-emerald-400 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-white mb-2">Perfil Vital</h1>
          <p className="text-slate-400 mb-6">
            Inicia sesión para ver tu saldo Maxo, protección, reputación y recursos de la comunidad.
          </p>
          <Link
            href="/login"
            className="inline-block px-6 py-3 rounded-xl bg-emerald-500 text-white font-bold hover:bg-emerald-600 transition-all"
          >
            Entrar
          </Link>
        </div>
      </div>
    );
  }

  const caps = protection?.caps;
  const myLevel = (protection?.protection_level || "standard") as keyof typeof LEVEL_META;
  const levelMeta = LEVEL_META[myLevel] || LEVEL_META.standard;

  return (
    <div className="min-h-screen max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white">Perfil Vital</h1>
          <p className="text-slate-400 mt-1">
            La contabilidad de tu vida: saldo, salvaguardas y comunidad (T13).
          </p>
        </div>
        {error && (
          <div className="flex items-center gap-2 text-amber-400 text-sm bg-amber-500/10 border border-amber-500/20 rounded-lg px-3 py-2">
            <AlertTriangle className="w-4 h-4" />
            {error}
          </div>
        )}
      </div>

      <div className="glass rounded-2xl border border-slate-800 p-6 mb-8 flex items-center gap-4">
        <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-2xl font-black text-white">
          {(user.alias || user.name || "?").charAt(0).toUpperCase()}
        </div>
        <div>
          <h2 className="text-xl font-bold text-white">{user.alias || user.name}</h2>
          <p className="text-sm text-slate-400">{user.email} · usuario #{user.id}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="glass rounded-2xl border border-slate-800 p-6 lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h3 className="flex items-center gap-2 font-bold text-white">
              <Coins className="w-5 h-5 text-emerald-400" />
              Saldo Maxo
            </h3>
            <button
              onClick={() => { setShowTransfer(!showTransfer); setTransferMsg(null); }}
              className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold bg-emerald-500 text-white hover:bg-emerald-600 transition-all active:scale-95"
            >
              <Send className="w-4 h-4" />
              Transferir
            </button>
          </div>

          {loading ? (
            <div className="flex items-center gap-2 text-slate-400 py-4">
              <Loader2 className="w-4 h-4 animate-spin" /> Cargando saldo...
            </div>
          ) : (
            <p className="text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-300 mb-4">
              {balance === null ? "—" : fmtAmount(balance)}
              <span className="text-lg font-bold text-slate-400 ml-2">Maxos</span>
            </p>
          )}

          {showTransfer && (
            <div className="glass rounded-xl border border-slate-700 p-4 mb-4 space-y-3">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <input
                  type="number"
                  placeholder="Destinatario (usuario #)"
                  value={transferForm.to_user_id}
                  onChange={(e) => setTransferForm({ ...transferForm, to_user_id: e.target.value })}
                  className="bg-slate-900/60 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                />
                <input
                  type="number"
                  placeholder="Monto (Maxos)"
                  value={transferForm.amount}
                  onChange={(e) => setTransferForm({ ...transferForm, amount: e.target.value })}
                  className="bg-slate-900/60 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                />
                <input
                  type="text"
                  placeholder="Razón (opcional)"
                  value={transferForm.reason}
                  onChange={(e) => setTransferForm({ ...transferForm, reason: e.target.value })}
                  className="bg-slate-900/60 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                />
              </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={doTransfer}
                  className="px-4 py-2 rounded-lg text-sm font-bold bg-emerald-500 text-white hover:bg-emerald-600 transition-all"
                >
                  Confirmar
                </button>
                {transferMsg && <span className="text-sm text-emerald-400">{transferMsg}</span>}
              </div>
            </div>
          )}

          <h4 className="text-xs font-bold uppercase tracking-widest text-slate-500 mb-2">
            Ledger de movimientos (T13)
          </h4>
          {ledger.length === 0 ? (
            <p className="text-sm text-slate-500 py-3">Sin movimientos registrados todavía.</p>
          ) : (
            <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
              {ledger.map((e) => (
                <div key={e.id} className="flex items-center justify-between bg-slate-900/40 rounded-lg px-4 py-2.5">
                  <div className="flex items-center gap-3 min-w-0">
                    {e.change_amount >= 0 ? (
                      <ArrowDownLeft className="w-4 h-4 text-emerald-400 shrink-0" />
                    ) : (
                      <ArrowUpRight className="w-4 h-4 text-rose-400 shrink-0" />
                    )}
                    <div className="min-w-0">
                      <p className="text-sm text-slate-300 truncate">{e.reason || "Movimiento"}</p>
                      <p className="text-xs text-slate-500">{e.created_at}</p>
                    </div>
                  </div>
                  <span className={`font-mono font-bold text-sm ${e.change_amount >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
                    {e.change_amount >= 0 ? "+" : ""}{fmtAmount(e.change_amount)}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="space-y-6">
          <div className="glass rounded-2xl border border-slate-800 p-6">
            <h3 className="flex items-center gap-2 font-bold text-white mb-3">
              <Star className="w-5 h-5 text-amber-400" />
              Reputación
            </h3>
            {reputation ? (
              <>
                <p className="text-4xl font-black text-amber-400">{reputation.score.toFixed(1)}</p>
                <p className="text-sm text-slate-400 mt-1">
                  {reputation.reviews_count} reseña{reputation.reviews_count === 1 ? "" : "s"} recibida{reputation.reviews_count === 1 ? "" : "s"}
                </p>
                <p className="text-xs text-slate-500 mt-3">
                  Grado de coherencia pública: la confianza se construye con acciones coherentes con los axiomas.
                </p>
              </>
            ) : (
              <p className="text-sm text-slate-500">Cargando...</p>
            )}
          </div>

          <div className="glass rounded-2xl border border-slate-800 p-6">
            <h3 className="flex items-center gap-2 font-bold text-white mb-3">
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
              Protección
            </h3>
            <span className={`inline-flex items-center px-3 py-1 rounded-lg text-xs font-bold border ${levelMeta.color}`}>
              {levelMeta.label}
            </span>
            <p className="text-xs text-slate-500 mt-2">
              {levelMeta.hint}
            </p>
            {caps && (
            <ul className="mt-3 space-y-1.5 text-sm text-slate-300">
              {caps.contract_hours !== null && caps.contract_hours !== undefined && (
                <li>· Tope por contrato: {caps.contract_hours} h</li>
              )}
              {caps.weekly_hours !== null && caps.weekly_hours !== undefined && (
                <li>· Tope semanal: {caps.weekly_hours} h</li>
              )}
              {caps.reflection_hours > 0 && <li>· Enfriamiento: {caps.reflection_hours} h</li>}
              {caps.requires_paraphrase && <li>· Paráfrasis oracular obligatoria</li>}
              {caps.requires_oracle_review && <li>· Revisión oracular pre-firma</li>}
              {caps.requires_witness && <li>· Co-testigo humano obligatorio</li>}
            </ul>
            )}
            <div className="mt-4 pt-4 border-t border-slate-800 space-y-2">
              <select
                value={protectForm.level}
                onChange={(e) => setProtectForm({ ...protectForm, level: e.target.value })}
                className="w-full bg-slate-900/60 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500"
              >
                <option value="standard">Estándar</option>
                <option value="assisted">Asistido</option>
                <option value="shielded">Blindado</option>
              </select>
              <div className="grid grid-cols-2 gap-2">
                <input
                  type="number"
                  placeholder="Acompañante (id)"
                  value={protectForm.companion_user_id}
                  onChange={(e) => setProtectForm({ ...protectForm, companion_user_id: e.target.value })}
                  className="bg-slate-900/60 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                />
                <input
                  type="number"
                  placeholder="Edad"
                  value={protectForm.declared_age}
                  onChange={(e) => setProtectForm({ ...protectForm, declared_age: e.target.value })}
                  className="bg-slate-900/60 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                />
              </div>
              <button
                onClick={doSaveProtection}
                className="w-full px-4 py-2 rounded-lg text-sm font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 hover:bg-emerald-500/20 transition-all"
              >
                Declarar perfil
              </button>
              {protectMsg && <p className="text-xs text-emerald-400">{protectMsg}</p>}
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="glass rounded-2xl border border-slate-800 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="flex items-center gap-2 font-bold text-white">
              <Boxes className="w-5 h-5 text-violet-400" />
              Recursos de la comunidad
            </h3>
            <button
              onClick={() => { setShowResource(!showResource); setResourceMsg(null); }}
              className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold bg-violet-500/10 text-violet-400 border border-violet-500/20 hover:bg-violet-500/20 transition-all"
            >
              <Plus className="w-4 h-4" />
              Ofrecer
            </button>
          </div>

          {showResource && (
            <div className="glass rounded-xl border border-slate-700 p-4 mb-4 space-y-3">
              <input
                type="text"
                placeholder="Título del recurso"
                value={resourceForm.title}
                onChange={(e) => setResourceForm({ ...resourceForm, title: e.target.value })}
                className="w-full bg-slate-900/60 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-violet-500"
              />
              <input
                type="text"
                placeholder="Descripción"
                value={resourceForm.description}
                onChange={(e) => setResourceForm({ ...resourceForm, description: e.target.value })}
                className="w-full bg-slate-900/60 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-violet-500"
              />
              <input
                type="text"
                placeholder="Categoría (ej. comida, herramienta, transporte)"
                value={resourceForm.category}
                onChange={(e) => setResourceForm({ ...resourceForm, category: e.target.value })}
                className="w-full bg-slate-900/60 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-violet-500"
              />
              <div className="flex items-center gap-3">
                <button
                  onClick={doCreateResource}
                  className="px-4 py-2 rounded-lg text-sm font-bold bg-violet-500 text-white hover:bg-violet-600 transition-all"
                >
                  Publicar
                </button>
                {resourceMsg && <span className="text-sm text-violet-400">{resourceMsg}</span>}
              </div>
            </div>
          )}

          {resources.length === 0 ? (
            <p className="text-sm text-slate-500 py-3">No hay recursos disponibles. Ofrece el tuyo.</p>
          ) : (
            <div className="space-y-2 max-h-80 overflow-y-auto pr-1">
              {resources.map((r) => (
                <div key={r.id} className="flex items-center justify-between gap-3 bg-slate-900/40 rounded-lg px-4 py-3">
                  <div className="min-w-0">
                    <p className="text-sm font-semibold text-white truncate">{r.title}</p>
                    <p className="text-xs text-slate-500 truncate">{r.description}</p>
                    {r.category && (
                      <span className="inline-block mt-1 px-2 py-0.5 rounded text-[10px] font-bold bg-violet-500/10 text-violet-400 border border-violet-500/20">
                        {r.category}
                      </span>
                    )}
                  </div>
                  {r.user_id === user.id ? (
                    <span className="text-xs text-slate-500 shrink-0">Tuyo</span>
                  ) : (
                    <button
                      onClick={() => doClaimResource(r.id)}
                      className="shrink-0 px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 hover:bg-emerald-500/20 transition-all"
                    >
                      Reclamar
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="glass rounded-2xl border border-slate-800 p-6">
          <h3 className="flex items-center gap-2 font-bold text-white mb-4">
            <GraduationCap className="w-5 h-5 text-emerald-400" />
            Camino de aprendizaje
            <InfoTip
              text="Lo que el nodo educativo (OEV) reportó de tu formación: temas aprobados, mentoría que diste a otros y la triada que lo confirmó. Cada registro lleva su huella T13 (verificable). La voz en la gobernanza no sube por aprender sola: la escalera sigue siendo por tu primer acuerdo — esta evidencia acompaña tu Perfil Vital."
            />
          </h3>
          {eduEvents.length === 0 ? (
            <p className="text-sm text-slate-500 py-3">
              Aún no hay evidencia educativa sincronizada. Aprueba y enseña desde el{" "}
              <Link href="/foro" className="text-emerald-400 hover:text-emerald-300 underline underline-offset-2">
                nodo educativo
              </Link>{" "}
              para que se vea aquí.
            </p>
          ) : (
            <div className="space-y-2 max-h-80 overflow-y-auto pr-1">
              {eduEvents.map((ev) => (
                <div key={ev.id} className="bg-slate-900/40 rounded-lg px-4 py-3 flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="text-sm font-semibold text-white truncate">
                      {ev.branch_slug.replace("_", " ")} · {ev.topic_slug.replace("_", " ")}
                    </p>
                    <p className="text-xs text-slate-500 mt-0.5">
                      {ev.verified_at?.slice(0, 10)}
                      {ev.score != null ? ` · avance ${Math.round(ev.score)}/100` : ""}
                      {ev.mentor_rounds > 0 ? ` · mentoría a ${ev.mentor_rounds} ronda${ev.mentor_rounds > 1 ? "s" : ""}` : ""}
                    </p>
                    <p className="text-[10px] font-mono text-slate-600 mt-1 truncate">
                      t13 {ev.t13_hash?.slice(0, 16)}…
                    </p>
                  </div>
                  {ev.triada_approved ? (
                    <span className="shrink-0 text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      ✓ triada
                    </span>
                  ) : (
                    <span className="shrink-0 text-[10px] font-bold px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">
                      en camino
                    </span>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="glass rounded-2xl border border-slate-800 p-6">
          <h3 className="flex items-center gap-2 font-bold text-white mb-4">
            <Handshake className="w-5 h-5 text-cyan-400" />
            Intercambios recientes
          </h3>
          {interchanges.length === 0 ? (
            <p className="text-sm text-slate-500 py-3">Aún no participas en intercambios registrados.</p>
          ) : (
            <div className="space-y-2 max-h-80 overflow-y-auto pr-1">
              {interchanges.map((i) => {
                const gave = i.giver_id === user.id;
                return (
                  <div key={i.id} className="bg-slate-900/40 rounded-lg px-4 py-3">
                    <div className="flex items-center justify-between gap-3">
                      <p className="text-sm font-semibold text-white truncate">
                        {i.description || i.type || i.interchange_id || `Intercambio #${i.id}`}
                      </p>
                      <span className={`shrink-0 text-xs font-bold px-2 py-0.5 rounded ${gave ? "bg-rose-500/10 text-rose-400 border border-rose-500/20" : "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"}`}>
                        {gave ? "Diste" : "Recibiste"}
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 mt-1">
                      {i.date || i.created_at}
                      {i.uth_hours ? ` · ${i.uth_hours} h` : ""}
                      {i.uvc_score ? ` · VHV ${i.uvc_score}` : ""}
                      {i.impact_resolution_score ? ` · impacto ${i.impact_resolution_score}/10` : ""}
                    </p>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
