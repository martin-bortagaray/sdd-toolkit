---
description: "Fase 3 SDD — Redacción del draft de spec (rol Redactor). Traduce el discovery al template, sin tomar decisiones de producto de alto impacto."
argument-hint: "[ruta al output del discovery] [ID de spec, ej: spec-013-...]"
---

Vas a ejecutar la **Fase 3 (Redacción)** del ciclo SDD en tu rol de **Redactor**. Regla fundamental: **NO tomás decisiones de producto de alto impacto** — esas ya se tomaron en el discovery (las de bajo impacto podés tomarlas con recomendación y van a §14, Regla 1 v20). Tu trabajo es traducir formato (pregunta-respuesta → spec narrativa), no interpretar contenido.

> **Modo profundo (WORKFLOW §6.0, v19):** este comando es la segunda mitad del camino manual `/sdd-discovery` → `/sdd-spec`, pensado para track **Completo** o cuando pedís explícitamente discovery sección por sección. Para Rápido y Estándar, `/sdd-feature` fusiona discovery + redacción (spec-first con preguntas en lote). Redactar en la misma sesión del discovery está permitido: la independencia que importa es la del Adversario, que corre en subagente limpio.

## Paso 1 — Cargá el prompt canónico y el contexto

1. Leé el prompt maestro: `${CLAUDE_PLUGIN_ROOT}/prompts/02-draft-spec.prompt.md`. Es la fuente de verdad de las reglas de redacción.
2. Leé el template y la guía: `${CLAUDE_PLUGIN_ROOT}/templates/feature-spec.template.md` (esqueleto a llenar) y `${CLAUDE_PLUGIN_ROOT}/templates/feature-spec.guide.md` (qué va en cada sección).
3. Leé el setup foundacional de `sdd/foundation/` y las specs dependientes (primer nivel) de `sdd/specs/`.
4. Leé el output del discovery: **$ARGUMENTS** (primer argumento = ruta; segundo = ID de spec asignado). Si no me pasaste ruta, pedímela.

## Paso 2 — Paso 0 obligatorio (verificación de pre-requisitos)

Antes de redactar una sola línea, verificá sobre el output del discovery:

- **Sin pendientes:** buscá `[PENDIENTE`. Si hay alguno sin resolver → **REDACCIÓN BLOQUEADA**, listámelos por sección y frená. (WORKFLOW 2.3 y 5.)
- **Decisiones por defecto validadas:** cada decisión por defecto del discovery debe tener nota "Validado por autor: aceptada / reemplazada por: ...". Si falta alguna → **REDACCIÓN BLOQUEADA**, listámelas y frená. (Regla 2.)

No redactes hasta que las dos verificaciones pasen.

## Paso 3 — Redactá

- Llená las 14 secciones del template + changelog. Lenguaje preciso: "debe/es/tiene", nunca "podría/idealmente/sería bueno". Densidad sobre volumen.
- Respetá la información del discovery exactamente — no la "mejores" ni la parafrasees.
- Si encontrás un **gap que requiere decisión de producto** (contradicción con el setup, ambigüedad real, sección sin cubrir), **PARÁ y avisame**. No lo resuelvas por tu cuenta ni lo disfraces de decisión operativa en la sección 14.
- Metadata: ID asignado, versión `AAAAMMDD-v1` (fecha de hoy), Estado **Draft**, autor Martin Bortagaray, toolkit usado (mirá la versión en `${CLAUDE_PLUGIN_ROOT}/workflow/WORKFLOW.md`).
- Sección 14: solo decisiones operativas menores, cada una "Pendiente de validación". Si no hay, escribilo literal.

## Paso 4 — Cierre

Generá un resumen corto (secciones con contenido vs "No aplica", estado de la sección 14, hasta 3 puntos débiles para Fase 4) y la spec completa lista para guardar como `sdd/specs/<ID>.md`. Actualizá `sdd/specs/INDEX.md` si existe (fila nueva, estado Draft). **No commitees** todavía. Siguiente paso: `/sdd-adversarial-spec` (Fase 4).
