"use client";

import React, { useState, useEffect } from "react";
import { Input } from "../ui/Input";
import { Button } from "../ui/Button";
import { motion } from "framer-motion";

interface VHVFormProps {
  onCalculate: (data: any) => void;
  initialData?: any;
}

export default function VHVForm({ onCalculate, initialData }: VHVFormProps) {
  const [formData, setFormData] = useState({
    name: initialData?.name || "",
    t_direct_hours: initialData?.t_direct_hours || 0,
    t_inherited_hours: initialData?.t_inherited_hours || 0,
    t_future_hours: initialData?.t_future_hours || 0,
    v_organisms_affected: initialData?.v_organisms_affected || 0,
    v_consciousness_factor: initialData?.v_consciousness_factor || 1,
    v_suffering_factor: initialData?.v_suffering_factor || 1,
    v_abundance_factor: initialData?.v_abundance_factor || 1,
    v_rarity_factor: initialData?.v_rarity_factor || 1,
    r_minerals_kg: initialData?.r_minerals_kg || 0,
    r_water_m3: initialData?.r_water_m3 || 0,
    r_petroleum_l: initialData?.r_petroleum_l || 0,
    r_land_hectares: initialData?.r_land_hectares || 0,
    r_frg_factor: initialData?.r_frg_factor || 1,
    r_cs_factor: initialData?.r_cs_factor || 1,
  });

  useEffect(() => {
    if (initialData) {
      setFormData(prev => ({ ...prev, ...initialData }));
    }
  }, [initialData]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "number" ? parseFloat(value) || 0 : value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onCalculate(formData);
  };

  const inputGroupClass = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8";
  const sectionTitleClass = "text-lg font-semibold mb-4 flex items-center gap-2";

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800 p-6 rounded-2xl shadow-2xl">
        <div className="mb-6">
          <Input
            label="Nombre del Producto"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Ej: Huevo Ético"
            className="text-lg"
          />
        </div>

        {/* TIME SECTION */}
        <section>
          <h3 className={`${sectionTitleClass} text-coral-400`}>
            <span className="w-8 h-8 rounded-full bg-coral-500/20 flex items-center justify-center text-sm">T</span>
            Tiempo Vital Invertido
          </h3>
          <div className={inputGroupClass}>
            <Input
              type="number"
              step="0.01"
              label="Horas Directas"
              name="t_direct_hours"
              value={formData.t_direct_hours}
              onChange={handleChange}
            />
            <Input
              type="number"
              step="0.01"
              label="Horas Heredadas"
              name="t_inherited_hours"
              value={formData.t_inherited_hours}
              onChange={handleChange}
            />
            <Input
              type="number"
              step="0.01"
              label="Horas Futuras"
              name="t_future_hours"
              value={formData.t_future_hours}
              onChange={handleChange}
            />
          </div>
        </section>

        {/* LIFE SECTION */}
        <section>
          <h3 className={`${sectionTitleClass} text-emerald-400`}>
            <span className="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center text-sm">V</span>
            Costo de Vida Afectada
          </h3>
          <div className={inputGroupClass}>
            <Input
              type="number"
              step="0.0001"
              label="Organismos Afectados"
              name="v_organisms_affected"
              value={formData.v_organisms_affected}
              onChange={handleChange}
            />
            <Input
              type="number"
              step="0.1"
              label="Factor de Conciencia (0-1)"
              name="v_consciousness_factor"
              value={formData.v_consciousness_factor}
              onChange={handleChange}
            />
            <Input
              type="number"
              step="0.1"
              label="Factor de Sufrimiento"
              name="v_suffering_factor"
              value={formData.v_suffering_factor}
              onChange={handleChange}
            />
            <Input
              type="number"
              step="0.0001"
              label="Factor de Abundancia"
              name="v_abundance_factor"
              value={formData.v_abundance_factor}
              onChange={handleChange}
            />
            <Input
              type="number"
              step="0.1"
              label="Factor de Rareza"
              name="v_rarity_factor"
              value={formData.v_rarity_factor}
              onChange={handleChange}
            />
          </div>
        </section>

        {/* RESOURCES SECTION */}
        <section>
          <h3 className={`${sectionTitleClass} text-amber-600`}>
            <span className="w-8 h-8 rounded-full bg-amber-600/20 flex items-center justify-center text-sm">R</span>
            Recursos Naturales
          </h3>
          <div className={inputGroupClass}>
            <Input
              type="number"
              step="0.01"
              label="Minerales (kg)"
              name="r_minerals_kg"
              value={formData.r_minerals_kg}
              onChange={handleChange}
            />
            <Input
              type="number"
              step="0.01"
              label="Agua (m³)"
              name="r_water_m3"
              value={formData.r_water_m3}
              onChange={handleChange}
            />
            <Input
              type="number"
              step="0.01"
              label="Petróleo (l)"
              name="r_petroleum_l"
              value={formData.r_petroleum_l}
              onChange={handleChange}
            />
            <Input
              type="number"
              step="0.01"
              label="Tierra (Ha)"
              name="r_land_hectares"
              value={formData.r_land_hectares}
              onChange={handleChange}
            />
            <Input
              type="number"
              step="0.1"
              label="Factor FRG"
              name="r_frg_factor"
              value={formData.r_frg_factor}
              onChange={handleChange}
            />
            <Input
              type="number"
              step="0.1"
              label="Factor CS"
              name="r_cs_factor"
              value={formData.r_cs_factor}
              onChange={handleChange}
            />
          </div>
        </section>

        <div className="flex justify-end gap-4 mt-8 pt-6 border-t border-slate-800">
          <Button type="submit" variant="primary" className="px-8">
            Calcular VHV
          </Button>
        </div>
      </div>
    </form>
  );
}
