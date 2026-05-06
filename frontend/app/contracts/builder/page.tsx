'use client';

import React, { useState, useCallback, useRef } from 'react';
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
    Panel,
} from 'reactflow';
import 'reactflow/dist/style.css';

import { ActionNode, ConditionNode, OracleNode, SDVNode, ReciprocityNode } from './components/CustomNodes';

// Definición de tipos de nodos personalizados
const nodeTypes = {
    action: ActionNode,
    condition: ConditionNode,
    oracle: OracleNode,
    sdv: SDVNode,
    reciprocity: ReciprocityNode,
};

// Tipos de nodos iniciales y básicos
const initialNodes: Node[] = [
    {
        id: 'start-node',
        type: 'input',
        data: { label: 'Inicio Contrato' },
        position: { x: 350, y: 5 },
        style: { 
            background: 'rgba(255, 255, 255, 0.8)', 
            backdropFilter: 'blur(10px)',
            border: '2px solid #10b981', 
            borderRadius: '12px', 
            padding: '12px',
            color: '#064e3b',
            fontWeight: 'bold',
            boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'
        }
    },
];

const initialEdges: Edge[] = [];

// Identificador único para nuevos nodos
let id = 0;
const getId = () => `node_${id++}`;

export default function ContractBuilder() {
    const reactFlowWrapper = useRef<HTMLDivElement>(null);
    const [nodes, setNodes] = useState<Node[]>(initialNodes);
    const [edges, setEdges] = useState<Edge[]>(initialEdges);
    const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);

    const onNodesChange: OnNodesChange = useCallback(
        (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
        [],
    );
    const onEdgesChange: OnEdgesChange = useCallback(
        (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
        [],
    );
    const onConnect: OnConnect = useCallback(
        (params) => setEdges((eds) => addEdge({ ...params, animated: true, style: { stroke: '#10b981' } }, eds)),
        [],
    );

    const onDragOver = useCallback((event: React.DragEvent) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'move';
    }, []);

    const onDrop = useCallback(
        (event: React.DragEvent) => {
            event.preventDefault();

            if (!reactFlowWrapper.current || !reactFlowInstance) return;

            const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
            const type = event.dataTransfer.getData('application/reactflow');

            // Verificar si el tipo es válido
            if (typeof type === 'undefined' || !type) {
                return;
            }

            const position = reactFlowInstance.project({
                x: event.clientX - reactFlowBounds.left,
                y: event.clientY - reactFlowBounds.top,
            });

            const newNode = {
                id: getId(),
                type,
                position,
                data: { label: `${type.charAt(0).toUpperCase() + type.slice(1)} Block` },
                style: { 
                    background: 'white', 
                    border: '1px solid #cbd5e1', 
                    borderRadius: '8px', 
                    padding: '10px',
                    boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1)'
                }
            };

            setNodes((nds) => nds.concat(newNode));
        },
        [reactFlowInstance]
    );

    const onDragStart = (event: React.DragEvent, nodeType: string) => {
        event.dataTransfer.setData('application/reactflow', nodeType);
        event.dataTransfer.effectAllowed = 'move';
    };

    const onSave = async () => {
        console.log('Enviando para validación axiomática...', { nodes, edges });
        
        try {
            const response = await fetch('/contracts/validate_graph', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}` // Asumiendo que el token está en localStorage
                },
                body: JSON.stringify({ nodes, edges })
            });

            const result = await response.json();

            if (result.valid) {
                alert('✅ Contrato Éticamente Válido. Todos los axiomas se cumplen.');
            } else {
                const errors = result.results
                    .filter((r: any) => !r.is_valid)
                    .map((r: any) => `• ${r.axiom}: ${r.message}`)
                    .join('\n');
                alert(`⚠️ Violación Axiomática Detectada:\n\n${errors}`);
            }
        } catch (error) {
            console.error('Error en la validación:', error);
            alert('Error al conectar con el Oráculo Axiomático. Revisa la consola.');
        }
    };

    return (
        <div className="h-screen w-screen flex flex-col bg-slate-50 overflow-hidden">
            <header className="h-16 border-b bg-white/80 backdrop-blur-md flex items-center px-8 justify-between z-10">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center text-white font-bold">M</div>
                    <h1 className="font-bold text-xl text-slate-800 tracking-tight">MaxoContracts Builder</h1>
                </div>
                <div className="flex gap-4 items-center">
                    <div className="flex flex-col items-end">
                        <span className="text-[10px] uppercase font-bold text-slate-400 tracking-widest">Estado Ético</span>
                        <span className="text-sm font-bold text-emerald-600 bg-emerald-50 px-3 py-0.5 rounded-full border border-emerald-100">
                            γ: 1.0 (Coherente)
                        </span>
                    </div>
                    <button 
                        onClick={onSave}
                        className="bg-slate-900 text-white px-6 py-2.5 rounded-xl font-semibold text-sm hover:bg-slate-800 transition-all active:scale-95 shadow-lg shadow-slate-200"
                    >
                        Validar y Guardar
                    </button>
                </div>
            </header>

            <div className="flex-1 flex overflow-hidden" ref={reactFlowWrapper}>
                {/* Sidebar */}
                <aside className="w-72 border-r bg-white p-6 flex flex-col gap-6 z-10 shadow-xl shadow-slate-100">
                    <div>
                        <h2 className="font-bold text-slate-800 mb-1">Biblioteca de Bloques</h2>
                        <p className="text-xs text-slate-400">Arrastra los componentes para diseñar tu contrato.</p>
                    </div>

                    <div className="flex flex-col gap-3">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Lógica Core</div>
                        
                        <div 
                            className="p-4 bg-white rounded-xl border-2 border-slate-100 cursor-grab hover:border-emerald-200 hover:bg-emerald-50/30 transition-all flex items-center gap-3 group"
                            onDragStart={(event) => onDragStart(event, 'condition')}
                            draggable
                        >
                            <div className="w-2 h-2 rounded-full bg-amber-400 group-hover:scale-125 transition-transform"></div>
                            <span className="font-medium text-slate-700">Condición (IF)</span>
                        </div>

                        <div 
                            className="p-4 bg-white rounded-xl border-2 border-slate-100 cursor-grab hover:border-emerald-200 hover:bg-emerald-50/30 transition-all flex items-center gap-3 group"
                            onDragStart={(event) => onDragStart(event, 'action')}
                            draggable
                        >
                            <div className="w-2 h-2 rounded-full bg-blue-400 group-hover:scale-125 transition-transform"></div>
                            <span className="font-medium text-slate-700">Acción (DO)</span>
                        </div>

                        <div 
                            className="p-4 bg-white rounded-xl border-2 border-slate-100 cursor-grab hover:border-emerald-200 hover:bg-emerald-50/30 transition-all flex items-center gap-3 group"
                            onDragStart={(event) => onDragStart(event, 'oracle')}
                            draggable
                        >
                            <div className="w-2 h-2 rounded-full bg-purple-400 group-hover:scale-125 transition-transform"></div>
                            <span className="font-medium text-slate-700">Oráculo (VERDICT)</span>
                        </div>

                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-4 mb-1">Protección Axiomática</div>

                        <div 
                            className="p-4 bg-white rounded-xl border-2 border-slate-100 cursor-grab hover:border-emerald-200 hover:bg-emerald-50/30 transition-all flex items-center gap-3 group"
                            onDragStart={(event) => onDragStart(event, 'sdv')}
                            draggable
                        >
                            <div className="w-2 h-2 rounded-full bg-emerald-400 group-hover:scale-125 transition-transform"></div>
                            <span className="font-medium text-slate-700">Suelo Dignidad (SDV)</span>
                        </div>

                        <div 
                            className="p-4 bg-white rounded-xl border-2 border-slate-100 cursor-grab hover:border-emerald-200 hover:bg-emerald-50/30 transition-all flex items-center gap-3 group"
                            onDragStart={(event) => onDragStart(event, 'reciprocity')}
                            draggable
                        >
                            <div className="w-2 h-2 rounded-full bg-rose-400 group-hover:scale-125 transition-transform"></div>
                            <span className="font-medium text-slate-700">Reciprocidad</span>
                        </div>
                    </div>

                    <div className="mt-auto p-4 bg-slate-50 rounded-2xl border border-slate-100">
                        <h3 className="text-xs font-bold text-slate-600 mb-2">Tip: Coherencia Axiomática</h3>
                        <p className="text-[11px] text-slate-500 leading-relaxed">
                            Asegúrate de que cada acción tenga una reciprocidad clara para mantener el balance γ.
                        </p>
                    </div>
                </aside>

                {/* Canvas */}
                <div className="flex-1 h-full relative">
                    <ReactFlow
                        nodes={nodes}
                        edges={edges}
                        onNodesChange={onNodesChange}
                        onEdgesChange={onEdgesChange}
                        onConnect={onConnect}
                        onInit={setReactFlowInstance}
                        onDrop={onDrop}
                        onDragOver={onDragOver}
                        nodeTypes={nodeTypes}
                        fitView
                        className="bg-slate-50"
                    >
                        <Background color="#e2e8f0" gap={20} size={1} />
                        <Controls />
                        <Panel position="bottom-right" className="bg-white/80 backdrop-blur-md p-3 rounded-xl border border-slate-200 shadow-sm mb-4 mr-4">
                            <div className="text-[10px] font-bold text-slate-400 uppercase mb-1">Coordenadas del Contrato</div>
                            <div className="text-xs font-mono text-slate-600">Nodes: {nodes.length} | Edges: {edges.length}</div>
                        </Panel>
                    </ReactFlow>
                </div>
            </div>
        </div>
    );
}

