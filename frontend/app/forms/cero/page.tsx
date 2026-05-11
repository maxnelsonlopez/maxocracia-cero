"use client";

import React, { useState } from "react";
import { FormWizard } from "../../components/ui/FormWizard";
import { FormStep } from "../../components/ui/FormStep";
import { Input } from "../../components/ui/Input";
import { FormTextArea } from "../../components/ui/FormTextArea";
import { FormCheckboxGroup } from "../../components/ui/FormCheckboxGroup";
import { FormRadioGroup } from "../../components/ui/FormRadioGroup";
import { apiFetch } from "../../lib/api";
import { motion } from "framer-motion";
import { CheckCircle2, AlertCircle } from "lucide-react";

const OFFER_CATEGORIES = [
  { label: "Objeto", value: "objeto", emoji: "📦" },
  { label: "Alimentación", value: "alimentacion", emoji: "🍽" },
  { label: "Habilidad / Servicio", value: "habilidad", emoji: "🛠" },
  { label: "Conocimiento / Consejo", value: "conocimiento", emoji: "📚" },
  { label: "Transporte / Acompañamiento", value: "transporte", emoji: "🚗" },
  { label: "Tiempo y Compañía", value: "tiempo", emoji: "⏰" },
  { label: "Espacio", value: "espacio", emoji: "🏠" },
  { label: "Apoyo Económico", value: "apoyo_economico", emoji: "💰" },
];

const HUMAN_DIMENSIONS = [
  { label: "Crecimiento y Aprendizaje", value: "crecimiento_aprendizaje" },
  { label: "Bienestar y Descanso", value: "bienestar_descanso" },
  { label: "Seguridad y Estabilidad", value: "seguridad_estabilidad" },
  { label: "Autoestima y Autonomía", value: "autoestima_autonomia" },
  { label: "Conexión Social", value: "conexion_social" },
];

const NEED_CATEGORIES = [
  { label: "Objeto", value: "objeto", emoji: "📦" },
  { label: "Alimentación", value: "alimentacion", emoji: "🍽" },
  { label: "Habilidad / Servicio", value: "habilidad", emoji: "🛠" },
];

const URGENCY_LEVELS = [
  { label: "Alta", value: "Alta", emoji: "🔴" },
  { label: "Media", value: "Media", emoji: "🟡" },
  { label: "Baja", value: "Baja", emoji: "🟢" },
];

export default function CeroFormPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    referred_by: "",
    phone_call: "",
    phone_whatsapp: "",
    telegram_handle: "",
    city: "",
    neighborhood: "",
    personal_values: "",
    offer_categories: [] as string[],
    offer_description: "",
    offer_human_dimensions: [] as string[],
    need_categories: [] as string[],
    need_description: "",
    need_urgency: "Media",
    consent_given: false,
  });

  const [status, setStatus] = useState<"idle" | "submitting" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    setStatus("submitting");
    try {
      const response = await apiFetch("/forms/participant", {
        method: "POST",
        body: JSON.stringify({
          ...formData,
          consent_given: formData.consent_given ? 1 : 0,
        }),
      });

      if (response.ok) {
        setStatus("success");
      } else {
        const data = await response.json();
        setErrorMessage(data.error || "Ocurrió un error al enviar el formulario.");
        setStatus("error");
      }
    } catch (err) {
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
          <h2 className="text-3xl font-bold text-white mb-4">¡Registro Exitoso!</h2>
          <p className="text-slate-400 mb-8">
            Gracias por unirte a la Red de Apoyo Maxocracia. Tus datos han sido guardados correctamente.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="w-full py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-xl transition-all shadow-lg shadow-emerald-500/20"
          >
            Registrar otro participante
          </button>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto mb-12 text-center">
        <h1 className="text-4xl md:text-5xl font-black text-white mb-4 tracking-tight">
          🤝 Únete a la <span className="text-emerald-500">Red de Apoyo</span>
        </h1>
        <p className="text-slate-400 max-w-2xl mx-auto">
          Este es el primer paso para crear una comunidad resiliente. Toda la información es voluntaria y confidencial.
        </p>
      </div>

      {status === "error" && (
        <div className="max-w-2xl mx-auto mb-8 p-4 bg-red-500/10 border border-red-500/30 rounded-xl flex items-center gap-3 text-red-400">
          <AlertCircle size={20} />
          <p className="text-sm font-medium">{errorMessage}</p>
        </div>
      )}

      <FormWizard
        steps={["Identidad", "Oferta", "Necesidad", "Finalizar"]}
        onComplete={handleSubmit}
        isSubmitting={status === "submitting"}
      >
        {/* Paso 1: ¿Quién Eres? */}
        <FormStep
          title="👤 ¿Quién Eres?"
          description="Cuéntanos un poco sobre ti para poder contactarte."
        >
          <Input
            label="Tu nombre o Alias"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            placeholder="Ej: Max Nelson"
          />
          <Input
            label="Tu correo electrónico"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            required
            placeholder="usuario@ejemplo.com"
          />
          <Input
            label="¿Quién te invitó?"
            name="referred_by"
            value={formData.referred_by}
            onChange={handleChange}
            required
            placeholder="Nombre de la persona o medio"
          />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Teléfono (Llamadas)"
              name="phone_call"
              value={formData.phone_call}
              onChange={handleChange}
              required
              placeholder="+57..."
            />
            <Input
              label="WhatsApp"
              name="phone_whatsapp"
              value={formData.phone_whatsapp}
              onChange={handleChange}
              required
              placeholder="+57..."
            />
          </div>
          <Input
            label="Telegram (@usuario)"
            name="telegram_handle"
            value={formData.telegram_handle}
            onChange={handleChange}
            placeholder="@maxocrata"
          />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Ciudad"
              name="city"
              value={formData.city}
              onChange={handleChange}
              required
            />
            <Input
              label="Barrio / Localidad"
              name="neighborhood"
              value={formData.neighborhood}
              onChange={handleChange}
              required
            />
          </div>
          <FormTextArea
            label="¿Qué valores te representan?"
            name="personal_values"
            value={formData.personal_values}
            onChange={handleChange}
            required
            placeholder="Ej: Solidaridad, transparencia, compromiso..."
          />
        </FormStep>

        {/* Paso 2: ¿Cómo podrías ayudar? */}
        <FormStep
          title="🎁 ¿Cómo Podrías Ayudar?"
          description="Selecciona las categorías donde puedes aportar a otros."
        >
          <FormCheckboxGroup
            label="Categorías de Ayuda"
            options={OFFER_CATEGORIES}
            selectedValues={formData.offer_categories}
            onChange={(vals) => setFormData((prev) => ({ ...prev, offer_categories: vals }))}
          />
          <FormTextArea
            label="Describe brevemente lo que ofreces"
            name="offer_description"
            value={formData.offer_description}
            onChange={handleChange}
            required
            placeholder='Ej: "Ofrezco mi taladro usado que está en buen estado"'
          />
          <FormCheckboxGroup
            label="¿En qué dimensiones humanas ayuda tu oferta?"
            options={HUMAN_DIMENSIONS}
            selectedValues={formData.offer_human_dimensions}
            onChange={(vals) => setFormData((prev) => ({ ...prev, offer_human_dimensions: vals }))}
          />
        </FormStep>

        {/* Paso 3: ¿Qué necesitas? */}
        <FormStep
          title="🙏 ¿Qué Necesitas?"
          description="No tengas miedo de pedir. La red funciona cuando todos somos honestos."
        >
          <FormCheckboxGroup
            label="Categorías de Necesidad"
            options={NEED_CATEGORIES}
            selectedValues={formData.need_categories}
            onChange={(vals) => setFormData((prev) => ({ ...prev, need_categories: vals }))}
          />
          <FormTextArea
            label="Describe tu necesidad"
            name="need_description"
            value={formData.need_description}
            onChange={handleChange}
            required
            placeholder="¿Qué necesitas hoy para estar mejor?"
          />
          <FormRadioGroup
            label="Urgencia"
            options={URGENCY_LEVELS}
            selectedValue={formData.need_urgency}
            onChange={(val) => setFormData((prev) => ({ ...prev, need_urgency: val }))}
          />
        </FormStep>

        {/* Paso 4: Consentimiento */}
        <FormStep
          title="✅ Finalizar"
          description="Casi terminamos. Por favor acepta el manejo de datos."
        >
          <div className="p-6 bg-slate-900/60 border border-slate-800 rounded-2xl">
            <label className="flex items-start gap-3 cursor-pointer group">
              <input
                type="checkbox"
                className="mt-1 w-5 h-5 rounded border-slate-700 bg-slate-950 text-emerald-500 focus:ring-emerald-500/50 transition-all"
                checked={formData.consent_given}
                onChange={(e) => setFormData((prev) => ({ ...prev, consent_given: e.target.checked }))}
                required
              />
              <span className="text-slate-300 text-sm leading-relaxed group-hover:text-white transition-colors">
                Acepto los términos y condiciones de la Red de Apoyo Maxocracia y autorizo el manejo de mis datos personales para ser contactado por facilitadores y otros participantes de la red con el fin de gestionar intercambios de ayuda.
              </span>
            </label>
          </div>
        </FormStep>
      </FormWizard>
    </div>
  );
}
