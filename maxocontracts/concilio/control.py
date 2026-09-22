# -*- coding: utf-8 -*-
"""Control remoto del Concilio — pausar, reanudar, detener y enviar mensajes.

El custodio (Max) gobierna sin intervenir sesión a sesión mediante un
archivo de control en el workspace (`scratch/concilio/control.json`):

    estado: "activo" | "pausado" | "detenido"
      - pausado: el ciclo actual termina limpio (sin más llamadas) y no
        arranca otro hasta reanudar.
      - detenido: igual, pero queda marcado para revisión (el custodio
        debe reanudarlo explícitamente).
    instrucciones: cola de mensajes del custodio que los oráculos leen
      antes de votar (aparecen como "DIRECTIVAS DEL CUSTODIO").

Todo cambio deja huella T13: nonce incremental + timestamp. La lectura del
control es una comprobación barata (archivo) en cada frontera de fase.
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

ACTIVE = "activo"
PAUSED = "pausado"
STOPPED = "detenido"

_MAX_INSTRUCCIONES = 20


def _default() -> Dict[str, Any]:
    return {
        "estado": ACTIVE,
        "instrucciones": [],
        "nonce": 0,
        "updated": 0.0,
    }


class Control:
    """Archivo de control del Concilio (fail-safe: activo si no existe)."""

    def __init__(self, workspace: str):
        self.path = Path(workspace) / "control.json"

    def leer(self) -> Dict[str, Any]:
        if not self.path.exists():
            return _default()
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return _default()
            data.setdefault("instrucciones", [])
            data.setdefault("nonce", 0)
            if data.get("estado") not in (ACTIVE, PAUSED, STOPPED):
                data["estado"] = ACTIVE
            return data
        except (OSError, ValueError):
            return _default()

    def escribir(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data["updated"] = time.time()
        data["nonce"] = int(data.get("nonce", 0)) + 1
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return data

    # --- Estado ---

    def estado(self) -> str:
        return str(self.leer().get("estado", ACTIVE))

    def pausar(self) -> Dict[str, Any]:
        data = self.leer()
        data["estado"] = PAUSED
        return self.escribir(data)

    def reanudar(self) -> Dict[str, Any]:
        data = self.leer()
        data["estado"] = ACTIVE
        return self.escribir(data)

    def detener(self) -> Dict[str, Any]:
        data = self.leer()
        data["estado"] = STOPPED
        return self.escribir(data)

    # --- Mensajes al Concilio ---

    def mensaje(self, texto: str) -> Dict[str, Any]:
        data = self.leer()
        data["instrucciones"].append(str(texto))
        data["instrucciones"] = data["instrucciones"][-_MAX_INSTRUCCIONES:]
        return self.escribir(data)

    def instrucciones(self) -> List[str]:
        data = self.leer()
        instrucciones = [str(i) for i in data.get("instrucciones", [])]
        return instrucciones

    def check(self) -> Tuple[str, List[str]]:
        """(estado, instrucciones) para una frontera de fase."""
        data = self.leer()
        return (
            str(data.get("estado", ACTIVE)),
            [str(i) for i in data.get("instrucciones", [])],
        )

    def borrar_instrucciones(self) -> Dict[str, Any]:
        data = self.leer()
        data["instrucciones"] = []
        return self.escribir(data)
