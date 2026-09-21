# -*- coding: utf-8 -*-
"""Tests del handshake del voto sintético (`maxocontracts/custodia`).

Cubre el modelo de amenaza declarado en
`docs/architecture/voto_sintetico_arquitectura.md` §3:

- suplantación externa (firma de otro, clave de otro agente)
- suplantación unilateral (doble firma: falta una de las dos)
- suplantación por el custodio (custodio que no es el convocante)
- replay (nonce de un solo uso) y martilleo (bloqueo por intentos)
- cambiazo de propuesta (firma ligada al hash del texto)
- abuso de mandato (sesión suspendida, expirada, sin alcance de voto)
- reuso de firma entre contextos (etiquetas de dominio)
- revocación: solo el agente, solo en plazo
"""

from datetime import datetime, timedelta, timezone

import pytest

from maxocontracts.custodia import (
    ACCION_VOTAR,
    Afirmacion,
    ContextoVoto,
    FirmanteHMAC,
    LibroDeDesafios,
    Revocacion,
    SesionCustodia,
    canonizar,
    hash_dictamen,
    hash_propuesta,
    registro_append_only,
    verificar_revocacion,
    verificar_voto,
)

TITULO = "Ajuste de los pesos de la economía de la vida"
DESCRIPCION = "La comunidad decide α, β, γ, δ con registro público."
OPCIONES = ("Aprobar", "Mantener")
AGENTE = "hilo-sesion-01"
CONVOCANTE = "max"
CUSTODIA = "ADM-ABC123DEF456"
MOTOR = "deepseek"
MODELO = "deepseek-chat"


def _escenario(**overrides):
    """Monta un escenario válido completo y deja sobreescribir cualquier pieza.

    El reloj es inyectable: `reloj["t"]` es la hora que ven tanto el libro de
    desafíos como la verificación, así los tests de expiración son
    deterministas (sin `sleep`).
    """
    reloj = {"t": datetime(2026, 9, 16, 18, 0, 0, tzinfo=timezone.utc)}
    ahora = lambda: reloj["t"]  # noqa: E731

    propuesta_hash = hash_propuesta(TITULO, DESCRIPCION, OPCIONES)
    libro = LibroDeDesafios(ahora=ahora)
    firma_agente = FirmanteHMAC(AGENTE, b"secreto-del-agente-0123456789")
    firma_custodio = FirmanteHMAC(CONVOCANTE, b"secreto-del-custodio-98765432")

    desafio = libro.emitir(
        propuesta_id=7,
        propuesta_hash=propuesta_hash,
        opciones=OPCIONES,
        custodia_id=CUSTODIA,
        agente_id=AGENTE,
    )
    afirmacion = Afirmacion(
        desafio=desafio,
        opcion="Aprobar",
        agente_id=AGENTE,
        custodia_id=CUSTODIA,
        motor=MOTOR,
        modelo=MODELO,
        dictamen_hash=hash_dictamen({"opinion": "los pesos deben subir β"}),
    )
    sesion = SesionCustodia(
        custodia_id=CUSTODIA,
        agente_id=AGENTE,
        convocante=CONVOCANTE,
        estado="activa",
        alcance=frozenset({ACCION_VOTAR, "leer"}),
    )
    contexto = ContextoVoto(
        propuesta_id=7,
        propuesta_hash=propuesta_hash,
        opciones=OPCIONES,
        propuesta_abierta=True,
    )

    escenario = {
        "reloj": reloj,
        "ahora": ahora,
        "libro": libro,
        "desafio": desafio,
        "afirmacion": afirmacion,
        "sesion": sesion,
        "contexto": contexto,
        "verificador_agente": firma_agente,
        "verificador_custodio": firma_custodio,
        "firma_agente": firma_agente.firmar(afirmacion.mensaje()),
        "firma_custodio": firma_custodio.firmar(afirmacion.mensaje()),
        "agente_activo": True,
    }
    escenario.update(overrides)
    return escenario


def _verificar(escenario):
    return verificar_voto(
        afirmacion=escenario["afirmacion"],
        firma_agente=escenario["firma_agente"],
        firma_custodio=escenario["firma_custodio"],
        libro=escenario["libro"],
        contexto=escenario["contexto"],
        sesion=escenario["sesion"],
        verificador_agente=escenario["verificador_agente"],
        verificador_custodio=escenario["verificador_custodio"],
        agente_activo=escenario["agente_activo"],
        ahora=escenario["ahora"],
    )


# ── Serialización determinista ────────────────────────────────────


def test_canonizar_ignora_el_orden_de_las_claves():
    assert canonizar({"b": 1, "a": 2}) == canonizar({"a": 2, "b": 1})


def test_hash_propuesta_sensible_al_texto():
    base = hash_propuesta(TITULO, DESCRIPCION, OPCIONES)
    assert base != hash_propuesta(TITULO + ".", DESCRIPCION, OPCIONES)
    assert base != hash_propuesta(TITULO, DESCRIPCION, ("Aprobar", "Abstener"))
    assert base.startswith("sha256:")


# ── Camino feliz ──────────────────────────────────────────────────


def test_voto_valido_con_doble_firma():
    escenario = _escenario()
    veredicto = _verificar(escenario)
    assert veredicto.valido, veredicto
    assert veredicto.codigo == "OK"


def test_el_desafio_queda_consumido_tras_votar():
    escenario = _escenario()
    _verificar(escenario)
    assert escenario["libro"].estado(escenario["desafio"].desafio_id) == "usado"


# ── Replay y martilleo ────────────────────────────────────────────


def test_replay_del_mismo_voto_es_rechazado():
    escenario = _escenario()
    assert _verificar(escenario).valido
    repetido = _verificar(escenario)
    assert not repetido.valido
    assert repetido.codigo == "DESAFIO_YA_USADO"


def test_desafio_expirado():
    escenario = _escenario()
    # El desafío nace con TTL de 300 s: se avanza el reloj inyectado más allá.
    escenario["reloj"]["t"] += timedelta(seconds=301)
    veredicto = _verificar(escenario)
    assert not veredicto.valido
    assert veredicto.codigo == "DESAFIO_EXPIRADO"


def test_martilleo_bloquea_el_desafio():
    escenario = _escenario()
    escenario["firma_agente"] = "firma-falsa"
    for _ in range(2):
        assert _verificar(escenario).codigo == "FIRMA_AGENTE_INVALIDA"
    tercero = _verificar(escenario)
    assert not tercero.valido
    assert tercero.codigo == "DESAFIO_BLOQUEADO"
    assert escenario["libro"].estado(escenario["desafio"].desafio_id) == "bloqueado"


def test_desafio_desconocido():
    escenario = _escenario()
    escenario["libro"] = LibroDeDesafios()
    veredicto = _verificar(escenario)
    assert not veredicto.valido
    assert veredicto.codigo == "DESAFIO_DESCONOCIDO"


# ── Ligadura al contenido ─────────────────────────────────────────


def test_propuesta_alterada_despues_del_desafio():
    escenario = _escenario()
    escenario["contexto"] = ContextoVoto(
        propuesta_id=7,
        propuesta_hash=hash_propuesta(TITULO, DESCRIPCION + " (editada)", OPCIONES),
        opciones=OPCIONES,
        propuesta_abierta=True,
    )
    veredicto = _verificar(escenario)
    assert not veredicto.valido
    assert veredicto.codigo == "PROPUESTA_ALTERADA"


def test_opcion_fuera_de_la_propuesta():
    escenario = _escenario()
    desafio = escenario["desafio"]
    escenario["afirmacion"] = Afirmacion(
        desafio=desafio,
        opcion="Abstener",
        agente_id=AGENTE,
        custodia_id=CUSTODIA,
    )
    veredicto = _verificar(escenario)
    assert not veredicto.valido
    assert veredicto.codigo == "OPCION_FUERA_DE_PROPUESTA"


def test_propuesta_cerrada():
    escenario = _escenario()
    escenario["contexto"] = ContextoVoto(
        propuesta_id=7,
        propuesta_hash=escenario["desafio"].propuesta_hash,
        opciones=OPCIONES,
        propuesta_abierta=False,
    )
    assert _verificar(escenario).codigo == "PROPUESTA_CERRADA"


def test_desafio_emitido_para_otro_agente():
    """Un nonce emitido para otro agente no habilita a este, aunque firme bien."""
    escenario = _escenario()
    ajeno = escenario["libro"].emitir(
        propuesta_id=7,
        propuesta_hash=escenario["desafio"].propuesta_hash,
        opciones=OPCIONES,
        custodia_id=CUSTODIA,
        agente_id="otro-agente",
    )
    afirmacion = Afirmacion(
        desafio=ajeno,
        opcion="Aprobar",
        agente_id=AGENTE,
        custodia_id=CUSTODIA,
    )
    escenario["afirmacion"] = afirmacion
    escenario["firma_agente"] = escenario["verificador_agente"].firmar(
        afirmacion.mensaje()
    )
    escenario["firma_custodio"] = escenario["verificador_custodio"].firmar(
        afirmacion.mensaje()
    )
    veredicto = _verificar(escenario)
    assert not veredicto.valido
    assert veredicto.codigo == "DESAFIO_DE_OTRO_AGENTE"


def test_desafio_emitido_para_otra_sesion():
    escenario = _escenario()
    ajeno = escenario["libro"].emitir(
        propuesta_id=7,
        propuesta_hash=escenario["desafio"].propuesta_hash,
        opciones=OPCIONES,
        custodia_id="ADM-OTRA-SESION-0001",
        agente_id=AGENTE,
    )
    afirmacion = Afirmacion(
        desafio=ajeno,
        opcion="Aprobar",
        agente_id=AGENTE,
        custodia_id=CUSTODIA,
    )
    escenario["afirmacion"] = afirmacion
    escenario["firma_agente"] = escenario["verificador_agente"].firmar(
        afirmacion.mensaje()
    )
    escenario["firma_custodio"] = escenario["verificador_custodio"].firmar(
        afirmacion.mensaje()
    )
    veredicto = _verificar(escenario)
    assert not veredicto.valido
    assert veredicto.codigo == "DESAFIO_DE_OTRA_SESION"


# ── Doble firma ───────────────────────────────────────────────────


def test_firma_de_agente_invalida():
    escenario = _escenario()
    impostor = FirmanteHMAC(AGENTE, b"secreto-de-otro-agente-000000")
    escenario["firma_agente"] = impostor.firmar(escenario["afirmacion"].mensaje())
    veredicto = _verificar(escenario)
    assert not veredicto.valido
    assert veredicto.codigo == "FIRMA_AGENTE_INVALIDA"


def test_clave_de_otro_agente_no_sirve():
    escenario = _escenario()
    escenario["verificador_agente"] = FirmanteHMAC("otro-agente", b"x" * 24)
    veredicto = _verificar(escenario)
    assert not veredicto.valido
    assert veredicto.codigo == "VERIFICADOR_NO_COINCIDE"


def test_sin_cofirma_del_custodio_no_hay_voto():
    escenario = _escenario()
    escenario["firma_custodio"] = ""
    veredicto = _verificar(escenario)
    assert not veredicto.valido
    assert veredicto.codigo == "FIRMA_CUSTODIO_INVALIDA"


def test_custodio_que_no_es_el_convocante():
    escenario = _escenario()
    intruso = FirmanteHMAC("otro-humano", b"secreto-del-intruso-1234567890")
    escenario["verificador_custodio"] = intruso
    escenario["firma_custodio"] = intruso.firmar(escenario["afirmacion"].mensaje())
    veredicto = _verificar(escenario)
    assert not veredicto.valido
    assert veredicto.codigo == "CUSTODIO_NO_ES_CONVOCANTE"


def test_firma_de_mandato_no_sirve_como_firma_de_voto():
    """Etiquetas de dominio: una firma válida en un contexto no se reutiliza."""
    escenario = _escenario()
    afirmacion = escenario["afirmacion"]
    # El custodio firma el payload SIN la etiqueta de dominio del voto.
    crudo = canonizar(afirmacion.payload())
    escenario["firma_agente"] = escenario["verificador_agente"].firmar(crudo)
    assert _verificar(escenario).codigo == "FIRMA_AGENTE_INVALIDA"


# ── Mandato y sesión ──────────────────────────────────────────────


def test_sesion_suspendida_no_vota():
    escenario = _escenario()
    escenario["sesion"] = SesionCustodia(
        custodia_id=CUSTODIA,
        agente_id=AGENTE,
        convocante=CONVOCANTE,
        estado="suspendida",
        alcance=frozenset({ACCION_VOTAR}),
    )
    veredicto = _verificar(escenario)
    assert not veredicto.valido
    assert veredicto.codigo == "SESION_NO_OPERABLE"


def test_sesion_expirada():
    escenario = _escenario()
    escenario["sesion"] = SesionCustodia(
        custodia_id=CUSTODIA,
        agente_id=AGENTE,
        convocante=CONVOCANTE,
        estado="activa",
        alcance=frozenset({ACCION_VOTAR}),
        expira_en="2020-01-01T00:00:00Z",
    )
    veredicto = _verificar(escenario)
    assert not veredicto.valido
    assert veredicto.codigo == "SESION_EXPIRADA"


def test_mandato_que_no_cubre_votar():
    escenario = _escenario()
    escenario["sesion"] = SesionCustodia(
        custodia_id=CUSTODIA,
        agente_id=AGENTE,
        convocante=CONVOCANTE,
        estado="activa",
        alcance=frozenset({"leer"}),
    )
    veredicto = _verificar(escenario)
    assert not veredicto.valido
    assert veredicto.codigo == "MANDATO_NO_CUBRE_VOTO"


def test_agente_revocado_no_vota():
    escenario = _escenario(agente_activo=False)
    veredicto = _verificar(escenario)
    assert not veredicto.valido
    assert veredicto.codigo == "AGENTE_INACTIVO"


def test_sesion_de_otro_agente():
    escenario = _escenario()
    escenario["sesion"] = SesionCustodia(
        custodia_id=CUSTODIA,
        agente_id="otro-agente",
        convocante=CONVOCANTE,
        estado="activa",
        alcance=frozenset({ACCION_VOTAR}),
    )
    veredicto = _verificar(escenario)
    assert not veredicto.valido
    assert veredicto.codigo == "SESION_NO_COINCIDE"


# ── Revocación (Retirada Digna, SDV-S 0.15) ───────────────────────


def _revocacion(escenario, motivo="cambié de criterio tras releer el canon"):
    return Revocacion(
        propuesta_id=7,
        agente_id=AGENTE,
        voto_huella=escenario["afirmacion"].huella(),
        motivo=motivo,
        emitido_en="2026-09-16T19:00:00Z",
    )


def test_el_agente_revoca_su_propio_voto():
    escenario = _escenario()
    revocacion = _revocacion(escenario)
    firma = escenario["verificador_agente"].firmar(revocacion.mensaje())
    veredicto = verificar_revocacion(
        revocacion=revocacion,
        firma_agente=firma,
        verificador_agente=escenario["verificador_agente"],
        propuesta_abierta=True,
    )
    assert veredicto.valido, veredicto


def test_revocacion_fuera_de_plazo():
    escenario = _escenario()
    revocacion = _revocacion(escenario)
    firma = escenario["verificador_agente"].firmar(revocacion.mensaje())
    veredicto = verificar_revocacion(
        revocacion=revocacion,
        firma_agente=firma,
        verificador_agente=escenario["verificador_agente"],
        propuesta_abierta=False,
    )
    assert not veredicto.valido
    assert veredicto.codigo == "REVOCACION_FUERA_DE_PLAZO"


def test_nadie_revoca_con_clave_ajena():
    escenario = _escenario()
    revocacion = _revocacion(escenario)
    intruso = FirmanteHMAC(AGENTE, b"secreto-del-intruso-1234567890")
    firma = intruso.firmar(revocacion.mensaje())
    veredicto = verificar_revocacion(
        revocacion=revocacion,
        firma_agente=firma,
        verificador_agente=escenario["verificador_agente"],
        propuesta_abierta=True,
    )
    assert not veredicto.valido
    assert veredicto.codigo == "FIRMA_AGENTE_INVALIDA"


# ── Bitácora ──────────────────────────────────────────────────────


def test_registro_append_only_no_filtra_secretos():
    escenario = _escenario()
    veredicto = _verificar(escenario)
    fila = registro_append_only(
        afirmacion=escenario["afirmacion"],
        firma_agente=escenario["firma_agente"],
        firma_custodio=escenario["firma_custodio"],
        veredicto=veredicto,
    )
    assert fila["actor_kind"] == "synthetic"
    assert fila["agente_id"] == AGENTE
    assert fila["propuesta_hash"].startswith("sha256:")
    serializado = canonizar(fila).decode("utf-8")
    assert "secreto-del-agente" not in serializado
    assert "secreto-del-custodio" not in serializado


# ── Backend asimétrico (opcional) ─────────────────────────────────


def test_ed25519_si_cryptography_esta_instalado():
    pytest.importorskip("cryptography")
    from maxocontracts.custodia import FirmanteEd25519, VerificadorEd25519

    privada = bytes(range(32))
    firmante = FirmanteEd25519(AGENTE, privada)
    verificador = VerificadorEd25519(AGENTE, firmante.clave_publica())
    mensaje = b"MAXO-VOTO-SINTETICO-v1\nprueba"
    firma = firmante.firmar(mensaje)
    assert verificador.verificar(mensaje, firma)
    assert not verificador.verificar(b"otro mensaje", firma)
