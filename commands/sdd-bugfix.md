---
description: "Sección 9 SDD — Tratamiento de bug con trazabilidad. Clasifica A/B/C, exige test de regresión antes de cerrar; bugfix-NNN.md solo cuando amerita (Tipo B, Crítico/Alto o causa no obvia)."
argument-hint: "[descripción del bug] [severidad: critico|alto|medio|bajo]"
---

Vas a tratar un bug siguiendo la **Sección 9 del WORKFLOW**. Principio: un bug no rompe la regla "spec antes que código". Lo que cambia es la velocidad, no la trazabilidad. **Todo bug queda trazado (WORKFLOW §9.3, v20):**

- **Con artefacto `bugfix-NNN.md`** si es **Tipo B**, severidad **Crítica o Alta**, o el **root cause no es obvio**.
- **Sin artefacto** en el resto (Tipo A, Media/Baja, causa clara): la trazabilidad es el **test de regresión + commit `fix(<spec-id>): …`** con observado vs esperado, causa y nombre del test en el cuerpo. Si en el camino la causa deja de ser obvia o resulta Tipo B, creás el artefacto en el acto.

## Paso 1 — Clasificá ANTES de tocar código (paso obligatorio)

El bug es: **$ARGUMENTS**. Antes de nada, clasificá el tipo — determina qué corregís y dónde:

| Tipo | Definición | Qué corrijo |
|------|-----------|-------------|
| **A — Implementación** | El código no cumple lo que la spec dice. La spec estaba bien. | Solo el código. La spec no cambia. |
| **B — Spec** | La spec no contempló el caso, era ambigua o modeló mal. El código hizo lo que la spec decía. | Primero la spec (nueva versión), luego el código. |
| **C — Cambio de negocio** | El sistema se comporta como la spec dice, pero el negocio cambió de opinión. | No es bug: es feature nueva → ciclo SDD completo (`/sdd-discovery`). |

> Señal de alerta: si dudás entre A y B, casi siempre es B. La ambigüedad de spec es la causa más frecuente de bugs.

Para clasificar, leé la spec afectada en `sdd/specs/` y compará comportamiento observado vs. lo que la spec dice. **En un solo mensaje** (WORKFLOW v19 — una espera, no tres) presentame: clasificación A/B/C + porqué, severidad, **si lleva artefacto o no** (con el criterio de arriba), root cause hipotético, el test de regresión que vas a escribir y el fix mínimo que proponés (y, si es Tipo B, el cambio de spec). Si es **Tipo C**, paramos acá y lo tratamos como feature (`/sdd-feature`).

**Con mi `ok` seguís sin más confirmaciones** por los Pasos 2-4 (artefacto, spec si es B, test que falla, fix, test en verde) hasta la prueba manual del Paso 5. Solo frenás si el root cause resulta distinto del hipotético o aparece una decisión de producto.

## Paso 2 — Creá el artefacto `bugfix-NNN.md` (solo si lleva artefacto)

1. Numeración secuencial por proyecto: mirá `sdd/bugs/` para el próximo NNN.
2. Usá el template `${CLAUDE_PLUGIN_ROOT}/templates/bugfix.template.md`. Completá: descripción (observado vs esperado), reproducción, root cause, criterio de aceptación testeable, severidad, tipo, spec afectada con versión.
3. Estado inicial **Abierto**.

## Paso 3 — Flujo según severidad

- **Crítico** (producción caída / dato corrupto): única excepción donde el fix mínimo puede preceder al artefacto completo. Fix mínimo (sin refactor), creá el `bugfix-NNN.md` Abierto el mismo día con root cause "Pendiente", completalo en 24h, actualizá spec si es Tipo B en la sesión siguiente.
- **Alto:** proceso completo con artefacto. **Medio / Bajo:** con artefacto si es Tipo B o causa no obvia; si no, test → fix → commit trazado. En todos los casos, si es **Tipo B → actualizá la spec primero** (nueva versión + changelog), recién después el código.

## Paso 4 — Test de regresión (regla de cierre)

**El bug no se cierra hasta que el test de regresión existe y pasa.**

1. Escribí el test ANTES del fix: debe **fallar** con el código actual y reproducir el caso exacto.
2. Generá el fix mínimo (instrucción explícita: no refactorizar, no mejorar, no agregar nada fuera del scope del bug).
3. Verificá que el test **pasa** y se incorpora a la suite de la feature afectada.
4. Referenciá el test (nombre + archivo) en el `bugfix-NNN.md`, o en el cuerpo del commit `fix:` si no hay artefacto.

## Paso 5 — Prueba manual ANTES de cerrar y commitear

El test de regresión prueba que el caso exacto no vuelve. La prueba manual se **acota a lo que ese test no cubre** (WORKFLOW §7.5 / §9.6, v20):

1. **Armá un plan de prueba manual** a partir de los pasos de reproducción y el criterio de aceptación del fix. Si el test de regresión **no ejercita el camino real** (UI, integración, datos reales), la prueba es reproducir el caso original en el entorno real y confirmar el arreglo. Si el test ya lo ejercita de punta a punta, alcanza con un recorrido corto del flujo afectado. Pasos numerados, con precondición y resultado esperado.
2. **Esperá mi confirmación explícita** de que reproduje el caso y el bug ya no ocurre. Si todavía falla, no cerramos ni commiteamos: seguimos en fix.

## Paso 6 — Cierre

Pasá el artefacto (si lo hay) a **Cerrado** solo con: fix verificado, test de regresión en verde y en la suite, **prueba manual confirmada por mí**, spec actualizada si era Tipo B. **Mi `ok` a la prueba manual autoriza el commit:** commiteá directo con prefijo `fix(bugfix-NNN):` — o `fix(<spec-id>):` con observado/esperado, causa y test en el cuerpo si no hubo artefacto — (convención de `/sdd-commit`), sin volver a preguntar por el gate ni por el mensaje. `ok push` → también pusheás.
