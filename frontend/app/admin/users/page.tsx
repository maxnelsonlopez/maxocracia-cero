"use client";

import React, { useEffect, useState } from "react";
import {
    Search,
    Filter,
    MoreHorizontal,
    UserPlus,
    Shield,
    CheckCircle2,
    XCircle,
    Clock,
    ExternalLink,
    Edit,
    Check
} from "lucide-react";

interface AdminUser {
    id: number;
    email: string;
    name: string;
    alias: string;
    tier: string | null;
    sub_status: string | null;
    expires_at: string | null;
    payment_method: string | null;
}

export default function AdminUsers() {
    const [users, setUsers] = useState<AdminUser[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [search, setSearch] = useState("");

    // State for manual activation modal
    const [selectedUser, setSelectedUser] = useState<AdminUser | null>(null);
    const [activationTier, setActivationTier] = useState("contributor");
    const [activationMonths, setActivationMonths] = useState(1);
    const [activationMethod, setActivationMethod] = useState("manual_transfer");
    const [isActivating, setIsActivating] = useState(false);

    useEffect(() => {
        fetchUsers();
    }, []);

    async function fetchUsers() {
        try {
            setLoading(true);
            const token = localStorage.getItem("mc_token");
            const res = await fetch("/subscriptions/admin/users", {
                headers: { "Authorization": `Bearer ${token}` }
            });
            if (!res.ok) throw new Error("Error cargando usuarios");
            const data = await res.json();
            setUsers(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Error desconocido");
        } finally {
            setLoading(false);
        }
    }

    async function handleActivate() {
        if (!selectedUser) return;

        try {
            setIsActivating(true);
            const token = localStorage.getItem("mc_token");
            const res = await fetch("/subscriptions/activate-manual", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    user_id: selectedUser.id,
                    tier: activationTier,
                    months: activationMonths,
                    payment_method: activationMethod,
                    notes: "Activado via Admin Dashboard"
                })
            });

            if (!res.ok) throw new Error("Error activando suscripción");

            // Refresh list
            await fetchUsers();
            setSelectedUser(null);
        } catch (err) {
            alert(err instanceof Error ? err.message : "Error al activar");
        } finally {
            setIsActivating(false);
        }
    }

    const filteredUsers = users.filter(u =>
        u.email.toLowerCase().includes(search.toLowerCase()) ||
        (u.name && u.name.toLowerCase().includes(search.toLowerCase())) ||
        (u.alias && u.alias.toLowerCase().includes(search.toLowerCase()))
    );

    return (
        <div className="space-y-6">
            {/* Header Actions */}
            <div className="flex flex-col sm:flex-row gap-4 justify-between items-center bg-slate-900/50 p-4 rounded-2xl border border-slate-800">
                <div className="relative w-full sm:w-96">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                    <input
                        type="text"
                        placeholder="Buscar por email, nombre o alias..."
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/50 transition-all"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                </div>
                <div className="flex gap-2">
                    <button className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-sm font-medium transition-colors">
                        <Filter className="w-4 h-4" />
                        Filtros
                    </button>
                    <button className="flex items-center gap-2 px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl text-sm font-medium transition-colors">
                        <UserPlus className="w-4 h-4" />
                        Invitar
                    </button>
                </div>
            </div>

            {/* Users Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm">
                        <thead className="bg-slate-800/50 text-slate-400 uppercase text-[10px] font-bold tracking-wider">
                            <tr>
                                <th className="px-6 py-4">Usuario</th>
                                <th className="px-6 py-4">Estado / Tier</th>
                                <th className="px-6 py-4">Suscripción</th>
                                <th className="px-6 py-4">Método</th>
                                <th className="px-6 py-4 text-right">Acciones</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800">
                            {loading ? (
                                <tr><td colSpan={5} className="px-6 py-12 text-center text-slate-500">Cargando ciudadanos...</td></tr>
                            ) : filteredUsers.length === 0 ? (
                                <tr><td colSpan={5} className="px-6 py-12 text-center text-slate-500">No se encontraron usuarios.</td></tr>
                            ) : filteredUsers.map((user) => (
                                <tr key={user.id} className="hover:bg-slate-800/30 transition-colors group">
                                    <td className="px-6 py-4">
                                        <div className="flex flex-col">
                                            <span className="font-bold text-white">{user.name || "Sin nombre"}</span>
                                            <span className="text-xs text-slate-500">{user.email}</span>
                                            {user.alias && <span className="text-[10px] text-emerald-500 mt-1">@{user.alias}</span>}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex flex-col gap-1">
                                            <div className="flex items-center gap-2">
                                                {user.sub_status === 'active' ? (
                                                    <span className="flex items-center gap-1 text-[10px] font-bold uppercase py-0.5 px-2 rounded-full bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">
                                                        <CheckCircle2 className="w-2.5 h-2.5" /> Activo
                                                    </span>
                                                ) : (
                                                    <span className="flex items-center gap-1 text-[10px] font-bold uppercase py-0.5 px-2 rounded-full bg-slate-800 text-slate-500 border border-slate-700">
                                                        <XCircle className="w-2.5 h-2.5" /> Inactivo
                                                    </span>
                                                )}
                                                <span className="text-xs font-medium text-slate-400 capitalize">{user.tier || "Free"}</span>
                                            </div>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex flex-col">
                                            <span className="text-xs text-slate-300">
                                                {user.expires_at ? new Date(user.expires_at).toLocaleDateString() : "Paquete vitalicio / N/A"}
                                            </span>
                                            {user.expires_at && (
                                                <span className="text-[10px] text-slate-500 flex items-center gap-1">
                                                    <Clock className="w-2.5 h-2.5" /> Expira pronto
                                                </span>
                                            )}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className="text-xs text-slate-400 capitalize">{user.payment_method?.replace('_', ' ') || "—"}</span>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                            <button
                                                onClick={() => setSelectedUser(user)}
                                                className="p-2 text-slate-400 hover:text-emerald-500 hover:bg-emerald-500/10 rounded-lg transition-all"
                                                title="Activar suscripción"
                                            >
                                                <Shield className="w-4 h-4" />
                                            </button>
                                            <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-all">
                                                <Edit className="w-4 h-4" />
                                            </button>
                                            <button className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-all">
                                                <MoreHorizontal className="w-4 h-4" />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Activation Modal */}
            {selectedUser && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
                    <div className="bg-slate-900 border border-slate-800 rounded-3xl w-full max-w-md p-8 shadow-2xl">
                        <h2 className="text-xl font-bold text-white mb-2 flex items-center gap-3">
                            <Shield className="w-6 h-6 text-emerald-500" />
                            Activar Suscripción
                        </h2>
                        <p className="text-sm text-slate-400 mb-8">
                            Otorgando acceso premium a <span className="text-white font-medium">{selectedUser.email}</span>
                        </p>

                        <div className="space-y-6">
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Plan Ético</label>
                                <select
                                    className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm focus:ring-2 focus:ring-emerald-500/50 outline-none"
                                    value={activationTier}
                                    onChange={(e) => setActivationTier(e.target.value)}
                                >
                                    <option value="contributor">Contributor ($25 Base / $8.75 COL)</option>
                                    <option value="enterprise">Enterprise ($200 Base / $70 COL)</option>
                                </select>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Meses</label>
                                    <input
                                        type="number"
                                        min="1"
                                        className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm"
                                        value={activationMonths}
                                        onChange={(e) => setActivationMonths(parseInt(e.target.value))}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Método</label>
                                    <select
                                        className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm"
                                        value={activationMethod}
                                        onChange={(e) => setActivationMethod(e.target.value)}
                                    >
                                        <option value="manual_transfer">Transferencia</option>
                                        <option value="github_sponsors">GitHub</option>
                                        <option value="wompi">Wompi</option>
                                        <option value="crypto">Cripto</option>
                                    </select>
                                </div>
                            </div>

                            <div className="flex gap-4 pt-4">
                                <button
                                    onClick={() => setSelectedUser(null)}
                                    className="flex-1 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-bold transition-all"
                                >
                                    Cancelar
                                </button>
                                <button
                                    onClick={handleActivate}
                                    disabled={isActivating}
                                    className="flex-1 py-3 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-white rounded-xl font-bold transition-all flex items-center justify-center gap-2"
                                >
                                    {isActivating ? "Procesando..." : <><Check className="w-4 h-4" /> Activar Ahora</>}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
