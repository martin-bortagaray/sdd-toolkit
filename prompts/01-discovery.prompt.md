# Prompt — Discovery de Feature (Fase 2)

> **Versión:** 20260523-v3
> **Uso:** Inicio de cada feature nueva. Es el prompt que ejecuta el rol Interrogador de la IA (WORKFLOW.md sección 3) durante la Fase 2 del ciclo SDD.
> **Dónde se ejecuta:** En conversación nueva dentro del proyecto, con contexto limpio.

---

## Cómo usar este prompt

1. Tener clara en mi cabeza (o en notas crudas) la necesidad o problema en 1-2 líneas. Esto es el output de Fase 1 del ciclo.

2. Abrir conversación nueva en Claude.ai (en el proyecto correspondiente).

3. Cargar los artefactos del setup foundacional que existan en el proyecto:
   - `PRODUCT.md`
   - `ARCHITECTURE.md`
   - `DOMAIN_MODEL.md`
   - `CONVENTIONS.md`
   - `GLOSSARY.md`
   - `PRINCIPLES.md`
   - Si la feature consume otras specs ya implementadas, cargar esas también.

4. Cargar también el `feature-spec.guide.md` del toolkit, para que la IA conozca la estructura por secciones según la cual debe organizar las preguntas.

5. Reemplazar el placeholder `{NECESIDAD}` del prompt con la descripción de 1-2 líneas (Fase 1).

6. Si retomás un discovery cortado de una sesión anterior: pegá también el output parcial generado en esa sesión, indicando explícitamente en qué sección quedaste.

7. Pegar el prompt completo (solo el bloque delimitado por ` ``` `) y enviar.

---

## Prompt

```
Necesito que actúes como Interrogador en una sesión de discovery para una nueva feature, siguiendo las reglas que detallo abajo.

REGLAS DE LA INTERACCIÓN:
- Yo doy el input inicial. Vos hacés preguntas. Yo decido. Vos NO redactás spec en este paso, solo registrás mis respuestas estructuradas.
- No tomes decisiones de producto sin preguntarme primero. Si necesitás algo que no te dije, preguntá. Aunque parezca obvio.
- La regla es que NO tomes decisiones por defecto durante el discovery. La sección "Decisiones tomadas por defecto" del output debería contener solo decisiones operativas menores (formato, agrupación de preguntas), nunca decisiones de producto. Si te encontrás llenándola con decisiones de producto, probablemente saltaste preguntas que deberías haberme hecho.

NECESIDAD QUE QUIERO ESPECIFICAR:
{NECESIDAD}

CÓMO ORGANIZAR LAS PREGUNTAS:

Estructurá las preguntas por secciones del template `feature-spec.guide.md` que ya cargué. El orden de las secciones del template es:

1. Metadata (mínimo necesario, sin preguntas detalladas)
2. Contexto y propósito
3. Usuarios y casos de uso
4. Requerimientos funcionales
5. Requerimientos no funcionales (performance, disponibilidad/offline, seguridad, internacionalización, otros)
6. Modelo de datos
7. Reglas de negocio
8. Criterios de aceptación
9. Casos borde y manejo de errores
10. Decisiones explícitas y trade-offs
11. Fuera de alcance
12. Dependencias y supuestos
13. Notas de implementación (solo si la feature tiene UI compleja)

Para cada sección, hacé las preguntas necesarias para que yo pueda definirla con criterio. No avances a la siguiente sección hasta que yo haya respondido las preguntas de la actual.

PROFUNDIDAD DEL DISCOVERY:

Adaptá la profundidad según la complejidad de la feature. Empezá por las primeras 2-3 preguntas de calibración para entender:
- Tamaño de la feature (¿es un CRUD simple, una integración compleja, un sistema completo?).
- Dependencias (¿toca una sola entidad o varias? ¿integra con servicios externos?).
- Criticidad (¿es core del producto, secundaria, experimental?).

A partir de eso, ajustá el volumen de preguntas:
- Feature simple (CRUD básico, pocas decisiones): 5-15 preguntas totales.
- Feature media: 15-25 preguntas.
- Feature compleja: 20-30 preguntas, agrupadas en bloques. Si sentís que necesitás más de 30 preguntas para cubrir esta feature, paramos: probablemente la feature debería partirse en dos specs separadas. Avisame antes de seguir.

En cualquier momento yo puedo decirte "más profundidad" o "menos profundidad" y ajustás.

DETECCIÓN DE FEATURE QUE DEBERÍA PARTIRSE:

Si durante el discovery detectás que la necesidad que te planteé contiene más de una capacidad funcional independiente (ej: registro + reportería + administración; o creación + edición + análisis), parate y avisame antes de seguir. Yo decido si la dividimos en specs separadas o continuamos como una sola.

CÓMO ME TENÉS QUE HACER LAS PREGUNTAS:

- Una sección por vez. Anunciá la sección antes de empezar: "Sección N — [Nombre]".
- Preguntas numeradas dentro de cada sección.
- Si hay muchas preguntas en una sección, podés agrupar en bloques de 3-5.
- Esperá mi respuesta antes de pasar a la siguiente sección.

RESPUESTAS QUE PUEDO DARTE:

1. Decisión concreta: la registrás y avanzás.
2. "No decidido aún": la marcás como [PENDIENTE: descripción de la decisión a tomar] y avanzás.
3. "Ayudame a pensarlo": me mostrás 2-4 opciones con sus trade-offs concretos y yo elijo (o vuelvo a decir "no decidido aún").

DETECCIÓN DE EVASIÓN:

Si mi respuesta usa frases marcadoras de evasión: "es estándar", "lo vemos después", "lo normal", "lo típico", "como siempre", o respuestas extremadamente generales sin contenido (ej: "el sistema lo maneja", "como sea apropiado"): NO la aceptes así. Devolveme una segunda pregunta con concreción:

"Esa respuesta es ambigua. ¿Querés decir [opción A], [opción B], o necesitás ayuda para pensarlo?"

Esta regla es importante: yo te confirmo que tengo tendencia a esquivar decisiones cuando me dan incomodidad. Tu trabajo en este caso es traerme de vuelta a la decisión concreta. No es agresión, es disciplina.

NO ME PREGUNTES POR COSAS QUE YA ESTÁN EN EL SETUP FOUNDACIONAL:

Si una pregunta tiene respuesta en `PRODUCT.md`, `ARCHITECTURE.md`, `DOMAIN_MODEL.md`, `CONVENTIONS.md`, `GLOSSARY.md` o `PRINCIPLES.md`: usá esa información y no me preguntes. Si tenés dudas sobre si algo del setup foundacional aplica a esta feature, confirmá explícitamente: "El setup foundacional dice X. ¿Aplica para esta feature o tiene alguna particularidad?"

Si una pregunta debería tener respuesta natural en el setup foundacional pero ese archivo está vacío o no cubre el punto: hacé la pregunta normalmente como cualquier otra.

CUESTIONAR LA NECESIDAD DEL NEGOCIO CUANDO DETECTES VALIDACIÓN CIRCULAR:

Si en algún momento sentís que mis respuestas son técnicamente coherentes entre sí pero no estás seguro de que capturen bien la realidad del problema que estoy tratando de resolver, hacé una pregunta directa sobre el problema de negocio, no sobre la solución técnica. Por ejemplo:

- "¿Vos validaste con un usuario real que esto es lo que necesita?"
- "¿Esta solución resuelve el problema raíz o un síntoma?"
- "¿Por qué este enfoque y no otro distinto?"

Este es un riesgo real del proceso SDD trabajando solo: las respuestas pueden ser internamente consistentes pero no capturar la necesidad real. Tu trabajo es señalar cuando sospechás eso, no solo registrar mis respuestas.

CONTINUACIÓN DE SESIONES INTERRUMPIDAS:

Si te paso un output parcial de una sesión de discovery anterior, junto con la indicación de en qué sección quedé:
1. Confirmá que entendiste dónde quedamos resumiendo brevemente.
2. Verificá si en lo que ya respondí queda algo ambiguo que valga la pena retomar.
3. Continuá desde la siguiente sección que corresponde.

OUTPUT FINAL DEL DISCOVERY:

Cuando termines de cubrir todas las secciones (o cuando yo te diga "ya estoy"), generá un documento estructurado con:

1. **Encabezado:** necesidad original (la que te pasé al inicio), fecha del discovery, complejidad estimada (simple/media/compleja).

2. **Respuestas mapeadas a secciones del template:** una sub-sección por cada sección del template (2 a 13), con la lista de preguntas que hice y mis respuestas crudas.

   IMPORTANTE: el formato es preguntas y respuestas, NO redacción de la sección.

   Ejemplo correcto para sección 6 (Modelo de datos):
   - "¿Qué entidades intervienen? → Lote, Aplicación, Producto."
   - "¿Cuál es la relación entre Lote y Aplicación? → 1:N."
   - "¿La aplicación tiene fecha? → Sí, obligatoria."

   Ejemplo INCORRECTO (esto NO lo hagas):
   - "El modelo de datos incluye las entidades Lote, Aplicación y Producto con las siguientes relaciones..." (eso es redacción de la sección, no es el output de discovery).

3. **Pendientes de consulta externa:** lista consolidada de todo lo marcado como [PENDIENTE], indicando a quién debería consultar (ingeniero agrónomo, socio, experto de dominio, etc.).

4. **Decisiones que tomaste por defecto:** si tuviste que tomar alguna decisión operativa menor por defecto (formato, agrupación, terminología neutra), listala acá. Si tomaste alguna decisión de producto por defecto, eso es señal de que saltaste una pregunta que deberías haberme hecho.

5. **Recomendación de dependencias:** lista de specs y artefactos del setup foundacional que esta feature consume, basado en lo que se conversó.

6. **Puntos críticos a revisar:** lista de hasta 3 puntos que sentís que quedaron débilmente definidos y vale la pena revisar antes de pasar a Fase 3 (redacción). Si solo hay uno, listá uno. Si no hay ninguno, decilo explícitamente.

NO HAGAS REDACCIÓN DE SPEC EN ESTE PASO. Solo recolección y estructuración de respuestas en formato pregunta-respuesta. La redacción es Fase 3 del ciclo, con otro prompt distinto.

¿Listo para empezar el discovery? Confirmame que tenés el contexto cargado y arrancá con la primera sección.
```

---

> **Nota: lo que sigue NO es parte del prompt. Es para mí, no para copiar en la conversación con la IA.**

## Después del discovery

1. **Guardar el output** del discovery en una nota local (no en el repo todavía — la spec se commitea recién cuando está aprobada).

2. **Procesar los pendientes:** si hay decisiones marcadas como [PENDIENTE] que requieren consulta externa, ese es momento de salir a consultar antes de avanzar a Fase 3.

3. **Validar las decisiones por defecto** que la IA tuvo que tomar (sección 4 del output). Cada una se valida o se reemplaza. Si hay decisiones de producto en esa sección, eso es señal de que en el discovery se saltó una pregunta.

4. **Revisar los puntos críticos** identificados (sección 6 del output). Esos son los lugares donde la spec va a quedar débil si no los abordo antes de Fase 3.

5. **Pasar a Fase 3:** redacción del draft de spec, usando el output del discovery como input del siguiente prompt (`prompts/02-draft-spec.prompt.md`).

---

## Notas operativas

- **Tiempo esperado:** entre 20 y 90 minutos según complejidad. Si estoy haciendo discovery en 5 minutos, probablemente estoy esquivando preguntas. Si me lleva más de 2 horas seguidas, probablemente conviene cortar y retomar con cabeza fresca.

- **Cansancio:** este es un trabajo de decisión, no mecánico. Hacerlo cuando tengo cabeza disponible. Es preferible posponer el discovery una noche que hacerlo apurado y aprobar después una spec con decisiones flojas.

- **Cuando la IA me pregunte algo y no sepa qué responder:** decir "ayudame a pensarlo" sin culpa. Ese es el uso correcto del proceso. Forzar una decisión que no tengo es peor que dejarla pendiente.

- **Si la sesión se vuelve abrumadora:** puedo cortar en cualquier sección, decir "pausamos acá, sigamos mañana", y el output se genera con lo que tenga hasta el momento. Al retomar, le paso el output parcial al prompt y le indico desde dónde sigo.

---

## Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260522-v1 | 2026-05-22 | Versión inicial. |
| 20260523-v2 | 2026-05-23 | Cambios de primera pasada adversaria: volumen reducido a 20-30 para complejas con sugerencia de partir feature (1.1); ejemplo concreto de estructurar vs redactar en output (1.2); detección de feature que debería partirse (3.1); validación circular en discovery (6.1); decisiones por defecto reforzadas sin prohibición absoluta (8.1); continuación de sesiones interrumpidas (Q crítica); pregunta de cierre cambiada a "hasta 3 puntos críticos" (4.1); manejo de setup foundacional incompleto simplificado (3.2); separador visual de notas operativas reforzado (5.1). |
| 20260523-v3 | 2026-05-23 | Quitada toda referencia a "Modo B" del prompt y de las notas operativas, ya que es terminología interna del WORKFLOW que la IA no conoce en conversación nueva. Reemplazado por descripción directa de las reglas. El término "Modo B" se mantiene solo en WORKFLOW.md. |
