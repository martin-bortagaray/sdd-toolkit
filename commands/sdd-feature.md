---
description: "SDD Modo Flow — ciclo completo de punta a punta (orquestador). Encadena spec → revisión → plan → código → revisión de código → prueba → commit y frena solo en los gates humanos."
argument-hint: "[necesidad en 1-2 líneas | ID de spec existente + qué cambiar]"
---

Vas a ejecutar el **ciclo SDD completo en Modo Flow** (WORKFLOW §6.0). Sos el orquestador: encadenás las fases **sin esperar a que yo invoque cada comando** y frenás **solo** en los gates humanos y en las interrupciones legítimas. Mi tiempo es el recurso escaso: cada vez que me hacés esperar o me pedís una confirmación que no decide nada, el proceso pierde.

Las **5 reglas no negociables siguen intactas** (ver `CLAUDE.md` del proyecto / WORKFLOW §2.2). Modo Flow no relaja ninguna: cambia *cuándo* y *cuántas veces* te detenés, no *qué* se garantiza.

## Gates humanos (los únicos puntos donde esperás)

| Gate | Qué me pedís | Qué decide |
|------|--------------|-----------|
| **G1 — Preguntas** | Las decisiones de producto abiertas, **en lote** (Regla 1). | El contenido de la spec. |
| **G2 — Aprobación de spec** | Leer la spec (Regla 3) + validar §14 + aprobar. | Spec → Approved. |
| **G3 — Plan** | Confirmar el plan único de implementación (todas las capas). En features **S** se fusiona con G2. | Alcance del código. |
| **G4 — Prueba manual** | Probar a mano y responder `ok` (o `ok push`). | Commit (y push). |

**Interrupciones legítimas (fuera de los gates, frenás y preguntás):** gap que requiere decisión de producto (Regla 1), válvula de escape de tier, conflicto spec vs foundation, tests en rojo tras 2 intentos de corrección, veredicto ROJO de la revisión. **Nada más te detiene.** No pidas "¿sigo?", "¿confirmás la tabla de la capa 2?" ni "¿hago el commit?": avanzás.

Al pasar de una fase a otra, informá en **una línea** dónde estás (ej: `▶ Fase D — Capa 2/3: tests en verde, sigo con Capa 3`). No narres.

## Paso 0 — Ruteo y reanudación

Entrada: **$ARGUMENTS** (si está vacío, pedime la necesidad en 1-2 líneas).

1. **Estado persistido.** Lo que no vive en la spec ni en git (fase actual, tier, plan confirmado de G3, decisiones técnicas por defecto acumuladas, resultado de la revisión de código) se guarda en `sdd/specs/<ID>.flow.md`, actualizado en cada transición. Es efímero: se borra en el commit de G4 (la trazabilidad queda en la spec, su changelog y el commit).
2. **Reanudación.** Si el argumento es un ID de spec, o hay una spec en curso en `sdd/specs/`, leé `<ID>.flow.md` (si existe) + estado de la spec + rama, y **retomá desde ahí** sin rehacer lo hecho:
   - `Draft` con `[DECIDIR` → G1 · `Draft` sin `[DECIDIR` → Fase B.
   - `Review` (= Fase B hecha) con `[DECIDIR` o §14 sin validar → G2 · `Review` limpia → G2.
   - Cualquier estado con `[PENDIENTE: …]` → frená: hay consultas externas abiertas (WORKFLOW §2.3); listámelas.
   - `Approved` sin plan confirmado en `.flow.md` → Fase C · con plan y rama `feature/<ID>` → Fase D desde la primera capa sin gate verde · revisión de código registrada → G4.
3. **Clasificá el cambio** (árbol de WORKFLOW §8.1/§9):
   - El sistema no hace lo que la spec dice → es **bug**: frená y derivá a `/sdd-bugfix`.
   - Cambia funcionalidad de una spec existente → **modificación**: clasificá el tier con `${CLAUDE_PLUGIN_ROOT}/protocols/tier-routing.md` (regla de duda hacia arriba). La **propuesta de tier es parte de G1** (va en el mismo mensaje que la lectura crítica de la spec y las preguntas del delta; Modo B: la confirmo ahí). **T1 que cumple el test de entrada** → carril rápido: un único mensaje con tier + enfoque + delta en una línea + plan corto (archivos a tocar); mi aprobación vale por G1+G2+G3. Después: línea de changelog en la spec (+ nota de sección si llena un hueco), Fase D, checks inline, G4. T2/T3 → Fase A en modo modificación (cirugía con `prompts/07-modify-spec.prompt.md`, CHANGE-SET incluido).
   - Capacidad nueva independiente → **feature nueva**.
4. **Tamaño** (features nuevas): S (CRUD/1 entidad, ≤1 integración) · M · L (varias entidades + integraciones, o >30 decisiones → proponé partirla, Regla del discovery). El tamaño lo proponés vos y lo confirmo en G1 junto con las preguntas — no gastes un gate solo en eso.

## Fase A — Spec-first (Interrogador + Redactor en una pasada)

Ejecutá `${CLAUDE_PLUGIN_ROOT}/prompts/08-spec-first.prompt.md` (en modificaciones: `07-modify-spec.prompt.md`, con sus verificaciones V1–V3 y el CHANGE-SET).

- Contexto: `sdd/foundation/` completo + specs dependientes que identifiques. **No** cargues `feature-spec.guide.md` entera: la consultás puntualmente (grep de la sección) solo si dudás qué va en una sección.
- Asigná el ID desde `sdd/specs/INDEX.md` y escribí el draft **directo a disco** (`sdd/specs/<ID>.md`, estado Draft, fila en INDEX). Toda decisión de producto que no esté en mi input ni en el foundation queda como `[DECIDIR-N: …]` en la spec.
- **G1:** presentame las `[DECIDIR-N]` **en lote** (máx. 8 por ronda y máx. 3 rondas, ordenadas por impacto), cada una con 2-4 opciones, trade-off en una línea y **tu recomendación**. Yo respondo `ok` (acepto todas las recomendadas), `ok salvo 3:B, 5:<texto>`, o `ayudame con N`. La detección de evasión del prompt sigue vigente.
- Incorporá las respuestas editando el archivo (Edit, no re-emitas la spec). Si una respuesta abre decisiones nuevas, ronda corta de G1 solo con esas.
- **S/M: lote** (lo de arriba). **L o pedido explícito de "modo profundo":** discovery sección por sección de `prompts/01-discovery.prompt.md` en vez del lote, y después la redacción de `02-draft-spec.prompt.md`; desde ahí el flujo sigue en Fase B.

## Fase B — Revisión unificada (adversaria + verificación en un solo subagente)

Lanzá **un** subagente con la tool **Agent** (`subagent_type: general-purpose`, `model: sonnet`) que ejecute en la misma pasada:

1. `${CLAUDE_PLUGIN_ROOT}/prompts/03-adversarial-spec.prompt.md` (las 10 categorías; en modificación T2, modo acotado al delta).
2. El checklist de `${CLAUDE_PLUGIN_ROOT}/prompts/06-spec-verification.prompt.md` en el modo que corresponda (COMPLETO / DELTA / EXPRESS), **omitiendo F1 y F3** (estado Approved y §14 validada los cierra G2, no el subagente).

Contexto del subagente: la spec, el foundation (carga selectiva en modificaciones según `tier-routing.md`), dependencias de §12. Indicale que **omita observaciones de estilo o preferencia** (un revisor al que se le pide encontrar problemas siempre encuentra algo; WORKFLOW §13.1). El subagente devuelve **un solo reporte**: hallazgos por categoría + semáforo pre-codegen. En modificaciones **T1** no hay subagente (excepción de Regla 4): corré vos D1–D3 + C3/C4/C5 del modo EXPRESS inline.

**Procesá los hallazgos vos mismo, sin esperarme**, con el criterio de WORKFLOW §13.1:
- **Sólidos sin decisión de producto** (tipo faltante, CA que falta para un RF declarado, caso borde aplicable no cubierto con resolución que se deriva de la spec): aplicalos a la spec y registralos en §10.2. **Si el arreglo agrega o define comportamiento** (no es solo corregir una contradicción o un error de forma), además va a §14 como "Pendiente de validación" (Regla 2): lo valido en G2.
- **Sólidos que requieren decisión de producto:** van al lote de G2 como `[DECIDIR-N]` con opciones y recomendación.
- **Descartables** (estilo, casos teóricos, sobre-especificación — §13.1): registralos en §10.2 como descartados con una línea de motivo; en G2 los ves como lista de una línea cada uno y puedo reabrir cualquiera por número. **Zona gris:** van al lote de G2 como pregunta, no se descartan solos.
- Subí versión, changelog, estado → **Review**.
- **Pasada 2 automática** solo si la Pasada 1 tuvo bloqueantes (WORKFLOW §13.2): lanzala vos antes de G2, para que yo vea el estado final una sola vez. Nunca más de 2.

## G2 — Aprobación de spec (Fase 5)

Presentame una **ficha de aprobación** compacta (no re-emitas la spec; está en disco):

- Ruta de la spec + versión + tamaño.
- Cambios que introdujo la revisión (resumen de §10.2: aplicados / descartados, una línea cada uno).
- `[DECIDIR-N]` surgidas de la revisión, si las hay (en lote, con recomendación).
- §14 — decisiones por defecto de la IA a validar (en lote: `ok` las valida todas).
- Semáforo pre-codegen. Los AMARILLO van con tu recomendación (resolver / aceptar y registrar en §10.1).
- **Features S:** agregá acá el plan de la Fase C (G2 y G3 se fusionan).

Recordame la pregunta de corte (§13.4) y las señales de aprobación con criterio de Fase 5 (las 3 decisiones clave, el trade-off y la parte más débil las nombro yo, no la ficha) en una línea.

- **Si respondo decisiones o rechazos que cambian la spec:** incorporalos, subí versión y mostrame **solo el diff** de lo que cambió; la aprobación vale sobre ese texto final.
- **Aprobación:** tiene que decir explícitamente que leí la spec entera (ej: `leí, apruebo`; un `ok` suelto no aprueba — Regla 3). Con eso: estado **Approved**, fecha + versión, INDEX actualizado, §14 marcada validada. **Sin esa aprobación no hay Fase C.**
- **Features S con plan fusionado:** si G2 cambió la spec, regenerá el plan antes de la Fase D y mostrámelo con el diff.

## Fase C — Plan único (G3)

Ejecutá el **Paso 0 de `${CLAUDE_PLUGIN_ROOT}/prompts/04-codegen-layer.prompt.md` en MODO FEATURE**: una sola tabla para todas las capas involucradas (requerimiento/CA → capa → archivos → test que lo cubre), más migraciones previstas y archivos existentes que se tocan. En modificaciones, con la columna "Estado en el cambio" y el chequeo de propagación del CHANGE-SET. Una confirmación mía (`plan ok`) cubre todas las capas.

## Fase D — Implementación autónoma

Con el plan confirmado, creá la rama `feature/<ID>` si no existe (WORKFLOW §11.6) y generá **capa por capa (1→2→3→4, solo las del plan) sin pedirme confirmación entre capas**, siguiendo las reglas del prompt 04:

1. **Tests primero:** escribí los tests de los criterios de aceptación (§8) y casos borde (§9) que tocan la capa; deben fallar.
2. Implementá la capa (Write/Edit directo a disco; no vuelques código en el chat).
3. **Gate automático entre capas:** tests de la capa + suite previa + typecheck/lint/build del proyecto en verde. Si falla, corregí (máx. 2 intentos, cambios quirúrgicos); al tercero, **frená** — probablemente el problema es la spec (WORKFLOW §8.2). Registrá en `.flow.md` cada capa en verde.
4. Acumulá las **DECISIONES TÉCNICAS TOMADAS POR DEFECTO** de todas las capas en una sola lista (se validan en G4).
5. Gap de producto, conflicto con foundation o válvula de escape → **interrupción** (frená y preguntá). **Si la resolución cambia la spec** (Regla 5 / WORKFLOW §8.3.1): editá la spec, subí versión + changelog; si el cambio es estructural, vuelve a **Review** y repasa G2 antes de seguir; regenerá las filas afectadas del plan y evaluá si las capas ya generadas quedan afectadas (si lo están, se rehacen). Nunca sigas generando contra una spec que ya no es la vigente.

## Fase E — Revisión de código (una pasada por feature, no por capa)

Con todas las capas en verde:

- **Build inicial / T3:** lanzá la pasada de `${CLAUDE_PLUGIN_ROOT}/prompts/05-adversarial-code.prompt.md` sobre el **diff completo de la feature** (`model: sonnet`). Contexto = unión de la matriz por capa de `tier-routing.md` para las capas tocadas; sin observaciones de estilo. Si la feature toca backend **y** UI con diff grande (>~800 líneas), lanzá **dos subagentes en paralelo en el mismo mensaje** (capas 1-3 / capa 4).
- **T2:** subagente acotado al diff. **T1:** checks inline (tests + typecheck + diff vs `CONVENTIONS.md`), sin subagente.
- **Procesá sin esperarme:** bloqueantes (desvío de spec, seguridad, PRINCIPLES, bug lógico) → corregilos y re-corré el gate automático; si corregir requiere decisión de producto → interrupción. No bloqueantes → registralos en `sdd/DEBT.md` (formato de `/sdd-defer`, tipo `deuda-tecnica`) y listalos en G4.

## G4 — Prueba manual → commit

Presentame, en un solo mensaje:

1. Resumen: capas generadas, archivos tocados (conteo), tests (n en verde).
2. Decisiones técnicas por defecto acumuladas (`ok` las valida todas; puedo rechazar por número).
3. Hallazgos corregidos de la Fase E (una línea c/u) y los no bloqueantes enviados a `DEBT.md`.
4. **Plan de prueba manual** derivado de §8 y §9 (en modificación, acotado al CHANGE-SET): pasos numerados, precondición/datos, resultado esperado, cómo levantar el entorno (WORKFLOW §7.5).

Si rechazo una decisión técnica por número: reemplazala, re-corré el gate automático y volvé a presentarme solo lo que cambió + el plan de prueba (si cambió). **Mi respuesta `ok` es la autorización del commit** — no me vuelvas a preguntar por el gate ni por el mensaje: commiteá directo con la convención de `/sdd-commit` (`feat(<ID>): …` + referencia a versión de spec). `ok push` → además pusheás la rama. Si reporto una falla, no commitees: volvé a Fase D (o abrí bug si corresponde).

Al commitear, borrá `sdd/specs/<ID>.flow.md`. Cierre en 2-3 líneas: commit creado, rama, siguiente paso (merge a staging y, tras el merge a `main`, spec → **Implemented** en spec e INDEX — WORKFLOW §11.6; si me lo pedís en ese momento, lo hacés vos).
