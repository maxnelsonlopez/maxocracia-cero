# -*- coding: utf-8 -*-
"""Concilio de Oráculos Sintéticos — paquete de ciclo de trabajo autónomo.

Fases (ver `docs/architecture/concilio_oraculos_sinteticos_piloto.md` §5):
F0 Despertar · F1 Absorción del canon · F2 Agenda votada · (F3-F5 en fases
posteriores del piloto).

Reglas del paquete (canon):
- Motor puro (sin Flask), solo stdlib + requests; sus oráculos vienen de
  `maxocontracts.oracles.engines` (multi-proveedor, firma T13 engine/model).
- Nunca escribe en el código vivo: produce artefactos en un workspace
  (por defecto `scratch/concilio/`), siempre con bitácora auditable.
- No imprime ni persiste claves; solo nombres de motores y modelos.
"""

from .control import ACTIVE, PAUSED, STOPPED, Control
from .cycle import CycleLockError, run_cycle
from .executor import EjecutorGuardado, GuardDeniedError
from .git_guard import guard_git_command

__all__ = [
    "run_cycle",
    "CycleLockError",
    "Control",
    "ACTIVE",
    "PAUSED",
    "STOPPED",
    "EjecutorGuardado",
    "GuardDeniedError",
    "guard_git_command",
]
