#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Validador Conceptual - Maxocracia Cero

Este script verifica la coherencia conceptual del código y la documentación del proyecto.
Valida:
1. Que no existan frases o citas prohibidas (versiones apócrifas del Axioma 4, etc.).
2. Que las menciones de los axiomas (1-8, T0-T13, V0-V8) utilicen la terminología oficial
   y no distorsionen los fundamentos del libro oficial.
"""

import os
import sys
import re
from typing import Dict, List, Tuple, Any

# ──────────────────────────────────────────────────────────────────
# CONFIGURACIÓN
# ──────────────────────────────────────────────────────────────────

# Carpetas a ignorar completamente en el escaneo
EXCLUDED_DIR_NAMES = {
    ".venv", ".git", "node_modules", ".next", "dist", ".pytest_cache",
    "__pycache__", ".vscode", "migrations", "tempmediaStorage",
    "traducciones", "ediciones_1_y_2", "legacy", "media", "out"
}

EXCLUDED_FILES = {
    "comun.db", "validador_conceptual.py", "test_validador_conceptual.py"
}

# Extensiones de archivos de texto válidas para escanear
ALLOWED_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".md", ".txt", ".html", ".css", ".sql"
}

# Frases globales prohibidas (ej. definiciones apócrifas históricas)
GLOBAL_FORBIDDEN_PHRASES: List[str] = [
    "verdad no necesita ser defendida",
    "solo necesita expandirse",
    "verdad no necesita ser convincente",
    "solo necesita ser visible",
]

# Definición de Axiomas Oficiales y palabras clave obligatorias para validación de contexto
# Soporta tanto las definiciones teóricas matemáticas como las de la implementación de MaxoContracts
AXIOMS_REGISTRY: Dict[str, Dict[str, Any]] = {
    # === AXIOMAS FUNDAMENTALES (1-8) ===
    "1": {
        "titles": ["La Verdad como Orientación Suprema", "Principio de la Brújula Interna"],
        "keywords": ["orientación suprema", "devoción epistémica", "brújula interna", "religión verdadera", "sentido", "brújula"],
    },
    "2": {
        "titles": ["El Deber de Buscar", "Principio del Compromiso Activo"],
        "keywords": ["deber de buscar", "compromiso activo", "no verdades", "prioridad metodológica", "búsqueda activa", "moral universal", "debes buscar", "buscar la verdad", "compromiso"],
    },
    "3": {
        "titles": ["La Complejidad de la Verdad", "Principio de la Profundidad"],
        "keywords": ["complejidad", "compleja", "profundidad", "robusta", "no es simple"],
    },
    "4": {
        "titles": ["El Camino Más Corto", "Principio de la Eficiencia Espiritual"],
        "keywords": ["camino más corto", "eficiencia epistémica", "contabilidad basada en tvi", "sucesos e información", "transparencia", "eficiencia", "espiritual"],
    },
    "5": {
        "titles": ["Objetividad Contextual", "Principio del Ojo Claro"],
        "keywords": ["ojo claro", "independiente del observador", "dependiente de su contexto", "contextual", "ojo"],
    },
    "6": {
        "titles": ["La Revelación Responsable", "Principio del Verbo Justo"],
        "keywords": ["revelación responsable", "verbo justo", "no toda verdad debe ser dicha", "veracidad suficiente", "sin ofuscación", "ofuscación", "verbo"],
    },
    "7": {
        "titles": ["La Utopía Alcanzable", "Principio del Optimismo Realista"],
        "keywords": ["utopía", "utopías", "optimismo realista", "verificable", "optimismo"],
    },
    "8": {
        "titles": ["La Supremacía Ontológica", "Principio de la Confianza Cósmica"],
        "keywords": ["supremacía ontológica", "confianza cósmica", "se estructura en la verdad", "confianza"],
    },
    
    # === AXIOMAS TEMPORALES (T0-T13) ===
    "T0": {
        "titles": ["Principio de Unicidad Existencial"],
        "keywords": ["unicidad existencial", "coordenada espacio-temporal", "tvi", "tiempo vital indexado", "superposici"],
    },
    "T1": {
        "titles": ["Finitud Absoluta"],
        "keywords": ["finitud absoluta", "finita", "no puede regenerarse", "almacenarse", "transferirse", "irreversibilidad", "finitud", "finitude"],
    },
    "T2": {
        "titles": ["Igualdad Temporal Fundamental"],
        "keywords": ["igualdad temporal", "valor existencial", "ser humano", "dignidad", "ratio", "tolerancia"],
    },
    "T3": {
        "titles": ["No-Fungibilidad Temporal"],
        "keywords": ["no-fungibilidad temporal", "tvi perdido", "único", "irrecuperable"],
    },
    "T4": {
        "titles": ["Materialización Temporal"],
        "keywords": ["materialización temporal", "tiempo cristalizado", "toda acción", "objeto", "servicio", "no renovable"],
    },
    "T5": {
        "titles": ["Interdependencia Temporal"],
        "keywords": ["interdependencia temporal", "consumir tvis", "pasado, presente o futuro", "recursos", "servicios"],
    },
    "T6": {
        "titles": ["Irreversibilidad Asimétrica del Retorno"],
        "keywords": ["irreversibilidad asimétrica", "verdadero retorno", "retrospectivamente", "inversión temporal"],
    },
    "T7": {
        "titles": ["Jerarquía Temporal", "Minimizar Daño"],
        "keywords": ["jerarquía temporal", "escalas temporales", "ta", "tvi", "tpi", "minimizar daño", "sufrimiento", "uvc", "afectadas"],
    },
    "T8": {
        "titles": ["Encadenamiento Temporal"],
        "keywords": ["encadenamiento temporal", "tiempo encadenado", "directo", "heredado", "futuro"],
    },
    "T9": {
        "titles": ["No-Antropocentrismo Temporal", "Reciprocidad Justa"],
        "keywords": ["no-antropocentrismo", "tiempo absoluto", "independientemente de la perspectiva humana", "reciprocidad justa", "balance", "desbalance", "tolerancia", "reciprocidad"],
    },
    "T10": {
        "titles": ["Responsabilidad Temporal Colectiva"],
        "keywords": ["responsabilidad temporal colectiva", "consume tvis ajenos", "medible"],
    },
    "T11": {
        "titles": ["Reconocimiento de Inversión Temporal Colectiva", "Verdad en Costos Reales"],
        "keywords": ["reconocimiento de inversión", "ratio beneficio/costo", "protegidas", "verdad en costos reales", "retractación", "retractaci", "libre"],
    },
    "T12": {
        "titles": ["Derecho a la Ineficiencia Política", "Sostenibilidad de Recursos"],
        "keywords": ["derecho a la ineficiencia", "actos políticos", "protesta", "huelga", "exentos", "sostenibilidad", "artistas", "capa ternura"],
    },
    "T13": {
        "titles": ["Transparencia Total de Cálculo", "Adaptabilidad"],
        "keywords": ["transparencia total", "cálculo de ta", "auditable", "disputa", "adaptabilidad", "hechos nuevos", "transparencia"],
    },

    # === AXIOMAS VITALES (V0-V8) ===
    "V0": {
        "titles": ["Principio de Herencia Evolutiva"],
        "keywords": ["herencia evolutiva", "adn", "tiempo evolutivo", "miles de millones de años"],
    },
    "V1": {
        "titles": ["Principio de Unicidad Biológica"],
        "keywords": ["unicidad biológica", "nft existencial", "solución evolutiva", "irrecuperable"],
    },
    "V2": {
        "titles": ["Principio de Interdependencia Vital", "Principio de Custodia Interdependiente"],
        "keywords": ["interdependencia vital", "custodia interdependiente", "responsabilidad fundamental", "secuencias vitales"],
    },
    "V3": {
        "titles": ["Principio de Custodia Intergeneracional"],
        "keywords": ["custodia intergeneracional", "patrimonio biológico", "reino humano", "custodio", "propietario"],
    },
    "V4": {
        "titles": ["Principio de Contabilidad Vital Completa"],
        "keywords": ["contabilidad vital completa", "costo real", "vidas consumidas", "consciencia", "sufrimiento"],
    },
    "V5": {
        "titles": ["Principio de Dignidad Experiencial"],
        "keywords": ["dignidad experiencial", "instancia de consciencia", "única e irrepetible"],
    },
    "V6": {
        "titles": ["Principio de Inconmensurabilidad Intra-Reino"],
        "keywords": ["inconmensurabilidad", "no puede ser reducida", "valor de otro ser"],
    },
    "V7": {
        "titles": ["Principio de Sufrimiento Innecesario"],
        "keywords": ["sufrimiento innecesario", "minimizar", "multiplicador de costo exponencial"],
    },
    "V8": {
        "titles": ["Principio de Deuda Existencial Reconocida"],
        "keywords": ["deuda existencial", "no puede saldarse", "consumido para beneficio"],
    },
}

# Regex para buscar "Axioma X" o "Axiom X" de manera flexible
AXIOM_MENTION_REGEX = re.compile(r'\b(?:Axioma|Axiom)\s*([TV]?\d+)\b', re.IGNORECASE)


# ──────────────────────────────────────────────────────────────────
# LÓGICA DE VALIDACIÓN
# ──────────────────────────────────────────────────────────────────

def safe_print(text: str):
    """Escribe en la salida estándar manejando errores de codificación (útil en Windows)."""
    try:
        sys.stdout.write(text + "\n")
        sys.stdout.flush()
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or 'utf-8'
        sys.stdout.write(text.encode(enc, errors='replace').decode(enc) + "\n")
        sys.stdout.flush()


def check_line_for_forbidden_phrases(line: str, filepath: str, line_num: int) -> List[str]:
    """Comprueba si la línea contiene alguna frase prohibida a nivel global."""
    errors = []
    line_lower = line.lower()
    for phrase in GLOBAL_FORBIDDEN_PHRASES:
        if phrase in line_lower:
            errors.append(
                f"[FRASE PROHIBIDA] En {filepath}:{line_num}\n"
                f"  -> Se encontró la frase obsoleta/apócrifa: '{phrase}'\n"
                f"  -> Línea: {line.strip()}"
            )
    return errors


def check_context_for_axiom_definition(
    axiom_id: str, context: str, filepath: str, line_num: int
) -> List[str]:
    """
    Comprueba si un texto (el contexto alrededor de la mención del axioma)
    contiene una definición válida para el Axioma correspondiente.
    """
    errors = []
    
    # Normalizar axioma_id (por ejemplo, '04' -> '4')
    norm_id = axiom_id.upper()
    if norm_id.startswith("T") or norm_id.startswith("V"):
        prefix = norm_id[0]
        try:
            num_part = str(int(norm_id[1:]))
            norm_id = prefix + num_part
        except ValueError:
            pass
    else:
        try:
            norm_id = str(int(norm_id))
        except ValueError:
            pass

    if norm_id not in AXIOMS_REGISTRY:
        return errors

    registry = AXIOMS_REGISTRY[norm_id]
    keywords = registry["keywords"]
    
    context_lower = context.lower()
    
    # Verificar si es un intento de definición
    # 1. Axioma X seguido directamente de un signo indicador (: = - ()
    # 2. Encabezado Markdown
    # 3. Mención del verbo "define", "significa" etc. inmediatamente cerca
    is_definition_attempt = (
        re.search(rf'\b(?:Axioma|Axiom)\s*{axiom_id}\b\s*[:=\-\(]', context, re.IGNORECASE) is not None
        or re.search(rf'###\s*(?:Axioma|Axiom)\s*{axiom_id}\b', context, re.IGNORECASE) is not None
        or re.search(rf'\b(?:Axioma|Axiom)\s*{axiom_id}\b\s+(?:define|significa|es decir)\b', context, re.IGNORECASE) is not None
        or re.search(rf'\b(?:AXIOM_?{axiom_id})\b\s*=', context, re.IGNORECASE) is not None
    )
    
    if is_definition_attempt:
        # Verificar que el contexto contenga al menos uno de los términos clave obligatorios
        has_keyword = any(kw in context_lower for kw in keywords)
        if not has_keyword:
            titles_str = " o ".join(f"'{t}'" for t in registry["titles"])
            keywords_str = ", ".join(f"'{k}'" for k in keywords[:3])
            errors.append(
                f"[COHERENCIA DE AXIOMA] En {filepath}:{line_num}\n"
                f"  -> Posible definición incorrecta o desactualizada para el Axioma {norm_id} ({titles_str}).\n"
                f"  -> Se requiere que contenga términos clave como: {keywords_str}\n"
                f"  -> Contexto: {context.strip()}"
            )
            
    return errors


def validate_file(filepath: str) -> List[str]:
    """Escanea un archivo línea por línea en busca de violaciones."""
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        return [f"[ERROR LECTURA] No se pudo leer {filepath}: {e}"]

    for i, line in enumerate(lines):
        line_num = i + 1
        
        # 1. Validar frases prohibidas
        forbidden_errors = check_line_for_forbidden_phrases(line, filepath, line_num)
        errors.extend(forbidden_errors)
        
        # 2. Validar consistencia de axiomas cuando son mencionados
        matches = AXIOM_MENTION_REGEX.findall(line)
        if matches:
            # Obtener contexto: la línea actual y la siguiente (si existe)
            next_line = lines[i + 1] if i + 1 < len(lines) else ""
            context = line + "\n" + next_line
            
            for axiom_id in matches:
                axiom_errors = check_context_for_axiom_definition(axiom_id, context, filepath, line_num)
                errors.extend(axiom_errors)
                
    return errors


def run_validador(root_dir: str) -> Tuple[int, List[str]]:
    """Camina recursivamente el directorio del proyecto y valida todos los archivos."""
    all_errors = []
    total_scanned = 0

    for root, dirs, files in os.walk(root_dir):
        # Excluir carpetas ignoradas in-place
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIR_NAMES]
        
        for file in files:
            if file in EXCLUDED_FILES:
                continue
                
            _, ext = os.path.splitext(file)
            if ext not in ALLOWED_EXTENSIONS:
                continue
                
            filepath = os.path.join(root, file)
            # Evitar escanear este mismo script y archivos de prueba del validador por ruta absoluta
            if "validador_conceptual" in filepath:
                continue
                
            total_scanned += 1
            file_errors = validate_file(filepath)
            all_errors.extend(file_errors)
            
    return total_scanned, all_errors


# ──────────────────────────────────────────────────────────────────
# EJECUCIÓN CLI
# ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Si se pasa un argumento, usarlo como directorio raíz, de lo contrario el directorio de trabajo actual
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    safe_print("=== Validador Conceptual de Axiomas ===")
    safe_print(f"Escaneando en: {os.path.abspath(project_root)}")
    
    scanned_count, errors = run_validador(project_root)
    
    safe_print(f"Archivos escaneados: {scanned_count}")
    
    if errors:
        safe_print(f"\n[ERROR] SE ENCONTRARON {len(errors)} VIOLACIONES CONCEPTUALES:\n")
        for err in errors:
            safe_print(err)
            safe_print("-" * 50)
        sys.exit(1)
    else:
        safe_print("\n[OK] ¡Todo perfecto! No se encontraron violaciones conceptuales en los axiomas.")
        sys.exit(0)
