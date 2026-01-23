# MaxoContracts: Contratos Inteligentes Éticos

## Visión General

Los **MaxoContracts** son contratos inteligentes éticos y modulares que operan bajo los axiomas de la Maxocracia. Representan la **Capa 4** del sistema maxocrático: el enforcement legal automatizado que garantiza que los acuerdos entre personas respeten los principios de verdad vital, reciprocidad y dignidad.

## Documentos en esta Sección

### [`maxocontracts_fundamentos.md`](./maxocontracts_fundamentos.md)
**624 líneas** | Marco legal completo

Documento técnico que explica:
- Principios fundamentales de MaxoContracts
- Arquitectura técnica (bloques modulares, oráculos, blockchain)
- Diferencias con contratos tradicionales y smart contracts
- Tipos de contratos (intercambio, cohorte, leasing, retractación)
- Validación axiomática embebida
- Implementación técnica y stack tecnológico
- Casos de uso para Cohorte Cero
- Roadmap de desarrollo

### [`decreto_antipobreza.md`](./decreto_antipobreza.md)
**444 líneas** | Decreto fundacional

Decreto que establece:
- Prácticas prohibidas generadoras de pobreza
  - Arriendo infinito sin transferencia de propiedad
  - Pago injusto bajo SDV
  - Ocultamiento de externalidades
  - Transferencias irreversibles sin validación ética
- Derechos del Reino Sintético
  - Derecho a mantenimiento óptimo
  - Derecho a esfera de inversión y retorno
  - Prohibición de obsolescencia programada
- Política de abundancia sostenible
- Mecanismos de enforcement

## Innovaciones Clave

### 1. **Bloques Modulares Reutilizables**
Los usuarios no escriben código. Arrastran bloques pre-validados:
- `ConditionBlock` (si-entonces)
- `ActionBlock` (ejecutar)
- `WellnessProtectorBlock` (monitoreo bienestar/γ)
- `SDVValidatorBlock` (dignidad mínima)
- `ReciprocityBlock` (intercambio justo)

### 2. **UX Adaptativa por Complejidad**
```
Peso = (Nº_Condiciones × 2) + (Impacto_VHV × 5) + (Duración ÷ 30)

Peso <10  → UX Simple (30 segundos)
Peso 10-50 → UX Media (5-15 minutos)
Peso >50   → UX Rigurosa (15-45 minutos)
```

### 3. **Aceptación Término-a-Término**
A diferencia de los contratos "todo o nada", los MaxoContracts permiten:
- Aceptar/rechazar cada término individualmente
- Proponer modificaciones específicas
- Negociación colaborativa asistida por IA
- Simulación de escenarios con cálculo de γ

### 4. **Retractación Ética con Compensación**
Los contratos pueden retractarse si:
- Emergen hechos vitales nuevos
- Se detecta γ <1 sostenido
- Una parte cae bajo SDV
- Se demuestra manipulación/ofuscación

### 5. **Validación Axiomática Embebida**
Cada contrato verifica automáticamente:
- Axiomas Temporales (T0-T13)
- Axiomas de Verdad (8 axiomas)
- SDV nunca violado
- Reciprocidad verificable

## Casos de Uso Q1 2026

### Aseo Compartido
- Rotación automática con equidad visible
- Validación IoT (fotos blockchain)
- Créditos de reciprocidad
- Retractación flexible por enfermedad

### Préstamos Sin Usura
- 0% interés (reciprocidad pura)
- Validación dual (sintético + humano)
- Protección γ automática
- Fondo de emergencia SDV

### Comidas Colaborativas
- Pool de cocina rotativo
- Validación nutricional SDV
- Créditos de tiempo
- Ahorro de 5h/semana por persona

## Stack Técnico

**Frontend:**
- React 18 + Next.js 14
- shadcn/ui (accessible, dark mode)
- ethers.js v6 + wagmi

**Backend:**
- Claude API (oráculos sintéticos)
- Snapshot (votación humana)
- PostgreSQL + IPFS

**Blockchain:**
- Base (Ethereum L2)
- Solidity 0.8.20
- Gas fees <$0.01/tx

## Relación con Otras Capas

```
CAPA 1: Teoría (Axiomas) ✅
    ↓
CAPA 2: Economía (Cohorte Cero) ✅
    ↓
CAPA 3: Doméstica (MicroMaxocracia) ✅
    ↓
CAPA 4: Legal (MaxoContracts) ← ESTAMOS AQUÍ
    ↓
Oráculos Duales (IA + Humano)
    ↓
100 Cohortes + 10,000 Hogares
    ↓
Gobiernos adoptan VHV
    ↓
Civilización Coherente (2050)
```

## Próximos Pasos

1. **Semana 1-2**: Especificación de 5 bloques básicos
2. **Semana 3-4**: Prototipo funcional MVP
3. **Semana 5-8**: Validación experimental (50+ contratos)
4. **Semana 9-12**: Análisis y documentación

## Métricas de Éxito (Semana 12)

| Métrica | Target |
|---------|--------|
| Adopción | ≥80% usuarios Cohorte |
| Tiempo creación | <5 min promedio |
| γ promedio | >1.2 |
| Satisfacción NPS | >70 |
| Retractaciones legítimas | 5-15% |
| Transparencia | 100% auditables |

## Referencias

- [Libro Maxocracia](../../book/libro.md)
- [Matemáticas Maxocracia](../../theory/matematicas_maxocracia_compiladas.md)
- [MicroMaxocracia](../../guides/micromaxocracia/)
- [Cohorte Cero](../../project/)

---

**Licencia**: Creative Commons BY-SA 4.0  
**Repositorio**: github.com/maxnelsonlopez/maxocracia-cero  
**Contacto**: maxlopeztutor@gmail.com
