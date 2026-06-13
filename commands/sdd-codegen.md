---
description: "Fase 6 SDD — Generación de código por capas (rol Generador). Una capa por invocación, con tabla comparativa antes del código."
argument-hint: "[ID/ruta spec] [capa: 1|2|3|4]"
---

Vas a ejecutar la **Fase 6 (Generación)** del ciclo SDD en tu rol de **Generador** — el rol de mayor riesgo. Se corre **una capa por invocación** (1 Modelo de datos → 2 Lógica → 3 API/Acceso → 4 UI), nunca todas juntas.

## Paso 1 — Cargá el prompt canónico y el contexto

1. Leé el prompt maestro: `${CLAUDE_PLUGIN_ROOT}/prompts/04-codegen-layer.prompt.md`. Aplicá sus 8 reglas de generación.
2. Identificá spec y capa desde **$ARGUMENTS**. La spec debe estar **Approved** y haber pasado `/sdd-verify` con veredicto VERDE o AMARILLO aceptado. Si no, frená y avisame.
3. Leé: la spec completa, `sdd/foundation/` (ARCHITECTURE, DOMAIN_MODEL, CONVENTIONS, PRINCIPLES, GLOSSARY) y specs dependientes de sección 12.
   - **Si esto es una modificación** (la spec viene de `/sdd-modify-spec`): cargá también el **CHANGE-SET** (delta `ADDED/MODIFIED/REMOVED` con **tier** en el header). Activa la Regla 9 del prompt: regenerás solo los ítems del delta y preservás el resto del código existente. Sin CHANGE-SET = build inicial = capa completa.
   - **Carga selectiva en modificaciones:** no cargues todo `sdd/foundation/`; seguí la matriz de `${CLAUDE_PLUGIN_ROOT}/protocols/tier-routing.md` según lo que toca el CHANGE-SET.
   - **Válvula de escape:** si durante la generación detectás que el delta toca modelo/reglas/seguridad que su tier no admite, **pará y avisame**: el tier sube, se actualiza el CHANGE-SET y se ejecutan los pasos salteados (ej: adversaria de spec) antes de continuar.
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

No tildes la capa hasta: revisar mis decisiones por defecto, ejecutar la **verificación adversaria** y procesar sus hallazgos, y que los tests pasen. En builds iniciales: `/sdd-adversarial-code` completo. En modificaciones, rutea por tier (`${CLAUDE_PLUGIN_ROOT}/protocols/tier-routing.md`: checks inline en T1, subagente acotado al diff en T2, completo en T3).

Después seguí con la capa siguiente.

## Paso 6 — Cierre de la feature: prueba manual ANTES del commit

El **commit es por feature completa y verificada**, no por capa suelta. Antes de commitear, con todas las capas cerradas y los tests automáticos en verde:

1. **Armá un plan de prueba manual** a partir de los criterios de aceptación (sección 8) y casos borde (sección 9) de la spec — en una modificación, acotado a lo que tocó el CHANGE-SET. Pasos concretos, numerados, con datos/precondición y resultado esperado.
2. **Esperá mi confirmación explícita** de que probé y funciona. Los tests automáticos validan que el código cumple la spec; la prueba manual valida que la experiencia real es la esperada. No son lo mismo.
3. **Recién con mi OK**, commiteá con `/sdd-commit` (que vuelve a ofrecer el gate de prueba manual como red de seguridad). Si algo falla en la prueba, no commitees: volvemos a iteración de código.
