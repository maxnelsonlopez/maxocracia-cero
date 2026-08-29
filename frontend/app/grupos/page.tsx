"use client";

import React, { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Network, Plus, Loader2, Users, GitFork, Award, Lock } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { apiFetch } from "../lib/api";
import InfoTip from "../components/ui/InfoTip";

interface EduGroup {
  id: number;
  kind: string;
  name: string;
  description: string;
  need_title: string | null;
  status: string;
  member_count: number;
  creator: { user_id: number; name: string };
  children: { id: number; name: string; kind: string; status: string }[];
  skill_nodes: { skill_node: string; evidence: string }[];
  members?: { user_id: number; name: string; role: string }[];
}

export default function GruposPage() {
  const { isAuthenticated, isLoading } = useAuth();
  const [groups, setGroups] = useState<EduGroup[]>([]);
  const [details, setDetails] = useState<Record<number, EduGroup>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    kind: "solution_group",
    name: "",
    description: "",
    need_title: "",
  });
  const [submitting, setSubmitting] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await apiFetch("/groups");
      if (!res.ok) throw new Error("No se pudieron cargar los grupos");
      const data = await res.json();
      setGroups(data.groups || []);
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
          <Network className="w-12 h-12 text-violet-400 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-white mb-2">Grupos de Solución y Células Madre</h1>
          <p className="text-slate-400 mb-6">
            Un "grupo de solución" se arma cuando la comunidad dice "necesitamos esto" y alguien
            se junta a resolverlo. Una "célula madre" es el grupo que forma otros grupos.
            Inicia sesión para participar.
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
    if (!form.name.trim()) return;
    if (form.kind === "solution_group" && !form.need_title.trim()) return;
    setSubmitting(true);
    try {
      const res = await apiFetch("/groups", {
        method: "POST",
        body: JSON.stringify(form),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "No se pudo crear");
      }
      setForm({ kind: "solution_group", name: "", description: "", need_title: "" });
      setShowForm(false);
      await load();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setSubmitting(false);
    }
  };

  const join = async (id: number) => {
    try {
      const res = await apiFetch(`/groups/${id}/join`, { method: "POST" });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "No se pudo unir");
      }
      await load();
    } catch (e: any) {
      setError(e.message);
    }
  };

  const registerChild = async (mother: EduGroup) => {
    const childId = Number(prompt("Número del grupo que nació de esta célula (ver su detalle):"));
    if (!childId) return;
    try {
      const res = await apiFetch(`/groups/${mother.id}/child`, {
        method: "POST",
        body: JSON.stringify({ child_group_id: childId }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "No se pudo registrar la réplica");
      }
      await load();
    } catch (e: any) {
      setError(e.message);
    }
  };

  const openDetail = async (id: number) => {
    try {
      const res = await apiFetch(`/groups/${id}`);
      if (!res.ok) throw new Error("No se pudo cargar el detalle");
      const data = await res.json();
      setDetails((d) => ({ ...d, [id]: data.group }));
    } catch (e: any) {
      setError(e.message);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-5xl mx-auto px-4 py-10 space-y-8">
        <div className="bg-gradient-to-r from-sky-900/20 to-slate-900/80 backdrop-blur border border-sky-500/30 rounded-2xl p-6">
          <h1 className="text-2xl font-bold flex items-center gap-3">
            <Network className="text-sky-400" />
            Grupos de Solución y Células Madre
          </h1>
          <p className="text-sm text-sky-400/80 font-mono mt-1">
            Las necesidades de la comunidad se resuelven en grupo, y cada grupo deja aprendizaje
          </p>
          <p className="text-slate-400 text-sm mt-2">
            Un grupo de solución resuelve una necesidad real; una célula madre forma grupos
            de solución.
            <InfoTip
              className="ml-2"
              text="'ECE' no es un grito ni una sigla secreta: son los Encargos Comunitarios Educativos — la necesidad entra desde la comunidad y la solución vuelve a ella. Las células madre son la capa que multiplica: forman grupos, y cada grupo formado deja constancia de quién lo hizo nacer (así se ve la fractalidad: un grupo → otro grupo → más aprendizaje)."
            />
          </p>
          <button
            onClick={() => setShowForm(!showForm)}
            className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-sky-500 text-white font-bold text-sm hover:bg-sky-600 transition-all"
          >
            <Plus className="w-4 h-4" /> Formar un grupo
          </button>
        </div>

        {showForm && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass rounded-2xl border border-slate-800 p-6 space-y-3"
          >
            <div className="flex gap-2">
              <button
                onClick={() => setForm({ ...form, kind: "solution_group" })}
                className={`px-3 py-1.5 rounded-lg border text-sm ${
                  form.kind === "solution_group"
                    ? "border-emerald-500/40 text-emerald-300 bg-emerald-950/20"
                    : "border-slate-700 text-slate-400"
                }`}
              >
                Grupo de solución (ECE)
              </button>
              <button
                onClick={() => setForm({ ...form, kind: "mother_cell" })}
                className={`px-3 py-1.5 rounded-lg border text-sm ${
                  form.kind === "mother_cell"
                    ? "border-sky-500/40 text-sky-300 bg-sky-950/20"
                    : "border-slate-700 text-slate-400"
                }`}
              >
                Célula madre
              </button>
            </div>
            <input
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              placeholder="Nombre del grupo"
              maxLength={160}
              className="w-full px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 focus:border-sky-500 outline-none"
            />
            {form.kind === "solution_group" && (
              <input
                value={form.need_title}
                onChange={(e) => setForm({ ...form, need_title: e.target.value })}
                placeholder="La necesidad real que resuelve (ej: agua en la vereda)"
                className="w-full px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 focus:border-sky-500 outline-none"
              />
            )}
            <textarea
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              placeholder="Descripción"
              rows={3}
              maxLength={3000}
              className="w-full px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 focus:border-sky-500 outline-none"
            />
            <button
              onClick={create}
              disabled={submitting || !form.name.trim()}
              className="px-4 py-2 rounded-xl bg-sky-500 text-white font-bold text-sm hover:bg-sky-600 disabled:opacity-40 transition-all"
            >
              {submitting ? "Creando..." : "Crear grupo"}
            </button>
          </motion.div>
        )}

        {error && (
          <div className="text-rose-400 text-sm bg-rose-950/30 border border-rose-500/30 rounded-xl px-4 py-3">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex justify-center py-10">
            <Loader2 className="w-6 h-6 animate-spin text-sky-400" />
          </div>
        ) : (
          <div className="space-y-4">
            {groups.length === 0 && (
              <p className="text-slate-500 text-center py-10">
                Aún no hay grupos. Levanta una necesidad en el foro o forma una célula madre.
              </p>
            )}
            {groups.map((g) => (
              <motion.article
                key={g.id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="glass rounded-2xl border border-slate-700 p-5 space-y-3"
              >
                <div className="flex items-start justify-between gap-4 flex-wrap">
                  <div>
                    <h2 className="text-lg font-bold flex items-center gap-2">
                      {g.kind === "mother_cell" && <GitFork className="w-4 h-4 text-sky-400" />}
                      {g.name}
                    </h2>
                    {g.need_title && (
                      <p className="text-xs text-amber-400/80 mt-1">Necesidad: {g.need_title}</p>
                    )}
                  </div>
                  <span
                    className={`px-2.5 py-0.5 rounded-full border text-xs font-semibold ${
                      g.kind === "mother_cell"
                        ? "border-sky-500/40 text-sky-300"
                        : "border-emerald-500/40 text-emerald-300"
                    }`}
                  >
                    {g.kind === "mother_cell" ? "Célula madre" : "Grupo de solución"}
                  </span>
                </div>
                {g.description && <p className="text-slate-400 text-sm">{g.description}</p>}
                <div className="flex items-center gap-4 text-xs text-slate-400">
                  <span className="flex items-center gap-1.5">
                    <Users className="w-3.5 h-3.5" /> {g.member_count} miembros
                  </span>
                  <span>Fundadora: {g.creator.name}</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => join(g.id)}
                    disabled={g.status !== "active"}
                    className="px-3 py-1.5 rounded-lg border border-emerald-500/40 text-emerald-300 text-xs hover:bg-emerald-950/20 disabled:opacity-40 transition-all"
                  >
                    Unirme
                  </button>
                  {g.kind === "mother_cell" && (
                    <button
                      onClick={() => registerChild(g)}
                      className="px-3 py-1.5 rounded-lg border border-sky-500/40 text-sky-300 text-xs hover:bg-sky-950/20 transition-all"
                    >
                      Registrar réplica
                    </button>
                  )}
                  <button
                    onClick={() => openDetail(g.id)}
                    className="px-3 py-1.5 rounded-lg border border-slate-600 text-xs text-slate-300 hover:text-white hover:bg-slate-800 transition-all"
                  >
                    Ver fractal
                  </button>
                  {g.status === "closed" && (
                    <span className="text-xs text-slate-500 flex items-center gap-1">
                      <Lock className="w-3 h-3" /> Cerrado
                    </span>
                  )}
                </div>

                {details[g.id] && (
                  <div className="border-t border-slate-800 pt-3 space-y-2 text-xs">
                    {details[g.id].children && details[g.id].children!.length > 0 && (
                      <div>
                        <p className="text-slate-500 mb-1">Réplicas que ha formado:</p>
                        <ul className="space-y-1">
                          {details[g.id].children!.map((c) => (
                            <li key={c.id} className="text-slate-300">
                              — {c.name} ({c.kind === "mother_cell" ? "célula" : "grupo de solución"})
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {details[g.id].skill_nodes && details[g.id].skill_nodes!.length > 0 && (
                      <div>
                        <p className="text-slate-500 mb-1 flex items-center gap-1">
                          <Award className="w-3 h-3" /> Nodos ganados:
                        </p>
                        <ul className="space-y-1">
                          {details[g.id].skill_nodes!.map((n) => (
                            <li key={n.skill_node} className="text-emerald-300">
                              {n.skill_node} — <span className="text-slate-500">{n.evidence}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
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
