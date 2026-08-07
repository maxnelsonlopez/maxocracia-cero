"use client";

import React, { useEffect, useState } from "react";
import {
    Landmark,
    Search,
    ShieldCheck,
    ShieldX,
    HeartPulse,
    FileCheck2,
    AlertTriangle,
    Activity,
    Layers,
    Scale,
    Lock,
} from "lucide-react";
import { apiFetch } from "../lib/api";

interface VerifierTerm {
    term_id: string;
    civil_text: string;
    vhv: { t: number; v: number; r: number };
    assigned_participant?: string | null;
}

interface VerifierParticipant {
    participant_id: string;
    party_type: string;
    is_collective: boolean;
    wellness: number;
    checkins_count: number;
    last_checkin_wellness?: number | null;
    last_checkin_at?: string | null;
}

interface VerifierContract {
    contract_id: string;
    state: string;
    civil_description: string;
    created_at?: string | null;
    canonical_hash: string;
    hash_matches: boolean | null;
    total_vhv: { t: number; v: number; r: number };
    terms_count: number;
    terms: VerifierTerm[];
    participants: VerifierParticipant[];
    events_count: number;
    asymmetry: { obligations?: Record<string, number>; max_party?: string; max_share?: number } | null;
}

interface VerifierCohort {
    plaza: string;
    totals: {
        contracts: number;
        states: Record<string, number>;
        terms: number;
        checkins_total: number;
        tvi_total_h: number;
        vhv_v: number;
        vhv_h: number;
        parties: number;
    };
    wellness: {
        avg: number | null;
        with_latido: number;
        without_latido: number;
        source: string | null;
    };
}

const STATE_LABELS: Record<string, { label: string; color: string }> = {
    draft: { label: "Borrador", color: "text-slate-400 border-slate-700" },
    pending: { label: "En firma", color: "text-amber-400 border-amber-500/30" },
    active: { label: "Activo", color: "text-emerald-400 border-emerald-500/30" },
    executed: { label: "Ejecutado", color: "text-blue-400 border-blue-500/30" },
    retracted: { label: "Retractado", color: "text-rose-400 border-rose-500/30" },
};

const PARTY_TYPE_LABELS: Record<string, string> = {
    human: "Persona",
    synthetic: "Sintética",
    society: "Micro-sociedad",
    cooperative: "Cooperativa",
    institution: "Institución",
    ecosystem: "Ecosistema",
};

export default function VerificadorClient() {
    const [contractId, setContractId] = useState("");
    const [expectedHash, setExpectedHash] = useState("");
    const [contract, setContract] = useState<VerifierContract | null>(null);
    const [verifying, setVerifying] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [cohort, setCohort] = useState<VerifierCohort | null>(null);
    const [cohortLoading, setCohortLoading] = useState(true);

    useEffect(() => {
        apiFetch("/verificador/cohort")
            .then((res) => {
                if (!res.ok) throw new Error("Error al obtener métricas de la plaza");
                return res.json();
            })
            .then((data: VerifierCohort) => setCohort(data))
            .catch(() => setCohort(null))
            .finally(() => setCohortLoading(false));
    }, []);

    const verify = async () => {
        const id = contractId.trim();
        if (!id) return;
        setVerifying(true);
        setError(null);
        try {
            const qs = new URLSearchParams();
            if (expectedHash.trim()) qs.set("hash", expectedHash.trim());
            const res = await apiFetch(`/verificador/contract/${encodeURIComponent(id)}?${qs.toString()}`);
            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                setContract(null);
                setError(data.error || "Contrato no encontrado en la plaza");
                return;
            }
            setContract(await res.json());
        } catch (err) {
            setContract(null);
            setError(err instanceof Error ? err.message : "Error de conexión con la plaza");
        } finally {
            setVerifying(false);
        }
    };

    const submit = (e: React.FormEvent) => {
        e.preventDefault();
        verify();
    };

    return (
        <div className="min-h-screen bg-slate-950 text-slate-200">
            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
                {/* Cabecera */}
                <div className="text-center mb-12">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 text-[11px] font-bold uppercase tracking-widest mb-4">
                        <Landmark className="w-3.5 h-3.5" />
                        T13 · Transparencia Radical · Sin login
                    </div>
                    <h1 className="text-3xl sm:text-4xl font-black text-white mb-3">
                        La Plaza Pública
                    </h1>
                    <p className="text-slate-400 max-w-2xl mx-auto text-sm leading-relaxed">
                        Cualquier persona puede auditar la integridad de un contrato por su{" "}
                        <strong className="text-slate-200">hash canónico</strong> y mirar el
                        bienestar agregado del barrio. Nadie necesita cuenta: la transparencia
                        no pide permiso.
                    </p>
                </div>

                {/* Verificador de integridad */}
                <div className="glass p-6 rounded-3xl border border-slate-900 bg-slate-900/30 mb-8">
                    <div className="flex items-center gap-2 mb-5">
                        <Search className="w-5 h-5 text-emerald-500" />
                        <h2 className="text-lg font-bold text-white uppercase tracking-wider">
                            Verificador Ciudadano
                        </h2>
                    </div>
                    <form onSubmit={submit} className="grid grid-cols-1 md:grid-cols-12 gap-3">
                        <div className="md:col-span-5">
                            <input
                                type="text"
                                value={contractId}
                                onChange={(e) => setContractId(e.target.value)}
                                placeholder="ID del contrato (ej: loan-001)"
                                className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm font-mono text-slate-300 focus:outline-none focus:border-emerald-500/40"
                            />
                        </div>
                        <div className="md:col-span-5">
                            <input
                                type="text"
                                value={expectedHash}
                                onChange={(e) => setExpectedHash(e.target.value)}
                                placeholder="Hash sellado (opcional, para comparar)"
                                className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-sm font-mono text-slate-400 focus:outline-none focus:border-emerald-500/40"
                            />
                        </div>
                        <div className="md:col-span-2">
                            <button
                                type="submit"
                                disabled={verifying || !contractId.trim()}
                                className="w-full px-4 py-2.5 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 text-white text-sm font-bold rounded-xl transition-all flex items-center justify-center gap-2"
                            >
                                {verifying ? (
                                    <span className="animate-pulse">Auditando…</span>
                                ) : (
                                    <>
                                        <ShieldCheck className="w-4 h-4" />
                                        Auditar
                                    </>
                                )}
                            </button>
                        </div>
                    </form>

                    {error && (
                        <div className="mt-4 p-3.5 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
                            <AlertTriangle className="w-4 h-4 shrink-0" />
                            {error}
                        </div>
                    )}

                    {contract && (
                        <div className="mt-6 space-y-6">
                            {/* Veredicto */}
                            <div
                                className={`p-4 rounded-2xl border flex items-start gap-3 ${
                                    contract.hash_matches === false
                                        ? "bg-rose-500/10 border-rose-500/40"
                                        : "bg-emerald-500/10 border-emerald-500/40"
                                }`}
                            >
                                {contract.hash_matches === false ? (
                                    <ShieldX className="w-6 h-6 text-rose-400 shrink-0" />
                                ) : (
                                    <ShieldCheck className="w-6 h-6 text-emerald-400 shrink-0" />
                                )}
                                <div>
                                    <div className="font-black text-sm uppercase tracking-wider text-white">
                                        {contract.hash_matches === false
                                            ? "El hash NO coincide: el acuerdo fue alterado o el hash es de otro contrato"
                                            : contract.hash_matches === true
                                              ? "Integridad confirmada: el hash sellado coincide con el acuerdo"
                                              : "Huella de integridad recomputada (T13)"}
                                    </div>
                                    <div className="text-[11px] font-mono text-slate-400 break-all mt-1">
                                        {contract.canonical_hash}
                                    </div>
                                    {contract.hash_matches === true && (
                                        <div className="text-[11px] text-emerald-300 mt-1">
                                            Este contrato puede recomputarse sin servidor: su huella
                                            cubre id, descripción, partes, términos y VHV total.
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* Datos del contrato */}
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                                <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-900">
                                    <div className="text-[10px] uppercase tracking-widest text-slate-500 mb-1">
                                        Estado
                                    </div>
                                    <div>
                                        {STATE_LABELS[contract.state] ? (
                                            <span
                                                className={`text-xs font-black px-2 py-1 rounded-full border ${STATE_LABELS[contract.state].color}`}
                                            >
                                                {STATE_LABELS[contract.state].label}
                                            </span>
                                        ) : (
                                            <span className="text-xs font-mono text-slate-300">{contract.state}</span>
                                        )}
                                    </div>
                                </div>
                                <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-900">
                                    <div className="text-[10px] uppercase tracking-widest text-slate-500 mb-1">
                                        TVI comprometido
                                    </div>
                                    <div className="text-lg font-black font-mono text-emerald-400">
                                        {contract.total_vhv.t.toFixed(1)}h
                                    </div>
                                </div>
                                <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-900">
                                    <div className="text-[10px] uppercase tracking-widest text-slate-500 mb-1">
                                        Cláusulas · Eventos
                                    </div>
                                    <div className="text-lg font-black font-mono text-slate-200">
                                        {contract.terms_count} · {contract.events_count}
                                    </div>
                                </div>
                            </div>

                            {/* Términos */}
                            <div>
                                <div className="flex items-center gap-2 mb-2">
                                    <FileCheck2 className="w-4 h-4 text-blue-400" />
                                    <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400">
                                        Cláusulas del acuerdo (lenguaje civil)
                                    </h3>
                                </div>
                                <div className="space-y-2">
                                    {contract.terms.map((t, i) => (
                                        <div
                                            key={t.term_id}
                                            className="p-3.5 rounded-2xl bg-slate-950/70 border border-slate-900 flex items-start justify-between gap-3"
                                        >
                                            <div>
                                                <div className="text-xs font-bold text-slate-200">
                                                    {i + 1}. {t.civil_text}
                                                </div>
                                                {t.assigned_participant && (
                                                    <div className="text-[10px] font-mono text-slate-500 mt-1">
                                                        Obligada: {t.assigned_participant}
                                                    </div>
                                                )}
                                            </div>
                                            <div className="text-[10px] font-mono text-slate-500 shrink-0">
                                                {t.vhv.t}h · V{t.vhv.v} · R{t.vhv.r}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Partes */}
                            <div>
                                <div className="flex items-center gap-2 mb-2">
                                    <HeartPulse className="w-4 h-4 text-emerald-400" />
                                    <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400">
                                        Partes y su γ (último latido)
                                    </h3>
                                </div>
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                                    {contract.participants.map((p) => (
                                        <div
                                            key={p.participant_id}
                                            className="p-3.5 rounded-2xl bg-slate-950/70 border border-slate-900"
                                        >
                                            <div className="flex justify-between items-center">
                                                <span className="text-xs font-bold text-slate-200 font-mono">
                                                    {p.participant_id}
                                                </span>
                                                <span
                                                    className={`text-xs font-mono ${
                                                        p.wellness < 0.8 ? "text-rose-400" : "text-emerald-400"
                                                    }`}
                                                >
                                                    γ = {p.wellness.toFixed(2)}
                                                </span>
                                            </div>
                                            <div className="flex justify-between items-center mt-1.5">
                                                <span className="text-[9px] font-mono text-slate-500">
                                                    {PARTY_TYPE_LABELS[p.party_type] || p.party_type} ·{" "}
                                                    {p.checkins_count} latido{p.checkins_count === 1 ? "" : "s"}
                                                </span>
                                                {p.last_checkin_wellness != null && (
                                                    <span className="text-[9px] font-mono text-slate-600">
                                                        último {p.last_checkin_wellness.toFixed(2)}{" "}
                                                        {p.last_checkin_at ? `· ${p.last_checkin_at.slice(0, 10)}` : ""}
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Bienestar agregado del barrio */}
                <div className="glass p-6 rounded-3xl border border-slate-900 bg-slate-900/30">
                    <div className="flex items-center gap-2 mb-5">
                        <Activity className="w-5 h-5 text-emerald-500" />
                        <h2 className="text-lg font-bold text-white uppercase tracking-wider">
                            La Economía de la Vida · Cohorte Cero
                        </h2>
                    </div>

                    {cohortLoading ? (
                        <div className="text-xs text-slate-500 animate-pulse">Leyendo el pulso del barrio…</div>
                    ) : cohort ? (
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                            <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-900">
                                <div className="text-[10px] uppercase tracking-widest text-slate-500 mb-1 flex items-center gap-1">
                                    <Scale className="w-3 h-3" /> Contratos
                                </div>
                                <div className="text-xl font-black font-mono text-white">
                                    {cohort.totals.contracts}
                                </div>
                                <div className="text-[9px] font-mono text-slate-500 mt-1">
                                    {cohort.totals.states.active} activos · {cohort.totals.states.executed} ejecutados
                                </div>
                            </div>
                            <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-900">
                                <div className="text-[10px] uppercase tracking-widest text-slate-500 mb-1 flex items-center gap-1">
                                    <HeartPulse className="w-3 h-3" /> γ del barrio
                                </div>
                                <div className={`text-xl font-black font-mono ${(cohort.wellness.avg ?? 1) < 0.8 ? "text-rose-400" : "text-emerald-400"}`}>
                                    {cohort.wellness.avg != null ? cohort.wellness.avg.toFixed(3) : "—"}
                                </div>
                                <div className="text-[9px] font-mono text-slate-500 mt-1">
                                    {cohort.wellness.with_latido} con latido real · fuente: {cohort.wellness.source || "n/a"}
                                </div>
                            </div>
                            <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-900">
                                <div className="text-[10px] uppercase tracking-widest text-slate-500 mb-1 flex items-center gap-1">
                                    <Layers className="w-3 h-3" /> TVI en juego
                                </div>
                                <div className="text-xl font-black font-mono text-emerald-400">
                                    {cohort.totals.tvi_total_h.toFixed(1)}h
                                </div>
                                <div className="text-[9px] font-mono text-slate-500 mt-1">
                                    {cohort.totals.terms} cláusulas · {cohort.totals.checkins_total} latidos
                                </div>
                            </div>
                            <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-900">
                                <div className="text-[10px] uppercase tracking-widest text-slate-500 mb-1 flex items-center gap-1">
                                    <Lock className="w-3 h-3" /> Colectivas
                                </div>
                                <div className="text-xl font-black font-mono text-white">
                                    {cohort.totals.parties}
                                </div>
                                <div className="text-[9px] font-mono text-slate-500 mt-1">
                                    cooperativas · instituciones · ecosistemas
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="text-xs text-slate-500">La plaza aún no tiene métricas agregadas.</div>
                    )}
                </div>
            </div>
        </div>
    );
}
