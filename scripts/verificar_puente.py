# -*- coding: utf-8 -*-
"""Verifica el puente start.maxocracia.com <-> escuela.maxocracia.com (M12).

Solo lectura por defecto: comprueba DNS, extremos públicos, millora del
buscador desplegado y el fail-closed del puente (401/403 sin credenciales).
Con ``MAXO_JWT`` verifica identidad unificada; con ``EDU_BRIDGE_SERVICE_TOKEN``
+ ``--escribir-prueba --user-id N`` envía UN evento real de prueba (escribe).

Uso::

    .venv\\Scripts\\python.exe scripts/verificar_puente.py
    $env:MAXO_JWT = "<jwt de start>"; .venv\\Scripts\\python.exe scripts/verificar_puente.py
"""

import json
import os
import socket
import sys
import urllib.parse
import urllib.request

START = "https://start.maxocracia.com"
ESCUELA = "https://escuela.maxocracia.com"
UA = {"User-Agent": "MaxocraciaPuenteCheck/0.1"}


def get(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            cuerpo = resp.read().decode("utf-8", "replace")
            try:
                return resp.status, json.loads(cuerpo)
            except ValueError:
                return resp.status, {"_texto": cuerpo[:120]}
    except Exception as exc:
        codigo = getattr(getattr(exc, "response", None), "status", None)
        if codigo is None and hasattr(exc, "code"):
            codigo = exc.code
        return codigo or ("ERR:" + exc.__class__.__name__), {}


def post(url, datos, headers=None, timeout=20):
    req = urllib.request.Request(
        url,
        data=json.dumps(datos).encode("utf-8"),
        headers={**UA, "Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8", "replace"))
    except Exception as exc:
        codigo = getattr(exc, "code", None) or ("ERR:" + exc.__class__.__name__)
        try:
            cuerpo = json.loads(exc.read().decode("utf-8", "replace"))
        except Exception:
            cuerpo = {}
        return codigo, cuerpo


def main(argv):
    ok = True

    def linea(nombre, bien, detalle=""):
        nonlocal ok
        ok = ok and bien
        print(
            ("PASS " if bien else "FAIL ")
            + nombre
            + (f" — {detalle}" if detalle else "")
        )

    # 1. DNS de ambos.
    try:
        ips_e = socket.gethostbyname_ex("escuela.maxocracia.com")[2]
        ips_s = socket.gethostbyname_ex("start.maxocracia.com")[2]
        linea("DNS escuela+start", True, f"escuela={ips_e[0]}, start={ips_s[0]}")
    except Exception as exc:
        linea("DNS escuela+start", False, str(exc)[:80])

    # 2. Extremos públicos.
    st, _ = get(START + "/")
    linea("start / responde 200", st == 200, f"HTTP {st}")
    st, params = get(ESCUELA + "/api/buscador/parametros")
    claves = sorted((params.get("parametros") or {}).keys()) if st == 200 else []
    linea("escuela parametros 200", st == 200, f"HTTP {st} params={claves}")

    # 3. Millora del buscador desplegado (capas + motores caídos = egreso).
    st, b = get(
        ESCUELA + "/api/buscador?" + urllib.parse.urlencode({"q": "maxocracia"})
    )
    capas = b.get("por_capa") if isinstance(b, dict) else None
    linea("escuela buscador responde", st == 200 and bool(capas), f"capas={capas}")
    if isinstance(b, dict):
        linea(
            "escuela egreso sano",
            not b.get("motores_fail_open"),
            f"fail_open={b.get('motores_fail_open') or 'ninguno'}",
        )

    # 4. Fail-closed del puente (sin credenciales).
    st, _ = get(START + "/edu-bridge/status")
    linea("puente status sin token -> 401", st == 401, f"HTTP {st}")
    st, cuerpo = post(START + "/edu-bridge/sync-mastery", {"user_id": 1})
    linea(
        "puente sync sin token -> 403",
        st == 403,
        f"HTTP {st} code={(cuerpo or {}).get('code')}",
    )

    # 5. Identidad unificada (opcional, con JWT humano de start).
    jwt = os.environ.get("MAXO_JWT", "").strip()
    if jwt:
        st, cuerpo = get(
            START + "/edu-bridge/status", headers={"Authorization": f"Bearer {jwt}"}
        )
        linea(
            "puente status con JWT",
            st == 200 and (cuerpo or {}).get("unified_identity") is True,
            f"HTTP {st}",
        )
    else:
        print("SKIP puente con JWT (sin MAXO_JWT)")

    # 6. Escritura real (opcional y explícita).
    svc = os.environ.get("EDU_BRIDGE_SERVICE_TOKEN", "").strip()
    if "--escribir-prueba" in argv and svc:
        uid = 1
        for a in argv:
            if a.startswith("--user-id="):
                uid = a.split("=", 1)[1]
        st, cuerpo = post(
            START + "/edu-bridge/sync-mastery",
            {
                "user_id": int(uid),
                "topic_slug": "prueba-puente",
                "branch_slug": "etica",
                "score": 100,
            },
            headers={"X-Edu-Bridge-Token": svc},
        )
        linea(
            "puente sync con token -> 201",
            st == 201,
            f"HTTP {st} event={(cuerpo or {}).get('event_id')}",
        )
    else:
        print(
            "SKIP escritura real (requiere EDU_BRIDGE_SERVICE_TOKEN + --escribir-prueba --user-id=N)"
        )

    print()
    print("Para federación completa (operación en el hosting):")
    print("  1. SECRET_KEY idéntica en start y escuela (sin esto, 503 en escuela).")
    print("  2. EDU_BRIDGE_SERVICE_TOKEN idéntico en ambos.")
    print("  3. EDU_BRIDGE_URL=https://start.maxocracia.com en escuela.")
    print("  4. Desplegar este código en escuela (migraciones corren al arrancar).")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
