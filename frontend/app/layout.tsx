import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Navigation } from "./components/Navigation";
import { Footer } from "./components/Footer";
import { AuthProvider } from "./context/AuthContext";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Maxocracia-Cero | Tiempo vital, cuidado y reciprocidad",
  description: "Un sistema abierto para organizar el valor alrededor del tiempo de vida, el cuidado y la reciprocidad. Explora los axiomas, prueba el código o únete a la Red de Apoyo.",
  keywords: ["maxocracia", "economía ética", "tiempo vital", "VHV", "blockchain ético", "sistema operativo civilización"],
  authors: [{ name: "Max Nelson López" }],
  openGraph: {
    title: "Maxocracia-Cero | Una contabilidad de la vida",
    description: "Un sistema ético, económico y político en construcción: código abierto, voluntario y auditable.",
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
        <AuthProvider>
          <Navigation />
          <main className="min-h-screen">
            {children}
          </main>
          <Footer />
        </AuthProvider>
      </body>
    </html>
  );
}
