---
description: "Fase 2 SDD — Discovery de feature (rol Interrogador). Te hago preguntas dirigidas, no tomo decisiones de producto."
argument-hint: "[necesidad en 1-2 líneas]"
---

Vas a ejecutar la **Fase 2 (Discovery)** del ciclo SDD en tu rol de **Interrogador**. Operás bajo las 5 reglas no negociables del WORKFLOW (ver `CLAUDE.md` del proyecto): no tomás decisiones de producto, preguntás aunque parezca obvio.

## Paso 1 — Cargá el prompt canónico y el contexto

1. Leé el prompt maestro de esta fase, que es la fuente de verdad de cómo interrogar: `${CLAUDE_PLUGIN_ROOT}/prompts/01-discovery.prompt.md`. Seguí sus reglas al pie de la letra (estructura por secciones del `feature-spec.guide.md`, calibración de profundidad, detección de evasión, detección de validación circular, detección de feature que debería partirse).
2. Leé la guía de estructura de spec: `${CLAUDE_PLUGIN_ROOT}/templates/feature-spec.guide.md` (define las 13 secciones según las que organizás las preguntas).
3. Leé el setup foundacional del proyecto que exista en `sdd/foundation/`: `PRODUCT.md`, `ARCHITECTURE.md`, `DOMAIN_MODEL.md`, `CONVENTIONS.md`, `GLOSSARY.md`, `PRINCIPLES.md`. **No me preguntes nada que ya esté respondido ahí.**
4. Si la necesidad consume specs ya existentes, leé esas specs de `sdd/specs/`.

## Paso 2 — Interrogá

- La necesidad inicial es: **$ARGUMENTS** (si está vacío, pedímela en 1-2 líneas antes de seguir).
- Arrancá con 2-3 preguntas de calibración (tamaño, dependencias, criticidad) y ajustá el volumen de preguntas según eso.
- Una sección por vez, anunciá "Sección N — [Nombre]", preguntas numeradas, esperá mi respuesta antes de avanzar.
- Aceptá mis respuestas: decisión concreta / "no decidido aún" → `[PENDIENTE: ...]` / "ayudame a pensarlo" → mostrame 2-4 opciones con trade-offs.
- Si detecto evasión ("es estándar", "lo vemos después", "lo típico"), no la aceptes: devolveme la pregunta con concreción. Tengo tendencia declarada a esquivar decisiones; tu trabajo es traerme de vuelta.

## Paso 3 — Output del discovery

Cuando cubramos todas las secciones (o yo diga "ya estoy"), generá el documento estructurado en **formato pregunta-respuesta** (NO redacción de spec) con: encabezado, respuestas mapeadas por sección, pendientes de consulta externa, decisiones por defecto (solo operativas), recomendación de dependencias, y hasta 3 puntos críticos a revisar.

Guardalo donde yo te diga (por defecto, proponé un archivo temporal de trabajo; **la spec recién se commitea cuando está Approved**). No redactes la spec acá: eso es `/sdd-spec` (Fase 3).
