'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { apiFetch } from '../../lib/api';
import { useAuth } from '../../context/AuthContext';
import { 
  FileText, ArrowLeft, ShieldAlert, Award, Info, CheckCircle2, 
  HelpCircle, UserCheck, AlertTriangle, Play, RefreshCw, Send, Zap,
  Clock, Users, Check
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface Term {
  term_id: string;
  civil_text: string;
  vhv: { t: number; v: number; r: number };
  accepted_by: Record<string, boolean>;
}

interface ParticipantDetail {
  id: string;
  name: string;
  wellness: number;
}

interface ContractDetails {
  contract_id: string;
  state: string;
  civil_description: string;
  participants: string[];
  participants_details?: ParticipantDetail[];
  terms: Term[];
  terms_count: number;
  total_vhv: { t: number; v: number; r: number };
  events_count: number;
  hash: string;
}

export default function ContractDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const { user: currentUser } = useAuth();
  const contractId = params.id as string;

  // Estados principales
  const [contract, setContract] = useState<ContractDetails | null>(null);
  const [civilSummary, setCivilSummary] = useState<string>('');
  const [activeRole, setActiveRole] = useState<'creator' | 'counterparty'>('creator'); // Rol simulado para firmar
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

      // Cargar traducción a lenguaje civil
      const civilRes = await apiFetch(`/contracts/${contractId}/civil`);
      if (civilRes.ok) {
        const civilData = await civilRes.json();
        setCivilSummary(civilData.civil_summary);
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

  // Obtener ID real del participante según el rol simulado
  const getSimulatedUserId = useCallback(() => {
    if (!contract) return null;
    
    // El creador es típicamente el primer participante
    const creatorIdStr = contract.participants[0] || `user-${currentUser?.id || 1}`;
    // La contraparte es típicamente el segundo participante
    const counterpartyIdStr = contract.participants[1] || 'user-2';

    const cleanId = (pId: string) => {
      const numStr = pId.replace('user-', '');
      const parsed = parseInt(numStr);
      return isNaN(parsed) ? 2 : parsed;
    };

    if (activeRole === 'creator') {
      return cleanId(creatorIdStr);
    } else {
      return cleanId(counterpartyIdStr);
    }
  }, [contract, currentUser, activeRole]);

  // Determinar si el participante simulado ya firmó todo
  const hasParticipantSignedAll = useCallback(() => {
    if (!contract) return false;
    const simPid = `user-${getSimulatedUserId()}`;
    return contract.terms.every(t => t.accepted_by[simPid] === true);
  }, [contract, getSimulatedUserId]);

  // Manejo del contador para firma Rigurosa
  useEffect(() => {
    let interval: any = null;
    if (isTimerActive && timer > 0) {
      interval = setInterval(() => {
        setTimer((prev) => prev - 1);
      }, 1000);
    } else if (timer === 0) {
      setIsTimerActive(false);
    }
    return () => clearInterval(interval);
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
      const initialChecklist: Record<string, boolean> = {};
      contract.terms.forEach(t => {
        const simPid = `user-${getSimulatedUserId()}`;
        initialChecklist[t.term_id] = t.accepted_by[simPid] === true;
      });
      setChecklistSelections(initialChecklist);

      // Si es rigurosa, iniciar el primer paso si no ha firmado todo
      const signedAll = contract.terms.every(t => t.accepted_by[`user-${getSimulatedUserId()}`] === true);
      if (!signedAll) {
        startRigorousStep(0);
      }
    }
  }, [contract, activeRole, getSimulatedUserId, startRigorousStep]);

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

  // Acción: Aceptar un término vía API
  const handleAcceptTerm = async (termId: string) => {
    const userId = getSimulatedUserId();
    if (!userId) return;

    try {
      const res = await apiFetch(`/contracts/${contractId}/accept`, {
        method: 'POST',
        body: JSON.stringify({
          term_id: termId,
          user_id: userId
        })
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
    const pendingTerms = contract?.terms.filter(t => checklistSelections[t.term_id] && !t.accepted_by[`user-${getSimulatedUserId()}`]) || [];
    
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

    const userId = getSimulatedUserId();

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

  // Verificar si ambas partes han firmado todos los términos
  const creatorSignedAll = contract.terms.every(t => t.accepted_by[contract.participants[0]] === true);
  const counterpartySignedAll = contract.terms.every(t => t.accepted_by[contract.participants[1]] === true);
  const canActivate = (isContractDraft || isContractPending) && creatorSignedAll && counterpartySignedAll;

  // Encontrar bienestar actual de cada participante
  const getWellnessValue = (pId: string) => {
    const detail = contract.participants_details?.find(d => d.id === pId);
    return detail ? detail.wellness : 1.0;
  };

  const creatorWellness = getWellnessValue(contract.participants[0]);
  const counterpartyWellness = getWellnessValue(contract.participants[1]);
  const hasSuffering = creatorWellness < 1.0 || counterpartyWellness < 1.0;

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
          </div>
        </div>

        {/* Simulador de Rol (Role Switcher) */}
        <div className="bg-slate-900/80 border border-slate-800 p-3 rounded-2xl flex flex-col gap-2">
          <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-1">
            <UserCheck className="w-3.5 h-3.5 text-emerald-500" />
            Simulador de Identidad Activa (Firmante actual)
          </span>
          <p className="text-[9px] text-slate-400 max-w-[320px] leading-snug">
            <strong>Simulación local:</strong> Alterna tu identidad de firmante para probar cómo cada parte visualiza, revisa y firma modularmente este acuerdo.
          </p>
          <div className="flex gap-2 bg-slate-950 p-1 rounded-xl border border-slate-850">
            <button
              onClick={() => setActiveRole('creator')}
              className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeRole === 'creator' 
                  ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/10' 
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Creador ({contract.participants[0] || 'Tú'})
            </button>
            <button
              onClick={() => setActiveRole('counterparty')}
              className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeRole === 'counterparty' 
                  ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/10' 
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Contraparte ({contract.participants[1] || 'Bob'})
            </button>
          </div>
        </div>
      </div>

      {/* Grid Principal */}
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
                "{civilSummary || contract.civil_description || 'Generando resumen en lenguaje comprensible...'}"
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
                const creatorSigned = term.accepted_by[contract.participants[0]] === true;
                const counterpartySigned = term.accepted_by[contract.participants[1]] === true;

                return (
                  <div key={term.term_id} className="p-4 rounded-2xl bg-slate-950/65 border border-slate-900 space-y-3">
                    <div className="flex justify-between items-start">
                      <span className="text-xs font-mono text-emerald-500 font-bold">#{index + 1} Cláusula: {term.term_id}</span>
                      <div className="flex gap-2">
                        {/* Indicadores de Firma */}
                        <div className="flex items-center gap-1.5 text-[9px] px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800">
                          <span className="text-slate-500">Creador:</span>
                          {creatorSigned ? (
                            <CheckCircle2 className="w-3 h-3 text-emerald-500" />
                          ) : (
                            <Clock className="w-3 h-3 text-amber-500" />
                          )}
                        </div>
                        <div className="flex items-center gap-1.5 text-[9px] px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800">
                          <span className="text-slate-500">Contraparte:</span>
                          {counterpartySigned ? (
                            <CheckCircle2 className="w-3 h-3 text-emerald-500" />
                          ) : (
                            <Clock className="w-3 h-3 text-amber-500" />
                          )}
                        </div>
                      </div>
                    </div>

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
                    </div>
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
              {/* Creator Status */}
              <div className="space-y-2">
                <div className="flex justify-between text-xs font-bold">
                  <span className="text-slate-300">Creador ({contract.participants[0] || 'Tú'})</span>
                  <span className={creatorWellness < 0.8 ? 'text-rose-400 font-mono' : 'text-emerald-400 font-mono'}>
                    γ = {creatorWellness.toFixed(2)}
                  </span>
                </div>
                <div className="h-2 bg-slate-950 rounded-full overflow-hidden border border-slate-900">
                  <div 
                    className={`h-full transition-all duration-500 ${
                      creatorWellness < 0.8 ? 'bg-rose-500 shadow-md shadow-rose-500/50' : 'bg-emerald-500 shadow-md shadow-emerald-500/50'
                    }`}
                    style={{ width: `${creatorWellness * 100}%` }}
                  />
                </div>
              </div>

              {/* Counterparty Status */}
              <div className="space-y-2">
                <div className="flex justify-between text-xs font-bold">
                  <span className="text-slate-300">Contraparte ({contract.participants[1] || 'Bob'})</span>
                  <span className={counterpartyWellness < 0.8 ? 'text-rose-400 font-mono' : 'text-emerald-400 font-mono'}>
                    γ = {counterpartyWellness.toFixed(2)}
                  </span>
                </div>
                <div className="h-2 bg-slate-950 rounded-full overflow-hidden border border-slate-900">
                  <div 
                    className={`h-full transition-all duration-500 ${
                      counterpartyWellness < 0.8 ? 'bg-rose-500 shadow-md shadow-rose-500/50' : 'bg-emerald-500 shadow-md shadow-emerald-500/50'
                    }`}
                    style={{ width: `${counterpartyWellness * 100}%` }}
                  />
                </div>
              </div>

              {/* Simulación e Info de Invariantes */}
              {isContractActive && (
                <div className="pt-2">
                  <button 
                    onClick={handleSimulateWellnessDrop}
                    className="w-full py-2 bg-slate-950 hover:bg-slate-900 border border-slate-800 text-slate-300 text-[10px] font-bold rounded-xl flex items-center justify-center gap-2 transition-all hover:border-amber-500/20"
                  >
                    <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
                    Simular Crisis de Bienestar en Bob (γ = 0.65)
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
              {hasParticipantSignedAll() ? (
                <div className="p-5 rounded-2xl bg-emerald-950/20 border border-emerald-900/30 text-center space-y-4">
                  <CheckCircle2 className="w-12 h-12 text-emerald-500 mx-auto" />
                  <div className="space-y-1">
                    <h4 className="text-sm font-bold text-white">¡Has firmado este MaxoContract!</h4>
                    <p className="text-xs text-slate-400">Esperando firmas de la contraparte si hay pendientes para su activación.</p>
                  </div>
                  {canActivate && activeRole === 'creator' && (
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
                          const isAlreadySigned = t.accepted_by[`user-${getSimulatedUserId()}`] === true;
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
                          "{contract.terms[currentStep].civil_text}"
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
                </div>
              )}
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
                      "{oracleVerdict.oracle_reasoning}"
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
        </div>
      </div>
    </div>
  );
}