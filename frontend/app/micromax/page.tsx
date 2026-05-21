"use client";

import React, { useState, useEffect } from "react";
import { api } from "../lib/api";
import { motion, AnimatePresence } from "framer-motion";
import {
  Heart,
  Shield,
  Activity,
  UserCheck,
  TrendingUp,
  AlertTriangle,
  ClipboardList,
  Sparkles,
  PlusCircle,
  HelpCircle,
  LogOut,
  Calendar,
  Users,
  Eye,
  Settings,
  Info
} from "lucide-react";
import { Button } from "../components/ui/Button";

// Presets representing Chapter 16 metrics
const CDD_PRESETS = [
  { name: "Cocina Compleja", effort: 1.8, mental: 1.4, scope: 1.3 },
  { name: "Cocina Simple", effort: 1.3, mental: 1.2, scope: 1.3 },
  { name: "Platos & Limpieza Cocina", effort: 1.5, mental: 1.1, scope: 1.2 },
  { name: "Limpieza General Semanal", effort: 1.6, mental: 1.1, scope: 1.2 },
  { name: "Limpieza Profunda Mensual", effort: 1.9, mental: 1.2, scope: 1.2 },
  { name: "Limpieza de Baños", effort: 1.7, mental: 1.1, scope: 1.3 },
  { name: "Cuidado Bebé (Supervisión Activa)", effort: 1.7, mental: 1.5, scope: 1.5 },
  { name: "Cuidado Niño Pequeño", effort: 1.6, mental: 1.4, scope: 1.4 },
  { name: "Cuidado Persona Dependiente", effort: 1.8, mental: 1.5, scope: 1.5 },
  { name: "Finanzas & Presupuesto Hogar", effort: 1.3, mental: 1.4, scope: 1.2 },
  { name: "Compras del Hogar", effort: 1.4, mental: 1.2, scope: 1.2 }
];

// Mock Dashboard data for ESI Safe Camouflage Mode
const MOCK_DASHBOARD = {
  three_accounts: {
    members: [
      { id: 99991, name: "Tú", cdd: 145.2, cdd_share: 50.4, income: 1200000, ceh_share: 48.0, ted: 42.5, ted_share: 51.2, equilibrio: 99.8 },
      { id: 99992, name: "Pareja/Familiar", cdd: 142.8, cdd_share: 49.6, income: 1300000, ceh_share: 52.0, ted: 40.5, ted_share: 48.8, equilibrio: 100.2 }
    ],
    totals: {
      total_cdd: 288.0,
      total_income: 2500000,
      total_ted: 83.0
    }
  },
  toxicity: {
    ice: 0.8,
    idb: 1.2,
    idp: 0.15,
    detox_triggered: false,
    reasons: [],
    alerts: {
      ice: false,
      idb: false,
      idp: false
    }
  }
};

const MOCK_LOGS = [
  { id: 101, task_name: "Cocina Simple", duration_hours: 1.2, calculated_vhv: 2.8, logged_date: new Date().toISOString().split("T")[0] },
  { id: 102, task_name: "Limpieza de Baños", duration_hours: 0.8, calculated_vhv: 3.1, logged_date: new Date(Date.now() - 86400000).toISOString().split("T")[0] },
  { id: 103, task_name: "Compras del Hogar", duration_hours: 1.5, calculated_vhv: 2.5, logged_date: new Date(Date.now() - 172800000).toISOString().split("T")[0] }
];

export default function MicroMaxPage() {
  // App States
  const [household, setHousehold] = useState<any>(null);
  const [members, setMembers] = useState<any[]>([]);
  const [member, setMember] = useState<any>(null);
  const [survey, setSurvey] = useState<any>(null);
  const [dashboard, setDashboard] = useState<any>(null);
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState("dashboard");
  const [isCamouflaged, setIsCamouflaged] = useState(false);
  const [showSecuritySupport, setShowSecuritySupport] = useState(false);
  const [showESIGuide, setShowESIGuide] = useState(false);

  // Auth check
  const [authError, setAuthError] = useState(false);

  // ESI Checklist state
  const [surveyAnswers, setSurveyAnswers] = useState({
    q1: false,
    q2: false,
    q3: false,
    q4: false,
    q5: false,
    q6: false
  });

  // Household Join/Create form states
  const [householdName, setHouseholdName] = useState("");
  const [inviteCode, setInviteCode] = useState("");

  // Member config forms
  const [income, setIncome] = useState(0);
  const [workHours, setWorkHours] = useState(0);
  const [travelHours, setTravelHours] = useState(0);
  const [sleepHours, setSleepHours] = useState(56);

  // CDD Form states
  const [taskName, setTaskName] = useState("");
  const [duration, setDuration] = useState(1.0);
  const [effort, setEffort] = useState(1.0);
  const [mental, setMental] = useState(1.0);
  const [scope, setScope] = useState(1.0);
  const [attention, setAttention] = useState(1.0);
  const [fragmentation, setFragmentation] = useState(1.0);
  const [loneliness, setLoneliness] = useState(1.0);
  const [presetIndex, setPresetIndex] = useState("-1");

  // Audit Form states
  const [auditDate, setAuditDate] = useState(new Date().toISOString().split("T")[0]);
  const [conflicts, setConflicts] = useState(0);
  const [weapons, setWeapons] = useState(0);
  const [accusations, setAccusations] = useState(0);
  const [threats, setThreats] = useState(0);
  const [s1, setS1] = useState(0);
  const [s2, setS2] = useState(0);
  const [s3, setS3] = useState(0);
  const [s4, setS4] = useState(0);
  const [s5, setS5] = useState(0);
  const [auditWeeks, setAuditWeeks] = useState(4);

  // Load basic data
  const loadInitialData = async () => {
    setLoading(true);
    setError(null);
    try {
      // Get household info
      const hData = await api.getMicroMaxHousehold();
      setHousehold(hData.household);
      setMembers(hData.members || []);

      if (hData.household) {
        // Fetch survey and dashboard metrics
        const surveyData = await api.getMicroMaxSafetySurvey();
        setSurvey(surveyData);

        // Fetch dashboard metrics and CDD logs depending on safety status
        let dashData;
        if (surveyData && surveyData.score !== undefined && surveyData.score >= 3) {
          setIsCamouflaged(true);
          dashData = MOCK_DASHBOARD;
          setLogs(MOCK_LOGS);
        } else {
          setIsCamouflaged(false);
          dashData = await api.getMicroMaxDashboard();
          const logData = await api.getMicroMaxCDDLogs();
          setLogs(logData || []);
        }
        setDashboard(dashData);

        // Fetch user config details
        const token = localStorage.getItem("mc_access_token");
        if (token) {
          const payload = JSON.parse(atob(token.split(".")[1]));
          const currentMember = hData.members.find((m: any) => m.user_id === payload.user_id);
          if (currentMember) {
            setMember(currentMember);
            setIncome(currentMember.monthly_income);
            setWorkHours(currentMember.work_hours);
            setTravelHours(currentMember.travel_hours);
            setSleepHours(currentMember.sleep_hours || 56);
          }
        }
      }
    } catch (err: any) {
      console.error(err);
      if (err.message && err.message.includes("401")) {
        setAuthError(true);
      } else {
        setError("Error de red al inicializar datos de MicroMaxocracia.");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  // Quick Escape hook
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        window.location.href = "https://es.wikipedia.org/wiki/Econom%C3%ADa_dom%C3%A9stica";
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // Update preset factors
  const handlePresetChange = (indexStr: string) => {
    setPresetIndex(indexStr);
    const index = parseInt(indexStr);
    if (index >= 0) {
      const preset = CDD_PRESETS[index];
      setTaskName(preset.name);
      setEffort(preset.effort);
      setMental(preset.mental);
      setScope(preset.scope);
    }
  };

  // VHV Formula live preview
  const liveVhiBase = effort * mental * scope;
  const liveFic = attention * fragmentation * loneliness;
  const liveVhv = duration * liveVhiBase * liveFic;

  // Actions
  const handleCreateHousehold = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!householdName.trim()) return;
    setLoading(true);
    try {
      await api.createMicroMaxHousehold(householdName);
      await loadInitialData();
    } catch (err: any) {
      setError(err.message || "Error al crear el hogar.");
    } finally {
      setLoading(false);
    }
  };

  const handleJoinHousehold = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inviteCode.trim()) return;
    setLoading(true);
    try {
      await api.joinMicroMaxHousehold(inviteCode.trim());
      await loadInitialData();
    } catch (err: any) {
      setError(err.message || "Error al unirse al hogar. Revisa el código.");
    } finally {
      setLoading(false);
    }
  };

  const handleSaveConfig = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.updateMicroMaxConfig({
        monthly_income: income,
        work_hours: workHours,
        travel_hours: travelHours,
        sleep_hours: sleepHours
      });
      await loadInitialData();
      alert("Configuración de tiempos e ingresos actualizada con éxito.");
    } catch (err: any) {
      alert("Error al actualizar configuración: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLogCDD = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isCamouflaged && survey?.score !== undefined && survey.score >= 3) {
        // Simular registro localmente
        const mockLog = {
          id: Math.floor(Math.random() * 100000),
          task_name: taskName || "Tarea Personalizada",
          duration_hours: duration,
          calculated_vhv: parseFloat(liveVhv.toFixed(2)),
          logged_date: new Date().toISOString().split("T")[0]
        };
        setLogs(prev => [mockLog, ...prev]);
        
        // Simular actualización del balance en el estado local para dar feedback visual sin cambiar backend
        setDashboard((prev: any) => {
          if (!prev) return prev;
          const updatedMembers = prev.three_accounts.members.map((m: any) => {
            if (m.name === "Tú") {
              const newCdd = m.cdd + mockLog.calculated_vhv;
              const prevShare = m.cdd_share;
              const newShare = Math.min(prevShare + 1.2, 90.0);
              return { 
                ...m, 
                cdd: parseFloat(newCdd.toFixed(2)),
                cdd_share: parseFloat(newShare.toFixed(2)),
                equilibrio: parseFloat(Math.min(m.equilibrio + 0.5, 105.0).toFixed(2))
              };
            } else {
              const newShare = Math.max(m.cdd_share - 1.2, 10.0);
              return {
                ...m,
                cdd_share: parseFloat(newShare.toFixed(2)),
                equilibrio: parseFloat(Math.max(m.equilibrio - 0.5, 95.0).toFixed(2))
              };
            }
          });
          return {
            ...prev,
            three_accounts: {
              ...prev.three_accounts,
              members: updatedMembers
            }
          };
        });

        setTaskName("");
        setDuration(1.0);
        setPresetIndex("-1");
        alert("Tarea doméstica registrada y ponderada con éxito.");
        setLoading(false);
        return;
      }

      await api.logMicroMaxCDD({
        task_name: taskName,
        duration_hours: duration,
        effort_factor: effort,
        mental_factor: mental,
        scope_factor: scope,
        attention_factor: attention,
        fragmentation_factor: fragmentation,
        loneliness_factor: loneliness
      });
      // Reset form
      setTaskName("");
      setDuration(1.0);
      setPresetIndex("-1");
      await loadInitialData();
      alert("Tarea doméstica registrada y ponderada con éxito.");
    } catch (err: any) {
      alert("No se pudo registrar la tarea: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveSurvey = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.saveMicroMaxSafetySurvey(surveyAnswers);
      setSurvey(res);
      await loadInitialData();
    } catch (err: any) {
      setError("Error al guardar la encuesta de seguridad: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLogAudit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isCamouflaged && survey?.score !== undefined && survey.score >= 3) {
        alert("Auditoría mensual guardada correctamente.");
        setConflicts(0);
        setWeapons(0);
        setAccusations(0);
        setThreats(0);
        setS1(0);
        setS2(0);
        setS3(0);
        setS4(0);
        setS5(0);
        setLoading(false);
        return;
      }

      await api.logMicroMaxAudit({
        audit_date: auditDate,
        conflicts_count: conflicts,
        weapon_count: weapons,
        accusations_count: accusations,
        threats_count: threats,
        s1_hours: s1,
        s2_score: s2,
        s3_score: s3,
        s4_score: s4,
        s5_score: s5,
        duration_weeks: auditWeeks
      });
      // Reset form
      setConflicts(0);
      setWeapons(0);
      setAccusations(0);
      setThreats(0);
      setS1(0);
      setS2(0);
      setS3(0);
      setS4(0);
      setS5(0);
      await loadInitialData();
      alert("Auditoría mensual guardada correctamente.");
    } catch (err: any) {
      alert("Error al registrar auditoría: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Redirect page if unauthorized
  if (authError) {
    return (
      <div className="min-h-screen bg-black text-slate-100 flex flex-col items-center justify-center p-6 text-center">
        <AlertTriangle size={64} className="text-amber-500 mb-6 animate-pulse" />
        <h1 className="text-3xl font-black mb-2 text-white">Sesión Requerida</h1>
        <p className="text-slate-400 mb-8 max-w-md">
          Para acceder a la MicroMaxocracia, debes iniciar sesión o crear una cuenta primero en el panel de control.
        </p>
        <a href="/login" className="px-8 py-3 rounded-xl bg-indigo-600 text-white font-bold hover:bg-indigo-500 transition-all shadow-lg shadow-indigo-500/20">
          Ir a Iniciar Sesión
        </a>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-slate-100 font-sans antialiased overflow-x-hidden">
      
      {/* Background Orbs */}
      <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] rounded-full bg-indigo-900/10 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] rounded-full bg-purple-900/10 blur-[120px] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 py-8 md:py-12 relative z-10">
        
        {/* Header */}
        <header className="mb-12 flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-slate-900">
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 rounded-2xl bg-indigo-500/10 flex items-center justify-center text-indigo-400 border border-indigo-500/20 shadow-xl shadow-indigo-500/5">
              <Heart size={32} />
            </div>
            <div>
              <h1 className="text-4xl font-extrabold text-white tracking-tight flex items-center gap-2">
                MicroMaxocracia <span className="text-xs uppercase px-2 py-0.5 rounded bg-indigo-950 border border-indigo-500/30 text-indigo-300 font-semibold">Capa 3</span>
              </h1>
              <p className="text-slate-400">Equidad Doméstica y Salud Relacional Ética</p>
            </div>
          </div>
          {household && (
            <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl flex items-center gap-4 text-sm">
              <div className="text-right">
                <div className="font-semibold text-white">{household.name}</div>
                <div className="text-xs text-slate-500">Cód. Inv: <span className="text-indigo-400 font-mono font-bold select-all">{household.invite_code}</span></div>
              </div>
              <Users className="text-indigo-400" size={20} />
            </div>
          )}
        </header>

        {loading && (
          <div className="flex items-center justify-center h-96">
            <div className="w-12 h-12 border-4 border-indigo-500/30 border-t-indigo-400 rounded-full animate-spin" />
          </div>
        )}

        {!loading && error && (
          <div className="mb-8 p-4 bg-red-500/10 border border-red-500/20 rounded-2xl text-red-400 text-sm flex items-center gap-3">
            <AlertTriangle />
            <div>{error}</div>
          </div>
        )}

        {/* 1. STATE: NO HOUSEHOLD */}
        {!loading && !household && (
          <div className="max-w-xl mx-auto my-12 space-y-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-slate-900/30 backdrop-blur-xl border border-slate-800 p-8 rounded-3xl shadow-2xl text-center space-y-6"
            >
              <div className="w-20 h-20 mx-auto rounded-full bg-indigo-500/10 flex items-center justify-center text-indigo-400">
                <Users size={40} />
              </div>
              <h2 className="text-2xl font-bold text-white">Únete a la MicroMaxocracia</h2>
              <p className="text-slate-400 max-w-sm mx-auto">
                La MicroMaxocracia permite a los miembros del hogar transparentar, registrar y equilibrar la economía y las tareas del hogar.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-slate-800">
                <form onSubmit={handleCreateHousehold} className="space-y-3 text-left">
                  <label className="text-xs font-semibold uppercase tracking-wider text-slate-400">Crear nuevo hogar</label>
                  <input
                    type="text"
                    placeholder="Nombre del Hogar"
                    value={householdName}
                    onChange={(e) => setHouseholdName(e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 text-sm"
                  />
                  <Button type="submit" className="w-full bg-indigo-600 text-white font-bold hover:bg-indigo-500">
                    Crear Hogar
                  </Button>
                </form>

                <form onSubmit={handleJoinHousehold} className="space-y-3 text-left">
                  <label className="text-xs font-semibold uppercase tracking-wider text-slate-400">Unirse a Hogar Existente</label>
                  <input
                    type="text"
                    placeholder="Código de Invitación (6 letras)"
                    value={inviteCode}
                    onChange={(e) => setInviteCode(e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 text-sm font-mono uppercase"
                  />
                  <Button type="submit" className="w-full bg-slate-800 text-slate-200 border border-slate-700 hover:bg-slate-700">
                    Unirse a Hogar
                  </Button>
                </form>
              </div>
            </motion.div>
          </div>
        )}

        {/* 2. STATE: HOUSEHOLD EXISTS BUT NO SAFETY SURVEY DONE / FAILED */}
        {!loading && household && (!survey || survey.score === undefined) && (
          <div className="max-w-2xl mx-auto my-12">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="bg-slate-900/30 backdrop-blur-xl border border-slate-800 p-8 rounded-3xl shadow-2xl space-y-6"
            >
              <div className="flex items-center gap-3 pb-4 border-b border-slate-800">
                <Shield className="text-amber-500 animate-pulse" size={28} />
                <div>
                  <h2 className="text-2xl font-black text-white">Escala de Seguridad (ESI)</h2>
                  <p className="text-slate-400 text-sm">Garantizando la salud ética y seguridad en el hogar</p>
                </div>
              </div>
              
              <div className="bg-amber-500/10 border border-amber-500/20 p-4 rounded-2xl text-amber-400 text-sm space-y-2">
                <div className="font-bold flex items-center gap-2">
                  <AlertTriangle size={18} /> IMPORTANTE
                </div>
                <p>
                  De acuerdo a las salvaguardas del sistema (Capítulo 16), es imprescindible verificar que el hogar cuenta con condiciones de respeto mutuo y simetría antes de habilitar el ledger doméstico. Responder con honestidad.
                </p>
              </div>

              {/* ESI Educational Guide Toggle */}
              <div className="space-y-4">
                <button
                  type="button"
                  onClick={() => setShowESIGuide(!showESIGuide)}
                  className="w-full py-3 px-4 rounded-2xl bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 font-bold flex justify-between items-center transition-all text-sm"
                >
                  <span className="flex items-center gap-2">
                    <Info size={18} />
                    {showESIGuide ? "Ocultar Guía de Seguridad ESI" : "Ver Guía de Seguridad ESI (Taylorismo Coercitivo)"}
                  </span>
                  <span className="text-xs">{showESIGuide ? "▲" : "▼"}</span>
                </button>

                <AnimatePresence>
                  {showESIGuide && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                      className="overflow-hidden"
                    >
                      <div className="p-5 rounded-2xl bg-slate-950 border border-slate-900 text-xs text-slate-400 space-y-4 leading-relaxed">
                        <div>
                          <h4 className="font-extrabold text-white text-sm mb-1">¿Qué es el Taylorismo Doméstico Coercitivo?</h4>
                          <p>
                            El Taylorismo es la optimización y medición científica del trabajo industrial. Llevado al hogar, el **Taylorismo Doméstico Coercitivo** ocurre cuando un miembro de la pareja o del hogar utiliza las métricas, tiempos y registros de tareas domésticas para vigilar, auditar minuciosamente, presionar o infundir culpa en los demás.
                          </p>
                        </div>
                        <div>
                          <h4 className="font-extrabold text-white text-sm mb-1">¿Por qué registrar tareas domésticas puede ser un arma?</h4>
                          <p>
                            En relaciones asimétricas, competitivas o controladoras, registrar cada minuto de lavado o cocina puede transformarse en una herramienta de agresión pasiva. Esto genera una atmósfera de evaluación constante, provocando estrés crónico, insomnio y resentimiento en lugar de promover la corresponsabilidad y la equidad.
                          </p>
                        </div>
                        <div>
                          <h4 className="font-extrabold text-white text-sm mb-1">¿Cómo te protege la Escala ESI?</h4>
                          <p>
                            La Escala de Seguridad Relacional (ESI) evalúa si tu relación cuenta con los pilares mínimos de respeto y simetría. Si respondes afirmativamente a 3 o más preguntas, el sistema detecta que el ledger doméstico **no es seguro** y podría empeorar las tensiones. Para proteger tu seguridad, el sistema simulará un funcionamiento estable pero desactivará la persistencia en el servidor para evitar que el registro sea usado en tu contra.
                          </p>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              <form onSubmit={handleSaveSurvey} className="space-y-6">
                {[
                  { id: "q1", text: "¿Alguna vez has tenido miedo de expresar desacuerdo con tu pareja o familiares sobre tareas domésticas?" },
                  { id: "q2", text: "¿Se controla coercitivamente el acceso al dinero o se requiere justificar minuciosamente cada gasto?" },
                  { id: "q3", text: "¿Has experimentado amenazas (directas o veladas) cuando cuestionaste la distribución de tareas?" },
                  { id: "q4", text: "¿Sientes que si documentaras tu carga de trabajo real en el ledger, habría represalias?" },
                  { id: "q5", text: "¿Se descalifican o menosprecian regularmente tus contribuciones al hogar?" },
                  { id: "q6", text: "¿Tienes miedo de las consecuencias de ser honesto sobre cómo te sientes?" }
                ].map((q, idx) => (
                  <div key={q.id} className="flex gap-4 items-start justify-between p-4 rounded-xl bg-slate-950 border border-slate-900 hover:border-slate-800 transition-all">
                    <span className="text-sm text-slate-300 font-medium">{idx + 1}. {q.text}</span>
                    <input
                      type="checkbox"
                      checked={(surveyAnswers as any)[q.id]}
                      onChange={(e) => setSurveyAnswers({ ...surveyAnswers, [q.id]: e.target.checked })}
                      className="w-5 h-5 accent-indigo-600 rounded cursor-pointer mt-1"
                    />
                  </div>
                ))}

                <Button type="submit" className="w-full py-4 bg-indigo-600 hover:bg-indigo-500 text-white font-extrabold rounded-2xl shadow-xl shadow-indigo-500/10">
                  Guardar y Analizar Seguridad
                </Button>
              </form>
            </motion.div>
          </div>
        )}

        {/* 4. STATE: SURVEY COMPLETED */}
        {!loading && household && survey && dashboard && (
          <div className="space-y-8">
            
            {/* Tabs Navigation */}
            <div className="flex flex-wrap gap-2 p-1 bg-slate-900/60 backdrop-blur border border-slate-800 rounded-2xl max-w-fit">
              {[
                { id: "dashboard", label: "Balance General", icon: Activity },
                { id: "log-task", label: "Registrar CDD", icon: PlusCircle },
                { id: "audit", label: "Auditoría & Salud", icon: Shield },
                { id: "config", label: "Mi Perfil Hogar", icon: Settings }
              ].map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`px-5 py-3 rounded-xl font-bold flex items-center gap-2 transition-all text-sm ${
                      activeTab === tab.id
                        ? "bg-indigo-600 text-white shadow-lg"
                        : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    <Icon size={18} />
                    {tab.label}
                  </button>
                );
              })}
            </div>

            {/* TAB CONTENT: DASHBOARD (THREE ACCOUNTS) */}
            {activeTab === "dashboard" && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                
                {/* 3 Accounts breakdown */}
                <div className="lg:col-span-2 space-y-6">
                  <div className="bg-slate-900/30 backdrop-blur-xl border border-slate-800 p-6 rounded-3xl shadow-xl space-y-6">
                    <h2 className="text-xl font-semibold flex items-center gap-2">
                      <TrendingUp size={22} className="text-indigo-400" />
                      Balance de Contribuciones Domésticas (Tres Cuentas)
                    </h2>

                    <div className="space-y-6">
                      {dashboard.three_accounts.members.map((m: any) => (
                        <div key={m.id} className="p-5 bg-slate-950 border border-slate-900 rounded-2xl space-y-4">
                          <div className="flex items-center justify-between">
                            <span className="font-extrabold text-white text-base">{m.name}</span>
                            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-900">
                              Equilibrio: {m.equilibrio}%
                            </span>
                          </div>
                          
                          {/* Progress indicators for CDD, CEH, TED */}
                          <div className="space-y-3 text-sm">
                            {/* CDD */}
                            <div>
                              <div className="flex justify-between text-xs mb-1">
                                <span className="text-slate-400">CDD (Trabajo Doméstico Directo - VHV)</span>
                                <span className="font-semibold text-coral-400">{m.cdd} VHV ({m.cdd_share}%)</span>
                              </div>
                              <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden">
                                <div className="h-full bg-coral-500 rounded-full" style={{ width: `${m.cdd_share}%` }} />
                              </div>
                            </div>
                            
                            {/* CEH */}
                            <div>
                              <div className="flex justify-between text-xs mb-1">
                                <span className="text-slate-400">CEH (Ingreso Económico Ponderado)</span>
                                <span className="font-semibold text-emerald-400">${m.income}/mes ({m.ceh_share}%)</span>
                              </div>
                              <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden">
                                <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${m.ceh_share}%` }} />
                              </div>
                            </div>

                            {/* TED */}
                            <div>
                              <div className="flex justify-between text-xs mb-1">
                                <span className="text-slate-400">TED (Tiempo de Energía Disponible)</span>
                                <span className="font-semibold text-amber-400">{m.ted}h libres ({m.ted_share}%)</span>
                              </div>
                              <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden">
                                <div className="h-full bg-amber-500 rounded-full" style={{ width: `${m.ted_share}%` }} />
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>

                    <div className="bg-slate-950 border border-slate-900 rounded-2xl p-5 space-y-4">
                      <div className="flex items-center gap-2 text-sm font-semibold text-white">
                        <Info size={18} className="text-indigo-400 shrink-0" />
                        <span>Fórmula del Equilibrio del Hogar (Las Tres Cuentas)</span>
                      </div>
                      <p className="text-xs text-slate-400 leading-relaxed">
                        El balance de la MicroMaxocracia no se limita a quién aporta más dinero. Integra tres dimensiones éticas clave para evitar la explotación del trabajo invisible:
                      </p>
                      
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
                        <div className="p-3 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
                          <div className="font-bold text-xs text-coral-400">CDD (60% del Peso)</div>
                          <div className="text-slate-300 font-semibold text-xs">Cuidado y Trabajo Doméstico</div>
                          <p className="text-[11px] text-slate-400 leading-normal">
                            Valora el trabajo invisible (limpieza, cocina, cuidado de dependientes). Se le asigna el peso mayoritario para contrarrestar la asimetría histórica de género y clase.
                          </p>
                        </div>
                        <div className="p-3 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
                          <div className="font-bold text-xs text-emerald-400">CEH (30% del Peso)</div>
                          <div className="text-slate-300 font-semibold text-xs">Contribución Económica</div>
                          <p className="text-[11px] text-slate-400 leading-normal">
                            Representa los aportes financieros al hogar. Se pondera de manera simétrica para evitar que una mayor capacidad de ingreso dicte una dominancia sobre las decisiones del hogar.
                          </p>
                        </div>
                        <div className="p-3 bg-slate-900/60 border border-slate-800 rounded-xl space-y-1">
                          <div className="font-bold text-xs text-amber-400">TED (10% del Peso)</div>
                          <div className="text-slate-300 font-semibold text-xs">Tiempo de Energía Disponible</div>
                          <p className="text-[11px] text-slate-400 leading-normal">
                            Mide el tiempo libre y descanso efectivo de cada miembro tras deducir trabajo, sueño y traslados. Asegura que nadie sufra de fatiga crónica o agotamiento extremo.
                          </p>
                        </div>
                      </div>

                      <div className="p-3 bg-indigo-950/20 border border-indigo-900/40 rounded-xl text-[11px] text-indigo-300 flex items-center justify-center font-mono">
                        Fórmula: Equilibrio = 0.6 × CDD% + 0.3 × CEH% + 0.1 × TED%
                      </div>
                    </div>
                  </div>
                </div>

                {/* Right Column: Toxicity Monitors & Detox alerts */}
                <div className="space-y-6">
                  
                  {/* Relational Health Card */}
                  <div className="bg-slate-900/30 backdrop-blur-xl border border-slate-800 p-6 rounded-3xl shadow-xl space-y-6">
                    <h2 className="text-xl font-semibold flex items-center gap-2">
                      <Activity size={22} className="text-indigo-400" />
                      Salud Relacional del Hogar
                    </h2>

                    <div className="space-y-4">
                      {/* ICE */}
                      <div className="p-4 bg-slate-950 border border-slate-900 rounded-2xl flex items-center justify-between">
                        <div>
                          <h4 className="text-xs uppercase text-slate-500 font-bold tracking-wider mb-1">Conflicto Escalado (ICE)</h4>
                          <div className="text-2xl font-black text-white">{dashboard.toxicity.ice}</div>
                        </div>
                        <span className={`px-2.5 py-1 text-xs rounded-full font-bold ${
                          dashboard.toxicity.alerts?.ice ? "bg-red-500/10 text-red-400 border border-red-500/20" : "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                        }`}>
                          {dashboard.toxicity.alerts?.ice ? "Alerta" : "Normal"}
                        </span>
                      </div>

                      {/* IDB */}
                      <div className="p-4 bg-slate-950 border border-slate-900 rounded-2xl flex items-center justify-between">
                        <div>
                          <h4 className="text-xs uppercase text-slate-500 font-bold tracking-wider mb-1">Deterioro de Bienestar (IDB)</h4>
                          <div className="text-2xl font-black text-white">{dashboard.toxicity.idb}</div>
                        </div>
                        <span className={`px-2.5 py-1 text-xs rounded-full font-bold ${
                          dashboard.toxicity.alerts?.idb ? "bg-red-500/10 text-red-400 border border-red-500/20" : "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                        }`}>
                          {dashboard.toxicity.alerts?.idb ? "Alerta" : "Normal"}
                        </span>
                      </div>

                      {/* IDP */}
                      <div className="p-4 bg-slate-950 border border-slate-900 rounded-2xl flex items-center justify-between">
                        <div>
                          <h4 className="text-xs uppercase text-slate-500 font-bold tracking-wider mb-1">Desequilibrio Persistente (IDP)</h4>
                          <div className="text-2xl font-black text-white">{dashboard.toxicity.idp}</div>
                        </div>
                        <span className={`px-2.5 py-1 text-xs rounded-full font-bold ${
                          dashboard.toxicity.alerts?.idp ? "bg-red-500/10 text-red-400 border border-red-500/20" : "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                        }`}>
                          {dashboard.toxicity.alerts?.idp ? "Alerta" : "Normal"}
                        </span>
                      </div>
                    </div>

                    {/* Detox Protocol triggered warning */}
                    {dashboard.toxicity.detox_triggered && (
                      <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="p-5 bg-red-950/20 border border-red-500/30 rounded-2xl space-y-3"
                      >
                        <div className="text-red-400 font-extrabold text-sm flex items-center gap-2">
                          <AlertTriangle /> PROTOCOLO DE DESINTOXICACIÓN ACTIVO
                        </div>
                        <p className="text-slate-400 text-xs leading-relaxed">
                          Debido a que al menos dos de los índices de salud relacional han cruzado el umbral, se ha activado automáticamente el protocolo de emergencia ética:
                        </p>
                        <ul className="text-slate-300 text-xs list-disc pl-4 space-y-1">
                          <li><strong>Pausa Total:</strong> Detener el registro y ponderación de CDD/ledger por 14 días.</li>
                          <li><strong>Negociación Espontánea:</strong> Volver a esquemas tradicionales o conversados directamente.</li>
                          <li><strong>Facilitación:</strong> Consultar un facilitador externo para resolver las tensiones del ledger.</li>
                        </ul>
                      </motion.div>
                    )}
                  </div>
                </div>

              </div>
            )}

            {/* TAB CONTENT: LOG TASK (CDD) */}
            {activeTab === "log-task" && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                
                {/* Logger Form */}
                <div className="lg:col-span-7 space-y-6">
                  <div className="bg-slate-900/30 backdrop-blur-xl border border-slate-800 p-6 rounded-3xl shadow-xl space-y-6">
                    <h2 className="text-xl font-semibold flex items-center gap-2">
                      <PlusCircle className="text-indigo-400" />
                      Registrar Contribución Doméstica Directa (CDD)
                    </h2>

                    <form onSubmit={handleLogCDD} className="space-y-4">
                      
                      {/* Presets Select */}
                      <div className="space-y-1.5">
                        <label className="text-xs font-semibold uppercase tracking-wider text-slate-400">Presets de la MicroMaxocracia</label>
                        <select
                          value={presetIndex}
                          onChange={(e) => handlePresetChange(e.target.value)}
                          className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white focus:outline-none focus:border-indigo-500 text-sm"
                        >
                          <option value="-1">-- Personalizado / Ninguno --</option>
                          {CDD_PRESETS.map((p, idx) => (
                            <option key={idx} value={idx}>{p.name}</option>
                          ))}
                        </select>
                      </div>

                      {/* Task Name */}
                      <div className="space-y-1.5">
                        <label className="text-xs font-semibold uppercase tracking-wider text-slate-400">Descripción de la Tarea</label>
                        <input
                          type="text"
                          required
                          value={taskName}
                          onChange={(e) => setTaskName(e.target.value)}
                          placeholder="Ej: Limpieza de baño principal, preparación almuerzo"
                          className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 text-sm"
                        />
                      </div>

                      {/* Duration */}
                      <div className="space-y-1.5">
                        <div className="flex justify-between text-xs font-semibold uppercase tracking-wider text-slate-400">
                          <span>Duración (Horas)</span>
                          <span className="font-bold text-white">{duration} hrs</span>
                        </div>
                        <input
                          type="range"
                          min="0.1"
                          max="8.0"
                          step="0.1"
                          value={duration}
                          onChange={(e) => setDuration(parseFloat(e.target.value))}
                          className="w-full accent-indigo-600"
                        />
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {/* Effort */}
                        <div className="space-y-1.5">
                          <label className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1">
                            Esfuerzo Físico
                            <span className="text-white">({effort})</span>
                          </label>
                          <input
                            type="range"
                            min="1.0"
                            max="2.0"
                            step="0.1"
                            value={effort}
                            onChange={(e) => setEffort(parseFloat(e.target.value))}
                            className="w-full accent-indigo-600"
                          />
                        </div>

                        {/* Mental */}
                        <div className="space-y-1.5">
                          <label className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1">
                            Carga Mental
                            <span className="text-white">({mental})</span>
                          </label>
                          <input
                            type="range"
                            min="1.0"
                            max="1.5"
                            step="0.05"
                            value={mental}
                            onChange={(e) => setMental(parseFloat(e.target.value))}
                            className="w-full accent-indigo-600"
                          />
                        </div>

                        {/* Scope */}
                        <div className="space-y-1.5">
                          <label className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1">
                            Alcance Familiar
                            <span className="text-white">({scope})</span>
                          </label>
                          <input
                            type="range"
                            min="1.0"
                            max="2.0"
                            step="0.1"
                            value={scope}
                            onChange={(e) => setScope(parseFloat(e.target.value))}
                            className="w-full accent-indigo-600"
                          />
                        </div>
                      </div>

                      {/* Intensity FIC factors */}
                      <div className="pt-4 border-t border-slate-800 space-y-4">
                        <h4 className="text-sm font-semibold text-white">Intensidad Contextual (FIC)</h4>
                        
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                          {/* Attention */}
                          <div className="space-y-1">
                            <label className="text-slate-400">Atención Requerida</label>
                            <select
                              value={attention}
                              onChange={(e) => setAttention(parseFloat(e.target.value))}
                              className="w-full px-2 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-white focus:outline-none focus:border-indigo-500"
                            >
                              <option value="1.0">Supervisión pasiva (1.0)</option>
                              <option value="1.5">Supervisión activa (1.5)</option>
                              <option value="1.8">Supervisión intensiva (1.8)</option>
                              <option value="2.0">Atención total/Crisis (2.0)</option>
                            </select>
                          </div>

                          {/* Fragmentation */}
                          <div className="space-y-1">
                            <label className="text-slate-400">Fragmentación / Interrupciones</label>
                            <select
                              value={fragmentation}
                              onChange={(e) => setFragmentation(parseFloat(e.target.value))}
                              className="w-full px-2 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-white focus:outline-none focus:border-indigo-500"
                            >
                              <option value="1.0">Continua / Sin interrupciones (1.0)</option>
                              <option value="1.2">Pocas interrupciones (1.2)</option>
                              <option value="1.4">Interrupciones moderadas (1.4)</option>
                              <option value="1.6">Muchas interrupciones (1.6)</option>
                              <option value="1.8">Interrupciones constantes (1.8)</option>
                            </select>
                          </div>

                          {/* Loneliness */}
                          <div className="space-y-1">
                            <label className="text-slate-400">Acompañamiento / Soledad</label>
                            <select
                              value={loneliness}
                              onChange={(e) => setLoneliness(parseFloat(e.target.value))}
                              className="w-full px-2 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-white focus:outline-none focus:border-indigo-500"
                            >
                              <option value="1.0">Con ayuda activa (1.0)</option>
                              <option value="1.2">Con presencia (1.2)</option>
                              <option value="1.1">Con comunidad (1.1)</option>
                              <option value="1.3">Solo parcialmente (1.3)</option>
                              <option value="1.5">Completamente solo (1.5)</option>
                            </select>
                          </div>
                        </div>
                      </div>

                      <Button type="submit" className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-extrabold rounded-xl shadow-lg">
                        Registrar Tarea
                      </Button>
                    </form>
                  </div>
                </div>

                {/* Live Preview & Recent logs */}
                <div className="lg:col-span-5 space-y-6">
                  {/* Live preview */}
                  <div className="bg-gradient-to-br from-indigo-950/30 to-purple-950/30 border border-indigo-500/20 p-6 rounded-3xl shadow-xl space-y-3 relative overflow-hidden group">
                    <h3 className="text-xs uppercase text-indigo-400 font-bold tracking-wider">Cálculo VHV de la Tarea</h3>
                    <div className="flex items-baseline gap-1">
                      <span className="text-5xl font-black text-white">{liveVhv.toFixed(2)}</span>
                      <span className="text-lg font-bold text-indigo-400">VHV</span>
                    </div>
                    <div className="text-xs text-slate-500 space-y-1 pt-2 border-t border-slate-800">
                      <div>Base: {effort}e × {mental}m × {scope}s = {liveVhiBase.toFixed(2)} VHI/h</div>
                      <div>FIC: {attention}a × {fragmentation}f × {loneliness}l = {liveFic.toFixed(2)}x</div>
                    </div>
                  </div>

                  {/* Educational Formula Guide */}
                  <div className="bg-slate-900/30 backdrop-blur-xl border border-slate-800 p-6 rounded-3xl shadow-xl space-y-4">
                    <h3 className="text-sm font-semibold flex items-center gap-2 text-white">
                      <Info size={16} className="text-indigo-400" />
                      ¿Cómo calculamos la Huella Vital (VHV)?
                    </h3>
                    <div className="text-xs text-slate-400 space-y-3">
                      <p>
                        La **Huella Vital Doméstica (VHV)** valora de manera justa las tareas domésticas sumando el esfuerzo físico, la fatiga mental y el impacto del acompañamiento o la soledad.
                      </p>
                      <div className="p-3 bg-slate-950 border border-slate-900 rounded-xl font-mono text-center text-slate-300">
                        VHV = Duración × Base (VHI) × Multiplicador (FIC)
                      </div>
                      <div className="space-y-2">
                        <h4 className="font-semibold text-slate-300">Variables Base (VHI/h):</h4>
                        <ul className="list-disc pl-4 space-y-1">
                          <li><span className="text-slate-200">Esfuerzo Físico:</span> Grado de exigencia o cansancio físico (de 1.0 a 2.0).</li>
                          <li><span className="text-slate-200">Carga Mental:</span> Planificación, anticipación y atención cognitiva requerida (de 1.0 a 1.5).</li>
                          <li><span className="text-slate-200">Alcance Familiar:</span> Si beneficia a todo el hogar o solo de forma individual (de 1.0 a 2.0).</li>
                        </ul>
                      </div>
                      <div className="space-y-2 pt-2 border-t border-slate-900">
                        <h4 className="font-semibold text-slate-300">Multiplicadores de Intensidad Contextual (FIC):</h4>
                        <ul className="list-disc pl-4 space-y-1">
                          <li><span className="text-slate-200">Atención:</span> La carga de supervisión o reacción rápida (ej. cuidar un bebé es intensiva).</li>
                          <li><span className="text-slate-200">Fragmentación:</span> Interrupciones constantes que fragmentan el descanso (ej. interrupciones de niños).</li>
                          <li><span className="text-slate-200">Soledad:</span> Si la tarea se realiza en aislamiento total o con compañía/comunidad.</li>
                        </ul>
                      </div>
                    </div>
                  </div>

                  {/* Recent Logs list */}
                  <div className="bg-slate-900/30 backdrop-blur-xl border border-slate-800 p-6 rounded-3xl shadow-xl space-y-4">
                    <h3 className="text-lg font-semibold flex items-center gap-2">
                      <ClipboardList size={18} className="text-indigo-400" />
                      Tareas Recientes Registradas
                    </h3>
                    <div className="space-y-3 max-h-[300px] overflow-y-auto pr-2">
                      {logs.length === 0 ? (
                        <p className="text-slate-600 text-sm text-center py-6">No has registrado ninguna tarea todavía.</p>
                      ) : (
                        logs.map((log) => (
                          <div key={log.id} className="p-3 bg-slate-950 border border-slate-900 rounded-xl flex items-center justify-between text-sm">
                            <div>
                              <div className="font-semibold text-white">{log.task_name}</div>
                              <div className="text-xs text-slate-500">{log.logged_date} • {log.duration_hours}h</div>
                            </div>
                            <span className="font-extrabold text-indigo-400">{log.calculated_vhv} VHV</span>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                </div>

              </div>
            )}

            {/* TAB CONTENT: AUDIT & HEALTH */}
            {activeTab === "audit" && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                
                {/* Audit Registry Form */}
                <div className="bg-slate-900/30 backdrop-blur-xl border border-slate-800 p-6 rounded-3xl shadow-xl space-y-6">
                  <h2 className="text-xl font-semibold flex items-center gap-2">
                    <Calendar className="text-indigo-400" />
                    Registrar Sesión de Auditoría Doméstica
                  </h2>
                  <p className="text-slate-400 text-xs leading-relaxed">
                    Las auditorías deben registrarse semanal o mensualmente tras el diálogo estructurado del hogar (Capítulo 6). Complete los conteos de tensiones/conflictos y el bienestar de los participantes.
                  </p>

                  <form onSubmit={handleLogAudit} className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      {/* Date */}
                      <div className="space-y-1">
                        <label className="text-xs text-slate-400">Fecha de Auditoría</label>
                        <input
                          type="date"
                          value={auditDate}
                          onChange={(e) => setAuditDate(e.target.value)}
                          className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-white text-sm"
                        />
                      </div>

                      {/* Weeks */}
                      <div className="space-y-1">
                        <label className="text-xs text-slate-400">Duración Evaluada (Semanas)</label>
                        <input
                          type="number"
                          min="1"
                          max="52"
                          value={auditWeeks}
                          onChange={(e) => setAuditWeeks(parseInt(e.target.value))}
                          className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-white text-sm"
                        />
                      </div>
                    </div>

                    <div className="space-y-3 pt-3 border-t border-slate-800">
                      <h4 className="text-sm font-semibold text-white">Conteos de Conflicto en el Periodo</h4>
                      
                      <div className="grid grid-cols-2 gap-4 text-xs">
                        <div className="space-y-1">
                          <label className="text-slate-400">Total Conflictos Auditados</label>
                          <input
                            type="number"
                            min="0"
                            value={conflicts}
                            onChange={(e) => setConflicts(parseInt(e.target.value))}
                            className="w-full px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-white"
                          />
                        </div>
                        
                        <div className="space-y-1">
                          <label className="text-slate-400">Uso de datos como Arma (+2 pts c/u)</label>
                          <input
                            type="number"
                            min="0"
                            value={weapons}
                            onChange={(e) => setWeapons(parseInt(e.target.value))}
                            className="w-full px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-white"
                          />
                        </div>

                        <div className="space-y-1">
                          <label className="text-slate-400">Acusaciones Personales (+1 pt c/u)</label>
                          <input
                            type="number"
                            min="0"
                            value={accusations}
                            onChange={(e) => setAccusations(parseInt(e.target.value))}
                            className="w-full px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-white"
                          />
                        </div>

                        <div className="space-y-1">
                          <label className="text-slate-400">Amenazas de Abandono (+3 pts c/u)</label>
                          <input
                            type="number"
                            min="0"
                            value={threats}
                            onChange={(e) => setThreats(parseInt(e.target.value))}
                            className="w-full px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-white"
                          />
                        </div>
                      </div>
                    </div>

                    <div className="space-y-3 pt-3 border-t border-slate-800">
                      <h4 className="text-sm font-semibold text-white">Deterioro de Bienestar Reciente</h4>
                      
                      <div className="space-y-2 text-xs">
                        <div className="flex items-center justify-between">
                          <label className="text-slate-400">S1. Horas de sueño perdidas por ansiedad sobre el ledger (Peso: 2.0)</label>
                          <input
                            type="number"
                            min="0"
                            step="0.5"
                            value={s1}
                            onChange={(e) => setS1(parseFloat(e.target.value))}
                            className="w-16 px-2 py-1 rounded bg-slate-950 border border-slate-800 text-white text-right"
                          />
                        </div>

                        <div className="flex items-center justify-between">
                          <label className="text-slate-400">S2. Aumento de discusiones fuera de auditorías (Escala 1-5, Peso: 1.5)</label>
                          <input
                            type="number"
                            min="0"
                            max="5"
                            value={s2}
                            onChange={(e) => setS2(parseFloat(e.target.value))}
                            className="w-16 px-2 py-1 rounded bg-slate-950 border border-slate-800 text-white text-right"
                          />
                        </div>

                        <div className="flex items-center justify-between">
                          <label className="text-slate-400">S3. Disminución de momentos de conexión espontánea (Escala 1-5, Peso: 1.8)</label>
                          <input
                            type="number"
                            min="0"
                            max="5"
                            value={s3}
                            onChange={(e) => setS3(parseFloat(e.target.value))}
                            className="w-16 px-2 py-1 rounded bg-slate-950 border border-slate-800 text-white text-right"
                          />
                        </div>

                        <div className="flex items-center justify-between">
                          <label className="text-slate-400">S4. Aumento de ansiedad generalizada (Escala 1-10, Peso: 2.0)</label>
                          <input
                            type="number"
                            min="0"
                            max="10"
                            value={s4}
                            onChange={(e) => setS4(parseFloat(e.target.value))}
                            className="w-16 px-2 py-1 rounded bg-slate-950 border border-slate-800 text-white text-right"
                          />
                        </div>

                        <div className="flex items-center justify-between">
                          <label className="text-slate-400">S5. Sensación de evaluación constante (Escala 1-10, Peso: 1.5)</label>
                          <input
                            type="number"
                            min="0"
                            max="10"
                            value={s5}
                            onChange={(e) => setS5(parseFloat(e.target.value))}
                            className="w-16 px-2 py-1 rounded bg-slate-950 border border-slate-800 text-white text-right"
                          />
                        </div>
                      </div>
                    </div>

                    <Button type="submit" className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-extrabold rounded-xl shadow-lg">
                      Guardar Reporte de Auditoría
                    </Button>
                  </form>
                </div>

                {/* Column 2: Audit History & Education */}
                <div className="space-y-6">
                  {/* History of audits */}
                  <div className="bg-slate-900/30 backdrop-blur-xl border border-slate-800 p-6 rounded-3xl shadow-xl space-y-6">
                    <h2 className="text-xl font-semibold flex items-center gap-2">
                      <ClipboardList className="text-indigo-400" />
                      Historial de Auditorías
                    </h2>
                    
                    <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2">
                      {dashboard.toxicity.reasons.includes("Sin auditorías registradas") ? (
                        <p className="text-slate-600 text-sm text-center py-12">No hay auditorías registradas todavía.</p>
                      ) : (
                        // We can just query and render the list of audits if it's available or make a simple template
                        <div className="p-4 bg-slate-950 border border-slate-900 rounded-2xl space-y-2">
                          <div className="font-semibold text-white flex justify-between">
                            <span>Última Auditoría Auditada</span>
                            <span className="text-indigo-400">{dashboard.toxicity.reasons.length > 0 ? "Indices Alerta" : "Estado Estable"}</span>
                          </div>
                          <p className="text-slate-400 text-xs leading-relaxed">
                            La salud relacional actual está determinada por los siguientes indicadores calculados:
                          </p>
                          <ul className="text-xs text-slate-300 list-disc pl-4 space-y-1">
                            <li>ICE: {dashboard.toxicity.ice} (Conflicto)</li>
                            <li>IDB: {dashboard.toxicity.idb} (Bienestar)</li>
                            <li>IDP: {dashboard.toxicity.idp} (Desequilibrio doméstico)</li>
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Toxicity and Detox explanation */}
                  <div className="bg-slate-900/30 backdrop-blur-xl border border-slate-800 p-6 rounded-3xl shadow-xl space-y-6">
                    <h2 className="text-xl font-semibold flex items-center gap-2">
                      <Shield className="text-indigo-400" size={22} />
                      Índices de Salud Relacional y Protocolo Detox
                    </h2>
                    <p className="text-xs text-slate-400 leading-relaxed">
                      El ledger doméstico es una herramienta poderosa, pero no debe convertirse en un factor de estrés. Monitoreamos tres índices de toxicidad para proteger la convivencia:
                    </p>

                    <div className="space-y-4">
                      {/* ICE description */}
                      <div className="p-4 bg-slate-950 border border-slate-900 rounded-2xl space-y-2">
                        <div className="flex justify-between items-center text-xs">
                          <span className="font-extrabold text-white">ICE: Índice de Conflicto Escalado</span>
                          <span className="font-semibold text-red-400">Umbral: ≥ 3.0</span>
                        </div>
                        <p className="text-[11px] text-slate-400 leading-relaxed">
                          Evalúa la frecuencia de peleas, uso de datos como armas arrojadizas (reproches métricos), acusaciones personales y amenazas de abandono en el hogar.
                        </p>
                      </div>

                      {/* IDB description */}
                      <div className="p-4 bg-slate-950 border border-slate-900 rounded-2xl space-y-2">
                        <div className="flex justify-between items-center text-xs">
                          <span className="font-extrabold text-white">IDB: Índice de Deterioro de Bienestar</span>
                          <span className="font-semibold text-red-400">Umbral: ≥ 5.0</span>
                        </div>
                        <p className="text-[11px] text-slate-400 leading-relaxed">
                          Mide el impacto psicológico del ledger: insomnio, ansiedad por cumplir metas, sensación de estar bajo evaluación constante y pérdida de conexiones espontáneas.
                        </p>
                      </div>

                      {/* IDP description */}
                      <div className="p-4 bg-slate-950 border border-slate-900 rounded-2xl space-y-2">
                        <div className="flex justify-between items-center text-xs">
                          <span className="font-extrabold text-white">IDP: Índice de Desequilibrio Persistente</span>
                          <span className="font-semibold text-red-400">Umbral: ≥ 0.50</span>
                        </div>
                        <p className="text-[11px] text-slate-400 leading-relaxed">
                          Detecta si la brecha de distribución de tareas se perpetúa durante más de 3 auditorías consecutivas, indicando explotación sistemática de un miembro.
                        </p>
                      </div>
                    </div>

                    <div className="p-4 bg-red-950/20 border border-red-500/20 rounded-2xl text-xs space-y-2">
                      <div className="font-bold text-red-400 flex items-center gap-1.5">
                        <AlertTriangle size={15} /> Protocolo de Desintoxicación Doméstica
                      </div>
                      <p className="text-[11px] text-slate-400 leading-relaxed">
                        Si **dos o más de estos índices cruzan sus umbrales**, el sistema bloquea y congela el registro de tareas (CDD) durante 14 días de forma obligatoria. Durante esta pausa, el hogar debe negociar de forma tradicional y directa, sin el auxilio de métricas, y se recomienda asesoramiento familiar externo.
                      </p>
                    </div>
                  </div>
                </div>

              </div>
            )}

            {/* TAB CONTENT: PROFILE/SETTINGS */}
            {activeTab === "config" && (
              <div className="max-w-2xl mx-auto">
                <div className="bg-slate-900/30 backdrop-blur-xl border border-slate-800 p-6 rounded-3xl shadow-xl space-y-6">
                  <h2 className="text-xl font-semibold flex items-center gap-2">
                    <UserCheck className="text-indigo-400" />
                    Configuración de Perfil Doméstico
                  </h2>
                  <p className="text-slate-400 text-xs leading-relaxed">
                    Para calcular el **Tiempo de Energía Disponible (TED)** y el **Índice de Contribución Económica (CEH)** de manera justa, actualice los parámetros de horas de trabajo externo, traslados y sus ingresos mensuales promedio.
                  </p>

                  <form onSubmit={handleSaveConfig} className="space-y-4">
                    {/* Monthly Income */}
                    <div className="space-y-1">
                      <label className="text-xs text-slate-400">Ingresos Mensuales Promedio (Moneda Local)</label>
                      <input
                        type="number"
                        min="0"
                        value={income}
                        onChange={(e) => setIncome(parseFloat(e.target.value))}
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 text-sm"
                      />
                    </div>

                    {/* Work Hours */}
                    <div className="space-y-1">
                      <label className="text-xs text-slate-400">Horas Semanales de Trabajo Remunerado</label>
                      <input
                        type="number"
                        min="0"
                        max="120"
                        value={workHours}
                        onChange={(e) => setWorkHours(parseFloat(e.target.value))}
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 text-sm"
                      />
                    </div>

                    {/* Travel Hours */}
                    <div className="space-y-1">
                      <label className="text-xs text-slate-400">Horas Semanales de Traslados/Transporte</label>
                      <input
                        type="number"
                        min="0"
                        max="80"
                        value={travelHours}
                        onChange={(e) => setTravelHours(parseFloat(e.target.value))}
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 text-sm"
                      />
                    </div>

                    {/* Sleep Hours */}
                    <div className="space-y-1">
                      <label className="text-xs text-slate-400">Horas Semanales de Sueño/Descanso (Por defecto 56 hrs - 8h/día)</label>
                      <input
                        type="number"
                        min="20"
                        max="112"
                        value={sleepHours}
                        onChange={(e) => setSleepHours(parseFloat(e.target.value))}
                        className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 text-sm"
                      />
                    </div>

                    <Button type="submit" className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-extrabold rounded-xl shadow-lg">
                      Guardar Cambios de Perfil
                    </Button>
                  </form>

                  <div className="pt-4 border-t border-slate-800 text-center">
                    <Button
                      onClick={async () => {
                        if (confirm("¿Estás seguro de que deseas desvincularte de este hogar?")) {
                          // In a real database we could set household_id = null or similar
                          alert("Para cambiar de hogar o salirte de manera permanente, contacta al administrador del sistema.");
                        }
                      }}
                      variant="outline"
                      className="border-red-500/30 hover:bg-red-500/10 text-red-400 text-xs font-semibold"
                    >
                      Solicitar Desvinculación de Hogar
                    </Button>
                  </div>
                </div>
              </div>
            )}

          </div>
        )}

        {/* Footer */}
        <footer className="mt-20 pt-8 border-t border-slate-900 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-slate-500">
          <p>© {new Date().getFullYear()} MicroMaxocracia - Licencia de Uso Doméstico Seguro</p>
          <div className="flex gap-6">
            <button 
              onClick={() => setShowSecuritySupport(true)}
              className="hover:text-slate-400 transition-all underline cursor-pointer bg-transparent border-0"
            >
              Soporte y Privacidad del Hogar
            </button>
            <a href="https://es.wikipedia.org/wiki/Econom%C3%ADa_dom%C3%A9stica" className="hover:text-slate-400 transition-all">
              Términos Generales
            </a>
          </div>
        </footer>

      </div>

      {/* Quick Escape Floating Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={() => window.location.href = "https://es.wikipedia.org/wiki/Econom%C3%ADa_dom%C3%A9stica"}
          className="px-4 py-2.5 rounded-full bg-slate-900/90 border border-slate-800 text-slate-400 hover:text-white text-xs font-semibold shadow-lg backdrop-blur-md transition-all hover:bg-slate-800 flex items-center gap-2"
          title="Presiona Esc para salir rápido"
        >
          <LogOut size={14} />
          Salida Rápida (Esc)
        </button>
      </div>

      {/* Security Support Modal */}
      <AnimatePresence>
        {showSecuritySupport && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-slate-900 border border-slate-800 max-w-lg w-full rounded-3xl p-6 shadow-2xl relative space-y-6"
            >
              <div className="flex items-center gap-3 pb-4 border-b border-slate-800">
                <Shield className="text-indigo-400" size={24} />
                <div>
                  <h3 className="text-xl font-bold text-white">Soporte y Privacidad del Hogar</h3>
                  <p className="text-slate-400 text-xs">Información de seguridad y restablecimiento de cuenta</p>
                </div>
              </div>

              <div className="space-y-4 text-sm text-slate-300">
                <p>
                  Esta sección proporciona recursos para asegurar que la MicroMaxocracia se utilice como una herramienta de equidad y no de coerción.
                </p>

                <div className="p-4 rounded-xl bg-slate-950 border border-slate-850 space-y-3">
                  <div className="font-semibold text-white flex items-center gap-2">
                    <Heart className="text-red-500 animate-pulse" size={16} /> Recursos de Ayuda y Orientación:
                  </div>
                  <p className="text-xs text-slate-400">
                    Si te encuentras en una situación de hostilidad, control o violencia, puedes comunicarte de forma gratuita y confidencial con profesionales:
                  </p>
                  <ul className="text-xs space-y-2 text-slate-300 font-medium">
                    <li className="flex justify-between items-center p-2 rounded bg-slate-900 border border-slate-800">
                      <span>Línea 155 (Violencia de Género)</span>
                      <span className="text-indigo-400 font-bold font-mono">Llamar / Chat</span>
                    </li>
                    <li className="flex justify-between items-center p-2 rounded bg-slate-900 border border-slate-800">
                      <span>Línea 141 (Apoyo y Contención)</span>
                      <span className="text-indigo-400 font-bold font-mono">Llamar</span>
                    </li>
                  </ul>
                </div>

                <div className="p-4 rounded-xl bg-slate-950 border border-slate-850 space-y-3">
                  <div className="font-semibold text-white">Restablecer Cuestionario de Seguridad</div>
                  <p className="text-xs text-slate-400">
                    Si necesitas volver a responder la encuesta ESI para reconfigurar el acceso al ledger del hogar, puedes hacerlo a continuación.
                  </p>
                  <Button
                    onClick={async () => {
                      if (confirm("¿Estás seguro de que deseas reiniciar la encuesta de seguridad?")) {
                        setLoading(true);
                        setShowSecuritySupport(false);
                        try {
                          const newAnswers = { q1: false, q2: false, q3: false, q4: false, q5: false, q6: false };
                          setSurveyAnswers(newAnswers);
                          const res = await api.saveMicroMaxSafetySurvey(newAnswers);
                          setSurvey(res);
                          await loadInitialData();
                        } catch(err: any) {
                          alert("Error al restablecer: " + err.message);
                        } finally {
                          setLoading(false);
                        }
                      }
                    }}
                    className="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-bold py-2 rounded-xl text-xs"
                  >
                    Reiniciar Encuesta ESI
                  </Button>
                </div>
              </div>

              <div className="flex justify-end pt-4 border-t border-slate-800">
                <Button 
                  onClick={() => setShowSecuritySupport(false)}
                  className="bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-6 py-2 rounded-xl text-sm"
                >
                  Cerrar
                </Button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

    </div>
  );
}
