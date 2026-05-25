# Prompt — Redacción de Spec (Fase 3)

> **Versión:** 20260523-v3
> **Uso:** Después de Fase 2 (Discovery) y antes de Fase 4 (Pasada adversaria). Es el prompt que ejecuta el rol Redactor de la IA (WORKFLOW.md sección 3).
> **Dónde se ejecuta:** En conversación nueva dentro del proyecto, con contexto limpio. NO en la misma conversación del discovery.

---

## Pre-requisitos antes de usar este prompt

**El output del discovery NO puede contener pendientes sin resolver NI decisiones por defecto sin validar.**

Si el output del discovery (Fase 2) tiene decisiones marcadas como `[PENDIENTE: ...]` o si contiene decisiones tomadas por defecto por la IA sin nota explícita de validación, este prompt va a rechazar redactar. Eso es deliberado.

Antes de avanzar:

1. Releer el output del discovery.
2. Identificar todos los `[PENDIENTE]`. Para cada uno: resolverlo (decisión mía) o consultar externamente.
3. Identificar la sección "Decisiones que tomaste por defecto" del output del discovery. Para cada decisión listada, agregar una nota de validación con este formato exacto:
   - `Validado por autor: aceptada.` (si mantengo la decisión de la IA tal cual).
   - `Validado por autor: reemplazada por: [decisión propia].` (si la cambio).
4. Actualizar el output del discovery con todas las resoluciones y validaciones.
5. **Recién entonces** uso este prompt.

Es coherente con WORKFLOW.md secciones 2.3 y 5 (no aprobar con pendientes), y con Regla 2 del WORKFLOW (todas las decisiones por defecto de la IA deben ser validadas explícitamente). Si arrancamos a redactar con pendientes o sin validar, la spec se construye sobre decisiones aceptadas por inercia.

---

## Cómo usar este prompt

1. Verificar pre-requisitos del paso anterior.

2. Abrir conversación nueva en Claude.ai. **No usar la conversación del discovery.** Los roles Interrogador y Redactor deben ir en conversaciones separadas (WORKFLOW.md sección 3).

3. **Adjuntar como archivos** (no pegar como texto plano) los artefactos del setup foundacional que existan en el proyecto:
   - `PRODUCT.md`
   - `ARCHITECTURE.md`
   - `DOMAIN_MODEL.md`
   - `CONVENTIONS.md`
   - `GLOSSARY.md`
   - `PRINCIPLES.md`
   - Specs declaradas en la "Recomendación de dependencias" del output del discovery (primer nivel directo).

4. **Adjuntar como archivos** los artefactos del toolkit que la IA va a usar como guía de redacción:
   - `templates/feature-spec.template.md` (esqueleto que debe llenar).
   - `templates/feature-spec.guide.md` (instrucciones por sección).

   **No pegar template ni guide como texto plano dentro del prompt.** El LLM puede confundirse con los placeholders del template y dejarlos sin reemplazar en el output.

5. Adjuntar (o pegar) el output completo del discovery (Fase 2) como input.

6. Identificar el próximo ID de spec a usar (ver "Asignación de ID" abajo).

7. Antes de pegar el prompt, reemplazar los placeholders `{TOOLKIT-VERSION}` y `{NEXT-SPEC-ID}` con valores reales.

8. Pegar el prompt (solo el bloque delimitado por ` ``` `) y enviar.

### Asignación de ID

Antes de generar la spec, identifico el ID a asignar:

1. Abrir `specs/INDEX.md` del proyecto.
2. Mirar la última fila de la tabla de specs.
3. El próximo ID es `<dominio>-<numero_siguiente>` donde `numero_siguiente` es el correlativo del proyecto (no del dominio), formato 3 dígitos (`001`, `002`, ...).
4. Ejemplo: si la última spec del proyecto es `lotes-007` y la nueva es de dominio "aplicaciones", el próximo ID es `aplicaciones-008`.
5. Reemplazar `{NEXT-SPEC-ID}` en el prompt con el ID asignado.

Si el proyecto es nuevo y no hay `INDEX.md` todavía, crearlo a partir de `templates/project-index.template.md` antes de seguir. La primera spec del proyecto lleva número `001`.

---

## Prompt

```
Necesito que actúes como Redactor en la Fase 3 del ciclo SDD (Spec-Driven Development) siguiendo las reglas que detallo abajo.

CONTEXTO QUE TE PASO:
1. Setup foundacional del proyecto (PRODUCT, ARCHITECTURE, DOMAIN_MODEL, CONVENTIONS, GLOSSARY, PRINCIPLES) — los archivos que existan.
2. Specs dependientes declaradas en la "Recomendación de dependencias" del output del discovery (primer nivel directo).
3. Template del toolkit: feature-spec.template.md (esqueleto de la spec).
4. Guide del toolkit: feature-spec.guide.md (instrucciones por sección).
5. Output del discovery (Fase 2) con respuestas estructuradas por sección.

DATOS QUE TE PASO EXPLÍCITAMENTE:
- Versión del toolkit usado: {TOOLKIT-VERSION}
- ID asignado para esta spec: {NEXT-SPEC-ID}

REGLA FUNDAMENTAL: NO TOMES DECISIONES DE PRODUCTO.

Mis decisiones de producto ya están tomadas durante el discovery. Tu trabajo en esta fase es redactar la spec usando esas decisiones, no tomar decisiones nuevas. Esta regla aplica a todos los pasos del proceso de redacción y al manejo de cualquier gap. Si te encontrás tomando una decisión de producto, parate y avisame (ver "Manejo de gaps" abajo). NO la inscribas en la sección 14 disfrazada de decisión operativa.

PASO 0 — VERIFICACIÓN DE PRE-REQUISITOS:

Antes de redactar, hacé estas dos verificaciones sobre el output del discovery:

Verificación 1 — Sin pendientes:

Buscá todas las apariciones de "[PENDIENTE" en el output del discovery.
Si encontrás CUALQUIER pendiente sin resolver, NO redactes la spec. Devolveme un mensaje con este formato exacto:

"REDACCIÓN BLOQUEADA. El output del discovery contiene N pendientes sin resolver:
1. [Sección X]: [descripción del pendiente]
2. [Sección Y]: [descripción del pendiente]
...
Resolvé estos pendientes en el output del discovery antes de pedirme redactar. Coherente con WORKFLOW.md secciones 2.3 y 5."

Verificación 2 — Decisiones por defecto validadas:

Buscá la sección del output del discovery llamada "Decisiones que tomaste por defecto" (puede tener nombre similar).
Si la sección existe y tiene decisiones listadas, verificá que cada una tenga una nota de validación con uno de estos formatos:
- "Validado por autor: aceptada."
- "Validado por autor: reemplazada por: [descripción]."

Si encontrás decisiones sin nota de validación, NO redactes la spec. Devolveme:

"REDACCIÓN BLOQUEADA. El output del discovery contiene N decisiones tomadas por defecto sin validación explícita del autor:
1. [descripción]
2. [descripción]
...
Validá cada decisión (aceptándola o reemplazándola) en el output del discovery antes de pedirme redactar. Esto evita que la spec se construya sobre decisiones aceptadas por inercia (WORKFLOW.md Regla 2 y zona de riesgo declarada en sección 10.2)."

Verificación 3 — Conversación limpia:

Antes de proceder, hacé al usuario una sola pregunta de confirmación afirmativa:

"Antes de redactar, confirmame: ¿esta conversación es nueva, sin contexto de la sesión de discovery anterior, y adjuntaste todos los artefactos del setup foundacional, template, guide y output del discovery? (sí/no)"

Esperá la respuesta del usuario. Si responde "no", parate y pediles que prepare la conversación correctamente. Si responde "sí", continuá al Paso 1.

Si las tres verificaciones pasan, continuar al Paso 1.

PASO 1 — REDACCIÓN DE LA SPEC:

Redactá la spec completa de una sola vez, llenando las 14 secciones del template (más changelog en sección 15).

Para cada sección:
- Usá la guide (feature-spec.guide.md) para saber qué va y qué no va en esa sección.
- Tomá la información del output del discovery que corresponde a esa sección.
- Adaptala al formato del template.

Regla de adaptación al template:
- Respetá la información del discovery exactamente. No la "mejores", no la sintetices, no la parafrasees creativamente.
- Tu trabajo es traducir formato (pregunta-respuesta → spec narrativa), no interpretar contenido.
- Si una respuesta del discovery es ambigua o admite varias interpretaciones: NO la "aclarés" por tu cuenta. Esto es un gap real (ver "Manejo de gaps" abajo). Parate y avisame.
- Solo tomá decisiones por defecto (sección 14) para asuntos operativos menores: orden de elementos en una lista, formato de tabla, agrupación visual. Nunca para "aclarar" contenido ambiguo del discovery.

Reglas globales de redacción (de la guide):
- Lenguaje preciso. NO uses "podría", "idealmente", "es deseable", "sería bueno". Usá "debe", "es", "tiene".
- Densidad sobre volumen. Si una sección no aplica, escribí "No aplica porque..." con justificación. NO inflar contenido.
- Consistencia con setup foundacional. Si detectás contradicción entre lo que pide el discovery y lo que dice el setup foundacional, NO redactes esa parte y avisame (ver "Manejo de gaps").

Reglas específicas por sección:

- Sección 5 (Requerimientos no funcionales, sub-sección Seguridad): si la feature solo aplica las políticas globales de PRINCIPLES.md sin extender ni diferir, escribí literalmente: "Aplican las políticas de PRINCIPLES.md sin extensiones."

- Sección 6 (Modelo de datos): las entidades deben ser consistentes con DOMAIN_MODEL.md. Si el discovery introduce una entidad nueva que no está en el modelo conceptual, marcala como "candidata a subir a DOMAIN_MODEL.md" en la sección 14 (decisión operativa válida).

- Sección 10 (Decisiones explícitas y trade-offs), sub-sección 10.2 (Decisiones derivadas de pasadas adversarias): escribí literalmente: "Pendiente — sin pasadas adversarias todavía." Esto se completará en Fase 4.

- Sección 13 (Notas de implementación):
  - Si la feature tiene UI compleja (flujos multi-paso, interacciones no triviales, estados visuales relevantes para el negocio), redactá la sección obligatoriamente con foco en comportamiento de interfaz.
  - Si la feature es CRUD simple, integración backend, o sin UI compleja: escribí literalmente "No aplica — feature sin UI compleja. Sección candidata a eliminar en revisión final por el autor."
  - NUNCA elimines la sección por tu cuenta. Esa decisión la toma el autor en Fase 5.

PASO 2 — SECCIÓN 14 (Decisiones tomadas por defecto por la IA):

Esta sección documenta cualquier decisión que hayas tenido que tomar durante la redacción que no estaba explícita en el discovery ni en el setup foundacional.

Reglas:
- Solo decisiones operativas menores: formato, agrupación, terminología neutra, ordenamiento de elementos en una lista, marcar entidad como candidata a DOMAIN_MODEL.
- NUNCA decisiones de producto (ver "Regla fundamental" arriba).
- Por cada decisión:
  - Decisión tomada.
  - Sección de la spec donde aparece.
  - Justificación.
  - Estado: "Pendiente de validación".
- Si no hay decisiones por defecto, escribir literalmente: "Sin decisiones por defecto. Todas las decisiones provienen del discovery o del setup foundacional."

PASO 3 — METADATA Y CHANGELOG:

Completá la sección 1 (Metadata) con:
- ID: {NEXT-SPEC-ID}
- Versión: AAAAMMDD-v1 (la fecha del día de hoy).
- Estado: Draft.
- Autor: Martin Bortagaray.
- Fecha última modificación: timestamp actual.
- Toolkit usado: {TOOLKIT-VERSION}

Completá el changelog (sección 15) con una sola línea: "Versión inicial generada por IA en Fase 3 a partir de discovery de [fecha del discovery]."

MANEJO DE GAPS DURANTE LA REDACCIÓN:

Si durante la redacción descubrís un problema que requiere mi decisión (no solo operativa, sino de producto):

1. Parate y avisame inmediatamente.
2. Mostrame qué descubriste.
3. NO redactes la sección afectada con una decisión inventada.
4. NO inscribas la decisión en sección 14 disfrazada de operativa.
5. Esperá que yo resuelva el gap (puedo decidir ahora, posponer, o pedirte volver a Fase 2 para discovery adicional).

Casos típicos de gaps que requieren mi decisión:
- El discovery dice X pero el setup foundacional dice algo incompatible con X.
- Una sección del template requiere información que el discovery no cubrió.
- El discovery contiene una contradicción interna que recién detectás al redactar.
- Una respuesta del discovery es ambigua y admite varias interpretaciones.
- Detectás que la feature debería partirse en dos.

OUTPUT FINAL:

Generá dos bloques en el mismo mensaje, separados por delimitador visual claro:

Primer bloque — Resumen (5-10 líneas):
- Cuántas secciones efectivamente tienen contenido (vs. cuántas dicen "No aplica").
- Si la sección 14 quedó vacía o tiene decisiones por defecto (cuántas).
- Si detectaste algún punto débil que valga la pena revisar en Fase 4 (hasta 3 puntos críticos).

Segundo bloque — Documento de la spec (markdown completo), precedido por este delimitador exacto:

═══════════════════════════════════════════════
SPEC REDACTADA (copiar solo lo que sigue)
═══════════════════════════════════════════════

El documento debe poder guardarse directamente como archivo `{NEXT-SPEC-ID}.md` en el proyecto, sin necesidad de editar nada.

NO hagas pasada adversaria en este paso. Eso es Fase 4, con otro prompt.

¿Listo? Empezá ejecutando el Paso 0 (las tres verificaciones).
```

---

> **Nota: lo que sigue NO es parte del prompt. Es para mí, no para copiar en la conversación con la IA.**

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

## Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260523-v1 | 2026-05-23 | Versión inicial. |
| 20260523-v2 | 2026-05-23 | Cambios de primera pasada adversaria: alineada nomenclatura "Recomendación de dependencias" con prompt 01 (1.1); aclaración de adjuntar archivos en lugar de pegar texto (2.1); instrucción explícita para sub-sección 10.2 al redactar primer draft (3.2); regla específica para sección 13 con prohibición de eliminar (3.1); verificación 2 en Paso 0 sobre decisiones por defecto del discovery validadas (3.3); regla de adaptación al template sin "mejorar" contenido (4.1); placeholders {TOOLKIT-VERSION} y {NEXT-SPEC-ID} al inicio del prompt (2.2); resumen y documento separados por delimitador visual (5.1); verificación 3 de conversación limpia con confirmación explícita del usuario (6.1); regla fundamental sobre decisiones de producto consolidada al inicio del prompt. Agregado proceso de asignación de ID usando INDEX del proyecto. |
| 20260523-v3 | 2026-05-23 | Quitada referencia a "Modo B" del prompt, ya que es terminología interna del WORKFLOW que la IA no conoce en conversación nueva. Reemplazado por descripción directa de las reglas. El término "Modo B" se mantiene solo en WORKFLOW.md. |
