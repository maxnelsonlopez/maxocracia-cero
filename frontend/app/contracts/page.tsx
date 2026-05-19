"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { 
  FileText, 
  Plus, 
  Search, 
  Filter, 
  ChevronRight, 
  Clock, 
  CheckCircle2, 
  AlertCircle,
  Zap,
  Users
} from "lucide-react";
import { motion } from "framer-motion";
import { apiFetch } from "../lib/api";

interface Contract {
  contract_id: string;
  state: string;
  participants: number;
  terms: number;
}

export default function ContractsPage() {
  const [contracts, setContracts] = useState<Contract[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    async function fetchContracts() {
      try {
        const res = await apiFetch("/contracts/");

        if (!res.ok) throw new Error("Error al cargar contratos");
        const data = await res.json();
        setContracts(data.contracts || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Error desconocido");
      } finally {
        setLoading(false);
      }
    }

    fetchContracts();
  }, []);

  const filteredContracts = contracts.filter(c => 
    c.contract_id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusColor = (state: string) => {
    switch (state.toLowerCase()) {
      case 'active': return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
      case 'draft': return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
      case 'pending': return 'text-blue-400 bg-blue-500/10 border-blue-500/20';
      case 'retracted': return 'text-rose-400 bg-rose-500/10 border-rose-500/20';
      default: return 'text-slate-400 bg-slate-500/10 border-slate-500/20';
    }
  };

  const getStatusIcon = (state: string) => {
    switch (state.toLowerCase()) {
      case 'active': return CheckCircle2;
      case 'draft': return Clock;
      case 'pending': return Zap;
      case 'retracted': return AlertCircle;
      default: return FileText;
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="space-y-2">
          <h1 className="text-4xl font-black tracking-tight text-white flex items-center gap-3">
            <FileText className="w-10 h-10 text-emerald-500" />
            MaxoContracts
          </h1>
          <p className="text-slate-400 max-w-2xl leading-relaxed">
            Explora y gestiona los contratos inteligentes éticos de la Cohorte Cero. 
            Transparencia axiomática para una economía vital.
          </p>
        </div>
        
        <Link 
          href="/contracts/builder" 
          className="flex items-center justify-center gap-2 px-6 py-3 rounded-2xl bg-emerald-500 text-white font-bold hover:bg-emerald-600 transition-all shadow-xl shadow-emerald-500/20 active:scale-95"
        >
          <Plus className="w-5 h-5" />
          Nuevo Contrato
        </Link>
      </div>

      {/* Stats Quick View */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass p-6 rounded-3xl border border-slate-800 space-y-2">
          <span className="text-[10px] font-black uppercase tracking-widest text-slate-500">Total Activos</span>
          <div className="flex items-end gap-2">
            <span className="text-3xl font-bold text-white">{contracts.filter(c => c.state === 'active').length}</span>
            <span className="text-emerald-500 text-xs font-bold mb-1">Coherentes</span>
          </div>
        </div>
        <div className="glass p-6 rounded-3xl border border-slate-800 space-y-2">
          <span className="text-[10px] font-black uppercase tracking-widest text-slate-500">En Borrador</span>
          <div className="flex items-end gap-2">
            <span className="text-3xl font-bold text-white">{contracts.filter(c => c.state === 'draft').length}</span>
            <span className="text-amber-500 text-xs font-bold mb-1">Diseñando</span>
          </div>
        </div>
        <div className="glass p-6 rounded-3xl border border-slate-800 space-y-2">
          <span className="text-[10px] font-black uppercase tracking-widest text-slate-500">Participantes</span>
          <div className="flex items-end gap-2">
            <span className="text-3xl font-bold text-white">{contracts.reduce((acc, c) => acc + c.participants, 0)}</span>
            <span className="text-blue-500 text-xs font-bold mb-1">Impactados</span>
          </div>
        </div>
      </div>

      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row gap-4 items-center">
        <div className="relative flex-1 w-full">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
          <input 
            type="text" 
            placeholder="Buscar por ID de contrato..."
            className="w-full bg-slate-900/50 border border-slate-800 rounded-2xl py-3 pl-12 pr-4 text-white placeholder:text-slate-600 focus:outline-none focus:border-emerald-500/50 transition-all"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <button className="flex items-center gap-2 px-6 py-3 rounded-2xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white transition-all">
          <Filter className="w-4 h-4" />
          Filtros
        </button>
      </div>

      {/* Contracts List */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
          {[1, 2, 3, 4, 5, 6].map(i => (
            <div key={i} className="h-48 bg-slate-900/50 rounded-3xl border border-slate-800" />
          ))}
        </div>
      ) : error ? (
        <div className="p-8 rounded-3xl bg-rose-500/10 border border-rose-500/20 text-center space-y-4">
          <AlertCircle className="w-12 h-12 text-rose-500 mx-auto" />
          <div className="space-y-1">
            <h3 className="text-white font-bold text-xl">Error de Conexión</h3>
            <p className="text-rose-400 text-sm">{error}</p>
          </div>
          <button 
            onClick={() => window.location.reload()}
            className="px-6 py-2 bg-rose-500 text-white rounded-xl text-sm font-bold"
          >
            Reintentar
          </button>
        </div>
      ) : filteredContracts.length === 0 ? (
        <div className="text-center py-20 space-y-6">
          <div className="w-20 h-20 bg-slate-900 rounded-full flex items-center justify-center mx-auto border border-slate-800">
            <FileText className="w-8 h-8 text-slate-700" />
          </div>
          <div className="space-y-2">
            <h3 className="text-white font-bold text-xl">No se encontraron contratos</h3>
            <p className="text-slate-500 text-sm max-w-xs mx-auto">
              Empieza por crear tu primer contrato inteligente usando el Constructor Visual.
            </p>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredContracts.map((contract) => {
            const StatusIcon = getStatusIcon(contract.state);
            return (
              <motion.div
                key={contract.contract_id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                whileHover={{ y: -5 }}
                className="group relative glass p-6 rounded-3xl border border-slate-800 hover:border-emerald-500/30 transition-all cursor-pointer"
              >
                <div className="flex justify-between items-start mb-4">
                  <div className={`p-3 rounded-2xl ${getStatusColor(contract.state)}`}>
                    <StatusIcon className="w-6 h-6" />
                  </div>
                  <span className={`text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-full border ${getStatusColor(contract.state)}`}>
                    {contract.state}
                  </span>
                </div>

                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-bold text-white group-hover:text-emerald-400 transition-colors truncate">
                      {contract.contract_id}
                    </h3>
                    <p className="text-xs text-slate-500 uppercase tracking-widest font-bold">MaxoContract v1.0</p>
                  </div>

                  <div className="grid grid-cols-2 gap-4 pt-4 border-t border-slate-800/50">
                    <div className="flex items-center gap-2">
                      <Users className="w-4 h-4 text-slate-600" />
                      <span className="text-xs text-slate-400 font-medium">{contract.participants} Participantes</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Zap className="w-4 h-4 text-slate-600" />
                      <span className="text-xs text-slate-400 font-medium">{contract.terms} Bloques</span>
                    </div>
                  </div>
                </div>

                <div className="absolute bottom-6 right-6 opacity-0 group-hover:opacity-100 transition-all translate-x-2 group-hover:translate-x-0">
                  <ChevronRight className="w-5 h-5 text-emerald-500" />
                </div>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
}
