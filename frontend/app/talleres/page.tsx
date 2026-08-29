"use client";

import React, { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  GraduationCap,
  Plus,
  Loader2,
  Users,
  Award,
  Lock,
  TreePine,
  ChevronDown,
  X,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { apiFetch } from "../lib/api";
import InfoTip from "../components/ui/InfoTip";

interface Workshop {
  id: number;
  title: string;
  skill_node: string;
  description: string;
  status: string;
  capacity: number;
  enrolled_count: number;
  facilitator: { user_id: number; name: string };
  my_award?: { outcome: string } | null;
  outputs?: { id: number; kind: string; title: string; author: { name: string } }[];
  enrollments?: { user_id: number; name: string }[];
}

interface TriadaState {
  workshop: Workshop;
  learnerId: string;
  mentorOk: boolean;
  peerOk: boolean;
  oracleVeto: boolean;
  hours: string;
  message: { kind: "ok" | "err"; text: string } | null;
  busy: boolean;
}

interface TreeBranch {
  branch: string;
  count: number;
  nodes: { id: string; name: string; dificultad: number; prereq_ids: string[] }[];
}

export default function TalleresPage() {
  const { isAuthenticated, isLoading, user } = useAuth();
  const [workshops, setWorkshops] = useState<Workshop[]>([]);
  const [details, setDetails] = useState<Record<number, Workshop>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    title: "",
    skill_node: "",
    description: "",
    capacity: 8,
  });
  const [submitting, setSubmitting] = useState(false);
  const [tree, setTree] = useState<TreeBranch[] | null>(null);
  const [openBranch, setOpenBranch] = useState<string | null>(null);
  const [triada, setTriada] = useState<TriadaState | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await apiFetch("/workshops");
      if (!res.ok) throw new Error("No se pudieron cargar los talleres");
      const data = await res.json();
      setWorkshops(data.workshops || []);
      setError("");
    } catch (e: any) {
      setError(e.message || "Error de red");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (isAuthenticated) load();
  }, [isAuthenticated, load]);

  // El tejido visible: ramas canónicas del árbol (T13, estado no tribunal).
  useEffect(() => {
    if (!isAuthenticated || tree) return;
    apiFetch("/workshops/tree")
      .then(async (res) => {
        if (res.ok) {
          const data = await res.json();
          setTree(data.tree?.branches || null);
        }
      })
      .catch(() => setTree(null));
  }, [isAuthenticated, tree]);

  const openDetail = async (id: number) => {
    try {
      const res = await apiFetch(`/workshops/${id}`);
      if (!res.ok) throw new Error("No se pudo cargar el detalle");
      const data = await res.json();
      setDetails((d) => ({ ...d, [id]: data.workshop }));
    } catch (e: any) {
      setError(e.message);
    }
  };

  if (isLoading)
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-violet-400" />
      </div>
    );

  if (!isAuthenticated)
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="max-w-md w-full glass rounded-2xl border border-slate-800 p-8 text-center">
          <GraduationCap className="w-12 h-12 text-violet-400 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-white mb-2">Talleres de Aprendizaje</h1>
          <p className="text-slate-400 mb-6">
            La unidad de enseñanza de cualquier skill. Regla de oro: el skill se gana
            enseñándolo (la vacuación). Inicia sesión para participar.
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

  const create = async () => {
    if (!form.title.trim() || !form.skill_node.trim()) return;
    setSubmitting(true);
    try {
      const res = await apiFetch("/workshops", {
        method: "POST",
        body: JSON.stringify(form),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "No se pudo crear");
      }
      setForm({ title: "", skill_node: "", description: "", capacity: 8 });
      setShowForm(false);
      await load();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setSubmitting(false);
    }
  };

  const enroll = async (id: number) => {
    try {
      const res = await apiFetch(`/workshops/${id}/enroll`, { method: "POST" });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "No se pudo inscribir");
      }
      await load();
    } catch (e: any) {
      setError(e.message);
    }
  };

  const addOutput = async (id: number, kind: "material" | "obra") => {
    const title = prompt(
      kind === "material" ? "Título del material de enseñanza (abierto, forkable):" : "Título de la obra aplicada:"
    );
    if (!title) return;
    try {
      const res = await apiFetch(`/workshops/${id}/outputs`, {
        method: "POST",
        body: JSON.stringify({ kind, title }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "No se pudo publicar");
      }
      await openDetail(id);
      await load();
    } catch (e: any) {
      setError(e.message);
    }
  };

  const openTriada = async (workshop: Workshop) => {
    // El detalle trae la lista de inscritos (T13): la triada no se hace a ciegas.
    await openDetail(workshop.id);
    const fresh = details[workshop.id] ?? workshop;
    setTriada({
      workshop: fresh,
      learnerId: "",
      mentorOk: false,
      peerOk: false,
      oracleVeto: false,
      hours: "1",
      message: null,
      busy: false,
    });
  };

  const submitTriada = async () => {
    if (!triada) return;
    const targetId = Number(triada.learnerId);
    if (!targetId) {
      setTriada({ ...triada, message: { kind: "err", text: "Elige quién vacua la habilidad." } });
      return;
    }
    setTriada({ ...triada, busy: true, message: null });
    try {
      const res = await apiFetch(`/workshops/${triada.workshop.id}/grant-skill`, {
        method: "POST",
        body: JSON.stringify({
          user_id: targetId,
          mentor_ok: triada.mentorOk,
          peer_ok: triada.peerOk,
          oracle_veto: triada.oracleVeto,
          mentoria_horas: Number(triada.hours) || 0,
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        setTriada((t) => t && { ...t, busy: false, message: { kind: "err", text: data.error || "No se pudo conceder" } });
        return;
      }
      const award = data.award;
      const text =
        award.outcome === "awarded"
          ? `🎉 ${award.skill_node}: ¡ha vacuado! La validación es la transferencia.`
          : award.outcome === "awaiting_triada"
            ? `En espera de la triada: ${(award.triada_bloqueos || []).join("; ")}`
            : `Rechazado por la regla de oro: ${(award.vacua_faltantes || []).join("; ")}`;
      setTriada((t) => t && { ...t, busy: false, message: { kind: "ok", text } });
      await openDetail(triada.workshop.id);
    } catch (e: any) {
      setTriada((t) => t && { ...t, busy: false, message: { kind: "err", text: e.message || "Error de conexión" } });
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-5xl mx-auto px-4 py-10 space-y-8">
        <div className="bg-gradient-to-r from-emerald-900/20 to-slate-900/80 backdrop-blur border border-emerald-500/30 rounded-2xl p-6">
          <h1 className="text-2xl font-bold flex items-center gap-3">
            <GraduationCap className="text-emerald-400" />
            Talleres de Aprendizaje
          </h1>
          <p className="text-sm text-emerald-400/80 font-mono mt-1">
            La escuela de cualquier cosa: un grupo pequeño (5-12) donde alguien que sabe enseña
          </p>
          <p className="text-slate-400 text-sm mt-2">
            Aquí no hay exámenes ni notas. Para que se te reconozca una habilidad:{" "}
            <b className="text-emerald-300">ponla en práctica</b>,{" "}
            <b className="text-emerald-300">enséñala con material propio</b> y{" "}
            <b className="text-emerald-300">ayuda a alguien a aprenderla</b>.
            Lo confirma el maestro + un compañero + un guardián con veto.
            <InfoTip
              className="ml-2"
              text="A esto lo llamamos 'vacuar' el conocimiento (la regla de oro): el saber se gana enseñándolo. Nada de clasificar personas ni rankings: cada paso se registra para que cualquiera pueda revisarlo (T13)."
            />
          </p>
          <button
            onClick={() => setShowForm(!showForm)}
            className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-500 text-white font-bold text-sm hover:bg-emerald-600 transition-all"
          >
            <Plus className="w-4 h-4" /> Ofrecer un taller
          </button>
        </div>

        {/* El tejido: ramas canónicas del árbol (estado, no tribunal) */}
        {tree && (
          <div className="glass rounded-2xl border border-slate-800 p-5 space-y-3">
            <div className="flex items-center gap-2">
              <TreePine className="w-4 h-4 text-emerald-400" />
              <h2 className="text-sm font-bold text-white">
                El mapa de lo que se puede aprender
              </h2>
              <InfoTip
                text="Estas son las ramas maestras del tejido: matemáticas, naturaleza, relaciones… Cada rama es un camino de habilidades, y el mapa no clasifica a nadie — solo muestra qué existe. El tejido es infinito y forkable: si la rama de tu comunidad no existe, se crea con su propia semilla (así crecen los árboles de verdad)."
              />
              <span className="text-[10px] font-mono text-slate-600 ml-auto">
                {tree.reduce((a, b) => a + b.count, 0)} semillas
              </span>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              {tree.map((b) => (
                <button
                  key={b.branch}
                  onClick={() => setOpenBranch(openBranch === b.branch ? null : b.branch)}
                  className={`px-3 py-2 rounded-xl border text-left text-xs transition-all ${
                    openBranch === b.branch
                      ? "border-emerald-500/50 bg-emerald-950/20 text-emerald-300"
                      : "border-slate-700 text-slate-300 hover:border-emerald-500/30"
                  }`}
                >
                  <span className="capitalize font-semibold">{b.branch.replace("_", " ")}</span>
                  <ChevronDown
                    className={`w-3 h-3 inline ml-1 transition-transform ${
                      openBranch === b.branch ? "rotate-180" : ""
                    }`}
                  />
                </button>
              ))}
            </div>
            {openBranch &&
              tree
                .filter((b) => b.branch === openBranch)
                .map((b) => (
                  <ul key={b.branch} className="space-y-1.5 text-xs">
                    {b.nodes.map((n) => (
                      <li key={n.id} className="flex items-start gap-2 text-slate-400">
                        <span className="text-emerald-400 mt-0.5">·</span>
                        <span>
                          <b className="text-slate-200">{n.name}</b>{" "}
                          <span className="text-slate-600">
                            ({"•".repeat(n.dificultad)}
                            {"○".repeat(5 - n.dificultad)})
                          </span>
                          {n.prereq_ids.length > 0 && (
                            <span className="text-slate-600">
                              {" "}
                              — antes: {n.prereq_ids.join(", ")}
                            </span>
                          )}
                        </span>
                      </li>
                    ))}
                  </ul>
                ))}
          </div>
        )}

        {showForm && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass rounded-2xl border border-slate-800 p-6 space-y-3"
          >
            <input
              value={form.title}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
              placeholder="Título del taller"
              maxLength={200}
              className="w-full px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 focus:border-emerald-500 outline-none"
            />
            <input
              value={form.skill_node}
              onChange={(e) => setForm({ ...form, skill_node: e.target.value })}
              placeholder="Rama de la habilidad (ej: naturaleza/huertas)"
              className="w-full px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 focus:border-emerald-500 outline-none"
            />
            <p className="text-[11px] text-slate-500 flex items-center gap-1.5">
              Todas las habilidades del mundo viven en un árbol que ramifica y se expande con la comunidad.
              <InfoTip text="El Árbol de Habilidades es el mapa completo de lo que un humano puede aprender: matemáticas, cocina, programación, jardinería… Cada rama tiene caminos (primero lo básico, luego lo avanzado) y cualquier persona puede proponer una rama nueva: el tejido es infinito y se bifurca (por eso no hay ningún currículo congelado)." />
            </p>
            <textarea
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              placeholder="Descripción (qué se aprende, qué obra deja el grupo)"
              rows={3}
              maxLength={3000}
              className="w-full px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 focus:border-emerald-500 outline-none"
            />
            <div className="flex items-center gap-3">
              <label className="text-sm text-slate-400">Cupos (5-12):</label>
              <input
                type="number"
                min={5}
                max={12}
                value={form.capacity}
                onChange={(e) => setForm({ ...form, capacity: Number(e.target.value) })}
                className="w-24 px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 focus:border-emerald-500 outline-none"
              />
              <button
                onClick={create}
                disabled={submitting || !form.title.trim() || !form.skill_node.trim()}
                className="px-4 py-2 rounded-xl bg-emerald-500 text-white font-bold text-sm hover:bg-emerald-600 disabled:opacity-40 transition-all"
              >
                {submitting ? "Creando..." : "Crear taller"}
              </button>
            </div>
          </motion.div>
        )}

        {error && (
          <div className="text-rose-400 text-sm bg-rose-950/30 border border-rose-500/30 rounded-xl px-4 py-3">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex justify-center py-10">
            <Loader2 className="w-6 h-6 animate-spin text-emerald-400" />
          </div>
        ) : (
          <div className="space-y-4">
            {workshops.length === 0 && (
              <p className="text-slate-500 text-center py-10">
                Aún no hay talleres. Ofrece el primero desde el foro o aquí.
              </p>
            )}
            {workshops.map((w) => (
              <motion.article
                key={w.id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="glass rounded-2xl border border-slate-700 p-5 space-y-3"
              >
                <div className="flex items-start justify-between gap-4 flex-wrap">
                  <div>
                    <h2 className="text-lg font-bold">{w.title}</h2>
                    <p className="text-xs text-emerald-400/80 font-mono">{w.skill_node}</p>
                  </div>
                  <span
                    className={`px-2.5 py-0.5 rounded-full border text-xs font-semibold ${
                      w.status === "open"
                        ? "border-emerald-500/40 text-emerald-400"
                        : w.status === "running"
                          ? "border-amber-500/40 text-amber-400"
                          : "border-slate-600 text-slate-400 flex items-center gap-1"
                    }`}
                  >
                    {w.status === "closed" && <Lock className="w-3 h-3" />}
                    {w.status === "open" ? "Abierto" : w.status === "running" ? "En curso" : "Cerrado"}
                  </span>
                </div>
                {w.description && <p className="text-slate-400 text-sm">{w.description}</p>}
                <div className="flex items-center gap-4 text-xs text-slate-400">
                  <span className="flex items-center gap-1.5">
                    <Users className="w-3.5 h-3.5" /> {w.enrolled_count}/{w.capacity} aprendices
                  </span>
                  <span>Facilita: {w.facilitator.name}</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => enroll(w.id)}
                    disabled={w.status !== "open"}
                    className="px-3 py-1.5 rounded-lg border border-emerald-500/40 text-emerald-300 text-xs hover:bg-emerald-950/20 disabled:opacity-40 transition-all"
                  >
                    Inscribirme
                  </button>
                  <button
                    onClick={() => openDetail(w.id)}
                    className="px-3 py-1.5 rounded-lg border border-slate-600 text-xs text-slate-300 hover:text-white hover:bg-slate-800 transition-all"
                  >
                    Ver obras y mi award
                  </button>
                </div>

                {details[w.id] && (
                  <div className="border-t border-slate-800 pt-3 space-y-3">
                    <div className="flex flex-wrap gap-2">
                      <button
                        onClick={() => addOutput(w.id, "material")}
                        className="px-3 py-1.5 rounded-lg border border-sky-500/40 text-sky-300 text-xs hover:bg-sky-950/20 transition-all"
                      >
                        + Material de enseñanza (abierto, forkable)
                      </button>
                      <button
                        onClick={() => addOutput(w.id, "obra")}
                        className="px-3 py-1.5 rounded-lg border border-amber-500/40 text-amber-300 text-xs hover:bg-amber-950/20 transition-all"
                      >
                        + Obra aplicada (hecho con la comunidad)
                      </button>
                      {user?.id === details[w.id]?.facilitator?.user_id && (
                        <button
                          onClick={() => openTriada(w)}
                          className="px-3 py-1.5 rounded-lg border border-violet-500/40 text-violet-300 text-xs hover:bg-violet-950/20 transition-all"
                        >
                          <Award className="w-3.5 h-3.5 inline mr-1" />
                          Conceder habilidad (triada)
                        </button>
                      )}
                      {user?.id !== details[w.id]?.facilitator?.user_id && (
                        <span className="text-[11px] text-slate-600 self-center">
                          La habilidad la concede el maestro del taller, por triada.
                        </span>
                      )}
                    </div>
                    {details[w.id].outputs && details[w.id].outputs!.length > 0 && (
                      <ul className="space-y-1 text-xs text-slate-400">
                        {details[w.id].outputs!.map((o) => (
                          <li key={o.id}>
                            <span className="text-slate-200">{o.title}</span>{" "}
                            <span className="text-slate-500">
                              ({o.kind} · {o.author.name})
                            </span>
                          </li>
                        ))}
                      </ul>
                    )}
                    {details[w.id].my_award && (
                      <p className="text-xs">
                        Mi award:{" "}
                        <span className="font-semibold text-emerald-400">
                          {details[w.id].my_award!.outcome}
                        </span>{" "}
                        <span className="text-slate-500">({details[w.id].skill_node})</span>
                      </p>
                    )}
                  </div>
                )}
              </motion.article>
            ))}
          </div>
        )}

        {/* Triada de concesión: sin prompt(), la lista de inscritos manda */}
        {triada && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              className="w-full max-w-lg glass rounded-2xl border border-violet-500/30 p-6 space-y-4"
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <Award className="w-4 h-4 text-violet-400" />
                    Conceder habilidad a quien la enseña
                  </h3>
                  <p className="text-[11px] text-slate-500 mt-1">
                    Taller: <b className="text-slate-300">{triada.workshop.title}</b> ·{" "}
                    {triada.workshop.skill_node}
                  </p>
                </div>
                <button
                  onClick={() => setTriada(null)}
                  className="text-slate-500 hover:text-white transition-colors"
                  aria-label="Cerrar"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              {(triada.workshop.enrollments?.length ?? 0) === 0 ? (
                <p className="text-xs text-amber-300/90 border border-amber-500/30 rounded-xl px-4 py-3 bg-amber-950/20">
                  Aún no hay aprendices inscritos. La triada espera: la habilidad se
                  gana enseñando a alguien de verdad (vacuación).
                </p>
              ) : (
                <>
                  <div className="space-y-1">
                    <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                      ¿Quién vacua la habilidad? (la lista del taller)
                    </label>
                    <select
                      value={triada.learnerId}
                      onChange={(e) => setTriada({ ...triada, learnerId: e.target.value })}
                      className="w-full px-3 py-2 text-sm rounded-xl bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-violet-500 text-white"
                    >
                      <option value="">— elige a un aprendiz —</option>
                      {(triada.workshop.enrollments || []).map((e) => (
                        <option key={e.user_id} value={String(e.user_id)}>
                          {e.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="grid grid-cols-1 gap-2">
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={triada.mentorOk}
                        onChange={(e) => setTriada({ ...triada, mentorOk: e.target.checked })}
                        className="accent-violet-500"
                      />
                      El maestro avala: ya enseña el material con la comunidad
                    </label>
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={triada.peerOk}
                        onChange={(e) => setTriada({ ...triada, peerOk: e.target.checked })}
                        className="accent-violet-500"
                      />
                      Una par avala: otro aprendiz lo confirma por haberlo visto
                    </label>
                    <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={triada.oracleVeto}
                        onChange={(e) => setTriada({ ...triada, oracleVeto: e.target.checked })}
                        className="accent-rose-500"
                      />
                      El guardián (oráculo) ejerce el veto — solo si un axioma está en riesgo
                      <InfoTip
                        text="El guardián no vota según gustos: solo puede vetar si la concesión rompe un axioma (por ejemplo, si la obra daña a alguien). Su veto se registra con quién fue y por qué (T13)."
                      />
                    </label>
                  </div>

                  <div className="space-y-1">
                    <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                      Horas de mentoría que el aprendiz dio a otros (TVI)
                    </label>
                    <input
                      type="number"
                      min={0}
                      step={0.5}
                      value={triada.hours}
                      onChange={(e) => setTriada({ ...triada, hours: e.target.value })}
                      className="w-full px-3 py-2 text-sm font-mono rounded-xl bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-violet-500 text-white"
                    />
                  </div>

                  {triada.message && (
                    <div
                      className={`text-[11px] font-mono ${
                        triada.message.kind === "ok" ? "text-emerald-400" : "text-rose-400"
                      }`}
                    >
                      {triada.message.text}
                    </div>
                  )}

                  <div className="flex gap-2 justify-end">
                    <button
                      onClick={() => setTriada(null)}
                      className="px-4 py-2 rounded-xl border border-slate-700 text-slate-300 text-xs hover:text-white transition-all"
                    >
                      Cerrar
                    </button>
                    <button
                      onClick={submitTriada}
                      disabled={triada.busy || !triada.learnerId}
                      className="px-4 py-2 rounded-xl bg-violet-500 hover:bg-violet-400 disabled:opacity-40 text-white text-xs font-bold transition-all"
                    >
                      {triada.busy ? "Vaciando..." : "Emitir veredicto"}
                    </button>
                  </div>
                </>
              )}
            </motion.div>
          </div>
        )}
      </div>
    </div>
  );
}
