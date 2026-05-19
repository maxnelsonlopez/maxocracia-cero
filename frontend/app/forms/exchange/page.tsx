"use client";

import React, { useState } from "react";
import { FormWizard } from "../../components/ui/FormWizard";
import { FormStep } from "../../components/ui/FormStep";
import { Input } from "../../components/ui/Input";
import { FormTextArea } from "../../components/ui/FormTextArea";
import { FormCheckboxGroup } from "../../components/ui/FormCheckboxGroup";
import { FormRadioGroup } from "../../components/ui/FormRadioGroup";
import { ParticipantSearch } from "../../components/ui/ParticipantSearch";
import { apiFetch } from "../../lib/api";
import { motion } from "framer-motion";
import { CheckCircle2, AlertCircle } from "lucide-react";

const EXCHANGE_TYPES = [
  { label: "Objeto", value: "objeto", emoji: "📦" },
  { label: "Habilidad / Servicio", value: "habilidad", emoji: "🛠" },
  { label: "Alimentación", value: "alimentacion", emoji: "🍽" },
  { label: "Conocimiento", value: "conocimiento", emoji: "📚" },
];

const URGENCY_LEVELS = [
  { label: "Alta", value: "Alta", emoji: "🔴" },
  { label: "Media", value: "Media", emoji: "🟡" },
  { label: "Baja", value: "Baja", emoji: "🟢" },
];

const RESOLUTION_SCORES = [
  { label: "5 - Completamente", value: "5" },
  { label: "3 - Parcialmente", value: "3" },
  { label: "1 - Poco o Nada", value: "1" },
];

const RECIPROCITY_STATUS = [
  { label: "Completada (I-A)", value: "Completada", emoji: "🔄" },
  { label: "Pendiente", value: "Pendiente", emoji: "⏳" },
  { label: "Dato Puro / Donativo", value: "Dato Puro", emoji: "🎁" },
];

const HUMAN_DIMENSIONS = [
  { label: "Subsistencia", value: "alimentacion" },
  { label: "Salud / Protección", value: "salud" },
  { label: "Conexión Social", value: "social" },
];

const COORDINATION_METHODS = [
  { label: "WhatsApp", value: "WhatsApp", emoji: "📱" },
  { label: "Telegram", value: "Telegram", emoji: "✈️" },
  { label: "Presencial", value: "Presencial", emoji: "👤" },
];

interface Participant {
  id: number;
  name: string;
  email: string;
  city: string;
}

export default function ExchangeFormPage() {
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split("T")[0],
    interchange_id: "",
    giver_id: null as number | null,
    receiver_id: null as number | null,
    type: [] as string[],
    description: "",
    urgency: "Media",
    uth_hours: "",
    economic_value: "",
    urf_description: "",
    impact_resolution_score: "5",
    reciprocity_status: "Completada",
    human_dimension: [] as string[],
    coordination_method: "WhatsApp",
    requires_followup: "0",
    followup_scheduled_date: "",
    facilitator_notes: "",
  });

  const [giver, setGiver] = useState<Participant | null>(null);
  const [receiver, setReceiver] = useState<Participant | null>(null);
  const [status, setStatus] = useState<"idle" | "submitting" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    if (!formData.giver_id || !formData.receiver_id) {
      setErrorMessage("Debes seleccionar tanto al emisor como al receptor de la ayuda.");
      setStatus("error");
      return;
    }

    setStatus("submitting");
    try {
      const response = await apiFetch("/forms/exchange", {
        method: "POST",
        body: JSON.stringify({
          ...formData,
          uth_hours: formData.uth_hours ? parseFloat(formData.uth_hours) : 0,
          economic_value: formData.economic_value ? parseInt(formData.economic_value) : 0,
          requires_followup: parseInt(formData.requires_followup),
        }),
      });

      if (response.ok) {
        setStatus("success");
      } else {
        const data = await response.json();
        setErrorMessage(data.error || "Ocurrió un error al registrar el intercambio.");
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
          <h2 className="text-3xl font-bold text-white mb-4">¡Intercambio Registrado!</h2>
          <p className="text-slate-400 mb-8">
            El flujo de la Red de Apoyo ha sido actualizado exitosamente.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="w-full py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-xl transition-all shadow-lg shadow-emerald-500/20"
          >
            Registrar otro intercambio
          </button>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto mb-12 text-center">
        <h1 className="text-4xl md:text-5xl font-black text-white mb-4 tracking-tight">
          🤝 Registro de <span className="text-emerald-500">Intercambio</span>
        </h1>
        <p className="text-slate-400 max-w-2xl mx-auto">
          Mide el flujo de ayuda y el impacto de la Red en tiempo real.
        </p>
      </div>

      {status === "error" && (
        <div className="max-w-2xl mx-auto mb-8 p-4 bg-red-500/10 border border-red-500/30 rounded-xl flex items-center gap-3 text-red-400">
          <AlertCircle size={20} />
          <p className="text-sm font-medium">{errorMessage}</p>
        </div>
      )}

      <FormWizard
        steps={["Identificación", "Descripción", "Métricas", "Logística"]}
        onComplete={handleSubmit}
        isSubmitting={status === "submitting"}
      >
        {/* Paso 1: Identificación */}
        <FormStep
          title="🔖 Identificación"
          description="Selecciona los participantes involucrados y la fecha."
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Fecha del Intercambio"
              name="date"
              type="date"
              value={formData.date}
              onChange={handleChange}
              required
            />
            <Input
              label="Código / ID de Intercambio"
              name="interchange_id"
              value={formData.interchange_id}
              onChange={handleChange}
              required
              placeholder="Ej: INT-001"
            />
          </div>
          <ParticipantSearch
            label="¿Quién DIO la ayuda?"
            selectedParticipant={giver}
            onSelect={(p) => {
              setGiver(p);
              setFormData((prev) => ({ ...prev, giver_id: p ? p.id : null }));
            }}
          />
          <ParticipantSearch
            label="¿Quién RECIBIÓ la ayuda?"
            selectedParticipant={receiver}
            onSelect={(p) => {
              setReceiver(p);
              setFormData((prev) => ({ ...prev, receiver_id: p ? p.id : null }));
            }}
          />
        </FormStep>

        {/* Paso 2: Descripción */}
        <FormStep
          title="📦 ¿Qué se intercambió?"
          description="Detalla el tipo de ayuda y su nivel de urgencia."
        >
          <FormCheckboxGroup
            label="Tipo de Intercambio"
            options={EXCHANGE_TYPES}
            selectedValues={formData.type}
            onChange={(vals) => setFormData((prev) => ({ ...prev, type: vals }))}
          />
          <FormTextArea
            label="Descripción del intercambio"
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            placeholder="Ej: Préstamo de escalera por 3 días o 2 horas de tutoría"
          />
          <FormRadioGroup
            label="Urgencia de la necesidad atendida"
            options={URGENCY_LEVELS}
            selectedValue={formData.urgency}
            onChange={(val) => setFormData((prev) => ({ ...prev, urgency: val }))}
          />
        </FormStep>

        {/* Paso 3: Métricas Maxocráticas */}
        <FormStep
          title="⏱️ Métricas y Impacto"
          description="Cuantifica el esfuerzo humano y la efectividad."
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex flex-col gap-1 w-full">
               <label className="text-sm font-medium text-slate-300 ml-1">Unidades de Talento Humano (Horas)</label>
               <div className="relative">
                  <input
                    type="number"
                    name="uth_hours"
                    step="0.5"
                    value={formData.uth_hours}
                    onChange={handleChange}
                    placeholder="0.0"
                    className="w-full px-4 py-3 bg-slate-900/50 backdrop-blur-md border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500/50"
                  />
                  <span className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 text-sm font-bold">UTH</span>
               </div>
            </div>
            <div className="flex flex-col gap-1 w-full">
               <label className="text-sm font-medium text-slate-300 ml-1">Valor Económico Ref. (Pesos)</label>
               <div className="relative">
                  <input
                    type="number"
                    name="economic_value"
                    value={formData.economic_value}
                    onChange={handleChange}
                    placeholder="0"
                    className="w-full px-4 py-3 bg-slate-900/50 backdrop-blur-md border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 pl-8"
                  />
                  <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 text-sm font-bold">$</span>
               </div>
            </div>
          </div>
          <FormTextArea
            label="Unidad de Recursos Físicos (URF)"
            name="urf_description"
            value={formData.urf_description}
            onChange={handleChange}
            placeholder="¿Qué materiales o herramientas se usaron?"
          />
          <FormRadioGroup
            label="Grado de resolución de la necesidad"
            options={RESOLUTION_SCORES}
            selectedValue={formData.impact_resolution_score}
            onChange={(val) => setFormData((prev) => ({ ...prev, impact_resolution_score: val }))}
          />
          <FormRadioGroup
            label="Estado de Reciprocidad"
            options={RECIPROCITY_STATUS}
            selectedValue={formData.reciprocity_status}
            onChange={(val) => setFormData((prev) => ({ ...prev, reciprocity_status: val }))}
          />
        </FormStep>

        {/* Paso 4: Logística y Notas */}
        <FormStep
          title="✨ Logística y Seguimiento"
          description="Registra cómo se coordinó y si requiere atención futura."
        >
          <FormCheckboxGroup
            label="Dimensión Humana Atendida"
            options={HUMAN_DIMENSIONS}
            selectedValues={formData.human_dimension}
            onChange={(vals) => setFormData((prev) => ({ ...prev, human_dimension: vals }))}
          />
          <FormRadioGroup
            label="¿Cómo se coordinó?"
            options={COORDINATION_METHODS}
            selectedValue={formData.coordination_method}
            onChange={(val) => setFormData((prev) => ({ ...prev, coordination_method: val }))}
          />
          <FormRadioGroup
            label="¿Requiere seguimiento?"
            options={[
              { label: "Sí", value: "1" },
              { label: "No", value: "0" },
            ]}
            selectedValue={formData.requires_followup}
            onChange={(val) => setFormData((prev) => ({ ...prev, requires_followup: val }))}
          />
          {formData.requires_followup === "1" && (
            <Input
              label="Fecha sugerida de seguimiento"
              name="followup_scheduled_date"
              type="date"
              value={formData.followup_scheduled_date}
              onChange={handleChange}
            />
          )}
          <FormTextArea
            label="Notas del Facilitador / Observaciones"
            name="facilitator_notes"
            value={formData.facilitator_notes}
            onChange={handleChange}
            placeholder="Cualquier detalle adicional relevante..."
          />
        </FormStep>
      </FormWizard>
    </div>
  );
}
