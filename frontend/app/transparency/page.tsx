import { Metadata } from "next";
import TransparencyClient from "./TransparencyClient";

export const metadata: Metadata = {
    title: "Transparencia Radical - Maxocracia",
    description:
        "Reporte público de flujos financieros de Maxocracia. Principio T13: todos los flujos son visibles y auditables.",
};

export default function TransparencyPage() {
    return <TransparencyClient />;
}
