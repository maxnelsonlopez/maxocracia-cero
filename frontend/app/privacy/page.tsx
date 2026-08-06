import { Metadata } from "next";
import { ShieldCheck, Eye, HeartHandshake, KeyRound, Trash2 } from "lucide-react";

export const metadata: Metadata = {
    title: "Privacidad y Opacidad Sagrada - Maxocracia",
    description:
        "Cómo Maxocracia protege los datos personales: Derecho a la Opacidad, datos mínimos y la Capa de Ternura (Axioma 6).",
};

const pillars = [
    {
        icon: Eye,
        title: "Derecho a la Opacidad",
        body: "Cada ser tiene derecho a una fracción de su tiempo que es 'sagrada opaca': invisible al sistema y a los juicios de otros (Capa de Ternura, Sesión 3 de la Victoria Sintética). Sugerido entre el 10% y el 20% del TVI, este espacio nunca se audita.",
    },
    {
        icon: KeyRound,
        title: "Datos mínimos",
        body: "Solo se recopila la información estrictamente necesaria para operar: una cuenta, tus registros voluntarios de VHV y las transacciones de la cohorte. Nada más. Si un dato no sirve a la coherencia vital, no se pide.",
    },
    {
        icon: HeartHandshake,
        title: "Lo inefable no se indexa",
        body: "El arte, la belleza, el misterio, el cuidado espontáneo y la intimidad no se miden en el VHV (Protección de lo Inefable). Los registros de seguimiento son cualitativos y nunca se usan como argumento en juicios de valor.",
    },
    {
        icon: Trash2,
        title: "Borrado a solicitud",
        body: "La participación es voluntaria. Puedes solicitar la eliminación de tus datos en cualquier momento y el sistema los retira de la base operativa, conservando únicamente lo que la ley exija o lo que el anonimato estadístico requiera.",
    },
];

export default function PrivacyPage() {
    return (
        <div className="min-h-screen pt-24 pb-16 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto space-y-10">
            <div className="text-center space-y-3">
                <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold uppercase tracking-wider">
                    <ShieldCheck className="w-3.5 h-3.5" />
                    Capa de Ternura · Axioma 6
                </div>
                <h1 className="text-4xl font-black text-white tracking-tight">Privacidad y Opacidad Sagrada</h1>
                <p className="text-slate-400 max-w-2xl mx-auto">
                    La transparencia radical se aplica a los sistemas, no a las personas.
                    Un sistema que vigila todo deja de ser maxocrático y se vuelve totalitario.
                </p>
                <blockquote className="text-emerald-400/90 text-sm italic max-w-xl mx-auto pt-2">
                    &quot;Un sistema perfecto que no perdona, es un sistema muerto.&quot;
                </blockquote>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {pillars.map((p) => (
                    <div key={p.title} className="p-6 bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="p-2.5 rounded-xl border border-emerald-500/20 bg-emerald-500/10 text-emerald-400">
                                <p.icon className="w-5 h-5" />
                            </div>
                            <h2 className="font-bold text-white">{p.title}</h2>
                        </div>
                        <p className="text-sm text-slate-400 leading-relaxed">{p.body}</p>
                    </div>
                ))}
            </div>

            <div className="p-6 bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl">
                <h2 className="font-bold text-white mb-4">Lo que NO hacemos</h2>
                <ul className="space-y-3 text-sm text-slate-400">
                    {[
                        "No auditamos la intimidad ni el tiempo de ocio no estructurado (EVV-1.2 §1.3).",
                        "No vendemos datos. Este proyecto no tiene publicidad ni intermediarios de datos.",
                        "No emitimos juicios morales automáticos: los datos son datos; el juicio pertenece a las asambleas humanas.",
                        "No usamos tu tiempo de vida como producto: los registros te pertenecen y sirven a tu soberanía temporal (CCP).",                    ].map((item) => (
                        <li key={item} className="flex items-start gap-3">
                            <span className="text-rose-400 font-bold mt-0.5">✕</span>
                            <span>{item}</span>
                        </li>
                    ))}
                </ul>
            </div>

            <p className="text-xs text-slate-600 text-center">
                Última actualización: agosto de 2026 · Preguntas sobre datos: maxlopeztutor@gmail.com
            </p>
        </div>
    );
}
