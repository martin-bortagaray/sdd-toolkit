---
description: "Fase 5→6 SDD — Verificación de spec pre-generación. Semáforo VERDE/AMARILLO/ROJO antes de generar código."
argument-hint: "[ID/ruta de la spec Approved]"
---

> **En Modo Flow (`/sdd-feature`, WORKFLOW v19) este paso no se invoca aparte:** su checklist corre dentro de la revisión unificada de Fase B, en el mismo subagente que la pasada adversaria. Este comando queda para el camino manual o para re-verificar una spec puntual.

Vas a ejecutar la **verificación pre-generación** del ciclo SDD: el semáforo de salida entre Fase 5 (aprobación) y Fase 6 (codegen). **No es una pasada adversaria** (eso ya ocurrió en Fase 4); verificás preparación operativa formal.

## Paso 1 — Cargá el prompt canónico, determiná el modo y el contexto

1. Leé el prompt maestro: `${CLAUDE_PLUGIN_ROOT}/prompts/06-spec-verification.prompt.md`. Ejecutá su checklist exactamente.
2. **Determiná el modo por track:** Rápido → EXPRESS; Estándar → COMPLETO (spec nueva) o DELTA (modificación); Completo → COMPLETO (ver `${CLAUDE_PLUGIN_ROOT}/protocols/track-routing.md`).
3. Leé la spec objetivo (**$ARGUMENTS**) y las specs dependientes de la sección 12. La guía `${CLAUDE_PLUGIN_ROOT}/templates/feature-spec.guide.md` solo puntualmente (la taxonomía de §9 ya está en el prompt). Setup foundacional: completo en modo COMPLETO; **carga selectiva según el CHANGE-SET** en DELTA/EXPRESS (matriz en `track-routing.md`).

## Paso 2 — Ejecutá el checklist según el modo

Ejecutá el checklist del prompt 06 (cargado en Paso 1) en el modo que corresponde. El alcance por modo:

- **COMPLETO** (spec nueva Estándar / Completo): F1–F8 + C1–C6; en modificaciones Completo sumá los chequeos delta D1–D3.
- **DELTA** (modificación Estándar): F1–F3 + D1–D3 + F5/F6/F7 y C1–C6 **acotados al CHANGE-SET**; no re-verifiques la base ya aprobada.
- **EXPRESS** (Rápido): F1–F3 + C3/C4/C5 acotados a la mini-spec o al delta (+ D1–D3 si es modificación).

**D3 es el control de honestidad del track:** si el contenido del delta excede su track declarado, es **BLOQUEANTE** — el track sube (válvula de escape) y los pasos salteados (ej: adversaria de spec) se ejecutan antes de Fase 6.

## Paso 3 — Veredicto

Generá el reporte en el formato del prompt canónico y terminá con un **VEREDICTO FINAL**:

- 🟢 **VERDE** → listo para Fase 6. Seguí con `/sdd-codegen`.
- 🟡 **AMARILLO** → por cada advertencia, decido conscientemente: resolver en la spec (sube versión, re-ejecutar) o aceptar y registrar en la sección 10.1 por qué la acepto. **No avanzar por inercia.**
- 🔴 **ROJO** → no se inicia Fase 6. Resolver bloqueantes (formal F → modificar spec; codegen C → puede requerir volver a Fase 2 discovery) antes de continuar.
