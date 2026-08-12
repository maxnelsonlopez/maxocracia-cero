import { Suspense } from "react";
import { Metadata } from "next";
import InviteClient from "./InviteClient";

export const metadata: Metadata = {
    title: "Invitación a la Cohorte - Maxocracia",
    description:
        "Has sido invitado a la Cohorte Cero. No hay prisa: primero tu pulso, luego tu acuerdo. La voz en la gobernanza llega con el tiempo.",
};

export default function InvitePage() {
    return (
        <Suspense fallback={<div className="min-h-screen bg-slate-950 flex items-center justify-center text-sm text-slate-500 animate-pulse">Abriendo la puerta…</div>}>
            <InviteClient />
        </Suspense>
    );
}
