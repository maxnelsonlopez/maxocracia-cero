"use client";

import { useState } from "react";
import Link from "next/link";
import { Mail, ArrowLeft, Send } from "lucide-react";
import { Input } from "../components/ui/Input";
import { Button } from "../components/ui/Button";
import { apiFetch } from "../lib/api";

export default function ForgotPage() {
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");
    try {
      const res = await apiFetch("/auth/forgot", {
        method: "POST",
        body: JSON.stringify({ email }),
      });
      if (!res.ok) throw new Error("No se pudo procesar la solicitud");
      // Respuesta siempre genérica (anti-enumeración): se muestra igual
      // exista o no la cuenta.
      setSent(true);
    } catch {
      setError("Error de red. Intenta nuevamente.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative">
      <div className="absolute inset-0 overflow-hidden -z-10 pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-emerald-500/10 rounded-full blur-[100px]" />
      </div>
      <div className="w-full max-w-md">
        <div className="glass-card p-8 relative overflow-hidden">
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-emerald-400 to-cyan-400" />
          <h2 className="text-2xl font-bold text-center text-white mb-2">
            Recupera tu acceso
          </h2>
          <p className="text-center text-slate-400 mb-8 text-sm">
            Sin prisa: te enviamos un enlace de un solo uso, válido por 1 hora.
          </p>
          {sent ? (
            <div className="space-y-4 text-center">
              <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-emerald-300 text-sm">
                Si el correo existe, enviamos instrucciones. Revisa tu bandeja
                (y el spam).
              </div>
              <Link href="/login" className="inline-flex items-center gap-2 text-emerald-400 text-sm font-medium">
                <ArrowLeft className="w-4 h-4" /> Volver a iniciar sesión
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
              <Button type="submit" className="w-full mt-6" isLoading={isLoading}>
                Enviar enlace
                <Send className="w-4 h-4 ml-1" />
              </Button>
              <div className="text-center text-sm text-slate-400">
                <Link href="/login" className="text-emerald-400 hover:text-emerald-300 font-medium">
                  Volver a iniciar sesión
                </Link>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
