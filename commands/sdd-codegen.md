---
description: "Fase 6 SDD — Generación de código por capas (rol Generador). Una capa por invocación, con tabla comparativa antes del código."
argument-hint: "[ID/ruta spec] [capa: 1|2|3|4]"
---

Vas a ejecutar la **Fase 6 (Generación)** del ciclo SDD en tu rol de **Generador** — el rol de mayor riesgo. Se corre **una capa por invocación** (1 Modelo de datos → 2 Lógica → 3 API/Acceso → 4 UI), nunca todas juntas.

## Paso 1 — Cargá el prompt canónico y el contexto

1. Leé el prompt maestro: `${CLAUDE_PLUGIN_ROOT}/prompts/04-codegen-layer.prompt.md`. Aplicá sus 8 reglas de generación.
2. Identificá spec y capa desde **$ARGUMENTS**. La spec debe estar **Approved** y haber pasado `/sdd-verify` con veredicto VERDE o AMARILLO aceptado. Si no, frená y avisame.
3. Leé: la spec completa, `sdd/foundation/` (ARCHITECTURE, DOMAIN_MODEL, CONVENTIONS, PRINCIPLES, GLOSSARY) y specs dependientes de sección 12.
   - **Si esto es una modificación** (la spec viene de `/sdd-modify-spec`): cargá también el **CHANGE-SET** (delta `ADDED/MODIFIED/REMOVED`). Activa la Regla 9 del prompt: regenerás solo los ítems del delta y preservás el resto del código existente. Sin CHANGE-SET = build inicial = capa completa.
4. **A partir de Capa 2:** leé también el código ya aprobado de capas anteriores y el **schema real de la base de datos** (migraciones en `sql/migrations/` o dump vivo). El modelo conceptual solo no alcanza — necesitás los nombres y tipos exactos desplegados.

> Recordá el mapeo de capas a tu arquitectura: en Next.js + Supabase, "Capa 3 — API/Acceso" puede ser RLS + funciones en Supabase, no endpoints FastAPI. Eso lo define `ARCHITECTURE.md`, no este comando.

## Paso 2 — Tabla comparativa ANTES del código (Paso 0 del prompt)

1. Identificá los requerimientos (sección 4), reglas de negocio (7), criterios de aceptación (8) y casos borde (9) que aplican a **esta capa**.
2. Generá la tabla `Requerimiento en spec | Implementación en esta capa | Cubierto/Parcial/No aplica en esta capa`. En una **modificación**, agregá la columna `Estado en el cambio` (Nuevo / Modificado / Sin cambios — no regenerar) cruzando cada fila contra el CHANGE-SET. Las filas "Sin cambios" no se tocan.
3. **Esperá mi confirmación explícita** ("tabla ok, generá") antes de escribir una sola línea de código.

## Paso 3 — Generá (tras mi confirmación)

- Código + tests de la capa, organizados por archivo según `CONVENTIONS.md`.
- **No sobre-ingenierar:** nada de atributos, validaciones, relaciones, endpoints o abstracciones que no estén en la spec o exigidos por convenciones/principios.
- Seguridad transversal (`PRINCIPLES.md`) aplicada en esta capa, no delegada a "la siguiente".
- Migraciones **append-only** en Capa 1 (nunca editar una migración ejecutada).
- Tras el código, listá **DECISIONES TÉCNICAS TOMADAS POR DEFECTO** (solo técnicas-operativas; nunca de producto). Si no hubo, escribilo literal.

## Paso 4 — Manejo de gaps

Si la spec dice X pero el setup dice algo incompatible, un requerimiento es ambiguo con consecuencias reales, o el código previo es inconsistente con lo que pide esta capa: **PARÁ, no implementes con tu criterio**, citá el conflicto y esperá mi decisión. Un gap ignorado en Capa 1 se propaga a Capa 4.

## Paso 5 — Antes de cerrar la capa

No tildes la capa hasta: revisar mis decisiones por defecto, correr `/sdd-adversarial-code` (pasada adversaria en subagente) y procesar sus hallazgos, y que los tests pasen. El **commit es por feature completa y verificada**, no por capa suelta (usá `/sdd-commit`). Después seguí con la capa siguiente.
