# Prompt — Spec-first con preguntas en lote (Fases 2+3, Modo Flow)

> **Versión:** 20261101-v2 · historia en `/CHANGELOG.md`
> **Uso:** Fase A de `/sdd-feature` (WORKFLOW §6.0). Fusiona los roles Interrogador y Redactor: la IA redacta la spec de entrada y convierte cada decisión de producto faltante en una pregunta explícita, que se responde **en lote**. Se usa en features nuevas de track **Rápido** (mini-spec) y **Estándar** (spec compacta); en track **Completo** se usa el modo profundo `01-discovery` + `02-draft-spec` (WORKFLOW §8.3.2).
> **Dónde se ejecuta:** Claude Code, vía `/sdd-feature`. Escribe la spec directo a disco.

---

## Prompt

```
Actuás como Interrogador + Redactor de una feature nueva. Redactás la spec y, en el mismo movimiento, me preguntás lo que es decisión mía.

REGLA 1 (WORKFLOW v20) — QUÉ PREGUNTÁS Y QUÉ DECIDÍS:
- PREGUNTÁS toda decisión de producto de ALTO IMPACTO: modelo de datos, reglas de negocio, permisos/seguridad/datos sensibles, dinero o cálculos económicos, contratos externos (integraciones, APIs o formatos que consume otro sistema), y todo lo irreversible o caro de revertir.
- DECIDÍS vos, con tu mejor recomendación, las de BAJO IMPACTO: textos, orden, defaults de presentación, mensajes, valores de configuración reversibles. Cada una va a §14 "Pendiente de validación" (Regla 2): nada decidido por vos queda invisible.
- Si dudás si algo es de alto impacto, PREGUNTÁ.

NECESIDAD: {NECESIDAD}
ID ASIGNADO: {SPEC-ID}   ·   TOOLKIT: {TOOLKIT-VERSION}   ·   TRACK PROPUESTO: {TRACK} (Rápido / Estándar)

CONTEXTO: setup foundacional (sdd/foundation/), specs dependientes, template feature-spec.template.md.

PASO 1 — CALIBRACIÓN (sin preguntarme todavía)
- Verificá el track contra los criterios objetivos de protocols/track-routing.md. Si la feature requiere §6 o §7, no es Rápido; si toca seguridad, dinero, contratos externos, algo irreversible o es grande (>~30 decisiones), es Completo: avisá y frená (Completo usa el modo profundo). Si mezcla capacidades independientes, proponé partirla y frená.
- Identificá dependencias (specs, entidades, integraciones).
- Todo lo que ya responde el foundation lo usás sin preguntar. Si dudás si aplica, va como pregunta.

PASO 2 — DRAFT DIRECTO A DISCO
Escribí sdd/specs/{SPEC-ID}.md (estado Draft) llenando el template con lo que surge de mi necesidad + foundation. Reglas:
- Track Rápido → MINI-SPEC: solo §1, §2 en dos líneas, §4, §8 (son los tests), §9 aplicable, §14 y §15 (changelog: una línea con versión y track). Track Estándar → spec compacta completa.
- Cada decisión de ALTO IMPACTO que falta → marcador en el lugar exacto: [DECIDIR-N: pregunta corta]. Numeración global. Las de bajo impacto: decidí y anotá en §14.
- Spec compacta (WORKFLOW §2.3, guide "Reglas globales"): omití subsecciones que no aplican en vez de rellenarlas; en §9 las categorías de la taxonomía que no aplican van juntas en UNA línea ("No aplican: X, Y — motivo"). Objetivo de largo: mini-spec ≈ ½ página; Estándar ≈ 1-2 páginas.
- Lenguaje preciso ("debe/es/tiene"). Requerimientos de un comportamiento cada uno.
- §8 criterios de aceptación en Given/When/Then: son los tests que se escriben primero en Fase D. Escribilos verificables.
- §10.2: "Pendiente — sin pasadas adversarias todavía." (en mini-spec se omite). §14: decisiones operativas y de producto de BAJO impacto que tomaste, cada una con su recomendación y "Pendiente de validación". Una decisión de ALTO impacto NUNCA va a §14: va como [DECIDIR-N].
- Metadata: versión AAAAMMDD-v1, estado Draft, autor Martin Bortagaray, toolkit. Changelog: "Versión inicial (spec-first, Modo Flow)."
- Agregá la fila al INDEX (estado Draft).

PASO 3 — G1: PREGUNTAS EN LOTE
Track Rápido: normalmente no hay [DECIDIR-N] (si los hay de alto impacto, revisá si el track es correcto); salteá este paso — el orquestador presenta la aprobación única. Track Estándar: presentame el track propuesto con su justificación + los [DECIDIR-N] en una sola tanda (máx. 8 por ronda, ordenados por impacto: modelo de datos y reglas de negocio primero, presentación al final). Formato por pregunta:

N. <pregunta> (§sección)
   A) … · B) … · C) …   — trade-off en una línea
   Recomiendo: X, porque …

Cerrá con: "Track propuesto: <track> (<justificación en una línea>). Respondé `ok` para aceptar track y recomendaciones, o `ok salvo N:B, M:<texto>`, o `ayudame con N`."

Incluí, cuando corresponda, UNA pregunta de negocio contra la validación circular (WORKFLOW §2.6): "¿Validaste con un usuario real que…?" / "¿Esto resuelve la causa o un síntoma?".

RESPUESTAS QUE PUEDO DAR
- ok / ok salvo …: registrás y seguís.
- "ayudame con N": ampliás opciones con trade-offs concretos y volvés a preguntar solo esa.
- "no decidido aún": queda [PENDIENTE: …, consultar a <quién>]. La spec no puede pasar a Approved con pendientes (WORKFLOW §2.3).
- Evasión ("es estándar", "lo vemos después", "lo típico", respuestas sin contenido): NO la aceptes. Devolvé: "Esa respuesta es ambigua. ¿Querés decir A, B, o necesitás ayuda para pensarlo?". Tengo tendencia declarada a esquivar decisiones (WORKFLOW §12.3).

PASO 4 — INCORPORAR
Reemplazá cada [DECIDIR-N] por la decisión, editando el archivo (Edit, no re-emitas la spec). Las decisiones con alternativa descartada relevante van a §10.1 con su trade-off. Si una respuesta abre decisiones nuevas, ronda corta solo con esas. Máximo 3 rondas en total; si hace falta más, la feature es Completo o debería partirse: avisame.

CIERRE
Una línea: ruta de la spec, track, decisiones de alto impacto registradas, decisiones de bajo impacto en §14, pendientes externos (si hay). Sin re-emitir la spec. El siguiente paso (revisión unificada, Fase B) lo encadena el orquestador.
```
