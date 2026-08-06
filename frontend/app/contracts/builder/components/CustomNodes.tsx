import React, { memo } from 'react';
import { Handle, Position, useReactFlow } from 'reactflow';

export interface NodeOwner {
    id: number;
    label: string;
}

interface CustomNodeProps {
    id: string;
    data: {
        label?: string;
        vhvCost?: number;
        oracleType?: string;
        penaltyType?: string;
        ownerUserId?: number;
        owners?: NodeOwner[];
    };
}

const OwnerSelect = ({ id, data }: CustomNodeProps) => {
    const { setNodes } = useReactFlow();

    const onOwnerChange = (evt: React.ChangeEvent<HTMLSelectElement>) => {
        const ownerId = evt.target.value ? parseInt(evt.target.value) : undefined;
        setNodes((nds) => nds.map((n) => n.id === id ? { ...n, data: { ...n.data, ownerUserId: ownerId } } : n));
    };

    const owners = data.owners || [];
    if (owners.length <= 1) return null;

    const current = owners.find((o) => o.id === data.ownerUserId);

    return (
        <div className="flex flex-col gap-0.5">
            <select
                value={data.ownerUserId !== undefined ? data.ownerUserId : ''}
                onChange={onOwnerChange}
                className="w-full bg-slate-50 text-[10px] font-bold text-slate-600 p-1.5 rounded-lg border border-slate-100 focus:outline-none appearance-none"
            >
                <option value="">Sin asignar</option>
                {owners.map((o) => (
                    <option key={o.id} value={o.id}>{o.label}</option>
                ))}
            </select>
            <div className="text-[7px] text-slate-400 leading-tight">
                Parte obligada de este bloque
            </div>
        </div>
    );
};

export const ActionNode = memo(({ id, data }: CustomNodeProps) => {
    const { setNodes } = useReactFlow();

    const onCostChange = (evt: React.ChangeEvent<HTMLInputElement>) => {
        const val = parseFloat(evt.target.value);
        setNodes((nds) => nds.map((n) => n.id === id ? { ...n, data: { ...n.data, vhvCost: isNaN(val) ? 0 : val } } : n));
    };

    const onLabelChange = (evt: React.ChangeEvent<HTMLTextAreaElement>) => {
        setNodes((nds) => nds.map((n) => n.id === id ? { ...n, data: { ...n.data, label: evt.target.value } } : n));
    };

    return (
        <div className="px-4 py-3 shadow-xl rounded-2xl bg-white border-2 border-blue-100 min-w-[200px]">
            <Handle type="target" position={Position.Top} className="w-3 h-3 bg-blue-400 border-2 border-white" />
            <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-blue-500" />
                <div className="text-[10px] font-bold text-blue-500 uppercase tracking-wider">Acción (DO)</div>
            </div>
            <textarea
                className="text-sm font-bold text-slate-700 bg-blue-50/30 p-2 rounded-lg border border-blue-50 w-full focus:outline-none resize-none"
                rows={2}
                value={data.label || ''}
                onChange={onLabelChange}
            />
            <div className="flex flex-col gap-1 mt-1">
                <div className="flex justify-between items-center bg-slate-50 p-1.5 rounded-lg border border-slate-100">
                    <span className="text-[9px] font-bold text-slate-400">COSTO VHV</span>
                    <input
                        type="number"
                        className="w-12 bg-transparent text-right text-xs font-bold text-slate-600 focus:outline-none"
                        value={data.vhvCost !== undefined ? data.vhvCost : 0.5}
                        onChange={onCostChange}
                        step={0.1}
                    />
                </div>
                <OwnerSelect id={id} data={data} />
            </div>
            <div className="text-[8px] text-slate-400 mt-1.5 leading-tight">
                <strong>Costo VHV:</strong> Tiempo Vital (en horas) que la parte asignada invertirá conscientemente.
            </div>
            <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-blue-400 border-2 border-white" />
        </div>
    );
});

export const ConditionNode = memo(({ id, data }: CustomNodeProps) => {
    const { setNodes } = useReactFlow();

    const onLabelChange = (evt: React.ChangeEvent<HTMLTextAreaElement>) => {
        setNodes((nds) => nds.map((n) => n.id === id ? { ...n, data: { ...n.data, label: evt.target.value } } : n));
    };

    return (
        <div className="px-4 py-3 shadow-xl rounded-2xl bg-white border-2 border-amber-100 min-w-[180px]">
            <Handle type="target" position={Position.Top} className="w-3 h-3 bg-amber-400 border-2 border-white" />
            <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-amber-500" />
                <div className="text-[10px] font-bold text-amber-500 uppercase tracking-wider">Condición (IF)</div>
            </div>
            <textarea 
                className="text-sm font-bold text-slate-700 bg-amber-50/30 p-2 rounded-lg border border-amber-50 w-full focus:outline-none resize-none" 
                rows={2}
                value={data.label || ''}
                onChange={onLabelChange}
            />
            <div className="text-[8px] text-slate-400 mt-1.5 leading-tight">
                <strong>Condición:</strong> Hecho verificable en el mundo real que activa o bifurca los términos del acuerdo.
            </div>
            <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-amber-400 border-2 border-white" />
        </div>
    );
});

export const OracleNode = memo(({ id, data }: CustomNodeProps) => {
    const { setNodes } = useReactFlow();

    const onOracleChange = (evt: React.ChangeEvent<HTMLSelectElement>) => {
        setNodes((nds) => nds.map((n) => n.id === id ? { ...n, data: { ...n.data, oracleType: evt.target.value } } : n));
    };

    return (
        <div className="px-4 py-3 shadow-xl rounded-2xl bg-white border-2 border-purple-100 min-w-[180px]">
            <Handle type="target" position={Position.Top} className="w-3 h-3 bg-purple-400 border-2 border-white" />
            <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-purple-500" />
                <div className="text-[10px] font-bold text-purple-500 uppercase tracking-wider">Oráculo (VERDICT)</div>
            </div>
            <select 
                className="w-full bg-slate-50 text-xs font-bold text-slate-600 p-2 rounded-lg border border-slate-100 focus:outline-none appearance-none"
                value={data.oracleType || 'Sintético (Gemini)'}
                onChange={onOracleChange}
            >
                <option value="Sintético (Gemini)">Sintético (Gemini)</option>
                <option value="Formulario (Humano)">Formulario (Humano)</option>
                <option value="Híbrido (Consenso)">Híbrido (Consenso)</option>
            </select>
            <div className="text-[8px] text-slate-400 mt-1.5 leading-tight">
                <strong>Oráculo:</strong> Juez sintético o humano neutral que evalúa el cumplimiento o las solicitudes de retractación.
            </div>
            <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-purple-400 border-2 border-white" />
        </div>
    );
});

export const SDVNode = memo(() => {
    return (
        <div className="px-4 py-3 shadow-xl rounded-2xl bg-white border-2 border-emerald-100 min-w-[180px]">
            <Handle type="target" position={Position.Top} className="w-3 h-3 bg-emerald-400 border-2 border-white" />
            <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-emerald-500" />
                <div className="text-[10px] font-bold text-emerald-500 uppercase tracking-wider">Suelo de Dignidad (SDV)</div>
            </div>
            <div className="text-[8px] text-slate-400 leading-tight mb-2">
                <strong>Suelo de Dignidad Vital (INV2):</strong> Protege que tus obligaciones no reduzcan tus mínimos vitales (alimento, techo, salud o descanso básico).
            </div>
            <div className="bg-emerald-50 p-2 rounded-lg text-[10px] font-bold text-emerald-700 text-center">
                VALIDACIÓN ACTIVA
            </div>
            <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-emerald-400 border-2 border-white" />
        </div>
    );
});

export const ReciprocityNode = memo(({ id, data }: CustomNodeProps) => {
    const { setNodes } = useReactFlow();

    const onPenaltyChange = (evt: React.ChangeEvent<HTMLSelectElement>) => {
        setNodes((nds) => nds.map((n) => n.id === id ? { ...n, data: { ...n.data, penaltyType: evt.target.value } } : n));
    };

    const onLabelChange = (evt: React.ChangeEvent<HTMLTextAreaElement>) => {
        setNodes((nds) => nds.map((n) => n.id === id ? { ...n, data: { ...n.data, label: evt.target.value } } : n));
    };

    return (
        <div className="px-4 py-3 shadow-xl rounded-2xl bg-white border-2 border-rose-100 min-w-[200px]">
            <Handle type="target" position={Position.Top} className="w-3 h-3 bg-rose-400 border-2 border-white" />
            <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-rose-500" />
                <div className="text-[10px] font-bold text-rose-500 uppercase tracking-wider">Reciprocidad (GIVE/BACK)</div>
            </div>
            <textarea
                className="text-xs font-bold text-slate-600 bg-rose-50/30 p-2 rounded-lg border border-rose-50 w-full focus:outline-none resize-none"
                rows={2}
                value={data.label || ''}
                onChange={onLabelChange}
            />
            <div className="flex flex-col gap-1 mt-1">
                <div className="text-[9px] font-bold text-slate-400">Si no se cumple:</div>
                <select
                    className="w-full bg-rose-50 text-[10px] font-bold text-rose-700 p-1.5 rounded-lg border border-rose-100 focus:outline-none appearance-none"
                    value={data.penaltyType || 'Penalización γ (-0.2)'}
                    onChange={onPenaltyChange}
                >
                    <option value="Penalización γ (-0.2)">Penalización γ (-0.2)</option>
                    <option value="Restitución de Tiempo">Restitución de Tiempo</option>
                    <option value="Mediación Humana">Mediación Humana</option>
                </select>
                <OwnerSelect id={id} data={data} />
            </div>
            <div className="text-[8px] text-slate-400 mt-1.5 leading-tight">
                <strong>Axioma T9 (Reciprocidad Justa):</strong> Toda acción de costo vital (DO) requiere una contraprestación equivalente (GIVE) — horas, objeto o servicio — evitando la explotación.
            </div>
            <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-rose-400 border-2 border-white" />
        </div>
    );
});

ActionNode.displayName = 'ActionNode';
ConditionNode.displayName = 'ConditionNode';
OracleNode.displayName = 'OracleNode';
SDVNode.displayName = 'SDVNode';
ReciprocityNode.displayName = 'ReciprocityNode';
