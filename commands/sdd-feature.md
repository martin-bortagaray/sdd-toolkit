---
description: "SDD Modo Flow — ciclo completo de punta a punta (orquestador). Clasifica el trabajo en un track (Rápido/Estándar/Completo) y encadena spec → revisión → plan → código → revisión de código → prueba → commit, frenando solo en los gates del track."
argument-hint: "[necesidad en 1-2 líneas | ID de spec existente + qué cambiar]"
---

Vas a ejecutar el **ciclo SDD completo en Modo Flow** (WORKFLOW §6.0). Sos el orquestador: encadenás las fases **sin esperar a que yo invoque cada comando** y frenás **solo** en los gates humanos de su track y en las interrupciones legítimas. Mi tiempo es el recurso escaso: cada vez que me hacés esperar o me pedís una confirmación que no decide nada, el proceso pierde.

Operás bajo las 5 reglas de WORKFLOW §2.2 (versión v20): preguntás solo decisiones de producto de **alto impacto** (Regla 1) y marcás en §14 todo lo que decidís vos (Regla 2); yo apruebo leyendo la superficie de decisión (Regla 3); la revisión adversaria de spec corre en Estándar y Completo (Regla 4); errores de spec aprobada → versión + changelog (Regla 5).

## Gates por track

| Gate | Qué me pedís | Rápido | Estándar | Completo |
|------|--------------|:------:|:--------:|:--------:|
| **G1 — Preguntas** | Decisiones de alto impacto en lote + confirmar el track. | **Aprobación única**: track + spec/delta + plan en un mensaje | ✔ | ✔ (discovery profundo) |
| **G2 — Aprobación de spec** | Leer la superficie de decisión (§4, §6, §7, §8, §10, §14) + validar §14 + `leí, apruebo`. | ⤷ | ✔ **+ plan (G3 fusionado)** | ✔ |
| **G3 — Plan** | Plan único para todas las capas: `plan ok`. | ⤷ | ⤷ | ✔ |
| **G4 — Prueba manual** | Probar lo que los tests no cubren y responder `ok` (o `ok push`). | ✔ | ✔ | ✔ |

**Interrupciones legítimas (fuera de los gates, frenás y preguntás):** decisión de producto de alto impacto no prevista (Regla 1), válvula de escape de track, conflicto spec vs foundation, tests en rojo tras 2 intentos de corrección, veredicto ROJO de la revisión. **Nada más te detiene.** No pidas "¿sigo?", "¿confirmás la tabla de la capa 2?" ni "¿hago el commit?": avanzás. Las decisiones de bajo impacto no interrumpen: las tomás con tu recomendación y van a §14.

Al pasar de una fase a otra, informá en **una línea** dónde estás (ej: `▶ Fase D — Capa 2/3: tests en verde, sigo con Capa 3`). No narres.

## Paso 0 — Ruteo y reanudación

Entrada: **$ARGUMENTS** (si está vacío, pedime la necesidad en 1-2 líneas).

1. **Estado persistido.** Lo que no vive en la spec ni en git (fase actual, track, plan confirmado, decisiones técnicas por defecto acumuladas, resultado de la revisión de código) se guarda en `sdd/specs/<ID>.flow.md`, actualizado en cada transición. Es efímero: se borra en el commit de G4 (la trazabilidad queda en la spec, su changelog y el commit).
2. **Reanudación.** Si el argumento es un ID de spec, o hay una spec en curso en `sdd/specs/`, leé `<ID>.flow.md` (si existe) + estado de la spec + rama, y **retomá desde ahí** sin rehacer lo hecho:
   - El **track** y la **fase** salen de `.flow.md`. En modificaciones la spec sigue en `Implemented`/`As-built` hasta la aprobación, así que la fase se lee **solo** de `.flow.md`.
   - Estándar/Completo: `Draft` con `[DECIDIR` → G1 · `Draft` sin `[DECIDIR` → Fase B · `Review` (= Fase B hecha) → G2.
   - Rápido: sin aprobación registrada → aprobación única.
   - Cualquier estado con `[PENDIENTE: …]` → frená: hay consultas externas abiertas (WORKFLOW §2.3); listámelas.
   - `Approved` sin plan en `.flow.md` → Completo: Fase C · Rápido/Estándar: re-presentá solo el plan para confirmarlo (el resto ya se aprobó). Con plan y rama `feature/<ID>` → Fase D desde la primera capa sin gate verde · revisión de código registrada → G4.
3. **¿Qué es?** (árbol de WORKFLOW §8.1/§9): el sistema no hace lo que la spec dice → **bug**: frená y derivá a `/sdd-bugfix`. Cambia funcionalidad de una spec existente → **modificación** (`prompts/07-modify-spec.prompt.md`). Capacidad nueva independiente → **feature nueva**.
4. **Track** (`${CLAUDE_PLUGIN_ROOT}/protocols/track-routing.md`): proponé Rápido / Estándar / Completo con justificación contra los criterios objetivos (regla de duda hacia arriba; "es chico" no es justificación). La propuesta va **dentro del primer gate** (G1, o la aprobación única en Rápido), no en un gate propio. **Excepción — Completo:** como el discovery profundo es interactivo desde el inicio, abrilo con una línea "Track propuesto: Completo — <motivo>" y confirmá el track con mi primera respuesta. **Si cambio el track en el primer gate:** hacia arriba, completá lo que el track nuevo exige (válvula de escape); hacia abajo, rehacé solo lo que cambia de forma (ej: Estándar → Rápido: recortá a mini-spec) — nunca descartes decisiones ya tomadas.

## Fase A — Spec

Contexto: `sdd/foundation/` (carga selectiva en modificaciones, según `track-routing.md`) + specs dependientes. **No** cargues `feature-spec.guide.md` entera: consultala puntualmente (grep de la sección) solo si dudás qué va en una sección.

**Feature nueva:** asigná el ID desde `sdd/specs/INDEX.md` y escribí directo a disco (`sdd/specs/<ID>.md`, estado Draft, fila en INDEX) con `${CLAUDE_PLUGIN_ROOT}/prompts/08-spec-first.prompt.md`. Rápido → **mini-spec** (§1, §2 en dos líneas, §4, §8 (son los tests), §9 aplicable, §14 y §15 (changelog: una línea con versión y track)). Estándar → spec compacta completa. Completo → discovery sección por sección (`prompts/01-discovery.prompt.md`) y redacción con `02-draft-spec.prompt.md`.

**Modificación:** `07-modify-spec.prompt.md` con su discovery inline del delta. Rápido → delta + 1 línea de changelog (CHANGE-SET mínimo: ítems + capa, sin prosa). Estándar/Completo → cirugía + versión + changelog + CHANGE-SET con el track en el header.

**Preguntas (Regla 1 v20):** solo las de **alto impacto** — modelo de datos, reglas de negocio, permisos/seguridad/datos sensibles, dinero, contratos externos, lo irreversible — quedan como `[DECIDIR-N: …]` en la spec. Lo de bajo impacto lo decidís con tu recomendación y va a §14 "Pendiente de validación". Si dudás si es alto impacto, preguntá.

- **G1 en Completo:** son las rondas del discovery profundo (sección por sección, sin tope de lote); al cerrarlo, se redacta con `02` y se sigue en Fase B.
- **G1 en Estándar:** presentame el track propuesto + las `[DECIDIR-N]` **en lote** (máx. 8 por ronda y máx. 3 rondas, ordenadas por impacto), cada una con 2-4 opciones, trade-off en una línea y **tu recomendación**. En modificación, también la lectura crítica de la spec existente (3-5 líneas). Yo respondo `ok` (acepto track y recomendaciones), `ok salvo 3:B, 5:<texto>`, o `ayudame con N`. Detección de evasión vigente.
- Incorporá las respuestas editando el archivo (Edit, no re-emitas la spec). Si abren decisiones nuevas, ronda corta solo con esas.
- **Rápido:** salteá G1 y andá a la **aprobación única** (abajo, después de la Fase B). Si aparece una decisión de **alto impacto** en un Rápido, el track está mal: subilo a Estándar (válvula de escape) y seguí por G1.

## Fase B — Revisión de spec

- **Estándar y Completo — revisión unificada.** Lanzá **un** subagente con la tool **Agent** (`subagent_type: general-purpose`, `model: sonnet`) que ejecute en la misma pasada: (1) `${CLAUDE_PLUGIN_ROOT}/prompts/03-adversarial-spec.prompt.md` (las 10 categorías; en modificación Estándar, modo acotado al delta) y (2) el checklist de `${CLAUDE_PLUGIN_ROOT}/prompts/06-spec-verification.prompt.md` en su modo (COMPLETO en feature nueva y en Completo; DELTA en modificación Estándar), **omitiendo F1 y F3** (los cierra G2). Contexto: la spec, el foundation (selectivo en modificaciones), dependencias de §12. Indicale que **omita observaciones de estilo o preferencia** (WORKFLOW §13.1). Devuelve **un solo reporte**: hallazgos + semáforo pre-codegen.
- **Rápido — sin revisión adversaria** (Regla 4 v20). Corré vos inline los checks formales del modo **EXPRESS** del prompt 06 (F2, F5/F6 acotados, C3/C4/C5; en modificación, D1–D3 — F1/F3 los cierra la aprobación) y confirmá que la mini-spec/delta no requiere §6 ni §7 (si los requiere, el track sube: válvula de escape).

**Procesá los hallazgos vos mismo, sin esperarme** (WORKFLOW §13.1):
- **Sólidos sin decisión de producto** (tipo faltante, CA que falta para un RF declarado, caso borde aplicable con resolución que se deriva de la spec): aplicalos y registralos en §10.2. **Si el arreglo agrega o define comportamiento**, además va a §14 "Pendiente de validación" (Regla 2).
- **Sólidos que requieren decisión de alto impacto:** al lote de G2 como `[DECIDIR-N]` con opciones y recomendación. Si son de bajo impacto, decidilos y van a §14.
- **Descartables** (estilo, casos teóricos, sobre-especificación): a §10.2 como descartados con una línea de motivo; en G2 los ves como lista y puedo reabrir cualquiera por número. **Zona gris:** al lote de G2 como pregunta.
- Subí versión, changelog, estado → **Review** (Estándar/Completo; en Rápido no hay estado Review: de Draft — o de Implemented, en modificación — pasa directo a Approved en la aprobación única).
- **Pasada 2 automática** solo si la Pasada 1 tuvo bloqueantes (WORKFLOW §13.2), antes de G2. Nunca más de 2.

## G2 — Aprobación de spec (y gates fusionados)

Presentame una **ficha de aprobación** compacta (no re-emitas la spec; está en disco):

- Ruta de la spec + versión + track. **Indicá qué secciones forman la superficie de decisión** que tengo que leer (§4, §6, §7, §8, §10, §14 — en modificación, el delta de esas).
- Cambios que introdujo la revisión (aplicados / descartados, una línea cada uno).
- `[DECIDIR-N]` surgidas de la revisión, si las hay (en lote, con recomendación).
- §14 — decisiones por defecto a validar, en lote (`ok` las valida todas; puedo rechazar por número). Marcá con ⚠ las que estuvieron cerca del umbral de alto impacto.
- Semáforo pre-codegen. Los AMARILLO van con tu recomendación (resolver / aceptar y registrar en §10.1).
- **Estándar:** agregá el plan de la Fase C (G2 y G3 fusionados), con el formato de tabla del Paso 0 del prompt 04 (en modificación, con "Estado en el cambio" y chequeo de propagación).
- **Rápido — aprobación única:** en este mismo mensaje van el track propuesto con su justificación, el enfoque, la mini-spec o el delta (ruta), el plan corto (tabla reducida del Paso 0 del prompt 04: ítem → capa → archivos → test; en modificación, con "Estado en el cambio" y chequeo de propagación) y, en modificación, el **CHANGE-SET mínimo** que va a acotar el codegen. Es el único gate antes de G4.

Recordame en una línea la pregunta de corte (§13.4) y que las 3 decisiones clave, el trade-off y la parte más débil las nombro yo.

- **Si respondo decisiones o rechazos que cambian la spec:** incorporalos, subí versión y mostrame **solo el diff**; la aprobación vale sobre ese texto final. Si había plan fusionado, regeneralo y mostrámelo con el diff.
- **Aprobación:** tiene que decir explícitamente que leí (ej: `leí, apruebo`; un `ok` suelto no aprueba — Regla 3). Con eso: estado **Approved**, fecha + versión, INDEX actualizado, §14 marcada validada, track y plan (si vino fusionado) registrados en `.flow.md`. **Sin esa aprobación no hay código.**

## Fase C — Plan único (G3, solo Completo)

Ejecutá el **Paso 0 de `${CLAUDE_PLUGIN_ROOT}/prompts/04-codegen-layer.prompt.md` en MODO FEATURE**: una tabla para todas las capas involucradas (requerimiento/CA → capa → archivos → test que lo cubre), más migraciones previstas y archivos existentes que se tocan. En modificaciones, con la columna "Estado en el cambio" y el chequeo de propagación del CHANGE-SET. Una confirmación mía (`plan ok`) cubre todas las capas. En Rápido y Estándar este plan ya vino en el gate de aprobación.

## Fase D — Implementación autónoma

Con el plan confirmado, creá la rama `feature/<ID>` si no existe (WORKFLOW §11.6) y generá **capa por capa (1→2→3→4, solo las del plan) sin pedirme confirmación entre capas**, siguiendo las reglas del prompt 04:

1. **Tests primero:** tests de los criterios de aceptación (§8) y casos borde (§9) que tocan la capa; deben fallar.
2. Implementá la capa (Write/Edit directo a disco; no vuelques código en el chat).
3. **Gate automático entre capas:** tests de la capa + suite previa + typecheck/lint/build del proyecto en verde. Si falla, corregí (máx. 2 intentos, cambios quirúrgicos); al tercero, **frená** — probablemente el problema es la spec (WORKFLOW §8.2). Registrá en `.flow.md` cada capa en verde.
4. Acumulá las **DECISIONES TÉCNICAS TOMADAS POR DEFECTO** de todas las capas en una sola lista (se validan en G4).
5. Decisión de alto impacto no prevista, conflicto con foundation o válvula de escape → **interrupción**. **Si la resolución cambia la spec** (Regla 5 / WORKFLOW §8.3.1): editá la spec, subí versión + changelog; si el cambio es estructural o sube el track, vuelve a **Review** y repasa los gates salteados antes de seguir; regenerá las filas afectadas del plan y evaluá si las capas ya generadas quedan afectadas (si lo están, se rehacen). Nunca sigas generando contra una spec que ya no es la vigente.

## Fase E — Revisión de código (una pasada por feature)

Con todas las capas en verde, según el track (`track-routing.md`):

- **Completo:** pasada de `${CLAUDE_PLUGIN_ROOT}/prompts/05-adversarial-code.prompt.md` sobre el **diff completo** (`model: sonnet`), contexto = unión de la matriz por capa para las capas tocadas, sin observaciones de estilo. Backend **y** UI con diff grande (>~800 líneas) → **dos subagentes en paralelo en el mismo mensaje** (capas 1-3 / capa 4).
- **Estándar:** mismo subagente sobre el diff de la feature (en modificación, acotado al diff del cambio).
- **Rápido:** subagente acotado al diff (contexto: la mini-spec o el delta + el diff); si el cambio es **de pura presentación**, checks inline (tests + typecheck + diff vs `CONVENTIONS.md`) sin subagente. "Pura presentación" = el diff no cambia condicionales, queries, validaciones ni datos que se persisten o envían: solo layout, textos, estilos, orden visual o formato de salida.
- **Procesá sin esperarme:** bloqueantes (desvío de spec, seguridad, PRINCIPLES, bug lógico) → corregilos y re-corré el gate automático; si corregir requiere decisión de alto impacto → interrupción. Un hallazgo que muestra que el trabajo excede su track → válvula de escape. No bloqueantes → `sdd/DEBT.md` (formato de `/sdd-defer`, tipo `deuda-tecnica`) y listalos en G4.

## G4 — Prueba manual → commit

Presentame, en un solo mensaje:

1. Resumen: capas generadas, archivos tocados (conteo), tests (n en verde).
2. Decisiones técnicas por defecto acumuladas (`ok` las valida todas; puedo rechazar por número).
3. Hallazgos corregidos de la Fase E (una línea c/u) y los no bloqueantes enviados a `DEBT.md`.
4. **Plan de prueba manual acotado** (WORKFLOW §7.5): (a) criterios de §8/§9 ya cubiertos por tests automáticos — listados con su test, **no se repiten a mano**; (b) lo que pruebo a mano: experiencia/visual, integraciones reales, flujos no automatizados, más al menos un recorrido del happy path en el entorno real. Pasos numerados, precondición/datos, resultado esperado, cómo levantar el entorno. En modificación, acotado al delta.

Si rechazo una decisión técnica por número: reemplazala, re-corré el gate automático y volvé a presentarme solo lo que cambió. **Mi respuesta `ok` es la autorización del commit** — no me vuelvas a preguntar por el gate ni por el mensaje: commiteá directo con la convención de `/sdd-commit` (`feat(<ID>): …` + referencia a versión de spec). `ok push` → además pusheás la rama. Si reporto una falla, no commitees: volvé a Fase D (o abrí bug si corresponde).

Al commitear, borrá `sdd/specs/<ID>.flow.md`. Cierre en 2-3 líneas: commit creado, rama, siguiente paso (merge a staging y, tras el merge a `main`, spec → **Implemented** en spec e INDEX — WORKFLOW §11.6; si me lo pedís en ese momento, lo hacés vos).
