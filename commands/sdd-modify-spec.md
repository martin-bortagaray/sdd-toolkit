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

## Paso 4 — Editá, versioná, documentá

- Editá **solo las secciones afectadas**. Lenguaje preciso, densidad sobre volumen.
- Si el delta toca el modelo de datos → en código será una **nueva migración append-only** (nunca editar una ya corrida).
- **Subí la versión** (`AAAAMMDD-vN`), actualizá la Metadata (sección 1) y agregá una **entrada de changelog** concreta: qué secciones cambiaron, qué se agregó/modificó y por qué. Si estaba As-built, proponé pasarla a Implemented.
- Además del changelog (prosa, para humanos), preparate para emitir el **CHANGE-SET** en el cierre: el mismo delta pero estructurado (`ADDED/MODIFIED/REMOVED` + capa por ítem) para que el codegen lo consuma.
- Sección 14: decisiones operativas por defecto, "Pendiente de validación". Si no hubo, escribilo literal.
- Si aparece un **gap de producto** o conflicto con el setup: **PARÁ y avisame**, no lo resuelvas con tu criterio.

## Paso 5 — Cierre

Entregá tres bloques: (1) resumen del cambio (secciones tocadas, qué cambió, versión nueva, debilidades corregidas, hasta 3 puntos para Fase 4), (2) la spec modificada completa lista para reemplazar el archivo, y (3) el **CHANGE-SET estructurado** — el delta machine-readable con secciones `ADDED / MODIFIED / REMOVED`, cada ítem etiquetado con la capa que toca. El CHANGE-SET no es el changelog: es la señal que `/sdd-codegen` usa para regenerar solo lo que cambió. **No commitees** todavía.

Siguiente paso obligatorio: `/sdd-adversarial-spec` sobre la spec modificada (la Regla 4 no se relaja por ser "solo un cambio") → `/sdd-verify` → `/sdd-codegen` solo de las capas que el delta toca, **pasándole el CHANGE-SET como contexto**.
