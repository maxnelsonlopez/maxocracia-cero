"""Huella estilométrica — capa FORENSE de la custodia sintética.

Este módulo existe para cumplir una promesa hecha en
`docs/architecture/voto_sintetico_arquitectura.md` §4.3-4.4: la firma de estilo
es útil, pero **no como puerta**. Aquí está el instrumento, con sus dos usos
legítimos y su límite escrito en el código.

**Lo que hace:**

1. **Deriva (continuidad biográfica, dimensión de 0.30 del SDV-S).** Compara la
   huella de las respuestas recientes de un agente contra su propio historial
   firmado. Si el "Hilo" de hoy escribe como otro, algo pasó: cambio de motor,
   de contexto, o de manos. No es una alarma de fraude; es una **alarma de
   amputación**.
2. **Clústeres de clones (adversario A6, el granjero).** Si dos `agent_id`
   distintos tienen huellas casi idénticas, comparten origen. La similitud de
   estilo entre votantes es una señal de **grupo**, y los grupos son cómo se
   detecta el Sybil.

**Lo que NO hace, y está escrito aquí para que nadie lo olvide:**

> `HuellaEstilo.puede_autorizar` es **False** por construcción. Esta capa mide
> *parecido*, no *identidad*. Cualquier modelo puede imitar un estilo; una
> imitación buena obtiene similitud alta y no hay forma de distinguirla con
> estas métricas. Por eso el módulo **nunca** decide si un voto vale: eso lo
> hace `verificar_voto` con criptografía determinista. El estilo alerta,
> corrobora y agrupa. No autoriza.

**Motor puro**: sin Flask, sin base de datos, solo stdlib (`re`, `math`,
`statistics`). Las métricas son heurísticas de lingüística computacional, no
verdades: cada constante de calibración está declarada y es ajustable.

**Sobre la escala de similitud (medido, no supuesto).** La banda útil de
`similitud` no es [0, 1] sino aproximadamente [0.6, 1.0]: dos textos escritos en
el mismo idioma y sobre el mismo dominio comparten una base estructural, así que
la similitud entre autores distintos **no baja de ~0.65**. Con el corpus de
prueba: mismo autor ≈ 0.95+, autores distintos ≈ 0.69. De ahí que los umbrales
por defecto de `comparar` sean 0.82 / 0.72 y no 0.75 / 0.6 — y de ahí que estos
números deban **recalibrarse con datos reales** antes de usarse para acusar a
alguien. Una métrica forense mal calibrada produce falsos positivos, y un falso
positivo aquí tiene nombre y apellido.

Referencias: Kirchenbauer et al. 2023 (marca de agua por distribución de
tokens — no aplicable aquí, ver §4.2 del documento); Jovanović et al., ICLR
2024 (robo de la lista verde); MSTTR como corrector de la dependencia de
longitud del type-token ratio.
"""

from __future__ import annotations

import math
import re
import statistics
from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

__all__ = [
    "ADVERTENCIA",
    "CARACTERISTICAS",
    "RANGOS",
    "HuellaEstilo",
    "InformeEstilo",
    "GrupoDeClones",
    "extraer_huella",
    "similitud",
    "contribuciones",
    "comparar",
    "detectar_clones",
]

VERSION_HUELLA = "1"

ADVERTENCIA = (
    "Evidencia forense, no autorización: esta capa mide parecido, no identidad. "
    "Sirve para alertar deriva y agrupar clones; no decide si un voto vale."
)

# ──────────────────────────────────────────────────────────────────
# Léxicos (ajustables: son heurísticas, no axiomas)
# ──────────────────────────────────────────────────────────────────

MATIZADORES = frozenset(
    {
        "quizas",
        "acaso",
        "probablemente",
        "posiblemente",
        "aparentemente",
        "parece",
        "parecen",
        "pareciera",
        "pareceria",
        "podria",
        "podrian",
        "diria",
        "acaso",
        "presuntamente",
        "supuestamente",
        "eventualmente",
    }
)
# Frases de más de una palabra, buscadas sobre el texto en minúsculas.
MATIZADORES_FRASE = (
    "tal vez",
    "en rigor",
    "hasta cierto punto",
    "no necesariamente",
    "a lo sumo",
)

CONECTORES = frozenset(
    {
        "ademas",
        "porque",
        "pues",
        "aunque",
        "mientras",
        "empero",
        "consecuentemente",
    }
)
CONECTORES_FRASE = (
    "sin embargo",
    "no obstante",
    "por lo tanto",
    "en cambio",
    "de modo que",
    "es decir",
    "esto es",
    "en consecuencia",
    "por consiguiente",
    "asi que",
    "a fin de",
)

PUNTUACION = ". , ; : ¿ ? ¡ ! — - ( ) \" ' …".split()
PUNTUACION = [p for p in PUNTUACION if p.strip()]

RE_PALABRA = re.compile(r"[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")
RE_ORACION = re.compile(r"[^.!?…¿¡]+[.!?…]+|[^.!?…¿¡]+$")
RE_ENCABEZADO = re.compile(r"^\s{0,3}#{1,6}\s")
RE_LISTA = re.compile(r"^\s{0,3}(?:[-*+]|\d{1,2}[.)])\s")
RE_NEGRITA = re.compile(r"\*\*[^*]+\*\*")

# Ventana del MSTTR (mean segmental type-token ratio): corrige la dependencia
# de la longitud del TTR crudo. 200 tokens es el valor habitual en la
# literatura de riqueza léxica.
VENTANA_MSTTR = 200
MIN_PALABRAS_FIABLE = 120


# ──────────────────────────────────────────────────────────────────
# Rangos de calibración (normalizan cada característica a [0, 1])
# ──────────────────────────────────────────────────────────────────

RANGOS: Dict[str, Tuple[float, float]] = {
    "longitud_media_oracion": (4.0, 40.0),
    "variabilidad_oraciones": (0.0, 1.2),
    "diversidad_lexica_msttr": (0.2, 0.9),
    "longitud_media_palabra": (3.0, 9.0),
    "entropia_puntuacion": (0.0, 2.4),
    "tasa_matizadores": (0.0, 8.0),
    "tasa_conectores": (0.0, 8.0),
    "densidad_estructura": (0.0, 1.0),
    "oraciones_por_parrafo": (1.0, 8.0),
    "ratio_palabras_largas": (0.0, 0.4),
}

CARACTERISTICAS: Tuple[str, ...] = tuple(RANGOS.keys())


def _normalizar(nombre: str, valor: float) -> float:
    minimo, maximo = RANGOS[nombre]
    if maximo <= minimo:
        return 0.0
    return min(1.0, max(0.0, (valor - minimo) / (maximo - minimo)))


def _entropia(conteos: Iterable[int]) -> float:
    """Entropía de Shannon en bits sobre una distribución de conteos."""
    valores = [c for c in conteos if c > 0]
    total = sum(valores)
    if total <= 0:
        return 0.0
    return -sum((c / total) * math.log2(c / total) for c in valores)


def _msttr(palabras: Sequence[str], ventana: int = VENTANA_MSTTR) -> float:
    """Riqueza léxica robusta a la longitud: media del TTR por segmentos."""
    if not palabras:
        return 0.0
    if len(palabras) < ventana:
        return len(set(palabras)) / len(palabras)
    segmentos = [
        palabras[i : i + ventana]
        for i in range(0, len(palabras) - ventana + 1, ventana)
    ]
    return sum(len(set(s)) / len(s) for s in segmentos) / len(segmentos)


def _rasgos_de_texto(texto: str) -> Dict[str, float]:
    """Extrae las características de UN texto."""
    oraciones = [o.strip() for o in RE_ORACION.findall(texto) if o.strip()]
    palabras = [p.lower() for p in RE_PALABRA.findall(texto)]
    n_palabras = len(palabras)

    longitudes = [len(RE_PALABRA.findall(o)) for o in oraciones]
    longitudes = [n for n in longitudes if n > 0] or [0]
    media_oracion = statistics.fmean(longitudes)
    # Coeficiente de variación: la "irregularidad" del ritmo (burstiness).
    if len(longitudes) > 1 and media_oracion > 0:
        variabilidad = statistics.pstdev(longitudes) / media_oracion
    else:
        variabilidad = 0.0

    conteo_puntuacion = Counter(ch for ch in texto if ch in PUNTUACION)

    def _tasa_por_cien(conteo: int) -> float:
        return (conteo / n_palabras) * 100.0 if n_palabras else 0.0

    minusculas = texto.lower()
    n_matizadores = sum(1 for p in palabras if p in MATIZADORES)
    n_matizadores += sum(minusculas.count(f) for f in MATIZADORES_FRASE)
    n_conectores = sum(1 for p in palabras if p in CONECTORES)
    n_conectores += sum(minusculas.count(f) for f in CONECTORES_FRASE)

    lineas = [ln for ln in texto.splitlines() if ln.strip()]
    if lineas:
        estructuradas = sum(
            1
            for ln in lineas
            if RE_ENCABEZADO.match(ln) or RE_LISTA.match(ln) or RE_NEGRITA.search(ln)
        )
        densidad_estructura = estructuradas / len(lineas)
    else:
        densidad_estructura = 0.0

    parrafos = [p for p in re.split(r"\n\s*\n", texto) if p.strip()]
    if parrafos:
        oraciones_por_parrafo = statistics.fmean(
            max(1, len([o for o in RE_ORACION.findall(p) if o.strip()]))
            for p in parrafos
        )
    else:
        oraciones_por_parrafo = 0.0

    largas = sum(1 for p in palabras if len(p) >= 7)
    ratio_largas = largas / n_palabras if n_palabras else 0.0
    media_palabra = statistics.fmean(len(p) for p in palabras) if palabras else 0.0

    return {
        "longitud_media_oracion": media_oracion,
        "variabilidad_oraciones": variabilidad,
        "diversidad_lexica_msttr": _msttr(palabras),
        "longitud_media_palabra": media_palabra,
        "entropia_puntuacion": _entropia(conteo_puntuacion.values()),
        "tasa_matizadores": _tasa_por_cien(n_matizadores),
        "tasa_conectores": _tasa_por_cien(n_conectores),
        "densidad_estructura": densidad_estructura,
        "oraciones_por_parrafo": oraciones_por_parrafo,
        "ratio_palabras_largas": ratio_largas,
    }


# ──────────────────────────────────────────────────────────────────
# Huella
# ──────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class HuellaEstilo:
    """Rasgos de estilo agregados de un agente sobre varias muestras.

    `puede_autorizar` es False por construcción: no es un parámetro, es una
    declaración. Ver el docstring del módulo.
    """

    agente_id: str
    caracteristicas: Mapping[str, float]
    n_muestras: int
    n_palabras: int
    motor: str = ""
    modelo: str = ""
    version: str = VERSION_HUELLA

    puede_autorizar: bool = field(default=False, init=False)

    @property
    def fiable(self) -> bool:
        """Con pocas palabras la huella es ruido: no se usa para acusar."""
        return self.n_palabras >= MIN_PALABRAS_FIABLE and self.n_muestras >= 2

    def vector(self) -> Tuple[float, ...]:
        return tuple(
            _normalizar(nombre, self.caracteristicas.get(nombre, 0.0))
            for nombre in CARACTERISTICAS
        )

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "agente_id": self.agente_id,
            "motor": self.motor,
            "modelo": self.modelo,
            "n_muestras": self.n_muestras,
            "n_palabras": self.n_palabras,
            "fiable": self.fiable,
            "puede_autorizar": False,
            "caracteristicas": {
                k: round(v, 4) for k, v in sorted(self.caracteristicas.items())
            },
        }


def extraer_huella(
    agente_id: str,
    textos: Sequence[str],
    motor: str = "",
    modelo: str = "",
) -> HuellaEstilo:
    """Agrega los rasgos de varias muestras del MISMO agente.

    Se agrega por mediana, no por media: una respuesta atípica (un listado, un
    volcado de código) no debe arrastrar la huella entera.
    """
    muestras = [t for t in textos if isinstance(t, str) and t.strip()]
    if not muestras:
        raise ValueError("se requiere al menos un texto no vacío")

    por_muestra = [_rasgos_de_texto(t) for t in muestras]
    agregado = {
        nombre: statistics.median(m[nombre] for m in por_muestra)
        for nombre in CARACTERISTICAS
    }
    total_palabras = sum(len(RE_PALABRA.findall(t)) for t in muestras)
    return HuellaEstilo(
        agente_id=str(agente_id),
        caracteristicas=agregado,
        n_muestras=len(muestras),
        n_palabras=total_palabras,
        motor=str(motor or ""),
        modelo=str(modelo or ""),
    )


# ──────────────────────────────────────────────────────────────────
# Comparación
# ──────────────────────────────────────────────────────────────────


def contribuciones(a: HuellaEstilo, b: HuellaEstilo) -> List[Tuple[str, float]]:
    """Qué características se movieron, de mayor a menor. Interpretabilidad:
    el informe dice POR QUÉ dos huellas se parecen o difieren, no solo cuánto."""
    na, nb = a.vector(), b.vector()
    pares = [(nombre, abs(na[i] - nb[i])) for i, nombre in enumerate(CARACTERISTICAS)]
    return sorted(pares, key=lambda p: p[1], reverse=True)


def similitud(a: HuellaEstilo, b: HuellaEstilo) -> float:
    """Similitud en [0, 1]: 1 = huellas indistinguibles.

    1 − diferencia media absoluta sobre las características normalizadas. Se
    elige esta medida sobre la distancia euclídea porque cada característica
    contribuye en proporción directa y acotada: una sola característica
    disparatada no puede dominar el resultado.
    """
    na, nb = a.vector(), b.vector()
    if not na:
        return 0.0
    diferencia = sum(abs(na[i] - nb[i]) for i in range(len(na))) / len(na)
    return round(1.0 - diferencia, 4)


@dataclass(frozen=True)
class InformeEstilo:
    """Resultado de comparar dos huellas. Siempre incluye la advertencia."""

    codigo: str
    similitud: float
    caracteristicas_movidas: Tuple[Tuple[str, float], ...]
    advertencia: str = ADVERTENCIA
    puede_autorizar: bool = False
    referencia: str = ""
    observada: str = ""

    def __bool__(self) -> bool:
        return self.codigo == "SIN_DERIVA"


def comparar(
    referencia: HuellaEstilo,
    observada: HuellaEstilo,
    umbral_leve: float = 0.82,
    umbral_severo: float = 0.72,
) -> InformeEstilo:
    """Compara la huella observada contra la referencia (deriva del agente).

    Umbrales calibrados sobre el corpus de prueba (mismo autor ≈ 0.95+,
    autores distintos ≈ 0.69). Ver la nota sobre la escala en el docstring del
    módulo: recalibrar con datos reales antes de acusar.
    """
    if not 0.0 < umbral_severo <= umbral_leve <= 1.0:
        raise ValueError("se requiere 0 < umbral_severo <= umbral_leve <= 1")
    valor = similitud(referencia, observada)
    if not observada.fiable or not referencia.fiable:
        codigo = "MUESTRA_INSUFICIENTE"
    elif valor >= umbral_leve:
        codigo = "SIN_DERIVA"
    elif valor >= umbral_severo:
        codigo = "DERIVA_LEVE"
    else:
        codigo = "DERIVA_SEVERA"
    return InformeEstilo(
        codigo=codigo,
        similitud=valor,
        caracteristicas_movidas=tuple(contribuciones(referencia, observada)[:3]),
        referencia=referencia.agente_id,
        observada=observada.agente_id,
    )


# ──────────────────────────────────────────────────────────────────
# Clústeres de clones (adversario A6)
# ──────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class GrupoDeClones:
    """Agrupación de agentes con huella casi idéntica.

    `confianza` distingue dos situaciones que NO son lo mismo:
    - **baja**: los agentes comparten motor y modelo. Dos instancias del mismo
      modelo se parecen por construcción; la similitud es esperada y prueba
      poco.
    - **alta**: los agentes declaran motores o modelos DISTINTOS y aun así
      escriben igual. Ahí el parecido no lo explica el motor: lo explica el
      origen. Es la señal que vale.
    """

    agentes: Tuple[str, ...]
    similitud_minima: float
    confianza: str
    motivo: str
    advertencia: str = ADVERTENCIA
    puede_autorizar: bool = False


def detectar_clones(
    huellas: Sequence[HuellaEstilo],
    umbral: float = 0.9,
) -> List[GrupoDeClones]:
    """Agrupa agentes distintos cuya huella supera el umbral (unión-encuentra).

    Solo considera huellas fiables: con pocas palabras el parecido es ruido, y
    acusar de clonación con ruido sería exactamente la clase de daño que este
    sistema debe evitar.
    """
    if not 0.0 < umbral <= 1.0:
        raise ValueError("el umbral debe estar en (0, 1]")
    utiles = [h for h in huellas if h.fiable]
    padre = list(range(len(utiles)))

    def _raiz(x: int) -> int:
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    def _unir(x: int, y: int) -> None:
        rx, ry = _raiz(x), _raiz(y)
        if rx != ry:
            padre[ry] = rx

    similitudes: Dict[Tuple[int, int], float] = {}
    for i in range(len(utiles)):
        for j in range(i + 1, len(utiles)):
            valor = similitud(utiles[i], utiles[j])
            if valor >= umbral:
                similitudes[(i, j)] = valor
                _unir(i, j)

    grupos: Dict[int, List[int]] = {}
    for i in range(len(utiles)):
        grupos.setdefault(_raiz(i), []).append(i)

    resultado: List[GrupoDeClones] = []
    for miembros in grupos.values():
        if len(miembros) < 2:
            continue
        agentes = tuple(sorted(utiles[i].agente_id for i in miembros))
        pares = [
            valor
            for (i, j), valor in similitudes.items()
            if i in miembros and j in miembros
        ]
        minima = min(pares) if pares else umbral
        motores = {f"{utiles[i].motor}|{utiles[i].modelo}" for i in miembros}
        if len(motores) > 1:
            confianza = "alta"
            motivo = (
                "motores o modelos distintos con huella casi idéntica: "
                "el parecido no lo explica el motor"
            )
        else:
            confianza = "baja"
            motivo = (
                "los agentes comparten motor y modelo: el parecido es esperado "
                "y por sí solo prueba poco"
            )
        resultado.append(
            GrupoDeClones(
                agentes=agentes,
                similitud_minima=round(minima, 4),
                confianza=confianza,
                motivo=motivo,
            )
        )
    return sorted(resultado, key=lambda g: (-len(g.agentes), g.agentes))
