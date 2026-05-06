import React, { memo } from 'react';
import { Handle, Position, useReactFlow } from 'reactflow';

export const ActionNode = memo(({ id, data }: any) => {
    const { setNodes } = useReactFlow();

    const onCostChange = (evt: React.ChangeEvent<HTMLInputElement>) => {
        const val = parseFloat(evt.target.value);
        setNodes((nds) => nds.map((n) => n.id === id ? { ...n, data: { ...n.data, vhvCost: isNaN(val) ? 0 : val } } : n));
    };

    return (
        <div className="px-4 py-3 shadow-xl rounded-2xl bg-white border-2 border-blue-100 min-w-[180px]">
            <Handle type="target" position={Position.Top} className="w-3 h-3 bg-blue-400 border-2 border-white" />
            <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-blue-500" />
                <div className="text-[10px] font-bold text-blue-500 uppercase tracking-wider">Acción (DO)</div>
            </div>
            <div className="text-sm font-bold text-slate-700 mb-2">{data.label}</div>
            <div className="flex flex-col gap-1">
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
            </div>
            <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-blue-400 border-2 border-white" />
        </div>
    );
});

export const ConditionNode = memo(({ id, data }: any) => {
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
            <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-amber-400 border-2 border-white" />
        </div>
    );
});

export const OracleNode = memo(({ id, data }: any) => {
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
            <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-purple-400 border-2 border-white" />
        </div>
    );
});

export const SDVNode = memo(({ data }: any) => {
    return (
        <div className="px-4 py-3 shadow-xl rounded-2xl bg-white border-2 border-emerald-100 min-w-[180px]">
            <Handle type="target" position={Position.Top} className="w-3 h-3 bg-emerald-400 border-2 border-white" />
            <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-emerald-500" />
                <div className="text-[10px] font-bold text-emerald-500 uppercase tracking-wider">Suelo de Dignidad (SDV)</div>
            </div>
            <div className="text-[11px] text-slate-500 italic mb-2">Garantiza mínimos existenciales</div>
            <div className="bg-emerald-50 p-2 rounded-lg text-[10px] font-bold text-emerald-700 text-center">
                VALIDACIÓN ACTIVA
            </div>
            <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-emerald-400 border-2 border-white" />
        </div>
    );
});

export const ReciprocityNode = memo(({ id, data }: any) => {
    const { setNodes } = useReactFlow();

    const onPenaltyChange = (evt: React.ChangeEvent<HTMLSelectElement>) => {
        setNodes((nds) => nds.map((n) => n.id === id ? { ...n, data: { ...n.data, penaltyType: evt.target.value } } : n));
    };

    return (
        <div className="px-4 py-3 shadow-xl rounded-2xl bg-white border-2 border-rose-100 min-w-[180px]">
            <Handle type="target" position={Position.Top} className="w-3 h-3 bg-rose-400 border-2 border-white" />
            <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-rose-500" />
                <div className="text-[10px] font-bold text-rose-500 uppercase tracking-wider">Reciprocidad (GIVE/BACK)</div>
            </div>
            <div className="text-xs font-bold text-slate-600 mb-1">Si no se cumple:</div>
            <select 
                className="w-full bg-rose-50 text-[10px] font-bold text-rose-700 p-2 rounded-lg border border-rose-100 focus:outline-none appearance-none"
                value={data.penaltyType || 'Penalización γ (-0.2)'}
                onChange={onPenaltyChange}
            >
                <option value="Penalización γ (-0.2)">Penalización γ (-0.2)</option>
                <option value="Restitución de Tiempo">Restitución de Tiempo</option>
                <option value="Mediación Humana">Mediación Humana</option>
            </select>
            <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-rose-400 border-2 border-white" />
        </div>
    );
});

ActionNode.displayName = 'ActionNode';
ConditionNode.displayName = 'ConditionNode';
OracleNode.displayName = 'OracleNode';
SDVNode.displayName = 'SDVNode';
ReciprocityNode.displayName = 'ReciprocityNode';
