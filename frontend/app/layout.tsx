import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Navigation } from "./components/Navigation";
import { Footer } from "./components/Footer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Maxocracia - Sistema Operativo para una Civilización Coherente",
  description: "Reemplaza la contabilidad del dinero por la contabilidad de la vida. Un sistema ético-económico-político basado en el Tiempo Vital Indexado (TVI).",
  keywords: ["maxocracia", "economía ética", "tiempo vital", "VHV", "blockchain ético", "sistema operativo civilización"],
  authors: [{ name: "Max Nelson López" }],
  openGraph: {
    title: "Maxocracia - Contabilidad de la Vida",
    description: "La moneda es tiempo de vida consciente. Nada más, nada menos.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-slate-950 text-slate-100`}
      >
        <Navigation />
        <main className="min-h-screen">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
