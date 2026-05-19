"use client";

import React from 'react';
import ReactFlow, {
    Background,
    Controls,
    Node,
    Edge,
    Handle,
    Position,
    NodeProps,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { User, Activity } from 'lucide-react';

// Custom Node Component
const ParticipantNode = ({ data, selected }: NodeProps) => {
    return (
        <div className={`px-4 py-3 rounded-2xl bg-slate-900 border-2 transition-all duration-300 ${
            selected ? 'border-emerald-500 shadow-[0_0_20px_rgba(16,185,129,0.3)] scale-110' : 'border-slate-800 shadow-xl'
        }`}>
            <Handle type="target" position={Position.Top} className="opacity-0" />
            <div className="flex items-center gap-3">
                <div className={`p-2 rounded-xl ${data.is_hub ? 'bg-amber-500/20 text-amber-500' : 'bg-slate-800 text-slate-400'}`}>
                    <User className="w-4 h-4" />
                </div>
                <div>
                    <div className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-0.5">Participante</div>
                    <div className="text-sm font-bold text-white leading-tight">{data.label}</div>
                    {data.is_hub && (
                        <div className="flex items-center gap-1 mt-1">
                            <Activity className="w-3 h-3 text-amber-500" />
                            <span className="text-[9px] font-bold text-amber-500 uppercase">Nodo Crítico</span>
                        </div>
                    )}
                </div>
            </div>
            <Handle type="source" position={Position.Bottom} className="opacity-0" />
        </div>
    );
};

const nodeTypes = {
    participant: ParticipantNode,
};

interface ExchangeNetworkGraphProps {
    nodes: Node[];
    edges: Edge[];
    onNodeClick?: (event: React.MouseEvent, node: Node) => void;
}

export default function ExchangeNetworkGraph({ nodes, edges, onNodeClick }: ExchangeNetworkGraphProps) {
    const proOptions = { hideAttribution: true };

    const defaultEdgeOptions = {
        animated: true,
        style: { stroke: 'rgba(148, 163, 184, 0.2)', strokeWidth: 2 },
    };

    return (
        <div className="w-full h-full bg-slate-950 rounded-3xl overflow-hidden border border-slate-800 relative group">
            <ReactFlow
                nodes={nodes}
                edges={edges}
                nodeTypes={nodeTypes}
                onNodeClick={onNodeClick}
                proOptions={proOptions}
                defaultEdgeOptions={defaultEdgeOptions}
                fitView
                className="bg-slate-950"
            >
                <Background color="#1e293b" gap={20} size={1} />
                <Controls className="bg-slate-900 border-slate-800 fill-slate-400" />
            </ReactFlow>
            
            {/* Legend Overlay */}
            <div className="absolute top-6 left-6 p-4 bg-slate-900/80 backdrop-blur-md border border-slate-800 rounded-2xl pointer-events-none z-10">
                <h4 className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-3">Leyenda de Red</h4>
                <div className="space-y-2">
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-slate-400" />
                        <span className="text-[10px] text-slate-400 font-bold uppercase">Participante Estándar</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-amber-500" />
                        <span className="text-[10px] text-amber-500 font-bold uppercase">Nodo de Alto Flujo</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
