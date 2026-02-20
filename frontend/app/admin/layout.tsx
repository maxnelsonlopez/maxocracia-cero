"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
    LayoutDashboard,
    Users,
    CreditCard,
    Settings,
    ShieldCheck,
    ArrowLeft,
    Activity
} from "lucide-react";

const sidebarLinks = [
    { href: "/admin/dashboard", label: "Vista General", icon: LayoutDashboard },
    { href: "/admin/users", label: "Usuarios", icon: Users },
    { href: "/admin/subscriptions", label: "Suscripciones", icon: CreditCard },
    { href: "/admin/settings", label: "Configuración", icon: Settings },
];

export default function AdminLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const pathname = usePathname();

    return (
        <div className="flex min-h-screen bg-slate-950 text-slate-100">
            {/* Sidebar */}
            <aside className="w-64 border-r border-slate-800 bg-slate-900/50 backdrop-blur-xl fixed h-full z-20">
                <div className="p-6">
                    <Link href="/" className="flex items-center gap-2 mb-8 group">
                        <ArrowLeft className="w-4 h-4 text-slate-400 group-hover:text-emerald-500 transition-colors" />
                        <span className="font-bold text-lg text-white">Panel Admin</span>
                    </Link>

                    <nav className="space-y-1">
                        {sidebarLinks.map((link) => {
                            const isActive = pathname === link.href;
                            const Icon = link.icon;

                            return (
                                <Link
                                    key={link.href}
                                    href={link.href}
                                    className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 ${isActive
                                            ? "bg-emerald-500/10 text-emerald-500 border border-emerald-500/20"
                                            : "text-slate-400 hover:text-white hover:bg-slate-800"
                                        }`}
                                >
                                    <Icon className="w-4 h-4" />
                                    {link.label}
                                </Link>
                            );
                        })}
                    </nav>
                </div>

                <div className="absolute bottom-0 left-0 right-0 p-6">
                    <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
                        <div className="flex items-center gap-3 mb-2">
                            <ShieldCheck className="w-4 h-4 text-emerald-500" />
                            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Estado: Admin</span>
                        </div>
                        <p className="text-[10px] text-slate-500 leading-relaxed uppercase">
                            Simbionte Sintético: Gemini 3 <br />
                            Modo: Coherencia Vital
                        </p>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 ml-64 p-8">
                <header className="mb-8 flex items-center justify-between">
                    <div>
                        <h1 className="text-2xl font-bold text-white mb-1">Maxocracia OS</h1>
                        <p className="text-slate-400 text-sm">Gobernanza y Sostenibilidad Económica</p>
                    </div>
                    <div className="flex items-center gap-4">
                        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-800 border border-slate-700 text-xs text-slate-300">
                            <Activity className="w-3 h-3 text-emerald-500" />
                            <span>Sistema Operativo v4.0</span>
                        </div>
                    </div>
                </header>

                {children}
            </main>
        </div>
    );
}
