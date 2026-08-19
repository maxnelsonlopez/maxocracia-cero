"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Compass,
  GitBranch,
  HeartHandshake,
  Landmark,
  Layers3,
  LockKeyhole,
  ShieldCheck,
  Sparkles,
  Terminal,
  Timer,
  Users,
  Zap,
} from "lucide-react";
import { useAuth } from "./context/AuthContext";

const principles = [
  {
    icon: Timer,
    eyebrow: "TVI",
    title: "Tiempo vital",
    text: "El tiempo de atención, cuidado y aprendizaje no se recupera. La primera pregunta es qué vida estamos sosteniendo.",
    color: "amber",
  },
  {
    icon: ShieldCheck,
    eyebrow: "VHV [T,V,R]",
    title: "Valor verificable",
    text: "Una contribución necesita trazabilidad, verificación y reciprocidad. El valor no desaparece detrás de una cifra.",
    color: "emerald",
  },
  {
    icon: HeartHandshake,
    eyebrow: "SDV",
    title: "Reciprocidad",
    text: "Una red coherente no busca extraer. Busca que las personas puedan recibir, aportar y mejorar su línea de base.",
    color: "violet",
  },
];

const layers = [
  {
    number: "01",
    title: "Axiomas",
    text: "Principios legibles que orientan qué llamamos verdad, valor y coherencia.",
    icon: Landmark,
  },
  {
    number: "02",
    title: "Economía operativa",
    text: "Herramientas para observar tiempo, aportes, necesidades y distribución sin depender de una blockchain.",
    icon: Layers3,
  },
  {
    number: "03",
    title: "Microcomunidades",
    text: "Experimentos domésticos y colectivos donde la dignidad vital puede convertirse en práctica cotidiana.",
    icon: Users,
  },
  {
    number: "04",
    title: "Contratos legibles",
    text: "Acuerdos que pueden leer las personas y verificar las máquinas, con salida y reciprocidad explícitas.",
    icon: GitBranch,
  },
];

const entrances = [
  {
    icon: BookOpen,
    title: "Entender el sistema",
    text: "Lee los conceptos, axiomas y promesas sin necesidad de registrarte.",
    href: "/participar",
    label: "Explorar la guía",
    accent: "emerald",
  },
  {
    icon: Terminal,
    title: "Probarlo localmente",
    text: "El código, los documentos y el camino de ejecución están abiertos.",
    href: "https://github.com/maxnelsonlopez/maxocracia-cero",
    label: "Abrir GitHub",
    accent: "amber",
    external: true,
  },
  {
    icon: HeartHandshake,
    title: "Unirse a la red",
    text: "Comparte qué puedes ofrecer y qué necesitas, de forma voluntaria.",
    href: "/forms/cero",
    label: "Ir a Red de Apoyo",
    accent: "violet",
  },
];

export default function HomePage() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.push("/forms/follow-up");
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#020617] text-slate-100 flex items-center justify-center">
        <div className="w-12 h-12 border-4 border-emerald-500/30 border-t-emerald-400 rounded-full animate-spin" />
      </div>
    );
  }

  if (isAuthenticated) {
    return null;
  }

  return (
    <main className="relative overflow-hidden bg-[#020617] text-slate-100 selection:bg-emerald-400/30 selection:text-emerald-100">
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 opacity-40"
        style={{
          backgroundImage:
            "linear-gradient(rgba(16,185,129,0.045) 1px, transparent 1px), linear-gradient(90deg, rgba(16,185,129,0.045) 1px, transparent 1px), radial-gradient(70% 55% at 50% 0%, rgba(16,185,129,0.12), transparent 72%), radial-gradient(45% 40% at 85% 20%, rgba(245,158,11,0.08), transparent 68%)",
          backgroundSize: "48px 48px, 48px 48px, auto, auto",
        }}
      />

      <section className="relative mx-auto max-w-7xl px-4 pb-20 pt-20 sm:px-6 md:pb-28 md:pt-28 lg:px-8">
        <div className="grid items-center gap-14 lg:grid-cols-[1.05fr_0.95fr] lg:gap-20">
          <div>
            <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/5 px-3 py-1.5 font-mono text-[10px] uppercase tracking-[0.22em] text-emerald-300">
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />
              Archivo vivo · Fase 2 · Bogotá / UTC-5
            </div>

            <p className="mb-5 font-mono text-xs uppercase tracking-[0.32em] text-amber-300/80">
              Sistema operativo civilizatorio
            </p>
            <h1 className="max-w-4xl text-5xl font-black leading-[0.96] tracking-[-0.04em] text-white sm:text-6xl md:text-7xl">
              La vida no es una cifra.
              <span className="mt-2 block bg-gradient-to-r from-emerald-300 via-cyan-300 to-amber-200 bg-clip-text text-transparent">
                Es el recurso que no vuelve.
              </span>
            </h1>
            <p className="mt-8 max-w-2xl text-lg leading-8 text-slate-300 sm:text-xl">
              <strong className="font-semibold text-white">Maxocracia</strong> es una forma abierta de organizar el valor alrededor del tiempo de vida, el cuidado y la reciprocidad, en lugar de hacerlo alrededor del dinero y la extracción.
            </p>
            <p className="mt-5 max-w-xl text-sm leading-7 text-slate-400">
              Un sistema ético, económico y político en construcción. Código abierto, voluntario y auditable. No es una criptomoneda, no es un partido y no es un producto terminado.
            </p>

            <div className="mt-9 flex flex-col gap-3 sm:flex-row sm:flex-wrap">
              <Link
                href="/participar"
                className="group inline-flex items-center justify-center gap-2 rounded-xl bg-emerald-400 px-5 py-3.5 text-sm font-bold text-slate-950 shadow-lg shadow-emerald-500/20 transition hover:bg-emerald-300"
              >
                Entender el sistema
                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Link>
              <Link
                href="/forms/cero"
                className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-700 bg-slate-900/50 px-5 py-3.5 text-sm font-bold text-slate-100 transition hover:border-violet-400/50 hover:bg-violet-400/10"
              >
                Unirse a la Red de Apoyo
                <HeartHandshake className="h-4 w-4 text-violet-300" />
              </Link>
            </div>
            <p className="mt-4 flex items-center gap-2 text-xs text-slate-500">
              <LockKeyhole className="h-3.5 w-3.5 text-emerald-400" />
              Puedes leer y explorar sin entregar ningún dato personal.
            </p>
          </div>

          <div className="relative mx-auto w-full max-w-xl">
            <div className="absolute -inset-10 rounded-full bg-emerald-500/10 blur-3xl" />
            <div className="relative overflow-hidden rounded-[2rem] border border-slate-700/70 bg-slate-950/80 p-5 shadow-2xl shadow-emerald-950/50 backdrop-blur-xl sm:p-7">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-4 font-mono text-[10px] uppercase tracking-[0.2em] text-slate-500">
                <span>VHV / red de reciprocidad</span>
                <span className="text-emerald-400">● operativo</span>
              </div>
              <div className="relative mt-6 aspect-square overflow-hidden rounded-2xl border border-emerald-400/10 bg-[#07111b]">
                <div className="absolute inset-0 opacity-30" style={{ backgroundImage: "radial-gradient(circle at center, rgba(16,185,129,0.25) 1px, transparent 1px)", backgroundSize: "24px 24px" }} />
                <svg viewBox="0 0 400 400" className="absolute inset-0 h-full w-full" aria-hidden="true">
                  <defs>
                    <linearGradient id="vital-line" x1="0" x2="1" y1="0" y2="1">
                      <stop offset="0" stopColor="#fbbf24" stopOpacity="0.2" />
                      <stop offset="0.5" stopColor="#34d399" stopOpacity="0.95" />
                      <stop offset="1" stopColor="#67e8f9" stopOpacity="0.25" />
                    </linearGradient>
                    <filter id="vital-glow">
                      <feGaussianBlur stdDeviation="4" result="blur" />
                      <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
                    </filter>
                  </defs>
                  <g stroke="url(#vital-line)" strokeWidth="1.2" fill="none" opacity="0.55">
                    <path d="M54 98 L142 165 L208 92 L305 145 L348 270 L232 316 L142 266 L54 300 L142 165 L232 316" />
                    <path d="M208 92 L232 316 M54 98 L305 145 M142 266 L348 270" opacity="0.45" />
                  </g>
                  <g fill="#07111b" stroke="#34d399" strokeWidth="2" filter="url(#vital-glow)">
                    <circle cx="54" cy="98" r="7" /><circle cx="142" cy="165" r="9" /><circle cx="208" cy="92" r="6" />
                    <circle cx="305" cy="145" r="8" /><circle cx="348" cy="270" r="6" /><circle cx="232" cy="316" r="10" />
                    <circle cx="142" cy="266" r="6" /><circle cx="54" cy="300" r="8" />
                  </g>
                  <circle cx="232" cy="316" r="24" fill="none" stroke="#fbbf24" strokeWidth="1" strokeDasharray="3 6" opacity="0.8" />
                </svg>
                <div className="absolute left-6 top-6 font-mono text-[10px] uppercase tracking-[0.2em] text-amber-200/70">Tiempo</div>
                <div className="absolute right-6 top-1/2 font-mono text-[10px] uppercase tracking-[0.2em] text-cyan-200/70">Valor</div>
                <div className="absolute bottom-6 left-1/2 -translate-x-1/2 font-mono text-[10px] uppercase tracking-[0.2em] text-emerald-200/70">Reciprocidad</div>
                <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-center">
                  <div className="font-mono text-4xl font-bold tracking-[-0.08em] text-white">TVI</div>
                  <div className="mt-1 text-[10px] uppercase tracking-[0.22em] text-slate-500">tiempo vital irrecuperable</div>
                </div>
              </div>
              <div className="mt-5 grid grid-cols-3 gap-2 text-center font-mono text-[10px] uppercase tracking-[0.16em] text-slate-500">
                <div className="rounded-lg border border-slate-800 bg-slate-900/70 px-2 py-3"><span className="block text-amber-300">T</span>Trazabilidad</div>
                <div className="rounded-lg border border-slate-800 bg-slate-900/70 px-2 py-3"><span className="block text-emerald-300">V</span>Verificación</div>
                <div className="rounded-lg border border-slate-800 bg-slate-900/70 px-2 py-3"><span className="block text-cyan-300">R</span>Reciprocidad</div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-20 grid gap-6 border-y border-slate-800/80 py-8 md:grid-cols-[0.7fr_1.3fr] md:items-center">
          <div className="flex items-center gap-3 font-mono text-xs uppercase tracking-[0.2em] text-amber-300/80">
            <Sparkles className="h-4 w-4" /> Axioma 4 · fundacional
          </div>
          <blockquote className="border-l border-amber-300/40 pl-5 text-lg leading-8 text-slate-300 sm:text-xl">
            «La verdad es el camino más corto de sucesos e información entre las personas, los hechos y la verdad misma.»
          </blockquote>
        </div>
      </section>

      <section className="relative border-t border-slate-800/60 bg-slate-950/40 py-20 md:py-28">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl">
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-emerald-300">01 / La pregunta de fondo</p>
            <h2 className="mt-4 text-3xl font-bold tracking-tight text-white sm:text-5xl">¿Qué cambia cuando dejamos de contar solamente el dinero?</h2>
            <p className="mt-6 text-lg leading-8 text-slate-400">El cuidado, el aprendizaje, la atención y la reparación sostienen cualquier comunidad, pero suelen quedar fuera de la contabilidad. Maxocracia-Cero es un laboratorio para hacer visibles esas relaciones sin convertir la intimidad en una mercancía.</p>
          </div>

          <div className="mt-12 grid gap-4 md:grid-cols-3">
            {principles.map((principle) => {
              const Icon = principle.icon;
              const colorClasses = {
                amber: "border-amber-400/20 bg-amber-400/5 text-amber-300",
                emerald: "border-emerald-400/20 bg-emerald-400/5 text-emerald-300",
                violet: "border-violet-400/20 bg-violet-400/5 text-violet-300",
              } as const;
              return (
                <article key={principle.eyebrow} className="rounded-2xl border border-slate-800 bg-slate-900/45 p-6 transition hover:-translate-y-1 hover:border-slate-700">
                  <div className={`mb-7 flex h-11 w-11 items-center justify-center rounded-xl border ${colorClasses[principle.color as keyof typeof colorClasses]}`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <p className="font-mono text-[10px] uppercase tracking-[0.22em] text-slate-500">{principle.eyebrow}</p>
                  <h3 className="mt-2 text-xl font-semibold text-white">{principle.title}</h3>
                  <p className="mt-3 text-sm leading-7 text-slate-400">{principle.text}</p>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section className="relative py-20 md:py-28">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid gap-12 lg:grid-cols-[0.8fr_1.2fr] lg:items-start">
            <div>
              <p className="font-mono text-xs uppercase tracking-[0.28em] text-amber-300">02 / Sin malentendidos</p>
              <h2 className="mt-4 text-3xl font-bold text-white sm:text-4xl">Una propuesta experimental, no una promesa financiera.</h2>
              <p className="mt-5 text-base leading-8 text-slate-400">El sistema está en construcción. Sus conceptos pueden ser ambiciosos y su lenguaje puede ser poético, pero cada afirmación operativa debe poder leerse, probarse y discutirse.</p>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="rounded-2xl border border-emerald-400/20 bg-emerald-400/5 p-6">
                <div className="flex items-center gap-2 text-sm font-semibold text-emerald-300"><CheckCircle2 className="h-4 w-4" /> Sí es</div>
                <ul className="mt-5 space-y-3 text-sm leading-6 text-slate-300">
                  <li>• Un laboratorio de economía vital y reciprocidad.</li>
                  <li>• Código, documentos y experimentos abiertos.</li>
                  <li>• Una invitación a hogares, cooperativas y comunidades.</li>
                  <li>• Un sistema voluntario que debe poder auditarse.</li>
                </ul>
              </div>
              <div className="rounded-2xl border border-rose-400/20 bg-rose-400/5 p-6">
                <div className="flex items-center gap-2 text-sm font-semibold text-rose-300"><Zap className="h-4 w-4" /> No es</div>
                <ul className="mt-5 space-y-3 text-sm leading-6 text-slate-300">
                  <li>• Una criptomoneda o una promesa de rentabilidad.</li>
                  <li>• Un partido, una religión o una autoridad central.</li>
                  <li>• Un sistema que deba medir la intimidad.</li>
                  <li>• Un producto terminado ni una verdad incuestionable.</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="relative border-y border-slate-800/70 bg-[#07111b] py-20 md:py-28">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl">
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-cyan-300">03 / Cómo se sostiene</p>
            <h2 className="mt-4 text-3xl font-bold text-white sm:text-4xl">Cuatro capas para pasar de la idea a la práctica.</h2>
          </div>
          <div className="mt-12 grid gap-4 md:grid-cols-2">
            {layers.map((layer) => {
              const Icon = layer.icon;
              return (
                <div key={layer.number} className="group flex gap-5 rounded-2xl border border-slate-800 bg-slate-950/50 p-6 transition hover:border-emerald-400/30">
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl border border-slate-700 bg-slate-900 font-mono text-xs text-emerald-300 group-hover:border-emerald-400/50">
                    <Icon className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="font-mono text-[10px] tracking-[0.2em] text-slate-600">CAPA {layer.number}</p>
                    <h3 className="mt-1 text-lg font-semibold text-white">{layer.title}</h3>
                    <p className="mt-2 text-sm leading-6 text-slate-400">{layer.text}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      <section className="relative py-20 md:py-28">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col justify-between gap-5 md:flex-row md:items-end">
            <div>
              <p className="font-mono text-xs uppercase tracking-[0.28em] text-violet-300">04 / Elige tu entrada</p>
              <h2 className="mt-4 text-3xl font-bold text-white sm:text-4xl">No tienes que creer. Puedes explorar.</h2>
            </div>
            <p className="max-w-md text-sm leading-6 text-slate-500">La plataforma está viva y en evolución. Cada ruta te muestra una parte distinta del sistema, sin pedirte confianza ciega.</p>
          </div>
          <div className="mt-10 grid gap-4 lg:grid-cols-3">
            {entrances.map((entrance) => {
              const Icon = entrance.icon;
              const accent = {
                emerald: "text-emerald-300 border-emerald-400/20 hover:border-emerald-400/50",
                amber: "text-amber-300 border-amber-400/20 hover:border-amber-400/50",
                violet: "text-violet-300 border-violet-400/20 hover:border-violet-400/50",
              } as const;
              const className = `group rounded-2xl border bg-slate-900/45 p-6 transition hover:-translate-y-1 ${accent[entrance.accent as keyof typeof accent]}`;
              const content = (
                <>
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-950/80"><Icon className="h-5 w-5" /></div>
                    <ArrowRight className="h-5 w-5 opacity-50 transition group-hover:translate-x-1 group-hover:opacity-100" />
                  </div>
                  <h3 className="mt-8 text-xl font-semibold text-white">{entrance.title}</h3>
                  <p className="mt-3 min-h-[3.5rem] text-sm leading-6 text-slate-400">{entrance.text}</p>
                  <span className="mt-6 inline-flex items-center gap-2 text-sm font-semibold">{entrance.label} <ArrowRight className="h-4 w-4" /></span>
                </>
              );
              return entrance.external ? (
                <a key={entrance.title} href={entrance.href} target="_blank" rel="noopener noreferrer" className={className}>{content}</a>
              ) : (
                <Link key={entrance.title} href={entrance.href} className={className}>{content}</Link>
              );
            })}
          </div>
        </div>
      </section>

      <section className="relative border-t border-slate-800/70 bg-gradient-to-b from-emerald-950/20 to-[#020617] py-20 text-center md:py-28">
        <div className="mx-auto max-w-3xl px-4 sm:px-6">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl border border-emerald-400/30 bg-emerald-400/10 text-emerald-300"><Compass className="h-7 w-7" /></div>
          <p className="mt-7 font-mono text-xs uppercase tracking-[0.28em] text-emerald-300">Archivo abierto · estado experimental</p>
          <h2 className="mt-4 text-3xl font-bold text-white sm:text-4xl">La coherencia también se construye conversando.</h2>
          <p className="mx-auto mt-5 max-w-2xl text-base leading-8 text-slate-400">Puedes leer el código, cuestionar los axiomas, ejecutar el sistema localmente o ayudar a que la Red de Apoyo encuentre su primera reciprocidad.</p>
          <Link href="/forms/cero" className="mt-8 inline-flex items-center gap-2 rounded-xl border border-emerald-400/40 bg-emerald-400/10 px-5 py-3.5 text-sm font-bold text-emerald-200 transition hover:bg-emerald-400/20">
            Dar el primer paso <ArrowRight className="h-4 w-4" />
          </Link>
          <p className="mx-auto mt-6 max-w-xl text-[11px] leading-5 text-slate-600">
            Portada cocreada por Max Nelson López y Manus · <a href="https://github.com/maxnelsonlopez/maxocracia-cero/blob/main/docs/architecture/atribuciones_sinteticas.md" target="_blank" rel="noopener noreferrer" className="text-slate-500 underline decoration-slate-700 underline-offset-2 transition hover:text-emerald-300">atribución sintética verificable</a>
          </p>
        </div>
      </section>
    </main>
  );
}
