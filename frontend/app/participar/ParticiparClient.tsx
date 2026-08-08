"use client";

import React, { useState } from "react";
import {
    HeartPulse,
    Handshake,
    Gift,
    Landmark,
    Volume2,
    VolumeX,
    ShieldCheck,
    Clock,
    Scale,
    HeartHandshake,
} from "lucide-react";

const CAMINOS = [
    {
        icon: HeartPulse,
        level: "Camino 1",
        title: "El Pulso",
        subtitle: "Una persona, un latido",
        color: "text-emerald-400 border-emerald-500/20 bg-emerald-500/10",
        body: "Reporta cómo te sientes una vez por semana — o cuando haga falta. Un toque: “¿cómo estás hoy?”. No necesitas entender contratos para cuidar de ti. Si tu bienestar baja, el sistema se entera al instante.",
    },
    {
        icon: Handshake,
        level: "Camino 2",
        title: "El Acuerdo",
        subtitle: "Recibir y pedir ayuda",
        color: "text-amber-400 border-amber-500/20 bg-amber-500/10",
        body: "Firma contratos de ayuda con firma asistida: el texto se lee en voz alta, se firma cláusula por cláusula con tus propias palabras y puedes traer un co-testigo. Nadie firma por ti y retractarte es tu derecho.",
    },
    {
        icon: Gift,
        level: "Camino 3",
        title: "La Oferta",
        subtitle: "Ofrecer tiempo y talento",
        color: "text-blue-400 border-blue-500/20 bg-blue-500/10",
        body: "Publica en palabras sencillas lo que sabes hacer: cocinar, acompañar, arreglar, enseñar. Cuando alguien lo necesita, el sistema redacta el borrador del acuerdo por ti. Tu tiempo vale igual que el recibido.",
    },
    {
        icon: Landmark,
        level: "Camino 4",
        title: "La Gobernanza",
        subtitle: "Cuidar la casa común",
        color: "text-violet-400 border-violet-500/20 bg-violet-500/10",
        body: "Vota, delega, audita en la plaza pública y verifica contratos por su huella. Todo es verificable. La mayoría de la comunidad no necesita llegar aquí: la gobernanza es un servicio voluntario, no un requisito.",
    },
];

const REGLAS_INTEGRANTE = [
    "Cuida tu latido. Reporta cómo te sientes. Es un acto de verdad, no un trámite.",
    "No firmes lo que no entiendes. Pide que te lo lean. Dilo con tus propias palabras. Trae a alguien de confianza si quieres.",
    "Tu tiempo vale igual que el de cualquiera. Si un acuerdo te parece injusto, no lo firmes.",
    "Nadie te puede obligar a quedarte. Retractarte es tu derecho. Si tu bienestar baja, el sistema te protege antes que el trámite.",
    "La tecnología es tu herramienta, no tu juez. Las máquinas calculan. Las personas deciden.",
    "Si algo te resulta difícil, pide la ruta sencilla. Existe, y es tuya.",
    "Lo que haces y recibes queda a la vista. La transparencia es tu escudo. Tu vida íntima es sagrada: nadie la audita.",
    "El error no se castiga: se repara. El sistema no expulsa: reintegra.",
];

const REGLAS_PROCESOS = [
    "La complejidad nunca se traslada a la persona. El sistema se adapta a tu capacidad, no al revés.",
    "El lenguaje civil es ley. Si un estudiante de octavo grado no lo entiende, no es un buen contrato.",
    "El bienestar manda sobre el trámite. Cualquier proceso se pausa si alguien sufre.",
    "Nadie queda afuera por capacidad. Lectura en voz alta, paráfrasis y co-testigos son el diseño, no un extra.",
    "Sin la palabra de la persona no hay consentimiento. Nadie firma por ti.",
    "Cada persona participa a su ritmo. La escalera es un camino, no una carrera.",
    "El sistema no expulsa: repara y reintegra. Los errores se corrigen con ternura, no con exclusión.",
    "La plaza es de todos. Cualquier ciudadano — con o sin cuenta — puede verificar un contrato.",
];

export default function ParticiparClient() {
    const [reading, setReading] = useState(false);

    const handleListen = () => {
        if (typeof window === "undefined" || !("speechSynthesis" in window)) {
            alert("Tu navegador no soporta lectura en voz alta.");
            return;
        }
        if (reading) {
            window.speechSynthesis.cancel();
            setReading(false);
            return;
        }
        const text = [
            "Cómo participar en la Maxocracia.",
            "El sistema es complejo; la participación no tiene por qué serlo. La complejidad la cargan las máquinas; la dignidad la vive cada persona.",
            ...CAMINOS.map((c) => `${c.level}, ${c.title}. ${c.subtitle}. ${c.body}`),
            "Tus reglas de oro.",
            ...REGLAS_INTEGRANTE,
            "Las reglas que los procesos deben cumplir contigo.",
            ...REGLAS_PROCESOS,
        ].join(". ");
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "es-ES";
        utterance.onend = () => setReading(false);
        utterance.onerror = () => setReading(false);
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
        setReading(true);
    };

    return (
        <div className="min-h-screen bg-slate-950 text-slate-200">
            <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-14 space-y-12">
                {/* Cabecera */}
                <div className="text-center space-y-4">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 text-[11px] font-bold uppercase tracking-widest">
                        <HeartHandshake className="w-3.5 h-3.5" />
                        Una vida digna para todos
                    </div>
                    <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
                        Cómo Participar
                    </h1>
                    <blockquote className="text-emerald-400/90 text-sm italic max-w-2xl mx-auto leading-relaxed">
                        &quot;El sistema es complejo; la participación no tiene por qué serlo.
                        La complejidad la cargan las máquinas; la dignidad la vive cada persona.&quot;
                    </blockquote>
                    <button
                        onClick={handleListen}
                        className={`inline-flex items-center gap-2 px-4 py-2 rounded-xl border text-xs font-bold transition-all ${
                            reading
                                ? "bg-rose-500/10 border-rose-500/30 text-rose-300"
                                : "bg-slate-900/60 border-slate-700 text-slate-300 hover:border-emerald-500/40 hover:text-emerald-300"
                        }`}
                    >
                        {reading ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
                        {reading ? "Detener lectura" : "Escuchar esta guía en voz alta"}
                    </button>
                </div>

                {/* La escalera */}
                <div>
                    <h2 className="text-sm font-black uppercase tracking-widest text-slate-400 mb-4 flex items-center gap-2">
                        <Scale className="w-4 h-4 text-emerald-500" />
                        La escalera de participación
                        <span className="text-slate-600 normal-case font-normal tracking-normal text-xs">
                            (caminos, no niveles: todos valen lo mismo)
                        </span>
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {CAMINOS.map((c) => (
                            <div key={c.title} className="p-5 rounded-2xl bg-slate-900/50 backdrop-blur-xl border border-slate-800 hover:border-slate-700 transition-all">
                                <div className="flex items-start justify-between gap-3 mb-3">
                                    <div className={`p-2.5 rounded-xl border ${c.color}`}>
                                        <c.icon className="w-5 h-5" />
                                    </div>
                                    <span className="text-[9px] font-mono text-slate-500 uppercase tracking-widest">{c.level}</span>
                                </div>
                                <h3 className="font-bold text-white">{c.title}</h3>
                                <div className="text-[11px] text-slate-500 mb-2">{c.subtitle}</div>
                                <p className="text-xs text-slate-400 leading-relaxed">{c.body}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Reglas del integrante */}
                <div>
                    <h2 className="text-sm font-black uppercase tracking-widest text-slate-400 mb-4 flex items-center gap-2">
                        <HeartPulse className="w-4 h-4 text-rose-400" />
                        Tus reglas de oro
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {REGLAS_INTEGRANTE.map((r, i) => (
                            <div key={i} className="flex items-start gap-3 p-4 rounded-2xl bg-slate-900/50 backdrop-blur-xl border border-slate-800">
                                <span className="w-6 h-6 shrink-0 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[11px] font-black flex items-center justify-center">
                                    {i + 1}
                                </span>
                                <p className="text-xs text-slate-300 leading-relaxed">{r}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Reglas de los procesos */}
                <div>
                    <h2 className="text-sm font-black uppercase tracking-widest text-slate-400 mb-4 flex items-center gap-2">
                        <ShieldCheck className="w-4 h-4 text-emerald-500" />
                        Lo que los procesos deben cumplir contigo
                    </h2>
                    <div className="p-5 rounded-2xl bg-emerald-500/5 border border-emerald-500/20 backdrop-blur-xl">
                        <ul className="space-y-3">
                            {REGLAS_PROCESOS.map((r, i) => (
                                <li key={i} className="flex items-start gap-3 text-xs text-slate-300 leading-relaxed">
                                    <Clock className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                                    {r}
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>

                {/* Cierre */}
                <div className="text-center pt-4">
                    <p className="text-sm text-slate-400 max-w-2xl mx-auto leading-relaxed">
                        No importa si la complejidad te resulta fácil o difícil:{" "}
                        <strong className="text-white">tu lugar está garantizado</strong>.
                        El tiempo de vida consciente tiene igual dignidad para cualquier
                        participante. La escalera no es una carrera — es un camino donde
                        todos llegamos a la misma casa.
                    </p>
                </div>
            </div>
        </div>
    );
}
