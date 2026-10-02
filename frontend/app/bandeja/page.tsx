"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Inbox, UserPlus, KeyRound, Bell, Check, ExternalLink } from "lucide-react";
import { apiFetch } from "../lib/api";

interface InboxMsg {
    id: number;
    to_email: string;
    kind: "invite" | "password_reset" | "notice";
    subject: string;
    body: string;
    link_url: string | null;
    has_link?: boolean;
    status: string;
    created_at: string;
}

const KIND_META = {
    invite: { label: "Invitación", icon: UserPlus, color: "text-emerald-400" },
    password_reset: { label: "Recuperación", icon: KeyRound, color: "text-amber-400" },
    notice: { label: "Aviso", icon: Bell, color: "text-sky-400" },
} as const;

export default function BandejaPage() {
    const [msgs, setMsgs] = useState<InboxMsg[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        apiFetch("/inbox")
            .then(async (res) => {
                if (!res.ok) throw new Error("Inicia sesión para ver tu bandeja");
                setMsgs(await res.json());
            })
            .catch((err) => setError(err instanceof Error ? err.message : "Error"))
            .finally(() => setLoading(false));
    }, []);

    async function markRead(id: number) {
        const res = await apiFetch(`/inbox/${id}/read`, { method: "POST" });
        if (res.ok) {
            setMsgs((ms) => ms.map((m) => (m.id === id ? { ...m, status: "read" } : m)));
        }
    }

    return (
        <div className="min-h-screen max-w-3xl mx-auto px-4 sm:px-6 py-24">
            <div className="flex items-center gap-3 mb-2">
                <Inbox className="w-6 h-6 text-emerald-400" />
                <h1 className="text-2xl font-bold text-white">Bandeja interna</h1>
            </div>
            <p className="text-sm text-slate-400 mb-8">
                El relevo cuando el correo no llega: invitaciones y avisos dirigidos a tu cuenta.
            </p>

            {loading ? (
                <p className="text-slate-500 text-sm animate-pulse">Abriendo la bandeja…</p>
            ) : error ? (
                <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 text-center space-y-3">
                    <p className="text-sm text-slate-400">{error}</p>
                    <Link href="/login" className="inline-block text-emerald-400 text-sm font-medium">
                        Iniciar sesión
                    </Link>
                </div>
            ) : msgs.length === 0 ? (
                <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 text-center">
                    <p className="text-sm text-slate-400">Bandeja vacía. Cuando alguien te invite o pidas recuperar tu acceso, aparecerá aquí.</p>
                </div>
            ) : (
                <div className="space-y-4">
                    {msgs.map((m) => {
                        const meta = KIND_META[m.kind] || KIND_META.notice;
                        const Icon = meta.icon;
                        return (
                            <div
                                key={m.id}
                                className={`p-5 rounded-2xl bg-slate-900/50 border ${m.status === "sent" ? "border-emerald-500/30" : "border-slate-800"}`}
                            >
                                <div className="flex items-center gap-2 mb-1">
                                    <Icon className={`w-4 h-4 ${meta.color}`} />
                                    <span className="text-[10px] font-bold uppercase tracking-widest text-slate-500">
                                        {meta.label} · {new Date(m.created_at).toLocaleDateString()}
                                    </span>
                                    {m.status === "sent" && (
                                        <span className="ml-auto text-[10px] font-bold uppercase px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                                            Nuevo
                                        </span>
                                    )}
                                </div>
                                <h3 className="font-bold text-white text-sm mb-1">{m.subject}</h3>
                                <p className="text-xs text-slate-400 leading-relaxed mb-3">{m.body}</p>
                                {m.kind === "invite" && m.link_url && (
                                    <Link
                                        href={m.link_url}
                                        className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition-all"
                                    >
                                        Abrir invitación <ExternalLink className="w-3.5 h-3.5" />
                                    </Link>
                                )}
                                {m.kind === "password_reset" && (
                                    <p className="text-[11px] text-amber-300/90 bg-amber-500/10 border border-amber-500/20 rounded-lg px-3 py-2">
                                        Por tu seguridad el enlace vive en tu correo (o pídelo a tu facilitador).
                                        Si no fuiste tú, ignora este aviso.
                                    </p>
                                )}
                                {m.status === "sent" && (
                                    <button
                                        onClick={() => markRead(m.id)}
                                        className="mt-3 inline-flex items-center gap-1 text-[11px] text-slate-500 hover:text-emerald-400 transition-colors"
                                    >
                                        <Check className="w-3 h-3" /> Marcar leído
                                    </button>
                                )}
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}
