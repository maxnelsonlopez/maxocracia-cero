'use client';

import React, { useState, useCallback, useRef, useEffect } from 'react';
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
    ReactFlowInstance,
} from 'reactflow';
import { apiFetch } from '../../lib/api';
import { useAuth } from '../../context/AuthContext';
import { useRouter } from 'next/navigation';
import { Info, HelpCircle, Save, Settings, ShieldAlert, Award, FileText, User } from 'lucide-react';
import 'reactflow/dist/style.css';

import { ActionNode, ConditionNode, OracleNode, SDVNode, ReciprocityNode } from './components/CustomNodes';

interface AxiomResult {
    axiom: string;
    is_valid: boolean;
    message: string;
}

interface UserProfile {
    id: number;
    email: string;
    name: string;
    alias?: string;
}

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
let idCounter = Date.now();
const getId = () => `node_${idCounter++}`;

export default function ContractBuilder() {
    const { user: currentUser } = useAuth();
    const router = useRouter();
    const reactFlowWrapper = useRef<HTMLDivElement>(null);
    const [nodes, setNodes] = useState<Node[]>(initialNodes);
    const [edges, setEdges] = useState<Edge[]>(initialEdges);
    const [reactFlowInstance, setReactFlowInstance] = useState<ReactFlowInstance | null>(null);

    // Nuevos estados
    const [duration, setDuration] = useState<number>(30);
    const [usersList, setUsersList] = useState<UserProfile[]>([]);
    const [selectedCoSigners, setSelectedCoSigners] = useState<number[]>([]);
    const [validationReport, setValidationReport] = useState<{
        valid: boolean;
        results: AxiomResult[];
        weight: number;
        ux_signature_type: string;
        total_vhv: { t: number; v: number; r: number };
    } | null>(null);

    // Opciones de parte obligada para los bloques (creador + co-firmantes)
    const ownerOptions = React.useMemo(() => [
        ...(currentUser ? [{ id: currentUser.id, label: `Yo (${currentUser.name.split(' ')[0]})` }] : []),
        ...usersList.map((u) => ({ id: u.id, label: u.name.split(' ')[0] })),
    ], [currentUser, usersList]);

    const injectOwners = useCallback((nds: Node[]) => {
        return nds.map((n) => ({ ...n, data: { ...n.data, owners: ownerOptions } }));
    }, [ownerOptions]);

    // Mantener la lista de partes disponible en los bloques al cambiar la selección
    useEffect(() => {
        setNodes((nds) => injectOwners(nds));
    }, [injectOwners]);

    // Cargador de plantillas predefinidas
    const loadTemplate = (templateName: string) => {
        if (nodes.length > 1) {
            const confirmLoad = window.confirm("¿Seguro que deseas cargar esta plantilla? Se reemplazará el lienzo actual.");
            if (!confirmLoad) return;
        }

        if (templateName === 'colab') {
            setDuration(15);
            const me = currentUser ? currentUser.id : 1;
            const firstCo = selectedCoSigners[0];
            setNodes(injectOwners([
                {
                    id: 'start-node',
                    type: 'input',
                    data: { label: 'Inicio Contrato' },
                    position: { x: 300, y: 10 },
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
                {
                    id: 'node_colab_do',
                    type: 'action',
                    position: { x: 260, y: 140 },
                    data: { label: 'Max ofrece 10 horas de trabajo', vhvCost: 10.0, ownerUserId: me }
                },
                {
                    id: 'node_colab_give',
                    type: 'reciprocity',
                    position: { x: 260, y: 300 },
                    data: {
                        label: 'La contraparte ofrece a cambio: [objeto / servicio / 10 horas de trabajo]',
                        ownerUserId: firstCo
                    }
                },
                {
                    id: 'node_colab_sdv',
                    type: 'sdv',
                    position: { x: 260, y: 460 },
                    data: { label: 'Suelo de Dignidad Vital (ninguna parte cae bajo sus mínimos)' }
                }
            ]));
            setEdges([
                { id: 'e1', source: 'start-node', target: 'node_colab_do', animated: true, style: { stroke: '#10b981' } },
                { id: 'e2', source: 'node_colab_do', target: 'node_colab_give', animated: true, style: { stroke: '#10b981' } },
                { id: 'e3', source: 'node_colab_give', target: 'node_colab_sdv', animated: true, style: { stroke: '#10b981' } }
            ]);
        } else if (templateName === 'support') {
            setDuration(30);
            setNodes(injectOwners([
                {
                    id: 'start-node',
                    type: 'input',
                    data: { label: 'Inicio Contrato' },
                    position: { x: 300, y: 10 },
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
                {
                    id: 'node_support_if',
                    type: 'condition',
                    position: { x: 260, y: 140 },
                    data: { label: 'Servidor web principal reporta caída > 2 horas continuas' }
                },
                {
                    id: 'node_support_oracle',
                    type: 'oracle',
                    position: { x: 260, y: 280 },
                    data: { label: 'Oráculo de API Monitoreo', oracleType: 'Híbrido (Consenso)' }
                },
                {
                    id: 'node_support_do',
                    type: 'action',
                    position: { x: 260, y: 400 },
                    data: { label: 'Soporte informático y restablecimiento de sistemas', vhvCost: 15.0 }
                },
                {
                    id: 'node_support_give',
                    type: 'reciprocity',
                    position: { x: 260, y: 550 },
                    data: { label: 'Devolución de 15 horas de consultoría de negocio equivalente' }
                }
            ]));
            setEdges([
                { id: 'e1', source: 'start-node', target: 'node_support_if', animated: true, style: { stroke: '#10b981' } },
                { id: 'e2', source: 'node_support_if', target: 'node_support_oracle', animated: true, style: { stroke: '#10b981' } },
                { id: 'e3', source: 'node_support_oracle', target: 'node_support_do', animated: true, style: { stroke: '#10b981' } },
                { id: 'e4', source: 'node_support_do', target: 'node_support_give', animated: true, style: { stroke: '#10b981' } }
            ]);
        } else if (templateName === 'loan') {
            setDuration(60);
            setNodes(injectOwners([
                {
                    id: 'start-node',
                    type: 'input',
                    data: { label: 'Inicio Contrato' },
                    position: { x: 300, y: 10 },
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
                {
                    id: 'node_loan_do',
                    type: 'action',
                    position: { x: 260, y: 140 },
                    data: { label: 'Transferir 40 horas de mentoría y tutoría de desarrollo de software', vhvCost: 40.0 }
                },
                {
                    id: 'node_loan_sdv',
                    type: 'sdv',
                    position: { x: 260, y: 310 },
                    data: { label: 'Suelo de Dignidad Vital (Límite semanal 5h máx)' }
                },
                {
                    id: 'node_loan_give',
                    type: 'reciprocity',
                    position: { x: 260, y: 440 },
                    data: { label: 'Devolver 40 horas de asistencia en proyectos de desarrollo' }
                }
            ]));
            setEdges([
                { id: 'e1', source: 'start-node', target: 'node_loan_do', animated: true, style: { stroke: '#10b981' } },
                { id: 'e2', source: 'node_loan_do', target: 'node_loan_sdv', animated: true, style: { stroke: '#10b981' } },
                { id: 'e3', source: 'node_loan_sdv', target: 'node_loan_give', animated: true, style: { stroke: '#10b981' } }
            ]);
        }
    };

    const [isValidating, setIsValidating] = useState<boolean>(false);
    const [isSaving, setIsSaving] = useState<boolean>(false);

    // Cargar lista de usuarios para los co-firmantes
    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await apiFetch('/users');
                if (response.ok) {
                    const data = await response.json();
                    // Filtrar al usuario logueado de la lista de co-firmantes
                    const otherUsers = data.filter((u: UserProfile) => u.id !== currentUser?.id);
                    setUsersList(otherUsers);
                }
            } catch (err) {
                console.error("Error al cargar usuarios:", err);
            }
        };
        fetchUsers();
    }, [currentUser]);

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

            if (typeof type === 'undefined' || !type) {
                return;
            }

            const position = reactFlowInstance.project({
                x: event.clientX - reactFlowBounds.left,
                y: event.clientY - reactFlowBounds.top,
            });

            // Establecer costos predeterminados
            const data: { label: string; vhvCost?: number } = { label: `${type.charAt(0).toUpperCase() + type.slice(1)} Block` };
            if (type === 'action') {
                data.vhvCost = 1.5; // Costo por defecto en horas de vida
            }

            const newNode = {
                id: getId(),
                type,
                position,
                data: {
                    ...data,
                    owners: ownerOptions,
                    ownerUserId: type === 'action' ? currentUser?.id : undefined,
                },
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
        [reactFlowInstance, ownerOptions, currentUser]
    );

    const onDragStart = (event: React.DragEvent, nodeType: string) => {
        event.dataTransfer.setData('application/reactflow', nodeType);
        event.dataTransfer.effectAllowed = 'move';
    };

    // Validación axiomática en tiempo real
    const performValidation = useCallback(async () => {
        if (nodes.length <= 1) return;
        setIsValidating(true);
        try {
            const response = await apiFetch('/contracts/validate_graph', {
                method: 'POST',
                body: JSON.stringify({ nodes, edges, duration })
            });
            if (response.ok) {
                const result = await response.json();
                setValidationReport(result);
            }
        } catch (error) {
            console.error('Error validando grafo:', error);
        } finally {
            setIsValidating(false);
        }
    }, [nodes, edges, duration]);

    // Ejecutar validación cada vez que cambien los nodos, edges o la duración
    useEffect(() => {
        const timer = setTimeout(() => {
            performValidation();
        }, 800); // Debounce de 800ms
        return () => clearTimeout(timer);
    }, [nodes, edges, duration, performValidation]);

    const onSaveAndCreate = async () => {
        if (selectedCoSigners.length === 0) {
            alert('⚠️ Debes seleccionar al menos un co-firmante (otro ciudadano de la cohorte) para asociarla al contrato.');
            return;
        }

        setIsSaving(true);
        try {
            // 1. Validar el grafo primero en el backend
            const validateRes = await apiFetch('/contracts/validate_graph', {
                method: 'POST',
                body: JSON.stringify({ nodes, edges, duration })
            });
            
            if (!validateRes.ok) {
                alert('Error al validar con el servidor.');
                setIsSaving(false);
                return;
            }

            const valResult = await validateRes.json();
            if (!valResult.valid) {
                const errors = (valResult.results || [])
                    .filter((r: AxiomResult) => !r.is_valid)
                    .map((r: AxiomResult) => `• ${r.axiom}: ${r.message}`)
                    .join('\n');
                alert(`⚠️ No se puede guardar. Se detectaron infracciones a las reglas éticas:\n\n${errors}`);
                setIsSaving(false);
                return;
            }

            // 2. Crear contrato vía API REST con todos los co-firmantes
            const contractId = `maxo-ctr-${Date.now()}`;
            const actionNodes = nodes.filter(n => n.type === 'action');
            const civilDesc = `Contrato de Intercambio Ético diseñado visualmente. Duración: ${duration} días. Complejidad: ${valResult.ux_signature_type.toUpperCase()}.`;

            const participants = [
                { user_id: currentUser?.id, wellness: 1.0 },
                ...selectedCoSigners.map((uid) => ({ user_id: uid, wellness: 1.0 })),
            ];

            const createRes = await apiFetch('/contracts/', {
                method: 'POST',
                body: JSON.stringify({
                    contract_id: contractId,
                    civil_description: civilDesc,
                    participants,
                    terms: actionNodes.map(node => {
                        const ownerId = (node.data as { ownerUserId?: number }).ownerUserId ?? currentUser?.id;
                        return {
                            term_id: node.id,
                            civil_text: node.data.label || 'Acción del Contrato',
                            vhv: {
                                t: node.data.vhvCost !== undefined ? node.data.vhvCost : 1.5,
                                v: 0,
                                h: 0
                            },
                            assigned_participant_id: ownerId ? `user-${ownerId}` : undefined,
                        };
                    })
                })
            });

            if (createRes.ok) {
                alert('✅ ¡Contrato guardado y registrado correctamente en la base de datos! Redirigiendo a su panel de gestión...');
                router.push(`/contracts/${contractId}`);
            } else {
                const errData = await createRes.json();
                alert(`Error al registrar el contrato: ${errData.error || 'error desconocido'}`);
            }
        } catch (error) {
            console.error('Error registrando contrato:', error);
            alert('Error al conectar con la base de datos.');
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <div className="h-screen w-screen flex flex-col bg-slate-950 overflow-hidden text-slate-100 font-sans">
            {/* Header premium y traslúcido */}
            <header className="h-16 border-b border-slate-800 bg-slate-900/60 backdrop-blur-md flex items-center px-8 justify-between z-10">
                <div className="flex items-center gap-3">
                    <div className="w-9 h-9 bg-emerald-500 rounded-xl flex items-center justify-center text-slate-950 font-black shadow-lg shadow-emerald-500/20">
                        <FileText className="w-5 h-5" />
                    </div>
                    <div>
                        <h1 className="font-extrabold text-lg text-white tracking-tight flex items-center gap-2">
                            MaxoContracts Builder
                            <span className="text-[10px] bg-slate-800 text-slate-400 border border-slate-700 px-2 py-0.5 rounded-full font-normal">v1.1</span>
                        </h1>
                        <p className="text-[10px] text-slate-400">Creador de Acuerdos Auto-Regulados Basados en Tiempo Vital</p>
                    </div>
                </div>
                
                <div className="flex gap-6 items-center">
                    <div className="flex items-center gap-3 bg-slate-900/80 border border-slate-800 px-4 py-1.5 rounded-xl">
                        <User className="w-4 h-4 text-emerald-500" />
                        <div className="flex flex-col">
                            <span className="text-[9px] uppercase font-bold text-slate-500 tracking-wider">Creador del Acuerdo</span>
                            <span className="text-xs font-bold text-slate-200">
                                {currentUser ? `${currentUser.name} (@${currentUser.alias || 'alias'})` : 'Cargando...'}
                            </span>
                        </div>
                    </div>

                    <button 
                        onClick={onSaveAndCreate}
                        disabled={isSaving}
                        className="bg-emerald-500 text-slate-950 px-6 py-2.5 rounded-xl font-bold text-sm hover:bg-emerald-400 transition-all active:scale-95 shadow-lg shadow-emerald-500/10 flex items-center gap-2 disabled:opacity-50"
                    >
                        <Save className="w-4 h-4" />
                        {isSaving ? 'Guardando...' : 'Validar y Registrar'}
                    </button>
                </div>
            </header>

            <div className="flex-1 flex overflow-hidden" ref={reactFlowWrapper}>
                {/* Sidebar Izquierdo: Configuración e Instrucciones */}
                <aside className="w-80 border-r border-slate-800 bg-slate-900/40 p-6 flex flex-col gap-6 z-10 overflow-y-auto backdrop-blur-md">
                    <div>
                        <h2 className="font-black text-white text-md mb-1 uppercase tracking-wider flex items-center gap-2 text-emerald-400">
                            <Settings className="w-4 h-4" />
                            Parámetros Core
                        </h2>
                        <p className="text-xs text-slate-400">Define los fundamentos de la relación del contrato.</p>
                    </div>

                    {/* Selector de Co-Firmantes */}
                    <div className="space-y-2">
                        <label className="text-xs font-bold text-slate-300 block uppercase tracking-wider">
                            Co-Firmantes ({selectedCoSigners.length} seleccionad{selectedCoSigners.length === 1 ? 'o' : 'os'})
                        </label>
                        <div className="max-h-40 overflow-y-auto space-y-1.5 pr-1 border border-slate-800 rounded-xl p-2 bg-slate-950/40">
                            {usersList.length === 0 && (
                                <p className="text-[10px] text-slate-500 p-2">No hay otros ciudadanos registrados en la cohorte.</p>
                            )}
                            {usersList.map((u) => {
                                const checked = selectedCoSigners.includes(u.id);
                                return (
                                    <label
                                        key={u.id}
                                        className={`flex items-center gap-2.5 px-2.5 py-1.5 rounded-lg cursor-pointer border transition-all text-xs ${
                                            checked
                                                ? 'bg-emerald-500/10 border-emerald-500/30 text-slate-200'
                                                : 'bg-slate-900/40 border-slate-800 text-slate-400 hover:border-slate-700'
                                        }`}
                                    >
                                        <input
                                            type="checkbox"
                                            checked={checked}
                                            onChange={(e) => {
                                                setSelectedCoSigners((prev) =>
                                                    e.target.checked
                                                        ? [...prev, u.id]
                                                        : prev.filter((id) => id !== u.id)
                                                );
                                            }}
                                            className="accent-emerald-500 rounded"
                                        />
                                        <span className="font-bold truncate">{u.name}</span>
                                        <span className="text-[9px] text-slate-500 ml-auto">@{u.alias || 'sin alias'}</span>
                                    </label>
                                );
                            })}
                        </div>
                        <p className="text-[10px] text-slate-500 leading-normal">
                            Personas de la cohorte que compartirán las obligaciones vitales de este acuerdo.
                            Cada bloque del lienzo puede asignarse a una parte distinta (selector en el nodo).
                        </p>
                    </div>

                    {/* Duración del Contrato */}
                    <div className="space-y-2 pt-2 border-t border-slate-800/60">
                        <div className="flex justify-between items-center">
                            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">Duración Vital</label>
                            <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-950/50 border border-emerald-900 px-2 py-0.5 rounded">{duration} Días</span>
                        </div>
                        <input 
                            type="range" 
                            min="1" 
                            max="180" 
                            value={duration} 
                            onChange={(e) => setDuration(parseInt(e.target.value))}
                            className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                        />
                        <div className="flex justify-between text-[9px] text-slate-600 font-mono">
                            <span>1 día</span>
                            <span>90 días</span>
                            <span>180 días</span>
                        </div>
                        <p className="text-[10px] text-slate-500 leading-normal">
                            Tiempo durante el cual el contrato permanecerá activo y bajo monitoreo ético del oráculo.
                        </p>
                    </div>

                    {/* Plantillas Predefinidas de Ejemplo */}
                    <div className="space-y-3 pt-4 border-t border-slate-800/60">
                        <div>
                            <h3 className="text-xs font-bold text-slate-300 block uppercase tracking-wider flex items-center gap-1.5 text-emerald-400">
                                <Award className="w-3.5 h-3.5" />
                                Plantillas de Ejemplo
                            </h3>
                            <p className="text-[10px] text-slate-500 leading-relaxed">
                                Carga esquemas prediseñados basados en los axiomas del Capítulo 17.
                            </p>
                        </div>
                        <div className="flex flex-col gap-2">
                            <button
                                onClick={() => loadTemplate('colab')}
                                className="w-full text-left p-2.5 rounded-xl bg-slate-950/60 hover:bg-slate-900 border border-slate-900 hover:border-emerald-500/30 transition-all text-[11px] space-y-1 group"
                            >
                                <span className="font-bold text-slate-200 block group-hover:text-emerald-400 transition-colors">1. Intercambio Ético (10h ↔ Objeto/Servicio)</span>
                                <span className="text-[9px] text-slate-500 block leading-snug">Max ofrece 10 horas de trabajo; la contraparte elige reciprocidad: objeto, servicio u horas. Editable en el lienzo.</span>
                            </button>
                            <button
                                onClick={() => loadTemplate('support')}
                                className="w-full text-left p-2.5 rounded-xl bg-slate-950/60 hover:bg-slate-900 border border-slate-900 hover:border-amber-500/30 transition-all text-[11px] space-y-1 group"
                            >
                                <span className="font-bold text-slate-200 block group-hover:text-amber-400 transition-colors">2. Soporte Condicionado</span>
                                <span className="text-[9px] text-slate-500 block leading-snug">Activado por downtime del servidor y auditado por oráculo. Nivel: Medio.</span>
                            </button>
                            <button
                                onClick={() => loadTemplate('loan')}
                                className="w-full text-left p-2.5 rounded-xl bg-slate-950/60 hover:bg-slate-900 border border-slate-900 hover:border-rose-500/30 transition-all text-[11px] space-y-1 group"
                            >
                                <span className="font-bold text-slate-200 block group-hover:text-rose-400 transition-colors">3. Préstamo Protegido</span>
                                <span className="text-[9px] text-slate-500 block leading-snug">Mentoría tutorada resguardada por el Suelo de Dignidad Vital. Nivel: Riguroso.</span>
                            </button>
                        </div>
                    </div>

                    {/* Biblioteca de Bloques */}
                    <div className="pt-4 border-t border-slate-800/60 flex flex-col gap-4">
                        <div>
                            <h3 className="text-xs font-bold text-slate-300 block uppercase tracking-wider mb-2">Bloques Disponibles</h3>
                            <p className="text-[10px] text-slate-500 leading-relaxed">
                                Arrastra estos componentes al lienzo para trazar la topología del acuerdo.
                            </p>
                        </div>
                        
                        <div className="flex flex-col gap-2.5">
                            <div 
                                className="p-3 bg-slate-900/60 hover:bg-slate-900 rounded-xl border border-slate-800 cursor-grab hover:border-amber-500/50 transition-all flex items-center gap-3 group"
                                onDragStart={(event) => onDragStart(event, 'condition')}
                                draggable
                            >
                                <div className="w-2.5 h-2.5 rounded bg-amber-500 group-hover:scale-125 transition-transform" />
                                <div className="flex flex-col">
                                    <span className="text-xs font-bold text-slate-200">Condición (IF)</span>
                                    <span className="text-[9px] text-slate-500">Bifurcación de estado</span>
                                </div>
                            </div>

                            <div 
                                className="p-3 bg-slate-900/60 hover:bg-slate-900 rounded-xl border border-slate-800 cursor-grab hover:border-blue-500/50 transition-all flex items-center gap-3 group"
                                onDragStart={(event) => onDragStart(event, 'action')}
                                draggable
                            >
                                <div className="w-2.5 h-2.5 rounded bg-blue-500 group-hover:scale-125 transition-transform" />
                                <div className="flex flex-col">
                                    <span className="text-xs font-bold text-slate-200">Acción (DO)</span>
                                    <span className="text-[9px] text-slate-500">Costo VHV asociado</span>
                                </div>
                            </div>

                            <div 
                                className="p-3 bg-slate-900/60 hover:bg-slate-900 rounded-xl border border-slate-800 cursor-grab hover:border-purple-500/50 transition-all flex items-center gap-3 group"
                                onDragStart={(event) => onDragStart(event, 'oracle')}
                                draggable
                            >
                                <div className="w-2.5 h-2.5 rounded bg-purple-500 group-hover:scale-125 transition-transform" />
                                <div className="flex flex-col">
                                    <span className="text-xs font-bold text-slate-200">Oráculo (VERDICT)</span>
                                    <span className="text-[9px] text-slate-500">Resolución automatizada</span>
                                </div>
                            </div>

                            <div 
                                className="p-3 bg-slate-900/60 hover:bg-slate-900 rounded-xl border border-slate-800 cursor-grab hover:border-emerald-500/50 transition-all flex items-center gap-3 group"
                                onDragStart={(event) => onDragStart(event, 'sdv')}
                                draggable
                            >
                                <div className="w-2.5 h-2.5 rounded bg-emerald-500 group-hover:scale-125 transition-transform" />
                                <div className="flex flex-col">
                                    <span className="text-xs font-bold text-slate-200">Suelo de Dignidad (SDV)</span>
                                    <span className="text-[9px] text-slate-500">Garantía existencial</span>
                                </div>
                            </div>

                            <div 
                                className="p-3 bg-slate-900/60 hover:bg-slate-900 rounded-xl border border-slate-800 cursor-grab hover:border-rose-500/50 transition-all flex items-center gap-3 group"
                                onDragStart={(event) => onDragStart(event, 'reciprocity')}
                                draggable
                            >
                                <div className="w-2.5 h-2.5 rounded bg-rose-500 group-hover:scale-125 transition-transform" />
                                <div className="flex flex-col">
                                    <span className="text-xs font-bold text-slate-200">Reciprocidad (GIVE)</span>
                                    <span className="text-[9px] text-slate-500">Asegura simetría ética</span>
                                </div>
                        </div>
                    </div>

                    {/* Guía de Conectividad Liminal */}
                    <div className="pt-4 border-t border-slate-800/60 space-y-3">
                        <h3 className="text-xs font-bold text-slate-350 block uppercase tracking-wider flex items-center gap-1.5 text-emerald-400">
                            <Info className="w-3.5 h-3.5" />
                            Guía de Conectividad
                        </h3>
                        <div className="bg-slate-950/60 border border-slate-900 rounded-xl p-3 space-y-2.5 text-[10px] text-slate-400 leading-normal">
                            <p className="text-white font-bold">Reglas de Integridad del Grafo:</p>
                            <div className="space-y-1.5">
                                <div className="flex gap-2">
                                    <span className="text-emerald-500 font-bold shrink-0">1.</span>
                                    <span>Inicia tu flujo conectando el nodo <strong>Inicio Contrato</strong>.</span>
                                </div>
                                <div className="flex gap-2">
                                    <span className="text-amber-500 font-bold shrink-0">2.</span>
                                    <span>Conecta nodos de <strong>Condición (IF)</strong> para estructurar precondiciones lógicas.</span>
                                </div>
                                <div className="flex gap-2">
                                    <span className="text-blue-500 font-bold shrink-0">3.</span>
                                    <span>Toda <strong>Acción (DO)</strong> debe conectarse eventualmente a un bloque de <strong>Reciprocidad (GIVE)</strong> (Axioma T9).</span>
                                </div>
                                <div className="flex gap-2">
                                    <span className="text-purple-500 font-bold shrink-0">4.</span>
                                    <span>Agrega un <strong>Oráculo (VERDICT)</strong> si el contrato incluye cláusulas de retractabilidad complejas.</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </aside>

                {/* Canvas de React Flow */}
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
                        className="bg-slate-950"
                    >
                        <Background color="#1e293b" gap={20} size={1} />
                        <Controls className="bg-slate-900 border border-slate-800 text-slate-200 fill-slate-200" />
                        
                        <Panel position="bottom-right" className="bg-slate-900/80 backdrop-blur-md p-3 rounded-xl border border-slate-800 shadow-lg mb-4 mr-4">
                            <div className="text-[9px] font-black text-slate-500 uppercase tracking-widest mb-1">Coordenadas del Grafo</div>
                            <div className="text-[11px] font-mono text-slate-300">Nodos: {nodes.length} | Edges: {edges.length}</div>
                        </Panel>
                    </ReactFlow>
                </div>

                {/* Sidebar Derecho: Complejidad Ética y Glosario (Siempre visibles y sobre explicados) */}
                <aside className="w-96 border-l border-slate-800 bg-slate-900/40 p-6 flex flex-col gap-6 z-10 overflow-y-auto backdrop-blur-md">
                    {/* Panel de Complejidad Ética */}
                    <div className="glass p-5 rounded-2xl border border-slate-800 bg-slate-950/60 shadow-xl space-y-4">
                        <div className="flex justify-between items-center">
                            <h3 className="font-extrabold text-xs text-white uppercase tracking-wider flex items-center gap-2">
                                <Award className="w-4 h-4 text-emerald-400" />
                                Complejidad Ética
                            </h3>
                            {isValidating && (
                                <span className="text-[10px] text-emerald-400 animate-pulse">Analizando...</span>
                            )}
                        </div>

                        {validationReport ? (
                            <div className="space-y-4">
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="bg-slate-900/80 border border-slate-800 p-3 rounded-xl flex flex-col justify-center">
                                        <span className="text-[9px] text-slate-500 uppercase font-black">Peso del Contrato</span>
                                        <span className="text-2xl font-black text-emerald-400">{validationReport.weight.toFixed(2)}</span>
                                    </div>
                                    <div className="bg-slate-900/80 border border-slate-800 p-3 rounded-xl flex flex-col justify-center">
                                        <span className="text-[9px] text-slate-500 uppercase font-black">Nivel de Firma UX</span>
                                        <span className="text-xs font-extrabold text-white uppercase mt-1 px-2 py-0.5 rounded bg-slate-800 border border-slate-700 w-max">
                                            {validationReport.ux_signature_type}
                                        </span>
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    <div className="text-[10px] font-black text-slate-400 uppercase tracking-wider">Costo VHV Total</div>
                                    <div className="bg-slate-950 border border-slate-900 p-2.5 rounded-xl grid grid-cols-3 text-center text-xs font-mono">
                                        <div>
                                            <div className="text-[9px] text-slate-500">T (Tiempo)</div>
                                            <div className="font-bold text-blue-400">{validationReport.total_vhv.t.toFixed(1)}h</div>
                                        </div>
                                        <div>
                                            <div className="text-[9px] text-slate-500">V (Voluntad)</div>
                                            <div className="font-bold text-purple-400">{validationReport.total_vhv.v.toFixed(1)}</div>
                                        </div>
                                        <div>
                                            <div className="text-[9px] text-slate-500">R (Recursos)</div>
                                            <div className="font-bold text-rose-400">{validationReport.total_vhv.r.toFixed(1)}</div>
                                        </div>
                                    </div>
                                </div>

                                {/* Explicación Detallada de Modalidades de Firma */}
                                <div className="space-y-2 pt-2 border-t border-slate-850">
                                    <div className="text-[10px] font-black text-slate-400 uppercase tracking-wider">Fórmula de Peso Contractual:</div>
                                    <div className="bg-slate-950 border border-slate-900 p-2.5 rounded-xl text-[10px] text-slate-400 leading-normal space-y-2">
                                        <p className="font-mono text-emerald-400 text-center bg-slate-900 py-1 rounded border border-slate-800">
                                            Peso = (N_cond × 2) + (VHV_total × 5) + (Duración ÷ 30)
                                        </p>
                                        <p>
                                            El peso mide el compromiso ético y la asimetría potencial del contrato, determinando dinámicamente cómo se firmará:
                                        </p>
                                        <div className="space-y-1.5 pt-1.5 border-t border-slate-900">
                                            <div className="flex justify-between items-center">
                                                <span className="font-bold text-white">Simple (Peso &lt; 10):</span>
                                                <span className="text-[9px] bg-slate-850 text-slate-350 px-1.5 py-0.5 rounded text-emerald-400">Firma Rápida</span>
                                            </div>
                                            <p className="text-[9px] pl-2 border-l border-emerald-550/30 text-slate-500">Acuerdos breves de bajo impacto. Firma en 1 solo clic tras verificar que el suelo mínimo vital está a salvo.</p>
                                            
                                            <div className="flex justify-between items-center mt-2">
                                                <span className="font-bold text-white">Medio (10 a 50):</span>
                                                <span className="text-[9px] bg-slate-850 text-slate-350 px-1.5 py-0.5 rounded text-amber-400">Término a Término</span>
                                            </div>
                                            <p className="text-[9px] pl-2 border-l border-amber-550/30 text-slate-500">Complejidad moderada. Requiere revisar y aceptar cada término mediante un checklist interactivo individual.</p>
                                            
                                            <div className="flex justify-between items-center mt-2">
                                                <span className="font-bold text-white">Riguroso (Peso &gt; 50):</span>
                                                <span className="text-[9px] bg-slate-850 text-slate-350 px-1.5 py-0.5 rounded text-rose-400">Firma Pausada</span>
                                            </div>
                                            <p className="text-[9px] pl-2 border-l border-rose-550/30 text-slate-500">Complejo o alto costo de Tiempo Vital. Exige un asistente paso a paso, con timer de reflexión obligatorio (10s por cláusula) y preguntas de control de comprensión.</p>
                                        </div>
                                    </div>
                                </div>

                                <div className="space-y-2 pt-2 border-t border-slate-850">
                                    <div className="text-[10px] font-black text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                                        <ShieldAlert className="w-3.5 h-3.5 text-amber-500" />
                                        Estado de los Axiomas (Libro Cap. 17)
                                    </div>
                                    
                                    <div className="space-y-1.5 max-h-48 overflow-y-auto pr-1">
                                        {validationReport.results.map((r, idx) => (
                                            <div 
                                                key={idx} 
                                                className={`p-2.5 rounded-xl border text-[11px] flex items-start gap-2 ${
                                                    r.is_valid 
                                                        ? 'bg-emerald-950/20 border-emerald-900/40 text-emerald-300' 
                                                        : 'bg-rose-950/20 border-rose-900/40 text-rose-300'
                                                }`}
                                            >
                                                <div className={`w-1.5 h-1.5 rounded-full mt-1.5 shrink-0 ${r.is_valid ? 'bg-emerald-400' : 'bg-rose-400'}`} />
                                                <div>
                                                    <span className="font-bold">[{r.axiom}]</span> {r.message}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <div className="text-center py-6 text-slate-500 text-xs italic">
                                Diseña tu acuerdo agregando y conectando bloques en el lienzo para realizar los cálculos éticos en tiempo real.
                            </div>
                        )}
                    </div>

                    {/* Glosario de Conceptos siempre visible y sobre-explicado */}
                    <div className="glass p-5 rounded-2xl border border-slate-800 bg-slate-950/40 space-y-4">
                        <h3 className="font-extrabold text-xs text-white uppercase tracking-wider flex items-center gap-2">
                            <Info className="w-4 h-4 text-emerald-400" />
                            Glosario Maxocrático (Cap. 17)
                        </h3>

                        <div className="space-y-3.5 text-xs text-slate-400 leading-normal">
                            <div className="p-2.5 rounded-xl bg-slate-950/50 border border-slate-900 space-y-1">
                                <span className="font-bold text-slate-200 block">VHV (Valor de Horas de Vida)</span>
                                <p className="text-[10px]">
                                    Métrica fundamental que reemplaza el valor abstracto del dinero por el <strong>Tiempo Vital Humano</strong>. Mide la cantidad de atención, energía consciente e insumos planetarios requeridos por cada término. Su valor se calcula en función de la huella vital de los firmantes.
                                </p>
                            </div>

                            <div className="p-2.5 rounded-xl bg-slate-950/50 border border-slate-900 space-y-1">
                                <span className="font-bold text-slate-200 block">Axioma T1 (Finitud del Tiempo)</span>
                                <p className="text-[10px]">
                                    Establece que el Tiempo Vital Humano (TVI) es finito, insustituible y no acumulable. Los MaxoContracts prohíben comprometer tiempo del que un ciudadano no dispone, evitando la servidumbre por deuda de tiempo.
                                </p>
                            </div>

                            <div className="p-2.5 rounded-xl bg-slate-950/50 border border-slate-900 space-y-1">
                                <span className="font-bold text-slate-200 block">SDV (Suelo de Dignidad Vital)</span>
                                <p className="text-[10px]">
                                    El conjunto de mínimos de subsistencia física, social y psicológica garantizados para todos. El oráculo ético rechaza automáticamente cualquier acuerdo que reduzca los indicadores vitales de un firmante bajo este umbral (Invariante INV2).
                                </p>
                            </div>

                            <div className="p-2.5 rounded-xl bg-slate-950/50 border border-slate-900 space-y-1">
                                <span className="font-bold text-slate-200 block">Axioma T9 (Reciprocidad Justa)</span>
                                <p className="text-[10px]">
                                    Establece que toda acción de costo vital (DO) en el contrato debe estar equilibrada con un bloque de reciprocidad (GIVE). Esto previene la explotación unilateral asegurando relaciones socioeconómicas simétricas.
                                </p>
                            </div>

                            <div className="p-2.5 rounded-xl bg-slate-950/50 border border-slate-900 space-y-1">
                                <span className="font-bold text-slate-200 block">Bienestar Relacional (γ)</span>
                                <p className="text-[10px]">
                                    Un índice ponderado (1.0 es coherencia plena, menor a 1.0 es sufrimiento) que monitorea la salud material y social de los firmantes. Si el bienestar decae drásticamente durante el acuerdo (Invariante INV1), se desbloquean los derechos de retractación.
                                </p>
                            </div>

                            <div className="p-2.5 rounded-xl bg-slate-950/50 border border-slate-900 space-y-1">
                                <span className="font-bold text-slate-200 block">Complejidad Ética (Peso)</span>
                                <p className="text-[10px] font-mono bg-slate-900 p-1.5 rounded text-[9px] border border-slate-800 text-emerald-400">
                                    Peso = (N_cond * 2) + (VHV * 5) + (Duración / 30)
                                </p>
                                <p className="text-[10px]">
                                    A mayor cantidad de condiciones, costo vital e incertidumbre temporal, se exige un proceso de firma progresivamente más riguroso (Simple, Medio, Riguroso) para evitar asimetrías cognitivas o firmas mecánicas.
                                </p>
                            </div>
                        </div>
                    </div>
                </aside>
            </div>
        </div>
    );
}


