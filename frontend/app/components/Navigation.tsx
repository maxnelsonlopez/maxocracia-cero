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
  Github
} from "lucide-react";
import { ContributorBadge } from "./ContributorBadge";

const navLinks = [
  { href: "/", label: "Inicio", icon: Sparkles },
  { href: "/upgrade", label: "Contribuir", icon: Heart },
  { href: "/contracts/builder", label: "Contratos", icon: FileText },
  { href: "http://localhost:5001/admin", label: "Dashboard", icon: Users, external: true },
  { href: "http://localhost:5001/vhv-calculator.html", label: "VHV Calc", icon: Calculator, external: true },
];

export function Navigation() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

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
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          scrolled
            ? "bg-slate-950/80 backdrop-blur-lg border-b border-slate-800"
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
              {navLinks.map((link) => (
                <NavLink key={link.href} {...link} />
              ))}
            </nav>

            {/* Right Side */}
            <div className="hidden md:flex items-center gap-4">
              <ContributorBadge size="sm" />
              <Link
                href="https://github.com/maxnelsonlopez/maxocracia-cero"
                target="_blank"
                rel="noopener noreferrer"
                className="text-slate-400 hover:text-white transition-colors"
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
            <nav className="absolute top-16 left-0 right-0 bottom-0 p-6 flex flex-col gap-2">
              {navLinks.map((link, index) => (
                <motion.div
                  key={link.href}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <MobileNavLink {...link} onClick={() => setIsOpen(false)} />
                </motion.div>
              ))}
              
              <div className="mt-6 pt-6 border-t border-slate-800">
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

function NavLink({ href, label, icon: Icon, external }: {
  href: string;
  label: string;
  icon: React.ElementType;
  external?: boolean;
}) {
  const baseClasses = `
    flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium
    transition-all duration-200
    text-slate-400 hover:text-white hover:bg-slate-800
  `;

  if (external) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" className={baseClasses}>
        <Icon className="w-4 h-4" />
        {label}
      </a>
    );
  }

  return (
    <Link href={href} className={baseClasses}>
      <Icon className="w-4 h-4" />
      {label}
    </Link>
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
