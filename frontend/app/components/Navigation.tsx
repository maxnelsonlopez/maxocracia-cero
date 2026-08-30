/*
 * Componente de Navegación - Maxocracia
 * ======================================
 * 
 * Navegación principal con:
 * - Logo y marca
 * - Links a secciones principales
 * - Badge de suscripción
 * - Botón de contribuir
 * - Modo responsive
 * 
 * Autor: Kimi (Moonshot AI)
 */

"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  Menu,
  X,
  Zap,
  Calculator,
  FileText,
  Users,
  Heart,
  Sparkles,
  Github,
  LogOut,
  LogIn,
  UserPlus,
  ClipboardList,
  Handshake,
  Activity,
  BarChart3,
  ChevronDown,
  Vote,
  Compass,
  MessagesSquare,
  GraduationCap
} from "lucide-react";
import { ContributorBadge } from "./ContributorBadge";
import { useAuth } from "../context/AuthContext";

const navSections = [
  {
    label: "Operaciones",
    links: [
      { href: "/forms/cero", label: "Inscripción", icon: ClipboardList },
      { href: "/forms/exchange", label: "Intercambio", icon: Handshake },
      { href: "/forms/follow-up", label: "Seguimiento", icon: Activity },
    ]
  },
  {
    label: "Inteligencia",
    links: [
      { href: "/vhv/calculator", label: "VHV Calc", icon: Calculator },
      { href: "/vhv/comparison", label: "Comparador", icon: BarChart3 },
      { href: "/tvi/stats", label: "TVI Stats", icon: Activity },
    ]
  },
  {
    label: "Contratos",
    links: [
      { href: "/contracts/builder", label: "Builder", icon: Zap },
      { href: "/contracts", label: "Lista", icon: FileText },
    ]
  },
  {
    label: "Aprendizaje",
    links: [
      { href: "/foro", label: "Foro Abierto", icon: MessagesSquare },
      { href: "/talleres", label: "Talleres", icon: GraduationCap },
      { href: "/grupos", label: "Grupos y Células", icon: Users },
    ]
  },
];

// Nodo educativo del OEV (espejo del default del backend `EDUCATIONAL_PLATFORM_URL`).
const OEV_URL = process.env.NEXT_PUBLIC_EDU_PLATFORM_URL || "http://localhost:5050";

// Puerta del OEV (:5050): el JWT viaja en el FRAGMENTO de la URL (#jwt=...),
// que nunca llega al servidor (no queda en logs); el nodo lo captura una vez
// y lo usa como identidad federada (M12).
function enterOevNode() {
  const token =
    typeof window !== "undefined" ? localStorage.getItem("mc_access_token") : null;
  const fragment = token ? `#jwt=${encodeURIComponent(token)}` : "";
  window.location.href = `${OEV_URL}/${fragment}`;
}

export function Navigation() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const { isAuthenticated, user, logout } = useAuth();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <>
      <motion.header
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled
            ? "glass border-t-0 border-x-0"
            : "bg-transparent"
          }`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link href="/" className="flex items-center gap-2 group">
              <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-lg text-white">
                Maxocracia
              </span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-1">
              <Link href="/" className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-slate-800 transition-all">
                Inicio
              </Link>
              
              {navSections.map((section) => (
                <NavDropdown key={section.label} section={section} />
              ))}

              {isAuthenticated && (
                <Link href="/pulso" className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-violet-400 hover:text-violet-300 hover:bg-violet-950/20 transition-all border border-violet-500/20 mr-1 shadow-lg shadow-violet-500/5">
                  <Activity className="w-3.5 h-3.5" />
                  Pulso Vital
                </Link>
              )}

              {isAuthenticated && (
                <Link href="/matching" className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-emerald-400 hover:text-emerald-300 hover:bg-emerald-950/20 transition-all border border-emerald-500/20 mr-1 shadow-lg shadow-emerald-500/5">
                  Plaza de Apoyo
                </Link>
              )}

              {isAuthenticated && (
                <Link href="/votaciones" className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-emerald-400 hover:text-emerald-300 hover:bg-emerald-950/20 transition-all border border-emerald-500/20 mr-1 shadow-lg shadow-emerald-500/5">
                  Votaciones
                </Link>
              )}

              {isAuthenticated && (
                <Link href="/guia" className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-violet-400 hover:text-violet-300 hover:bg-violet-950/20 transition-all border border-violet-500/20 mr-1 shadow-lg shadow-violet-500/5">
                  <Compass className="w-3.5 h-3.5" />
                  Guía
                </Link>
              )}

              {isAuthenticated && (
                <button
                  onClick={enterOevNode}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-emerald-400 hover:text-emerald-300 hover:bg-emerald-950/20 transition-all border border-emerald-500/20 mr-1 shadow-lg shadow-emerald-500/5 cursor-pointer"
                  title="Entrar al nodo educativo con tu identidad (una sola puerta)"
                >
                  <GraduationCap className="w-3.5 h-3.5" />
                  Nodo Educativo
                </button>
              )}

              {isAuthenticated && (
                <Link href="/perfil" className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-amber-400 hover:text-amber-300 hover:bg-amber-950/20 transition-all border border-amber-500/20 mr-1 shadow-lg shadow-amber-500/5">
                  Perfil Vital
                </Link>
              )}

              {isAuthenticated && (
                <Link href="/admin/dashboard" className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-slate-800 transition-all">
                  Admin
                </Link>
              )}
            </nav>

            {/* Right Side */}
            <div className="hidden md:flex items-center gap-4">
              <Link href="/upgrade" className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold bg-emerald-500 text-white hover:bg-emerald-600 transition-all shadow-lg shadow-emerald-500/20 active:scale-95">
                <Heart className="w-4 h-4" />
                Contribuir
              </Link>
              
              <div className="h-6 w-[1px] bg-slate-800 mx-2" />
              
              {isAuthenticated ? (
                <div className="flex items-center gap-3 ml-2">
                  <span className="text-sm font-medium text-emerald-400">
                    {user?.alias || user?.name?.split(' ')[0]}
                  </span>
                  <button
                    onClick={logout}
                    className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
                  >
                    <LogOut className="w-4 h-4" />
                    Salir
                  </button>
                </div>
              ) : (
                <div className="flex items-center gap-2 ml-2">
                  <Link
                    href="/login"
                    className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800 transition-all"
                  >
                    <LogIn className="w-4 h-4" />
                    Entrar
                  </Link>
                  <Link
                    href="/register"
                    className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 transition-all"
                  >
                    <UserPlus className="w-4 h-4" />
                    Registro
                  </Link>
                </div>
              )}

              <Link
                href="https://github.com/maxnelsonlopez/maxocracia-cero"
                target="_blank"
                rel="noopener noreferrer"
                className="text-slate-400 hover:text-white transition-colors ml-2"
              >
                <Github className="w-5 h-5" />
              </Link>
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden p-2 text-slate-300 hover:text-white"
            >
              {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </motion.header>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, x: "100%" }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: "100%" }}
            transition={{ type: "tween", duration: 0.3 }}
            className="fixed inset-0 z-40 md:hidden"
          >
            <div className="absolute inset-0 bg-slate-950/95 backdrop-blur-lg" />
            <nav className="absolute top-16 left-0 right-0 bottom-0 p-6 overflow-y-auto flex flex-col gap-6">
              <Link 
                href="/" 
                className="flex items-center gap-3 px-4 py-3 rounded-xl text-lg font-bold text-white bg-slate-900 border border-slate-800"
                onClick={() => setIsOpen(false)}
              >
                <Sparkles className="w-5 h-5 text-amber-400" />
                Inicio
              </Link>

              {navSections.map((section) => (
                <div key={section.label} className="space-y-3">
                  <h3 className="px-4 text-[10px] font-black uppercase tracking-[0.2em] text-slate-500">
                    {section.label}
                  </h3>
                  <div className="grid grid-cols-1 gap-1">
                    {section.links.map((link) => (
                      <MobileNavLink key={link.href} {...link} onClick={() => setIsOpen(false)} />
                    ))}
                  </div>
                </div>
              ))}

              {isAuthenticated && (
                <div className="space-y-3">
                  <h3 className="px-4 text-[10px] font-black uppercase tracking-[0.2em] text-slate-500">
                    Comunidad
                  </h3>
                  <MobileNavLink href="/pulso" label="Pulso Vital" icon={Activity} onClick={() => setIsOpen(false)} />
                  <MobileNavLink href="/matching" label="Plaza de Apoyo" icon={Handshake} onClick={() => setIsOpen(false)} />
                  <MobileNavLink href="/votaciones" label="Votaciones" icon={Vote} onClick={() => setIsOpen(false)} />
                  <MobileNavLink href="/guia" label="Guía de la Maxocracia" icon={Compass} onClick={() => setIsOpen(false)} />
                  <MobileNavLink href="/foro" label="Foro Abierto" icon={MessagesSquare} onClick={() => setIsOpen(false)} />
                  <MobileNavLink href="/talleres" label="Talleres de Aprendizaje" icon={GraduationCap} onClick={() => setIsOpen(false)} />
                  <MobileNavLink href="/grupos" label="Grupos y Células" icon={Users} onClick={() => setIsOpen(false)} />
                  <button
                    onClick={() => {
                      setIsOpen(false);
                      enterOevNode();
                    }}
                    className="flex items-center gap-3 px-4 py-3 rounded-xl text-lg font-medium text-emerald-300 hover:text-white hover:bg-slate-800 transition-all duration-200 text-left w-full"
                  >
                    <GraduationCap className="w-5 h-5 text-emerald-500" />
                    Nodo Educativo (plaza viva)
                  </button>
                  <MobileNavLink href="/perfil" label="Perfil Vital" icon={Heart} onClick={() => setIsOpen(false)} />
                </div>
              )}

              {isAuthenticated && (
                <div className="space-y-3">
                  <h3 className="px-4 text-[10px] font-black uppercase tracking-[0.2em] text-slate-500">
                    Administración
                  </h3>
                  <MobileNavLink href="/admin/dashboard" label="Dashboard Maestro" icon={Users} onClick={() => setIsOpen(false)} />
                </div>
              )}

              <div className="mt-auto pt-6 flex flex-col gap-4">
                <Link 
                  href="/upgrade" 
                  className="flex items-center justify-center gap-2 p-4 rounded-2xl bg-emerald-500 text-white font-bold"
                  onClick={() => setIsOpen(false)}
                >
                  <Heart className="w-5 h-5" />
                  Contribuir al Proyecto
                </Link>
                <ContributorBadge />
              </div>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Spacer */}
      <div className="h-16" />
    </>
  );
}

function NavDropdown({ section }: { section: typeof navSections[0] }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div 
      className="relative"
      onMouseEnter={() => setIsOpen(true)}
      onMouseLeave={() => setIsOpen(false)}
    >
      <button className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
        isOpen ? "text-white bg-slate-800" : "text-slate-400 hover:text-white hover:bg-slate-800"
      }`}>
        {section.label}
        <ChevronDown className={`w-3 h-3 transition-transform duration-300 ${isOpen ? 'rotate-180 text-emerald-500' : ''}`} />
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="absolute top-full left-0 mt-1 w-52 glass border border-slate-800 rounded-xl overflow-hidden shadow-2xl z-50 p-2"
          >
            <div className="flex flex-col gap-1">
              {section.links.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setIsOpen(false)}
                  className="flex items-center gap-3 px-4 py-3 text-sm text-slate-300 hover:text-white hover:bg-white/5 transition-all group"
                >
                  <link.icon className="w-4 h-4 text-slate-500 group-hover:text-emerald-500 transition-colors" />
                  {link.label}
                </Link>
              ))}
              {section.label === "Aprendizaje" && (
                <button
                  onClick={() => {
                    setIsOpen(false);
                    enterOevNode();
                  }}
                  className="flex items-center gap-3 px-4 py-3 text-sm text-emerald-300 hover:text-white hover:bg-white/5 transition-all group w-full text-left"
                >
                  <GraduationCap className="w-4 h-4 text-emerald-500 group-hover:text-emerald-400 transition-colors" />
                  Nodo Educativo (una sola puerta)
                </button>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function MobileNavLink({ href, label, icon: Icon, external, onClick }: {
  href: string;
  label: string;
  icon: React.ElementType;
  external?: boolean;
  onClick?: () => void;
}) {
  const baseClasses = `
    flex items-center gap-3 px-4 py-3 rounded-xl text-lg font-medium
    transition-all duration-200
    text-slate-300 hover:text-white hover:bg-slate-800
  `;

  if (external) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" className={baseClasses} onClick={onClick}>
        <Icon className="w-5 h-5 text-emerald-500" />
        {label}
      </a>
    );
  }

  return (
    <Link href={href} className={baseClasses} onClick={onClick}>
      <Icon className="w-5 h-5 text-emerald-500" />
      {label}
    </Link>
  );
}


