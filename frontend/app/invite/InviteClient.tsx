"use client";

import React, { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { HeartPulse, Handshake, Landmark, Mail, ShieldCheck, ArrowRight } from "lucide-react";
import { apiFetch } from "../lib/api";

interface InviteInfo {
    valid: boolean;
    email_masked: string;
    already_registered: boolean;
    welcome: string;
    register_url: string;
}

export default function InviteClient() {
    const searchParams = useSearchParams();
    const token = searchParams.get("t") || "";
    const [info, setInfo] = useState<InviteInfo | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    useEffect(() => {
        if (!token) return; // sin token: el render muestra la invitación inválida
        apiFetch(`/invite/${encodeURIComponent(token)}`)
            .then((res) => (res.ok ? res.json() : null))
            .then((data: InviteInfo | null) => {
                if (!data) setError(true);
                else setInfo(data);
            })
            .catch(() => setError(true))
            .finally(() => setLoading(false));
    }, [token]);

    const invalid = !token || error;

    const steps = [
        { icon: HeartPulse, title: "Primero, tu pulso", body: "Reporta cómo te sientes cuando quieras. Un toque. Nadie te pide más." },
        { icon: Handshake, title: "Luego, tu acuerdo", body: "Cuando llegue el momento, firmas con ayuda: en voz alta, con tus palabras, a tu ritmo." },
        { icon: Landmark, title: "La voz llega sola", body: "La gobernanza no es una prisa: se gana caminando tu primer acuerdo. La comunidad decide." },
    ];

    return (
        <div className="min-h-screen bg-slate-950 text-slate-200">
            <div className="max-w-3xl mx-auto px-4 sm:px-6 py-16 space-y-10">
                {loading ? (
                    <div className="text-center text-sm text-slate-500 animate-pulse pt-24">Abriendo la puerta…</div>
                ) : invalid ? (
                    <div className="text-center pt-24 space-y-3">
                        <div className="text-4xl">🕊️</div>
                        <h1 className="text-2xl font-black text-white">Esta invitación no es válida</h1>
                        <p className="text-sm text-slate-400 max-w-md mx-auto">
                            Las invitaciones de la Cohorte se entregan de persona a persona.
                            Si crees que es un error, pide una nueva invitación a quien te la envió.
                        </p>
                    </div>
                ) : info ? (
                    <>
                        {/* Bienvenida */}
                        <div className="text-center space-y-4">
                            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 text-[11px] font-bold uppercase tracking-widest">
                                <Mail className="w-3.5 h-3.5" />
                                Invitado · {info.email_masked}
                            </div>
                            <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
                                {info.already_registered
                                    ? "Ya eres parte de la Cohorte"
                                    : "Te estábamos esperando"}
                            </h1>
                            <p className="text-slate-400 max-w-xl mx-auto leading-relaxed">
                                {info.welcome}
                            </p>
                            <blockquote className="text-emerald-400/90 text-sm italic max-w-xl mx-auto">
                                &quot;No eres un cliente: eres un futuro vecino. Aquí nadie llega
                                corriendo — todos llegamos cuando es el momento.&quot;
                            </blockquote>
                        </div>

                        {/* La escalera, sin prisa */}
                        {!info.already_registered && (
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                {steps.map((s, i) => (
                                    <div key={i} className="p-5 rounded-2xl bg-slate-900/50 backdrop-blur-xl border border-slate-800">
                                        <div className="p-2.5 rounded-xl border border-emerald-500/20 bg-emerald-500/10 text-emerald-400 w-fit mb-3">
                                            <s.icon className="w-5 h-5" />
                                        </div>
                                        <h3 className="font-bold text-white text-sm mb-1">{s.title}</h3>
                                        <p className="text-[11px] text-slate-400 leading-relaxed">{s.body}</p>
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* Acción */}
                        <div className="text-center">
                            {info.already_registered ? (
                                <Link
                                    href="/login"
                                    className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-bold transition-all"
                                >
                                    Entrar a la Cohorte <ArrowRight className="w-4 h-4" />
                                </Link>
                            ) : (
                                <Link
                                    href={info.register_url}
                                    className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-bold transition-all shadow-lg shadow-emerald-500/20"
                                >
                                    <ShieldCheck className="w-4 h-4" />
                                    Crear mi cuenta (sin prisa)
                                </Link>
                            )}
                            <p className="text-[10px] text-slate-600 mt-3 font-mono">
                                Tu email ya está esperándote en el formulario. La invitación no caduca.
                            </p>
                        </div>
                    </>
                ) : null}
            </div>
        </div>
    );
}
