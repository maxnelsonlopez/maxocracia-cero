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
  Users,
  Info,
  ShieldAlert,
  Bot,
  Landmark,
  Leaf
} from "lucide-react";
import { motion } from "framer-motion";
import { apiFetch } from "../lib/api";

interface Contract {
  contract_id: string;
  state: string;
  participants: number;
  terms: number;
}

interface CohortParty {
  party_id: string;
  party_type: string;
  display_name: string;
  wellness: number;
  contracts_total: number;
  contracts_active: number;
  contracts_pending: number;
  terms_sealed: number;
}

interface CohortOverview {
  parties: CohortParty[];
  totals: {
    parties: number;
    total_contracts: number;
    active: number;
    pending: number;
    terms_sealed: number;
  };
}

export default function ContractsPage() {
  const [contracts, setContracts] = useState<Contract[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [cohort, setCohort] = useState<CohortOverview | null>(null);

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

    async function fetchCohort() {
      try {
        const res = await apiFetch("/contracts/cohort");
        if (res.ok) {
          setCohort(await res.json());
        }
      } catch (err) {
        console.error("Error al cargar la cohorte:", err);
      }
    }

    fetchContracts();
    fetchCohort();
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
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8 text-slate-200">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="space-y-2">
          <h1 className="text-4xl font-black tracking-tight text-white flex items-center gap-3">
            <FileText className="w-10 h-10 text-emerald-500" />
            MaxoContracts
          </h1>
          <p className="text-slate-450 max-w-2xl leading-relaxed text-sm">
            Explora y gestiona los contratos inteligentes éticos de la Cohorte Cero. 
            Transparencia axiomática y monitoreo vital P2P en tiempo real.
          </p>
        </div>
        
        <div className="flex flex-col sm:flex-row gap-3">
          <Link 
            href="/contracts/negotiate" 
            className="flex items-center justify-center gap-2 px-6 py-3 rounded-2xl bg-violet-600 text-white font-black hover:bg-violet-500 transition-all shadow-xl shadow-violet-600/20 active:scale-95 text-sm"
          >
            <Bot className="w-5 h-5" />
            Negociar con el Oráculo
          </Link>
          <Link 
            href="/contracts/builder" 
            className="flex items-center justify-center gap-2 px-6 py-3 rounded-2xl bg-emerald-500 text-slate-950 font-black hover:bg-emerald-400 transition-all shadow-xl shadow-emerald-500/20 active:scale-95 text-sm"
          >
            <Plus className="w-5 h-5 stroke-[3px]" />
            Nuevo Contrato Visual
          </Link>
        </div>
      </div>

      {/* BANNER COMPARATIVO: ¿Qué es un MaxoContract? */}
      <div className="glass p-6 rounded-3xl border border-slate-900 bg-slate-900/20 space-y-6">
        <div className="space-y-1">
          <span className="text-[10px] font-black uppercase tracking-widest text-emerald-400 flex items-center gap-1.5">
            <Info className="w-4 h-4" />
            Marco Conceptual e Histórico de la Cohorte Cero
          </span>
          <h2 className="text-xl font-extrabold text-white">¿Qué es un MaxoContract y en qué se diferencia?</h2>
          <p className="text-xs text-slate-400 max-w-4xl leading-relaxed">
            De acuerdo con el Capítulo 17 del libro, los acuerdos en la Cohorte Cero no se basan en la fe ciega ni en la coerción violenta del Estado, sino en el respeto mutuo a la dignidad y la supervisión algorítmica voluntaria de nuestro bienestar.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Tarjeta 1: Contrato Tradicional */}
          <div className="p-4 rounded-2xl bg-slate-950/40 border border-slate-950 space-y-2 text-xs text-slate-400">
            <span className="font-extrabold text-rose-400 uppercase text-[10px] block">Contratos Tradicionales (Civiles/Comerciales)</span>
            <p className="leading-relaxed">
              <strong>Mecanismo:</strong> Dependen de una coerción judicial ex-post (policía, tribunales, abogados).
            </p>
            <p className="leading-relaxed">
              <strong>Falta de Humanidad:</strong> Son estáticos y ciegos al bienestar de las partes. No importa si ejecutar el contrato te desgasta físicamente o te arruina la salud; la ley exige su cumplimiento a toda costa.
            </p>
          </div>

          {/* Tarjeta 2: Smart Contract */}
          <div className="p-4 rounded-2xl bg-slate-950/40 border border-slate-950 space-y-2 text-xs text-slate-400">
            <span className="font-extrabold text-amber-400 uppercase text-[10px] block">Smart Contracts (Blockchain / Web3)</span>
            <p className="leading-relaxed">
              <strong>Mecanismo:</strong> Ejecución irrevocable y automatizada mediante código autoejecutable (&quot;Code is Law&quot;).
            </p>
            <p className="leading-relaxed">
              <strong>Ceguera Existencial:</strong> Son inmutables de forma absoluta. Carecen de empatía o noción de crisis vitales. Si una de las partes sufre un accidente o asimetría extrema, el código sigue ejecutando transferencias sin piedad.
            </p>
          </div>

          {/* Tarjeta 3: MaxoContract */}
          <div className="p-4 rounded-2xl bg-slate-900/40 border border-emerald-950 space-y-2 text-xs text-slate-350">
            <span className="font-extrabold text-emerald-400 uppercase text-[10px] block">MaxoContracts (Cohorte Cero)</span>
            <p className="leading-relaxed">
              <strong>Mecanismo:</strong> Autoejecución ética acoplada a oráculos y modelos de monitoreo de Bienestar P2P.
            </p>
            <p className="leading-relaxed">
              <strong>Centralidad Humana:</strong> Se rigen por dos invariantes: la Invariante INV1 (Bienestar No-Negativo, γ &ge; umbral) y la Invariante INV2 (Suelo de Dignidad Vital). Permiten la <strong>retractación ética unilateral</strong> si continuar con el acuerdo genera sufrimiento sistémico.
            </p>
          </div>
        </div>
      </div>

      {/* Stats Quick View */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass p-6 rounded-3xl border border-slate-900 bg-slate-900/30 space-y-2">
          <span className="text-[10px] font-black uppercase tracking-widest text-slate-500">Total Activos</span>
          <div className="flex items-end gap-2">
            <span className="text-3xl font-bold text-white">{contracts.filter(c => c.state === 'active').length}</span>
            <span className="text-emerald-500 text-xs font-bold mb-1">Coherentes</span>
          </div>
        </div>
        <div className="glass p-6 rounded-3xl border border-slate-900 bg-slate-900/30 space-y-2">
          <span className="text-[10px] font-black uppercase tracking-widest text-slate-500">En Borrador</span>
          <div className="flex items-end gap-2">
            <span className="text-3xl font-bold text-white">{contracts.filter(c => c.state === 'draft').length}</span>
            <span className="text-amber-500 text-xs font-bold mb-1">Diseñando</span>
          </div>
        </div>
        <div className="glass p-6 rounded-3xl border border-slate-900 bg-slate-900/30 space-y-2">
          <span className="text-[10px] font-black uppercase tracking-widest text-slate-500">Participantes</span>
          <div className="flex items-end gap-2">
            <span className="text-3xl font-bold text-white">{contracts.reduce((acc, c) => acc + c.participants, 0)}</span>
            <span className="text-blue-500 text-xs font-bold mb-1">Impactados</span>
          </div>
        </div>
      </div>

      {/* Cohorte de partes colectivas (ROADMAP Ext. 5: multi-contrato agregado) */}
      {cohort && cohort.parties.length > 0 && (
        <div className="glass p-6 rounded-3xl border border-slate-900 bg-slate-900/30 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <span className="text-[10px] font-black uppercase tracking-widest text-amber-400 flex items-center gap-1.5">
                <Landmark className="w-4 h-4" />
                Cohorte de Partes Colectivas
              </span>
              <h2 className="text-lg font-extrabold text-white mt-1">Vida económica agregada de las escalas</h2>
            </div>
            <div className="flex gap-4 text-center">
              <div>
                <span className="text-2xl font-black text-emerald-400 block">{cohort.totals.active}</span>
                <span className="text-[9px] uppercase tracking-widest text-slate-500 font-bold">Activos</span>
              </div>
              <div>
                <span className="text-2xl font-black text-amber-400 block">{cohort.totals.pending}</span>
                <span className="text-[9px] uppercase tracking-widest text-slate-500 font-bold">En firma</span>
              </div>
              <div>
                <span className="text-2xl font-black text-blue-400 block">{cohort.totals.terms_sealed}</span>
                <span className="text-[9px] uppercase tracking-widest text-slate-500 font-bold">Cláusulas selladas</span>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {cohort.parties.slice(0, 6).map((p) => (
              <Link
                key={p.party_id}
                href={`/contracts/?participant=${p.party_id}`}
                className="p-3.5 rounded-2xl bg-slate-950/50 border border-slate-900 hover:border-amber-500/30 transition-all flex items-center gap-3 group"
              >
                <div className="p-2 rounded-xl bg-amber-500/10 border border-amber-500/20 shrink-0">
                  {p.party_type === 'ecosystem' ? (
                    <Leaf className="w-4 h-4 text-emerald-400" />
                  ) : (
                    <Landmark className="w-4 h-4 text-amber-400" />
                  )}
                </div>
                <div className="min-w-0 flex-1">
                  <span className="block text-xs font-bold text-slate-200 truncate">{p.display_name}</span>
                  <span className="text-[9px] text-slate-500 font-mono">{p.party_id}</span>
                </div>
                <div className="text-right shrink-0">
                  <span className="block text-sm font-black text-emerald-400">{p.contracts_active}<span className="text-[9px] text-slate-500 font-normal"> act.</span></span>
                  <span className="text-[9px] text-slate-500 font-mono">γ {p.wellness.toFixed(2)}</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Toolbar & Legend */}
      <div className="space-y-4">
        {/* Leyenda de Estados */}
        <div className="bg-slate-950/60 border border-slate-900 p-4 rounded-2xl">
          <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-3">Leyenda Axiomática de Estados de un Contrato</span>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
            <div className="flex items-start gap-2.5">
              <div className="p-1.5 rounded-lg text-amber-400 bg-amber-500/10 border border-amber-500/20 mt-0.5 shrink-0">
                <Clock className="w-3.5 h-3.5" />
              </div>
              <div>
                <span className="font-bold text-slate-300 block text-[11px]">DRAFT (Borrador)</span>
                <span className="text-[10px] text-slate-500">La topología y cláusulas se están modelando. No vinculante aún.</span>
              </div>
            </div>

            <div className="flex items-start gap-2.5">
              <div className="p-1.5 rounded-lg text-blue-400 bg-blue-500/10 border border-blue-500/20 mt-0.5 shrink-0">
                <Zap className="w-3.5 h-3.5" />
              </div>
              <div>
                <span className="font-bold text-slate-300 block text-[11px]">PENDING (Firma)</span>
                <span className="text-[10px] text-slate-500">Bloques definidos. Esperando firmas correspondientes al peso ético.</span>
              </div>
            </div>

            <div className="flex items-start gap-2.5">
              <div className="p-1.5 rounded-lg text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 mt-0.5 shrink-0">
                <CheckCircle2 className="w-3.5 h-3.5" />
              </div>
              <div>
                <span className="font-bold text-slate-300 block text-[11px]">ACTIVE (Activo)</span>
                <span className="text-[10px] text-slate-500">En vigor. Vigilancia axiomática de bienestar activa en tiempo real.</span>
              </div>
            </div>

            <div className="flex items-start gap-2.5">
              <div className="p-1.5 rounded-lg text-rose-400 bg-rose-500/10 border border-rose-500/20 mt-0.5 shrink-0">
                <ShieldAlert className="w-3.5 h-3.5" />
              </div>
              <div>
                <span className="font-bold text-slate-300 block text-[11px]">RETRACTED (Retractado)</span>
                <span className="text-[10px] text-slate-500">Rescindido unilateralmente con aprobación del oráculo sintético.</span>
              </div>
            </div>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 items-center">
          <div className="relative flex-1 w-full">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-550" />
            <input 
              type="text" 
              placeholder="Buscar por ID de contrato..."
              className="w-full bg-slate-900/50 border border-slate-900 rounded-2xl py-3 pl-12 pr-4 text-white placeholder:text-slate-600 focus:outline-none focus:border-emerald-500/50 transition-all text-sm"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <button className="flex items-center gap-2 px-6 py-3 rounded-2xl bg-slate-900 border border-slate-900 text-slate-400 hover:text-white transition-all text-xs font-bold">
            <Filter className="w-4 h-4" />
            Filtros
          </button>
        </div>
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
              <Link href={`/contracts/${contract.contract_id}`} key={contract.contract_id} className="block">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  whileHover={{ y: -5 }}
                  className="group relative glass p-6 rounded-3xl border border-slate-800 hover:border-emerald-500/30 transition-all cursor-pointer h-full"
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
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
