'use client';

import React, { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiFetch } from '../../lib/api';
import {
  Bot, Send, RefreshCw, ShieldCheck, ShieldAlert, AlertTriangle,
  FilePlus2, Sparkles, ArrowLeft, ClipboardList, User, Loader2, XCircle
} from 'lucide-react';
import {
  DraftResult, materializeContract, SUGGESTED_INSTRUCTIONS,
} from '../../components/oracle';

interface ChatMessage {
  role: 'user' | 'oracle';
  content: string;
}

interface DisplayTerm {
  term_id: string;
  civil_text: string;
  vhv: { t: number; v: number; h: number };
  assigned_participant?: string;
}

export default function NegotiationPageClient() {
  const router = useRouter();

  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [draft, setDraft] = useState<DraftResult | null>(null);
  const [displayTerms, setDisplayTerms] = useState<DisplayTerm[]>([]);
  const [contractName, setContractName] = useState('');
  const [loading, setLoading] = useState(false);
  const [materializing, setMaterializing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [unavailable, setUnavailable] = useState(false);
  const [started, setStarted] = useState(false);

  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, displayTerms, loading]);

  const pushMessage = (role: 'user' | 'oracle', content: string) => {
    setMessages((prev) => [...prev, { role, content }]);
  };

  const handleUnavailable = (body: { error?: string; hint?: string } | null) => {
    setUnavailable(true);
    setError(body?.hint || body?.error || 'El oráculo en vivo no está disponible.');
  };

  const showDraft = (next: DraftResult) => {
    setDraft(next);
    setContractName(next.suggested_contract_id);
    const v = next.version;
    const parties = next.proposed_parties.length;
    const terms = next.draft_terms.length;
    const state = next.axiom_check.valid
      ? 'cumple T > 0, partes ≥ 2 y T17'
      : `tiene ${next.axiom_check.violations.length} violación(es) axiomática(s)`;
    pushMessage(
      'oracle',
      `Versión ${v} del borrador lista: ${terms} términos, ${parties} partes, ${state}. Puedes responderme con ajustes y yo renegocio.`
    );
    setDisplayTerms(next.draft_terms);
  };

  const send = async (e?: React.FormEvent) => {
    e?.preventDefault();
    const text = input.trim();
    if (!text || loading) return;
    setInput('');
    setError(null);
    setUnavailable(false);
    setStarted(true);
    setLoading(true);
    try {
      const isFeedback = Boolean(draft);
      const res = await apiFetch(
        isFeedback ? '/contracts/negotiate/feedback' : '/contracts/negotiate',
        {
          method: 'POST',
          body: JSON.stringify(
            isFeedback
              ? { session_id: draft!.session_id, feedback: text }
              : { instruction: text, participants: [] }
          ),
        }
      );
      const body = await res.json();
      if (res.status === 503) {
        handleUnavailable(body);
        return;
      }
      if (!res.ok) {
        setError(body.error || 'El oráculo falló al responder.');
        return;
      }
      pushMessage('user', text);
      showDraft(body);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error de conexión con el oráculo.');
    } finally {
      setLoading(false);
    }
  };

  const materialize = async () => {
    if (!draft || materializing) return;
    const name = contractName.trim();
    if (!name) {
      setError('Escribe un nombre para el contrato.');
      return;
    }
    setMaterializing(true);
    setError(null);
    try {
      const res = await apiFetch('/contracts/', {
        method: 'POST',
        body: JSON.stringify(materializeContract(draft, name, '')),
      });
      const body = await res.json();
      if (!res.ok) {
        setError(body.error || 'No se pudo materializar el contrato.');
        return;
      }
      pushMessage('oracle', `Contrato "${name}" materializado. Te llevo a la sala de firma.`);
      setDraft(null);
      setDisplayTerms([]);
      router.push(`/contracts/${name}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al materializar el contrato.');
    } finally {
      setMaterializing(false);
    }
  };

  const resetSession = () => {
    setDraft(null);
    setDisplayTerms([]);
    setMessages([]);
    setInput('');
    setStarted(false);
    setError(null);
  };

  return (
    <div className="h-screen w-screen flex flex-col bg-slate-950 overflow-hidden text-slate-100 font-sans">
      {/* Header */}
      <header className="h-16 border-b border-slate-800 bg-slate-900/60 backdrop-blur-md flex items-center px-6 justify-between z-10 shrink-0">
        <div className="flex items-center gap-4">
          <button
            onClick={() => router.push('/contracts')}
            className="flex items-center gap-2 text-xs font-bold text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Volver a Contratos
          </button>
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-violet-600 rounded-xl flex items-center justify-center shadow-lg shadow-violet-600/30">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-black text-white text-base tracking-tight flex items-center gap-2">
                Oráculo Sintético en Vivo
                {draft && (
                  <span className="text-[9px] bg-violet-500/20 text-violet-300 border border-violet-500/30 px-2 py-0.5 rounded-full font-normal">
                    v{draft.version}
                  </span>
                )}
              </h1>
              <p className="text-[10px] text-slate-400">DeepSeek conversa con las partes hasta el contrato idóneo</p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span className={`flex items-center gap-1.5 text-[9px] font-black uppercase tracking-widest px-3 py-1.5 rounded-full border ${
            unavailable
              ? 'text-amber-400 bg-amber-500/10 border-amber-500/20'
              : 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
          }`}>
            <span className={`w-1.5 h-1.5 rounded-full ${unavailable ? 'bg-amber-400' : 'bg-emerald-400 animate-pulse'}`} />
            {unavailable ? 'No disponible' : draft ? `Sesión activa · v${draft.version}` : 'Oráculo en vivo'}
          </span>
          {started && (
            <button
              onClick={resetSession}
              className="text-[10px] font-bold text-slate-400 hover:text-white border border-slate-800 px-3 py-1.5 rounded-lg transition-colors"
            >
              Nueva negociación
            </button>
          )}
        </div>
      </header>

      {/* Main */}
      <div className="flex-1 flex overflow-hidden">
        {/* Chat — el protagonista */}
        <main className="flex-1 flex flex-col min-w-0">
          <div className="flex-1 overflow-y-auto px-6 py-6 space-y-5">
            {/* Bienvenida */}
            {!started && (
              <div className="max-w-3xl mx-auto w-full space-y-6 pt-10">
                <div className="text-center space-y-3">
                  <div className="w-20 h-20 mx-auto bg-gradient-to-br from-violet-600 to-fuchsia-600 rounded-3xl flex items-center justify-center shadow-2xl shadow-violet-600/40">
                    <Bot className="w-10 h-10 text-white" />
                  </div>
                  <h2 className="text-3xl font-black text-white tracking-tight">
                    Soy el Oráculo de la Maxocracia
                  </h2>
                  <p className="text-sm text-slate-400 max-w-xl mx-auto leading-relaxed">
                    Descríbeme el intercambio que imaginas y yo lo convierto en un
                    MaxoContract coherente: términos en lenguaje civil, costos VHV,
                    partes obligadas y chequeo de los axiomas (T13, INV2/INV2-S, T17, γ ≥ 1).
                  </p>
                </div>
                <div className="space-y-2">
                  <span className="text-[10px] font-black uppercase tracking-widest text-slate-500 block text-center">
                    Empieza con un ejemplo
                  </span>
                  <div className="grid gap-2 max-w-2xl mx-auto">
                    {SUGGESTED_INSTRUCTIONS.map((s) => (
                      <button
                        key={s}
                        onClick={() => {
                          setInput(s);
                          setStarted(true);
                        }}
                        className="text-left p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-violet-500/40 hover:bg-slate-900 text-xs text-slate-300 transition-all flex items-center gap-2.5 group"
                      >
                        <Sparkles className="w-4 h-4 text-violet-400 shrink-0 group-hover:scale-110 transition-transform" />
                        {s}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {unavailable && (
              <div className="max-w-3xl mx-auto w-full p-4 rounded-2xl bg-amber-950/20 border border-amber-900/30 text-xs text-amber-200/80 leading-relaxed">
                {error} Configura <code className="font-mono bg-slate-900 px-1.5 py-0.5 rounded">DEEPSEEK_API_KEY</code> en el .env y recarga.
              </div>
            )}

            {/* Burbujas */}
            {messages.map((m, i) => (
              <div key={i} className={`max-w-3xl mx-auto w-full flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] flex gap-3 ${m.role === 'user' ? 'flex-row-reverse' : ''}`}>
                  <div className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 mt-1 ${
                    m.role === 'user' ? 'bg-slate-800' : 'bg-violet-600'
                  }`}>
                    {m.role === 'user' ? (
                      <User className="w-4 h-4 text-slate-300" />
                    ) : (
                      <Bot className="w-4 h-4 text-white" />
                    )}
                  </div>
                  <div className={`p-4 rounded-2xl border text-xs leading-relaxed ${
                    m.role === 'user'
                      ? 'bg-emerald-950/40 border-emerald-900/40 text-slate-200 rounded-tr-md'
                      : 'bg-slate-900/70 border-slate-800 text-slate-300 rounded-tl-md'
                  }`}>
                    {m.content}
                  </div>
                </div>
              </div>
            ))}

            {/* Tarjeta del borrador dentro del chat */}
            {draft && (
              <div className="max-w-3xl mx-auto w-full space-y-4">
                <div className="p-5 rounded-3xl bg-slate-900/80 border border-slate-800 shadow-xl space-y-4">
                  {/* Chequeo axiomático */}
                  <div className={`p-4 rounded-2xl border ${
                    draft.axiom_check.valid
                      ? 'bg-emerald-950/20 border-emerald-900/30'
                      : 'bg-rose-950/20 border-rose-900/30'
                  }`}>
                    <div className="flex items-center gap-2">
                      {draft.axiom_check.valid ? (
                        <ShieldCheck className="w-5 h-5 text-emerald-500" />
                      ) : (
                        <ShieldAlert className="w-5 h-5 text-rose-500" />
                      )}
                      <span className={`text-xs font-black uppercase tracking-wider ${
                        draft.axiom_check.valid ? 'text-emerald-400' : 'text-rose-400'
                      }`}>
                        {draft.axiom_check.valid ? 'Axiomas cumplidos' : 'Violaciones axiomáticas'}
                      </span>
                    </div>
                    {draft.axiom_check.violations.map((v, i) => (
                      <p key={i} className="mt-2 text-[11px] text-rose-300 flex items-start gap-1.5">
                        <XCircle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                        <span><strong>{v.axiom}:</strong> {v.message}</span>
                      </p>
                    ))}
                    {draft.axiom_check.warnings.map((w, i) => (
                      <p key={i} className="mt-2 text-[11px] text-amber-300 flex items-start gap-1.5">
                        <AlertTriangle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                        <span><strong>{w.axiom}:</strong> {w.message}</span>
                      </p>
                    ))}
                  </div>

                  {/* Razonamiento */}
                  <div className="p-4 bg-slate-950/70 border border-slate-800 rounded-2xl">
                    <span className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-1.5">Razonamiento del oráculo</span>
                    <p className="text-xs text-slate-300 leading-relaxed italic">
                      &quot;{draft.reasoning || 'Sin explicación.'}&quot;
                    </p>
                  </div>

                  {/* Términos */}
                  <div className="space-y-2">
                    <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider flex items-center gap-1.5">
                      <ClipboardList className="w-3.5 h-3.5" /> Borrador v{draft.version} — {draft.draft_terms.length} términos · {draft.proposed_parties.length} partes
                    </span>
                    {draft.draft_terms.map((t) => (
                      <div key={t.term_id} className="p-3.5 bg-slate-950/50 border border-slate-800 rounded-xl text-xs space-y-1.5">
                        <div className="flex items-center justify-between gap-2">
                          <span className="font-bold text-white font-mono text-[10px]">{t.term_id}</span>
                          <span className="text-[9px] font-mono text-violet-400">
                            {t.assigned_participant || 'sin parte'}
                            {' '}· VHV T={t.vhv.t} V={t.vhv.v} H={t.vhv.h}
                          </span>
                        </div>
                        <p className="text-slate-300 leading-relaxed">{t.civil_text}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Materializar */}
                <div className="p-5 rounded-3xl bg-slate-900/80 border border-emerald-900/50 shadow-xl space-y-3">
                  <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider flex items-center gap-1.5">
                    <FilePlus2 className="w-3.5 h-3.5 text-emerald-400" /> ¿De acuerdo? Materializa el contrato
                  </span>
                  <div className="flex gap-2">
                    <input
                      value={contractName}
                      onChange={(e) => setContractName(e.target.value)}
                      placeholder="Nombre del contrato"
                      className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-xs text-white focus:outline-none focus:border-emerald-500/50 placeholder:text-slate-700"
                    />
                    <button
                      onClick={materialize}
                      disabled={materializing}
                      className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-900 text-white font-black rounded-xl text-xs uppercase tracking-wider transition-all flex items-center gap-2 shrink-0"
                    >
                      {materializing ? (
                        <>
                          <Loader2 className="w-4 h-4 animate-spin" />
                          Creando...
                        </>
                      ) : (
                        <>
                          <FilePlus2 className="w-4 h-4" />
                          Materializar
                        </>
                      )}
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Indicador de escritura */}
            {loading && (
              <div className="max-w-3xl mx-auto w-full flex justify-start">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-xl bg-violet-600 flex items-center justify-center">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                  <div className="px-4 py-3 rounded-2xl bg-slate-900/70 border border-slate-800 flex gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-violet-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                    <span className="w-2 h-2 rounded-full bg-violet-400 animate-bounce" style={{ animationDelay: '150ms' }} />
                    <span className="w-2 h-2 rounded-full bg-violet-400 animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            )}

            {error && !unavailable && (
              <div className="max-w-3xl mx-auto w-full text-[11px] text-rose-400 flex items-center gap-1.5">
                <AlertTriangle className="w-3.5 h-3.5" /> {error}
              </div>
            )}

            <div ref={chatEndRef} />
          </div>

          {/* Input */}
          <form onSubmit={send} className="border-t border-slate-800 bg-slate-900/60 backdrop-blur-md px-6 py-4 shrink-0">
            <div className="max-w-3xl mx-auto flex gap-3">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    send();
                  }
                }}
                placeholder={draft
                  ? 'Responde al borrador: ajustes, objeciones, contraprestaciones... (Enter para enviar)'
                  : 'Describe tu intercambio en lenguaje natural... (Enter para enviar)'}
                rows={2}
                className="flex-1 bg-slate-950 border border-slate-800 rounded-2xl px-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-violet-500/50 placeholder:text-slate-700 resize-none"
              />
              <button
                type="submit"
                disabled={loading || !input.trim()}
                className="px-5 py-3 bg-violet-600 hover:bg-violet-500 disabled:bg-slate-900 text-white font-black rounded-2xl transition-all flex items-center gap-2 shrink-0"
              >
                {loading ? (
                  <RefreshCw className="w-5 h-5 animate-spin" />
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    <span className="hidden md:inline">{draft ? 'Iterar' : 'Consultar'}</span>
                  </>
                )}
              </button>
            </div>
            <p className="max-w-3xl mx-auto text-[9px] text-slate-600 mt-2">
              El oráculo aplica T13 (transparencia radical), INV2/INV2-S (suelos de dignidad), T17 (reciprocidad justa), γ ≥ 1 y la Capa de Ternura. Nunca oculta costos ni riesgos.
            </p>
          </form>
        </main>

        {/* Rail derecho: estado de la negociación */}
        <aside className="w-80 border-l border-slate-800 bg-slate-900/40 p-5 flex flex-col gap-5 overflow-y-auto hidden lg:flex shrink-0">
          <div>
            <h3 className="text-xs font-black text-white uppercase tracking-wider flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-violet-400" />
              Estado de la negociación
            </h3>
            <p className="text-[10px] text-slate-500 mt-1 leading-relaxed">
              Cada respuesta del oráculo produce una nueva versión del borrador. La sesión vive 30 minutos.
            </p>
          </div>

          {!draft ? (
            <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 text-center space-y-2">
              <Bot className="w-8 h-8 text-slate-700 mx-auto" />
              <p className="text-[11px] text-slate-500 leading-relaxed">
                Aún no hay borrador. Escribe tu primera instrucción para empezar.
              </p>
            </div>
          ) : (
            <>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-950/60 border border-slate-800 p-3 rounded-xl text-center">
                  <span className="text-[9px] text-slate-500 uppercase font-black block">Versión</span>
                  <span className="text-2xl font-black text-violet-400">{draft.version}</span>
                </div>
                <div className="bg-slate-950/60 border border-slate-800 p-3 rounded-xl text-center">
                  <span className="text-[9px] text-slate-500 uppercase font-black block">Términos</span>
                  <span className="text-2xl font-black text-white">{draft.draft_terms.length}</span>
                </div>
              </div>

              <div className="space-y-1.5">
                <span className="text-[9px] font-black uppercase tracking-widest text-slate-500">Partes propuestas</span>
                {draft.proposed_parties.map((p) => (
                  <div key={p} className="flex items-center gap-2 bg-slate-950/60 border border-slate-800 px-3 py-2 rounded-xl text-[11px] font-mono text-slate-300">
                    <User className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                    {p}
                  </div>
                ))}
              </div>

              <div className="space-y-1.5">
                <span className="text-[9px] font-black uppercase tracking-widest text-slate-500">Balance T17 por parte</span>
                {Object.entries(draft.axiom_check.reciprocity_balance).map(([pid, total]) => (
                  <div key={pid} className="flex items-center justify-between bg-slate-950/60 border border-slate-800 px-3 py-2 rounded-xl text-[11px]">
                    <span className="font-mono text-slate-400">{pid}</span>
                    <span className="font-bold text-emerald-400">{total.toFixed(1)}</span>
                  </div>
                ))}
              </div>

              <div className="p-3 rounded-2xl bg-violet-950/20 border border-violet-900/30">
                <span className="text-[9px] font-black uppercase tracking-widest text-violet-300 block mb-1">Consejo del oráculo</span>
                <p className="text-[10px] text-slate-400 leading-relaxed">
                  Si algo no te convence, dilo en tus palabras: «Ana no puede dar más de 5 horas», «falta una cláusula de transparencia», «quiero que Luis avale».
                </p>
              </div>
            </>
          )}
        </aside>
      </div>
    </div>
  );
}
