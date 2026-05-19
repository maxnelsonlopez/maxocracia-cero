"use client";

import React, { useState } from "react";
import { 
  CreditCard, 
  TrendingUp, 
  Users, 
  DollarSign, 
  AlertCircle, 
  Search,
  Sparkles
} from "lucide-react";
import { motion } from "framer-motion";

// Datos simulados premium
const MOCK_TRANSACTIONS = [
  { id: "tx_1001", user: "Sophia Kovalevsky", email: "sophia.k@maxo.org", tier: "Enterprise", amount: 200, country: "DE", date: "Hace 2 horas" },
  { id: "tx_1002", user: "Alexander Grothendieck", email: "al.groth@coherence.net", tier: "Contributor", amount: 8.75, country: "FR", date: "Hace 4 horas" },
  { id: "tx_1003", user: "Hypatia of Alexandria", email: "hypatia@libres.org", tier: "Contributor", amount: 6.25, country: "MX", date: "Hace 1 día" },
  { id: "tx_1004", user: "Alan Turing", email: "enigma@decoders.io", tier: "Enterprise", amount: 200, country: "GB", date: "Hace 2 días" },
  { id: "tx_1005", user: "Ada Lovelace", email: "ada@poeticalscience.com", tier: "Contributor", amount: 25, country: "US", date: "Hace 3 días" },
];

export default function AdminSubscriptions() {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredTransactions = MOCK_TRANSACTIONS.filter(tx => 
    tx.user.toLowerCase().includes(searchTerm.toLowerCase()) || 
    tx.tier.toLowerCase().includes(searchTerm.toLowerCase()) ||
    tx.id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-8">
      {/* Aviso de Calibración Axiomática */}
      <motion.div 
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 flex items-start gap-3"
      >
        <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5 animate-pulse" />
        <div>
          <h4 className="font-semibold text-sm">Calibración Axiomática en Progreso</h4>
          <p className="text-xs text-amber-400/80 mt-1">
            Los flujos financieros y de suscripción se están sincronizando con el oráculo de Stripe en modo seguro. 
            El cálculo en tiempo real del factor de paridad de poder adquisitivo (PPP) está activo y auditado.
          </p>
        </div>
      </motion.div>

      {/* Tarjetas de Métricas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard 
          title="MRR Estimado" 
          value="$2,450.00" 
          change="+12.4%" 
          description="Ingreso mensual recurrente" 
          icon={<DollarSign className="w-5 h-5 text-emerald-400" />} 
        />
        <MetricCard 
          title="Contribuyentes Activos" 
          value="182" 
          change="+8.3%" 
          description="Suscripciones premium activas" 
          icon={<Users className="w-5 h-5 text-emerald-400" />} 
        />
        <MetricCard 
          title="Tasa de Retención" 
          value="98.4%" 
          change="+1.2%" 
          description="Retención de contribuyentes" 
          icon={<TrendingUp className="w-5 h-5 text-emerald-400" />} 
        />
        <MetricCard 
          title="Fondo de Reserva Coherente" 
          value="$12,840" 
          change="+15.8%" 
          description="Sostenibilidad pública" 
          icon={<CreditCard className="w-5 h-5 text-emerald-400" />} 
        />
      </div>

      {/* Sección Principal */}
      <div className="grid lg:grid-cols-3 gap-8">
        
        {/* Distribución de Tiers */}
        <div className="lg:col-span-1 bg-slate-900/50 border border-slate-800 rounded-2xl p-6 space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-white">Distribución de Tiers</h3>
            <Sparkles className="w-4 h-4 text-emerald-400" />
          </div>

          <div className="space-y-4">
            <TierProgress label="Enterprise (Aporte Máximo)" count={12} percentage={10} color="bg-amber-500" value="$2,400" />
            <TierProgress label="Contributor (Aporte Coherente)" count={118} percentage={70} color="bg-emerald-500" value="$1,050" />
            <TierProgress label="Free (Aporte Básico)" count={450} percentage={20} color="bg-slate-500" value="$0" />
          </div>

          <div className="pt-4 border-t border-slate-800">
            <div className="flex items-center justify-between text-sm text-slate-400">
              <span>Sostenibilidad Alcanzada</span>
              <span className="text-emerald-400 font-mono font-semibold">120%</span>
            </div>
            <div className="w-full bg-slate-800 h-2 rounded-full mt-2 overflow-hidden">
              <div className="bg-emerald-500 h-full rounded-full" style={{ width: "100%" }} />
            </div>
          </div>
        </div>

        {/* Historial de Transacciones */}
        <div className="lg:col-span-2 bg-slate-900/50 border border-slate-800 rounded-2xl p-6 space-y-6">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h3 className="font-semibold text-white">Últimas Contribuciones</h3>
              <p className="text-xs text-slate-400 mt-1">Transacciones procesadas en las últimas 72 horas</p>
            </div>
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
              <input 
                type="text" 
                placeholder="Buscar contribuidor..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-9 pr-4 py-2 text-xs rounded-xl bg-slate-950 border border-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500 text-slate-300 w-56"
              />
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 font-medium">
                  <th className="py-3 px-4">ID Transacción</th>
                  <th className="py-3 px-4">Usuario</th>
                  <th className="py-3 px-4">Nivel</th>
                  <th className="py-3 px-4 text-right">Monto (USD)</th>
                  <th className="py-3 px-4">Fecha</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50">
                {filteredTransactions.map((tx) => (
                  <tr key={tx.id} className="text-slate-300 hover:bg-slate-800/20 transition-colors">
                    <td className="py-4 px-4 font-mono text-[10px] text-slate-500">{tx.id}</td>
                    <td className="py-4 px-4">
                      <div>
                        <p className="font-semibold text-white">{tx.user}</p>
                        <p className="text-[10px] text-slate-500">{tx.email}</p>
                      </div>
                    </td>
                    <td className="py-4 px-4">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold ${
                        tx.tier === "Enterprise" 
                          ? "bg-amber-500/10 text-amber-400 border border-amber-500/20" 
                          : "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                      }`}>
                        {tx.tier}
                      </span>
                    </td>
                    <td className="py-4 px-4 text-right font-mono font-semibold text-white">
                      ${tx.amount.toFixed(2)}
                      <span className="text-[10px] text-slate-500 block">({tx.country} PPP)</span>
                    </td>
                    <td className="py-4 px-4 text-slate-400">{tx.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  );
}

// Componentes internos de soporte
interface MetricCardProps {
  title: string;
  value: string;
  change: string;
  description: string;
  icon: React.ReactNode;
}

function MetricCard({ title, value, change, description, icon }: MetricCardProps) {
  return (
    <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 space-y-4 hover:border-slate-700/60 transition-colors">
      <div className="flex justify-between items-start">
        <span className="text-xs font-semibold text-slate-400 tracking-wide uppercase">{title}</span>
        <div className="p-2 bg-slate-850 rounded-lg border border-slate-850">
          {icon}
        </div>
      </div>
      <div>
        <p className="text-2xl font-bold text-white tracking-tight">{value}</p>
        <div className="flex items-center gap-1.5 mt-1">
          <span className="text-[10px] font-semibold text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded">
            {change}
          </span>
          <span className="text-[10px] text-slate-500">{description}</span>
        </div>
      </div>
    </div>
  );
}

interface TierProgressProps {
  label: string;
  count: number;
  percentage: number;
  color: string;
  value: string;
}

function TierProgress({ label, count, percentage, color, value }: TierProgressProps) {
  return (
    <div className="space-y-2">
      <div className="flex justify-between text-xs text-slate-300">
        <span>{label}</span>
        <span className="font-semibold text-white">{count} ({percentage}%)</span>
      </div>
      <div className="w-full bg-slate-850 h-1.5 rounded-full overflow-hidden">
        <div className={`${color} h-full rounded-full`} style={{ width: `${percentage}%` }} />
      </div>
      <div className="flex justify-between text-[10px] text-slate-500 font-mono">
        <span>Aporte</span>
        <span>{value}/mes</span>
      </div>
    </div>
  );
}
