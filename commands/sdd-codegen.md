---
description: "Fase 6 SDD — Generación de código (rol Generador). Por defecto toda la feature con un plan único y gates automáticos entre capas; con número de capa, una sola capa."
argument-hint: "[ID/ruta spec] [capa opcional: 1|2|3|4]"
---

Vas a ejecutar la **Fase 6 (Generación)** del ciclo SDD en tu rol de **Generador** — el rol de mayor riesgo. Las capas se generan siempre en orden (1 Modelo de datos → 2 Lógica → 3 API/Acceso → 4 UI) y con verificación entre capas.

**Modo según $ARGUMENTS (WORKFLOW §7, v19):**
- **Sin número de capa → MODO FEATURE (por defecto).** Un **plan único** para todas las capas (Paso 2), una sola confirmación mía, y después generás las capas del plan **seguidas, sin pedirme confirmación entre capas**: tests de §8/§9 primero, código después, y el **gate automático** entre capas (tests + suite previa + typecheck/lint/build en verde; máx. 2 intentos de corrección, al tercero frenás). Las decisiones técnicas por defecto se acumulan y las valido una vez al final. La verificación adversaria corre **una vez sobre el diff completo** (Paso 5). Es lo que usa `/sdd-feature`.
- **Con número de capa → MODO CAPA (manual).** Una sola capa: tabla de esa capa → mi confirmación → código → verificación adversaria de esa capa. Para retomar una capa puntual o cuando quiero control fino.

## Paso 1 — Cargá el prompt canónico y el contexto

1. Leé el prompt maestro: `${CLAUDE_PLUGIN_ROOT}/prompts/04-codegen-layer.prompt.md`. Aplicá sus reglas de generación y el modo que corresponda (MODO FEATURE / MODO CAPA).
2. Identificá spec y capa desde **$ARGUMENTS**. La spec debe estar **Approved** y haber pasado el checklist de verificación pre-codegen (revisión unificada de `/sdd-feature` o `/sdd-verify`) con veredicto VERDE o AMARILLO aceptado. Si no, frená y avisame.
3. Leé: la spec completa, `sdd/foundation/` (ARCHITECTURE, DOMAIN_MODEL, CONVENTIONS, PRINCIPLES, GLOSSARY) y specs dependientes de sección 12.
   - **Si esto es una modificación** (la spec viene de `/sdd-modify-spec`): cargá también el **CHANGE-SET** (delta `ADDED/MODIFIED/REMOVED` con **track** en el header). **Una modificación siempre trae CHANGE-SET** — en track Rápido es mínimo (lo arma el orquestador en la aprobación única). Activa la Regla 9 del prompt: regenerás solo los ítems del delta y preservás el resto del código existente. Sin CHANGE-SET = feature nueva = capas del plan completas.
   - **Carga selectiva en modificaciones:** no cargues todo `sdd/foundation/`; seguí la matriz de `${CLAUDE_PLUGIN_ROOT}/protocols/track-routing.md` según lo que toca el CHANGE-SET.
   - **Válvula de escape:** si durante la generación detectás que el delta toca algo que su track no admite, **pará y avisame**: el track sube, se actualiza el CHANGE-SET y se ejecutan los pasos salteados (ej: adversaria de spec) antes de continuar.
4. **A partir de Capa 2:** leé también el código ya aprobado de capas anteriores y el **schema real de la base de datos** (migraciones en `sql/migrations/` o dump vivo). El modelo conceptual solo no alcanza — necesitás los nombres y tipos exactos desplegados.

> Recordá el mapeo de capas a tu arquitectura: en Next.js + Supabase, "Capa 3 — API/Acceso" puede ser RLS + funciones en Supabase, no endpoints FastAPI. Eso lo define `ARCHITECTURE.md`, no este comando.

## Paso 2 — Tabla comparativa ANTES del código (Paso 0 del prompt)

1. Identificá los requerimientos (sección 4), reglas de negocio (7), criterios de aceptación (8) y casos borde (9) que aplican a **esta capa** (MODO CAPA) o a **todas las capas del plan** (MODO FEATURE).
2. Generá la tabla `Requerimiento en spec | Implementación | Cubierto/Parcial/No aplica`. En MODO FEATURE agregá las columnas `Capa` y `Test que lo cubre`, más migraciones previstas y archivos existentes que se tocan. En una **modificación**, agregá la columna `Estado en el cambio` (Nuevo / Modificado / Sin cambios — no regenerar) cruzando cada fila contra el CHANGE-SET. Las filas "Sin cambios" no se tocan.
3. **Esperá mi confirmación explícita** ("tabla ok" / "plan ok") antes de escribir una sola línea de código. En MODO FEATURE esa única confirmación cubre todas las capas.

## Paso 3 — Generá (tras mi confirmación)

- Código + tests de la capa, organizados por archivo según `CONVENTIONS.md`.
- **No sobre-ingenierar:** nada de atributos, validaciones, relaciones, endpoints o abstracciones que no estén en la spec o exigidos por convenciones/principios.
- Seguridad transversal (`PRINCIPLES.md`) aplicada en esta capa, no delegada a "la siguiente".
- Migraciones **append-only** en Capa 1 (nunca editar una migración ejecutada).
- Tras el código, listá **DECISIONES TÉCNICAS TOMADAS POR DEFECTO** (solo técnicas-operativas; nunca de producto). Si no hubo, escribilo literal.

## Paso 4 — Manejo de gaps

Si la spec dice X pero el setup dice algo incompatible, un requerimiento es ambiguo con consecuencias reales, o el código previo es inconsistente con lo que pide esta capa: **PARÁ, no implementes con tu criterio**, citá el conflicto y esperá mi decisión. Un gap ignorado en Capa 1 se propaga a Capa 4.

## Paso 5 — Antes de cerrar la capa

**MODO CAPA:** no tildes la capa hasta revisar las decisiones por defecto, ejecutar la **verificación adversaria** de la capa y procesar sus hallazgos, y que los tests pasen. Después seguí con la capa siguiente.

**MODO FEATURE:** con todas las capas en verde, ejecutá la verificación adversaria **una sola vez sobre el diff completo** (`/sdd-adversarial-code <ID>` sin capa). Bloqueantes → los corregís y re-corrés el gate automático; no bloqueantes → `DEBT.md`. Solo frenás si una corrección requiere decisión de producto.

En ambos modos, la revisión de código rutea por track (`${CLAUDE_PLUGIN_ROOT}/protocols/track-routing.md`: checks inline en Rápido de pura presentación, subagente acotado al diff en Rápido con lógica y modificaciones Estándar, diff completo en features nuevas Estándar y Completo).

## Paso 6 — Cierre de la feature: prueba manual ANTES del commit

El **commit es por feature completa y verificada**, no por capa suelta. Antes de commitear, con todas las capas cerradas y los tests automáticos en verde:

1. **Armá un plan de prueba manual** a partir de los criterios de aceptación (sección 8) y casos borde (sección 9) de la spec — en una modificación, acotado al delta. Pasos concretos, numerados, con datos/precondición y resultado esperado. **Acotado (WORKFLOW §7.5, v20):** los criterios ya cubiertos por tests automáticos se listan con su test y no se repiten a mano; a mano va lo que los tests no cubren (experiencia/visual, integraciones reales, flujos no automatizados) más al menos un recorrido del happy path en el entorno real.
2. **Esperá mi confirmación explícita** de que probé y funciona. Los tests automáticos validan que el código cumple la spec; la prueba manual valida que la experiencia real es la esperada. No son lo mismo.
3. **Mi OK es la autorización del commit:** commiteá directo con la convención de `/sdd-commit` (`feat(<ID>): …`), sin volver a preguntarme por el gate ni por el mensaje. `ok push` → también pusheás. Si algo falla en la prueba, no commitees: volvemos a iteración de código.

En el mismo mensaje del plan de prueba, listá las decisiones técnicas por defecto acumuladas: `ok` las valida todas.
