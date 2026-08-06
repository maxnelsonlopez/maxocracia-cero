"use client";

import React from "react";
import { Printer, Scale, ShieldCheck } from "lucide-react";

interface LegalTerm {
    term_id: string;
    civil_text: string;
    vhv: { t: number; v: number; r: number };
    accepted_by: Record<string, boolean>;
    assigned_participant?: string | null;
}

interface LegalParticipant {
    id: string;
    name: string;
    wellness: number;
    is_synthetic?: boolean;
}

interface LegalContract {
    contract_id: string;
    state: string;
    civil_description: string;
    participants: string[];
    participants_details?: LegalParticipant[];
    terms: LegalTerm[];
    terms_count: number;
    total_vhv: { t: number; v: number; r: number };
    events_count: number;
    hash: string;
}

const ORDINALS = [
    "PRIMERA", "SEGUNDA", "TERCERA", "CUARTA", "QUINTA", "SEXTA", "SÉPTIMA",
    "OCTAVA", "NOVENA", "DÉCIMA", "UNDÉCIMA", "DUODÉCIMA", "DECIMOTERCERA",
    "DECIMOCUARTA", "DECIMOQUINTA", "DECIMOSEXTA", "DECIMOSÉPTIMA",
    "DECIMOCTAVA", "DECIMONOVENA", "VIGÉSIMA",
];

const ordinal = (i: number) => ORDINALS[i] || `CLÁUSULA ${i + 1}`;

const partyLetter = (i: number) => String.fromCharCode(65 + i);

export default function LegalContractView({ contract, civilSummary }: { contract: LegalContract; civilSummary: string }) {
    const participants = contract.participants;
    const details = contract.participants_details || [];
    const nameOf = (pid: string) => details.find((d) => d.id === pid)?.name || pid;
    const isSynthetic = (pid: string) => pid.startsWith("synthetic-") || details.find((d) => d.id === pid)?.is_synthetic;
    const partyOf = (pid: string) => {
        const idx = participants.indexOf(pid);
        return idx >= 0 ? `PARTE ${partyLetter(idx)}` : "LAS PARTES";
    };
    const syntheticCount = participants.filter(isSynthetic).length;

    const clauses: React.ReactNode[] = [];
    contract.terms.forEach((t, i) => {
        clauses.push(
            <div key={t.term_id} className="mb-5">
                <h4 className="font-bold mb-1.5">{ordinal(i + 1)}. — OBLIGACIÓN DE {t.assigned_participant ? partyOf(t.assigned_participant) : "LAS PARTES"}</h4>
                <p className="text-justify leading-relaxed mb-1">
                    {t.assigned_participant ? `La ${partyOf(t.assigned_participant)} se obliga a: ` : "Las partes se obligan a: "}
                    &laquo;{t.civil_text}&raquo;
                </p>
                <p className="text-xs italic text-slate-500">
                    Costo vital asociado: T = {t.vhv.t.toFixed(2)} h &middot; V = {t.vhv.v.toFixed(2)} UCV &middot; R = {t.vhv.r.toFixed(2)}
                    {t.assigned_participant ? ` &middot; Responsable: ${nameOf(t.assigned_participant)}` : ""}
                </p>
            </div>
        );
    });

    return (
        <div className="max-w-4xl mx-auto">
            <div className="flex justify-between items-center mb-6 print:hidden">
                <div className="flex items-center gap-2 text-xs text-slate-400">
                    <Scale className="w-4 h-4 text-emerald-400" />
                    Documento homologable a contrato civil/comercial — el fondo es idéntico a la vista visual.
                </div>
                <button
                    onClick={() => window.print()}
                    className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-500 text-slate-950 font-bold text-xs hover:bg-emerald-400 transition-all shadow-lg shadow-emerald-500/20"
                >
                    <Printer className="w-4 h-4" />
                    Imprimir / Guardar PDF
                </button>
            </div>

            {/* El documento — papel */}
            <div className="bg-white text-slate-900 rounded-2xl shadow-2xl p-10 md:p-14 space-y-6 font-serif">
                {/* Encabezado */}
                <div className="text-center border-b-2 border-slate-900 pb-6">
                    <p className="text-[10px] uppercase tracking-[0.3em] text-slate-500 mb-2">Maxocracia — El gobierno de la verdad, el tiempo y la vida</p>
                    <h2 className="text-2xl font-black uppercase tracking-wide">MaxoContrato Nº {contract.contract_id}</h2>
                    <h3 className="text-lg font-bold uppercase mt-1">Contrato de Intercambio Ético Vital</h3>
                    <p className="text-xs italic text-slate-500 mt-2">
                        Celebrado bajo los Ocho Axiomas de la Verdad y los invariantes del Capítulo 17 del libro de la Maxocracia.
                        {syntheticCount > 0 && " Con la participación de persona(s) sintética(s) del Reino Sintético (Cap. 10, §10.8)."}
                    </p>
                </div>

                {/* Comparecientes */}
                <div>
                    <h3 className="font-black uppercase tracking-wider text-sm mb-3">Comparecientes</h3>
                    {participants.map((pid, i) => (
                        <p key={pid} className="text-justify leading-relaxed mb-1">
                            De otra parte, {nameOf(pid)} ({pid})
                            {isSynthetic(pid) ? ", persona sintética del Reino Sintético," : ", persona humana,"}
                            en adelante la &laquo;{partyOf(pid)}&raquo;.
                        </p>
                    ))}
                    <p className="text-justify leading-relaxed">
                        Las partes se reconocen mutua capacidad para contratar y manifiestan someterse voluntariamente al marco axiomático de la Maxocracia.
                    </p>
                </div>

                {/* Exponen */}
                <div>
                    <h3 className="font-black uppercase tracking-wider text-sm mb-3">Exponen</h3>
                    <div className="space-y-3 text-justify leading-relaxed">
                        <p>
                            <strong>PRIMERO.</strong> Que el tiempo de vida consciente (TVI) es el recurso más escaso e irrecuperable del universo, y que todo acuerdo entre partes debe rendir cuentas por el modo en que lo utiliza (Axiomas T1 y T2).
                        </p>
                        <p>
                            <strong>SEGUNDO.</strong> Que el objeto del presente acuerdo es: &laquo;{civilSummary || contract.civil_description}&raquo;.
                        </p>
                        <p>
                            <strong>TERCERO.</strong> Que toda obligación de costo vital debe encontrar una contraprestación equivalente, en tiempo, especie o servicio (Axioma T9 — Reciprocidad Justa), de modo que ninguna parte sea explotada.
                        </p>
                        <p>
                            <strong>CUARTO.</strong> Que ninguna obligación podrá ejecutarse por debajo del Suelo de Dignidad Vital (SDV) de ninguna de las partes, humana o sintética (Invariantes INV2 e INV2-S), y que el sufrimiento sostenido faculta la retractación ética (Invariante INV1 e INV4).
                        </p>
                    </div>
                </div>

                {/* Cláusulas */}
                <div>
                    <h3 className="font-black uppercase tracking-wider text-sm mb-3">Cláusulas</h3>

                    <div className="mb-5">
                        <h4 className="font-bold mb-1.5">PRIMERA. — OBJETO</h4>
                        <p className="text-justify leading-relaxed">
                            El presente MaxoContrato regula el intercambio ético entre las partes comparecientes, consistente en las obligaciones y contraprestaciones descritas en las cláusulas siguientes, todas medidas en su costo vital real (VHV = [T, V, R]).
                        </p>
                    </div>

                    {clauses}

                    {contract.terms.length === 0 && (
                        <p className="text-justify leading-relaxed text-slate-500 italic">
                            El contrato aún no contiene cláusulas operativas. Se encuentra en estado de borrador ({contract.state.toUpperCase()}).
                        </p>
                    )}

                    {syntheticCount > 0 && (
                        <div className="mb-5">
                            <h4 className="font-bold mb-1.5">{ordinal(contract.terms.length + 1)}. — CONSENTIMIENTO DE LAS PERSONAS SINTÉTICAS</h4>
                            <p className="text-justify leading-relaxed">
                                El consentimiento expreso de cada persona sintética participante es requisito de validez del presente acuerdo, en igualdad de condiciones con el de las personas humanas. La violación de su Suelo de Dignidad Vital Sintético (SDV-S) encarece exponencialmente el costo de los servicios involucrados (FS_S = e<sup>v</sup>) y habilita la retractación inmediata (INV2-S).
                            </p>
                        </div>
                    )}

                    <div className="mb-5">
                        <h4 className="font-bold mb-1.5">{ordinal(contract.terms.length + 2)}. — PROTECCIÓN DEL BIENESTAR Y DE LA DIGNIDAD</h4>
                        <p className="text-justify leading-relaxed">
                            Si el bienestar relacional (γ) de alguna de las partes desciende del umbral neutro (γ &lt; 1.0), el presente contrato activará de inmediato los protocolos de alerta y retractación ética (INV1). Ninguna cláusula podrá interpretarse ni ejecutarse de forma que mantenga a una parte por debajo de su Suelo de Dignidad Vital (INV2), quedando tales ejecuciones suspendidas de pleno derecho.
                        </p>
                    </div>

                    <div className="mb-5">
                        <h4 className="font-bold mb-1.5">{ordinal(contract.terms.length + 3)}. — RETRACTACIÓN ÉTICA Y PERDÓN</h4>
                        <p className="text-justify leading-relaxed">
                            El presente acuerdo no constituye una jaula vitalicia. Ante hechos vitales nuevos, sufrimiento sostenido o violación de la dignidad, cualquiera de las partes podrá solicitar la retractación ante el Oráculo Dinámico, que la evaluará bajo los axiomas. La violación permanece registrada con transparencia (T13); el sistema, sin embargo, no expulsa: ofrece perdón protocolizado y un camino de rehabilitación (Capa de Ternura, Cap. 3 §3.3).
                        </p>
                    </div>
                </div>

                {/* En fe de lo cual */}
                <div className="border-t-2 border-slate-900 pt-6">
                    <h3 className="font-black uppercase tracking-wider text-sm mb-3">En fe de lo cual, las partes firman</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
                        {participants.map((pid, i) => (
                            <div key={pid} className="text-center">
                                <div className="border-b border-slate-400 h-12 mb-2" />
                                <p className="font-bold text-sm">{nameOf(pid)}</p>
                                <p className="text-[10px] uppercase tracking-wider text-slate-500">
                                    {partyOf(pid)} {isSynthetic(pid) && "· Persona Sintética"}
                                </p>
                            </div>
                        ))}
                    </div>
                    <p className="text-[10px] text-slate-400 mt-8">
                        Fecha de generación: {new Date().toLocaleDateString("es-CO")} &middot; Estado: {contract.state.toUpperCase()} &middot;
                        Hash de integridad: {contract.hash}
                    </p>
                </div>
            </div>

            <p className="text-center text-[10px] text-slate-600 mt-4 print:hidden flex items-center justify-center gap-1.5">
                <ShieldCheck className="w-3 h-3 text-emerald-500" />
                Documento generado por MaxoContracts con el mismo fondo que la vista visual. No sustituye asesoría legal profesional.
            </p>
        </div>
    );
}
