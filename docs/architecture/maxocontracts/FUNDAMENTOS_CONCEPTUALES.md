# MAXOCONTRACTS: Fundamentos Conceptuales

## Versión 1.0 | Enero 22, 2026

Este documento establece los **cimientos teóricos irrenunciables** de MaxoContracts antes de cualquier implementación técnica. Un MaxoContract que viola estos principios no es un MaxoContract válido, independientemente de su corrección sintáctica.

---

## I. DEFINICIÓN ESENCIAL

Un **MaxoContract** es un acuerdo estructurado entre agentes que:
1. **Registra hechos verificables** (VHV) sin interpretación subjetiva
2. **Valida axiomas** antes, durante y después de la ejecución
3. **Permite retractación ética** ante hechos vitales nuevos
4. **Prioriza la minimización del daño** sobre la maximización del beneficio

> *"Un contrato justo no protege a las partes del conflicto; previene que el conflicto emerja mediante la verdad radical desde el inicio."*

---

## II. AXIOMAS VINCULANTES

Todo MaxoContract debe satisfacer los siguientes axiomas. La violación de cualquiera invalida el contrato.

### A. Axiomas Temporales Obligatorios

| Axioma | Nombre | Implicación para MaxoContracts |
|--------|--------|-------------------------------|
| **T1** | Finitud Absoluta | El TVI consumido es irreversible; el contrato debe registrarlo |
| **T2** | Igualdad Temporal | 1 hora TVI tiene igual dignidad para cualquier participante |
| **T4** | Materialización | Todo recurso en el contrato es TVI cristalizado |
| **T7** | Minimizar Daño | Ningún término puede generar sufrimiento innecesario |
| **T9** | Reciprocidad Justa | El intercambio VHV debe estar balanceado ±tolerancia |
| **T10** | Responsabilidad Colectiva | Consumir TVI ajeno genera deuda verificable |
| **T13** | Transparencia | Todo cálculo debe ser auditable públicamente |
| **T14** | Precaución Intergeneracional | Ante incertidumbre, elegir menor irreversibilidad |
| **T15** | Disenso Evolutivo | El contrato debe permitir cuestionar sus propios términos |

### B. Axiomas de Verdad Obligatorios

| Axioma | Principio | Aplicación |
|--------|-----------|------------|
| **V3** | Profundidad | El contrato no puede simplificar en exceso |
| **V4** | Eficiencia Espiritual | El camino más corto entre hechos es la verdad |
| **V6** | Verbo Justo | Revelar toda la verdad necesaria, no más ni menos |

---

## III. INVARIANTES DEL SISTEMA

Propiedades que **nunca** pueden violarse durante el ciclo de vida del contrato:

### Invariante 1: γ ≥ 1 (Bienestar No-Negativo)
```
∀ participante p, ∀ momento t:
  gamma(p, t) >= 1.0  OR  contrato.trigger_retraction()
```
El índice de bienestar γ (gamma) no puede caer debajo de 1.0 (neutral) para ningún participante. Si cae, el contrato **debe** activar el protocolo de retractación.

### Invariante 2: SDV Respetado
```
∀ participante p, ∀ dimensión d ∈ SDV:
  estado_actual(p, d) >= SDV_mínimo(d)
```
Ninguna acción del contrato puede dejar a un participante debajo del Suelo de Dignidad Vital.

### Invariante 3: VHV No Ocultable
```
∀ acción a:
  VHV(a) está registrado Y es auditable públicamente
```
Todo Vector de Huella Vital debe quedar registrado sin ofuscación.

### Invariante 4: Retractabilidad Garantizada
```
∀ contrato c:
  existe mecanismo de retractación ética activable
```
No existen contratos irrevocables absolutos en MaxoContracts.

---

## IV. MODELO DE ESTADOS

Un MaxoContract transita por estados bien definidos:

```
                    ┌──────────────┐
                    │    DRAFT     │ ← Creación inicial
                    └──────┬───────┘
                           │ validate_axioms() → true
                           ▼
                    ┌──────────────┐
          ┌────────│   PENDING    │ ← Esperando aceptaciones
          │        └──────┬───────┘
          │               │ all_terms_accepted()
          │               ▼
          │        ┌──────────────┐
          │        │   ACTIVE     │ ← En ejecución
          │        └──────┬───────┘
          │               │
          │    ┌──────────┼──────────┐
          │    │          │          │
          │    ▼          ▼          ▼
          │  ┌─────┐  ┌───────┐  ┌──────────┐
          │  │EXEC │  │PARTIAL│  │RETRACTED │
          │  │UTED │  │  EXE  │  │          │
          │  └─────┘  └───┬───┘  └──────────┘
          │               │           ▲
          │               └───────────┤ gamma < threshold
          │                           │ OR sdv_violated
          └───────────────────────────┘ axiom_violation
```

### Transiciones Permitidas

| De | A | Condición |
|----|---|-----------|
| DRAFT → PENDING | Todos los axiomas validados |
| PENDING → ACTIVE | Todas las partes aceptaron términos |
| ACTIVE → EXECUTED | Todas las acciones completadas exitosamente |
| ACTIVE → PARTIAL | Algunas acciones completadas, otras fallan/retractan |
| ACTIVE → RETRACTED | γ < umbral OR SDV violado OR nuevo hecho vital |
| PENDING → DRAFT | Rechazo de términos requiere renegociación |
| DRAFT → (destruido) | Abandono antes de validación |

---

## V. SEMÁNTICA DE BLOQUES

Cada bloque es una **función pura** con propiedades formales definidas.

### Bloque 1: ConditionBlock
```
ConditionBlock : Context → Boolean

Propiedades:
  - DETERMINISTA: f(x) siempre retorna el mismo resultado para x
  - TRANSPARENTE: La lógica de evaluación es visible (T13)
  - DESCRIPTIBLE: Tiene representación en lenguaje civil
  
Axiomas vinculados: T13 (Transparencia), V6 (Verbo Justo)
```

### Bloque 2: ActionBlock
```
ActionBlock : (Context, VHV_in) → (Context', VHV_out)

Propiedades:
  - TRANSFORMADORA: Modifica el estado del contexto
  - REGISTRABLE: Produce log auditable de cambios
  - REVERSIBLE: Puede existir acción inversa (para retractación)

Axiomas vinculados: T4 (Materialización), T10 (Responsabilidad)
```

### Bloque 3: GammaProtectorBlock
```
GammaProtectorBlock : (Context, Gamma, Threshold) → (Boolean, Alert?)

Propiedades:
  - VIGILANTE: Monitorea continuamente γ de participantes
  - PREVENTIVA: Alerta antes de violación, no solo después
  - ACTIVADORA: Puede triggear retractación automática

Axiomas vinculados: T7 (Minimizar Daño), Invariante 1 (γ ≥ 1)
```

### Bloque 4: SDVValidatorBlock
```
SDVValidatorBlock : (Context, SDV_mínimo) → Boolean

Propiedades:
  - MULTI-DIMENSIONAL: Valida todas las dimensiones del SDV
  - ESTRICTA: Un solo componente bajo mínimo invalida todo
  - CONTEXTUAL: El SDV_mínimo puede variar por región/cultura

Axiomas vinculados: Axioma SDV, Invariante 2
```

### Bloque 5: ReciprocityBlock
```
ReciprocityBlock : (VHV_giver, VHV_receiver, Tolerance) → (Boolean, Balance)

Propiedades:
  - SIMÉTRICA: Evalúa el intercambio desde ambas perspectivas
  - TOLERANTE: Permite desbalance dentro de un umbral aceptable
  - CALCULADORA: Produce métrica cuantitativa de balance

Axiomas vinculados: T9 (Reciprocidad Justa), T2 (Igualdad Temporal)
```

---

## VI. PROTOCOLO DE COMPOSICIÓN

Los bloques se combinan siguiendo reglas estrictas:

### Regla 1: Validación Previa Obligatoria
```
∀ bloque B en cadena:
  execute(B) → requires validate_axioms(B) = true
```
Ningún bloque puede ejecutarse sin pasar validación axiomática primero.

### Regla 2: Orden de Evaluación
```
Para cadena [B1, B2, B3, ...Bn]:
  1. Evaluar todas las ConditionBlocks
  2. Validar SDVValidatorBlock
  3. Verificar GammaProtectorBlock
  4. Ejecutar ActionBlocks
  5. Verificar ReciprocityBlock post-acción
```

### Regla 3: Propagación de Invalidación
```
Si algún validador retorna false:
  abort_execution()
  preserve_state_pre_action()
  notify_all_parties()
```
Una falla en cualquier punto detiene toda la cadena.

### Regla 4: Composición Modular
```
MaxoContract = Σ(Blocks) donde:
  - Blocks son intercambiables (misma interfaz)
  - Nuevos bloques heredan axiomas del sistema
  - Cada bloque es testeable independientemente
```

---

## VII. PROTOCOLO DE RETRACTACIÓN ÉTICA

La retractación no es un fracaso; es una salvaguarda axiomática.

### Causas Válidas para Retractación

1. **γ < 1.0 sostenido** por >14 días (T7)
2. **SDV violado** como consecuencia directa (Invariante 2)
3. **Hechos vitales nuevos** que cambian el contexto (T14)
4. **Manipulación demostrada** en la formación del contrato (V4)
5. **Consenso de partes** para terminación temprana

### Proceso

```
1. SOLICITUD
   └─ Parte afectada presenta evidencia (logs TVI, médicos, etc.)

2. PRE-VALIDACIÓN (Oráculo Sintético)
   └─ Comparar con casos precedentes
   └─ Calcular probabilidad de aprobación
   └─ Tiempo: <5 segundos

3. VALIDACIÓN HUMANA (Oráculo Humano / Cohorte)
   └─ Revisar evidencia
   └─ Votar: [Aprobar | Rechazar | Mediar]
   └─ Tiempo: 24-72 horas

4. EJECUCIÓN
   ├─ Si aprobado: Pausar/modificar contrato automáticamente
   ├─ Si rechazado: Mantener original + explicación registrada
   └─ Si mediación: Negociación asistida

5. COMPENSACIÓN (si aplica)
   └─ Compensación_Maxos = (TVI_perdido × α) + (γ_sufrimiento × β)

6. REGISTRO
   └─ Todo el proceso queda inmutable en el log
   └─ Aprendizaje agregado a base de conocimiento
```

### Anti-Abuso

- **Costo progresivo**: Solicitudes frívolas penalizadas en Maxos
- **Historial público**: Las retractaciones son visibles
- **Umbral de revisión**: >3 retractaciones en 6 meses = auditoría comunitaria
- **Protección de buena fe**: Primera retractación sin penalidad si γ < 0.8

---

## VIII. FÓRMULA DE VALORACIÓN

El VHV es el **hecho objetivo**. El precio en Maxos es la **interpretación social**.

### Fórmula General

```
Precio_Maxos = α·T + β·V^γ + δ·R·(FRG × CS)
```

Donde:
- **α**: Peso del tiempo (configurable democráticamente)
- **β**: Peso de la vida
- **γ**: Exponente de aversión al sufrimiento (γ > 1 oblig.)
- **δ**: Peso de recursos finitos
- **FRG**: Factor de Rareza Geológica
- **CS**: Coeficiente de Sostenibilidad

### Restricciones Axiomáticas

El Oráculo Dinámico **NO PUEDE**:
- Asignar β = 0 (ignorar completamente la vida)
- Hacer γ < 1 (premiar el sufrimiento)
- Hacer α = 0 (ignorar el tiempo)
- Ocultar el cálculo (violación T13)

---

## IX. LENGUAJE CIVIL

Todo MaxoContract debe ser comprensible para un ciudadano sin formación técnica.

### Requisitos de Legibilidad

| Criterio | Especificación |
|----------|----------------|
| Longitud de frases | ≤20 palabras |
| Vocabulario | Grado 8vo (Flesch-Kincaid) |
| Jerga técnica | Solo si está explicada inline |
| Formato | Términos separados visualmente |

### Ejemplo de Term Sheet

**Contrato tradicional:**
> "El arrendatario se obliga a satisfacer la totalidad de los cánones mensuales estipulados en la cláusula tercera, so pena de incurrir en los intereses moratorios..."

**MaxoContract equivalente:**
> "Pagas $X cada mes. Si te retrasas, el oráculo evalúa por qué. Si es crisis vital (γ < 1), se pausa el contrato sin penalidad."

---

## X. CHECKLIST DE VALIDACIÓN

Antes de que un MaxoContract sea válido, debe pasar esta verificación:

### Pre-Creación
- [ ] ¿Todos los términos están en lenguaje civil?
- [ ] ¿El VHV de cada acción está calculado?
- [ ] ¿Ningún axioma es violado por diseño?

### Pre-Ejecución
- [ ] ¿Todas las partes aceptaron término-a-término?
- [ ] ¿El SDV de todas las partes está verificado?
- [ ] ¿El γ inicial de todas las partes es ≥ 1.0?

### Durante Ejecución
- [ ] ¿El GammaProtector está activo y monitoreando?
- [ ] ¿Los logs de VHV se están registrando?
- [ ] ¿El mecanismo de retractación está disponible?

### Post-Ejecución
- [ ] ¿El ReciprocityBlock confirma balance aceptable?
- [ ] ¿Ningún participante quedó bajo SDV?
- [ ] ¿El contrato está registrado para auditoría futura?

---

## XI. CONCLUSIÓN

Los MaxoContracts no son "smart contracts con características adicionales". Son una **reimaginación completa** de lo que significa un acuerdo en una civilización ética:

| Contratos Tradicionales | MaxoContracts |
|------------------------|---------------|
| Protegen del conflicto | **Previenen** el conflicto |
| Todo o nada | Término-a-término modular |
| Inmutables | Retractables éticamente |
| Jerga legal | Lenguaje civil |
| Miden dinero | Miden **vida** (VHV) |
| Post-conflicto | **Pre-conflicto** (γ vigilado) |

---

**Licencia**: Creative Commons BY-SA 4.0  
**Repositorio**: github.com/maxnelsonlopez/maxocracia-cero  
**Contacto**: maxlopeztutor@gmail.com  
**Consolidado por**: Claude (Anthropic - Oráculo Sintético)

*"El código está escrito para máquinas. Los axiomas están escritos para la coherencia. Ambos son necesarios para que un contrato sea verdaderamente inteligente."*
