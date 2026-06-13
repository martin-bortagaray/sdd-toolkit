---
description: "SDD — Modificar una spec existente (Implemented/As-built) para agregar o cambiar funcionalidad. Edición quirúrgica + sube versión + changelog."
argument-hint: "[ID/ruta de la spec a modificar] [ruta al output del discovery del delta]"
---

Vas a **modificar una spec que ya existe** (estado Implemented o As-built) para agregar o cambiar funcionalidad — el flujo de WORKFLOW sección 8.3. Regla fundamental: **NO tomás decisiones de producto** (ya están en el discovery del delta) y **editás con cirugía**, no reescribís la spec entera.

## Paso 1 — Cargá el prompt canónico y el contexto

1. Leé el prompt maestro: `${CLAUDE_PLUGIN_ROOT}/prompts/07-modify-spec.prompt.md`. Es la fuente de verdad.
2. Leé la guía: `${CLAUDE_PLUGIN_ROOT}/templates/feature-spec.guide.md`.
3. Identificá desde **$ARGUMENTS**: la spec a modificar (`sdd/specs/<ID>.md`) y el output del discovery del delta. Si no me pasaste el discovery del delta, hacelo primero con `/sdd-discovery` acotado al cambio.
4. Leé el setup foundacional de `sdd/foundation/` y las specs dependientes (sección 12).

## Paso 2 — Verificaciones (Paso 0 del prompt)

- **V1 — Sin pendientes** en el discovery del delta. Si hay `[PENDIENTE]` → **MODIFICACIÓN BLOQUEADA**, listalos y frená.
- **V2 — Decisiones por defecto validadas** en el discovery. Si falta alguna → **MODIFICACIÓN BLOQUEADA**, listalas y frená.
- **V3 — ¿Es realmente modificación de esta spec?** Frená y avisame si en realidad es: un **bug** (el sistema hace lo que la spec dice → `/sdd-bugfix`), una **capacidad independiente** (→ `/sdd-spec`, spec nueva), o un cambio que **se repite en varias features / es arquitectónico** (→ primero el setup foundacional, WORKFLOW 8.4).

## Paso 3 — Lectura crítica de la spec existente

Antes de editar, leé la spec completa y decime si refleja con precisión el comportamiento actual. **Ojo con las as-built:** suelen tener huecos por venir de ingeniería inversa. Si la base está floja, completarla es parte de este cambio (espíritu de Regla 5) — avisámelo antes de construir el delta encima.

## Paso 4 — Clasificá el tier y esperá mi confirmación

Proponeme el **tier de la modificación** (WORKFLOW 8.3.2) con justificación contra los criterios objetivos — "es un cambio chico" no es justificación:

- **T1 — Cosmético:** no toca modelo de datos (sección 6), ni reglas de negocio (sección 7), ni seguridad, ni introduce entidades/flujos/integraciones. Solo presentación (layout, textos, colores, orden, formato de salida).
- **T2 — Lógica acotada:** toca comportamiento (secciones 4/7/8/9) en funciones existentes, sin sección 6, sin entidades/flujos nuevos, sin seguridad.
- **T3 — Estructural:** toca sección 6, entidad/flujo/integración nueva, o seguridad.

**Si dudás entre dos tiers, proponé el superior.** No edites hasta que yo confirme el tier (Modo B). El tier determina qué pasos del ciclo se ejecutan después y va al header del CHANGE-SET + changelog de la spec.

## Paso 5 — Editá, versioná, documentá

- Editá **solo las secciones afectadas, directamente sobre el archivo** con la herramienta Edit (cambios quirúrgicos). **No re-emitas la spec completa en el chat:** ya está en el disco; reportá la lista de ediciones aplicadas. Lenguaje preciso, densidad sobre volumen.
- Si el delta toca el modelo de datos → en código será una **nueva migración append-only** (nunca editar una ya corrida).
- **Subí la versión** (`AAAAMMDD-vN`), actualizá la Metadata (sección 1) y agregá una **entrada de changelog** concreta: qué secciones cambiaron, qué se agregó/modificó, por qué, y el **tier confirmado**. Si estaba As-built, proponé pasarla a Implemented.
- Además del changelog (prosa, para humanos), preparate para emitir el **CHANGE-SET** en el cierre: el mismo delta pero estructurado (`ADDED/MODIFIED/REMOVED` + capa por ítem) para que el codegen lo consuma.
- Sección 14: decisiones operativas por defecto, "Pendiente de validación". Si no hubo, escribilo literal.
- Si aparece un **gap de producto** o conflicto con el setup: **PARÁ y avisame**, no lo resuelvas con tu criterio.

## Paso 6 — Cierre

Entregá tres bloques: (1) resumen del cambio (tier confirmado + justificación, secciones tocadas, qué cambió, versión nueva, debilidades corregidas, hasta 3 puntos para Fase 4 — omitir si es T1), (2) la lista de **ediciones aplicadas al archivo** (sección + qué cambió; la spec completa NO se re-emite), y (3) el **CHANGE-SET estructurado** — el delta machine-readable con `Tier` en el header y secciones `ADDED / MODIFIED / REMOVED`, cada ítem etiquetado con la capa que toca. El CHANGE-SET no es el changelog: es la señal que el resto del ciclo consume (scope del codegen + ruteo por tier). **No commitees** todavía.

Siguiente paso **según el tier** (WORKFLOW 8.3.2):

- **T1:** directo a `/sdd-verify` (modo express) → `/sdd-codegen` de las capas del CHANGE-SET (adversaria de código reemplazada por checks inline). La adversaria de spec se omite (excepción codificada de Regla 4).
- **T2:** `/sdd-adversarial-spec` acotada al delta (pasada 2 solo si la 1 tuvo bloqueantes) → `/sdd-verify` (modo delta) → `/sdd-codegen` con adversaria de código acotada al diff.
- **T3:** `/sdd-adversarial-spec` completa → `/sdd-verify` completo → `/sdd-codegen` con adversaria de código completa.

En todos los tiers: `/sdd-codegen` recibe el **CHANGE-SET como contexto** y antes del commit exige la **prueba manual** acotada a lo que el CHANGE-SET tocó (gate, WORKFLOW.md 7.5 — no se relaja en ningún tier). **Válvula de escape:** si en cualquier paso aparece evidencia de que el delta excede su tier, el tier sube, se actualiza el CHANGE-SET y se ejecutan los pasos salteados antes de continuar.
