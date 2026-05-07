"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Zap, ArrowRight, Lock, Mail, User, Shield } from "lucide-react";
import { Input } from "../components/ui/Input";
import { Button } from "../components/ui/Button";
import { useAuth } from "../context/AuthContext";
import { apiFetch } from "../lib/api";

export default function RegisterPage() {
  const [name, setName] = useState("");
  const [alias, setAlias] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      const res = await apiFetch("/auth/register", {
        method: "POST",
        body: JSON.stringify({ name, alias, email, password }),
      });

      const data = await res.json();

      if (res.ok) {
        login(data.access_token);
        router.push("/contracts/builder"); 
      } else {
        setError(data.error || "Error al registrar ciudadano");
      }
    } catch (err) {
      setError("Error de red. Intenta nuevamente.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative pt-24 pb-12">
      {/* Background elements */}
      <div className="absolute inset-0 overflow-hidden -z-10 pointer-events-none">
        <div className="absolute top-1/4 right-1/4 w-[500px] h-[500px] bg-cyan-500/10 rounded-full blur-[100px]" />
        <div className="absolute bottom-1/4 left-1/4 w-[500px] h-[500px] bg-emerald-500/10 rounded-full blur-[100px]" />
      </div>

      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-lg"
      >
        <div className="glass-card p-8 relative overflow-hidden">
          {/* Decoración superior */}
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-emerald-400 to-cyan-400" />
          
          <div className="flex justify-center mb-6">
            <div className="w-12 h-12 bg-emerald-500/10 rounded-xl flex items-center justify-center border border-emerald-500/20">
              <Shield className="w-6 h-6 text-emerald-400" />
            </div>
          </div>
          
          <h2 className="text-2xl font-bold text-center text-white mb-2">
            Registro de Ciudadano
          </h2>
          <p className="text-center text-slate-400 mb-8 text-sm px-4">
            Reclama tu soberanía y únete a la red de contabilidad de la vida.
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-sm text-center">
                {error}
              </div>
            )}
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="relative">
                <Input 
                  label="Nombre Completo" 
                  type="text" 
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Tu nombre"
                  required
                  className="pl-10"
                />
                <User className="w-5 h-5 text-slate-500 absolute left-3 top-9" />
              </div>

              <div className="relative">
                <Input 
                  label="Alias (Opcional)" 
                  type="text" 
                  value={alias}
                  onChange={(e) => setAlias(e.target.value)}
                  placeholder="@alias"
                  className="pl-10"
                />
                <User className="w-5 h-5 text-slate-500 absolute left-3 top-9" />
              </div>
            </div>

            <div className="relative">
              <Input 
                label="Correo Electrónico" 
                type="email" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="tu@email.com"
                required
                className="pl-10"
              />
              <Mail className="w-5 h-5 text-slate-500 absolute left-3 top-9" />
            </div>

            <div className="relative">
              <Input 
                label="Contraseña" 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                minLength={8}
                className="pl-10"
              />
              <Lock className="w-5 h-5 text-slate-500 absolute left-3 top-9" />
              <p className="text-xs text-slate-500 mt-1 ml-1">Mín. 8 caracteres, 1 mayúscula, 1 minúscula y 1 número.</p>
            </div>

            <Button type="submit" className="w-full mt-6" isLoading={isLoading}>
              Crear Identidad
              <ArrowRight className="w-4 h-4 ml-1" />
            </Button>
          </form>

          <div className="mt-6 text-center text-sm text-slate-400">
            ¿Ya tienes una identidad?{" "}
            <Link href="/login" className="text-emerald-400 hover:text-emerald-300 transition-colors font-medium">
              Inicia sesión aquí
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
