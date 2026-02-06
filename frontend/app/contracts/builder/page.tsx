'use client';

import React, { useState, useCallback } from 'react';
import ReactFlow, {
    Controls,
    Background,
    applyNodeChanges,
    applyEdgeChanges,
    addEdge,
    Node,
    Edge,
    OnNodesChange,
    OnEdgesChange,
    OnConnect,
} from 'reactflow';
import 'reactflow/dist/style.css';

const initialNodes: Node[] = [
    {
        id: '1',
        type: 'input',
        data: { label: 'Inicio Contrato' },
        position: { x: 250, y: 5 },
        style: { background: '#f0fdf4', border: '1px solid #4ade80', borderRadius: '10px', padding: '10px' }
    },
];

const initialEdges: Edge[] = [];

export default function ContractBuilder() {
    const [nodes, setNodes] = useState<Node[]>(initialNodes);
    const [edges, setEdges] = useState<Edge[]>(initialEdges);

    const onNodesChange: OnNodesChange = useCallback(
        (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
        [],
    );
    const onEdgesChange: OnEdgesChange = useCallback(
        (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
        [],
    );
    const onConnect: OnConnect = useCallback(
        (params) => setEdges((eds) => addEdge(params, eds)),
        [],
    );

    return (
        <div className="h-screen w-screen flex flex-col bg-slate-50">
            <header className="h-14 border-b bg-white/70 backdrop-blur-md flex items-center px-6 justify-between">
                <h1 className="font-bold text-lg text-slate-800">MaxoContracts Builder</h1>
                <div className="flex gap-4 items-center">
                    <span className="text-sm font-semibold text-emerald-600 bg-emerald-100 px-3 py-1 rounded-full">
                        γ: 1.0 (Neutro)
                    </span>
                    <button className="bg-slate-900 text-white px-4 py-2 rounded-lg text-sm hover:bg-slate-800">
                        Simular
                    </button>
                </div>
            </header>

            <div className="flex-1 flex">
                {/* Sidebar */}
                <aside className="w-64 border-r bg-white p-4 flex flex-col gap-4">
                    <div className="font-semibold text-slate-500 text-sm uppercase">Bloques</div>

                    <div className="p-3 bg-slate-100 rounded border border-slate-200 cursor-grab hover:bg-slate-200">
                        Condición
                    </div>
                    <div className="p-3 bg-slate-100 rounded border border-slate-200 cursor-grab hover:bg-slate-200">
                        Acción
                    </div>
                    <div className="p-3 bg-slate-100 rounded border border-slate-200 cursor-grab hover:bg-slate-200">
                        Oráculo
                    </div>
                </aside>

                {/* Canvas */}
                <div className="flex-1 h-full">
                    <ReactFlow
                        nodes={nodes}
                        edges={edges}
                        onNodesChange={onNodesChange}
                        onEdgesChange={onEdgesChange}
                        onConnect={onConnect}
                        fitView
                    >
                        <Background color="#cbd5e1" gap={16} />
                        <Controls />
                    </ReactFlow>
                </div>
            </div>
        </div>
    );
}
