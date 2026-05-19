"use client";

import React, { useState, useEffect } from "react";
import { FormWizard } from "../../components/ui/FormWizard";
import { FormStep } from "../../components/ui/FormStep";
import { Input } from "../../components/ui/Input";
import { FormTextArea } from "../../components/ui/FormTextArea";
import { FormCheckboxGroup } from "../../components/ui/FormCheckboxGroup";
import { FormRadioGroup } from "../../components/ui/FormRadioGroup";
import { ParticipantSearch } from "../../components/ui/ParticipantSearch";
import { apiFetch } from "../../lib/api";
import { motion } from "framer-motion";
import { CheckCircle2, AlertCircle, RefreshCcw } from "lucide-react";

const FOLLOWUP_TYPES = [
  { label: "Rutina", value: "Rutina", emoji: "🔄" },
  { label: "Urgente", value: "Urgente", emoji: "🚨" },
  { label: "Cierre de Caso", value: "Cierre", emoji: "🏁" },
];

const NEED_LEVELS = [
  { label: "1 - Estable", value: "1" },
  { label: "2 - Leve", value: "2" },
  { label: "3 - Moderada", value: "3" },
  { label: "4 - Alta", value: "4" },
  { label: "5 - Crítica", value: "5" },
];

const SITUATION_CHANGES = [
  { label: "Mejoró", value: "Mejoró", emoji: "📈" },
  { label: "Igual", value: "Igual", emoji: "➖" },
  { label: "Empeoró", value: "Empeoró", emoji: "📉" },
];

const ACTIVE_INTERCHANGES_STATUS = [
  { label: "Ninguno activo", value: "none" },
  { label: "Fluyendo bien", value: "fluyendo" },
  { label: "Estancado / Problemas", value: "estancado" },
];

const WELL_WORKING_FACTORS = [
  { label: "Comunicación", value: "comunicacion" },
  { label: "Tiempos de entrega", value: "tiempos" },
  { label: "Calidad de la ayuda", value: "calidad" },
];

const NEW_NEEDS = [
  { label: "Alimentación", value: "alimentacion" },
  { label: "Salud / Bienestar", value: "salud" },
  { label: "Herramientas / Objetos", value: "herramientas" },
];

const EMOTIONAL_STATES = [
  { label: "Positivo", value: "positivo", emoji: "😊" },
  { label: "Neutral", value: "neutral", emoji: "😐" },
  { label: "Negativo / Estresado", value: "negativo", emoji: "😔" },
];

const REQUIRED_ACTIONS = [
  { label: "Buscar nuevo match", value: "nuevo_match" },
  { label: "Mediación en conflicto", value: "mediacion" },
  { label: "Gestionar recurso externo", value: "gestionar_recurso" },
];

const FOLLOWUP_PRIORITIES = [
  { label: "Alta (Inmediata)", value: "high", emoji: "🔴" },
  { label: "Media (Semanal)", value: "medium", emoji: "🟡" },
  { label: "Baja (Mensual)", value: "low", emoji: "🟢" },
  { label: "Cerrado", value: "closed", emoji: "✅" },
];

interface Participant {
  id: number;
  name: string;
  email: string;
  city: string;
}

interface Exchange {
  id: number;
  interchange_id: string;
  description: string;
  date: string;
}

export default function FollowUpFormPage() {
  const [formData, setFormData] = useState({
    follow_up_date: new Date().toISOString().split("T")[0],
    participant_id: null as number | null,
    related_interchange_id: "",
    follow_up_type: "Rutina",
    current_situation: "",
    need_level: "1",
    situation_change: "Igual",
    active_interchanges_status: "none",
    interchanges_working_well: [] as string[],
    new_needs_detected: [] as string[],
    new_offers_detected: "",
    emotional_state: "neutral",
    actions_required: [] as string[],
    follow_up_priority: "medium",
    next_follow_up_date: "",
    learnings: "",
  });

  const [participant, setParticipant] = useState<Participant | null>(null);
  const [exchanges, setExchanges] = useState<Exchange[]>([]);
  const [isLoadingExchanges, setIsLoadingExchanges] = useState(false);
  const [status, setStatus] = useState<"idle" | "submitting" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    if (participant) {
      loadExchanges(participant.id);
    } else {
      setExchanges([]);
    }
  }, [participant]);

  const loadExchanges = async (pid: number) => {
    setIsLoadingExchanges(true);
    try {
      // Intentamos cargar intercambios donde sea giver o receiver
      const [resGiver, resReceiver] = await Promise.all([
        apiFetch(`/forms/exchanges?giver_id=${pid}&limit=10`),
        apiFetch(`/forms/exchanges?receiver_id=${pid}&limit=10`)
      ]);

      let allExchanges: Exchange[] = [];
      if (resGiver.ok) {
        const data = await resGiver.json();
        allExchanges = [...allExchanges, ...(data.exchanges || [])];
      }
      if (resReceiver.ok) {
        const data = await resReceiver.json();
        allExchanges = [...allExchanges, ...(data.exchanges || [])];
      }

      // Eliminar duplicados si los hay y ordenar por fecha
      const uniqueExchanges = Array.from(new Set(allExchanges.map(e => e.id)))
        .map(id => allExchanges.find(e => e.id === id)!)
        .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

      setExchanges(uniqueExchanges);
    } catch {
      console.error("Error loading exchanges");
    } finally {
      setIsLoadingExchanges(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    if (!formData.participant_id) {
      setErrorMessage("Debes seleccionar un participante.");
      setStatus("error");
      return;
    }

    setStatus("submitting");
    try {
      const response = await apiFetch("/forms/follow-up", {
        method: "POST",
        body: JSON.stringify({
          ...formData,
          need_level: parseInt(formData.need_level),
          related_interchange_id: formData.related_interchange_id ? parseInt(formData.related_interchange_id) : null,
        }),
      });

      if (response.ok) {
        setStatus("success");
      } else {
        const data = await response.json();
        setErrorMessage(data.error || "Ocurrió un error al registrar el seguimiento.");
        setStatus("error");
      }
    } catch {
      setErrorMessage("Error de conexión con el servidor.");
      setStatus("error");
    }
  };

  if (status === "success") {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="bg-slate-900/40 backdrop-blur-xl border border-emerald-500/30 rounded-3xl p-10 text-center max-w-md shadow-2xl"
        >
          <div className="w-20 h-20 bg-emerald-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle2 className="text-emerald-500" size={48} />
          </div>
          <h2 className="text-3xl font-bold text-white mb-4">¡Seguimiento Registrado!</h2>
          <p className="text-slate-400 mb-8">
            El reporte ha sido procesado y la prioridad del participante actualizada.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="w-full py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-xl transition-all shadow-lg shadow-emerald-500/20"
          >
            Registrar otro seguimiento
          </button>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto mb-12 text-center">
        <h1 className="text-4xl md:text-5xl font-black text-white mb-4 tracking-tight">
          📊 Reporte de <span className="text-emerald-500">Seguimiento</span>
        </h1>
        <p className="text-slate-400 max-w-2xl mx-auto">
          Evalúa la evolución de los participantes y el impacto de los intercambios.
        </p>
      </div>

      {status === "error" && (
        <div className="max-w-2xl mx-auto mb-8 p-4 bg-red-500/10 border border-red-500/30 rounded-xl flex items-center gap-3 text-red-400">
          <AlertCircle size={20} />
          <p className="text-sm font-medium">{errorMessage}</p>
        </div>
      )}

      <FormWizard
        steps={["Identificación", "Estado Actual", "Impacto", "Hallazgos", "Cierre"]}
        onComplete={handleSubmit}
        isSubmitting={status === "submitting"}
      >
        {/* Paso 1: Identificación */}
        <FormStep
          title="🔖 Identificación"
          description="Selecciona el participante y el intercambio relacionado."
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Fecha del Seguimiento"
              name="follow_up_date"
              type="date"
              value={formData.follow_up_date}
              onChange={handleChange}
              required
            />
            <div className="flex flex-col gap-1 w-full">
              <label className="text-sm font-medium text-slate-300 ml-1">Tipo de Seguimiento</label>
              <select
                name="follow_up_type"
                value={formData.follow_up_type}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-slate-900/50 backdrop-blur-md border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500/50"
              >
                {FOLLOWUP_TYPES.map(t => (
                  <option key={t.value} value={t.value}>{t.emoji} {t.label}</option>
                ))}
              </select>
            </div>
          </div>
          <ParticipantSearch
            label="Nombre del Participante"
            selectedParticipant={participant}
            onSelect={(p) => {
              setParticipant(p);
              setFormData((prev) => ({ ...prev, participant_id: p ? p.id : null }));
            }}
          />
          {participant && (
            <div className="flex flex-col gap-1 w-full animate-in fade-in slide-in-from-top-2 duration-300">
              <label className="text-sm font-medium text-slate-300 ml-1">Intercambio Relacionado (Opcional)</label>
              <div className="relative">
                <select
                  name="related_interchange_id"
                  value={formData.related_interchange_id}
                  onChange={handleChange}
                  disabled={isLoadingExchanges}
                  className="w-full px-4 py-3 bg-slate-900/50 backdrop-blur-md border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 appearance-none disabled:opacity-50"
                >
                  <option value="">Ninguno o Selecciona uno...</option>
                  {exchanges.map(e => (
                    <option key={e.id} value={e.id}>
                      {e.interchange_id} - {e.description.substring(0, 40)}... ({e.date})
                    </option>
                  ))}
                </select>
                {isLoadingExchanges && (
                  <RefreshCcw size={16} className="absolute right-4 top-1/2 -translate-y-1/2 text-emerald-500 animate-spin" />
                )}
              </div>
            </div>
          )}
        </FormStep>

        {/* Paso 2: Estado Actual */}
        <FormStep
          title="📈 Estado Actual"
          description="¿Cómo se encuentra el participante en este momento?"
        >
          <FormTextArea
            label="Situación Actual del Participante"
            name="current_situation"
            value={formData.current_situation}
            onChange={handleChange}
            required
            placeholder="Describe detalladamente cómo está la persona hoy..."
          />
          <FormRadioGroup
            label="Nivel de Necesidad Actual"
            options={NEED_LEVELS}
            selectedValue={formData.need_level}
            onChange={(val) => setFormData((prev) => ({ ...prev, need_level: val }))}
          />
          <FormRadioGroup
            label="Cambio desde el último contacto"
            options={SITUATION_CHANGES}
            selectedValue={formData.situation_change}
            onChange={(val) => setFormData((prev) => ({ ...prev, situation_change: val }))}
          />
        </FormStep>

        {/* Paso 3: Impacto de Intercambios */}
        <FormStep
          title="🤝 Impacto de Intercambios"
          description="Evaluación de la efectividad de la ayuda recibida."
        >
          <FormRadioGroup
            label="Estado de Intercambios en curso"
            options={ACTIVE_INTERCHANGES_STATUS}
            selectedValue={formData.active_interchanges_status}
            onChange={(val) => setFormData((prev) => ({ ...prev, active_interchanges_status: val }))}
          />
          <FormCheckboxGroup
            label="Cosas que están funcionando bien"
            options={WELL_WORKING_FACTORS}
            selectedValues={formData.interchanges_working_well}
            onChange={(vals) => setFormData((prev) => ({ ...prev, interchanges_working_well: vals }))}
          />
          <FormRadioGroup
            label="Estado Emocional Observado"
            options={EMOTIONAL_STATES}
            selectedValue={formData.emotional_state}
            onChange={(val) => setFormData((prev) => ({ ...prev, emotional_state: val }))}
          />
        </FormStep>

        {/* Paso 4: Nuevos Hallazgos */}
        <FormStep
          title="🔍 Nuevos Hallazgos"
          description="Nuevas necesidades u ofertas detectadas durante el contacto."
        >
          <FormCheckboxGroup
            label="Nuevas Necesidades Detectadas"
            options={NEW_NEEDS}
            selectedValues={formData.new_needs_detected}
            onChange={(vals) => setFormData((prev) => ({ ...prev, new_needs_detected: vals }))}
          />
          <FormTextArea
            label="Nuevas Ofertas / Talentos Detectados"
            name="new_offers_detected"
            value={formData.new_offers_detected}
            onChange={handleChange}
            placeholder="¿Algo nuevo que la persona pueda ofrecer a la red?"
          />
          <FormCheckboxGroup
            label="Acciones Requeridas"
            options={REQUIRED_ACTIONS}
            selectedValues={formData.actions_required}
            onChange={(vals) => setFormData((prev) => ({ ...prev, actions_required: vals }))}
          />
        </FormStep>

        {/* Paso 5: Acciones y Cierre */}
        <FormStep
          title="🎯 Acciones y Cierre"
          description="Define la prioridad y el próximo contacto."
        >
          <FormRadioGroup
            label="Prioridad de Próximo Seguimiento"
            options={FOLLOWUP_PRIORITIES}
            selectedValue={formData.follow_up_priority}
            onChange={(val) => setFormData((prev) => ({ ...prev, follow_up_priority: val }))}
          />
          <Input
            label="Fecha Programada Siguiente contacto"
            name="next_follow_up_date"
            type="date"
            value={formData.next_follow_up_date}
            onChange={handleChange}
          />
          <FormTextArea
            label="Lecciones aprendidas o Notas del facilitador"
            name="learnings"
            value={formData.learnings}
            onChange={handleChange}
            placeholder="Reflexiones sobre el caso o detalles operativos..."
          />
        </FormStep>
      </FormWizard>
    </div>
  );
}
