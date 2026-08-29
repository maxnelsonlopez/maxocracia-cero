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
}

export default function TalleresPage() {
  const { isAuthenticated, isLoading } = useAuth();
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

  const grantSkill = async (workshop: Workshop) => {
    const targetId = Number(prompt("ID del aprendiz que vacua el skill (user_id):"));
    if (!targetId) return;
    const mentorOk = confirm("¿El mentor (facilitador) avala?");
    const peerOk = confirm("¿Un par aprendiz avala?");
    const oracleVeto = confirm("¿El oráculo ejerce el VETO? (solo si un axioma está en riesgo)");
    const hours = Number(prompt("Horas de mentoría registradas (TVI):", "1")) || 0;
    try {
      const res = await apiFetch(`/workshops/${workshop.id}/grant-skill`, {
        method: "POST",
        body: JSON.stringify({
          user_id: targetId,
          mentor_ok: mentorOk,
          peer_ok: peerOk,
          oracle_veto: oracleVeto,
          mentoria_horas: hours,
        }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "No se pudo conceder");
      }
      const data = await res.json();
      const award = data.award;
      setError("");
      alert(
        award.outcome === "awarded"
          ? `🎉 Skill "${award.skill_node}" vacua: la validación es la transferencia.`
          : award.outcome === "awaiting_triada"
            ? `En espera de la triada: ${award.triada_bloqueos.join("; ")}`
            : `Rechazado por la regla de oro: ${award.vacua_faltantes.join("; ")}`
      );
      await openDetail(workshop.id);
    } catch (e: any) {
      setError(e.message);
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
                      <button
                        onClick={() => grantSkill(w)}
                        className="px-3 py-1.5 rounded-lg border border-violet-500/40 text-violet-300 text-xs hover:bg-violet-950/20 transition-all"
                      >
                        <Award className="w-3.5 h-3.5 inline mr-1" />
                        Conceder skill (triada)
                      </button>
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
      </div>
    </div>
  );
}
