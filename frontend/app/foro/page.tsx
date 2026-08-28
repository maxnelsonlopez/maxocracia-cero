"use client";

import React, { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  MessagesSquare,
  Plus,
  Loader2,
  Lock,
  CheckCircle2,
  Tag,
  User,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { apiFetch } from "../lib/api";

interface ForumPost {
  id: number;
  kind: string;
  kind_label: string;
  title: string;
  body: string;
  tags: string[];
  status: string;
  reply_count?: number;
  author: { user_id: number; name: string };
  created_at: string;
}

const KINDS = [
  { id: "topic", label: "Tema" },
  { id: "question", label: "Pregunta" },
  { id: "workshop_offer", label: "Oferta de taller" },
  { id: "need", label: "Necesidad" },
];

const KIND_STYLE: Record<string, string> = {
  topic: "border-sky-500/30 text-sky-400",
  question: "border-amber-500/30 text-amber-400",
  workshop_offer: "border-emerald-500/30 text-emerald-400",
  need: "border-rose-500/30 text-rose-400",
};

export default function ForoPage() {
  const { isAuthenticated, isLoading, user } = useAuth();
  const [posts, setPosts] = useState<ForumPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ kind: "question", title: "", body: "", tags: "" });
  const [submitting, setSubmitting] = useState(false);
  const [repliesOpen, setRepliesOpen] = useState<Record<number, boolean>>({});
  const [repliesByPost, setRepliesByPost] = useState<
    Record<number, { id: number; body: string; author: { name: string }; created_at: string }[]>
  >({});
  const [replyDrafts, setReplyDrafts] = useState<Record<number, string>>({});

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const url = filter ? `/forum/posts?type=${filter}` : "/forum/posts";
      const res = await apiFetch(url);
      if (!res.ok) throw new Error("No se pudieron cargar los posts");
      const data = await res.json();
      setPosts(data.posts || []);
      setError("");
    } catch (e: any) {
      setError(e.message || "Error de red");
    } finally {
      setLoading(false);
    }
  }, [filter]);

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
          <MessagesSquare className="w-12 h-12 text-violet-400 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-white mb-2">Foro Abierto</h1>
          <p className="text-slate-400 mb-6">
            La plaza del conocimiento: cualquier persona propone un tema, pregunta, ofrece
            un taller o levanta una necesidad. Sin matrícula, sin credencial: la ignorancia
            bienvenida.
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

  const publish = async () => {
    if (!form.title.trim() || !form.body.trim()) return;
    setSubmitting(true);
    try {
      const tags = form.tags.split(",").map((t) => t.trim()).filter(Boolean);
      const res = await apiFetch("/forum/posts", {
        method: "POST",
        body: JSON.stringify({ ...form, tags }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "No se pudo publicar");
      }
      setForm({ kind: "question", title: "", body: "", tags: "" });
      setShowForm(false);
      await load();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setSubmitting(false);
    }
  };

  const closePost = async (post: ForumPost) => {
    const resolution = prompt(
      "Resolución (opcional): ¿qué salió de esta conversación?"
    );
    if (resolution === null) return;
    try {
      const res = await apiFetch(`/forum/posts/${post.id}/close`, {
        method: "POST",
        body: JSON.stringify({ resolution }),
      });
      if (!res.ok) throw new Error("No se pudo cerrar");
      await load();
    } catch (e: any) {
      setError(e.message);
    }
  };

  const toggleReplies = async (postId: number) => {
    const open = !repliesOpen[postId];
    setRepliesOpen((r) => ({ ...r, [postId]: open }));
    if (open && !repliesByPost[postId]) {
      try {
        const res = await apiFetch(`/forum/posts/${postId}/replies`);
        if (!res.ok) throw new Error("No se pudieron cargar las respuestas");
        const data = await res.json();
        setRepliesByPost((r) => ({ ...r, [postId]: data.replies || [] }));
      } catch (e: any) {
        setError(e.message);
      }
    }
  };

  const sendReply = async (postId: number) => {
    const body = (replyDrafts[postId] || "").trim();
    if (!body) return;
    try {
      const res = await apiFetch(`/forum/posts/${postId}/replies`, {
        method: "POST",
        body: JSON.stringify({ body }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "No se pudo responder");
      }
      setReplyDrafts((d) => ({ ...d, [postId]: "" }));
      const list = await apiFetch(`/forum/posts/${postId}/replies`);
      const data = await list.json();
      setRepliesByPost((r) => ({ ...r, [postId]: data.replies || [] }));
      await load();
    } catch (e: any) {
      setError(e.message);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-5xl mx-auto px-4 py-10 space-y-8">
        <div className="bg-gradient-to-r from-violet-900/20 to-slate-900/80 backdrop-blur border border-violet-500/30 rounded-2xl p-6">
          <h1 className="text-2xl font-bold flex items-center gap-3">
            <MessagesSquare className="text-violet-400" />
            Foro Abierto
          </h1>
          <p className="text-sm text-violet-400/80 font-mono mt-1">
            OEV §1.7 — la plaza del conocimiento: temas, preguntas, talleres y necesidades
          </p>
          <p className="text-slate-400 text-sm mt-2">
            La ignorancia bienvenida: no hay examen de entrada, no hay credencial.
            Del foro nacen talleres (preguntas), grupos de solución (necesidades) y células (personas).
          </p>
          <button
            onClick={() => setShowForm(!showForm)}
            className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-violet-500 text-white font-bold text-sm hover:bg-violet-600 transition-all"
          >
            <Plus className="w-4 h-4" /> Publicar en la plaza
          </button>
        </div>

        {showForm && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass rounded-2xl border border-slate-800 p-6 space-y-4"
          >
            <div className="flex flex-wrap gap-2">
              {KINDS.map((k) => (
                <button
                  key={k.id}
                  onClick={() => setForm({ ...form, kind: k.id })}
                  className={`px-3 py-1.5 rounded-lg border text-sm transition-all ${
                    form.kind === k.id
                      ? KIND_STYLE[k.id] + " bg-slate-900"
                      : "border-slate-700 text-slate-400 hover:text-white"
                  }`}
                >
                  {k.label}
                </button>
              ))}
            </div>
            <input
              value={form.title}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
              placeholder="Título"
              maxLength={200}
              className="w-full px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 focus:border-violet-500 outline-none"
            />
            <textarea
              value={form.body}
              onChange={(e) => setForm({ ...form, body: e.target.value })}
              placeholder="Cuerpo: la ignorancia bienvenida, la disidencia con silla"
              rows={4}
              maxLength={5000}
              className="w-full px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 focus:border-violet-500 outline-none"
            />
            <input
              value={form.tags}
              onChange={(e) => setForm({ ...form, tags: e.target.value })}
              placeholder="Tags separados por coma (ej: naturaleza, taller)"
              className="w-full px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 focus:border-violet-500 outline-none"
            />
            <button
              onClick={publish}
              disabled={submitting || !form.title.trim() || !form.body.trim()}
              className="px-4 py-2 rounded-xl bg-violet-500 text-white font-bold text-sm hover:bg-violet-600 disabled:opacity-40 transition-all"
            >
              {submitting ? "Publicando..." : "Publicar"}
            </button>
          </motion.div>
        )}

        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setFilter("")}
            className={`px-3 py-1.5 rounded-lg border text-sm transition-all ${
              filter === ""
                ? "border-violet-500/40 text-violet-300 bg-violet-950/20"
                : "border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            Todo
          </button>
          {KINDS.map((k) => (
            <button
              key={k.id}
              onClick={() => setFilter(k.id)}
              className={`px-3 py-1.5 rounded-lg border text-sm transition-all ${
                filter === k.id
                  ? KIND_STYLE[k.id] + " bg-slate-900"
                  : "border-slate-700 text-slate-400 hover:text-white"
              }`}
            >
              {k.label}
            </button>
          ))}
        </div>

        {error && (
          <div className="text-rose-400 text-sm bg-rose-950/30 border border-rose-500/30 rounded-xl px-4 py-3">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex justify-center py-10">
            <Loader2 className="w-6 h-6 animate-spin text-violet-400" />
          </div>
        ) : (
          <div className="space-y-4">
            {posts.length === 0 && (
              <p className="text-slate-500 text-center py-10">
                La plaza está en silencio. Publica la primera pregunta.
              </p>
            )}
            {posts.map((post) => (
              <motion.article
                key={post.id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className={`glass rounded-2xl border p-5 ${
                  post.status !== "open" ? "opacity-60 border-slate-800" : "border-slate-700"
                }`}
              >
                <div className="flex items-center gap-3 flex-wrap">
                  <span
                    className={`px-2.5 py-0.5 rounded-full border text-xs font-semibold ${KIND_STYLE[post.kind] || "border-slate-600 text-slate-300"}`}
                  >
                    {post.kind_label}
                  </span>
                  {post.status === "resolved" && (
                    <span className="px-2.5 py-0.5 rounded-full border border-emerald-500/40 text-emerald-400 text-xs font-semibold flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" /> Resuelto
                    </span>
                  )}
                  {post.status === "closed" && (
                    <span className="px-2.5 py-0.5 rounded-full border border-slate-600 text-slate-400 text-xs font-semibold flex items-center gap-1">
                      <Lock className="w-3 h-3" /> Cerrado
                    </span>
                  )}
                  {post.tags.map((tag) => (
                    <span key={tag} className="flex items-center gap-1 text-xs text-emerald-400/80">
                      <Tag className="w-3 h-3" /> {tag}
                    </span>
                  ))}
                </div>
                <h2 className="text-lg font-bold mt-2">{post.title}</h2>
                <p className="text-slate-300 text-sm mt-1 whitespace-pre-wrap">{post.body}</p>
                <div className="flex items-center justify-between mt-3 text-xs text-slate-500">
                  <span className="flex items-center gap-1.5">
                    <User className="w-3.5 h-3.5" /> {post.author.name}
                  </span>
                  <span>{post.created_at}</span>
                </div>
                {post.status === "open" && user && post.author.user_id === user.id && (
                  <button
                    onClick={() => closePost(post)}
                    className="mt-3 px-3 py-1.5 rounded-lg border border-slate-600 text-xs text-slate-300 hover:text-white hover:bg-slate-800 transition-all"
                  >
                    Cerrar con resolución
                  </button>
                )}
                <div className="mt-3 border-t border-slate-800/60 pt-3">
                  <button
                    onClick={() => toggleReplies(post.id)}
                    className="px-3 py-1.5 rounded-lg border border-slate-700 text-xs text-slate-300 hover:text-white hover:bg-slate-800 transition-all"
                  >
                    💬 Respuestas ({post.reply_count ?? 0})
                  </button>
                  {repliesOpen[post.id] && (
                    <div className="mt-3 space-y-3">
                      <div className="space-y-2">
                        {(repliesByPost[post.id] || []).map((rep) => (
                          <div
                            key={rep.id}
                            className="bg-slate-900/60 border border-slate-800 rounded-xl px-4 py-2.5"
                          >
                            <p className="text-sm text-slate-200 whitespace-pre-wrap">{rep.body}</p>
                            <p className="text-[11px] text-slate-500 mt-1">
                              {rep.author.name} · {rep.created_at}
                            </p>
                          </div>
                        ))}
                        {post.status === "open" && (
                          <div className="flex gap-2">
                            <input
                              value={replyDrafts[post.id] || ""}
                              onChange={(e) =>
                                setReplyDrafts((d) => ({ ...d, [post.id]: e.target.value }))
                              }
                              placeholder="Tu voz en la plaza…"
                              maxLength={5000}
                              className="flex-1 px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 focus:border-violet-500 outline-none text-sm"
                            />
                            <button
                              onClick={() => sendReply(post.id)}
                              disabled={!(replyDrafts[post.id] || "").trim()}
                              className="px-3 py-2 rounded-xl bg-violet-500 text-white text-xs font-bold hover:bg-violet-600 disabled:opacity-40 transition-all"
                            >
                              Responder
                            </button>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </motion.article>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
