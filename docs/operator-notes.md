# Operator Notes - sdd-toolkit

> Notas operativas del autor, extraidas de la cola humana de cada prompt (las secciones marcadas como NO parte del prompt). Viven aca para que los comandos slash del plugin no las carguen en contexto en cada invocacion. Son referencia del autor, no instrucciones para la IA. Agrupadas por prompt.


---

## Fase 0 - Discovery inicial del proyecto

*(prompts/00-project-discovery.prompt.md)*

## Después del discovery inicial

1. **Guardar el output** del discovery en una nota local. La carpeta del proyecto todavía no existe formalmente.

2. **Procesar los pendientes:** si hay decisiones marcadas como [PENDIENTE] que requieren consulta externa (experto de dominio, socio, validación con usuarios), ese es momento de salir a consultar antes de avanzar al prompt 00b.

3. **Validar las decisiones por defecto** que la IA tuvo que tomar (sección 4 del output). Cada una se valida o se reemplaza. Si hay decisiones de producto/arquitectura/dominio en esa sección, eso es señal de que en el discovery se saltó una pregunta.

4. **Revisar los cuestionamientos de viabilidad** (sección 5 del output). Si la IA detectó problemas en el proyecto, decidir qué hacer:
   - Resolver el problema y actualizar las respuestas.
   - Aceptar el problema conscientemente y documentarlo como riesgo.
   - Pausar el proyecto si el problema es estructural.

5. **Revisar los puntos críticos** identificados (sección 7 del output). Esos son los lugares donde el setup foundacional va a quedar débil si no se abordan antes de redactar.

6. **Pasar al prompt 00b:** redacción del setup foundacional + roadmap, usando este output como input.

---

## Notas operativas

- **Tiempo esperado:** entre 1 y 4 horas según tamaño del proyecto. Si lo hacés en 15 minutos, probablemente estás esquivando preguntas. Si te lleva más de 4 horas seguidas, conviene cortar y retomar con cabeza fresca.

- **Este es un trabajo de decisión estratégica.** Hacerlo cuando tengo energía y tiempo. Es preferible posponer el discovery una semana que hacerlo apurado y producir un setup foundacional débil que paga costos en cada feature posterior.

- **Cuando la IA me pregunte algo y no sepa qué responder:** decir "ayudame a pensarlo" sin culpa. Ese es el uso correcto del proceso. Para un proyecto entero, hay muchas decisiones que no se pueden tomar sin pensar.

- **Si la sesión se vuelve abrumadora:** podés cortar en cualquier bloque, decir "pausamos acá, sigamos mañana", y el output se genera con lo que tengas hasta el momento. Al retomar, le pasás el output parcial al prompt y le indicás desde qué bloque sigue.

- **Consulta a experto de dominio:** para proyectos donde el dominio no es tu especialidad (ej: el proyecto agro con tu hermano agrónomo), es esperable que muchas respuestas del Bloque 3 (Dominio y entidades) queden como [PENDIENTE]. Eso es correcto. Resolvelas antes de pasar al prompt 00b.


---

## Fase 0 - Setup foundacional + roadmap

*(prompts/00b-setup-foundation.prompt.md)*

## Después de la redacción

1. **Lectura crítica de los 7 documentos.** No "le doy una mirada". Lectura completa con cabeza fresca (Regla 3).

2. **Validar la sección de decisiones por defecto.** Cada una se valida o se reemplaza. Si hay decisiones de producto/arquitectura/dominio (no debería, pero por las dudas), eso es señal de que algo se saltó.

3. **Verificar consistencia entre documentos.** El prompt 00b ya hizo verificación interna, pero vale releer:
   - Entidades del DOMAIN_MODEL ↔ términos del GLOSSARY.
   - Arquitectura del ARCHITECTURE ↔ principios del PRINCIPLES.
   - Casos de uso del PRODUCT ↔ specs del ROADMAP.

4. **Si todo cierra:** los 7 documentos quedan listos para guardar en el repo del proyecto. Crear el repo, hacer commit inicial.

5. **Crear `INDEX.md`** del proyecto usando `templates/project-index.template.md`. La primera spec del proyecto va a llevar número 001.

6. **Pasar al Paso 3 de Fase 0:** diseño del prototipo UI con Claude Design (prompt `00c-design-prototype.prompt.md`).

---

## Notas operativas

- **Tiempo esperado:** la redacción en sí toma minutos para el LLM. La lectura crítica posterior puede llevar 1-2 horas según complejidad del proyecto.

- **Por qué conversación separada del discovery:** los roles Interrogador y Redactor son distintos. Si los mezclás, el LLM tiene sesgo a "completar" lo que él mismo preguntó, perdiendo distancia crítica.

- **Si el LLM se desvía mucho de los templates:** parar y reformular el prompt apuntando al template específico violado.

- **Si después de la redacción los documentos se ven "muy parecidos al discovery":** buena señal. La redacción es traducir las respuestas crudas a documentos estructurados, no reescribir.

- **Si encontrás un error grave en revisión:** según la naturaleza:
  - Error de redacción (estructura mal aplicada): pedir corrección quirúrgica al LLM.
  - Error de contenido (decisión mal interpretada): puede requerir volver al discovery.
  - Error estructural (faltó cubrir algo importante): puede requerir extender el discovery con preguntas adicionales antes de regenerar.


---

## Fase 0 - Diseno de prototipo

*(prompts/00c-design-prototype.prompt.md)*

## Después de generar el brief

1. **Copiar el brief** generado por el prompt.

2. **Abrir Claude Design** y pegar el brief.

3. **Iterar con Claude Design** hasta tener un prototipo navegable de las pantallas aprobadas. Mantener el design system declarado en el brief.

4. **Guardar el output** en `docs/prototype/` del repo del proyecto:
   - URL compartible (si Claude Design lo permite).
   - Export del prototipo si está disponible.
   - Screenshots de cada pantalla principal (mínimo).
   - Una breve nota markdown describiendo qué incluye el prototipo y qué versión del brief usó.

5. **El prototipo es input para:**
   - La propuesta comercial al cliente (mostrar el producto visualmente).
   - El primer discovery de feature (Fase 2 del ciclo) cuando arranque desarrollo. Las decisiones del prototipo informan las specs, aunque las specs gobiernan en caso de conflicto.

---

## Notas operativas

- **No sobre-iterar en Claude Design.** El prototipo es exploración visual, no implementación final. Si pasás más de 1 hora iterando una pantalla, parar. El detalle fino se resuelve en la spec de esa feature, no en el prototipo.

- **El prototipo es referencia histórica.** Una vez que arranca desarrollo y se redactan las specs, el prototipo queda como referencia visual inicial, no se mantiene actualizado. Si una spec cambia algo respecto al prototipo, gana la spec (regla "prototipo informa, spec gobierna").

- **Si Claude Design genera algo muy distinto al design system declarado:** parar la iteración y verificar el brief. Probablemente algún elemento del design system no quedó claro en el brief.

- **Si el cliente pide cambios significativos al prototipo durante la propuesta:** esos cambios afectan al alcance del proyecto. Documentar los cambios y evaluar si afectan al setup foundacional o al roadmap. Si afectan, actualizar antes de avanzar.


---

## Fase 2 - Discovery de feature

*(prompts/01-discovery.prompt.md)*

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

## Fase 3 - Draft de spec

*(prompts/02-draft-spec.prompt.md)*

## Después de la redacción

1. **Lectura crítica del draft.** No "le doy una mirada". Lectura completa con cabeza fresca (Regla 3).

2. **Validar la sección 14 (Decisiones por defecto):** cada una se valida o se reemplaza. Si hay decisiones de producto en esa sección (no debería, pero por las dudas), eso es señal de que algo se saltó.

3. **Si todo cierra:** la spec queda en estado Draft, lista para Fase 4 (pasada adversaria con `prompts/03-adversarial-spec.prompt.md`).

4. **Actualizar el INDEX del proyecto:** agregar una fila a `specs/INDEX.md` con el ID, dominio, título, estado Draft, versión y fecha.

5. **Si encuentro problemas serios en el draft:** puedo volver a Fase 2 para discovery adicional, o pedir re-redacción con instrucciones específicas. El draft inicial no es sagrado.

6. **No commitear todavía.** La spec se commitea recién cuando está en estado Approved. Durante Draft y Review vive como archivo local.

---

## Notas operativas

- **Tiempo esperado:** la redacción en sí toma minutos para el LLM. La lectura crítica posterior puede llevar 20-40 minutos según complejidad.

- **Por qué conversación separada del discovery:** los roles Interrogador y Redactor están definidos como distintos en WORKFLOW.md sección 3. Si los mezclás en la misma conversación, el LLM tiene sesgo a "completar" lo que él mismo preguntó, perdiendo distancia crítica.

- **Si el LLM se desvía mucho del template:** parar y reformular el prompt apuntando a la regla específica violada. No iterar varias veces con instrucciones genéricas.

- **Si después de la redacción la spec se ve "muy parecida al discovery":** eso suele ser buena señal. La redacción es traducir las decisiones del discovery al formato del template. Si está muy distinta, posiblemente el LLM agregó decisiones que no le pediste.


---

## Fase 4 - Pasada adversaria de spec

*(prompts/03-adversarial-spec.prompt.md)*

## Después de la pasada adversaria

1. **No procesar hallazgos en caliente.** Leelos todos primero. Cabeza fresca.

2. **Clasificar hallazgos antes de iterar** (WORKFLOW.md sección 13.1):
   - Sólidos para iterar: contradicciones reales, gaps operativos concretos, violaciones a setup foundacional, decisiones implícitas no marcadas.
   - Zona gris: discutir antes de decidir.
   - Descartar: sugerencias estilísticas, casos teóricos improbables, sobre-especificación.

3. **Para cada hallazgo aceptado:** procesarlo y actualizar la spec.

4. **Documentar en sub-sección 10.2** de la spec todos los hallazgos procesados, con resolución (aceptado, descartado, modificado) y justificación. Esto es crítico para Pasada 2 (evita re-marcado).

5. **Subir versión de la spec** (`YYYYMMDD-vN+1`) y agregar entrada al changelog (sección 15).

6. **Estado:** la spec pasa de Draft a Review después de procesar Pasada 1. Permanece en Review durante Pasada 2 (si aplica) y hasta Fase 5.

---

## Notas operativas

- **Calidad de hallazgos, no cantidad.** Aplicar criterio de WORKFLOW.md sección 13.1. Una pasada que devuelve 20 hallazgos donde 15 son sugerencias estilísticas no es mejor que una de 5 hallazgos sustantivos.

- **Si el adversario marca muy poco:** probablemente la spec es buena, o el adversario no buscó bien. Verificá leyéndola vos. Si encontrás cosas que el adversario no marcó, considerá repetir con prompt reforzado.

- **Si el adversario marca contradicción con setup foundacional:** primero verificá si es real (releer ambos documentos). A veces el LLM marca "contradicción" cuando son matices que no se contradicen. Si es real, decidí: ¿corrijo la spec, o corrijo el setup foundacional? (WORKFLOW.md sección 7.1).

- **No iterar hallazgos repetidos entre pasadas:** la sub-sección 10.2 te protege de esto si la mantenés actualizada. Si el adversario re-marca algo ya cerrado, es señal de que olvidaste documentarlo en 10.2 o de que el adversario ignoró la instrucción. En ambos casos, descartá el hallazgo y verificá la sub-sección.


---

## Fase 6 - Codegen por capas

*(prompts/04-codegen-layer.prompt.md)*

## Después de cada capa

1. **Revisar la tabla comparativa** antes de confirmar. Si falta algún requerimiento en la tabla, pedirle al LLM que lo agregue antes de generar código.

2. **Revisar código y tests** con el checklist de WORKFLOW.md sección 7.4.

3. **Ejecutar pasada adversaria de código según tier** (WORKFLOW.md 8.3.2): en modificaciones **T1**, se reemplaza por checks inline en la misma sesión (tests + typecheck/build + revisión del diff contra `CONVENTIONS.md`); en **T2**, subagente con `prompts/05-adversarial-code.prompt.md` acotado al diff y contexto selectivo; en **T3 y builds iniciales**, pasada completa en conversación nueva/subagente.

4. **Procesar decisiones técnicas tomadas por defecto.** Para cada una: aceptar o pedir cambio quirúrgico. Si alguna decisión "técnica" esconde una decisión de producto, modificar la spec primero.

5. **Si el LLM detectó un gap:** resolverlo antes de continuar. Según la naturaleza:
   - Gap de redacción (la spec es ambigua pero la decisión ya está tomada): modificar spec, subir versión.
   - Gap de producto (decisión no tomada): volver a Fase 2 (discovery adicional) o decidir ahora y documentar en spec.
   - Gap de arquitectura: modificar ARCHITECTURE.md y evaluar impacto en specs anteriores.

6. **No commitees por capa.** El commit es uno solo, cuando la feature completa pasó la verificación de las 4 capas **y la prueba manual del autor** (gate previo al commit, WORKFLOW.md sección 7.5): un commit por feature, no por capa ni por archivo (granularidad en sección 7.6).

7. **Pasar a la siguiente capa** adjuntando el código aprobado como contexto adicional.

---

## Notas operativas

- **Claude Code vs. Claude.ai:** Claude Code mantiene contexto del proyecto por sí solo. Claude.ai requiere cargar contexto explícitamente en cada conversación. El prompt funciona en ambos, pero con Claude Code podés omitir el paso de adjuntar archivos de setup foundacional si ya están en el contexto del proyecto.

- **Si el LLM genera código que "funciona" pero no está en la spec:** eso es sobre-ingeniería. Pedirle que lo elimine. No es negociable.

- **Si la tabla comparativa muestra items "Parcial":** verificar que estén cubiertos en otra capa. Si llegan a Capa 4 como "Parcial", hay un gap de implementación.

- **Si el LLM pide aclaraciones sobre la spec:** eso es señal de que la spec tiene ambigüedad. Resolverla en la spec primero, no en el chat. Ver WORKFLOW.md sección 7.3.

- **Tests primero o después:** el prompt pide tests en el mismo output que el código de producción. Si preferís separar (generar código, revisar, después tests), podés adaptar el Paso 1 para pedirlo en dos rondas. Lo que no es negociable es que los tests existan antes de pasar a la siguiente capa.


---

## Fase 6 - Pasada adversaria de codigo

*(prompts/05-adversarial-code.prompt.md)*

## Después de la pasada adversaria

1. Procesá los hallazgos uno por uno. NO los aceptes todos por inercia.
2. Para cada hallazgo, decidí:
   - **Iterar código:** error técnico claro, lo corregís pidiendo cambio quirúrgico al LLM Generador (en la conversación original).
   - **Modificar spec:** si el "desvío" en realidad revela un gap o ambigüedad de la spec. Subir versión.
   - **Modificar setup foundacional:** si el problema afecta a más de una feature.
   - **Descartar:** si después de procesarlo, decidís que el hallazgo es flojo o no aplica.
3. Clasificá hallazgos en bloqueantes / no bloqueantes según protocolo del WORKFLOW.md sección 7.4.1.
4. Una vez procesados todos, ejecutás el checklist completo de verificación entre capas (sección 7.4) antes de pasar a la siguiente capa.

---

## Notas operativas

- **Conversación limpia:** la pasada adversaria del código NUNCA se hace en la conversación donde se generó. El LLM tiene sesgo a defender lo que escribió.
- **Si la pasada adversaria devuelve "todo está bien":** desconfiá. O el código es trivial, o el adversario no buscó bien. Repetir con prompt reforzado.
- **Si la pasada adversaria devuelve más de 20 hallazgos serios:** probablemente la capa tiene problemas estructurales. Considerá descartar la generación y volver a generar con prompt mejorado, en vez de iterar.
- **Si tenés dudas sobre la spec en sí:** este prompt no las va a resolver. Esas dudas se trabajan en Fase 4 con pasada adversaria de spec o con consulta a experto de dominio. Ver WORKFLOW.md sección 2.6 sobre riesgo de validación circular.


---

## Fase 5-6 - Verificacion pre-generacion

*(prompts/06-spec-verification.prompt.md)*

## Después de la verificación

### Si el veredicto es VERDE
Procedé a Fase 6 con `prompts/04-codegen-layer.prompt.md`.

### Si el veredicto es AMARILLO
Leé cada advertencia. Para cada una decidí:
- **Resolver antes de generar:** modificá la spec (sube versión), volvé a ejecutar este prompt.
- **Aceptar conscientemente:** registrá en sección 10.1 de la spec la decisión de avanzar con la advertencia y por qué la aceptás. Procedé a Fase 6.

No avancés con AMARILLO por inercia. La decisión de aceptar una advertencia tiene que ser explícita.

### Si el veredicto es ROJO
Resolvé los bloqueantes antes de continuar. Según la naturaleza del bloqueante:
- **Bloqueante formal (F1-F8):** modificá la spec (sube versión) y volvé a ejecutar.
- **Bloqueante de codegen (C1-C6):** puede requerir volver a Fase 2 (discovery adicional) si el problema es falta de información del negocio, o solo modificar la spec si es gap de redacción.

---

## Notas operativas

- **Este prompt no reemplaza la pasada adversaria de spec (Fase 4).** Son distintos: la pasada adversaria busca problemas de contenido y diseño; este verifica preparación operativa para generación.

- **Si el veredicto es VERDE pero tenés dudas:** las dudas sobre la spec se resuelven acá, antes de generar. Una vez que empezás Fase 6, cambiar la spec tiene costo (volver a generar capas, ver WORKFLOW.md sección 8.3.1).

- **Si una advertencia se repite en varias capas:** es señal de que el problema está en la spec, no en el código. Resolverlo en la spec antes de generar.


---

## Modificacion de spec existente

*(prompts/07-modify-spec.prompt.md)*

## Después de la modificación

1. **Lectura crítica de la spec modificada** completa, no solo del delta (Regla 3). Un cambio puede romper coherencia con secciones que no tocaste.
2. **Validar la sección 14** (decisiones por defecto).
3. **Pasada adversaria según tier** (WORKFLOW.md 8.3.2): **T1 la omite** (excepción codificada de Regla 4 — no hay riesgo de diseño que auditar); **T2** corre `/sdd-adversarial-spec` acotada al delta con contexto selectivo; **T3** la corre completa. En T2/T3, la pasada 2 solo se ejecuta si la pasada 1 tuvo bloqueantes (WORKFLOW.md 13.2).
4. **Actualizar el INDEX** del proyecto si cambió el estado de la spec.
5. **Verificación pre-generación** (`/sdd-verify`) en el modo del tier: **express** para T1, **delta** para T2, **completo** para T3.
6. **Codegen del delta** (`/sdd-codegen`): solo las capas que el cambio toca. Si el delta no afecta el modelo de datos, no se regenera Capa 1. **Pasale el CHANGE-SET (Bloque 3) como contexto:** es lo que hace que el codegen regenere solo los ítems ADDED/MODIFIED y preserve el resto del código existente, en vez de reconstruir la capa completa. El tier del header decide además la adversaria de código: checks inline en T1, subagente acotado en T2, completo en T3.

## Notas operativas

- **Specs as-built:** la primera modificación de cada spec reverse-engineered suele revelar que la descripción as-built tiene huecos. Es esperable. Completar esa base es parte del trabajo, no una distracción.
- **No infles el changelog ni la spec.** El cambio se documenta con densidad: qué y por qué, sin relleno.
- **Si el delta crece:** si al editar descubrís que el "cambio chico" toca media spec, pará y reconsiderá si no es en realidad una feature nueva o un cambio que debía ir al setup foundacional.
- **Válvula de escape del tier (WORKFLOW.md 8.3.2):** el tier es una hipótesis, no un permiso. Si en cualquier paso posterior (adversaria, verify, codegen, prueba manual) aparece evidencia de que el delta toca modelo de datos, reglas de negocio o seguridad: el tier sube en el acto, se actualiza el header del CHANGE-SET, se ejecutan los pasos salteados antes de continuar, y la re-clasificación queda en el changelog de la spec.
- **Antipatrón:** clasificar hacia abajo por ansiedad o cansancio. Si la justificación del tier no cita los criterios objetivos, la clasificación está mal hecha.

