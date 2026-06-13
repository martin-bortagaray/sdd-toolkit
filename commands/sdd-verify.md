---
description: "Fase 5→6 SDD — Verificación de spec pre-generación. Semáforo VERDE/AMARILLO/ROJO antes de generar código."
argument-hint: "[ID/ruta de la spec Approved]"
---

Vas a ejecutar la **verificación pre-generación** del ciclo SDD: el semáforo de salida entre Fase 5 (aprobación) y Fase 6 (codegen). **No es una pasada adversaria** (eso ya ocurrió en Fase 4); verificás preparación operativa formal.

## Paso 1 — Cargá el prompt canónico, determiná el modo y el contexto

1. Leé el prompt maestro: `${CLAUDE_PLUGIN_ROOT}/prompts/06-spec-verification.prompt.md`. Ejecutá su checklist exactamente.
2. **Determiná el modo (WORKFLOW 8.3.2):** si la spec viene de `/sdd-modify-spec`, leé el `Tier` del CHANGE-SET — **T1 → modo EXPRESS**, **T2 → modo DELTA**, **T3 → modo COMPLETO**. Sin CHANGE-SET (spec nueva) → COMPLETO.
3. Leé la spec objetivo (**$ARGUMENTS**), las specs dependientes de la sección 12, y la guía `${CLAUDE_PLUGIN_ROOT}/templates/feature-spec.guide.md`. Setup foundacional de `sdd/foundation/`: completo en modo COMPLETO; **carga selectiva según el CHANGE-SET** en DELTA/EXPRESS (CONVENTIONS+PRINCIPLES siempre; DOMAIN_MODEL/ARCHITECTURE/GLOSSARY según capas tocadas).

## Paso 2 — Ejecutá el checklist según el modo

- **Modo COMPLETO** — **Parte 1 (F1–F8):** estado Approved, sin `[PENDIENTE]`/`TBD`, sección 14 validada, sección 10.1 con decisiones+trade-off, ≥5 criterios de aceptación verificables, taxonomía de 10 casos borde cubierta, consistencia con setup foundacional, dependencias reales en estado Approved/Implemented. **Parte 2 (C1–C6):** modelo de datos detallado, reglas de negocio implementables, requerimientos sin ambigüedad, casos de error definidos, notas de UI suficientes, stack compatible. En modificaciones T3, sumá los chequeos delta D1–D3.
- **Modo DELTA (T2):** F1–F3 + chequeos delta **D1–D3** (versión+changelog con tier, CHANGE-SET↔spec coherentes, tier verificado contra el contenido) + F5/F6/F7 y C1–C6 **acotados a los ítems del CHANGE-SET**. No re-verifiques la base ya aprobada.
- **Modo EXPRESS (T1):** solo F1–F3 + **D1–D3** + C3/C4/C5 acotados al delta.
- **D3 es el control de honestidad del tier:** si el contenido del CHANGE-SET excede su tier declarado (toca sección 6/7 o seguridad), es **BLOQUEANTE** — el tier sube (válvula de escape) y los pasos salteados (ej: adversaria de spec) se ejecutan antes de Fase 6.

## Paso 3 — Veredicto

Generá el reporte en el formato del prompt canónico y terminá con un **VEREDICTO FINAL**:

- 🟢 **VERDE** → listo para Fase 6. Seguí con `/sdd-codegen`.
- 🟡 **AMARILLO** → por cada advertencia, decido conscientemente: resolver en la spec (sube versión, re-ejecutar) o aceptar y registrar en la sección 10.1 por qué la acepto. **No avanzar por inercia.**
- 🔴 **ROJO** → no se inicia Fase 6. Resolver bloqueantes (formal F → modificar spec; codegen C → puede requerir volver a Fase 2 discovery) antes de continuar.
