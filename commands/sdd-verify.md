---
description: "Fase 5→6 SDD — Verificación de spec pre-generación. Semáforo VERDE/AMARILLO/ROJO antes de generar código."
argument-hint: "[ID/ruta de la spec Approved]"
---

Vas a ejecutar la **verificación pre-generación** del ciclo SDD: el semáforo de salida entre Fase 5 (aprobación) y Fase 6 (codegen). **No es una pasada adversaria** (eso ya ocurrió en Fase 4); verificás preparación operativa formal.

## Paso 1 — Cargá el prompt canónico y el contexto

1. Leé el prompt maestro: `${CLAUDE_PLUGIN_ROOT}/prompts/06-spec-verification.prompt.md`. Ejecutá su checklist exactamente.
2. Leé la spec objetivo (**$ARGUMENTS**), el setup foundacional de `sdd/foundation/`, las specs dependientes de la sección 12, y la guía `${CLAUDE_PLUGIN_ROOT}/templates/feature-spec.guide.md`.

## Paso 2 — Ejecutá las dos partes del checklist

- **Parte 1 — Checklist formal (F1–F8):** estado Approved, sin `[PENDIENTE]`/`TBD`, sección 14 validada, sección 10.1 con decisiones+trade-off, ≥5 criterios de aceptación verificables, taxonomía de 10 casos borde cubierta, consistencia con setup foundacional, dependencias reales en estado Approved/Implemented. Cada ítem: PASA / FALLA con justificación.
- **Parte 2 — Preparación para codegen (C1–C6):** modelo de datos detallado, reglas de negocio implementables, requerimientos sin ambigüedad, casos de error con comportamiento definido, notas de UI suficientes si aplica, stack compatible con `ARCHITECTURE.md`. Cada ítem: LISTO / ADVERTENCIA / BLOQUEANTE.

## Paso 3 — Veredicto

Generá el reporte en el formato del prompt canónico y terminá con un **VEREDICTO FINAL**:

- 🟢 **VERDE** → listo para Fase 6. Seguí con `/sdd-codegen`.
- 🟡 **AMARILLO** → por cada advertencia, decido conscientemente: resolver en la spec (sube versión, re-ejecutar) o aceptar y registrar en la sección 10.1 por qué la acepto. **No avanzar por inercia.**
- 🔴 **ROJO** → no se inicia Fase 6. Resolver bloqueantes (formal F → modificar spec; codegen C → puede requerir volver a Fase 2 discovery) antes de continuar.
