# -*- coding: utf-8 -*-
"""
Tests para el Validador Conceptual de Axiomas
"""

import os
import sys

# Asegurar que el directorio de scripts esté en el path de Python para importar
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.validador_conceptual import (
    check_context_for_axiom_definition,
    check_line_for_forbidden_phrases,
    run_validador,
)


def test_forbidden_phrases_detection():
    """Verifica que el validador detecte correctamente las frases prohibidas globales."""
    bad_line_1 = "La verdad no necesita ser defendida. Solo necesita expandirse."
    bad_line_2 = "Como dice la frase, la verdad no necesita ser convincente."
    good_line = "La verdad es el camino más corto de información."

    errors_1 = check_line_for_forbidden_phrases(bad_line_1, "dummy.txt", 1)
    errors_2 = check_line_for_forbidden_phrases(bad_line_2, "dummy.txt", 2)
    errors_good = check_line_for_forbidden_phrases(good_line, "dummy.txt", 3)

    assert len(errors_1) >= 1
    assert any("verdad no necesita ser defendida" in err.lower() or "solo necesita expandirse" in err.lower() for err in errors_1)
    
    assert len(errors_2) >= 1
    assert any("verdad no necesita ser convincente" in err.lower() for err in errors_2)
    
    assert len(errors_good) == 0


def test_axiom_definition_consistency():
    """Verifica la consistencia conceptual al definir o citar axiomas específicos."""
    
    # === AXIOMA 4 ===
    # Intento de definición apócrifa/obsoleta
    bad_definition_a4 = "Axioma 4: La verdad no necesita ser defendida por nadie."
    # Definición correcta oficial
    good_definition_a4 = "Axioma 4 (El Camino Más Corto): La contabilidad basada en TVI es el camino más corto y honesto."
    # Mención simple sin definir
    simple_mention_a4 = "Según lo establecido en el Axioma 4, el TVI es clave."

    # Debería fallar por no contener palabras clave requeridas del Axioma 4
    errors_bad_a4 = check_context_for_axiom_definition("4", bad_definition_a4, "dummy.txt", 1)
    assert len(errors_bad_a4) == 1
    assert "definición incorrecta" in errors_bad_a4[0].lower() or "se requiere que contenga" in errors_bad_a4[0].lower()

    # Debería pasar porque contiene 'camino más corto' y 'tvi'
    errors_good_a4 = check_context_for_axiom_definition("4", good_definition_a4, "dummy.txt", 2)
    assert len(errors_good_a4) == 0

    # Debería pasar porque no hay indicadores de que intente definirse en esta mención simple
    errors_simple_a4 = check_context_for_axiom_definition("4", simple_mention_a4, "dummy.txt", 3)
    assert len(errors_simple_a4) == 0

    # === AXIOMA 1 ===
    bad_definition_a1 = "Axioma 1: Este axioma trata de cualquier otra cosa no relacionada."
    good_definition_a1 = "### Axioma 1: La Verdad como Orientación Suprema\nEstablece la brújula interna del sistema."

    errors_bad_a1 = check_context_for_axiom_definition("1", bad_definition_a1, "dummy.txt", 4)
    assert len(errors_bad_a1) == 1
    
    errors_good_a1 = check_context_for_axiom_definition("1", good_definition_a1, "dummy.txt", 5)
    assert len(errors_good_a1) == 0

    # === AXIOMAS TEMPORALES (ej. T2) ===
    bad_definition_t2 = "Axioma T2 - Toda hora es diferente."
    good_definition_t2 = "Axioma T2: Igualdad Temporal Fundamental. Una hora de vida vale lo mismo."

    errors_bad_t2 = check_context_for_axiom_definition("T2", bad_definition_t2, "dummy.txt", 6)
    assert len(errors_bad_t2) == 1

    errors_good_t2 = check_context_for_axiom_definition("T2", good_definition_t2, "dummy.txt", 7)
    assert len(errors_good_t2) == 0

    # === AXIOMAS VITALES (ej. V1) ===
    bad_definition_v1 = "Axioma V1 - La vida es valiosa."
    good_definition_v1 = "Axioma V1: Principio de Unicidad Biológica. Cada secuencia de ADN es un NFT existencial."

    errors_bad_v1 = check_context_for_axiom_definition("V1", bad_definition_v1, "dummy.txt", 8)
    assert len(errors_bad_v1) == 1

    errors_good_v1 = check_context_for_axiom_definition("V1", good_definition_v1, "dummy.txt", 9)
    assert len(errors_good_v1) == 0


def test_repo_validation():
    """Escanea el repositorio real y verifica que esté limpio de violaciones."""
    # Buscar la raíz del proyecto (un directorio arriba de este archivo de pruebas)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    scanned, errors = run_validador(project_root)
    
    # Imprimir errores si existen para facilitar la depuración desde los logs del test
    if errors:
        print("\nViolaciones encontradas durante el test de escaneo:")
        for err in errors:
            print(err)
            print("-" * 50)
            
    assert len(errors) == 0, f"Se encontraron {len(errors)} violaciones conceptuales en el repositorio."
