"use client";

import React, { useEffect, useState } from "react";
import { apiFetch } from "../../lib/api";
import { Inbox, Copy, Check } from "lucide-react";

interface OutboxMsg {
    id: number;
    to_email: string;
    kind: string;
    subject: string;
    body: string;
    link_url: string | null;
    status: string;
    mail_status?: string | null;
    created_by: number | null;
    created_at: string;
}

function mailBadge(s?: string | null) {
    if (s === "sent") return <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">correo ✓</span>;
    if (s === "failed") return <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20">correo ✗</span>;
    if (s === "skipped") return <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20" title="Sin SMTP configurado: releva el enlace de viva voz">sin SMTP</span>;
    return <span className="text-xs text-slate-600">—</span>;
}

const FILTERS = [
    { key: "", label: "Todas" },
    { key: "invite", label: "Invitaciones" },
    { key: "password_reset", label: "Recuperaciones" },
    { key: "notice", label: "Avisos" },
];

export default function AdminInbox() {
    const [msgs, setMsgs] = useState<OutboxMsg[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [filter, setFilter] = useState("");
    const [copiedId, setCopiedId] = useState<number | null>(null);

    useEffect(() => {
        fetchOutbox(filter);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [filter]);

    async function fetchOutbox(kind: string) {
        try {
            setLoading(true);
            const res = await apiFetch(kind ? `/inbox/outbox?kind=${kind}` : "/inbox/outbox");
            if (!res.ok) throw new Error("Error cargando outbox (¿eres admin?)");
            setMsgs(await res.json());
        } catch (err) {
            setError(err instanceof Error ? err.message : "Error desconocido");
        } finally {
            setLoading(false);
        }
    }

    async function copyLink(m: OutboxMsg) {
        if (!m.link_url) return;
        try {
            await navigator.clipboard.writeText(`${window.location.origin}${m.link_url}`);
        } catch {
            const ta = document.createElement("textarea");
            ta.value = `${window.location.origin}${m.link_url}`;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand("copy");
            document.body.removeChild(ta);
        }
        setCopiedId(m.id);
        setTimeout(() => setCopiedId((c) => (c === m.id ? null : c)), 2000);
    }

    return (
        <div className="space-y-6">
            {error && (
                <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-semibold text-center">
                    ⚠️ {error}
                </div>
            )}
            <div className="flex flex-col sm:flex-row gap-4 justify-between items-center bg-slate-900/50 p-4 rounded-2xl border border-slate-800">
                <div className="flex items-center gap-2">
                    <Inbox className="w-4 h-4 text-emerald-500" />
                    <span className="text-sm font-bold text-white">Outbox del facilitador</span>
                    <span className="text-xs text-slate-500">releva de viva voz lo que el correo no entregó</span>
                </div>
                <div className="flex gap-2">
                    {FILTERS.map((f) => (
                        <button
                            key={f.key}
                            onClick={() => setFilter(f.key)}
                            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-colors ${filter === f.key ? "bg-emerald-500 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}
                        >
                            {f.label}
                        </button>
                    ))}
                </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm">
                        <thead className="bg-slate-800/50 text-slate-400 uppercase text-[10px] font-bold tracking-wider">
                            <tr>
                                <th className="px-6 py-4">Para</th>
                                <th className="px-6 py-4">Tipo</th>
                                <th className="px-6 py-4">Asunto</th>
                                <th className="px-6 py-4">Estado</th>
                                <th className="px-6 py-4">Correo</th>
                                <th className="px-6 py-4 text-right">Enlace</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800">
                            {loading ? (
                                <tr><td colSpan={6} className="px-6 py-12 text-center text-slate-500">Cargando outbox...</td></tr>
                            ) : msgs.length === 0 ? (
                                <tr><td colSpan={6} className="px-6 py-12 text-center text-slate-500">Nada por relevar. Genera una invitación desde Usuarios.</td></tr>
                            ) : msgs.map((m) => (
                                <tr key={m.id} className="hover:bg-slate-800/30 transition-colors">
                                    <td className="px-6 py-4">
                                        <div className="flex flex-col">
                                            <span className="text-xs text-white font-medium">{m.to_email}</span>
                                            <span className="text-[10px] text-slate-500">{new Date(m.created_at).toLocaleString()}</span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                                            {m.kind === "password_reset" ? "recuperación" : m.kind === "invite" ? "invitación" : m.kind}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 text-xs text-slate-300">{m.subject}</td>
                                    <td className="px-6 py-4 text-xs text-slate-500">{m.status === "read" ? "leído" : "enviado"}</td>
                                    <td className="px-6 py-4">{mailBadge(m.mail_status)}</td>
                                    <td className="px-6 py-4 text-right">
                                        {m.link_url ? (
                                            <button
                                                onClick={() => copyLink(m)}
                                                className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 hover:bg-emerald-500/20 transition-colors"
                                                title={m.kind === "password_reset" ? "Relevo sensible: entrégalo solo a su dueño" : "Copiar enlace"}
                                            >
                                                {copiedId === m.id ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                                                {copiedId === m.id ? "Copiado" : "Copiar"}
                                            </button>
                                        ) : (
                                            <span className="text-xs text-slate-600">—</span>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
            <p className="text-[11px] text-slate-600">
                Los enlaces de recuperación son sensibles: relévalos solo a su dueño y por un canal de confianza.
            </p>
        </div>
    );
}
