# -*- coding: utf-8 -*-
"""Bitácora del Concilio — memoria verificable de cada ciclo (T13).

Cada evento registra qué motor/modelo produjo qué (la firma T13 del canon:
transparencia total de cálculo). La bitácora es JSONL; el manifiesto del
ciclo es `ciclo.json`. Nunca se persisten claves ni datos de participantes.
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


class Bitacora:
    """Bitácora de un ciclo: eventos append-only + manifiesto final."""

    def __init__(self, cycle_dir: Path):
        self.cycle_dir = Path(cycle_dir)
        self.cycle_dir.mkdir(parents=True, exist_ok=True)
        self.events_path = self.cycle_dir / "eventos.jsonl"
        self.manifest_path = self.cycle_dir / "ciclo.json"

    def log(self, event: Dict[str, Any]) -> None:
        """Registra un evento. `sig` (engine/model) es la firma T13."""
        record = {"ts": time.time(), **event}
        with open(self.events_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    def write_manifest(self, manifest: Dict[str, Any]) -> Path:
        with open(self.manifest_path, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, ensure_ascii=False, indent=2)
        return self.manifest_path

    def events(self) -> List[Dict[str, Any]]:
        if not self.events_path.exists():
            return []
        out: List[Dict[str, Any]] = []
        with open(self.events_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
        return out


def load_cycle(cycle_dir) -> Optional[Dict[str, Any]]:
    """Carga el manifiesto de un ciclo, si existe."""
    path = Path(cycle_dir) / "ciclo.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)
