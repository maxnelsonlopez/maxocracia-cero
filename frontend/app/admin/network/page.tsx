"use client";

import React, { useEffect, useState, useCallback } from "react";
import { Node, Edge } from "reactflow";
import { 
    Search, 
    Filter, 
    Info, 
    X, 
    ExternalLink, 
    Phone, 
    Mail, 
    MapPin,
    AlertCircle
} from "lucide-react";
import ExchangeNetworkGraph from "@/app/components/admin/ExchangeNetworkGraph";
import { motion, AnimatePresence } from "framer-motion";

export default function NetworkPage() {
    const [nodes, setNodes] = useState<Node[]>([]);
    const [edges, setEdges] = useState<Edge[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedNode, setSelectedNode] = useState<Node | null>(null);
    const [participantDetails, setParticipantDetails] = useState<any>(null);

    const fetchNetwork = useCallback(async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem("mc_token");
            const res = await fetch("/forms/dashboard/network", {
                headers: { "Authorization": `Bearer ${token}` }
            });

            if (!res.ok) throw new Error("Error al obtener la red");

            const data = await res.json();
            
            // Distribute nodes in a circle initially if they don't have positions
            const distributedNodes = data.nodes.map((node: Node, i: number) => ({
                ...node,
                position: {
                    x: Math.cos(i * (2 * Math.PI / data.nodes.length)) * 400,
                    y: Math.sin(i * (2 * Math.PI / data.nodes.length)) * 400,
                }
            }));

            setNodes(distributedNodes);
            setEdges(data.edges);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Error desconocido");
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchNetwork();
    }, [fetchNetwork]);

    const handleNodeClick = async (_: React.MouseEvent, node: Node) => {
        setSelectedNode(node);
        try {
            const token = localStorage.getItem("mc_token");
            const res = await fetch(`/forms/participants/${node.id}`, {
                headers: { "Authorization": `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                setParticipantDetails(data);
            }
        } catch (err) {
            console.error("Error fetching participant details:", err);
        }
    };

    if (error) return (
        <div className="flex flex-col items-center justify-center h-[calc(100vh-200px)] text-rose-500 gap-4">
            <AlertCircle className="w-12 h-12" />
            <div className="text-center">
                <h3 className="font-bold text-xl uppercase tracking-tighter">Error de Red</h3>
                <p className="opacity-70">{error}</p>
            </div>
            <button 
                onClick={fetchNetwork}
                className="mt-4 px-6 py-2 bg-rose-500/10 border border-rose-500/20 rounded-xl hover:bg-rose-500/20 transition-colors uppercase font-black text-xs"
            >
                Reintentar
            </button>
        </div>
    );

    return (
        <div className="h-[calc(100vh-160px)] flex gap-6 relative overflow-hidden">
            {/* Main Graph Area */}
            <div className="flex-1 relative">
                <div className="absolute top-6 left-6 right-6 flex justify-between z-20 pointer-events-none">
                    <div className="flex gap-3 pointer-events-auto">
                        <div className="relative group">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                            <input 
                                type="text" 
                                placeholder="Buscar participante..." 
                                className="pl-10 pr-4 py-2 bg-slate-900/80 backdrop-blur-xl border border-slate-800 rounded-xl text-sm text-white focus:outline-none focus:border-emerald-500/50 w-64 transition-all"
                            />
                        </div>
                        <button className="p-2.5 bg-slate-900/80 backdrop-blur-xl border border-slate-800 rounded-xl text-slate-400 hover:text-white transition-colors">
                            <Filter className="w-4 h-4" />
                        </button>
                    </div>
                </div>

                {loading ? (
                    <div className="w-full h-full bg-slate-950 rounded-3xl border border-slate-800 flex items-center justify-center">
                        <div className="flex flex-col items-center gap-4">
                            <div className="w-12 h-12 border-4 border-emerald-500/20 border-t-emerald-500 rounded-full animate-spin" />
                            <p className="text-xs text-slate-500 font-bold uppercase tracking-widest">Sincronizando Red...</p>
                        </div>
                    </div>
                ) : (
                    <ExchangeNetworkGraph 
                        nodes={nodes} 
                        edges={edges} 
                        onNodeClick={handleNodeClick}
                    />
                )}
            </div>

            {/* Sidebar Details Panel */}
            <AnimatePresence>
                {selectedNode && (
                    <motion.aside
                        initial={{ x: 400, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        exit={{ x: 400, opacity: 0 }}
                        className="w-96 bg-slate-900/50 backdrop-blur-2xl border border-slate-800 rounded-3xl overflow-hidden flex flex-col z-30"
                    >
                        <div className="p-6 border-b border-slate-800 flex items-center justify-between">
                            <h3 className="font-bold text-white flex items-center gap-2">
                                <Info className="w-4 h-4 text-emerald-500" />
                                Detalles del Nodo
                            </h3>
                            <button 
                                onClick={() => setSelectedNode(null)}
                                className="p-1.5 hover:bg-slate-800 rounded-lg text-slate-500 transition-colors"
                            >
                                <X className="w-4 h-4" />
                            </button>
                        </div>

                        <div className="flex-1 overflow-y-auto p-6 space-y-8 custom-scrollbar">
                            {participantDetails ? (
                                <>
                                    {/* Header */}
                                    <div>
                                        <h2 className="text-2xl font-bold text-white mb-1">{participantDetails.name}</h2>
                                        <div className="flex items-center gap-2 text-xs text-slate-400 font-medium">
                                            <MapPin className="w-3 h-3" />
                                            {participantDetails.neighborhood}, {participantDetails.city}
                                        </div>
                                    </div>

                                    {/* Contact Info */}
                                    <div className="space-y-3">
                                        <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-800/30 border border-slate-700/30">
                                            <Mail className="w-4 h-4 text-blue-400" />
                                            <span className="text-xs text-slate-300 truncate">{participantDetails.email}</span>
                                        </div>
                                        <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-800/30 border border-slate-700/30">
                                            <Phone className="w-4 h-4 text-emerald-400" />
                                            <span className="text-xs text-slate-300">{participantDetails.phone_whatsapp}</span>
                                        </div>
                                    </div>

                                    {/* Offer / Need Summary */}
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="p-4 rounded-2xl bg-emerald-500/5 border border-emerald-500/10">
                                            <div className="text-[10px] font-black text-emerald-500 uppercase mb-2">Ofrece</div>
                                            <div className="text-xs text-slate-300 line-clamp-3">{participantDetails.offer_description}</div>
                                        </div>
                                        <div className="p-4 rounded-2xl bg-rose-500/5 border border-rose-500/10">
                                            <div className="text-[10px] font-black text-rose-500 uppercase mb-2">Necesita</div>
                                            <div className="text-xs text-slate-300 line-clamp-3">{participantDetails.need_description}</div>
                                        </div>
                                    </div>

                                    {/* Metrics */}
                                    <div>
                                        <h4 className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-4">Métricas de Coherencia</h4>
                                        <div className="space-y-4">
                                            <div className="flex justify-between items-end">
                                                <span className="text-xs text-slate-400">Impacto en Red</span>
                                                <span className="text-sm font-bold text-white">8.4/10</span>
                                            </div>
                                            <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                                                <div className="h-full bg-emerald-500 w-[84%]" />
                                            </div>
                                        </div>
                                    </div>
                                </>
                            ) : (
                                <div className="flex flex-col items-center justify-center h-full gap-4 text-slate-600">
                                    <div className="w-8 h-8 border-2 border-slate-800 border-t-slate-600 rounded-full animate-spin" />
                                    <p className="text-[10px] font-bold uppercase tracking-widest">Cargando perfil...</p>
                                </div>
                            )}
                        </div>

                        <div className="p-6 border-t border-slate-800">
                            <button className="w-full py-3 bg-emerald-500 text-slate-950 rounded-xl font-bold text-sm hover:bg-emerald-400 transition-all active:scale-95 flex items-center justify-center gap-2">
                                Ver Perfil Completo
                                <ExternalLink className="w-4 h-4" />
                            </button>
                        </div>
                    </motion.aside>
                )}
            </AnimatePresence>
        </div>
    );
}
