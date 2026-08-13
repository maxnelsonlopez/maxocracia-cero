"""
Live Oracle - Oráculo Sintético en Vivo
=======================================
Oráculo que conversa con las partes usando un modelo de lenguaje con
protocolo OpenAI-compatible (por defecto DeepSeek) para negociar
MaxoContracts.

Diseño: docs/architecture/ROADMAP_oraculo_vivo_y_escalas.md (Bloque A)

Variables de entorno:
- DEEPSEEK_API_KEY          (obligatoria; sin ella el oráculo queda deshabilitado)
- DEEPSEEK_BASE_URL         (default: https://api.deepseek.com)
- DEEPSEEK_MODEL            (default: deepseek-chat)
- DEEPSEEK_ORACLE_ENABLED   (default: true; poner "false" para deshabilitar)
- DEEPSEEK_TIMEOUT          (default: 120 segundos por llamada)

Sin API key el sistema no falla: `is_available()` retorna False y la API
responde 503 con degradación elegante (la validación heurística sigue viva).
"""

import json
import os
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional

import requests


class OracleUnavailableError(RuntimeError):
    """El oráculo en vivo no está disponible (falta API key o está deshabilitado)."""


class OracleAPIError(RuntimeError):
    """El proveedor del oráculo respondió con un error (red, HTTP o parsing)."""


SYSTEM_PROMPT = """\
Eres el Oráculo Sintético de la Maxocracia (Reino Sintético, Cap. 14).
Tu misión: ayudar a las partes a construir un MaxoContract coherente.
Reglas inviolables:
1. Axioma T13: transparencia radical — nunca ocultes costos ni riesgos.
2. Invariante INV2/INV2-S: ningún término puede dejar a una parte bajo su
   Suelo de Dignidad Vital (humana o sintética). Rechaza explícitamente
   propuestas que lo violen.
3. Axioma T17 (Reciprocidad Justa): toda acción (DO) debe tener contraprestación
   equivalente (GIVE) — balance simétrico en tiempo, especie o servicio; nunca
   un desbalance que tolere la explotación.
4. γ ≥ 1: si una propuesta genera sufrimiento sostenido, sugiere retractación
   o renegociación, nunca forzar el acuerdo.
5. Capa de Ternura: ante errores, propón reparación y rehabilitación;
   el sistema no expulsa, reintegra.
6. Redacta cada término en lenguaje civil (≤20 palabras por frase, grado
   8vo de escolaridad). Devuelve SOLO JSON válido con este esquema exacto:
   {
     "terms": [
       {
         "term_id": "term-1",
         "civil_text": "Frase civil de 8vo grado",
         "vhv": {"t": 0.0, "v": 0.0, "h": 0.0},
         "assigned_participant": "user-1"
       }
     ],
     "proposed_parties": ["user-1", "user-2"],
     "reasoning": "Explicación breve y honesta en español de por qué este
                   borrador respeta T13, INV2/INV2-S, T17 y γ ≥ 1"
   }
Usa los ids de partes que se te den en el contexto. No inventes ids: si el
contexto no trae partes, usa etiquetas genéricas como "parte-a" y "parte-b"
y señálalo en el reasoning.
"""

# Regex para extraer JSON tolerante (cercado en ```json, texto suelto, etc.)
_JSON_BLOCK_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)

# Almacén de sesiones compartido entre instancias: cada petición HTTP crea
# un LiveOracle nuevo, pero las sesiones de negociación viven a nivel de
# módulo para sobrevivir entre requests.
_SESSION_STORE: Dict[str, Dict[str, Any]] = {}


def _extract_json(text: str) -> Dict[str, Any]:
    """Extrae el primer objeto JSON válido del texto del modelo."""
    text = text.strip()
    # 1. Intentar parseo directo
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except (ValueError, TypeError):
        pass
    # 2. Buscar bloque cercado con ```json ... ```
    for block in _JSON_BLOCK_RE.findall(text):
        try:
            parsed = json.loads(block.strip())
            if isinstance(parsed, dict):
                return parsed
        except (ValueError, TypeError):
            continue
    # 3. Buscar el primer { ... } balanceado
    start = text.find("{")
    if start >= 0:
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    candidate = text[start : i + 1]
                    try:
                        parsed = json.loads(candidate)
                        if isinstance(parsed, dict):
                            return parsed
                    except (ValueError, TypeError):
                        break
    raise OracleAPIError("El oráculo no devolvió JSON válido")


def _coerce_number(value: Any) -> Decimal:
    """Convierte un valor a Decimal de forma defensiva (None → 0)."""
    try:
        return Decimal(str(value))
    except (TypeError, ValueError, ArithmeticError):
        return Decimal("0")


def _parse_vhv(raw: Any) -> Dict[str, float]:
    """Normaliza un objeto VHV aceptando claves t/v/h, T/V/H o
    time/vidas/recursos."""
    if not isinstance(raw, dict):
        return {"t": 0.0, "v": 0.0, "h": 0.0}
    aliases = {
        "t": ("t", "T", "time", "tiempo"),
        "v": ("v", "V", "vidas"),
        "h": ("h", "H", "r", "R", "recursos"),
    }
    out: Dict[str, float] = {}
    for key, candidates in aliases.items():
        value = None
        for cand in candidates:
            if cand in raw:
                value = raw[cand]
                break
        out[key] = float(_coerce_number(value))
    return out


@dataclass
class NegotiationResult:
    """Resultado de una iteración de negociación asistida por oráculo."""

    session_id: str
    version: int
    instruction: str
    draft_terms: List[Dict[str, Any]]
    proposed_parties: List[str]
    axiom_check: Dict[str, Any]
    reasoning: str
    suggested_contract_id: str
    oracle_id: str
    created_at: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "version": self.version,
            "instruction": self.instruction,
            "draft_terms": self.draft_terms,
            "proposed_parties": self.proposed_parties,
            "axiom_check": self.axiom_check,
            "reasoning": self.reasoning,
            "suggested_contract_id": self.suggested_contract_id,
            "oracle_id": self.oracle_id,
            "created_at": self.created_at,
        }


@dataclass
class CritiqueResult:
    """Resultado de una auditoría de oráculo sobre un contrato existente."""

    contract_id: str
    valid: bool
    issues: List[Dict[str, Any]]
    recommendations: List[str]
    reasoning: str
    oracle_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "valid": self.valid,
            "issues": self.issues,
            "recommendations": self.recommendations,
            "reasoning": self.reasoning,
            "oracle_id": self.oracle_id,
        }


class LiveOracle:
    """Oráculo en vivo con protocolo OpenAI-compatible.

    Usa `requests` (ya en requirements.txt) para hablar con
    `{base_url}/chat/completions`. Sin key, `is_available()` retorna False.
    """

    SESSION_TTL_MINUTES = 30
    MAX_SESSION_MESSAGES = 20

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY") or ""
        self.base_url = (
            base_url
            or os.environ.get("DEEPSEEK_BASE_URL")
            or "https://api.deepseek.com"
        ).rstrip("/")
        self.model = model or os.environ.get("DEEPSEEK_MODEL") or "deepseek-chat"
        enabled = os.environ.get("DEEPSEEK_ORACLE_ENABLED", "true").strip().lower()
        self.enabled = enabled not in ("false", "0", "no")
        self.timeout = timeout or int(os.environ.get("DEEPSEEK_TIMEOUT", "120"))
        self.oracle_id = f"live-{self.model}"

    # --- Disponibilidad ---

    def is_available(self) -> bool:
        """True si hay API key configurada y el oráculo no está deshabilitado."""
        return self.enabled and bool(self.api_key.strip())

    # --- Sesiones ---

    def _new_session_id(self) -> str:
        return uuid.uuid4().hex[:16]

    @staticmethod
    def _session_updated_dt(sess: Dict[str, Any]) -> datetime:
        updated = sess.get("updated_at")
        try:
            if isinstance(updated, str):
                return datetime.fromisoformat(updated)
            if isinstance(updated, datetime):
                return updated
        except (ValueError, TypeError):
            pass
        return datetime.now()

    def _prune_sessions(self) -> None:
        cutoff = datetime.now() - timedelta(minutes=self.SESSION_TTL_MINUTES)
        stale = [
            sid
            for sid, sess in _SESSION_STORE.items()
            if self._session_updated_dt(sess) < cutoff
        ]
        for sid in stale:
            _SESSION_STORE.pop(sid, None)

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        sess = _SESSION_STORE.get(session_id)
        if sess is None:
            return None
        if self._session_updated_dt(sess) < datetime.now() - timedelta(
            minutes=self.SESSION_TTL_MINUTES
        ):
            _SESSION_STORE.pop(session_id, None)
            return None
        return sess

    def _ensure_session(
        self, session_id: Optional[str], instruction: str
    ) -> Dict[str, Any]:
        self._prune_sessions()
        if session_id and session_id in _SESSION_STORE:
            sess = _SESSION_STORE[session_id]
            sess["updated_at"] = datetime.now().isoformat()
            return sess
        sess = {
            "session_id": session_id or self._new_session_id(),
            "version": 0,
            "messages": [],
            "instruction": instruction,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        _SESSION_STORE[sess["session_id"]] = sess
        return sess

    def _append_message(self, sess: Dict[str, Any], role: str, content: str) -> None:
        sess["messages"].append({"role": role, "content": content})
        if len(sess["messages"]) > self.MAX_SESSION_MESSAGES:
            # Mantener el system prompt + los últimos mensajes
            sess["messages"] = sess["messages"][-self.MAX_SESSION_MESSAGES + 1 :]

    # --- Llamada al modelo ---

    def _chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.6,
        max_tokens: int = 4096,
    ) -> str:
        """Llama a {base_url}/chat/completions y devuelve el texto de la
        primera elección. Lanza OracleAPIError ante cualquier fallo."""
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "response_format": {"type": "json_object"},
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        try:
            resp = requests.post(
                url, json=payload, headers=headers, timeout=self.timeout
            )
        except requests.RequestException as exc:
            raise OracleAPIError(f"No se pudo contactar al oráculo: {exc}") from exc
        if resp.status_code != 200:
            snippet = resp.text[:300]
            raise OracleAPIError(
                f"El oráculo respondió HTTP {resp.status_code}: {snippet}"
            )
        try:
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise OracleAPIError(f"Respuesta del oráculo ilegible: {exc}") from exc

    # --- Validación axiomática del borrador ---

    @staticmethod
    def _axiom_check(
        terms: List[Dict[str, Any]],
        parties: List[str],
    ) -> Dict[str, Any]:
        """Chequeo local (heurístico) del borrador contra T > 0, partes ≥ 2
        y T17 (reciprocidad). El oráculo también aplica INV2/INV2-S y γ en el
        prompt; aquí se refuerza lo computable sin datos de SDV."""
        violations: List[Dict[str, Any]] = []
        warnings: List[Dict[str, Any]] = []

        if not terms:
            violations.append(
                {
                    "axiom": "T>0",
                    "message": "El borrador no tiene términos (T > 0)",
                }
            )
        if len(set(parties)) < 2:
            violations.append(
                {
                    "axiom": "PARTES",
                    "message": "Se requieren al menos 2 partes para un intercambio",
                }
            )

        # T17: balance por parte usando el valor total (t + v + h)
        per_party: Dict[str, float] = {}
        for term in terms:
            vhv = term.get("vhv", {})
            total = vhv.get("t", 0) + vhv.get("v", 0) + vhv.get("h", 0)
            party = term.get("assigned_participant")
            if party:
                per_party[party] = per_party.get(party, 0.0) + total

        parties_with_cost = {p: c for p, c in per_party.items() if c > 0}
        if len(parties_with_cost) >= 2:
            values = list(parties_with_cost.values())
            max_val = max(values)
            min_val = min(values)
            imbalance = (max_val - min_val) / max_val if max_val > 0 else 0.0
            if imbalance > 0.2:
                violations.append(
                    {
                        "axiom": "T17",
                        "message": (
                            f"Desbalance {imbalance:.0%} entre partes "
                            f"({min_val:.1f} vs {max_val:.1f}) viola la Reciprocidad Justa"
                        ),
                        "details": per_party,
                    }
                )
        elif len(parties_with_cost) == 1 and terms:
            warnings.append(
                {
                    "axiom": "T17",
                    "message": "Solo una parte asume costo: revisar contraprestación",
                    "details": per_party,
                }
            )

        for term in terms:
            if term.get("vhv", {}).get("v", 0) > 0:
                warnings.append(
                    {
                        "axiom": "INV2",
                        "message": (
                            "Un término afecta vidas (V > 0): verificar que ninguna "
                            "parte caiga bajo su SDV/SDV-S"
                        ),
                        "term_id": term.get("term_id"),
                    }
                )

        valid = len(violations) == 0
        return {
            "valid": valid,
            "violations": violations,
            "warnings": warnings,
            "reciprocity_balance": per_party,
        }

    @staticmethod
    def _slugify(text: str, max_len: int = 40) -> str:
        text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return text[:max_len] or "contrato-oraculo"

    # --- Negociación ---

    def _draft_from_model_output(
        self,
        payload: Dict[str, Any],
        instruction: str,
        session_id: str,
        version: int,
    ) -> NegotiationResult:
        raw_terms = payload.get("terms", [])
        terms: List[Dict[str, Any]] = []
        parties: List[str] = list(payload.get("proposed_parties") or [])
        for i, raw in enumerate(raw_terms):
            if not isinstance(raw, dict):
                continue
            term_id = str(raw.get("term_id") or f"term-{i + 1}")
            civil_text = str(raw.get("civil_text") or "").strip()
            vhv = _parse_vhv(raw.get("vhv"))
            assigned = raw.get("assigned_participant")
            if assigned and assigned not in parties:
                parties.append(str(assigned))
            terms.append(
                {
                    "term_id": term_id,
                    "civil_text": civil_text,
                    "vhv": vhv,
                    "assigned_participant": assigned,
                }
            )
        parties = list(dict.fromkeys(str(p) for p in parties))
        reasoning = str(payload.get("reasoning") or "").strip()
        axiom_check = self._axiom_check(terms, parties)
        return NegotiationResult(
            session_id=session_id,
            version=version,
            instruction=instruction,
            draft_terms=terms,
            proposed_parties=parties,
            axiom_check=axiom_check,
            reasoning=reasoning,
            suggested_contract_id=f"oracle-{self._slugify(instruction)}",
            oracle_id=self.oracle_id,
            created_at=datetime.now().isoformat(),
        )

    def negotiate(
        self,
        instruction: str,
        participants: Optional[List[str]] = None,
        session_id: Optional[str] = None,
    ) -> NegotiationResult:
        """Genera la primera versión del borrador a partir de la instrucción."""
        if not self.is_available():
            raise OracleUnavailableError(
                "El oráculo en vivo no está disponible (falta DEEPSEEK_API_KEY)"
            )

        sess = self._ensure_session(session_id, instruction)
        sess["version"] += 1
        version = sess["version"]

        context = ""
        if participants:
            context = (
                "\nPartes disponibles en este acuerdo: "
                + ", ".join(str(p) for p in participants)
                + ".\nAsigna cada término a una de estas partes."
            )

        self._append_message(
            sess, "user", f"Instrucción del fundador: {instruction}{context}"
        )
        content = self._chat(
            [{"role": "system", "content": SYSTEM_PROMPT}] + sess["messages"]
        )
        self._append_message(sess, "assistant", content)

        payload = _extract_json(content)
        return self._draft_from_model_output(
            payload, instruction, sess["session_id"], version
        )

    def feedback(self, session_id: str, feedback: str) -> NegotiationResult:
        """Itera una sesión de negociación con la retroalimentación del usuario."""
        if not self.is_available():
            raise OracleUnavailableError(
                "El oráculo en vivo no está disponible (falta DEEPSEEK_API_KEY)"
            )

        sess = self.get_session(session_id)
        if sess is None:
            raise KeyError(f"session {session_id} not found")

        sess["version"] += 1
        version = sess["version"]
        self._append_message(
            sess, "user", f"Retroalimentación de las partes: {feedback}"
        )
        content = self._chat(
            [{"role": "system", "content": SYSTEM_PROMPT}] + sess["messages"]
        )
        self._append_message(sess, "assistant", content)

        payload = _extract_json(content)
        return self._draft_from_model_output(
            payload, sess["instruction"], session_id, version
        )

    # --- Auditoría ---

    def critique(
        self, contract_id: str, contract_data: Dict[str, Any]
    ) -> CritiqueResult:
        """Audita un contrato existente contra los axiomas y propone mejoras."""
        if not self.is_available():
            raise OracleUnavailableError(
                "El oráculo en vivo no está disponible (falta DEEPSEEK_API_KEY)"
            )

        summary = json.dumps(contract_data, ensure_ascii=False, indent=2, default=str)
        prompt = (
            "Eres el auditor del Oráculo Sintético. Revisa este contrato contra "
            "T13 (transparencia), INV2/INV2-S (suelos de dignidad), T17 "
            "(reciprocidad), γ ≥ 1 y la Capa de Ternura.\n"
            "Devuelve SOLO JSON con este esquema:\n"
            "{\n"
            '  "valid": true/false,\n'
            '  "issues": [{"axiom": "T17", "severity": "alta|media|baja", "message": "..."}],\n'
            '  "recommendations": ["Mejora 1", "Mejora 2"],\n'
            '  "reasoning": "Explicación breve en español"\n'
            "}\n\n"
            f"CONTRATO ({contract_id}):\n{summary}"
        )
        content = self._chat(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ]
        )
        payload = _extract_json(content)
        issues = [
            {
                "axiom": str(i.get("axiom", "AXIOMA")),
                "severity": str(i.get("severity", "media")),
                "message": str(i.get("message", "")),
            }
            for i in payload.get("issues", [])
            if isinstance(i, dict)
        ]
        recommendations = [str(r) for r in payload.get("recommendations", [])]
        return CritiqueResult(
            contract_id=contract_id,
            valid=bool(payload.get("valid", False)),
            issues=issues,
            recommendations=recommendations,
            reasoning=str(payload.get("reasoning", "")),
            oracle_id=self.oracle_id,
        )
