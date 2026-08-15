---
description: "Fase 4 SDD — Pasada adversaria de spec (rol Adversario). Corre en subagente con contexto limpio. Busca contradicciones, gaps y ambigüedades."
argument-hint: "[ID/ruta de la spec] [pasada: 1|2]"
---

Vas a ejecutar la **Fase 4 (Pasada adversaria de spec)** del ciclo SDD. El rol Adversario debe correr con **contexto limpio**, separado de quien redactó la spec (WORKFLOW sección 3). En Claude Code eso se logra con un **subagente dedicado**: vos NO hacés la pasada vos mismo en esta sesión.

## Paso 1 — Preparación

1. Identificá la spec objetivo y la pasada (1 o 2) desde: **$ARGUMENTS**. Máximo 2 pasadas (WORKFLOW 13.2). **Pasada 2 solo si la Pasada 1 tuvo bloqueantes** (contradicción real, gap operativo, violación al setup, decisión implícita sin marcar); si la 1 fue limpia o solo dejó descartables, avisame que corresponde ir directo a `/sdd-verify`.
2. **Gate de tier (solo modificaciones):** si la spec viene de `/sdd-modify-spec`, buscá el CHANGE-SET y leé su `Tier`. Si es **T1**, NO lances la pasada: avisame que T1 la omite (excepción codificada de Regla 4, WORKFLOW 8.3.2) y que el siguiente paso es `/sdd-verify` en modo express. Si es **T2**, la pasada corre en **modo acotado al delta** con contexto selectivo. Si es **T3** o no hay CHANGE-SET, pasada completa.
3. Antes de lanzar, leé **solo** la sub-sección **10.2** de la spec ("Decisiones derivadas de pasadas adversarias") y el header de versión — no cargues la spec completa en esta sesión. Localizá la §10.2 con una lectura acotada (offset/limit, o un grep de la sección), no leyendo el documento entero: la spec completa es trabajo del subagente, que corre con contexto limpio. Sirve para saber qué hallazgos ya se cerraron — esos no se re-marcan salvo nuevo criterio.

## Paso 2 — Lanzá el subagente adversario

Usá la tool **Agent** (subagent_type: `general-purpose`, `model: sonnet`) con un prompt que le ordene:

> **Modelo del subagente:** fijá `model: sonnet` en la llamada a `Agent`. La pasada adversaria es razonamiento estructurado (contradicciones, ambigüedades, decisiones no marcadas) donde Sonnet rinde bien a una fracción del costo/latencia de Opus. Esto NO cambia el modelo de tu sesión principal: solo el del subagente. Si al medir una pasada real ves que Sonnet se pierde hallazgos que Opus sí encuentra, subilo a `opus` acá.

1. Leer el prompt canónico `${CLAUDE_PLUGIN_ROOT}/prompts/03-adversarial-spec.prompt.md` y ejecutarlo al pie de la letra (rol Adversario, las 10 categorías de hallazgos en orden de prioridad).
2. Leer como contexto: la spec objetivo (`sdd/specs/<ID>.md`), el setup foundacional de `sdd/foundation/`, las specs dependientes de primer nivel declaradas en la sección 12 de la spec. La guía `${CLAUDE_PLUGIN_ROOT}/templates/feature-spec.guide.md` es **opcional**: cargala solo si hace falta el detalle de qué va en cada sección — la taxonomía de casos borde que se audita ya está embebida en el prompt canónico. **En modificaciones T2, carga selectiva (WORKFLOW 8.3.2):** el CHANGE-SET + siempre `CONVENTIONS.md` y `PRINCIPLES.md`; `DOMAIN_MODEL.md` solo si el delta toca Capa 1/2; `ARCHITECTURE.md` solo si toca Capa 2/3 o integraciones; `GLOSSARY.md` solo si hay términos nuevos. En T3/specs nuevas: todo.
3. **En modificaciones T2:** activar el MODO ACOTADO AL DELTA del prompt canónico — hallazgos solo sobre lo que el delta introduce o toca (con foco en propagación); problemas pre-existentes en una línea bajo "FUERA DE SCOPE".
4. Respetar las restricciones: no felicitar nada, no suavizar, no inventar hallazgos para llenar categorías, no re-marcar lo ya cerrado en 10.2.
5. Devolver solo las categorías con hallazgos + una línea final de cobertura (qué categorías quedaron sin hallazgos) + la pregunta crítica de cierre.

Indicale al subagente que su mensaje final es el reporte de hallazgos (no un resumen humano).

## Paso 3 — Procesá los hallazgos conmigo (esto sí lo hacés en esta sesión)

Cuando el subagente devuelva:

- **No los aceptes en caliente.** Presentámelos clasificados: sólidos para iterar (contradicciones reales, gaps operativos, violaciones al setup, decisiones implícitas no marcadas) / zona gris / descartables (estilo, casos teóricos, sobre-especificación). WORKFLOW 13.1.
- Para cada hallazgo aceptado, actualizá la spec y **documentá en la sub-sección 10.2** la resolución (aceptado/descartado/modificado) + justificación. Esto es lo que evita el re-marcado en la pasada 2.
- **Subí versión** de la spec (`YYYYMMDD-vN+1`) y agregá entrada al changelog.
- Estado: tras procesar Pasada 1, la spec pasa de **Draft → Review**.

Recordame la pregunta de corte (WORKFLOW 13.4): *"Si apruebo esta spec hoy y aparece un problema, ¿voy a poder decir que aprobé con criterio?"*. Siguiente paso: si la pasada tuvo **bloqueantes**, procesarlos y recién ahí evaluar Pasada 2; si fue limpia o solo dejó descartables, **no hay Pasada 2** (WORKFLOW 13.2) — directo a `/sdd-verify` antes de generar código.
