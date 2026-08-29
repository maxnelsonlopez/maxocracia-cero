"use client";

import React, { useCallback, useEffect, useState } from "react";
import { GraduationCap, Send, History, AlertTriangle, CheckCircle2, Lock } from "lucide-react";
import { apiFetch } from "../lib/api";
import InfoTip from "../components/ui/InfoTip";

interface ParlamentoEducativoData {
    current: { umbral_anios: number; provenance: string } | null;
    pending_proposals: Array<{ id: number; title: string; status: string; deadline: string | null }>;
    history: Array<{ proposal_id: number; umbral_anios: number; applied_at: string }>;
    audit_hash: string;
}

export default function ParlamentoEducativo() {
    const [data, setData] = useState<ParlamentoEducativoData | null>(null);
    const [umbral, setUmbral] = useState<string>("12");
    const [reason, setReason] = useState("");
    const [busy, setBusy] = useState(false);
    const [msg, setMsg] = useState<{ kind: "ok" | "err"; text: string } | null>(null);

    const load = useCallback(async () => {
        try {
            const res = await apiFetch("/voting/parliament/educativo");
            if (res.ok) {
                const parsed = await res.json();
                setData(parsed);
                if (parsed.current && Number.isFinite(Number(parsed.current.umbral_anios))) {
                    setUmbral(String(parsed.current.umbral_anios));
                }
            }
        } catch {
            // silencioso: el parlamento es auxiliar
        }
    }, []);

    useEffect(() => {
        load();
    }, [load]);

    const propose = async () => {
        setBusy(true);
        setMsg(null);
        try {
            const res = await apiFetch("/voting/parliament/educativo", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ umbral_anios: Number(umbral), reason }),
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

    const n = Number(umbral);
    const invalid = !data?.current || !Number.isFinite(n) || n < 12 || n > 30;

    return (
        <div className="bg-gradient-to-br from-emerald-950/30 to-slate-900/40 border border-emerald-500/20 rounded-2xl p-5 space-y-4">
            <div className="flex items-center justify-between gap-3 flex-wrap">
                <div>
                    <h2 className="text-sm font-bold text-white flex items-center gap-2">
                        <GraduationCap className="w-4 h-4 text-emerald-400" />
                        La escuela que queremos
                        <InfoTip
                            text="Parlamento Educativo: la comunidad vota cuántos años de estudio equivalen a una educación 'plena' en la medición del bienestar (el índice educativo). Si la comunidad vota 14, quien estudió la ley (12 años) sigue sin problemas legales, pero su índice baja porque el saber se olvida si no se mantiene (entropía del conocimiento)."
                        />
                        <span className="text-[9px] font-mono text-emerald-400/70 uppercase tracking-widest">
                            rama educativa
                        </span>
                    </h2>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                        La comunidad decide cuántos años de estudio cuentan como "educación completa".
                        El piso legal (12 años) no se toca. Decisión seria: 60% de participación y 75% de acuerdo.
                    </p>
                </div>
                {data?.audit_hash && (
                    <span className="text-[9px] font-mono text-slate-600">audit {data.audit_hash}</span>
                )}
            </div>

            <div className="flex items-center gap-3 flex-wrap">
                <span className="text-sm text-white font-mono">
                    Ahora mismo:{" "}
                    <b className="text-emerald-300">{data?.current ? `${data.current.umbral_anios} años` : "…"}</b>
                    <span className="text-[10px] text-slate-500 ml-2">
                        {data?.current?.provenance === "canon_sdv_h"
                            ? "· el valor de siempre (aún no votado)"
                            : data?.current?.provenance === "comunidad"
                                ? "· lo que decidió la comunidad"
                                : ""}
                    </span>
                </span>
            </div>

            <div className="flex flex-col md:flex-row gap-3 items-end">
                <div className="flex-1 space-y-1">
                    <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                        ¿Cuántos años de estudio = "pleno"? (12–30)
                        <InfoTip
                            text="Ejemplo sencillo: hoy el sistema dice que 12 años de estudio es lo pleno. La comunidad puede votar 14 porque la vida es aprendizaje continuo y el conocimiento se olvida. Quedan fijos, sin importar la votación: el piso legal de 12 años y que quien no reporta sus años no se castiga."
                        />
                    </label>
                    <input
                        type="number"
                        step={0.1}
                        min={12}
                        max={30}
                        value={umbral}
                        onChange={(e) => setUmbral(e.target.value)}
                        className="w-full px-3 py-2 text-sm font-mono rounded-xl bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500 text-white"
                    />
                </div>
                <div className="flex-1 space-y-1">
                    <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                        Motivo (auditable, T13)
                    </label>
                    <input
                        value={reason}
                        onChange={(e) => setReason(e.target.value)}
                        placeholder="¿Por qué este umbral? (la comunidad lo leerá)"
                        className="w-full px-3 py-2 text-xs rounded-xl bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500 text-white placeholder:text-slate-600"
                    />
                </div>
                <button
                    onClick={propose}
                    disabled={busy || invalid}
                    className="flex items-center justify-center gap-2 px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 disabled:opacity-40 text-white text-xs font-bold transition-all"
                >
                    <Send className="w-3.5 h-3.5" />
                    {busy ? "Creando..." : "Proponer umbral"}
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
                                <span className="text-emerald-300">{h.umbral_anios} años</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {data && data.pending_proposals.length > 0 && (
                <p className="text-[10px] font-mono text-amber-400/80">
                    {data.pending_proposals.length} propuesta{data.pending_proposals.length === 1 ? "" : "s"} educativa{data.pending_proposals.length === 1 ? "" : "s"} abierta{data.pending_proposals.length === 1 ? "" : "s"} en votación.
                </p>
            )}

            <p className="text-[9px] text-slate-600 flex items-start gap-1.5">
                <Lock className="w-3 h-3 mt-0.5 shrink-0" />
                Lo que no se vota: el piso legal de 12 años. Y el número no puede saltar de un día
                para otro: entre cambios se espera una ventana de 14 días.
                <InfoTip
                    text="La decisión se registra públicamente (T13): quién la propuso, por qué, cuántos votó y cuándo se aplicó. Con la ventana de 14 días, la comunidad evita que el número 'rebote' cada semana por capricho."
                />
            </p>
        </div>
    );
}
