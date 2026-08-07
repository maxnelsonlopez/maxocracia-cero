import { Metadata } from "next";
import VerificadorClient from "./VerificadorClient";

export const metadata: Metadata = {
    title: "Plaza Pública · Verificador Ciudadano - Maxocracia",
    description:
        "Audita la integridad de un contrato por su hash canónico y mira el bienestar agregado de la Cohorte Cero. Sin login: T13, transparencia radical.",
};

export default function VerificadorPage() {
    return <VerificadorClient />;
}
