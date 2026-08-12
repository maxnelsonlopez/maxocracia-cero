'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiFetch } from '../lib/api';
import {
  Bot, Send, RefreshCw, ShieldCheck, ShieldAlert, AlertTriangle,
  FilePlus2, Sparkles, CheckCircle2, XCircle, ClipboardList, Maximize2
} from 'lucide-react';
import {
  DraftResult, CritiqueResult, mapParty,
} from './oracle';

interface ChatMessage {
  role: 'user' | 'oracle';
  content: string;
}

interface OracleNegotiationPanelProps {
  contractId?: string;
  participants?: string[];
  onMaterialized?: (contractId: string) => void;
}

export default function OracleNegotiationPanel({
  contractId,
  participants,
  onMaterialized,
}: OracleNegotiationPanelProps) {
  const router = useRouter();

  const [instruction, setInstruction] = useState('');
  const [feedback, setFeedback] = useState('');
  const [contractName, setContractName] = useState('');
  const [draft, setDraft] = useState<DraftResult | null>(null);
  const [critique, setCritique] = useState<CritiqueResult | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [materializing, setMaterializing] = useState(false);
  const [critiquing, setCritiquing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [unavailable, setUnavailable] = useState(false);

  const handleUnavailable = (body: { error?: string; hint?: string } | null) => {
    setUnavailable(true);
    setError(body?.hint || body?.error || 'El oráculo en vivo no está disponible.');
  };

  const addMessage = (role: 'user' | 'oracle', content: string) => {
    setMessages((prev) => [...prev, { role, content }]);
  };

  const negotiate = async (e?: React.FormEvent) => {
    e?.preventDefault();
    const instr = instruction.trim();
    if (!instr || loading) return;
    setLoading(true);
    setError(null);
    setUnavailable(false);
    try {
      const res = await apiFetch('/contracts/negotiate', {
        method: 'POST',
        body: JSON.stringify({
          instruction: instr,
          participants: participants || [],
          session_id: draft?.session_id,
        }),
      });
      const body = await res.json();
      if (res.status === 503) {
        handleUnavailable(body);
        return;
      }
      if (!res.ok) {
        setError(body.error || 'El oráculo falló al generar el borrador.');
        return;
      }
      addMessage('user', instr);
      setDraft(body);
      setContractName(body.suggested_contract_id);
      addMessage('oracle', `Borrador v${body.version} generado: ${body.draft_terms.length} términos para ${body.proposed_parties.length} partes.`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error de conexión con el oráculo.');
    } finally {
      setLoading(false);
    }
  };

  const iterate = async (e?: React.FormEvent) => {
    e?.preventDefault();
    const fb = feedback.trim();
    if (!fb || !draft || loading) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch('/contracts/negotiate/feedback', {
        method: 'POST',
        body: JSON.stringify({ session_id: draft.session_id, feedback: fb }),
      });
      const body = await res.json();
      if (res.status === 503) {
        handleUnavailable(body);
        return;
      }
      if (!res.ok) {
        setError(body.error || 'No se pudo iterar el borrador.');
        return;
      }
      addMessage('user', fb);
      setDraft(body);
      addMessage('oracle', `Borrador v${body.version} generado: ${body.draft_terms.length} términos.`);
      setFeedback('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error de conexión con el oráculo.');
    } finally {
      setLoading(false);
    }
  };

  const materialize = async (e?: React.FormEvent) => {
    e?.preventDefault();
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
        body: JSON.stringify({
          contract_id: name,
          civil_description: draft.instruction,
          participants: draft.proposed_parties.map(mapParty),
          terms: draft.draft_terms.map((t) => ({
            term_id: t.term_id,
            civil_text: t.civil_text,
            vhv: t.vhv,
            assigned_participant_id: t.assigned_participant,
          })),
        }),
      });
      const body = await res.json();
      if (!res.ok) {
        setError(body.error || 'No se pudo materializar el contrato.');
        return;
      }
      addMessage('oracle', `Contrato "${name}" materializado y guardado en la base.`);
      setDraft(null);
      setMessages([]);
      if (onMaterialized) {
        onMaterialized(name);
      } else {
        router.push(`/contracts/${name}`);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al materializar el contrato.');
    } finally {
      setMaterializing(false);
    }
  };

  const audit = async () => {
    if (!contractId || critiquing) return;
    setCritiquing(true);
    setError(null);
    setUnavailable(false);
    try {
      const res = await apiFetch(`/contracts/${contractId}/critique`, { method: 'POST' });
      const body = await res.json();
      if (res.status === 503) {
        handleUnavailable(body);
        return;
      }
      if (!res.ok) {
        setError(body.error || 'No se pudo auditar el contrato.');
        return;
      }
      setCritique(body);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error de conexión con el oráculo.');
    } finally {
      setCritiquing(false);
    }
  };

  return (
    <div className="glass p-6 rounded-3xl border border-slate-900 bg-slate-900/30 space-y-5">
      {/* Cabecera */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Bot className="w-5 h-5 text-violet-500" />
            Negociación Asistida por Oráculo
          </h2>
          <p className="text-[11px] text-slate-500">DeepSeek conversa con las partes hasta el contrato idóneo (ROADMAP Bloque A)</p>
        </div>
        <div className="flex flex-col items-end gap-2 shrink-0">
          <span className={`flex items-center gap-1.5 text-[9px] font-black uppercase tracking-widest px-3 py-1 rounded-full border ${
            unavailable
              ? 'text-amber-400 bg-amber-500/10 border-amber-500/20'
              : 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
          }`}>
            <span className={`w-1.5 h-1.5 rounded-full ${unavailable ? 'bg-amber-400' : 'bg-emerald-400 animate-pulse'}`} />
            {unavailable ? 'No disponible' : 'Oráculo en vivo'}
          </span>
          <button
            onClick={() => router.push('/contracts/negotiate')}
            className="flex items-center gap-1.5 text-[10px] font-bold text-violet-400 hover:text-violet-300 transition-colors"
            title="Abrir la negociación en pantalla completa"
          >
            <Maximize2 className="w-3.5 h-3.5" />
            Pantalla completa
          </button>
        </div>
      </div>

      {unavailable && (
        <div className="p-3.5 rounded-2xl bg-amber-950/20 border border-amber-900/30 text-[11px] text-amber-200/80 leading-relaxed">
          {error} La validación heurística (SyntheticOracle) sigue funcionando con normalidad.
        </div>
      )}

      {/* Conversación */}
      {messages.length > 0 && (
        <div className="space-y-3 max-h-56 overflow-y-auto pr-1">
          {messages.map((m, i) => (
            <div
              key={i}
              className={`p-3 rounded-2xl border text-xs leading-relaxed ${
                m.role === 'user'
                  ? 'bg-slate-950/70 border-slate-800 text-slate-300 ml-8'
                  : 'bg-violet-950/20 border-violet-900/30 text-slate-300 mr-8'
              }`}
            >
              <span className="font-bold uppercase text-[9px] tracking-widest block mb-1 text-slate-500">
                {m.role === 'user' ? 'Tú (fundador)' : 'Oráculo'}
              </span>
              {m.content}
            </div>
          ))}
        </div>
      )}

      {/* Instrucción inicial */}
      <form onSubmit={negotiate} className="space-y-3">
        <div className="space-y-2">
          <label className="text-[10px] text-slate-400 font-bold block uppercase tracking-wider">
            Describe el intercambio en lenguaje natural
          </label>
          <textarea
            value={instruction}
            onChange={(e) => setInstruction(e.target.value)}
            placeholder="Ej: Max ofrece 10 horas de trabajo y quiere que Ana dé a cambio un objeto, un servicio o sus propias horas..."
            rows={3}
            className="w-full bg-slate-950 border border-slate-900 rounded-xl px-3 py-2 text-xs text-slate-300 focus:outline-none focus:border-violet-500/50 placeholder:text-slate-700"
          />
        </div>
        <button
          type="submit"
          disabled={loading || !instruction.trim()}
          className="w-full py-3 bg-violet-600 hover:bg-violet-500 disabled:bg-slate-900 text-white font-black rounded-xl text-xs uppercase tracking-wider transition-all flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              El Oráculo está redactando...
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4" />
              {draft ? 'Regenerar borrador' : 'Consultar al Oráculo'}
            </>
          )}
        </button>
      </form>

      {error && !unavailable && (
        <p className="text-[11px] text-rose-400 flex items-center gap-1.5">
          <AlertTriangle className="w-3.5 h-3.5" /> {error}
        </p>
      )}

      {/* Borrador */}
      {draft && (
        <div className="space-y-4">
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
                {draft.axiom_check.valid ? 'Axiomas cumplidos (T>0 · Partes · T17)' : 'Violaciones axiomáticas detectadas'}
              </span>
            </div>
            {draft.axiom_check.violations.length > 0 && (
              <ul className="mt-2 space-y-1">
                {draft.axiom_check.violations.map((v, i) => (
                  <li key={i} className="text-[11px] text-rose-300 flex items-start gap-1.5">
                    <XCircle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                    <span><strong>{v.axiom}:</strong> {v.message}</span>
                  </li>
                ))}
              </ul>
            )}
            {draft.axiom_check.warnings.length > 0 && (
              <ul className="mt-2 space-y-1">
                {draft.axiom_check.warnings.map((w, i) => (
                  <li key={i} className="text-[11px] text-amber-300 flex items-start gap-1.5">
                    <AlertTriangle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                    <span><strong>{w.axiom}:</strong> {w.message}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Razonamiento */}
          <div className="p-4 bg-slate-950/70 border border-slate-800 rounded-2xl">
            <p className="text-xs text-slate-300 leading-relaxed italic">
              &quot;{draft.reasoning || 'El oráculo no incluyó explicación.'}&quot;
            </p>
          </div>

          {/* Términos */}
          <div className="space-y-2">
            <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider flex items-center gap-1.5">
              <ClipboardList className="w-3.5 h-3.5" /> Borrador v{draft.version} — {draft.draft_terms.length} términos · {draft.proposed_parties.length} partes
            </span>
            {draft.draft_terms.map((t) => (
              <div key={t.term_id} className="p-3 bg-slate-950/50 border border-slate-800 rounded-xl text-xs space-y-1">
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

          {/* Retroalimentación */}
          <form onSubmit={iterate} className="space-y-3 pt-2 border-t border-slate-800">
            <div className="space-y-2">
              <label className="text-[10px] text-slate-400 font-bold block uppercase tracking-wider">
                Respuesta de las partes (iteración)
              </label>
              <textarea
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                placeholder="Ej: Ana no puede dar más de 5 horas; sugiere un servicio de diseño..."
                rows={2}
                className="w-full bg-slate-950 border border-slate-900 rounded-xl px-3 py-2 text-xs text-slate-300 focus:outline-none focus:border-violet-500/50 placeholder:text-slate-700"
              />
            </div>
            <button
              type="submit"
              disabled={loading || !feedback.trim()}
              className="w-full py-2.5 bg-slate-800 hover:bg-slate-700 disabled:bg-slate-900 text-white font-black rounded-xl text-xs uppercase tracking-wider transition-all flex items-center justify-center gap-2"
            >
              <Send className="w-4 h-4" />
              Iterar borrador
            </button>
          </form>

          {/* Materializar */}
          <form onSubmit={materialize} className="space-y-3 pt-2 border-t border-slate-800">
            <div className="space-y-2">
              <label className="text-[10px] text-slate-400 font-bold block uppercase tracking-wider">
                Nombre del contrato a materializar
              </label>
              <input
                value={contractName}
                onChange={(e) => setContractName(e.target.value)}
                className="w-full bg-slate-950 border border-slate-900 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500/50"
              />
            </div>
            <button
              type="submit"
              disabled={materializing || draft.draft_terms.length === 0}
              className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-900 text-white font-black rounded-xl text-xs uppercase tracking-wider transition-all flex items-center justify-center gap-2"
            >
              {materializing ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  Materializando...
                </>
              ) : (
                <>
                  <FilePlus2 className="w-4 h-4" />
                  Materializar contrato (POST /contracts/)
                </>
              )}
            </button>
          </form>
        </div>
      )}

      {/* Auditoría del contrato existente */}
      {contractId && (
        <div className="pt-2 border-t border-slate-800 space-y-4">
          <button
            onClick={audit}
            disabled={critiquing}
            className="w-full py-3 bg-slate-800 hover:bg-slate-700 disabled:bg-slate-900 text-white font-black rounded-xl text-xs uppercase tracking-wider transition-all flex items-center justify-center gap-2"
          >
            {critiquing ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                Auditar contrato...
              </>
            ) : (
              <>
                <ShieldAlert className="w-4 h-4" />
                Auditar este contrato contra los axiomas
              </>
            )}
          </button>

          {critique && (
            <div className="space-y-3">
              <div className={`p-4 rounded-2xl border ${
                critique.valid
                  ? 'bg-emerald-950/20 border-emerald-900/30'
                  : 'bg-rose-950/20 border-rose-900/30'
              }`}>
                <div className="flex items-center gap-2">
                  {critique.valid ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                  ) : (
                    <ShieldAlert className="w-5 h-5 text-rose-500" />
                  )}
                  <span className={`text-xs font-black uppercase tracking-wider ${
                    critique.valid ? 'text-emerald-400' : 'text-rose-400'
                  }`}>
                    {critique.valid ? 'Contrato coherente' : 'Contrato con hallazgos'}
                  </span>
                </div>
                {critique.issues.map((issue, i) => (
                  <p key={i} className="mt-2 text-[11px] text-slate-300">
                    <span className="font-mono text-rose-400">{issue.axiom}</span>
                    <span className="text-slate-600"> ({issue.severity})</span> — {issue.message}
                  </p>
                ))}
              </div>
              {critique.recommendations.length > 0 && (
                <div className="p-4 bg-slate-950/70 border border-slate-800 rounded-2xl space-y-1.5">
                  <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Recomendaciones del oráculo</span>
                  {critique.recommendations.map((r, i) => (
                    <p key={i} className="text-[11px] text-slate-300 flex items-start gap-1.5">
                      <Sparkles className="w-3.5 h-3.5 mt-0.5 text-violet-400 shrink-0" /> {r}
                    </p>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
