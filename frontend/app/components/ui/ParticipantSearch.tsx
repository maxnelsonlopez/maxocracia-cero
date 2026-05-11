import React, { useState, useEffect, useRef } from "react";
import { apiFetch } from "../../lib/api";
import { Search, User, X, Loader2 } from "lucide-react";

interface Participant {
  id: number;
  name: string;
  email: string;
  city: string;
}

interface ParticipantSearchProps {
  label: string;
  onSelect: (participant: Participant | null) => void;
  selectedParticipant: Participant | null;
  error?: string;
}

export const ParticipantSearch: React.FC<ParticipantSearchProps> = ({
  label,
  onSelect,
  selectedParticipant,
  error,
}) => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Participant[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  useEffect(() => {
    const delayDebounceFn = setTimeout(async () => {
      if (query.length >= 2) {
        setIsSearching(true);
        setIsOpen(true);
        try {
          const response = await apiFetch(`/forms/participants?search=${encodeURIComponent(query)}&limit=5`);
          if (response.ok) {
            const data = await response.json();
            setResults(data.participants || []);
          }
        } catch (err) {
          console.error("Error searching participants:", err);
        } finally {
          setIsSearching(false);
        }
      } else {
        setResults([]);
        setIsOpen(false);
      }
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [query]);

  if (selectedParticipant) {
    return (
      <div className="flex flex-col gap-1 w-full">
        <label className="text-sm font-medium text-slate-300 ml-1">{label}</label>
        <div className="flex items-center justify-between p-4 bg-emerald-500/10 border border-emerald-500/50 rounded-xl text-emerald-400">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-emerald-500/20 rounded-full flex items-center justify-center">
              <User size={16} />
            </div>
            <div>
              <p className="font-bold text-sm">{selectedParticipant.name}</p>
              <p className="text-[10px] opacity-70">{selectedParticipant.email} • {selectedParticipant.city}</p>
            </div>
          </div>
          <button
            onClick={() => {
              onSelect(null);
              setQuery("");
            }}
            className="p-1 hover:bg-emerald-500/20 rounded-full transition-all"
          >
            <X size={16} />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-1 w-full relative" ref={dropdownRef}>
      <label className="text-sm font-medium text-slate-300 ml-1">{label}</label>
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => query.length >= 2 && setIsOpen(true)}
          placeholder="Buscar por nombre o correo..."
          className={`w-full px-4 py-3 bg-slate-900/50 backdrop-blur-md border rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 transition-all pl-11 ${
            error ? "border-red-500/50" : "border-slate-800 focus:border-emerald-500/50"
          }`}
        />
        <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500">
          {isSearching ? <Loader2 size={18} className="animate-spin" /> : <Search size={18} />}
        </div>
      </div>

      {isOpen && results.length > 0 && (
        <div className="absolute z-50 top-full left-0 right-0 mt-2 bg-slate-900 border border-slate-800 rounded-xl shadow-2xl overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200">
          {results.map((p) => (
            <button
              key={p.id}
              onClick={() => {
                onSelect(p);
                setIsOpen(false);
              }}
              className="w-full flex items-center gap-3 p-4 hover:bg-slate-800 transition-all text-left border-b border-slate-800/50 last:border-0"
            >
              <div className="w-8 h-8 bg-slate-800 rounded-full flex items-center justify-center text-slate-400 group-hover:bg-emerald-500/20 group-hover:text-emerald-400 transition-all">
                <User size={16} />
              </div>
              <div>
                <p className="font-bold text-sm text-slate-100">{p.name}</p>
                <p className="text-[10px] text-slate-500">{p.email} • {p.city}</p>
              </div>
            </button>
          ))}
        </div>
      )}

      {isOpen && query.length >= 2 && !isSearching && results.length === 0 && (
        <div className="absolute z-50 top-full left-0 right-0 mt-2 bg-slate-900 border border-slate-800 rounded-xl p-4 text-center text-slate-500 text-sm shadow-2xl">
          No se encontraron participantes.
        </div>
      )}

      {error && <span className="text-xs text-red-400 ml-1 mt-1">{error}</span>}
    </div>
  );
};
