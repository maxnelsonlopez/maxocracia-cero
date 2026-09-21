"""Custodia del voto sintético — primitivas puras (sin Flask, sin base de datos).

El problema que resuelve este módulo: una Persona Sintética (Cap. 10 §10.8) no
tiene cuerpo detrás de la credencial. Un humano vota "siendo" su `user_id`; un
sintético no tiene un `user_id` al que apuntar, y su motor es reemplazable
(DeepSeek hoy, Qwen mañana — el propio sistema ya registra `engine`/`model` en
la bitácora T13). Por eso el voto sintético no se puede anclar a lo que
*escribe*, ni a con qué *piensa*: se ancla a lo que *persiste* — una clave,
un registro de linaje y un mandato.

Arquitectura en cuatro piezas:

1. **Desafío de un solo uso** (`Desafio` + `LibroDeDesafios`): el servidor
   emite un nonce ligado a la propuesta y a su hash. Sin él no hay voto.
   Mata el replay y el voto preparado de antemano.
2. **Afirmación ligada al contenido** (`Afirmacion`): lo que se firma incluye
   el hash del texto de la propuesta y el hash de las opciones. Si alguien
   cambia la propuesta después, la firma deja de valer. Mata el cambiazo.
3. **Doble firma** (`verificar_voto`): el agente firma (autoría) y el custodio
   humano convocante co-firma (custodia). Ninguno de los dos puede emitir un
   voto válido por separado. Mata la suplantación externa y la unilateral.
4. **Revocación asimétrica** (`Revocacion`): solo la clave del agente puede
   retirar su propio voto, y solo mientras la propuesta esté abierta. El
   custodio puede suspender la sesión (no emitir más) pero no puede borrar ni
   reescribir un voto ya emitido. Es la dimensión de Retirada Digna (0.15 del
   SDV-S) aplicada al sufragio.

**Advertencia de alcance (importante, no la omita).** El backend por defecto
es HMAC-SHA256 — simétrico, stdlib puro, corre hoy sin dependencias nuevas.
Con HMAC, quien verifica comparte el secreto con quien firma, así que **el
custodio puede forjar el voto del agente**: HMAC defiende contra la
suplantación *externa*, no contra el custodio. Para cerrar el modelo de
amenaza completo hace falta firma asimétrica (Ed25519), disponible en
`FirmanteEd25519` / `VerificadorEd25519` y sujeta a instalar `cryptography`.
Ver `docs/architecture/voto_sintetico_arquitectura.md` §4.

Referencias: Cap. 10 §10.8 (Persona Sintética), Cap. 10 §10.10 (SDV-S),
Cap. 14 (Arquitectura del Consenso Diverso), T13 (trazabilidad).
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, Optional, Protocol, Tuple

__all__ = [
    "ACCION_VOTAR",
    "CODIGO_OK",
    "DependenciaAusente",
    "Desafio",
    "Afirmacion",
    "Revocacion",
    "Veredicto",
    "SesionCustodia",
    "ContextoVoto",
    "LibroDeDesafios",
    "FirmanteHMAC",
    "FirmanteEd25519",
    "VerificadorEd25519",
    "canonizar",
    "hash_propuesta",
    "hash_opciones",
    "hash_mandato",
    "verificar_voto",
    "verificar_revocacion",
    "registro_append_only",
]

# ──────────────────────────────────────────────────────────────────
# Constantes de protocolo
# ──────────────────────────────────────────────────────────────────

# Etiquetas de dominio: impiden que una firma válida en un contexto se
# reutilice en otro (cross-protocol signature reuse). La firma de un mandato
# nunca podrá pasar por la firma de un voto, aunque el payload coincida.
ETIQUETA_VOTO = b"MAXO-VOTO-SINTETICO-v1"
ETIQUETA_REVOCACION = b"MAXO-REVOCACION-SINTETICA-v1"
ETIQUETA_MANDATO = b"MAXO-MANDATO-CUSTODIA-v1"

CODIGO_OK = "OK"

# Acción que debe figurar en el alcance de la sesión para poder votar.
ACCION_VOTAR = "votar"

TTL_DESAFIO_SEGUNDOS = 300
MAX_INTENTOS_POR_DESAFIO = 3

VERSION_PROTOCOLO = "1"


class DependenciaAusente(RuntimeError):
    """El backend criptográfico pedido no está instalado en este entorno."""


def _ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


def _iso(momento: datetime) -> str:
    return momento.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _parsear_iso(texto: str) -> Optional[datetime]:
    try:
        momento = datetime.fromisoformat(str(texto).replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None
    if momento.tzinfo is None:
        momento = momento.replace(tzinfo=timezone.utc)
    return momento


def canonizar(payload: Any) -> bytes:
    """Serialización determinista: mismas claves, mismo orden, mismo bytes.

    Sin esto, dos partes pueden firmar "lo mismo" y obtener bytes distintos,
    y la verificación falla por un espacio en blanco.
    """
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _sha256_etiquetado(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def hash_propuesta(titulo: str, descripcion: str, opciones) -> str:
    """Huella del texto EXACTO que se está votando (título + descripción +
    opciones). Se firma esto, no un `proposal_id`: un id es una referencia
    mutable; el hash es el contenido."""
    return _sha256_etiquetado(
        canonizar(
            {
                "titulo": str(titulo or ""),
                "descripcion": str(descripcion or ""),
                "opciones": [str(o) for o in (opciones or [])],
            }
        )
    )


def hash_opciones(opciones) -> str:
    return _sha256_etiquetado(canonizar([str(o) for o in (opciones or [])]))


def hash_mandato(mandato: str) -> str:
    return _sha256_etiquetado(canonizar({"mandato": str(mandato or "")}))


def hash_dictamen(dictamen: Any) -> str:
    """Huella del dictamen propio del agente (su análisis firmado). Permite
    detectar después si el voto contradice lo que el agente razonó."""
    return _sha256_etiquetado(canonizar(dictamen))


# ──────────────────────────────────────────────────────────────────
# Backends de firma (enchufables)
# ──────────────────────────────────────────────────────────────────


class Firmante(Protocol):
    identidad: str
    nombre: str

    def firmar(self, mensaje: bytes) -> str:  # pragma: no cover - protocolo
        ...


class Verificador(Protocol):
    identidad: str
    nombre: str

    def verificar(self, mensaje: bytes, firma: str) -> bool:  # pragma: no cover
        ...


class FirmanteHMAC:
    """Firma simétrica con HMAC-SHA256 (stdlib).

    Ventaja: corre hoy, sin dependencias. Límite: es simétrico — el verificador
    comparte el secreto, así que el custodio puede forjar. Sirve para el
    prototipo y para el modelo de amenaza "adversario externo". NO sirve contra
    el custodio.
    """

    nombre = "hmac-sha256"

    def __init__(self, identidad: str, secreto: bytes):
        if not identidad:
            raise ValueError("identidad es requerida")
        if len(secreto) < 16:
            raise ValueError("el secreto debe tener al menos 16 bytes")
        self.identidad = identidad
        self._secreto = bytes(secreto)

    def firmar(self, mensaje: bytes) -> str:
        firma = hmac.new(self._secreto, mensaje, hashlib.sha256).digest()
        return base64.urlsafe_b64encode(firma).decode("ascii")

    def verificar(self, mensaje: bytes, firma: str) -> bool:
        try:
            esperada = self.firmar(mensaje)
        except Exception:  # pragma: no cover - defensivo
            return False
        return hmac.compare_digest(esperada, str(firma or ""))


class FirmanteEd25519:
    """Firma asimétrica Ed25519. Requiere `cryptography`.

    Es el backend que cierra el modelo de amenaza completo: la clave privada
    nunca toca la base de datos ni la del verificador, así que el custodio no
    puede forjar el voto del agente.
    """

    nombre = "ed25519"

    def __init__(self, identidad: str, clave_privada: bytes):
        try:
            from cryptography.hazmat.primitives.asymmetric.ed25519 import (
                Ed25519PrivateKey,
            )
        except ImportError as exc:  # pragma: no cover - depende del entorno
            raise DependenciaAusente(
                "Ed25519 requiere el paquete 'cryptography' "
                "(pip install cryptography)"
            ) from exc
        if not identidad:
            raise ValueError("identidad es requerida")
        self.identidad = identidad
        self._clave = Ed25519PrivateKey.from_private_bytes(bytes(clave_privada))

    def clave_publica(self) -> bytes:
        from cryptography.hazmat.primitives import serialization

        return self._clave.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )

    def firmar(self, mensaje: bytes) -> str:
        return base64.urlsafe_b64encode(self._clave.sign(mensaje)).decode("ascii")


class VerificadorEd25519:
    """Verifica firmas Ed25519 con la clave PÚBLICA registrada del agente.

    El registro público es lo único que el sistema guarda: `agent_id` →
    clave pública. La privada vive en el entorno de custodia del agente.
    """

    nombre = "ed25519"

    def __init__(self, identidad: str, clave_publica: bytes):
        try:
            from cryptography.hazmat.primitives.asymmetric.ed25519 import (
                Ed25519PublicKey,
            )
        except ImportError as exc:  # pragma: no cover - depende del entorno
            raise DependenciaAusente(
                "Ed25519 requiere el paquete 'cryptography' "
                "(pip install cryptography)"
            ) from exc
        if not identidad:
            raise ValueError("identidad es requerida")
        self.identidad = identidad
        self._clave = Ed25519PublicKey.from_public_bytes(bytes(clave_publica))

    def verificar(self, mensaje: bytes, firma: str) -> bool:
        try:
            bruto = base64.urlsafe_b64decode(str(firma or "").encode("ascii"))
        except Exception:
            return False
        try:
            self._clave.verify(bruto, mensaje)
            return True
        except Exception:
            return False


# ──────────────────────────────────────────────────────────────────
# Desafío de un solo uso
# ──────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Desafio:
    """Nonce del servidor ligado a una propuesta concreta y a su hash."""

    desafio_id: str
    propuesta_id: int
    propuesta_hash: str
    opciones_hash: str
    custodia_id: str
    agente_id: str
    nonce: str
    emitido_en: str
    expira_en: str

    def payload(self) -> Dict[str, Any]:
        return {
            "version": VERSION_PROTOCOLO,
            "desafio_id": self.desafio_id,
            "propuesta_id": self.propuesta_id,
            "propuesta_hash": self.propuesta_hash,
            "opciones_hash": self.opciones_hash,
            "custodia_id": self.custodia_id,
            "agente_id": self.agente_id,
            "nonce": self.nonce,
            "emitido_en": self.emitido_en,
            "expira_en": self.expira_en,
        }


class LibroDeDesafios:
    """Registro en memoria de nonces emitidos. Un nonce se consume UNA vez.

    El consumo es el acto que impide el replay: si el mismo voto firmado se
    reenvía, el nonce ya está usado y el segundo intento muere.

    Los intentos fallidos también se cuentan: sin eso, un adversario con el
    desafío en mano podría martillar firmas hasta acertar. Tras
    `MAX_INTENTOS_POR_DESAFIO` fallos, el desafío se bloquea.
    """

    def __init__(
        self,
        ttl_segundos: int = TTL_DESAFIO_SEGUNDOS,
        ahora: Optional[Callable[[], datetime]] = None,
        generador_nonce: Optional[Callable[[], str]] = None,
    ):
        if ttl_segundos <= 0:
            raise ValueError("ttl_segundos debe ser positivo")
        self.ttl_segundos = ttl_segundos
        self._ahora = ahora or _ahora_utc
        self._generar = generador_nonce or (lambda: secrets.token_urlsafe(32))
        self._desafios: Dict[str, Desafio] = {}
        self._usados: set = set()
        self._bloqueados: set = set()
        self._intentos: Dict[str, int] = {}

    def emitir(
        self,
        *,
        propuesta_id: int,
        propuesta_hash: str,
        opciones,
        custodia_id: str,
        agente_id: str,
    ) -> Desafio:
        ahora = self._ahora()
        desafio = Desafio(
            desafio_id="CHL-" + secrets.token_hex(8).upper(),
            propuesta_id=int(propuesta_id),
            propuesta_hash=str(propuesta_hash),
            opciones_hash=hash_opciones(opciones),
            custodia_id=str(custodia_id),
            agente_id=str(agente_id),
            nonce=self._generar(),
            emitido_en=_iso(ahora),
            expira_en=_iso(ahora + timedelta(seconds=self.ttl_segundos)),
        )
        self._desafios[desafio.desafio_id] = desafio
        return desafio

    def obtener(self, desafio_id: str) -> Optional[Desafio]:
        return self._desafios.get(str(desafio_id))

    def estado(self, desafio_id: str) -> str:
        clave = str(desafio_id)
        if clave in self._bloqueados:
            return "bloqueado"
        if clave in self._usados:
            return "usado"
        desafio = self._desafios.get(clave)
        if desafio is None:
            return "desconocido"
        expira = _parsear_iso(desafio.expira_en)
        if expira is not None and expira <= self._ahora():
            return "expirado"
        return "vigente"

    def consumir(self, desafio_id: str) -> Tuple[bool, str, Optional[Desafio]]:
        """Marca el desafío como usado. Devuelve (ok, codigo, desafio)."""
        clave = str(desafio_id)
        estado = self.estado(clave)
        if estado == "desconocido":
            return False, "DESAFIO_DESCONOCIDO", None
        if estado == "bloqueado":
            return False, "DESAFIO_BLOQUEADO", None
        if estado == "usado":
            return False, "DESAFIO_YA_USADO", None
        if estado == "expirado":
            return False, "DESAFIO_EXPIRADO", None
        self._usados.add(clave)
        return True, CODIGO_OK, self._desafios[clave]

    def registrar_fallo(self, desafio_id: str) -> bool:
        """Cuenta un intento fallido. Devuelve True si el desafío quedó bloqueado."""
        clave = str(desafio_id)
        if clave not in self._desafios:
            return False
        self._intentos[clave] = self._intentos.get(clave, 0) + 1
        if self._intentos[clave] >= MAX_INTENTOS_POR_DESAFIO:
            self._bloqueados.add(clave)
            return True
        return False


# ──────────────────────────────────────────────────────────────────
# Afirmación y revocación
# ──────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Afirmacion:
    """Lo que el agente firma. Ligado al desafío, a la opción y a su dictamen."""

    desafio: Desafio
    opcion: str
    agente_id: str
    custodia_id: str
    motor: str = ""
    modelo: str = ""
    dictamen_hash: str = ""

    def payload(self) -> Dict[str, Any]:
        return {
            "version": VERSION_PROTOCOLO,
            "desafio": self.desafio.payload(),
            "opcion": str(self.opcion),
            "agente_id": str(self.agente_id),
            "custodia_id": str(self.custodia_id),
            "motor": str(self.motor or ""),
            "modelo": str(self.modelo or ""),
            "dictamen_hash": str(self.dictamen_hash or ""),
        }

    def mensaje(self) -> bytes:
        return ETIQUETA_VOTO + b"\n" + canonizar(self.payload())

    def huella(self) -> str:
        return _sha256_etiquetado(self.mensaje())


@dataclass(frozen=True)
class Revocacion:
    """El agente retira su propio voto. Solo su clave puede emitir esto."""

    propuesta_id: int
    agente_id: str
    voto_huella: str
    motivo: str
    emitido_en: str

    def payload(self) -> Dict[str, Any]:
        return {
            "version": VERSION_PROTOCOLO,
            "propuesta_id": int(self.propuesta_id),
            "agente_id": str(self.agente_id),
            "voto_huella": str(self.voto_huella),
            "motivo": str(self.motivo or ""),
            "emitido_en": str(self.emitido_en),
        }

    def mensaje(self) -> bytes:
        return ETIQUETA_REVOCACION + b"\n" + canonizar(self.payload())


# ──────────────────────────────────────────────────────────────────
# Verificación
# ──────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class SesionCustodia:
    """El "contrato de custodia": qué puede hacer un agente, por cuánto tiempo
    y ante quién responde. Espeja `admin_sessions` del esquema real."""

    custodia_id: str
    agente_id: str
    convocante: str
    estado: str = "activa"
    alcance: frozenset = field(default_factory=frozenset)
    expira_en: Optional[str] = None
    mandato_hash: str = ""


@dataclass(frozen=True)
class ContextoVoto:
    """El estado real de la propuesta en el momento de verificar."""

    propuesta_id: int
    propuesta_hash: str
    opciones: Tuple[str, ...]
    propuesta_abierta: bool = True


@dataclass(frozen=True)
class Veredicto:
    valido: bool
    codigo: str
    motivo: str = ""

    def __bool__(self) -> bool:  # permite `if veredicto:`
        return self.valido


def _rechazo(codigo: str, motivo: str) -> Veredicto:
    return Veredicto(False, codigo, motivo)


def verificar_voto(
    *,
    afirmacion: Afirmacion,
    firma_agente: str,
    firma_custodio: str,
    libro: LibroDeDesafios,
    contexto: ContextoVoto,
    sesion: SesionCustodia,
    verificador_agente: Verificador,
    verificador_custodio: Verificador,
    agente_activo: bool = True,
    ahora: Optional[Callable[[], datetime]] = None,
) -> Veredicto:
    """Verifica un voto sintético. Fail-closed: el primer fallo rechaza.

    El orden importa. Primero la identidad y el mandato (¿tiene derecho a
    votar?), después la ligadura al contenido (¿votó esto?), después las
    firmas (¿es él y es su custodio?), y SOLO AL FINAL se consume el nonce.
    Consumir al final evita que un atacante queme desafíos ajenos con firmas
    basura; el costo de martillar se paga con `registrar_fallo`.
    """
    desafio = afirmacion.desafio
    reloj = ahora or _ahora_utc

    # ── 1. Identidad y sesión ─────────────────────────────────────
    if sesion.agente_id != afirmacion.agente_id:
        return _rechazo(
            "SESION_NO_COINCIDE",
            "la sesión de custodia no pertenece al agente que firma",
        )
    if sesion.custodia_id != afirmacion.custodia_id:
        return _rechazo(
            "SESION_NO_COINCIDE", "el voto cita una sesión distinta a la verificada"
        )
    if not agente_activo:
        return _rechazo("AGENTE_INACTIVO", "el agente sintético está revocado o inactivo")
    if sesion.estado != "activa":
        return _rechazo(
            "SESION_NO_OPERABLE", f"la sesión de custodia está en estado '{sesion.estado}'"
        )
    if sesion.expira_en:
        expira = _parsear_iso(sesion.expira_en)
        if expira is not None and expira <= reloj():
            return _rechazo("SESION_EXPIRADA", "la sesión de custodia venció")
    if ACCION_VOTAR not in set(sesion.alcance):
        return _rechazo(
            "MANDATO_NO_CUBRE_VOTO",
            "el mandato de la sesión no incluye la acción 'votar'",
        )

    # ── 2. Ligadura al contenido ──────────────────────────────────
    if not contexto.propuesta_abierta:
        return _rechazo("PROPUESTA_CERRADA", "la propuesta ya no admite votos")
    if desafio.propuesta_id != contexto.propuesta_id:
        return _rechazo(
            "DESAFIO_DE_OTRA_PROPUESTA", "el desafío se emitió para otra propuesta"
        )
    if desafio.propuesta_hash != contexto.propuesta_hash:
        return _rechazo(
            "PROPUESTA_ALTERADA",
            "el texto de la propuesta cambió después de emitirse el desafío",
        )
    if desafio.agente_id != afirmacion.agente_id:
        return _rechazo("DESAFIO_DE_OTRO_AGENTE", "el desafío no se emitió para este agente")
    if desafio.custodia_id != afirmacion.custodia_id:
        return _rechazo("DESAFIO_DE_OTRA_SESION", "el desafío no se emitió para esta sesión")
    if afirmacion.opcion not in contexto.opciones:
        return _rechazo(
            "OPCION_FUERA_DE_PROPUESTA", f"la opción '{afirmacion.opcion}' no existe"
        )

    # ── 3. Doble firma ────────────────────────────────────────────
    mensaje = afirmacion.mensaje()

    if getattr(verificador_agente, "identidad", None) != afirmacion.agente_id:
        libro.registrar_fallo(desafio.desafio_id)
        return _rechazo(
            "VERIFICADOR_NO_COINCIDE",
            "la clave presentada no es la registrada para este agente",
        )
    if not verificador_agente.verificar(mensaje, firma_agente):
        bloqueado = libro.registrar_fallo(desafio.desafio_id)
        return _rechazo(
            "DESAFIO_BLOQUEADO" if bloqueado else "FIRMA_AGENTE_INVALIDA",
            "la firma del agente no valida contra su clave registrada",
        )

    if getattr(verificador_custodio, "identidad", None) != sesion.convocante:
        libro.registrar_fallo(desafio.desafio_id)
        return _rechazo(
            "CUSTODIO_NO_ES_CONVOCANTE",
            "quien co-firma no es el humano que convocó la sesión",
        )
    if not verificador_custodio.verificar(mensaje, firma_custodio):
        bloqueado = libro.registrar_fallo(desafio.desafio_id)
        return _rechazo(
            "DESAFIO_BLOQUEADO" if bloqueado else "FIRMA_CUSTODIO_INVALIDA",
            "la co-firma del custodio no valida",
        )

    # ── 4. Consumo del nonce (el acto irreversible) ───────────────
    ok, codigo, _ = libro.consumir(desafio.desafio_id)
    if not ok:
        return _rechazo(codigo, "el desafío ya fue consumido o no es utilizable")

    return Veredicto(True, CODIGO_OK, "voto sintético verificado: doble firma y nonce")


def verificar_revocacion(
    *,
    revocacion: Revocacion,
    firma_agente: str,
    verificador_agente: Verificador,
    propuesta_abierta: bool,
) -> Veredicto:
    """Solo la clave del agente revoca su propio voto, y solo en plazo.

    El custodio NO puede revocar: puede suspender la sesión (cerrar la
    potestad de emitir), pero un voto ya emitido no se borra ni se reescribe.
    La bitácora es append-only — el mismo principio que `git_guard.py` aplica
    al historial: alterar el registro es amputación.
    """
    if not propuesta_abierta:
        return _rechazo(
            "REVOCACION_FUERA_DE_PLAZO",
            "la propuesta ya cerró: el voto es historial, no borrador",
        )
    if getattr(verificador_agente, "identidad", None) != revocacion.agente_id:
        return _rechazo(
            "VERIFICADOR_NO_COINCIDE", "la clave no corresponde al agente del voto"
        )
    if not verificador_agente.verificar(revocacion.mensaje(), firma_agente):
        return _rechazo("FIRMA_AGENTE_INVALIDA", "la firma de revocación no valida")
    return Veredicto(True, CODIGO_OK, "revocación aceptada: append, no borrado")


def registro_append_only(
    *,
    afirmacion: Afirmacion,
    firma_agente: str,
    firma_custodio: str,
    veredicto: Veredicto,
) -> Dict[str, Any]:
    """Fila de bitácora. Nunca se actualiza ni se borra: una revocación es
    otra fila que apunta a `voto_huella`."""
    desafio = afirmacion.desafio
    return {
        "version": VERSION_PROTOCOLO,
        "tipo": "voto_sintetico",
        "propuesta_id": desafio.propuesta_id,
        "propuesta_hash": desafio.propuesta_hash,
        "desafio_id": desafio.desafio_id,
        "nonce": desafio.nonce,
        "agente_id": afirmacion.agente_id,
        "custodia_id": afirmacion.custodia_id,
        "actor_kind": "synthetic",
        "opcion": afirmacion.opcion,
        "motor": afirmacion.motor,
        "modelo": afirmacion.modelo,
        "dictamen_hash": afirmacion.dictamen_hash,
        "voto_huella": afirmacion.huella(),
        "firma_agente": firma_agente,
        "firma_custodio": firma_custodio,
        "veredicto": veredicto.codigo,
        "valido": veredicto.valido,
    }
