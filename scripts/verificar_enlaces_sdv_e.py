# -*- coding: utf-8 -*-
"""Verificador de enlaces de la biblioteca SDV-E (Reino Natural).

Regla del proyecto (M15): los enlaces del mundo se siembran SOLO verificados
(estado HTTP real; jamas URLs alucinadas - el director verifica).

Este script extrae todas las URLs http(s) de los documentos de
`docs/theory/SDV-E/` y comprueba su estado HTTP real, con veredicto duro
(exit code) para poder encadenarlo al verificador de coherencia.

    .venv\\Scripts\\python.exe scripts\\verificar_enlaces_sdv_e.py
    .venv\\Scripts\\python.exe scripts\\verificar_enlaces_sdv_e.py --listar

Clasificacion:
    OK            200-299        -> verificada
    BLOQUEADA     401/403/429/5xx -> real, pero rechaza clientes automaticos
                                     (un humano la abre: se acepta para citar)
    SIN_RESPUESTA 0 tras reintentos -> red, TLS o limite de peticiones: NO
                                     prueba que el enlace este muerto
    MUERTA        400/404/410/451 -> el recurso ya no existe

Una URL muerta NO falla el verificador si el documento la declara como fuente
descartada (seccion "Fuentes descartadas", con marcas como "muerta" o "404").
El canon exige esa honestidad: distinguir lo verificado de lo que fallo.

Sin dependencias externas: usa urllib de la libreria estandar.

Nota de consola Windows (cp1252): los prints usan solo ASCII.
"""

import argparse
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BIBLIOTECA = REPO / "docs" / "theory" / "SDV-E"

# Captura desde http(s):// hasta el primer espacio. El recorte fino (parentesis
# balanceados, puntuacion y comodines colgantes) lo hace _limpiar_url: extraer
# URLs de prosa es mas delicado de lo que parece y un falso positivo aqui
# acusa injustamente a un documento correcto.
URL_RE = re.compile(r"https?://\S+")

# Codigos que significan "el servidor existe pero no me atiende a mi".
ACEPTABLE_BLOQUEADA = (401, 403, 405, 406, 429, 503)
# Codigos que prueban que el recurso ya no esta.
MUERTA = (400, 404, 410, 451)

TIMEOUT = 25
REINTENTOS = 2
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def _limpiar_url(cruda: str) -> str:
    """Recorta una URL capturada de prosa sin romper las legitimas.

    Casos reales que hay que respetar:
      .../ambient-(outdoor)-air-quality   -> los parentesis son parte de la URL
      .../guideline-values/default/*      -> el asterisco es un comodin de prosa
      (https://ejemplo.org/x).            -> el punto y el parentesis cierran la frase
      `https://ejemplo.org/x`             -> las comillas de codigo no son de la URL
    """
    url = cruda.rstrip(".,;:'\"*`]}>)")
    # Un parentesis de cierre solo se retira si no tiene su apertura en la URL.
    while url.endswith(")") and url.count("(") < url.count(")"):
        url = url[:-1].rstrip(".,;:'\"*`]}>)")
    return url


def es_malformada(url: str) -> bool:
    """True si la URL esta corrupta: caracteres de reemplazo o espacios internos.

    Una URL con `\\ufffd` es un defecto real del documento (tipografia o copia
    rota), no un problema de red: hay que arreglarla en el texto.
    """
    return "\ufffd" in url or " " in url or "\\u" in url


def extraer_urls(texto: str):
    """Devuelve las URLs unicas de un texto, ya limpias y sin duplicados."""
    vistas = []
    for cruda in URL_RE.findall(texto):
        limpia = _limpiar_url(cruda)
        if limpia and limpia not in vistas:
            vistas.append(limpia)
    return vistas


def recolectar(biblioteca: Path):
    """Mapea url -> lista de (archivo, numero_de_linea) que la citan."""
    mapa = {}
    for ruta in sorted(biblioteca.rglob("*.md")):
        try:
            lineas = ruta.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        rel = ruta.relative_to(REPO).as_posix()
        for numero, linea in enumerate(lineas, start=1):
            for url in extraer_urls(linea):
                mapa.setdefault(url, []).append((rel, numero, lineas))
    return mapa


# Un documento puede citar legitimamente una fuente que ya no existe, siempre
# que lo declare (secciones "Fuentes descartadas" / "Vacios"). El canon lo exige:
# distinguir lo verificado de lo inferido, y no ocultar lo que fallo.
MARCAS_DESCARTE = (
    "muert", "descartad", "404", "410", "403", "no se pudo leer", "binario",
    "no responde", "sin respuesta", "no cita", "bloquean", "bloquea",
    "no verific", "ilegible",
)

# Titulos de seccion que declaran un bloque entero de fuentes no citables.
MARCAS_SECCION = (
    "descartad", "vac\u00edo", "vacio", "no citab", "no citable", "ilegible",
)


def _titulo_seccion(lineas, numero: int) -> str:
    """Titulo de la seccion que contiene la linea indicada (1-based)."""
    for i in range(numero - 1, -1, -1):
        if lineas[i].lstrip().startswith("#"):
            return lineas[i].lower()
    return ""


def esta_declarada_muerta(url: str, archivo: str, numero: int, lineas) -> bool:
    """True si el documento marca esa URL como fuente caida o descartada.

    Dos vias, porque los documentos usan las dos:
      1. La marca esta en la propia linea o en su vecindad inmediata.
      2. La URL vive bajo una seccion de descarte ("Fuentes descartadas",
         "Vacios que bloquean dimensiones enteras"), aunque la fila no repita
         la palabra "muerta".
    """
    desde = max(0, numero - 2)
    hasta = min(len(lineas), numero + 2)
    contexto = " ".join(lineas[desde:hasta]).lower()
    if any(marca in contexto for marca in MARCAS_DESCARTE):
        return True
    titulo = _titulo_seccion(lineas, numero)
    return any(marca in titulo for marca in MARCAS_SECCION)


def estado_http(url: str):
    """Devuelve el codigo HTTP, o 0 si no hubo respuesta tras reintentar.

    Un 0 no prueba que el enlace este muerto: puede ser red, DNS, TLS o un
    servidor que limita peticiones seguidas. Por eso se reintenta y, si
    persiste, se informa como advertencia y no como enlace muerto.
    """
    peticion = urllib.request.Request(url, headers={"User-Agent": UA})
    for intento in range(REINTENTOS + 1):
        try:
            with urllib.request.urlopen(peticion, timeout=TIMEOUT) as resp:
                return resp.status
        except urllib.error.HTTPError as exc:
            return exc.code
        except Exception:
            if intento < REINTENTOS:
                time.sleep(2 * (intento + 1))
    return 0


def clasificar(codigo: int) -> str:
    if 200 <= codigo < 300:
        return "OK"
    if codigo in ACEPTABLE_BLOQUEADA or 500 <= codigo < 600:
        return "BLOQUEADA"
    if codigo in MUERTA:
        return "MUERTA"
    return "SIN_RESPUESTA"


def ejecutar(listar: bool) -> int:
    if not BIBLIOTECA.exists():
        print(f"[XX] No existe la biblioteca: {BIBLIOTECA}")
        return 1

    mapa = recolectar(BIBLIOTECA)
    if not mapa:
        print("[XX] La biblioteca no cita ninguna URL: nada que verificar.")
        return 1

    print(f"-> Verificando {len(mapa)} enlaces unicos de {BIBLIOTECA.name}/ ...")
    conteo = {"OK": 0, "BLOQUEADA": 0, "SIN_RESPUESTA": 0, "MUERTA": 0}
    muertas = []
    justificadas = []
    sin_respuesta = []
    malformadas = []

    for url in sorted(mapa):
        citas = mapa[url]
        if es_malformada(url):
            malformadas.append((url, [(a, n) for a, n, _ in citas]))
            continue
        codigo = estado_http(url)
        clase = clasificar(codigo)
        conteo[clase] += 1
        if clase == "MUERTA":
            pendientes = [
                (archivo, numero)
                for archivo, numero, lineas in citas
                if not esta_declarada_muerta(url, archivo, numero, lineas)
            ]
            if pendientes:
                muertas.append((url, codigo, pendientes))
            else:
                justificadas.append(url)
        elif clase == "SIN_RESPUESTA":
            sin_respuesta.append((url, [a for a, _, _ in citas]))
        elif listar:
            print(f"  [{clase}] {codigo} {url}")

    print(
        f"  OK: {conteo['OK']} | BLOQUEADA (real, rechaza bots): "
        f"{conteo['BLOQUEADA']} | SIN RESPUESTA: {conteo['SIN_RESPUESTA']} | "
        f"MUERTA: {conteo['MUERTA']} ({len(justificadas)} declaradas como descartadas) | "
        f"MALFORMADA: {len(malformadas)}"
    )

    if malformadas:
        print("\n>> URLs MALFORMADAS (caracteres de reemplazo o espacios: el texto")
        print("   tiene la direccion rota; no es un problema de red):")
        for url, citas in malformadas:
            print(f"  {url!r}")
            for archivo, numero in citas:
                print(f"        {archivo}:{numero}")

    if sin_respuesta:
        print(
            "\n>> SIN RESPUESTA (no prueba muerte: red, TLS o limite de peticiones)."
            "\n   Revisar a mano antes de retirar:"
        )
        for url, archivos in sin_respuesta:
            print(f"  {url}")
            for archivo in archivos:
                print(f"        citado en {archivo}")

    if muertas:
        print("\n>> ENLACES MUERTOS SIN DECLARAR (404/410/451 citados como si")
        print("   estuvieran vivos: corregir la URL o declararla en 'Fuentes descartadas'):")
        for url, codigo, pendientes in muertas:
            print(f"  [{codigo}] {url}")
            for archivo, numero in pendientes:
                print(f"        {archivo}:{numero}")
        print("\n>> ENLACES: ROJO. Hay fuentes citadas que ya no existen.")
        return 1

    if malformadas:
        print("\n>> ENLACES: ROJO. Hay direcciones rotas en el texto.")
        return 1

    print("\n>> ENLACES: VERDE. Toda fuente citada responde o esta declarada caida.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--listar", action="store_true", help="muestra tambien los enlaces correctos"
    )
    args = parser.parse_args()
    return ejecutar(args.listar)


if __name__ == "__main__":
    sys.exit(main())
