import { Suspense } from "react";
import { Metadata } from "next";
import ResetClient from "./ResetClient";

export const metadata: Metadata = {
    title: "Restablece tu contraseña - Maxocracia",
    description:
        "Fija una nueva contraseña con tu enlace de un solo uso (válido por 1 hora).",
};

export default function ResetPage() {
    return (
        <Suspense fallback={<div className="min-h-screen bg-slate-950 flex items-center justify-center text-sm text-slate-500 animate-pulse">Abriendo…</div>}>
            <ResetClient />
        </Suspense>
    );
}
