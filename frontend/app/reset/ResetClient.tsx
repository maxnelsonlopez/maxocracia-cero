"use client";

import React, { useState } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { Lock, ArrowRight, ShieldCheck } from "lucide-react";
import { Input } from "../components/ui/Input";
import { Button } from "../components/ui/Button";
import { apiFetch } from "../lib/api";

export default function ResetClient() {
    const searchParams = useSearchParams();
    const token = searchParams.get("token") || "";
    const [password, setPassword] = useState("");
    const [confirm, setConfirm] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");
    const [done, setDone] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        if (password !== confirm) {
            setError("Las contraseñas no coinciden.");
            return;
        }
        setIsLoading(true);
        try {
            const res = await apiFetch("/auth/reset", {
                method: "POST",
                body: JSON.stringify({ token, password }),
            });
            const data = await res.json().catch(() => ({}));
            if (!res.ok) throw new Error(data.error || "Enlace inválido o expirado");
            setDone(true);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Error al restablecer");
        } finally {
            setIsLoading(false);
        }
    };

    if (!token) {
        return (
            <div className="min-h-screen flex items-center justify-center p-4">
                <div className="glass-card p-8 max-w-md w-full text-center space-y-3">
                    <h1 className="text-xl font-bold text-white">Enlace incompleto</h1>
                    <p className="text-sm text-slate-400">
                        Abre el enlace completo del correo o pide uno nuevo.
                    </p>
                    <Link href="/forgot" className="inline-block text-emerald-400 text-sm font-medium">
                        Pedir nuevo enlace
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen flex items-center justify-center p-4 relative">
            <div className="absolute inset-0 overflow-hidden -z-10 pointer-events-none">
                <div className="absolute top-1/4 right-1/4 w-[500px] h-[500px] bg-emerald-500/10 rounded-full blur-[100px]" />
            </div>
            <div className="w-full max-w-md">
                <div className="glass-card p-8 relative overflow-hidden">
                    <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-emerald-400 to-cyan-400" />
                    <h2 className="text-2xl font-bold text-center text-white mb-2">
                        Nueva contraseña
                    </h2>
                    <p className="text-center text-slate-400 mb-8 text-sm">
                        Mín. 8 caracteres, 1 mayúscula, 1 minúscula y 1 número.
                    </p>
                    {done ? (
                        <div className="space-y-4 text-center">
                            <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-emerald-300 text-sm flex items-center justify-center gap-2">
                                <ShieldCheck className="w-4 h-4" /> Contraseña actualizada. Tus sesiones anteriores se cerraron.
                            </div>
                            <Link
                                href="/login"
                                className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-bold transition-all"
                            >
                                Entrar ahora <ArrowRight className="w-4 h-4" />
                            </Link>
                        </div>
                    ) : (
                        <form onSubmit={handleSubmit} className="space-y-5">
                            {error && (
                                <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-sm text-center">
                                    {error}
                                </div>
                            )}
                            <div className="relative">
                                <Input
                                    label="Nueva contraseña"
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="••••••••"
                                    required
                                    minLength={8}
                                    className="pl-10"
                                />
                                <Lock className="w-5 h-5 text-slate-500 absolute left-3 top-9" />
                            </div>
                            <div className="relative">
                                <Input
                                    label="Confirma la contraseña"
                                    type="password"
                                    value={confirm}
                                    onChange={(e) => setConfirm(e.target.value)}
                                    placeholder="••••••••"
                                    required
                                    minLength={8}
                                    className="pl-10"
                                />
                                <Lock className="w-5 h-5 text-slate-500 absolute left-3 top-9" />
                            </div>
                            <Button type="submit" className="w-full mt-6" isLoading={isLoading}>
                                Fijar contraseña
                                <ArrowRight className="w-4 h-4 ml-1" />
                            </Button>
                        </form>
                    )}
                </div>
            </div>
        </div>
    );
}
