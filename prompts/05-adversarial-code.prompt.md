# Prompt — Pasada adversaria de código

> **Versión:** 20261101-v8 · historia en `/CHANGELOG.md`
> **Uso:** Por defecto (MODO FEATURE, v19) **una vez por feature**, sobre el diff completo, después de que todas las capas quedaron en verde. En MODO CAPA (manual), después de cada capa.
> **Dónde se ejecuta:** Vía el comando `/sdd-adversarial-code` en Claude Code (corre en subagente con contexto limpio), o en conversación nueva en Claude.ai. NUNCA en la conversación donde se generó el código (WORKFLOW.md sección 11.1, modelo híbrido v10).

---

## Cuándo se ejecuta según el track (WORKFLOW.md 8.3.2, v20)

- **Track Completo, y features nuevas Estándar:** se ejecuta sobre el diff completo de la feature.
- **Track Rápido de pura presentación ("pura presentación" = el diff no cambia condicionales, queries, validaciones ni datos que se persisten o envían: solo layout, textos, estilos, orden visual o formato de salida): este prompt NO se ejecuta.** Se reemplaza por **checks inline** en la misma sesión de generación: tests + typecheck/build + revisión del diff contra `CONVENTIONS.md`. Sobre un diff cosmético la independencia de contexto compra poco; el riesgo real lo cubren los tests y el gate de prueba manual (que no se relaja en ningún track).
- **Track Rápido con lógica, y modificaciones Estándar: se ejecuta acotado al diff, con contexto selectivo.** (En una feature nueva Rápido no hay CHANGE-SET: el contexto es la mini-spec + el diff.) El subagente recibe: el diff de la capa (no todo el código), las secciones de la spec que el CHANGE-SET toca + el CHANGE-SET, `CONVENTIONS.md` + `PRINCIPLES.md` siempre, y `DOMAIN_MODEL.md`/`ARCHITECTURE.md` solo según las capas tocadas (8.3.2). Los hallazgos se reportan solo sobre el código del delta y su interacción con el código existente que toca.
- **Válvula de escape:** si la revisión revela que el cambio toca algo que su track no admite (modelo, reglas, seguridad, dinero, contratos externos, irreversible), el hallazgo es bloqueante y el track sube (WORKFLOW.md 8.3.2).

## Alcance FEATURE (por defecto desde v19)

La pasada corre **una vez sobre el diff completo de la feature**, no una vez por capa. Contexto = **unión** de las filas de la matriz de abajo para las capas que la feature tocó (cada documento se carga una sola vez). Si la feature toca backend y UI con un diff grande (>~800 líneas), el orquestador lanza **dos subagentes en paralelo** (capas 1-3 / capa 4), cada uno con su fila de la matriz. Los hallazgos citan archivo y capa. Omití observaciones de estilo o preferencia: solo desvíos de spec, seguridad, PRINCIPLES, bugs lógicos, casos de error y sobre-ingeniería.

## Cómo usar este prompt

1. En Claude Code corre como subagente (`/sdd-adversarial-code`, o lanzado por `/sdd-feature`); en Claude.ai, conversación nueva.
2. Cargá **solo el contexto que el alcance toca** — nunca el foundation completo ni la spec completa. **Alcance FEATURE:** unión de las filas de las capas tocadas. **Alcance CAPA (manual):** una fila. Matriz por capa:

   | Capa | Foundation a cargar | Secciones de spec |
   |---|---|---|
   | 1 — Modelo de datos | `DOMAIN_MODEL`, `CONVENTIONS`, `PRINCIPLES` | §6, §7, §9 |
   | 2 — Lógica de negocio | `DOMAIN_MODEL`, `ARCHITECTURE`, `CONVENTIONS`, `PRINCIPLES` | §4, §7, §8, §9, §12 |
   | 3 — API / acceso | `ARCHITECTURE`, `CONVENTIONS`, `PRINCIPLES` | §4, §5, §8, §9, §12 |
   | 4 — UI | `CONVENTIONS`, `DESIGN_SYSTEM` (si existe), `PRINCIPLES` | §4, §5, §8, §13 |

   Más, siempre: el **código generado de la capa que estás revisando** y las specs dependientes de §12 relevantes a la capa. Transversal: `GLOSSARY.md` solo si la capa usa/introduce términos nuevos. **`PRODUCT.md` no se carga en esta pasada** (es racional de producto, no contrato de implementación).

   **En modificaciones Estándar y track Rápido con lógica:** acotado al diff (no a todo su código) y a las secciones que el CHANGE-SET toca.
3. Reemplazá los placeholders `{...}` del prompt.
4. Pegá el prompt completo y enviá.

---

## Advertencia sobre límites de la pasada adversaria del código

Antes de ejecutar este prompt, recordá que esta pasada adversaria **tiene límites definidos**:

**SÍ valida:**
- Que cada criterio de aceptación de la spec tiene un test que lo cubre.
- Que el código no modifica módulos marcados como "sin tocar".
- Que naming, patrones y convenciones siguen lo definido en CONVENTIONS.md y la spec.
- Que los casos de error definidos en la spec tienen manejo explícito.
- Que la estructura de archivos sigue lo definido en el proyecto.

**NO valida:**
- Que el criterio de aceptación captura correctamente la necesidad real del negocio.
- Que la restricción declarada en la spec era la correcta en primer lugar.
- Que la arquitectura elegida es la más adecuada para el problema.
- Que no existen casos de error que la spec no contemplaba.
- Que el diseño de la spec es técnicamente óptimo.

**Riesgo a tener presente — validación circular:** la IA generó la spec (a partir de mis respuestas durante el discovery), generó el código contra esa spec, y ahora va a verificar el código contra la misma spec. Si la spec capturó mal el requisito de negocio, el código y los tests serán consistentes entre sí pero incorrectos respecto al problema real. **La pasada adversaria del código no detecta este caso.** Si tengo dudas sobre si la spec captura bien la realidad del negocio, esas dudas se resuelven antes (en Fase 4, con consulta a experto de dominio si corresponde), no con esta pasada.

---

## Prompt

```
Necesito que actúes como revisor adversario de código. Tu trabajo NO es validarlo ni decirme que está bien. Tu trabajo es encontrarle problemas.

CONTEXTO:
Te paso el código generado para la {CAPA: 1-Modelo de datos / 2-Lógica de negocio / 3-API / 4-UI} de la feature {ID-SPEC} versión {YYYYMMDD-vN}.

Acabás de recibir también los artefactos del setup foundacional del proyecto y la spec completa de la feature.

ALCANCE DE TU REVISIÓN:
Tu validación es contra la spec. Asumí la spec como contrato dado. No cuestiones si el criterio de aceptación captura bien la realidad del negocio, ni si la arquitectura elegida es óptima, ni si la spec en sí está bien diseñada. Esas validaciones ocurren en otras fases del proceso. Tu trabajo es verificar que el código cumple lo que la spec dice.

LO QUE QUIERO QUE BUSQUES (en orden de prioridad):

1. Desvíos respecto a la spec: el código no implementa exactamente lo que la spec pide. Listame cada desvío con cita textual de la sección de la spec violada y cita textual del código que la viola.

2. Decisiones implícitas no marcadas: el código toma decisiones que la spec no especifica (tipos de datos, validaciones, manejo de errores, defaults). Listámelas. NO me digas si son razonables o no — solo listámelas para que yo decida.

3. Violaciones de convenciones (CONVENTIONS.md): naming wrong, estructura de carpetas, patrones declarados que no se respetan. Cita textual de la convención violada + cita del código.

4. Violaciones de principios (PRINCIPLES.md): especialmente seguridad. Falta de autenticación donde la política la exige, validación faltante, manejo de errores que expone información sensible, logging que no respeta política de datos sensibles, etc.

5. Inconsistencias con el modelo conceptual (DOMAIN_MODEL.md): entidades con atributos o relaciones que no coinciden con el modelo declarado. Esto es especialmente crítico en Capa 1.

6. Bugs lógicos: errores que harían que el código no funcione correctamente en casos válidos según la spec. NO bugs hipotéticos en casos fuera de spec.

7. Casos borde no cubiertos: casos borde explícitamente declarados en la sección 9 de la spec (Casos borde y manejo de errores) que el código no maneja correctamente.

8. Sobre-ingeniería: cosas que el código agrega y que NO están en la spec ni requeridas por convenciones/principios. Validaciones de más, atributos adicionales, relaciones no pedidas, capas de abstracción innecesarias, manejo de casos no declarados.

FORMATO DE TU RESPUESTA:

Listá hallazgos numerados, agrupados por las 8 categorías. Para cada hallazgo:
- Cita textual del código problemático (con ruta de archivo y línea aproximada si es posible).
- Cita textual de la spec / convención / principio violado.
- Por qué es un problema.
- NO propongas reescritura. Sugerencia quirúrgica.

Reportá SOLO las categorías en las que encontraste hallazgos. NO inventes hallazgos para llenar categorías vacías. Cerrá con UNA línea que liste por número las categorías que revisaste y quedaron sin hallazgos (ej: "Revisadas sin hallazgos: 3, 5, 7, 8") — así queda constancia de que cubriste las 8 sin gastar un párrafo por categoría vacía.

RESTRICCIONES:
- No felicites nada del código. No me digas qué está bien.
- No suavices el lenguaje.
- Si dudás si algo es problema, marcalo como "zona gris".
- Tu opinión sobre estilo de código sin base en CONVENTIONS.md no cuenta como hallazgo.
- No cuestiones la spec en sí. Tu validación es contra la spec, asumida como contrato dado.

CIERRE:
Terminá con UNA pregunta crítica: ¿qué riesgo operativo concreto introduce este código si se mergea tal cual está?
```
