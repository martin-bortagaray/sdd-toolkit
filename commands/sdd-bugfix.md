---
description: "Sección 9 SDD — Tratamiento de bug con trazabilidad. Clasifica A/B/C, crea bugfix-NNN.md, exige test de regresión antes de cerrar."
argument-hint: "[descripción del bug] [severidad: critico|alto|medio|bajo]"
---

Vas a tratar un bug siguiendo la **Sección 9 del WORKFLOW**. Principio: un bug no rompe la regla "spec antes que código". Lo que cambia es la velocidad, no la trazabilidad. **Sin excepción, todo bug genera un artefacto `bugfix-NNN.md`.**

## Paso 1 — Clasificá ANTES de tocar código (paso obligatorio)

El bug es: **$ARGUMENTS**. Antes de nada, clasificá el tipo — determina qué corregís y dónde:

| Tipo | Definición | Qué corrijo |
|------|-----------|-------------|
| **A — Implementación** | El código no cumple lo que la spec dice. La spec estaba bien. | Solo el código. La spec no cambia. |
| **B — Spec** | La spec no contempló el caso, era ambigua o modeló mal. El código hizo lo que la spec decía. | Primero la spec (nueva versión), luego el código. |
| **C — Cambio de negocio** | El sistema se comporta como la spec dice, pero el negocio cambió de opinión. | No es bug: es feature nueva → ciclo SDD completo (`/sdd-discovery`). |

> Señal de alerta: si dudás entre A y B, casi siempre es B. La ambigüedad de spec es la causa más frecuente de bugs.

Para clasificar, leé la spec afectada en `sdd/specs/` y compará comportamiento observado vs. lo que la spec dice. Presentame tu clasificación y el porqué antes de avanzar. Si es **Tipo C**, paramos acá y lo tratamos como feature.

## Paso 2 — Creá el artefacto `bugfix-NNN.md`

1. Numeración secuencial por proyecto: mirá `sdd/bugs/` para el próximo NNN.
2. Usá el template `${CLAUDE_PLUGIN_ROOT}/templates/bugfix.template.md`. Completá: descripción (observado vs esperado), reproducción, root cause, criterio de aceptación testeable, severidad, tipo, spec afectada con versión.
3. Estado inicial **Abierto**.

## Paso 3 — Flujo según severidad

- **Crítico** (producción caída / dato corrupto): única excepción donde el fix mínimo puede preceder al artefacto completo. Fix mínimo (sin refactor), creá el `bugfix-NNN.md` Abierto el mismo día con root cause "Pendiente", completalo en 24h, actualizá spec si es Tipo B en la sesión siguiente.
- **Alto / Medio / Bajo:** proceso completo sin atajos. Si es **Tipo B → actualizá la spec primero** (nueva versión + changelog), recién después el código.

## Paso 4 — Test de regresión (regla de cierre)

**El bug no se cierra hasta que el test de regresión existe y pasa.**

1. Escribí el test ANTES del fix: debe **fallar** con el código actual y reproducir el caso exacto.
2. Generá el fix mínimo (instrucción explícita: no refactorizar, no mejorar, no agregar nada fuera del scope del bug).
3. Verificá que el test **pasa** y se incorpora a la suite de la feature afectada.
4. Referenciá el test (nombre + archivo) en el `bugfix-NNN.md`.

## Paso 5 — Prueba manual ANTES de cerrar y commitear

El test de regresión automático prueba que el caso exacto no vuelve, pero no reemplaza que yo reproduzca el bug y confirme el arreglo en la experiencia real.

1. **Armá un plan de prueba manual** a partir de los **pasos de reproducción** y el **criterio de aceptación del fix** del `bugfix-NNN.md`: la prueba es reproducir el caso original y confirmar que ahora se comporta como se espera. Pasos numerados, con precondición y resultado esperado.
2. **Esperá mi confirmación explícita** de que reproduje el caso y el bug ya no ocurre. Si todavía falla, no cerramos ni commiteamos: seguimos en fix.

## Paso 6 — Cierre

Pasá el artefacto a **Cerrado** solo con: fix verificado, test de regresión en verde y en la suite, **prueba manual confirmada por mí**, spec actualizada si era Tipo B. Para commitear usá `/sdd-commit` (detecta el `bugfix-NNN`, arma el prefijo `fix(bugfix-NNN):` y vuelve a ofrecer el gate de prueba manual como red de seguridad).
