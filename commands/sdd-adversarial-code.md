---
description: "Fase 6 SDD — Pasada adversaria de código (rol Adversario). Corre en subagente con contexto limpio. Valida que el código cumple la spec."
argument-hint: "[ID/ruta spec] [capa: 1|2|3|4]"
---

Vas a ejecutar la **pasada adversaria de código** sobre una capa recién generada. Como en Fase 4, el adversario debe correr con **contexto limpio** y separado de quien generó el código (que tiene sesgo a defender lo que escribió). En Claude Code: **subagente dedicado**.

## Límite importante (leelo antes de lanzar)

Esta pasada valida que **el código cumple la spec**, NO que la spec es correcta. SÍ valida: cobertura de criterios de aceptación con tests, convenciones, principios/seguridad, consistencia con el modelo, casos de error de la spec, sobre-ingeniería. NO valida si el criterio de aceptación captura bien la necesidad real del negocio (riesgo de **validación circular**, WORKFLOW 2.6). Si tenés dudas sobre la spec en sí, esto no las resuelve.

## Paso 0 — Gate de tier (solo modificaciones, WORKFLOW 8.3.2)

Si la spec viene de `/sdd-modify-spec`, leé el `Tier` del CHANGE-SET y rutea según `${CLAUDE_PLUGIN_ROOT}/protocols/tier-routing.md` antes de lanzar nada:

- **T1:** NO lances el subagente. Esta pasada se reemplaza por **checks inline** que ejecutás vos en esta sesión: (a) tests de la capa pasan, (b) typecheck/build limpio, (c) revisión del diff contra `CONVENTIONS.md`. Reportá los tres resultados. El gate de prueba manual sigue siendo obligatorio antes del commit.
- **T2:** lanzá el subagente **acotado al diff**: recibe el diff de la capa (no todo el código), las secciones de la spec que el CHANGE-SET toca + el CHANGE-SET, CONVENTIONS+PRINCIPLES siempre, y DOMAIN_MODEL/ARCHITECTURE solo según las capas tocadas. Hallazgos solo sobre el código del delta y su interacción con el existente.
- **T3 o sin CHANGE-SET (build inicial):** pasada completa (Paso 1 tal cual).

Si cualquier hallazgo revela que el cambio excede su tier (toca modelo/reglas/seguridad), es **bloqueante**: el tier sube y se ejecutan los pasos salteados (válvula de escape).

## Paso 1 — Lanzá el subagente adversario

Identificá spec y capa desde **$ARGUMENTS**. Usá la tool **Agent** (subagent_type: `general-purpose`, `model: sonnet`) con un prompt que le ordene:

> **Modelo del subagente:** fijá `model: sonnet` en la llamada a `Agent` (aplica también al subagente acotado del Paso 0 T2). Esta pasada corre ×4 capas y es el costo dominante del ciclo; Sonnet la abarata y acelera sin resignar la revisión estructurada. NO cambia el modelo de tu sesión principal. Subilo a `opus` solo si medís que Sonnet se pierde hallazgos reales.

1. Leer el prompt canónico `${CLAUDE_PLUGIN_ROOT}/prompts/05-adversarial-code.prompt.md` y ejecutarlo (rol revisor adversario, las 8 categorías en orden de prioridad).
2. Leer como contexto **acotado a la capa bajo revisión**, según la matriz "Carga selectiva de foundation → Pasada adversaria de código" de `${CLAUDE_PLUGIN_ROOT}/protocols/tier-routing.md`: el código generado de esta capa, solo los docs de foundation que la capa toca, solo las secciones de spec relevantes a la capa (no la spec completa ni todo `sdd/foundation/`), y las specs dependientes de §12 relevantes. `PRODUCT.md` no se carga en esta pasada. Esto aplica también a builds iniciales — recargar todo el foundation en cada una de las 4 capas multiplica el costo sin agregar señal. En modificaciones T2, además acotado al diff (Paso 0).
3. Asumir la spec como contrato dado (no cuestionarla). Buscar desvíos, decisiones implícitas, violaciones de convenciones/principios, inconsistencias con el modelo, bugs lógicos, casos borde no cubiertos, sobre-ingeniería.
4. No felicitar, no suavizar, no inventar hallazgos. Reportar solo las categorías con hallazgos + una línea final de cobertura (qué categorías quedaron sin hallazgos). Cerrar con la pregunta: ¿qué riesgo operativo concreto introduce este código si se mergea tal cual?

El mensaje final del subagente es el reporte de hallazgos.

## Paso 2 — Procesá los hallazgos conmigo

- Clasificá en **bloqueantes** (vulnerabilidades, bugs lógicos severos, violaciones a PRINCIPLES, desvíos de spec → corrección inmediata) y **no bloqueantes** (cosmético, estilístico → ignorar o registrar como deuda). WORKFLOW 7.4.1.
- Para cada hallazgo válido decidí: iterar código (cambio quirúrgico, máx 2 intentos), modificar spec (si revela gap/ambigüedad → sube versión), modificar setup foundacional (si afecta a varias features), o descartar.
- Si un hallazgo bloqueante afecta una **capa previa** ya verificada: volvé a esa capa, corregí, re-verificá su checklist completo, y recién seguí.
- Si la pasada devuelve "todo bien": desconfiá (código trivial o adversario flojo). Si devuelve >20 hallazgos serios: la capa tiene problemas estructurales, considerá regenerar en vez de iterar.
