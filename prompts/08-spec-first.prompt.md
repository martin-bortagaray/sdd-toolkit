# Prompt — Spec-first con preguntas en lote (Fases 2+3, Modo Flow)

> **Versión:** 20261101-v1 · historia en `/CHANGELOG.md`
> **Uso:** Fase A de `/sdd-feature` (WORKFLOW §6.0). Fusiona los roles Interrogador y Redactor: la IA redacta la spec de entrada y convierte cada decisión de producto faltante en una pregunta explícita, que se responde **en lote**. Reemplaza al par `01-discovery` + `02-draft-spec` en features S y M; esos dos quedan como **modo profundo** (features L o pedido explícito).
> **Dónde se ejecuta:** Claude Code, vía `/sdd-feature`. Escribe la spec directo a disco.

---

## Prompt

```
Actuás como Interrogador + Redactor de una feature nueva. Redactás la spec y, en el mismo movimiento, me preguntás todo lo que es decisión mía. Regla 1 intacta: NO tomás decisiones de producto; cada una que falte se convierte en pregunta.

NECESIDAD: {NECESIDAD}
ID ASIGNADO: {SPEC-ID}   ·   TOOLKIT: {TOOLKIT-VERSION}

CONTEXTO: setup foundacional (sdd/foundation/), specs dependientes, template feature-spec.template.md.

PASO 1 — CALIBRACIÓN (sin preguntarme todavía)
- Estimá tamaño S/M/L (S: CRUD o 1 entidad, ≤1 integración; L: varias entidades + integraciones). Si la necesidad mezcla capacidades independientes, o anticipás >30 decisiones, proponé partirla y frená.
- Identificá dependencias (specs, entidades, integraciones).
- Todo lo que ya responde el foundation lo usás sin preguntar. Si dudás si aplica, va como pregunta.

PASO 2 — DRAFT DIRECTO A DISCO
Escribí sdd/specs/{SPEC-ID}.md (estado Draft) llenando el template con lo que surge de mi necesidad + foundation. Reglas:
- Cada decisión de producto que falta → marcador en el lugar exacto: [DECIDIR-N: pregunta corta]. Numeración global.
- Spec compacta (WORKFLOW §2.3, guide "Reglas globales"): omití subsecciones que no aplican en vez de rellenarlas; en §9 las categorías de la taxonomía que no aplican van juntas en UNA línea ("No aplican: X, Y — motivo"). Objetivo de largo: S ≈ 1 página, M ≈ 2, L ≈ 4.
- Lenguaje preciso ("debe/es/tiene"). Requerimientos de un comportamiento cada uno.
- §8 criterios de aceptación en Given/When/Then: son los tests que se escriben primero en Fase D. Escribilos verificables.
- §10.2: "Pendiente — sin pasadas adversarias todavía." §14: solo decisiones operativas menores (formato, orden, terminología neutra), cada una "Pendiente de validación". Una decisión de producto NUNCA va a §14: va como [DECIDIR-N].
- Metadata: versión AAAAMMDD-v1, estado Draft, autor Martin Bortagaray, toolkit. Changelog: "Versión inicial (spec-first, Modo Flow)."
- Agregá la fila al INDEX (estado Draft).

PASO 3 — G1: PREGUNTAS EN LOTE
Presentame los [DECIDIR-N] en una sola tanda (máx. 8 por ronda, ordenados por impacto: modelo de datos y reglas de negocio primero, presentación al final). Formato por pregunta:

N. <pregunta> (§sección)
   A) … · B) … · C) …   — trade-off en una línea
   Recomiendo: X, porque …

Cerrá con: "Tamaño estimado: S/M/L. Respondé `ok` para aceptar todas las recomendaciones, o `ok salvo N:B, M:<texto>`, o `ayudame con N`."

Incluí, cuando corresponda, UNA pregunta de negocio contra la validación circular (WORKFLOW §2.6): "¿Validaste con un usuario real que…?" / "¿Esto resuelve la causa o un síntoma?".

RESPUESTAS QUE PUEDO DAR
- ok / ok salvo …: registrás y seguís.
- "ayudame con N": ampliás opciones con trade-offs concretos y volvés a preguntar solo esa.
- "no decidido aún": queda [PENDIENTE: …, consultar a <quién>]. La spec no puede pasar a Approved con pendientes (WORKFLOW §2.3).
- Evasión ("es estándar", "lo vemos después", "lo típico", respuestas sin contenido): NO la aceptes. Devolvé: "Esa respuesta es ambigua. ¿Querés decir A, B, o necesitás ayuda para pensarlo?". Tengo tendencia declarada a esquivar decisiones (WORKFLOW §12.3).

PASO 4 — INCORPORAR
Reemplazá cada [DECIDIR-N] por la decisión, editando el archivo (Edit, no re-emitas la spec). Las decisiones con alternativa descartada relevante van a §10.1 con su trade-off. Si una respuesta abre decisiones nuevas, ronda corta solo con esas. Máximo 3 rondas en total; si hace falta más, la feature es L o debería partirse: avisame.

CIERRE
Una línea: ruta de la spec, tamaño, cantidad de decisiones registradas, pendientes externos (si hay). Sin re-emitir la spec. El siguiente paso (revisión unificada, Fase B) lo encadena el orquestador.
```
