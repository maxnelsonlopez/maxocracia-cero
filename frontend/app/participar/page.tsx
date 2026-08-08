import { Metadata } from "next";
import ParticiparClient from "./ParticiparClient";

export const metadata: Metadata = {
    title: "Cómo Participar · La Escalera de la Vida Digna - Maxocracia",
    description:
        "Instrucciones para los integrantes humanos de la Maxocracia: cuatro caminos de participación, reglas de oro en lenguaje civil y las reglas que los procesos deben cumplir contigo.",
};

export default function ParticiparPage() {
    return <ParticiparClient />;
}
