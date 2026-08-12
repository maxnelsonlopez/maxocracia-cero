"use client";

import React, { useCallback, useEffect, useState } from "react";
import { Scale, Send, History, AlertTriangle, CheckCircle2 } from "lucide-react";
import { apiFetch } from "../lib/api";

interface ParliamentData {
    current: { alpha: number; beta: number; gamma: number; delta: number } | null;
    pending_proposals: Array<{ id: number; title: string; status: string; deadline: string | null }>;
    history: Array<{ proposal_id: number; alpha: number; beta: number; gamma: number; delta: number; applied_at: string }>;
    audit_hash: string;
}

const FIELDS: Array<{ key: "alpha" | "beta" | "gamma" | "delta"; label: string; hint: string; step: number }> = [
    { key: "alpha", label: "α · peso del tiempo", hint: "> 0 (no se ignora el tiempo)", step: 1 },
    { key: "beta", label: "β · peso de la vida", hint: "> 0 (no se ignora la vida)", step: 1 },
    { key: "gamma", label: "γ · aversión al sufrimiento", hint: "≥ 1 (nunca premiar el sufrimiento)", step: 0.1 },
    { key: "delta", label: "δ · recursos finitos", hint: "≥ 0 (no se ignoran los recursos)", step: 1 },
];

export default function ParlamentoParams() {
    const [data, setData] = useState<ParliamentData | null>(null);
    const [values, setValues] = useState<Record<string, string>>({});
    const [reason, setReason] = useState("");
    const [busy, setBusy] = useState(false);
    const [msg, setMsg] = useState<{ kind: "ok" | "err"; text: string } | null>(null);

    const load = useCallback(async () => {
        try {
            const res = await apiFetch("/voting/parliament/params");
            if (res.ok) {
                setData(await res.json());
            }
        } catch {
            // silencioso: el parlamento es auxiliar
        }
    }, []);

    useEffect(() => {
        load();
    }, [load]);

    // Pre-llenar el formulario con los pesos actuales solo si está vacío
    useEffect(() => {
        if (!data?.current || Object.keys(values).length > 0) return;
        const v: Record<string, string> = {};
        for (const f of FIELDS) v[f.key] = String(data.current[f.key]);
        setValues(v);
    }, [data, values]);

    const propose = async () => {
        setBusy(true);
        setMsg(null);
        try {
            const body: Record<string, number | string> = { reason };
            for (const f of FIELDS) body[f.key] = Number(values[f.key]);
            const res = await apiFetch("/voting/parliament/params", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
            });
            const parsed = await res.json().catch(() => ({}));
            if (!res.ok) {
                setMsg({ kind: "err", text: parsed.error || "No se pudo crear la propuesta" });
                return;
            }
            setMsg({
                kind: "ok",
                text: `Propuesta #${parsed.proposal.id} creada: exige consenso crítico del 75% (Cap. 14).`,
            });
            setReason("");
            load();
        } catch (err) {
            setMsg({ kind: "err", text: err instanceof Error ? err.message : "Error de conexión" });
        } finally {
            setBusy(false);
        }
    };

    const invalid = !data?.current || FIELDS.some((f) => {
        const n = Number(values[f.key]);
        if (!Number.isFinite(n)) return true;
        if (f.key === "gamma") return n < 1;
        if (f.key === "delta") return n < 0;
        return n <= 0;
    });

    return (
        <div className="bg-gradient-to-br from-violet-950/30 to-slate-900/40 border border-violet-500/20 rounded-2xl p-5 space-y-4">
            <div className="flex items-center justify-between gap-3 flex-wrap">
                <div>
                    <h2 className="text-sm font-bold text-white flex items-center gap-2">
                        <Scale className="w-4 h-4 text-violet-400" />
                        Parlamento de Parámetros
                        <span className="text-[9px] font-mono text-violet-400/70 uppercase tracking-widest">
                            Cap. 11 · Oráculo Dinámico
                        </span>
                    </h2>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                        La comunidad decide con cuánto peso la vida se valora (α, β, γ, δ).
                        Propuesta crítica: quórum 60% y consenso del 75%. Si se aprueba, se aplica con registro público (T13).
                    </p>
                </div>
                {data?.audit_hash && (
                    <span className="text-[9px] font-mono text-slate-600">audit {data.audit_hash}</span>
                )}
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {FIELDS.map((f) => (
                    <div key={f.key} className="space-y-1">
                        <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                            {f.label}
                        </label>
                        <input
                            type="number"
                            step={f.step}
                            min={f.key === "gamma" ? 1 : f.key === "delta" ? 0 : 0.1}
                            value={values[f.key] ?? ""}
                            onChange={(e) => setValues((v) => ({ ...v, [f.key]: e.target.value }))}
                            className="w-full px-3 py-2 text-sm font-mono rounded-xl bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-violet-500 text-white"
                        />
                        <p className="text-[9px] text-slate-600">{f.hint}</p>
                    </div>
                ))}
            </div>

            <div className="flex flex-col md:flex-row gap-3">
                <input
                    value={reason}
                    onChange={(e) => setReason(e.target.value)}
                    placeholder="Motivo del ajuste (auditable, T13)..."
                    className="flex-1 px-3 py-2 text-xs rounded-xl bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-violet-500 text-white placeholder:text-slate-600"
                />
                <button
                    onClick={propose}
                    disabled={busy || invalid}
                    className="flex items-center justify-center gap-2 px-4 py-2 rounded-xl bg-violet-500 hover:bg-violet-400 disabled:opacity-40 text-white text-xs font-bold transition-all"
                >
                    <Send className="w-3.5 h-3.5" />
                    {busy ? "Creando..." : "Proponer ajuste"}
                </button>
            </div>

            {msg && (
                <div className={`flex items-center gap-2 text-[11px] font-mono ${msg.kind === "ok" ? "text-emerald-400" : "text-rose-400"}`}>
                    {msg.kind === "ok" ? <CheckCircle2 className="w-3.5 h-3.5" /> : <AlertTriangle className="w-3.5 h-3.5" />}
                    {msg.text}
                </div>
            )}

            {data && data.history.length > 0 && (
                <div>
                    <div className="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-widest text-slate-500 mb-2">
                        <History className="w-3 h-3" />
                        Resoluciones de la comunidad
                    </div>
                    <div className="space-y-1.5">
                        {data.history.map((h) => (
                            <div key={h.proposal_id} className="flex items-center justify-between px-3 py-2 rounded-xl bg-slate-950/60 border border-slate-800 text-[10px] font-mono">
                                <span className="text-slate-400">
                                    propuesta #{h.proposal_id} · {h.applied_at?.slice(0, 10)}
                                </span>
                                <span className="text-violet-300">
                                    α {h.alpha} · β {h.beta} · γ {h.gamma} · δ {h.delta}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {data && data.pending_proposals.length > 0 && (
                <p className="text-[10px] font-mono text-amber-400/80">
                    {data.pending_proposals.length} propuesta{data.pending_proposals.length === 1 ? "" : "s"} de parámetros abierta{data.pending_proposals.length === 1 ? "" : "s"} en votación — vota en el TruthLedger.
                </p>
            )}
        </div>
    );
}
