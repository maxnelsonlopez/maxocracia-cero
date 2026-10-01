"use client";

import React, { useEffect, useState } from "react";
import { apiFetch } from "../../lib/api";
import {
    Search,
    MoreHorizontal,
    UserPlus,
    Shield,
    CheckCircle2,
    XCircle,
    Clock,
    Eye,
    Check,
    Copy,
    ArrowUpCircle,
    X
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
    created_at: string | null;
    trust_level: number | null;
    is_admin: number | boolean | null;
}

function formatFecha(iso: string | null) {
    if (!iso) return "—";
    try {
        return new Date(iso).toLocaleDateString();
    } catch {
        return iso;
    }
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

    // Menú de 3 puntos + ficha + invitaciones
    const [openMenuId, setOpenMenuId] = useState<number | null>(null);
    const [detailUser, setDetailUser] = useState<AdminUser | null>(null);
    const [inviteModalOpen, setInviteModalOpen] = useState(false);
    const [inviteEmail, setInviteEmail] = useState("");
    const [inviteResult, setInviteResult] = useState<string | null>(null);
    const [inviteLoading, setInviteLoading] = useState(false);
    const [promotingId, setPromotingId] = useState<number | null>(null);

    useEffect(() => {
        fetchUsers();
    }, []);

    async function fetchUsers() {
        try {
            setLoading(true);
            const res = await apiFetch("/subscriptions/admin/users");
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
            const res = await apiFetch("/subscriptions/activate-manual", {
                method: "POST",
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

    async function generateInvite(email: string): Promise<string> {
        const res = await apiFetch("/invite/generate", {
            method: "POST",
            body: JSON.stringify({ email })
        });
        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            throw new Error(data.error || "Error generando invitación");
        }
        const data = await res.json();
        return data.invite_url as string;
    }

    async function copyText(text: string) {
        try {
            await navigator.clipboard.writeText(text);
        } catch {
            const ta = document.createElement("textarea");
            ta.value = text;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand("copy");
            document.body.removeChild(ta);
        }
    }

    async function handleCopyInvite(user: AdminUser) {
        try {
            const url = await generateInvite(user.email);
            const full = window.location.origin.replace(/:\d+$/, ":3000") + url;
            await copyText(`${window.location.origin}${url}`);
            alert(`Invitación lista (copiada): ${url}\nRegistro: /register?email=${user.email}\nOrigen local: ${full}`);
            setOpenMenuId(null);
        } catch (err) {
            alert(err instanceof Error ? err.message : "Error al generar invitación");
        }
    }

    async function handlePromote(user: AdminUser) {
        try {
            setPromotingId(user.id);
            const res = await apiFetch(`/users/${user.id}/trust`, { method: "POST" });
            if (!res.ok) throw new Error("Error ascendiendo confianza");
            await fetchUsers();
            setDetailUser((d) => (d && d.id === user.id ? { ...d, trust_level: 1 } : d));
            setOpenMenuId(null);
        } catch (err) {
            alert(err instanceof Error ? err.message : "Error al ascender");
        } finally {
            setPromotingId(null);
        }
    }

    async function handleInviteNew() {
        if (!inviteEmail.trim()) return;
        try {
            setInviteLoading(true);
            setInviteResult(null);
            const url = await generateInvite(inviteEmail.trim());
            setInviteResult(url);
            await copyText(`${window.location.origin}${url}`);
        } catch (err) {
            alert(err instanceof Error ? err.message : "Error al invitar");
        } finally {
            setInviteLoading(false);
        }
    }

    const filteredUsers = users.filter(u =>
        u.email.toLowerCase().includes(search.toLowerCase()) ||
        (u.name && u.name.toLowerCase().includes(search.toLowerCase())) ||
        (u.alias && u.alias.toLowerCase().includes(search.toLowerCase()))
    );

    return (
        <div className="space-y-6">
            {openMenuId !== null && (
                <div className="fixed inset-0 z-10" onClick={() => setOpenMenuId(null)} />
            )}
            {error && (
                <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-semibold text-center">
                    ⚠️ {error}
                </div>
            )}
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
                    <span className="px-3 py-2 text-xs text-slate-500">
                        {filteredUsers.length} ciudadanos
                    </span>
                    <button
                        onClick={() => { setInviteModalOpen(true); setInviteResult(null); }}
                        className="flex items-center gap-2 px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl text-sm font-medium transition-colors"
                    >
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
                                <th className="px-6 py-4">Registro</th>
                                <th className="px-6 py-4">Suscripción</th>
                                <th className="px-6 py-4">Método</th>
                                <th className="px-6 py-4 text-right">Acciones</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800">
                            {loading ? (
                                <tr><td colSpan={6} className="px-6 py-12 text-center text-slate-500">Cargando ciudadanos...</td></tr>
                            ) : filteredUsers.length === 0 ? (
                                <tr><td colSpan={6} className="px-6 py-12 text-center text-slate-500">No se encontraron usuarios.</td></tr>
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
                                        <div className="flex flex-col gap-1">
                                            <span className="text-xs text-slate-300">{formatFecha(user.created_at)}</span>
                                            <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full border w-fit ${Number(user.trust_level || 0) >= 1 ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" : "bg-amber-500/10 text-amber-400 border-amber-500/20"}`}>
                                                {Number(user.trust_level || 0) >= 1 ? "N1 · voz" : "N0 · llegada"}
                                            </span>
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
                                        <div className="relative flex justify-end gap-2 opacity-100 lg:opacity-0 lg:group-hover:opacity-100 transition-opacity">
                                            <button
                                                onClick={() => setSelectedUser(user)}
                                                className="p-2 text-slate-400 hover:text-emerald-500 hover:bg-emerald-500/10 rounded-lg transition-all"
                                                title="Activar suscripción"
                                            >
                                                <Shield className="w-4 h-4" />
                                            </button>
                                            <button
                                                onClick={() => setDetailUser(user)}
                                                className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-all"
                                                title="Ver ficha"
                                            >
                                                <Eye className="w-4 h-4" />
                                            </button>
                                            <button
                                                onClick={() => setOpenMenuId(openMenuId === user.id ? null : user.id)}
                                                className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-all"
                                                title="Más acciones"
                                            >
                                                <MoreHorizontal className="w-4 h-4" />
                                            </button>
                                            {openMenuId === user.id && (
                                                <div className="absolute right-0 top-10 z-20 w-52 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl overflow-hidden text-left">
                                                    <button
                                                        onClick={() => { setDetailUser(user); setOpenMenuId(null); }}
                                                        className="w-full flex items-center gap-2 px-4 py-2.5 text-xs text-slate-300 hover:bg-slate-800"
                                                    >
                                                        <Eye className="w-3.5 h-3.5" /> Ver ficha completa
                                                    </button>
                                                    <button
                                                        onClick={() => handleCopyInvite(user)}
                                                        className="w-full flex items-center gap-2 px-4 py-2.5 text-xs text-slate-300 hover:bg-slate-800"
                                                    >
                                                        <Copy className="w-3.5 h-3.5" /> Copiar invitación
                                                    </button>
                                                    {Number(user.trust_level || 0) < 1 && (
                                                        <button
                                                            onClick={() => handlePromote(user)}
                                                            disabled={promotingId === user.id}
                                                            className="w-full flex items-center gap-2 px-4 py-2.5 text-xs text-emerald-400 hover:bg-emerald-500/10 disabled:opacity-50"
                                                        >
                                                            <ArrowUpCircle className="w-3.5 h-3.5" /> {promotingId === user.id ? "Ascendiendo..." : "Ascender a N1"}
                                                        </button>
                                                    )}
                                                    <button
                                                        onClick={() => { setSelectedUser(user); setOpenMenuId(null); }}
                                                        className="w-full flex items-center gap-2 px-4 py-2.5 text-xs text-slate-300 hover:bg-slate-800"
                                                    >
                                                        <Shield className="w-3.5 h-3.5" /> Activar suscripción
                                                    </button>
                                                </div>
                                            )}
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Invite Modal */}
            {inviteModalOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
                    <div className="bg-slate-900 border border-slate-800 rounded-3xl w-full max-w-md p-8 shadow-2xl">
                        <div className="flex items-center justify-between mb-2">
                            <h2 className="text-xl font-bold text-white flex items-center gap-3">
                                <UserPlus className="w-6 h-6 text-emerald-500" />
                                Invitar vecino
                            </h2>
                            <button onClick={() => setInviteModalOpen(false)} className="p-2 text-slate-500 hover:text-white">
                                <X className="w-4 h-4" />
                            </button>
                        </div>
                        <p className="text-sm text-slate-400 mb-6">
                            Se genera un link firmado (HMAC). Fase 1: cópialo y envíalo por tu canal. Queda en bitácora.
                        </p>
                        <div className="space-y-4">
                            <input
                                type="email"
                                placeholder="vecina@email.com"
                                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm outline-none focus:ring-2 focus:ring-emerald-500/50"
                                value={inviteEmail}
                                onChange={(e) => setInviteEmail(e.target.value)}
                            />
                            {inviteResult && (
                                <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300 break-all">
                                    {inviteResult} — copiado al portapapeles
                                </div>
                            )}
                            <div className="flex gap-4">
                                <button
                                    onClick={() => setInviteModalOpen(false)}
                                    className="flex-1 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-bold transition-all"
                                >
                                    Cerrar
                                </button>
                                <button
                                    onClick={handleInviteNew}
                                    disabled={inviteLoading || !inviteEmail.trim()}
                                    className="flex-1 py-3 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-white rounded-xl font-bold transition-all flex items-center justify-center gap-2"
                                >
                                    {inviteLoading ? "Generando..." : <><Copy className="w-4 h-4" /> Generar y copiar</>}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Detail Modal */}
            {detailUser && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
                    <div className="bg-slate-900 border border-slate-800 rounded-3xl w-full max-w-md p-8 shadow-2xl">
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-xl font-bold text-white flex items-center gap-3">
                                <Eye className="w-6 h-6 text-emerald-500" />
                                Ficha del ciudadano
                            </h2>
                            <button onClick={() => setDetailUser(null)} className="p-2 text-slate-500 hover:text-white">
                                <X className="w-4 h-4" />
                            </button>
                        </div>
                        <div className="space-y-2 text-sm">
                            <p className="text-white font-bold text-lg">{detailUser.name || "Sin nombre"}</p>
                            <p className="text-slate-400">{detailUser.email}</p>
                            {detailUser.alias && <p className="text-emerald-500 text-xs">@{detailUser.alias}</p>}
                            <div className="pt-3 grid grid-cols-2 gap-3 text-xs">
                                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                                    <p className="text-slate-500 uppercase font-bold text-[10px] mb-1">Registrado desde</p>
                                    <p className="text-white">{formatFecha(detailUser.created_at)}</p>
                                </div>
                                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                                    <p className="text-slate-500 uppercase font-bold text-[10px] mb-1">Confianza</p>
                                    <p className="text-white">{Number(detailUser.trust_level || 0) >= 1 ? "N1 · integrada" : "N0 · recién llegada"}</p>
                                </div>
                                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                                    <p className="text-slate-500 uppercase font-bold text-[10px] mb-1">Rol</p>
                                    <p className="text-white">{detailUser.is_admin ? "Admin" : "Ciudadano"}</p>
                                </div>
                                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                                    <p className="text-slate-500 uppercase font-bold text-[10px] mb-1">Tier</p>
                                    <p className="text-white capitalize">{detailUser.tier || "Free"} · {detailUser.sub_status || "sin suscripción"}</p>
                                </div>
                            </div>
                        </div>
                        <div className="flex gap-3 pt-6">
                            <button
                                onClick={() => handleCopyInvite(detailUser)}
                                className="flex-1 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-bold text-sm flex items-center justify-center gap-2"
                            >
                                <Copy className="w-4 h-4" /> Invitación
                            </button>
                            {Number(detailUser.trust_level || 0) < 1 ? (
                                <button
                                    onClick={() => handlePromote(detailUser)}
                                    disabled={promotingId === detailUser.id}
                                    className="flex-1 py-3 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-white rounded-xl font-bold text-sm"
                                >
                                    {promotingId === detailUser.id ? "Ascendiendo..." : "Ascender a N1"}
                                </button>
                            ) : (
                                <button
                                    onClick={() => { setSelectedUser(detailUser); setDetailUser(null); }}
                                    className="flex-1 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl font-bold text-sm"
                                >
                                    Activar plan
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            )}

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
