# -*- coding: utf-8 -*-
"""Custodia sintética — paquete de primitivas para el voto del Reino Sintético.

El sufragio sintético no puede anclarse a lo que el agente *escribe* (el
estilo se imita) ni a lo que *piensa* (el motor se reemplaza): se ancla a lo
que *persiste* — una clave, un linaje y un mandato.

Reglas del paquete (canon):
- Motor puro (sin Flask, sin base de datos): solo stdlib. La persistencia la
  hace el blueprint; aquí vive la verificación.
- Nada de claves en la bitácora: se registran firmas y huellas, nunca secretos.
- El backend de firma es enchufable (`FirmanteHMAC` hoy, `FirmanteEd25519`
  cuando se instale `cryptography`). El módulo declara su propio límite.
- Dos capas con estatutos distintos, y la distinción es deliberada:
  `voto_sintetico` **autoriza** (determinista: firma, nonce, mandato) y
  `huella_estilo` **atribuye** (probabilístico: forense, nunca puerta).
"""

from .huella_estilo import (
    ADVERTENCIA,
    CARACTERISTICAS,
    RANGOS,
    GrupoDeClones,
    HuellaEstilo,
    InformeEstilo,
    comparar,
    contribuciones,
    detectar_clones,
    extraer_huella,
    similitud,
)
from .voto_sintetico import (
    ACCION_VOTAR,
    CODIGO_OK,
    Afirmacion,
    ContextoVoto,
    DependenciaAusente,
    Desafio,
    FirmanteEd25519,
    FirmanteHMAC,
    LibroDeDesafios,
    Revocacion,
    SesionCustodia,
    Veredicto,
    VerificadorEd25519,
    canonizar,
    hash_dictamen,
    hash_mandato,
    hash_opciones,
    hash_propuesta,
    registro_append_only,
    verificar_revocacion,
    verificar_voto,
)

__all__ = [
    "verificar_voto",
    "verificar_revocacion",
    "registro_append_only",
    "LibroDeDesafios",
    "Desafio",
    "Afirmacion",
    "Revocacion",
    "Veredicto",
    "SesionCustodia",
    "ContextoVoto",
    "FirmanteHMAC",
    "FirmanteEd25519",
    "VerificadorEd25519",
    "DependenciaAusente",
    "canonizar",
    "hash_propuesta",
    "hash_opciones",
    "hash_mandato",
    "hash_dictamen",
    "ACCION_VOTAR",
    "CODIGO_OK",
    "extraer_huella",
    "similitud",
    "contribuciones",
    "comparar",
    "detectar_clones",
    "HuellaEstilo",
    "InformeEstilo",
    "GrupoDeClones",
    "CARACTERISTICAS",
    "RANGOS",
    "ADVERTENCIA",
]
