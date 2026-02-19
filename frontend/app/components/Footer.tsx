"""
Componente Footer - Maxocracia
===============================

Footer con:
- Links a secciones
- Reporte de transparencia
- Axiomas
- Créditos

Autor: Kimi (Moonshot AI)
"""

import Link from "next/link";
import { 
  Heart, 
  Github, 
  Twitter, 
  Mail,
  ExternalLink,
  Scale
} from "lucide-react";

const footerLinks = {
  proyecto: [
    { label: "Libro Completo", href: "https://github.com/maxnelsonlopez/maxocracia-cero/blob/main/docs/book/edicion_3_dinamica/libro_completo_310126.md" },
    { label: "API Docs", href: "http://localhost:5001/admin" },
    { label: "Changelog", href: "https://github.com/maxnelsonlopez/maxocracia-cero/blob/main/CHANGELOG.md" },
  ],
  comunidad: [
    { label: "GitHub Discussions", href: "#" },
    { label: "Cohorte Cero", href: "#" },
    { label: "Contribuir", href: "/upgrade" },
  ],
  legal: [
    { label: "Transparencia", href: "http://localhost:5001/subscriptions/transparency-report" },
    { label: "Privacidad", href: "#" },
    { label: "Términos", href: "#" },
  ],
};

const axioms = [
  { id: "T2", text: "Igualdad Temporal" },
  { id: "T7", text: "Minimizar Daño" },
  { id: "T9", text: "Reciprocidad Justa" },
  { id: "T13", text: "Transparencia Radical" },
];

export function Footer() {
  return (
    <footer className="bg-slate-950 border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 mb-12">
          {/* Brand */}
          <div className="lg:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center">
                <Scale className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-lg text-white">Maxocracia</span>
            </div>
            <p className="text-slate-400 text-sm mb-4 max-w-sm">
              Un sistema operativo para una civilización coherente. 
              Basado en el principio de que el tiempo de vida consciente 
              es el recurso más escaso del universo.
            </p>
            
            {/* Axioms */}
            <div className="flex flex-wrap gap-2">
              {axioms.map((axiom) => (
                <span
                  key={axiom.id}
                  className="px-2 py-1 bg-slate-900 border border-slate-800 rounded text-xs text-slate-400"
                  title={axiom.text}
                >
                  {axiom.id}
                </span>
              ))}
            </div>
          </div>

          {/* Links */}
          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h4 className="font-semibold text-white mb-4 capitalize">{category}</h4>
              <ul className="space-y-2">
                {links.map((link) => (
                  <li key={link.label}>
                    <FooterLink {...link} />
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom */}
        <div className="pt-8 border-t border-slate-800 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-slate-500 text-sm">
            © {new Date().getFullYear()} Maxocracia. Licencia MIT / CC BY-SA 4.0
          </p>
          
          <div className="flex items-center gap-4">
            <a
              href="https://github.com/maxnelsonlopez/maxocracia-cero"
              target="_blank"
              rel="noopener noreferrer"
              className="text-slate-400 hover:text-white transition-colors"
            >
              <Github className="w-5 h-5" />
            </a>
            <a
              href="mailto:maxlopeztutor@gmail.com"
              className="text-slate-400 hover:text-white transition-colors"
            >
              <Mail className="w-5 h-5" />
            </a>
          </div>
        </div>

        {/* Quote */}
        <div className="mt-8 text-center">
          <p className="text-slate-600 text-sm italic">
            "La verdad no necesita ser defendida. Solo necesita expandirse."
          </p>
          <p className="text-slate-700 text-xs mt-1">— Axioma 4, Maxocracia</p>
        </div>
      </div>
    </footer>
  );
}

function FooterLink({ label, href }: { label: string; href: string }) {
  const isExternal = href.startsWith("http");
  
  if (isExternal) {
    return (
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="text-sm text-slate-400 hover:text-emerald-400 transition-colors flex items-center gap-1"
      >
        {label}
        <ExternalLink className="w-3 h-3" />
      </a>
    );
  }

  return (
    <Link
      href={href}
      className="text-sm text-slate-400 hover:text-emerald-400 transition-colors"
    >
      {label}
    </Link>
  );
}
