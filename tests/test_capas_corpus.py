# -*- coding: utf-8 -*-
"""Tests de las capas del corpus (hito 3, 09-10-2026).

C0 (índice) siempre abre; C1 (axiomas + ledger + agenda) nunca se cae aunque
el presupuesto apriete; C2 rellena y lo que no quepa queda listado en el
manifiesto — jamás en silencio.
"""

from pathlib import Path

import pytest

from maxocontracts.concilio import canon as canon_mod

REPO = Path(__file__).resolve().parents[1]


def test_perfil_esencial_cabe_en_40k_y_trae_c1():
    """La firma barata: índice + ledger + axiomas + agenda, sin recortes."""
    texto, man = canon_mod.ensamblar_capas(str(REPO), perfil="esencial")
    assert man.perfil == "esencial"
    assert len(texto) <= 40_000
    assert man.degradada is False
    assert "INV1" in texto  # axiomas C1
    assert "corpus/registro-pre-ledger-" in texto  # ledger C1
    assert "[recortado por el Concilio]" not in texto


def test_manifiesto_del_completo_sin_degradacion_hoy():
    """El repo real cabe entero: nada omitido, nada recortado."""
    texto, man = canon_mod.ensamblar_capas(str(REPO))
    assert man.perfil == "completo"
    assert man.degradada is False
    assert man.omitidas() == []
    assert man.recortadas() == []
    assert len(texto) <= canon_mod.DEFAULT_MAX_CHARS


def test_degradacion_elegante_prioriza_c1():
    """Con presupuesto apretado C2 se cae listada, C1 sigue intacta."""
    texto, man = canon_mod.ensamblar_capas(str(REPO), total_max_chars=50_000)
    assert man.degradada is True
    assert man.omitidas() != []
    assert "INV1" in texto
    assert "maxocontracts/core/axioms.py" not in man.omitidas()
    assert "maxocontracts/core/axioms.py" not in man.recortadas()


def test_perfil_desconocido_falla_duro():
    with pytest.raises(ValueError):
        canon_mod.ensamblar_capas(str(REPO), perfil="oracular")


def test_read_canon_sigue_sirviendo_el_completo():
    """Compatibilidad: read_canon() es el perfil completo de siempre."""
    texto, _ = canon_mod.ensamblar_capas(str(REPO), perfil="completo")
    assert canon_mod.read_canon(str(REPO)) == texto
