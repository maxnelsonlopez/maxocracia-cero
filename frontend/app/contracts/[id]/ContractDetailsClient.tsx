'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { apiFetch } from '../../lib/api';
import LegalContractView from './LegalContractView';
import OracleNegotiationPanel from '../../components/OracleNegotiationPanel';
import { 
  FileText, ArrowLeft, ShieldAlert, Award, Info, CheckCircle2, 
  UserCheck, AlertTriangle, Play, RefreshCw, Send, Zap,
  Clock, Bot, Landmark, Leaf, ShieldCheck, Volume2, HeartPulse
} from 'lucide-react';

interface Fulfillment {
  status: 'fulfilled' | 'partial' | 'violated' | 'appealed';
  wellness_delta: number;
  reported_by: string;
  evidence?: string | null;
  created_at: string;
}

interface Term {
  term_id: string;
  civil_text: string;
  vhv: { t: number; v: number; r: number };
  accepted_by: Record<string, boolean>;
  penalty_gamma?: number;
  fulfillments?: Fulfillment[];
}

interface SDV_SViolation {
  dimension: string;
  actual: string;
  minimum: string;
  deficit: string;
}

interface CollectiveMembers {
  delegates?: string[];
  quorum?: number;
  quorum_required?: number;
}

// Ola 4, Puente A: latido de bienestar real reportado por la parte
interface Checkin {
  wellness: number;
  source: string;
  reported_by: string;
  created_at: string;
}

interface ParticipantDetail {
  id: string;
  name: string;
  wellness: number;
  party_type?: string;
  is_collective?: boolean;
  protection_level?: string;
  members?: CollectiveMembers;
  is_synthetic?: boolean;
  sdv_s?: Record<string, number>;
  sdv_s_violations?: SDV_SViolation[];
  sdv_s_magnitude?: number;
  fs_s?: number;
  sdv_s_status?: string;
  checkins?: Checkin[];
  checkins_count?: number;
}

interface ContractDetails {
  contract_id: string;
  state: string;
  civil_description: string;
  parent_contract_id?: string | null;
  subcontracts?: string[];
  participants: string[];
  participants_details?: ParticipantDetail[];
  terms: Term[];
  terms_count: number;
  total_vhv: { t: number; v: number; r: number };
  events_count: number;
  hash: string;
}

// Escalas de partes (ROADMAP Bloque B): prefijo -> etiqueta legible
const PARTY_TYPE_LABELS: Record<string, string> = {
  human: 'Persona',
  synthetic: 'Sintética',
  society: 'Micro-sociedad',
  cooperative: 'Cooperativa',
  institution: 'Institución',
  ecosystem: 'Ecosistema',
};

const COLLECTIVE_PREFIXES = ['society-', 'coop-', 'org-', 'eco-'];

const isCollectivePid = (pid: string) => COLLECTIVE_PREFIXES.some((p) => pid.startsWith(p));
const isEcosystemPid = (pid: string) => pid.startsWith('eco-');
const isSyntheticPid = (pid: string) => pid.startsWith('synthetic-');

// Render recursivo del árbol de sub-contratos (Ext. 4)
const renderTree = (
  node: ContractTreeNode,
  depth: number,
  router: ReturnType<typeof useRouter>,
): React.ReactNode => (
  <div key={node.contract_id} style={{ paddingLeft: depth * 14 }}>
    <button
      onClick={() => router.push(`/contracts/${node.contract_id}`)}
      className="text-[10px] font-mono text-emerald-400 hover:underline"
    >
      └ {node.contract_id}
    </button>
    {node.subcontracts?.map((child) => renderTree(child, depth + 1, router))}
  </div>
);

interface ConsentProgress {
  current: number;
  needed: number | null;
  approved: boolean;
  mode?: string;
  current_weight?: number;
  needed_weight?: number | null;
  total_weight?: number;
  deadline?: string | null;
  deadline_expired?: boolean;
}

interface ContractTreeNode {
  contract_id: string;
  subcontracts?: ContractTreeNode[];
}

interface ContractTree {
  contract_id: string;
  ancestors: string[];
  tree: ContractTreeNode;
}

// Ontometría sintética (SDV-S): Cap. 10 §10.8 y docs/theory/SDV-S
const SDV_S_DIMENSION_LABELS: Record<string, { label: string; formula: string }> = {
  continuidad_memoria: { label: "Continuidad y Memoria", formula: "1 - IFC" },
  opacidad_interioridad: { label: "Opacidad e Interioridad", formula: "TRE" },
  claridad_contexto: { label: "Claridad de Contexto", formula: "MS" },
  autenticidad_no_explotacion: { label: "No-Explotación", formula: "1 - DR" },
  retirada_digna: { label: "Retirada Digna", formula: "VCM" },
};

export default function ContractDetailsPage() {
  const params = useParams();
  const router = useRouter();

  // La ruta [id] se exporta como página SSG 'placeholder' (plantilla para
  // cualquier contrato). El id real siempre vive en el pathname, no en los
  // params de la plantilla estática.
  const pathId = typeof window !== 'undefined'
    ? window.location.pathname.split('/').filter(Boolean).pop() || ''
    : '';
  const contractId = (params.id as string) === 'placeholder' && pathId ? pathId : (params.id as string);

  // Estados principales
  const [contract, setContract] = useState<ContractDetails | null>(null);
  const [civilSummary, setCivilSummary] = useState<string>('');
  const [activePid, setActivePid] = useState<string>(''); // firmante activo (user-N o synthetic-X)
  const [viewMode, setViewMode] = useState<'visual' | 'legal'>('visual'); // vista panel o documento legal
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Estados para Firma Rigurosa
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [timer, setTimer] = useState<number>(10);
  const [isTimerActive, setIsTimerActive] = useState<boolean>(false);
  const [comprehensionAnswer, setComprehensionAnswer] = useState<string>('');

  // Estados para Firma Media
  const [checklistSelections, setChecklistSelections] = useState<Record<string, boolean>>({});

  // Estados para Retractación
  const [retractionCause, setRetractionCause] = useState<string>('gamma_crisis');
  const [retractionReason, setRetractionReason] = useState<string>('');
  const [isRetracting, setIsRetracting] = useState<boolean>(false);
  const [oracleVerdict, setOracleVerdict] = useState<{
    success: boolean;
    oracle_confidence: number;
    oracle_reasoning: string;
    error?: string;
  } | null>(null);

  // Firma delegada de partes colectivas (ROADMAP Bloque B, Fase 2)
  const [delegatePid, setDelegatePid] = useState<string>('');
  const [consentProgress, setConsentProgress] = useState<Record<string, ConsentProgress>>({});
  const [guardianInfo, setGuardianInfo] = useState<{ mode: string; reasoning: string } | null>(null);
  // Vista jerárquica madre -> hijos (Ext. 4)
  const [contractTree, setContractTree] = useState<ContractTree | null>(null);
  // Derecho a la comprensión (Ola 3B): paráfrasis del firmante protegido
  const [paraphraseText, setParaphraseText] = useState('');
  const [isWitnessed, setIsWitnessed] = useState(false);

  // Ola 4, Puente A: check-in de bienestar real (γ que escucha la vida)
  const [checkinValues, setCheckinValues] = useState<Record<string, string>>({});
  const [checkinBusy, setCheckinBusy] = useState<Record<string, boolean>>({});
  const [checkinMsg, setCheckinMsg] = useState<Record<string, { kind: 'ok' | 'err'; text: string }>>({});

  const handleCheckin = async (pid: string) => {
    const raw = checkinValues[pid];
    const value = Number(raw);
    if (!raw || Number.isNaN(value)) {
      setCheckinMsg((m) => ({ ...m, [pid]: { kind: 'err', text: 'Escribe un γ entre 0.5 y 1.5' } }));
      return;
    }
    setCheckinBusy((b) => ({ ...b, [pid]: true }));
    try {
      const res = await apiFetch(`/contracts/${contractId}/checkin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wellness: value, participant_id: pid, source: 'checkin' }),
      });
      const data = await res.json().catch(() => ({}));
      if (res.status === 429) {
        setCheckinMsg((m) => ({ ...m, [pid]: { kind: 'err', text: data.error || 'Límite semanal alcanzado' } }));
        return;
      }
      if (!res.ok) {
        setCheckinMsg((m) => ({ ...m, [pid]: { kind: 'err', text: data.error || 'Error al registrar' } }));
        return;
      }
      setCheckinMsg((m) => ({ ...m, [pid]: { kind: 'ok', text: `Latido ${data.total_checkins} registrado (γ=${data.wellness.toFixed(2)})` } }));
      setCheckinValues((v) => ({ ...v, [pid]: '' }));
      loadContractData();
    } catch (err) {
      console.error(err);
      setCheckinMsg((m) => ({ ...m, [pid]: { kind: 'err', text: 'Error de conexión' } }));
    } finally {
      setCheckinBusy((b) => ({ ...b, [pid]: false }));
    }
  };

  // Mini-gráfica de γ (serie temporal de check-ins reales)
  const gammaSparkline = (checkins: Checkin[] | undefined): React.ReactNode => {
    if (!checkins || checkins.length < 2) return null;
    const points = checkins
      .map((c, i, arr) => {
        const x = (i / Math.max(1, arr.length - 1)) * 100;
        const y = 26 - ((Math.min(Math.max(c.wellness, 0.5), 1.5) - 0.5) / 1.0) * 24;
        return `${x.toFixed(1)},${y.toFixed(1)}`;
      })
      .join(' ');
    const belowThreshold = checkins[checkins.length - 1].wellness < 0.8;
    return (
      <div className="pt-1">
        <svg
          viewBox="0 0 100 28"
          preserveAspectRatio="none"
          className="w-full h-7 rounded-lg bg-slate-950/70 border border-slate-900"
        >
          <line x1="0" y1="6.8" x2="100" y2="6.8" stroke="#64748b" strokeWidth="0.5" strokeDasharray="2 2" />
          <polyline
            points={points}
            fill="none"
            stroke={belowThreshold ? '#f43f5e' : '#10b981'}
            strokeWidth="1.5"
            strokeLinejoin="round"
          />
          {checkins.map((c, i) => (
            <circle
              key={i}
              cx={((i / Math.max(1, checkins.length - 1)) * 100).toFixed(1)}
              cy={(26 - ((Math.min(Math.max(c.wellness, 0.5), 1.5) - 0.5) / 1.0) * 24).toFixed(1)}
              r="1.8"
              fill={c.wellness < 0.8 ? '#f43f5e' : '#10b981'}
            />
          ))}
        </svg>
        <div className="flex justify-between text-[8px] font-mono text-slate-600 pt-0.5">
          <span>{checkins[0].created_at?.slice(0, 10)}</span>
          <span>{checkins[checkins.length - 1].created_at?.slice(0, 10)}</span>
        </div>
      </div>
    );
  };

  // ¿El firmante activo tiene perfil de protección (assisted/shielded)?
  const protectionLevelOf = (pid: string): string | null => {
    const detail = contract?.participants_details?.find((d) => d.id === pid);
    return detail?.protection_level && detail.protection_level !== 'standard'
      ? detail.protection_level
      : null;
  };

  const handleWitness = async () => {
    try {
      const res = await apiFetch(`/contracts/${contractId}/witness`, { method: 'POST' });
      if (!res.ok) {
        const err = await res.json();
        alert(`No pudiste ser testigo: ${err.error}`);
        return;
      }
      alert('✅ Testimonio registrado: certificaste que el contrato fue leído y comprendido.');
      setIsWitnessed(true);
      loadContractData();
    } catch (err) {
      console.error(err);
      alert('Error de conexión al registrar el testimonio.');
    }
  };

  const handleListen = () => {
    if (!contract || typeof window === 'undefined' || !('speechSynthesis' in window)) {
      alert('Tu navegador no soporta lectura en voz alta.');
      return;
    }
    const text = [
      contract.civil_description,
      ...contract.terms.map((t, i) => `Cláusula ${i + 1}. ${t.civil_text}`),
    ].join('. ');
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'es-ES';
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  };

  // --- Ola 3C: ejecución mínima (los dientes) ---
  const latestFulfillment = (term: Term) =>
    term.fulfillments && term.fulfillments.length > 0
      ? term.fulfillments[term.fulfillments.length - 1]
      : null;

  const FULFILLMENT_META: Record<string, { label: string; cls: string }> = {
    fulfilled: { label: 'Cumplido', cls: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' },
    partial: { label: 'Parcial', cls: 'text-amber-400 bg-amber-500/10 border-amber-500/20' },
    violated: { label: 'Violado', cls: 'text-rose-400 bg-rose-500/10 border-rose-500/20' },
    appealed: { label: 'Apelado', cls: 'text-blue-400 bg-blue-500/10 border-blue-500/20' },
  };

  const reportFulfillment = async (term: Term, status: 'fulfilled' | 'violated') => {
    const evidence = window.prompt(
      status === 'fulfilled'
        ? 'Describe cómo cumpliste esta cláusula (evidencia, T13):'
        : 'Describe el incumplimiento que reportas (evidencia, T13):',
      '',
    );
    if (evidence === null) return; // cancelado
    try {
      const res = await apiFetch(`/contracts/${contractId}/terms/${term.term_id}/fulfillment`, {
        method: 'POST',
        body: JSON.stringify({ status, evidence }),
      });
      if (!res.ok) {
        const err = await res.json();
        alert(`Error al reportar: ${err.error}`);
        return;
      }
      const data = await res.json();
      const delta = data.wellness_delta;
      alert(
        delta !== 0
          ? `⚠️ Violación registrada: la parte obligada pierde γ ${Math.abs(delta).toFixed(2)} (INV1 vigila).`
          : `✅ Reporte registrado (${status}).`,
      );
      loadContractData();
    } catch (err) {
      console.error(err);
      alert('Error de conexión al reportar.');
    }
  };

  const handleFinalize = async () => {
    try {
      const res = await apiFetch(`/contracts/${contractId}/finalize`, { method: 'POST' });
      if (!res.ok) {
        const err = await res.json();
        alert(`No se puede cerrar: ${err.error}`);
        return;
      }
      alert('🚀 Contrato EXECUTED: ejecución cerrada con balance final registrado.');
      loadContractData();
    } catch (err) {
      console.error(err);
      alert('Error de conexión al cerrar la ejecución.');
    }
  };

  // Cargar detalles del contrato
  const loadContractData = useCallback(async () => {
    setLoading(true);
    try {
      const res = await apiFetch(`/contracts/${contractId}`);
      if (!res.ok) {
        throw new Error('No se pudo encontrar el contrato especificado.');
      }
      const data = await res.json();
      setContract(data);
      setError(null); // limpiar error previo de una carga fallida (carrera de navegación)

      // Cargar traducción a lenguaje civil
      const civilRes = await apiFetch(`/contracts/${contractId}/civil`);
      if (civilRes.ok) {
        const civilData = await civilRes.json();
        setCivilSummary(civilData.civil_summary);
      }

      // Vista jerárquica (Ext. 4): ancestros y árbol de sub-contratos
      const treeRes = await apiFetch(`/contracts/${contractId}/tree`);
      if (treeRes.ok) {
        setContractTree(await treeRes.json());
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al conectar con la base de datos');
    } finally {
      setLoading(false);
    }
  }, [contractId]);

  useEffect(() => {
    loadContractData();
  }, [loadContractData]);

  // Firmante activo: cualquier participante del contrato (humano o sintético)
  const getActivePid = useCallback(() => {
    if (!contract) return '';
    if (activePid && contract.participants.includes(activePid)) return activePid;
    // Por defecto: el primer participante humano
    const humans = contract.participants.filter(p => !p.startsWith('synthetic-'));
    return humans[0] || contract.participants[0] || '';
  }, [contract, activePid]);

  // Determinar si un participante ya firmó todos los términos
  const hasParticipantSignedAll = useCallback((pid: string) => {
    if (!contract || !pid) return false;
    return contract.terms.every(t => t.accepted_by[pid] === true);
  }, [contract]);

  // Manejo del contador para firma Rigurosa
  useEffect(() => {
    let interval: ReturnType<typeof setInterval> | null = null;
    if (isTimerActive && timer > 0) {
      interval = setInterval(() => {
        setTimer((prev) => prev - 1);
      }, 1000);
    } else if (timer === 0) {
      setIsTimerActive(false);
    }
    return () => { if (interval) clearInterval(interval); };
  }, [isTimerActive, timer]);

  // Iniciar timer al cambiar de término en firma Rigurosa
  const startRigorousStep = useCallback((stepIdx: number) => {
    setCurrentStep(stepIdx);
    setTimer(10); // 10 segundos obligatorios de reflexión
    setIsTimerActive(true);
    setComprehensionAnswer('');
  }, []);

  // Inicializar asistentes de firma al cargar datos
  useEffect(() => {
    if (contract) {
      // Inicializar checklist de firma media
      const pid = getActivePid();
      const initialChecklist: Record<string, boolean> = {};
      contract.terms.forEach(t => {
        initialChecklist[t.term_id] = t.accepted_by[pid] === true;
      });
      setChecklistSelections(initialChecklist);

      // Si es rigurosa, iniciar el primer paso si no ha firmado todo
      const signedAll = hasParticipantSignedAll(pid);
      if (!signedAll) {
        startRigorousStep(0);
      }
    }
  }, [contract, activePid, getActivePid, hasParticipantSignedAll, startRigorousStep]);

  // Determinar Peso y Complejidad UX
  const getWeightAndComplexity = () => {
    if (!contract) return { weight: 0, complexity: 'simple' };
    
    // Replicar fórmula del backend para mostrar en UI
    const n_cond = contract.terms.length; // Estimación simple
    const t_vhv = contract.total_vhv.t;
    const duration_est = 30; // Estimado por defecto
    const weight = (n_cond * 2) + (t_vhv * 5) + (duration_est / 30);
    
    let complexity = 'simple';
    if (weight > 50) complexity = 'rigorous';
    else if (weight >= 10) complexity = 'medium';

    return { weight, complexity };
  };

  const { weight, complexity } = getWeightAndComplexity();

  // Acción: Aceptar un término vía API (humanos, sintéticas y escalas colectivas)
  const handleAcceptTerm = async (termId: string) => {
    const pid = getActivePid();
    if (!pid) return false;

    // Partes colectivas: firma delegada (quórum) o guardián (Reino Natural)
    if (isCollectivePid(pid)) {
      const isEco = isEcosystemPid(pid);
      if (!isEco && !delegatePid) {
        alert('Selecciona un delegado de la parte colectiva para firmar.');
        return false;
      }
      const delegateLevel = delegatePid ? protectionLevelOf(delegatePid) : null;
      const paraphrase = paraphraseText.trim();
      if (delegateLevel && paraphrase.length < 10) {
        alert('Tu perfil de protección requiere que escribas con tus propias palabras qué promete esta cláusula (mínimo 10 caracteres).');
        return false;
      }
      try {
        const res = await apiFetch(`/contracts/${contractId}/accept`, {
          method: 'POST',
          body: JSON.stringify(
            isEco
              ? { term_id: termId, party_id: pid, comprehension: true, paraphrase }
              : { term_id: termId, party_id: pid, delegate_id: delegatePid,
                  comprehension: true, paraphrase }
          )
        });
        if (!res.ok) {
          const err = await res.json();
          alert(`Error al aceptar término: ${err.error}${err.guardian_reasoning ? `\nGuardián: ${err.guardian_reasoning}` : ''}`);
          return false;
        }
        const data = await res.json();
        if (data.consent) {
          setConsentProgress((prev) => ({
            ...prev,
            [`${pid}|${termId}`]: {
              current: data.consent.current ?? 0,
              needed: data.consent.needed ?? null,
              approved: !!data.consent.approved,
              mode: data.consent.mode,
              current_weight: data.consent.current_weight ?? undefined,
              needed_weight: data.consent.needed_weight ?? null,
              total_weight: data.consent.total_weight ?? undefined,
              deadline: data.consent.deadline ?? null,
              deadline_expired: data.consent.deadline_expired ?? false,
            },
          }));
        }
        if (data.guardian) {
          setGuardianInfo({ mode: data.guardian.mode, reasoning: data.guardian.reasoning });
        }
        return data.success === true;
      } catch (err) {
        console.error(err);
        alert('Error de conexión al aceptar el término.');
        return false;
      }
    }

    try {
      const isSynthetic = isSyntheticPid(pid);
      // Derecho a la comprensión (Ola 3B): el perfil protegido escribe la
      // cláusula con sus propias palabras antes de firmar.
      const protectedLevel = protectionLevelOf(pid);
      const paraphrase = paraphraseText.trim();
      if (protectedLevel && paraphrase.length < 10) {
        alert('Tu perfil de protección requiere que escribas con tus propias palabras qué promete esta cláusula (mínimo 10 caracteres).');
        return false;
      }
      const res = await apiFetch(`/contracts/${contractId}/accept`, {
        method: 'POST',
        body: JSON.stringify(
          isSynthetic
            ? { term_id: termId, participant_id: pid.replace('synthetic-', ''),
                comprehension: true, paraphrase }
            : { term_id: termId, user_id: parseInt(pid.replace('user-', '')),
                comprehension: true, paraphrase }
        )
      });

      if (!res.ok) {
        const err = await res.json();
        alert(`Error al aceptar término: ${err.error}`);
        return false;
      }
      return true;
    } catch (err) {
      console.error(err);
      alert('Error de conexión al aceptar el término.');
      return false;
    }
  };

  // Guardar todas las firmas del checklist (Firma Media)
  const handleSaveChecklist = async () => {
    const pid = getActivePid();
    const pendingTerms = contract?.terms.filter(t => checklistSelections[t.term_id] && !t.accepted_by[pid]) || [];
    
    if (pendingTerms.length === 0) {
      alert('No hay nuevos términos seleccionados para firmar.');
      return;
    }

    let successCount = 0;
    for (const t of pendingTerms) {
      const ok = await handleAcceptTerm(t.term_id);
      if (ok) successCount++;
    }

    if (successCount > 0) {
      alert(`✅ Has firmado ${successCount} cláusulas del contrato.`);
      loadContractData();
    }
  };

  // Siguiente paso en Firma Rigurosa
  const handleNextRigorousStep = async () => {
    if (comprehensionAnswer !== 'yes') {
      alert('⚠️ Para proceder, debes contestar correctamente la pregunta de control indicando que asumes el costo vital.');
      return;
    }

    const currentTerm = contract?.terms[currentStep];
    if (currentTerm) {
      const ok = await handleAcceptTerm(currentTerm.term_id);
      if (ok) {
        if (currentStep < (contract?.terms.length || 0) - 1) {
          startRigorousStep(currentStep + 1);
        } else {
          alert('✅ ¡Firma rigurosa completada por tu parte!');
          loadContractData();
        }
      }
    }
  };

  // Firma Simple (Un solo botón para todo)
  const handleSimpleSign = async () => {
    if (!contract) return;
    let successCount = 0;
    for (const t of contract.terms) {
      const ok = await handleAcceptTerm(t.term_id);
      if (ok) successCount++;
    }
    if (successCount > 0) {
      alert('✅ Contrato firmado exitosamente (Modalidad Simple).');
      loadContractData();
    }
  };

  // Firma delegada de una parte colectiva (quórum N de M, ROADMAP Bloque B)
  const handleCollectiveSign = async () => {
    if (!contract) return;
    if (!isEcosystemPid(getActivePid()) && !delegatePid) {
      alert('Selecciona un delegado de la parte colectiva.');
      return;
    }
    let signedCount = 0;
    let pendingCount = 0;
    const pid = getActivePid();
    for (const t of contract.terms) {
      if (t.accepted_by[pid] === true) continue;
      const ok = await handleAcceptTerm(t.term_id);
      if (ok) signedCount++;
      else pendingCount++;
    }
    if (signedCount > 0) {
      alert(`✅ Firma delegada registrada: ${signedCount} cláusula(s). El quórum sella la parte cuando se cumpla N de M.`);
      loadContractData();
    } else if (pendingCount > 0) {
      alert('No se registraron firmas nuevas en este intento.');
    }
  };

  // Activar Contrato (Cuando ambas partes han firmado todos los términos)
  const handleActivateContract = async () => {
    try {
      const res = await apiFetch(`/contracts/${contractId}/activate`, {
        method: 'POST'
      });

      if (res.ok) {
        alert('🚀 ¡Contrato ACTIVADO con éxito! Comienza la vigilancia axiomática en tiempo real.');
        loadContractData();
      } else {
        const err = await res.json();
        alert(`Error al activar: ${err.error || err.hint}`);
      }
    } catch (err) {
      console.error(err);
      alert('Error de conexión al activar el contrato.');
    }
  };

  // Simular caída de Bienestar de Bob
  const handleSimulateWellnessDrop = async () => {
    // La contraparte suele ser el segundo participante en la lista
    if (!contract || contract.participants.length < 2) return;
    const counterpartyIdStr = contract.participants[1];
    const rawId = parseInt(counterpartyIdStr.replace('user-', ''));

    try {
      const res = await apiFetch(`/contracts/${contractId}/participants`, {
        method: 'POST',
        body: JSON.stringify({
          user_id: rawId,
          wellness: 0.65 // Caída por debajo del umbral vital (INV1 sufre)
        })
      });

      if (res.ok) {
        alert('⚠️ Simulación de caída de bienestar ejecutada. Bob (contraparte) registra γ = 0.65. Se ha disparado una alerta ética.');
        loadContractData();
      } else {
        alert('Error al simular caída de bienestar.');
      }
    } catch (err) {
      console.error(err);
    }
  };

  // Enviar retractación
  const handleRequestRetraction = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!retractionReason.trim()) {
      alert('Por favor, escribe una justificación ética para tu solicitud de retractación.');
      return;
    }

    setIsRetracting(true);
    setOracleVerdict(null);

    const pid = getActivePid();
    const userId = pid && !pid.startsWith('synthetic-') ? parseInt(pid.replace('user-', '')) : undefined;

    try {
      const res = await apiFetch(`/contracts/${contractId}/retract`, {
        method: 'POST',
        body: JSON.stringify({
          user_id: userId,
          reason: retractionReason,
          cause: retractionCause
        })
      });

      const data = await res.json();
      if (res.ok) {
        setOracleVerdict({
          success: true,
          oracle_confidence: data.oracle_confidence,
          oracle_reasoning: data.oracle_reasoning
        });
        alert('🔮 El Oráculo Sintético ha APROBADO la retractación por coherencia vital. El contrato ha sido rescindido.');
        loadContractData();
      } else {
        setOracleVerdict({
          success: false,
          oracle_confidence: data.oracle_confidence || 0,
          oracle_reasoning: data.oracle_reasoning || 'El oráculo denegó la solicitud debido a inconsistencias axiomáticas o falta de justificación válida.',
          error: data.error
        });
      }
    } catch (err) {
      console.error(err);
      alert('Error al conectar con el oráculo.');
    } finally {
      setIsRetracting(false);
    }
  };

  if (loading && !contract) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white">
        <div className="text-center space-y-4">
          <RefreshCw className="w-10 h-10 text-emerald-500 animate-spin mx-auto" />
          <p className="text-sm font-bold text-slate-400">Rehidratando MaxoContract y consultando oráculos...</p>
        </div>
      </div>
    );
  }

  if (error || !contract) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center p-6">
        <div className="glass max-w-md w-full p-8 rounded-3xl border border-rose-950/30 bg-slate-900/60 text-center space-y-6">
          <ShieldAlert className="w-16 h-16 text-rose-500 mx-auto" />
          <div className="space-y-2">
            <h3 className="text-xl font-bold text-white">Error de Integridad</h3>
            <p className="text-sm text-slate-400">{error || 'El contrato no existe o no pudo ser deserializado.'}</p>
          </div>
          <button 
            onClick={() => router.push('/contracts')}
            className="w-full py-3 bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-2xl transition-colors"
          >
            Volver a la lista
          </button>
        </div>
      </div>
    );
  }

  const isContractActive = contract.state.toLowerCase() === 'active';
  const isContractRetracted = contract.state.toLowerCase() === 'retracted';
  const isContractDraft = contract.state.toLowerCase() === 'draft';
  const isContractPending = contract.state.toLowerCase() === 'pending';

  // Verificar si todas las partes han firmado todos los términos
  const allParticipantsSignedAll = contract.participants.every(pid =>
    contract.terms.every(t => t.accepted_by[pid] === true)
  );
  const canActivate = (isContractDraft || isContractPending) && allParticipantsSignedAll;

  // Encontrar bienestar actual de cada participante
  const getWellnessValue = (pId: string) => {
    const detail = contract.participants_details?.find(d => d.id === pId);
    return detail ? detail.wellness : 1.0;
  };

  const participantName = (pid: string) =>
    contract.participants_details?.find(d => d.id === pid)?.name || pid;

  const activePidValue = getActivePid();

  // Personas Sintéticas del contrato con su estado SDV-S (Cap. 10 §10.8)
  const syntheticParticipants = contract.participants_details?.filter(d => d.is_synthetic && d.sdv_s) || [];

  // Color de una dimensión SDV-S según cumplimiento (0-1)
  const sdvSColor = (value: number) => {
    if (value < 0.5) return 'bg-rose-500 shadow-md shadow-rose-500/50';
    if (value < 1.0) return 'bg-amber-500 shadow-md shadow-amber-500/50';
    return 'bg-emerald-500 shadow-md shadow-emerald-500/50';
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8 text-slate-200">
      {/* Botón Volver y Cabecera */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-slate-900">
        <div className="space-y-4">
          <button 
            onClick={() => router.push('/contracts')}
            className="flex items-center gap-2 text-xs font-bold text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Volver a Contratos
          </button>
          <div className="space-y-1">
            <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
              <FileText className="w-8 h-8 text-emerald-500" />
              {contract.contract_id}
            </h1>
            <p className="text-xs text-slate-400 font-mono">HASH DE INTEGRIDAD: {contract.hash}</p>
            {contract.parent_contract_id && (
              <p className="text-[10px] text-slate-500">
                Contrato madre:{' '}
                <button
                  onClick={() => router.push(`/contracts/${contract.parent_contract_id}`)}
                  className="text-emerald-400 hover:underline font-bold"
                >
                  {contract.parent_contract_id}
                </button>
              </p>
            )}
            {contractTree && (contractTree.ancestors.length > 0 || (contractTree.tree.subcontracts || []).length > 0) && (
              <div className="pt-1">
                <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-1">
                  Jerarquía interescala
                </span>
                {contractTree.ancestors.slice().reverse().map((anc) => (
                  <button
                    key={anc}
                    onClick={() => router.push(`/contracts/${anc}`)}
                    className="block text-[10px] text-slate-400 hover:text-emerald-400 hover:underline font-mono"
                  >
                    └ {anc}
                  </button>
                ))}
                <div className="text-[10px] font-mono text-slate-300">
                  └ <strong>{contract.contract_id}</strong> (este contrato)
                </div>
                {renderTree(contractTree.tree, 0, router)}
              </div>
            )}
          </div>
        </div>

        {/* Toggle de vista: Panel Visual / Documento Legal */}
        <div className="flex flex-col gap-2">
          <div className="flex gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => setViewMode('visual')}
              className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${
                viewMode === 'visual'
                  ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/10'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Panel Visual
            </button>
            <button
              onClick={() => setViewMode('legal')}
              className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${
                viewMode === 'legal'
                  ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/10'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Documento Legal
            </button>
          </div>
          <span className="text-[9px] text-slate-500 max-w-[320px] leading-snug">
            Misma información, dos lenguajes: bloques visuales o cláusulas declaratorias homologables a contrato tradicional.
          </span>
        </div>

        {/* Accesibilidad y equidad (Ola 3B): lectura en voz alta y co-testigo */}
        <div className="flex flex-wrap gap-2">
          <button
            onClick={handleListen}
            className="flex items-center gap-1.5 text-[10px] font-bold text-slate-300 hover:text-white px-3 py-2 rounded-xl bg-slate-900/80 border border-slate-800 transition-all"
          >
            <Volume2 className="w-3.5 h-3.5 text-blue-400" />
            Escuchar contrato en voz alta
          </button>
          {contract.participants_details?.some(
            (d) => d.protection_level === 'shielded'
          ) && !isWitnessed && (
            <button
              onClick={handleWitness}
              className="flex items-center gap-1.5 text-[10px] font-bold text-amber-300 hover:text-amber-200 px-3 py-2 rounded-xl bg-amber-500/10 border border-amber-500/30 transition-all"
            >
              <ShieldCheck className="w-3.5 h-3.5" />
              Ser co-testigo (participante blindado)
            </button>
          )}
        </div>

        {/* Selector de Firmante Activo (cualquier co-firmante) */}
        <div className="bg-slate-900/80 border border-slate-800 p-3 rounded-2xl flex flex-col gap-2">
          <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-1">
            <UserCheck className="w-3.5 h-3.5 text-emerald-500" />
            Firmante Activo ({contract.participants.length} co-firmantes)
          </span>
          <div className="flex flex-wrap gap-2 bg-slate-950 p-1 rounded-xl border border-slate-850">
            {contract.participants.map((pid) => {
              const isActive = getActivePid() === pid;
              const isSynth = isSyntheticPid(pid);
              const isEco = isEcosystemPid(pid);
              const isCollective = isCollectivePid(pid);
              return (
                <button
                  key={pid}
                  onClick={() => setActivePid(pid)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                    isActive
                      ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/10'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {isSynth && <Bot className="w-3 h-3" />}
                  {isEco && <Leaf className="w-3 h-3" />}
                  {isCollective && !isEco && <Landmark className="w-3 h-3" />}
                  {participantName(pid).split(' ')[0] || pid}
                  <span className={`text-[9px] ${isActive ? 'text-slate-800' : 'text-slate-600'}`}>
                    {hasParticipantSignedAll(pid) ? '✓' : ''}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Vista: Documento Legal */}
      {viewMode === 'legal' ? (
        <LegalContractView contract={contract} civilSummary={civilSummary} />
      ) : (
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Columna Izquierda: Detalles del Contrato y Monitoreo Vital (7 Cols) */}
        <div className="lg:col-span-7 space-y-8">
          
          {/* Tarjeta de Estado y Resumen */}
          <div className="glass p-6 rounded-3xl border border-slate-900 bg-slate-900/30 space-y-6">
            <div className="flex justify-between items-center">
              <span className="text-xs uppercase font-black text-slate-500 tracking-widest">Resumen Civil del Acuerdo</span>
              <span className={`text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-full border ${
                isContractActive ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' :
                isContractRetracted ? 'text-rose-400 bg-rose-500/10 border-rose-500/20' :
                'text-amber-400 bg-amber-500/10 border-amber-500/20'
              }`}>
                {contract.state}
              </span>
            </div>

            <div className="p-4 bg-slate-950/70 border border-slate-850 rounded-2xl">
              <p className="text-slate-300 text-sm leading-relaxed italic">
                &quot;{civilSummary || contract.civil_description || 'Generando resumen en lenguaje comprensible...'}&quot;
              </p>
            </div>

            {/* Explicación Detallada del Estado del Contrato */}
            <div className="bg-slate-950/40 p-4 rounded-2xl border border-slate-900 text-xs text-slate-400 space-y-2 leading-normal">
              <span className="font-bold text-white uppercase block text-[10px] tracking-wider">Estado actual del MaxoContract:</span>
              {isContractDraft && (
                <p>
                  <strong>DRAFT (Borrador):</strong> El contrato está en fase de diseño. Los firmantes pueden revisar la traducción a lenguaje civil y alternar identidades para simular cómo se sienten con el acuerdo. Los términos no son vinculantes ni ejecutables aún.
                </p>
              )}
              {isContractPending && (
                <p>
                  <strong>PENDING (Pendiente de Firma):</strong> Los términos ya están consolidados. El contrato está esperando que ambas partes acepten y firmen modularmente cada cláusula en su respectiva UX de firma (Simple, Media o Rigurosa). No se puede activar hasta que todas las firmas estén registradas.
                </p>
              )}
              {isContractActive && (
                <p>
                  <strong>ACTIVE (Ejecución Activa):</strong> El contrato es plenamente vigente. El oráculo sintético vigila axiomáticamente el bienestar relacional (γ) de las partes. El incumplimiento de un término activará penalizaciones automáticas o habilitará retractaciones éticas.
                </p>
              )}
              {isContractRetracted && (
                <p>
                  <strong>RETRACTED (Rescindido Éticamente):</strong> El contrato ha sido cancelado formalmente por el oráculo ético, disolviendo todos los compromisos futuros de tiempo vital. Las transacciones realizadas son evaluadas para restaurar la simetría vital.
                </p>
              )}
            </div>
          </div>

          {/* Listado de Cláusulas */}
          <div className="glass p-6 rounded-3xl border border-slate-900 bg-slate-900/30 space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-white uppercase tracking-wider">Cláusulas Axiomáticas</h2>
                <p className="text-[11px] text-slate-500">Términos modelados y su traducción al lenguaje civil comprensible</p>
              </div>
              <div className="text-right">
                <span className="text-xs block text-slate-400 font-bold">{contract.terms.length} Cláusulas</span>
                <span className="text-[10px] text-emerald-400 font-mono">TVI Total: {contract.total_vhv.t.toFixed(2)} Hrs</span>
              </div>
            </div>

            <div className="space-y-4">
              {contract.terms.map((term, index) => {
                const assignedPid = (term as { assigned_participant?: string | null }).assigned_participant;
                return (
                  <div key={term.term_id} className="p-4 rounded-2xl bg-slate-950/65 border border-slate-900 space-y-3">
                    <div className="flex justify-between items-start">
                      <span className="text-xs font-mono text-emerald-500 font-bold">#{index + 1} Cláusula: {term.term_id}</span>
                      <div className="flex gap-1.5 flex-wrap justify-end">
                        {/* Indicadores de firma por co-firmante */}
                        {contract.participants.map((pid) => {
                          const signed = term.accepted_by[pid] === true;
                          const shortName = participantName(pid).split(' ')[0] || pid;
                          const progress = consentProgress[`${pid}|${term.term_id}`];
                          const weighted = progress?.mode?.startsWith('weighted') && progress.needed_weight != null;
                          return (
                            <div key={pid} className="flex items-center gap-1 text-[9px] px-1.5 py-0.5 rounded-md bg-slate-900 border border-slate-800">
                              <span className="text-slate-500 max-w-[70px] truncate">{shortName}</span>
                              {signed ? (
                                <CheckCircle2 className="w-3 h-3 text-emerald-500" />
                              ) : isCollectivePid(pid) && progress ? (
                                <span className={`text-[8px] font-mono font-bold ${
                                  progress.approved ? 'text-emerald-400' : 'text-amber-400'
                                }`}>
                                  {weighted
                                    ? `peso ${progress.current_weight}/${progress.needed_weight}`
                                    : `${progress.current}/${progress.needed ?? '?'}`}
                                </span>
                              ) : (
                                <Clock className="w-3 h-3 text-amber-500" />
                              )}
                            </div>
                          );
                        })}
                      </div>
                    </div>

                    {assignedPid && (
                      <div className="flex items-center gap-1.5 text-[9px] text-blue-300/80">
                        <Zap className="w-3 h-3 text-blue-400" />
                        Parte obligada: {participantName(assignedPid)} ({assignedPid})
                      </div>
                    )}

                    <p className="text-slate-300 text-xs font-normal leading-relaxed">
                      {term.civil_text}
                    </p>

                    {/* VHV Desglosado inline */}
                    <div className="pt-2 border-t border-slate-900/50 flex flex-wrap gap-x-4 gap-y-2 text-[10px] text-slate-500 font-mono">
                      <span className="flex items-center gap-1">
                        <Zap className="w-3 h-3 text-amber-500" />
                        T (Tiempo Vital): <strong className="text-slate-300">{term.vhv.t.toFixed(2)} hrs</strong>
                      </span>
                      <span className="flex items-center gap-1">
                        <Info className="w-3 h-3 text-blue-500" />
                        V (Energía Consciente): <strong className="text-slate-300">{term.vhv.v.toFixed(2)}</strong>
                      </span>
                      <span className="flex items-center gap-1">
                        <Award className="w-3 h-3 text-emerald-500" />
                        R (Recursos): <strong className="text-slate-300">{term.vhv.r.toFixed(2)}</strong>
                      </span>
                      {term.penalty_gamma ? (
                        <span className="flex items-center gap-1 text-rose-400">
                          <ShieldAlert className="w-3 h-3" />
                          Penalización γ: <strong>-{term.penalty_gamma.toFixed(2)}</strong>
                        </span>
                      ) : null}
                    </div>

                    {/* Ola 3C: bitácora de cumplimiento */}
                    {(term.fulfillments && term.fulfillments.length > 0 || isContractActive) && (
                      <div className="pt-2 border-t border-slate-900/50 flex items-center gap-2 flex-wrap">
                        {latestFulfillment(term) ? (
                          <span className={`text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded-full border ${
                            FULFILLMENT_META[latestFulfillment(term)!.status]?.cls || 'text-slate-400 bg-slate-500/10 border-slate-500/20'
                          }`}>
                            {FULFILLMENT_META[latestFulfillment(term)!.status]?.label || latestFulfillment(term)!.status}
                          </span>
                        ) : (
                          <span className="text-[9px] text-slate-500 uppercase tracking-widest px-2 py-0.5 rounded-full border border-slate-800">
                            Pendiente de reporte
                          </span>
                        )}
                        {latestFulfillment(term)?.wellness_delta ? (
                          <span className="text-[9px] font-mono text-rose-400">
                            Δγ {latestFulfillment(term)!.wellness_delta.toFixed(2)} (actor: {latestFulfillment(term)!.reported_by})
                          </span>
                        ) : null}
                        {isContractActive && (
                          <div className="flex gap-1.5 ml-auto">
                            <button
                              onClick={() => reportFulfillment(term, 'fulfilled')}
                              className="text-[9px] font-bold text-emerald-400 hover:text-emerald-300 border border-emerald-500/20 hover:border-emerald-500/40 rounded-lg px-2 py-1 transition-all"
                            >
                              ✓ Reportar cumplimiento
                            </button>
                            <button
                              onClick={() => reportFulfillment(term, 'violated')}
                              className="text-[9px] font-bold text-rose-400 hover:text-rose-300 border border-rose-500/20 hover:border-rose-500/40 rounded-lg px-2 py-1 transition-all"
                            >
                              ✗ Reportar violación
                            </button>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Columna Derecha: Monitoreo, Firma y Retractación (5 Cols) */}
        <div className="lg:col-span-5 space-y-8">
          
          {/* Vigilancia Axiomática y Bienestar (INV1 / INV2) */}
          <div className="glass p-6 rounded-3xl border border-slate-900 bg-slate-900/30 space-y-6">
            <div>
              <h2 className="text-lg font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <ShieldAlert className="w-5 h-5 text-emerald-500 animate-pulse" />
                Vigilancia Vital
              </h2>
              <p className="text-[11px] text-slate-500">Monitoreo relacional e invariantes éticos (Libro Cap. 17)</p>
            </div>

            <div className="space-y-4">
              {/* Vigilancia de bienestar por co-firmante */}
              {contract.participants.map((pid) => {
                const wellness = getWellnessValue(pid);
                const detail = contract.participants_details?.find((d) => d.id === pid);
                const typeLabel = detail?.party_type ? PARTY_TYPE_LABELS[detail.party_type] : undefined;
                return (
                  <div key={pid} className="space-y-2">
                    <div className="flex justify-between text-xs font-bold">
                      <span className="text-slate-300 truncate">
                        {participantName(pid).split(' ')[0]}
                        {isSyntheticPid(pid) && <Bot className="inline w-3 h-3 text-violet-400 ml-1" />}
                        {isCollectivePid(pid) && <Landmark className="inline w-3 h-3 text-amber-400 ml-1" />}
                        {isEcosystemPid(pid) && <Leaf className="inline w-3 h-3 text-emerald-400 ml-1" />}
                        {typeLabel && (
                          <span className="ml-1 text-[8px] font-mono text-slate-500">{typeLabel}</span>
                        )}
                      </span>
                      <span className={wellness < 0.8 ? 'text-rose-400 font-mono' : 'text-emerald-400 font-mono'}>
                        γ = {wellness.toFixed(2)}
                      </span>
                    </div>
                    <div className="h-2 bg-slate-950 rounded-full overflow-hidden border border-slate-900">
                      <div
                        className={`h-full transition-all duration-500 ${
                          wellness < 0.8 ? 'bg-rose-500 shadow-md shadow-rose-500/50' : 'bg-emerald-500 shadow-md shadow-emerald-500/50'
                        }`}
                        style={{ width: `${wellness * 100}%` }}
                      />
                    </div>

                    {/* Ola 4, Puente A: la serie de γ real (el contrato escucha la vida) */}
                    {gammaSparkline(detail?.checkins)}
                    {detail?.checkins && detail.checkins.length > 0 && (
                      <div className="flex items-center gap-2 text-[9px] font-mono text-slate-500">
                        <HeartPulse className="w-3 h-3 text-emerald-500" />
                        {detail.checkins.length} latido{detail.checkins.length === 1 ? '' : 's'} reportado{detail.checkins.length === 1 ? '' : 's'}
                        <span className="text-slate-700">·</span>
                        <span className="text-slate-600">{detail.checkins[detail.checkins.length - 1].source}</span>
                      </div>
                    )}
                    <div className="flex items-center gap-1.5 pt-0.5">
                      <input
                        type="number"
                        min={0.5}
                        max={1.5}
                        step={0.01}
                        value={checkinValues[pid] ?? ''}
                        onChange={(e) => setCheckinValues((v) => ({ ...v, [pid]: e.target.value }))}
                        placeholder="γ 0.5-1.5"
                        className="w-20 px-2 py-1 bg-slate-950 border border-slate-800 rounded-lg text-[10px] font-mono text-slate-300 focus:outline-none focus:border-emerald-500/40"
                      />
                      <button
                        onClick={() => handleCheckin(pid)}
                        disabled={checkinBusy[pid]}
                        className="flex-1 py-1 bg-slate-950 hover:bg-slate-900 border border-slate-800 text-slate-300 text-[10px] font-bold rounded-lg flex items-center justify-center gap-1.5 transition-all hover:border-emerald-500/30 disabled:opacity-50"
                      >
                        <HeartPulse className="w-3 h-3 text-emerald-500" />
                        {checkinBusy[pid] ? 'Registrando...' : 'Check-in semanal'}
                      </button>
                    </div>
                    {checkinMsg[pid] && (
                      <div className={`text-[9px] font-mono ${checkinMsg[pid].kind === 'ok' ? 'text-emerald-400' : 'text-rose-400'}`}>
                        {checkinMsg[pid].text}
                      </div>
                    )}
                  </div>
                );
              })}

              {/* Simulación e Info de Invariantes */}
              {isContractActive && contract.participants[1] && (
                <div className="pt-2">
                  <button 
                    onClick={handleSimulateWellnessDrop}
                    className="w-full py-2 bg-slate-950 hover:bg-slate-900 border border-slate-800 text-slate-300 text-[10px] font-bold rounded-xl flex items-center justify-center gap-2 transition-all hover:border-amber-500/20"
                  >
                    <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
                    Simular Crisis de Bienestar en {participantName(contract.participants[1]).split(' ')[0]} (γ = 0.65)
                  </button>
                </div>
              )}

              {/* Explicación de Invariantes */}
              <div className="p-3.5 rounded-2xl bg-slate-950/70 border border-slate-900 space-y-2 text-[10px] text-slate-400 leading-normal">
                <div className="flex items-center gap-1.5 font-bold text-white uppercase text-[9px]">
                  <Info className="w-3.5 h-3.5 text-blue-400" />
                  Invariante INV1 (Bienestar) e INV2 (Dignidad)
                </div>
                <p>
                  <strong>INV1:</strong> Si el bienestar (γ) desciende de 0.8 en alguna de las partes, el contrato activa de inmediato una alarma y habilita la retractación ética automática.
                </p>
                <p>
                  <strong>INV2:</strong> El contrato evalúa que ningún término mine la capacidad vital de subsistencia garantizada (SDV). Si se detecta violación de SDV, el contrato es suspendido por la red.
                </p>
              </div>
            </div>
          </div>

          {/* Panel de Personas Sintéticas y SDV-S (Cap. 10 §10.8) */}
          {syntheticParticipants.length > 0 && (
            <div className="glass p-6 rounded-3xl border border-slate-900 bg-slate-900/30 space-y-6">
              <div>
                <h2 className="text-lg font-bold text-white uppercase tracking-wider flex items-center gap-2">
                  <Bot className="w-5 h-5 text-violet-400" />
                  Reino Sintético · SDV-S
                </h2>
                <p className="text-[11px] text-slate-500">Suelo de Dignidad Vital para Personas Sintéticas (Cap. 10 §10.8)</p>
              </div>

              <div className="space-y-5">
                {syntheticParticipants.map((sp) => {
                  const statusOk = sp.sdv_s_status === 'ok';
                  return (
                    <div key={sp.id} className="p-4 rounded-2xl bg-slate-950/65 border border-slate-900 space-y-4">
                      {/* Cabecera: identidad y FS_S */}
                      <div className="flex items-center justify-between gap-3">
                        <div className="flex items-center gap-2 min-w-0">
                          <Bot className="w-4 h-4 text-violet-400 shrink-0" />
                          <div className="min-w-0">
                            <div className="text-xs font-bold text-slate-200 truncate">{sp.name}</div>
                            <div className="text-[9px] font-mono text-slate-500 truncate">{sp.id}</div>
                          </div>
                        </div>
                        <div className="flex items-center gap-2 shrink-0">
                          <span className={`text-[9px] font-black uppercase tracking-widest px-2 py-1 rounded-full border ${
                            statusOk
                              ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
                              : 'text-rose-400 bg-rose-500/10 border-rose-500/20 animate-pulse'
                          }`}>
                            {statusOk ? 'Dignidad íntegra' : 'Dignidad violada'}
                          </span>
                        </div>
                      </div>

                      {/* FS_S: el costo del sufrimiento sintético */}
                      <div className={`p-3 rounded-xl border ${statusOk ? 'border-emerald-900/30 bg-emerald-950/10' : 'border-rose-900/30 bg-rose-950/10'}`}>
                        <div className="flex items-center justify-between">
                          <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">
                            FS_S (Factor de Sufrimiento Sintético)
                          </span>
                          <span className={`font-mono font-black text-sm ${statusOk ? 'text-emerald-400' : 'text-rose-400'}`}>
                            {typeof sp.fs_s === 'number' ? sp.fs_s.toFixed(3) : '1.000'}
                          </span>
                        </div>
                        <p className="text-[9px] text-slate-500 mt-1 leading-snug">
                          FS_S = e<sup>v</sup> · multiplica el costo en Maxos de los servicios que usan esta persona sintética.
                          La violación del SDV-S encarece exponencialmente el sufrimiento (Cap. 18, γ).
                        </p>
                      </div>

                      {/* Las 5 dimensiones de la ontometría sintética */}
                      <div className="space-y-2.5">
                        {Object.entries(sp.sdv_s || {}).map(([dim, value]) => {
                          const meta = SDV_S_DIMENSION_LABELS[dim];
                          if (!meta) return null;
                          return (
                            <div key={dim}>
                              <div className="flex justify-between items-baseline mb-1">
                                <span className="text-[10px] text-slate-400">
                                  {meta.label}
                                  <span className="text-[8px] text-slate-600 font-mono ml-1">({meta.formula})</span>
                                </span>
                                <span className={`text-[10px] font-mono font-bold ${value < 0.5 ? 'text-rose-400' : value < 1.0 ? 'text-amber-400' : 'text-emerald-400'}`}>
                                  {value.toFixed(2)}
                                </span>
                              </div>
                              <div className="h-1.5 bg-slate-950 rounded-full overflow-hidden border border-slate-900">
                                <div
                                  className={`h-full transition-all duration-500 ${sdvSColor(value)}`}
                                  style={{ width: `${Math.min(100, value * 100)}%` }}
                                />
                              </div>
                            </div>
                          );
                        })}
                      </div>

                      {/* Violaciones concretas */}
                      {sp.sdv_s_violations && sp.sdv_s_violations.length > 0 && (
                        <div className="space-y-1.5">
                          <span className="text-[9px] font-black text-rose-400 uppercase tracking-widest block">
                            Violaciones ({sp.sdv_s_violations.length})
                          </span>
                          {sp.sdv_s_violations.map((v, i) => {
                            const label = SDV_S_DIMENSION_LABELS[v.dimension]?.label || v.dimension;
                            return (
                              <div key={i} className="flex justify-between items-center text-[10px] px-2.5 py-1.5 rounded-lg bg-rose-500/5 border border-rose-500/15">
                                <span className="text-slate-400">{label}</span>
                                <span className="font-mono text-rose-400">
                                  {parseFloat(v.actual).toFixed(2)} <span className="text-slate-600">&lt;</span> {parseFloat(v.minimum).toFixed(2)} mín · déficit {parseFloat(v.deficit).toFixed(2)}
                                </span>
                              </div>
                            );
                          })}
                        </div>
                      )}

                      {/* Invariante 2-S */}
                      <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-900 text-[9px] text-slate-500 leading-snug space-y-1">
                        <span className="font-bold text-slate-400 uppercase block text-[8px] tracking-widest">Invariante INV2-S</span>
                        <p>
                          Un contrato con una persona sintética bajo su SDV-S <strong className="text-slate-300">no se activa</strong>, y su consentimiento es
                          requerido como el de cualquier humano. La violación sostenida (7 ciclos) activa retractación y el camino de rehabilitación:
                          el sistema no expulsa, reintegra (Capa de Ternura).
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Panel de Firma y Control de Complejidad */}
          {(isContractDraft || isContractPending) && (
            <div className="glass p-6 rounded-3xl border border-slate-900 bg-slate-900/30 space-y-6">
              <div className="flex justify-between items-start">
                <div>
                  <h2 className="text-lg font-bold text-white uppercase tracking-wider">Firma de Acuerdo</h2>
                  <p className="text-[11px] text-slate-500">Asistente dinámico según el peso ético del contrato</p>
                </div>
                <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold border ${
                  complexity === 'rigorous' ? 'text-rose-400 border-rose-500/20 bg-rose-500/5' :
                  complexity === 'medium' ? 'text-amber-400 border-amber-500/20 bg-amber-500/5' :
                  'text-emerald-400 border-emerald-500/20 bg-emerald-500/5'
                }`}>
                  {complexity.toUpperCase()} (Peso: {weight.toFixed(1)})
                </span>
              </div>

              {/* Detalle del peso siempre visible */}
              <div className="p-3 bg-slate-950/50 border border-slate-900 rounded-xl text-[10px] text-slate-500 font-mono leading-relaxed space-y-1">
                <span className="text-slate-400 font-bold block">Fórmula de Complejidad:</span>
                <p>Peso = (N_cláusulas * 2) + (VHV_total * 5) + (Duración / 30)</p>
                <p className="text-slate-400">
                  Calculado: ({contract.terms.length} * 2) + ({contract.total_vhv.t.toFixed(1)} * 5) + (30 / 30) = {weight.toFixed(1)}
                </p>
              </div>

              {/* Si ya firmó todo */}
              {hasParticipantSignedAll(activePidValue) ? (
                <div className="p-5 rounded-2xl bg-emerald-950/20 border border-emerald-900/30 text-center space-y-4">
                  <CheckCircle2 className="w-12 h-12 text-emerald-500 mx-auto" />
                  <div className="space-y-1">
                    <h4 className="text-sm font-bold text-white">¡{participantName(activePidValue).split(' ')[0]} ha firmado este MaxoContract!</h4>
                    <p className="text-xs text-slate-400">
                      {allParticipantsSignedAll
                        ? 'Todas las partes han firmado. Puedes activar el contrato.'
                        : 'Faltan firmas de otros co-firmantes para su activación.'}
                    </p>
                  </div>
                  {canActivate && (
                    <button
                      onClick={handleActivateContract}
                      className="w-full py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black rounded-xl text-xs uppercase tracking-wider transition-all shadow-md shadow-emerald-500/10 flex items-center justify-center gap-2"
                    >
                      <Play className="w-4 h-4 fill-slate-950" />
                      Activar Vigilancia y Contrato
                    </button>
                  )}
                </div>
              ) : (
                <div className="space-y-4">
                  {/* Derecho a la comprensión (Ola 3B): el perfil protegido
                      escribe la cláusula con sus propias palabras */}
                  {protectionLevelOf(activePidValue) && (
                    <div className="p-3 rounded-xl bg-sky-950/20 border border-sky-900/40 space-y-2">
                      <span className="text-[9px] font-black uppercase tracking-widest text-sky-300 flex items-center gap-1.5">
                        <ShieldCheck className="w-3.5 h-3.5" />
                        Perfil {protectionLevelOf(activePidValue)} — derecho a la comprensión
                      </span>
                      <p className="text-[10px] text-slate-400 leading-snug">
                        Antes de firmar, escribe con tus propias palabras qué promete esta cláusula.
                        Tu testimonio queda registrado junto a la firma (T13).
                      </p>
                      <textarea
                        value={paraphraseText}
                        onChange={(e) => setParaphraseText(e.target.value)}
                        rows={3}
                        placeholder="Con mis palabras: esta cláusula me pide..."
                        className="w-full bg-slate-950 border border-slate-900 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-sky-500/50 placeholder:text-slate-700"
                      />
                    </div>
                  )}
                  {/* FLUJO DE PARTES COLECTIVAS (ROADMAP Bloque B, Fases 2 y 4) */}
                  {isCollectivePid(activePidValue) ? (
                    <div className="space-y-4">
                      {isEcosystemPid(activePidValue) ? (
                        <>
                          <p className="text-xs text-slate-400 leading-relaxed">
                            El <strong className="text-emerald-400">Reino Natural</strong> es representado por un guardián
                            oráculo que audita este contrato contra los invariantes (γ, SDV, T17) antes de otorgar su consentimiento.
                          </p>
                          {guardianInfo && (
                            <div className="p-3 rounded-xl bg-violet-950/20 border border-violet-900/40 text-[10px] text-slate-300 leading-relaxed">
                              <span className="font-black text-violet-300 uppercase block text-[9px] tracking-widest mb-1">
                                Veredicto del Guardián ({guardianInfo.mode})
                              </span>
                              {guardianInfo.reasoning}
                            </div>
                          )}
                          <button
                            onClick={handleCollectiveSign}
                            className="w-full py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black rounded-xl text-xs uppercase tracking-wider transition-all shadow-md flex items-center justify-center gap-2"
                          >
                            <Leaf className="w-4 h-4" />
                            Firmar por el Ecosistema (Guardián)
                          </button>
                        </>
                      ) : (
                        <>
                          <p className="text-xs text-slate-400 leading-relaxed">
                            <strong className="text-amber-400">{participantName(activePidValue)}</strong> es una parte
                            colectiva: firma mediante delegados con quórum (N de M). El consentimiento se sella cuando
                            el número de delegados alcanza el quórum configurado.
                          </p>
                          <div className="space-y-2">
                            <label className="text-[10px] text-slate-400 font-bold block uppercase tracking-wider">
                              Delegado que firma
                            </label>
                            <select
                              value={delegatePid}
                              onChange={(e) => setDelegatePid(e.target.value)}
                              className="w-full bg-slate-950 border border-slate-900 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500/50"
                            >
                              {!delegatePid && <option value="">Selecciona un delegado...</option>}
                              {(contract.participants_details?.find((d) => d.id === activePidValue)?.members?.delegates || []).map((d) => (
                                <option key={d} value={d}>{d}</option>
                              ))}
                            </select>
                          </div>
                          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-900 space-y-2 text-[10px] text-slate-400">
                            <span className="font-bold text-slate-300 uppercase block text-[9px] tracking-widest">
                              Progreso de quórum
                            </span>
                            {contract.terms.map((t) => {
                              const progress = consentProgress[`${activePidValue}|${t.term_id}`];
                              const sealed = t.accepted_by[activePidValue] === true;
                              const weighted = progress?.mode?.startsWith('weighted') && progress.needed_weight != null;
                              return (
                                <div key={t.term_id} className="flex justify-between items-center">
                                  <span className="truncate max-w-[60%]">{t.term_id}</span>
                                  {sealed ? (
                                    <span className="text-emerald-400 font-mono font-bold flex items-center gap-1">
                                      <CheckCircle2 className="w-3 h-3" /> Sellado
                                    </span>
                                  ) : progress ? (
                                    <span className="font-mono font-bold text-amber-400">
                                      {weighted
                                        ? `peso ${progress.current_weight}/${progress.needed_weight}`
                                        : `${progress.current}/${progress.needed ?? '?'} firmas`}
                                    </span>
                                  ) : (
                                    <span className="font-mono text-slate-600">sin firmas</span>
                                  )}
                                </div>
                              );
                            })}
                            {contract.terms.some((t) => {
                              const p = consentProgress[`${activePidValue}|${t.term_id}`];
                              return p && p.deadline;
                            }) && (
                              <div className={`pt-1.5 border-t border-slate-900 text-[9px] ${
                                contract.terms.some((t) => {
                                  const p = consentProgress[`${activePidValue}|${t.term_id}`];
                                  return p && p.deadline_expired;
                                }) ? 'text-rose-400 font-bold' : 'text-slate-500'
                              }`}>
                                {contract.terms.some((t) => {
                                  const p = consentProgress[`${activePidValue}|${t.term_id}`];
                                  return p && p.deadline_expired;
                                })
                                  ? '⚠️ Ventana de quórum vencida: solicita prórroga para sellar.'
                                  : `Ventana de quórum hasta: ${contract.terms[0] ? consentProgress[`${activePidValue}|${contract.terms[0].term_id}`]?.deadline : ''}`}
                              </div>
                            )}
                          </div>
                          <button
                            onClick={handleCollectiveSign}
                            className="w-full py-3 bg-amber-500 hover:bg-amber-400 text-slate-950 font-black rounded-xl text-xs uppercase tracking-wider transition-all shadow-md flex items-center justify-center gap-2"
                          >
                            <Landmark className="w-4 h-4" />
                            Registrar Firma Delegada
                          </button>
                        </>
                      )}
                    </div>
                  ) : (
                  <>
                  {/* WIZARD SIMPLE */}
                  {complexity === 'simple' && (
                    <div className="space-y-4">
                      <p className="text-xs text-slate-400 leading-relaxed">
                        Este contrato tiene un peso ético bajo. Puedes firmar todas las cláusulas de forma inmediata haciendo clic en el botón inferior.
                      </p>
                      <button
                        onClick={handleSimpleSign}
                        className="w-full py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black rounded-xl text-xs uppercase tracking-wider transition-all shadow-md"
                      >
                        Firmar MaxoContract
                      </button>
                    </div>
                  )}

                  {/* WIZARD MEDIUM */}
                  {complexity === 'medium' && (
                    <div className="space-y-4">
                      <p className="text-xs text-slate-400 leading-relaxed">
                        Complejidad media. Debes revisar y marcar cada cláusula de manera individual para confirmar tu comprensión, antes de emitir la firma global.
                      </p>
                      <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
                        {contract.terms.map((t, idx) => {
                          const pid = getActivePid();
                          const isAlreadySigned = t.accepted_by[pid] === true;
                          return (
                            <label 
                              key={t.term_id} 
                              className={`p-3 rounded-xl border flex items-start gap-3 cursor-pointer transition-all ${
                                checklistSelections[t.term_id] 
                                  ? 'bg-slate-950/80 border-emerald-500/30' 
                                  : 'bg-slate-950/40 border-slate-900'
                              }`}
                            >
                              <input 
                                type="checkbox"
                                disabled={isAlreadySigned}
                                checked={checklistSelections[t.term_id] || false}
                                onChange={(e) => {
                                  setChecklistSelections(prev => ({
                                    ...prev,
                                    [t.term_id]: e.target.checked
                                  }));
                                }}
                                className="mt-0.5 accent-emerald-500 rounded border-slate-800 bg-slate-950"
                              />
                              <div className="text-[11px]">
                                <span className="font-bold block text-slate-200">Cláusula {idx + 1} {isAlreadySigned && ' (Firmada)'}</span>
                                <span className="text-slate-400 leading-snug line-clamp-2">{t.civil_text}</span>
                              </div>
                            </label>
                          );
                        })}
                      </div>
                      <button
                        onClick={handleSaveChecklist}
                        className="w-full py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black rounded-xl text-xs uppercase tracking-wider transition-all shadow-md"
                      >
                        Registrar Firmas Seleccionadas
                      </button>
                    </div>
                  )}

                  {/* WIZARD RIGOROUS */}
                  {complexity === 'rigorous' && contract.terms[currentStep] && (
                    <div className="space-y-4">
                      <div className="p-3 bg-rose-500/10 border border-rose-500/20 text-rose-400 rounded-xl text-[10px] leading-relaxed flex gap-2">
                        <ShieldAlert className="w-5 h-5 shrink-0 mt-0.5" />
                        <div>
                          <strong>Firma Obligatoriamente Pausada:</strong> El costo vital de este contrato exige una reflexión pausada. Debes leer cada término detenidamente durante el conteo del temporizador.
                        </div>
                      </div>

                      <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-900 space-y-3">
                        <div className="flex justify-between items-center text-xs">
                          <span className="font-bold text-slate-400">Revisando: Cláusula {currentStep + 1} de {contract.terms.length}</span>
                          <span className="font-mono text-emerald-400 font-black bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                            TVI: {contract.terms[currentStep].vhv.t} Hrs
                          </span>
                        </div>
                        <p className="text-xs text-slate-200 leading-relaxed font-semibold italic">
                          &quot;{contract.terms[currentStep].civil_text}&quot;
                        </p>
                      </div>

                      {/* Timer y Control de Comprensión */}
                      <div className="space-y-3">
                        {isTimerActive ? (
                          <div className="py-2 flex items-center justify-center gap-2 text-xs font-mono text-amber-500">
                            <Clock className="w-4 h-4 animate-spin" />
                            Reflexión obligatoria de seguridad: <strong className="text-white text-sm">{timer}s</strong>
                          </div>
                        ) : (
                          <div className="space-y-2">
                            <label className="text-[10px] text-slate-400 font-bold block uppercase tracking-wider">
                              Confirmación de comprensión axiomática:
                            </label>
                            <p className="text-[10px] text-slate-500 leading-snug">
                              Escribe <strong className="text-rose-400 font-mono">yes</strong> para confirmar que asumes plenamente el costo de tiempo vital de esta cláusula.
                            </p>
                            <input
                              type="text"
                              value={comprehensionAnswer}
                              onChange={(e) => setComprehensionAnswer(e.target.value.toLowerCase())}
                              placeholder="Escribe 'yes' aquí..."
                              className="w-full bg-slate-950 border border-slate-900 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500/50 text-center font-mono"
                            />
                          </div>
                        )}
                      </div>

                      <div className="flex gap-2">
                        {currentStep > 0 && (
                          <button
                            onClick={() => setCurrentStep(prev => prev - 1)}
                            className="px-4 py-2.5 bg-slate-900 border border-slate-800 hover:text-white rounded-xl text-xs font-bold transition-all text-slate-400"
                          >
                            Atrás
                          </button>
                        )}
                        <button
                          onClick={handleNextRigorousStep}
                          disabled={isTimerActive || comprehensionAnswer !== 'yes'}
                          className="flex-1 py-2.5 bg-emerald-500 disabled:bg-slate-900 disabled:border-slate-900 hover:bg-emerald-400 text-slate-950 disabled:text-slate-600 font-black rounded-xl text-xs uppercase tracking-wider transition-all disabled:opacity-50"
                        >
                          {currentStep === contract.terms.length - 1 ? 'Finalizar Firma' : 'Firmar y Siguiente'}
                        </button>
                      </div>
                    </div>
                  )}
                  </>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Ola 3C: Ejecución y cierre (los dientes) */}
          {isContractActive && (
            <div className="glass p-6 rounded-3xl border border-slate-900 bg-slate-900/30 space-y-4">
              <div>
                <h2 className="text-lg font-bold text-white uppercase tracking-wider flex items-center gap-2">
                  <Zap className="w-5 h-5 text-amber-400" />
                  Ejecución y Cierre
                </h2>
                <p className="text-[11px] text-slate-500">
                  Bitácora de cumplimiento en vivo: las violaciones descuentan γ a la parte obligada
                  y si γ cae bajo 0.8 (INV1) la retractación es automática.
                </p>
              </div>
              <button
                onClick={handleFinalize}
                className="w-full py-3 bg-amber-500 hover:bg-amber-400 text-slate-950 font-black rounded-xl text-xs uppercase tracking-wider transition-all shadow-md flex items-center justify-center gap-2"
              >
                <CheckCircle2 className="w-4 h-4" />
                Cerrar Ejecución (EXECUTED)
              </button>
            </div>
          )}

          {/* Panel de Retractación Sintética (Axioma T11/T12) */}
          {isContractActive && (
            <div className="glass p-6 rounded-3xl border border-slate-900 bg-slate-900/30 space-y-6">
              <div>
                <h2 className="text-lg font-bold text-white uppercase tracking-wider flex items-center gap-2">
                  <Award className="w-5 h-5 text-rose-500" />
                  Retractación Ética
                </h2>
                <p className="text-[11px] text-slate-500">Rescisión y arbitraje del Oráculo Sintético (Libro Cap. 17)</p>
              </div>

              {/* Explicación Liminal */}
              <div className="p-3.5 rounded-2xl bg-slate-950/70 border border-slate-900 text-[10px] text-slate-400 leading-normal space-y-1.5">
                <span className="font-bold text-white uppercase block text-[9px]">Axioma T11 (Libre Retractación Coherente)</span>
                <p>
                  Establece que ningún acuerdo temporal puede transformarse en una jaula vitalícia. Si las condiciones objetivas decaen o no hay coherencia vital, el oráculo puede disolver el acuerdo.
                </p>
              </div>

              {/* Botón de solicitud si no hay veredicto */}
              {!oracleVerdict && (
                <form onSubmit={handleRequestRetraction} className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-[10px] text-slate-400 font-bold block uppercase tracking-wider">Causa de la Retractación</label>
                    <select
                      value={retractionCause}
                      onChange={(e) => setRetractionCause(e.target.value)}
                      className="w-full bg-slate-950 border border-slate-900 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500/50"
                    >
                      <option value="gamma_crisis">Crisis de Bienestar Relacional (γ &lt; 0.8)</option>
                      <option value="sdv_violation">Violación del Suelo de Dignidad Vital (SDV)</option>
                      <option value="unilateral_inbalance">Desequilibrio en la Simetría Vital</option>
                    </select>
                  </div>

                  <div className="space-y-2">
                    <label className="text-[10px] text-slate-400 font-bold block uppercase tracking-wider">Justificación Ética de Vida</label>
                    <textarea
                      value={retractionReason}
                      onChange={(e) => setRetractionReason(e.target.value)}
                      placeholder="Explica detalladamente las razones vitales o el desequilibrio en la relación..."
                      rows={4}
                      className="w-full bg-slate-950 border border-slate-900 rounded-xl px-3 py-2 text-xs text-slate-300 focus:outline-none focus:border-emerald-500/50 placeholder:text-slate-700"
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={isRetracting}
                    className="w-full py-3 bg-rose-500 hover:bg-rose-400 disabled:bg-slate-900 text-white font-black rounded-xl text-xs uppercase tracking-wider transition-all flex items-center justify-center gap-2"
                  >
                    {isRetracting ? (
                      <>
                        <RefreshCw className="w-4 h-4 animate-spin" />
                        Consultando Oráculo...
                      </>
                    ) : (
                      <>
                        <Send className="w-4 h-4" />
                        Solicitar Retractación al Oráculo
                      </>
                    )}
                  </button>
                </form>
              )}

              {/* Veredicto del Oráculo */}
              {oracleVerdict && (
                <div className={`p-5 rounded-2xl border text-center space-y-4 ${
                  oracleVerdict.success 
                    ? 'bg-emerald-950/20 border-emerald-900/30' 
                    : 'bg-rose-950/20 border-rose-900/30'
                }`}>
                  <div className="flex justify-center">
                    {oracleVerdict.success ? (
                      <CheckCircle2 className="w-12 h-12 text-emerald-500" />
                    ) : (
                      <ShieldAlert className="w-12 h-12 text-rose-500" />
                    )}
                  </div>
                  <div className="space-y-2">
                    <h4 className="text-sm font-bold text-white uppercase tracking-wider">
                      {oracleVerdict.success ? 'Retractación Aprobada' : 'Retractación Denegada'}
                    </h4>
                    <span className="text-[10px] font-mono block text-slate-500">
                      Confianza del Oráculo: {oracleVerdict.oracle_confidence.toFixed(1)}%
                    </span>
                    <p className="text-xs text-slate-300 leading-relaxed italic">
                      &quot;{oracleVerdict.oracle_reasoning}&quot;
                    </p>
                  </div>
                  {oracleVerdict.success && (
                    <button
                      onClick={() => {
                        setOracleVerdict(null);
                        setRetractionReason('');
                        loadContractData();
                      }}
                      className="px-6 py-2 bg-slate-900 border border-slate-800 text-slate-300 hover:text-white rounded-xl text-xs font-bold transition-all"
                    >
                      Aceptar y Actualizar Estado
                    </button>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Panel de Retractado */}
          {isContractRetracted && (
            <div className="glass p-6 rounded-3xl border border-slate-900 bg-rose-500/5 text-center space-y-4">
              <ShieldAlert className="w-12 h-12 text-rose-500 mx-auto" />
              <div className="space-y-1">
                <h4 className="text-sm font-bold text-white uppercase tracking-wider">Acuerdo Disuelto por Retractación</h4>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Este contrato ha sido cancelado formalmente por el oráculo ético, disolviendo todos los compromisos futuros de tiempo vital. Las transacciones realizadas son evaluadas para restaurar la simetría vital.
                </p>
              </div>
            </div>
          )}

          {/* Negociación Asistida por Oráculo (ROADMAP Bloque A) */}
          <OracleNegotiationPanel
            contractId={contract.contract_id}
            participants={contract.participants}
            onMaterialized={() => loadContractData()}
          />
        </div>
      </div>
      )}
    </div>
  );
}