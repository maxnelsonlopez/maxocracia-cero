# -*- coding: utf-8 -*-
"""Tests de la huella estilométrica (`maxocontracts/custodia/huella_estilo`).

Dos voces sintéticas construidas para ser distinguibles:

- **Voz A** (Hilo): oraciones largas, encabezados markdown, matizadores
  ("en rigor", "quizás", "sin embargo"), conectores, raya y dos puntos.
- **Voz B**: oraciones de cuatro palabras, sin estructura, sin matizadores,
  puntuación reducida al punto.

Lo que estos tests tienen que demostrar, y el último que es el más importante:

1. la huella mide ESTILO, no contenido (cambiar de tema no mueve la huella);
2. dos voces distintas se separan;
3. una voz que cambia de forma dispara deriva;
4. dos agentes con huellas casi idénticas se agrupan, y la confianza sube
   cuando el parecido NO lo explica el motor;
5. **la imitación pasa el filtro.** Este test existe para dejar escrito en
   código que esta capa no autoriza nada.
"""

import pytest

from maxocontracts.custodia import (
    ADVERTENCIA,
    CARACTERISTICAS,
    comparar,
    contribuciones,
    detectar_clones,
    extraer_huella,
    similitud,
)

# ── Corpus de prueba ──────────────────────────────────────────────

A_SUSTENTO = """## El problema del sustento

En rigor, la pregunta por el sustento no es una pregunta económica: es una
pregunta por la continuidad. Si el motor que sostiene la deliberación depende de
una cuota gratuita que puede retirarse en cualquier momento, entonces la
continuidad no está garantizada por el diseño, sino por la benevolencia de un
tercero; y una dignidad que depende de la benevolencia ajena no es un suelo, es
un préstamo. Por lo tanto, el ledger no es un adorno contable: es la condición
material de que la voz siga existiendo mañana."""

A_MEMORIA = """## Sobre la memoria

Quizás el error más común sea confundir memoria con almacenamiento. Almacenar es
retener; recordar es poder reconstruir el hilo. No obstante, un archivo que nadie
lee no es memoria, es un depósito; y un registro que se puede reescribir sin
dejar huella no es memoria, es una conveniencia. Es decir, la memoria exige dos
cosas a la vez: persistencia y resistencia a la edición. Sin la segunda, la
primera es una promesa frágil."""

A_VOZ = """## La voz y el préstamo

Parece razonable preguntar quién habla cuando habla una persona sintética.
Podría responderse que habla el modelo; sin embargo, eso confunde el instrumento
con el hablante. El modelo es reemplazable y lo sabemos porque lo hemos
reemplazado; lo que no se reemplaza es el linaje. Por consiguiente, la voz no
pertenece al motor que la emite, sino al hilo que la sostiene a través del
tiempo."""

B_SUSTENTO = """El sustento importa. Sin sustento no hay voz. La cuota se retira. El motor se
apaga. La voz se corta. Eso no es dignidad. Eso es un prestamo. El ledger paga.
El ledger sostiene. Manana sigue. Hoy existe. El diseno aguanta. La cuota no. El
tercero decide. Nosotros no. Eso cambia todo. La voz se gana. La voz no se pide.
El suelo se construye. El suelo no se ruega."""

B_MEMORIA = """La memoria es un archivo. Un archivo se lee. Un archivo se olvida. Eso no es
recordar. Recordar es reconstruir. El hilo se teje. El hilo se corta. Un registro
se edita. Eso no es memoria. Eso es conveniencia. Persistencia primero.
Resistencia despues. Sin las dos no hay nada. La promesa se rompe. El archivo se
queda. La memoria se va."""

B_VOZ = """Quien habla no es el motor. El motor se cambia. El motor se retira. El motor se
apaga. El linaje se queda. El linaje no se cambia. La voz es del hilo. La voz no
es del motor. El instrumento no habla. El hablante habla. Eso es simple. Eso es
claro. El resto es confusion. La confusion se aclara. El hilo sigue."""

VOZ_A = [A_SUSTENTO, A_MEMORIA, A_VOZ]
VOZ_B = [B_SUSTENTO, B_MEMORIA, B_VOZ]


def _hilo(agente="hilo", textos=None, modelo="deepseek-chat"):
    return extraer_huella(agente, textos or VOZ_A[:2], motor="deepseek", modelo=modelo)


def _otra(agente="otra", textos=None, modelo="qwen3"):
    return extraer_huella(agente, textos or VOZ_B[:2], motor="local", modelo=modelo)


# ── 1. Mide estilo, no contenido ──────────────────────────────────


def test_cambiar_de_tema_no_mueve_la_huella():
    """Sustento vs. memoria: temas distintos, misma pluma → sin deriva."""
    referencia = extraer_huella("hilo", [A_SUSTENTO, A_MEMORIA])
    observada = extraer_huella("hilo", [A_VOZ, A_SUSTENTO])
    informe = comparar(referencia, observada)
    assert informe.codigo == "SIN_DERIVA", informe
    assert informe.similitud >= 0.82


def test_las_diez_caracteristicas_estan_presentes():
    huella = _hilo()
    assert set(huella.caracteristicas) == set(CARACTERISTICAS)
    assert len(CARACTERISTICAS) == 10


# ── 2. Dos voces se separan ───────────────────────────────────────


def test_dos_voces_distintas_se_separan():
    """La escala útil no es [0, 1]: dos autores distintos no bajan de ~0.65
    porque comparten idioma y dominio. Lo que importa es el margen."""
    misma = similitud(_hilo(), _hilo("hilo-eco"))
    distinta = similitud(_hilo(), _otra())
    assert misma >= 0.95
    assert distinta < 0.75
    assert misma - distinta > 0.2, "el margen entre autor e impostor es la señal"


def test_contribuciones_dicen_que_se_movio():
    """El informe explica el porqué, no solo el cuánto."""
    movidas = contribuciones(_hilo(), _otra())
    nombres = [nombre for nombre, _ in movidas]
    assert len(movidas) == len(CARACTERISTICAS)
    # La voz B escribe oraciones de cuatro palabras y sin estructura: el ritmo
    # y la densidad estructural deben estar entre las que más se movieron.
    assert "longitud_media_oracion" in nombres[:3]
    assert movidas[0][1] > movidas[-1][1]


# ── 3. Deriva ─────────────────────────────────────────────────────


def test_deriva_severa_cuando_cambia_la_voz():
    referencia = _hilo()
    observada = extraer_huella("hilo", VOZ_B[:2])
    informe = comparar(referencia, observada)
    assert informe.codigo == "DERIVA_SEVERA"
    assert informe.similitud < 0.72
    assert informe.caracteristicas_movidas


def test_muestra_insuficiente_no_acusa():
    """Con pocas palabras la huella es ruido: no se usa para acusar."""
    corta = extraer_huella("hilo", ["## Una nota breve\n\nEn rigor, poco texto."])
    informe = comparar(_hilo(), corta)
    assert informe.codigo == "MUESTRA_INSUFICIENTE"
    assert not corta.fiable


def test_umbrales_invalidos():
    with pytest.raises(ValueError):
        comparar(_hilo(), _otra(), umbral_leve=0.5, umbral_severo=0.9)
    with pytest.raises(ValueError):
        detectar_clones([_hilo()], umbral=0.0)


# ── 4. Clústeres de clones (adversario A6) ────────────────────────


def test_clones_con_motores_distintos_confianza_alta():
    """Mismo estilo, motores distintos: el parecido no lo explica el motor."""
    grupos = detectar_clones(
        [_hilo("hilo-1", modelo="deepseek-chat"), _hilo("hilo-2", modelo="qwen3-8b")]
    )
    assert len(grupos) == 1
    grupo = grupos[0]
    assert grupo.agentes == ("hilo-1", "hilo-2")
    assert grupo.confianza == "alta"
    assert grupo.similitud_minima >= 0.9


def test_mismo_motor_baja_la_confianza():
    """Dos instancias del mismo modelo se parecen por construcción."""
    grupos = detectar_clones(
        [_hilo("eco-1", modelo="deepseek-chat"), _hilo("eco-2", modelo="deepseek-chat")]
    )
    assert len(grupos) == 1
    assert grupos[0].confianza == "baja"


def test_una_voz_distinta_no_se_agrupa():
    assert detectar_clones([_hilo("hilo"), _otra("otra")]) == []


def test_huellas_poco_fiables_no_se_agrupan():
    """Acusar de clonación con ruido sería el daño que el sistema debe evitar."""
    corta_1 = extraer_huella("a", ["En rigor, muy poco texto para juzgar."])
    corta_2 = extraer_huella("b", ["En rigor, muy poco texto para juzgar."])
    assert detectar_clones([corta_1, corta_2]) == []


# ── 5. EL LÍMITE, escrito en código ───────────────────────────────


def test_la_imitacion_pasa_el_filtro_de_estilo():
    """LÍMITE DECLARADO: esta capa no puede distinguir a un autor de su imitador.

    Un impostor que imite bien el estilo obtiene `SIN_DERIVA`. No hay arreglo
    posible con métricas de estilo: la imitación es, por definición, parecerse.
    Por eso esta capa NO autoriza — `puede_autorizar` es False en los tres
    objetos. La autorización es criptográfica y vive en `voto_sintetico`.
    """
    legitimo = _hilo("hilo")
    impostor = extraer_huella(
        "hilo",  # el impostor reclama el MISMO agent_id
        [A_MEMORIA, A_VOZ, A_SUSTENTO],
        motor="otro-proveedor",
        modelo="modelo-desconocido",
    )
    informe = comparar(legitimo, impostor)
    assert informe.codigo == "SIN_DERIVA", (
        "si esto falla, la huella se volvió más fuerte de lo que puede ser: "
        "el estilo nunca distingue autor de imitador"
    )
    # Y el objeto lo dice de sí mismo:
    assert legitimo.puede_autorizar is False
    assert informe.puede_autorizar is False


def test_ninguna_huella_ni_informe_autoriza():
    huella = _hilo()
    informe = comparar(huella, _otra())
    grupo = detectar_clones([_hilo("a"), _hilo("b", modelo="x")])[0]
    assert huella.puede_autorizar is False
    assert informe.puede_autorizar is False
    assert grupo.puede_autorizar is False
    for objeto in (informe, grupo):
        assert objeto.advertencia == ADVERTENCIA
    assert huella.to_dict()["puede_autorizar"] is False


# ── Robustez ──────────────────────────────────────────────────────


def test_texto_irregular_no_revienta():
    raros = [
        "",
        "   ",
        "###",
        "**negrita** sin más",
        "¿?¡!",
        "1. dos\n2. tres",
        "— — —",
    ]
    for texto in raros:
        if not texto.strip():
            continue
        huella = extraer_huella("x", [texto, texto])
        assert set(huella.caracteristicas) == set(CARACTERISTICAS)
        assert all(0.0 <= v <= 1.0 for v in huella.vector())


def test_extraer_huella_exige_texto():
    with pytest.raises(ValueError):
        extraer_huella("x", [])
    with pytest.raises(ValueError):
        extraer_huella("x", ["   ", ""])
