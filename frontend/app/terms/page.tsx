import { Metadata } from "next";
import { Scale, FlaskConical, HeartHandshake, BookOpen } from "lucide-react";

export const metadata: Metadata = {
    title: "Términos y Coherencia - Maxocracia",
    description:
        "Términos de uso del proyecto Maxocracia: experimento abierto de ingeniería social, licencia libre y coherencia axiomática.",
};

const sections = [
    {
        icon: FlaskConical,
        title: "Un experimento abierto",
        body: "Maxocracia es un proyecto experimental de ingeniería social en validación (Cohorte Cero, Bogotá, 90 días). Las herramientas se ofrecen tal cual, sin garantías de ningún tipo, explícitas o implícitas. Participas como pionero en un laboratorio de coherencia, no como consumidor de un producto terminado.",
    },
    {
        icon: HeartHandshake,
        title: "Participación voluntaria",
        body: "Toda participación es voluntaria y reversible. Nadie es obligado a medir, registrar ni intercambiar. Puedes pausar o retirarte en cualquier momento sin penalización, como establece la MicroMaxocracia (Nivel 0-4) y el Protocolo de Aborto de la Cohorte Cero cuando el sistema genera más daño que claridad.",
    },
    {
        icon: Scale,
        title: "Marco axiomático",
        body: "Este proyecto se rige por los Ocho Axiomas de la Verdad y los axiomas temporales T0-T15. Toda decisión del sistema se audita contra ellos. Si alguna funcionalidad los viola, el sistema debe corregirse — y si tú encuentras una violación, tienes el derecho y el deber de denunciarla (Protocolo de Disenso, T15).",
    },
    {
        icon: BookOpen,
        title: "Licencia y código abierto",
        body: "El código fuente es abierto y puede ser 'forkeado' (copiado y modificado) por cualquiera si el liderazgo se corrompe. El contenido se distribuye bajo Creative Commons BY-SA 4.0 y el software bajo licencia MIT. No existe una 'Maxocracia central': quien cumpla los axiomas, la construye.",
    },
];

export default function TermsPage() {
    return (
        <div className="min-h-screen pt-24 pb-16 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto space-y-10">
            <div className="text-center space-y-3">
                <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold uppercase tracking-wider">
                    <Scale className="w-3.5 h-3.5" />
                    Coherencia Vital
                </div>
                <h1 className="text-4xl font-black text-white tracking-tight">Términos de Participación</h1>
                <p className="text-slate-400 max-w-2xl mx-auto">
                    &quot;No buscamos la perfección, buscamos la verdad de la experiencia.
                    Somos científicos de nuestra propia existencia.&quot; — Principio rector de la Cohorte Cero
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {sections.map((s) => (
                    <div key={s.title} className="p-6 bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="p-2.5 rounded-xl border border-emerald-500/20 bg-emerald-500/10 text-emerald-400">
                                <s.icon className="w-5 h-5" />
                            </div>
                            <h2 className="font-bold text-white">{s.title}</h2>
                        </div>
                        <p className="text-sm text-slate-400 leading-relaxed">{s.body}</p>
                    </div>
                ))}
            </div>

            <div className="p-6 bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl">
                <h2 className="font-bold text-white mb-4">Lo que prometemos</h2>
                <ul className="space-y-3 text-sm text-slate-400">
                    {[
                        "Sin explotación: ninguna herramienta opera por debajo del Suelo de Dignidad Vital (γ ≥ 1, Invariante 1 de MaxoContracts).",
                        "Sin costo oculto: todo flujo financiero es público en el reporte de transparencia (T13).",
                        "Sin letra pequeña: los contratos se explican en lenguaje civil (≤ 20 palabras por frase).",
                        "Con retractación ética: si emergen hechos vitales nuevos, los acuerdos pueden pausarse y renegociarse.",
                    ].map((item) => (
                        <li key={item} className="flex items-start gap-3">
                            <span className="text-emerald-400 font-bold mt-0.5">✓</span>
                            <span>{item}</span>
                        </li>
                    ))}
                </ul>
            </div>

            <p className="text-xs text-slate-600 text-center">
                Última actualización: agosto de 2026 · Contacto: maxlopeztutor@gmail.com
            </p>
        </div>
    );
}
