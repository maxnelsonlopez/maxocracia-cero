"use client";

import React, { useEffect, useState } from "react";
import { apiFetch } from "../../lib/api";
import {
  Search,
  Package,
  Eye,
  X,
  AlertTriangle,
  Plus,
  Layers,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface VHVProduct {
  id: number;
  name?: string;
  category?: string;
  description?: string;
  vhv?: { T?: number; V?: number; R?: number } | null;
  maxo_price?: number;
  created_at?: string;
  components?: {
    T: Record<string, number>;
    V: Record<string, number>;
    R: Record<string, number>;
  };
}

function fmt(n?: number) {
  if (n === undefined || n === null) return "—";
  const rounded = Math.round(n * 100) / 100;
  return Number.isInteger(rounded) ? String(rounded) : String(rounded);
}

export default function AdminVHVProducts() {
  const [products, setProducts] = useState<VHVProduct[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState<string>("all");
  const [offset, setOffset] = useState(0);
  const limit = 50;

  const [selected, setSelected] = useState<VHVProduct | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  useEffect(() => {
    fetchProducts();
  }, [categoryFilter, offset]);

  async function fetchProducts() {
    try {
      setLoading(true);
      let url = `/vhv/products?limit=${limit}&offset=${offset}`;
      if (categoryFilter !== "all") {
        url += `&category=${encodeURIComponent(categoryFilter)}`;
      }
      const res = await apiFetch(url);
      if (!res.ok) throw new Error("Error cargando productos VHV");
      const data = await res.json();
      setProducts(data.products || []);
      setTotal(data.total || 0);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setLoading(false);
    }
  }

  const categories = Array.from(new Set(products.map((p) => p.category || "").filter(Boolean))).sort();

  const displayed = products.filter((p) => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return (
      (p.name || "").toLowerCase().includes(q) ||
      (p.category || "").toLowerCase().includes(q) ||
      (p.description || "").toLowerCase().includes(q) ||
      String(p.id).includes(q)
    );
  });

  const handleDetail = async (p: VHVProduct) => {
    setSelected(p);
    setDetailLoading(true);
    try {
      const res = await apiFetch(`/vhv/products/${p.id}`);
      if (res.ok) {
        const data = await res.json();
        setSelected(data);
      }
    } catch {
      setDetailLoading(false);
      setSelected(p);
      return;
    } finally {
      setDetailLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 text-[11px] font-semibold w-fit">
        <AlertTriangle className="w-3.5 h-3.5" />
        Solo lectura (el backend no expone PUT/DELETE para productos); creación vía /vhv/calculate (gap RF-G4)
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-450 text-xs font-semibold text-center">
          {error}
        </div>
      )}

      <div className="flex flex-col lg:flex-row gap-4 justify-between items-center bg-slate-900/50 p-4 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="relative w-full lg:w-96">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Buscar por nombre, categoría o descripción..."
            className="w-full bg-slate-950 border border-slate-850 rounded-xl py-2.5 pl-10 pr-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-all"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <div className="flex flex-wrap gap-2 w-full lg:w-auto justify-end items-center">
          <div className="flex items-center bg-slate-950 border border-slate-850 rounded-xl px-3 py-1">
            <span className="text-xs text-slate-500 mr-2">Categoría:</span>
            <select
              className="bg-transparent text-xs text-slate-300 focus:outline-none py-1 cursor-pointer font-medium"
              value={categoryFilter}
              onChange={(e) => {
                setCategoryFilter(e.target.value);
                setOffset(0);
              }}
            >
              <option value="all" className="bg-slate-950 text-slate-300">Todas</option>
              {categories.map((c) => (
                <option key={c} value={c} className="bg-slate-950 text-slate-300">{c}</option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-1.5">
            <button
              onClick={() => setOffset(Math.max(0, offset - limit))}
              disabled={offset === 0}
              className="px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs font-bold text-slate-300 hover:border-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            >
              Anterior
            </button>
            <button
              onClick={() => setOffset(offset + limit)}
              disabled={offset + limit >= total}
              className="px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs font-bold text-slate-300 hover:border-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            >
              Siguiente
            </button>
          </div>

          <a
            href="/vhv/calculator"
            className="flex items-center gap-2 px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 rounded-xl text-xs font-bold transition-all hover:scale-[1.02]"
          >
            <Plus className="w-4 h-4" />
            Crear Producto
          </a>
        </div>
      </div>

      <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-800/40 text-slate-450 uppercase text-[10px] font-bold tracking-wider border-b border-slate-850">
              <tr>
                <th className="px-6 py-4">Producto</th>
                <th className="px-6 py-4">Categoría</th>
                <th className="px-6 py-4">VHV (T / V / R)</th>
                <th className="px-6 py-4">Precio Maxo</th>
                <th className="px-6 py-4">Creado</th>
                <th className="px-6 py-4 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-850">
              {loading ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-slate-500 font-medium">
                    Cargando productos VHV...
                  </td>
                </tr>
              ) : displayed.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-slate-500 font-medium">
                    No se encontraron productos.
                  </td>
                </tr>
              ) : (
                displayed.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-800/20 transition-colors group">
                    <td className="px-6 py-4">
                      <div className="flex flex-col">
                        <span className="font-extrabold text-white text-sm">{p.name || `Producto #${p.id}`}</span>
                        <p className="text-xs text-slate-350 line-clamp-1 max-w-xs">{p.description || "—"}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-[10px] bg-slate-950 text-slate-400 border border-slate-800 px-2 py-0.5 rounded uppercase">
                        {p.category || "sin categoría"}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex gap-1.5">
                        <span className="text-[9px] font-black px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20">
                          T {fmt(p.vhv?.T)}
                        </span>
                        <span className="text-[9px] font-black px-2 py-0.5 rounded bg-rose-500/10 text-rose-450 border border-rose-500/20">
                          V {fmt(p.vhv?.V)}
                        </span>
                        <span className="text-[9px] font-black px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">
                          R {fmt(p.vhv?.R)}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm font-bold text-emerald-400">
                        {p.maxo_price === undefined || p.maxo_price === null ? "—" : `${fmt(p.maxo_price)} maxo`}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-xs text-slate-500">{p.created_at || "—"}</span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={() => handleDetail(p)}
                          className="p-2 text-slate-400 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-xl transition-all"
                          title="Ver detalle del producto"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      <AnimatePresence>
        {selected && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelected(null)}
              className="absolute inset-0"
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="bg-slate-900 border border-slate-850 rounded-3xl w-full max-w-2xl overflow-hidden shadow-2xl relative z-10 flex flex-col max-h-[90vh]"
            >
              <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-emerald-500/0 via-emerald-500 to-emerald-500/0" />
              <div className="flex items-center justify-between p-6 border-b border-slate-850">
                <div>
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <Package className="w-5 h-5 text-emerald-400" />
                    {selected.name || `Producto #${selected.id}`}
                  </h3>
                  <p className="text-xs text-slate-400 mt-1">
                    #{selected.id} · {selected.category || "sin categoría"} · {selected.created_at || ""}
                  </p>
                </div>
                <button
                  onClick={() => setSelected(null)}
                  className="p-2 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {detailLoading ? (
                  <div className="py-10 text-center text-slate-500 text-xs font-medium">
                    Cargando desglose completo...
                  </div>
                ) : (
                  <>
                    <div className="grid grid-cols-3 gap-4">
                      <div className="p-4 rounded-xl bg-sky-500/5 border border-sky-500/20 text-center">
                        <p className="text-[9px] font-black uppercase tracking-wider text-sky-400">T · Tiempo</p>
                        <p className="text-2xl font-black text-white mt-1">{fmt(selected.vhv?.T)}</p>
                      </div>
                      <div className="p-4 rounded-xl bg-rose-500/5 border border-rose-500/20 text-center">
                        <p className="text-[9px] font-black uppercase tracking-wider text-rose-450">V · Vida</p>
                        <p className="text-2xl font-black text-white mt-1">{fmt(selected.vhv?.V)}</p>
                      </div>
                      <div className="p-4 rounded-xl bg-amber-500/5 border border-amber-500/20 text-center">
                        <p className="text-[9px] font-black uppercase tracking-wider text-amber-400">R · Recursos</p>
                        <p className="text-2xl font-black text-white mt-1">{fmt(selected.vhv?.R)}</p>
                      </div>
                    </div>

                    <div className="p-4 rounded-xl bg-emerald-500/5 border border-emerald-500/20 flex items-center justify-between">
                      <div>
                        <p className="text-[9px] font-black uppercase tracking-wider text-emerald-400">
                          Precio Maxo
                        </p>
                        <p className="text-sm text-slate-300 mt-1">{selected.maxo_price ?? "—"}</p>
                      </div>
                      <Layers className="w-5 h-5 text-emerald-400" />
                    </div>

                    {selected.description && (
                      <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                        <p className="text-[9px] font-black uppercase tracking-wider text-slate-500">Descripción</p>
                        <p className="text-sm text-slate-300 mt-2 leading-relaxed">{selected.description}</p>
                      </div>
                    )}

                    {selected.components && (
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {(["T", "V", "R"] as const).map((comp) => (
                          <div key={comp} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                            <p className="text-[9px] font-black uppercase tracking-wider text-slate-500">
                              Componente {comp}
                            </p>
                            <div className="mt-2 space-y-1">
                              {Object.entries(selected.components![comp] || {}).map(([key, val]) => (
                                <div key={key} className="flex justify-between text-xs">
                                  <span className="text-slate-500">{key.replace(/_/g, " ")}</span>
                                  <span className="text-white font-semibold">{fmt(val)}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </>
                )}
              </div>

              <div className="p-6 border-t border-slate-850 bg-slate-950/20 flex justify-end">
                <button
                  type="button"
                  onClick={() => setSelected(null)}
                  className="px-5 py-2.5 bg-slate-950 hover:bg-slate-900 border border-slate-800 rounded-xl text-slate-350 hover:text-white transition-all text-xs font-bold"
                >
                  Cerrar
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
