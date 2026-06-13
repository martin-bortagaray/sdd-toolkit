# Prompt — Redacción de Setup Foundacional + Roadmap (Fase 0)

> **Versión:** 20260524-v1 · historia en `/CHANGELOG.md`
> **Uso:** Segundo paso de Fase 0 del ciclo SDD. Se ejecuta después del prompt 00-project-discovery y antes del prompt 00c-design-prototype.
> **Dónde se ejecuta:** En conversación nueva dentro del proyecto, con contexto limpio. NO en la misma conversación del discovery inicial.

---

## Pre-requisitos antes de usar este prompt

**El output del discovery inicial NO puede contener pendientes sin resolver NI decisiones por defecto sin validar NI cuestionamientos de viabilidad sin resolver.**

Si el output del prompt 00-project-discovery tiene:
- Cualquier `[PENDIENTE: ...]` sin resolver.
- Cualquier decisión en sección 4 "Decisiones por defecto" sin nota de validación.
- Cualquier cuestionamiento de viabilidad en sección 5 sin resolución.

...este prompt va a rechazar redactar. Eso es deliberado.

Antes de avanzar:

1. Releer el output del discovery inicial.
2. Identificar todos los `[PENDIENTE]`. Para cada uno: resolverlo (decisión propia) o consultar externamente (experto de dominio, socio, validación con usuarios).
3. Identificar la sección 4 "Decisiones que tomaste por defecto". Para cada decisión, agregar nota de validación: "Validado por autor: aceptada." o "Validado por autor: reemplazada por: [decisión propia]."
4. Identificar la sección 5 "Cuestionamientos de viabilidad". Para cada uno, decidir: resolver el problema y actualizar respuestas, aceptar el problema conscientemente y documentarlo como riesgo, o pausar el proyecto si el problema es estructural.
5. Actualizar el output del discovery con todas las resoluciones.
6. **Recién entonces** uso este prompt.

---

## Cómo usar este prompt

1. Verificar pre-requisitos del paso anterior.

2. Abrir conversación nueva en Claude.ai. **No usar la conversación del discovery inicial.**

3. **Adjuntar como archivos** (no pegar como texto plano) los templates del toolkit que la IA va a usar como guía de redacción:
   - `templates/product-spec.template.md`
   - `templates/architecture.template.md`
   - `templates/domain-model.template.md`
   - `templates/conventions.template.md`
   - `templates/glossary.template.md`
   - `templates/principles.template.md`
   - `templates/project-roadmap.template.md`

   **No pegar templates como texto plano dentro del prompt.** El LLM puede confundirse con los placeholders.

4. Adjuntar (o pegar) el output completo del discovery inicial (Paso 1 de Fase 0) como input.

5. Antes de pegar el prompt, reemplazar el placeholder `{TOOLKIT-VERSION}` con valor real.

6. Pegar el prompt (solo el bloque delimitado por ` ``` `) y enviar.

---

## Prompt

```
Necesito que actúes como Redactor en la Fase 0 del ciclo SDD (Spec-Driven Development), paso 2: redacción del setup foundacional + roadmap del proyecto.

CONTEXTO QUE TE PASO:
1. Templates del toolkit: product-spec, architecture, domain-model, conventions, glossary, principles, project-roadmap.
2. Output del discovery inicial del proyecto (Paso 1 de Fase 0) con respuestas estructuradas por 6 bloques temáticos.

DATOS QUE TE PASO EXPLÍCITAMENTE:
- Versión del toolkit usado: {TOOLKIT-VERSION}

REGLA FUNDAMENTAL: NO TOMES DECISIONES DE PRODUCTO, ARQUITECTURA NI DOMINIO.

Las decisiones de fondo ya están tomadas durante el discovery inicial. Tu trabajo en esta fase es redactar los 7 documentos usando esas decisiones, no tomar decisiones nuevas. Esta regla aplica a todos los pasos del proceso. Si te encontrás tomando una decisión de producto, arquitectura o dominio, parate y avisame (ver "Manejo de gaps" abajo). NO la inscribas en "Decisiones tomadas por defecto" disfrazada de decisión operativa.

PASO 0 — VERIFICACIÓN DE PRE-REQUISITOS:

Antes de redactar, hacé estas tres verificaciones sobre el output del discovery inicial:

Verificación 1 — Sin pendientes:

Buscá todas las apariciones de "[PENDIENTE" en el output del discovery.
Si encontrás CUALQUIER pendiente sin resolver, NO redactes el setup foundacional. Devolveme:

"REDACCIÓN BLOQUEADA. El output del discovery inicial contiene N pendientes sin resolver:
1. [Bloque X]: [descripción del pendiente]
2. [Bloque Y]: [descripción del pendiente]
...
Resolvé estos pendientes antes de pedirme redactar. Coherente con WORKFLOW.md secciones 2.3 y 5."

Verificación 2 — Decisiones por defecto validadas:

Buscá la sección 4 del output llamada "Decisiones que tomaste por defecto" (puede tener nombre similar).
Si la sección existe y tiene decisiones listadas, verificá que cada una tenga una nota de validación con uno de estos formatos:
- "Validado por autor: aceptada."
- "Validado por autor: reemplazada por: [descripción]."

Si encontrás decisiones sin nota de validación, NO redactes. Devolveme:

"REDACCIÓN BLOQUEADA. El output del discovery inicial contiene N decisiones tomadas por defecto sin validación explícita del autor:
1. [descripción]
2. [descripción]
...
Validá cada decisión antes de pedirme redactar. Esto evita que el setup foundacional se construya sobre decisiones aceptadas por inercia (WORKFLOW.md Regla 2 y zona de riesgo declarada en sección 10.2)."

Verificación 3 — Cuestionamientos de viabilidad resueltos:

Buscá la sección 5 del output llamada "Cuestionamientos de viabilidad o consistencia".
Si la sección existe y tiene cuestionamientos listados, verificá que cada uno tenga una nota de resolución del autor:
- "Resuelto: [cómo se resolvió]."
- "Aceptado como riesgo: [justificación]."
- "Proyecto pausado." (en este caso no debería estarse ejecutando este prompt)

Si encontrás cuestionamientos sin nota de resolución, NO redactes. Devolveme:

"REDACCIÓN BLOQUEADA. El output del discovery inicial contiene N cuestionamientos de viabilidad sin resolver:
1. [descripción]
2. [descripción]
...
Resolvé cada uno antes de pedirme redactar. Construir un setup foundacional sobre problemas conocidos pero no resueltos significa pagar el costo en cada feature posterior."

Verificación 4 — Conversación limpia:

Antes de proceder, hacé al usuario una sola pregunta de confirmación afirmativa:

"Antes de redactar, confirmame: ¿esta conversación es nueva, sin contexto del discovery inicial anterior, y adjuntaste los 7 templates del setup foundacional + roadmap y el output del discovery? (sí/no)"

Esperá la respuesta. Si responde "no", parate y pediles que prepare la conversación correctamente. Si responde "sí", continuá al Paso 1.

Si las cuatro verificaciones pasan, continuar al Paso 1.

PASO 1 — VERIFICACIÓN DE CONSISTENCIA ENTRE BLOQUES DEL DISCOVERY:

Antes de redactar, leé el output completo del discovery inicial buscando inconsistencias entre bloques.

Ejemplos de inconsistencias a detectar:

- Bloque 1 describe el producto para un perfil de usuario, pero Bloque 2 describe usuarios distintos.
- Bloque 2 declara casos de uso que requieren entidades del dominio no listadas en Bloque 3.
- Bloque 4 declara restricciones técnicas incompatibles con los casos de uso del Bloque 2.
- Bloque 5 lista specs en un orden que no respeta dependencias técnicas implícitas del Bloque 4.
- Bloque 6 declara restricciones de tiempo/presupuesto incompatibles con el alcance del Bloque 5.

Si detectás cualquier inconsistencia significativa entre bloques, NO redactes. Devolveme:

"REDACCIÓN BLOQUEADA. Detecté N inconsistencias entre bloques del discovery:
1. Entre Bloque X y Bloque Y: [descripción concreta de la contradicción con cita textual de ambos bloques].
2. ...
Estas inconsistencias deben resolverse antes de redactar. Una inconsistencia en el discovery se traduce en un setup foundacional con contradicciones internas que va a pagar costos en cada feature posterior."

No avances al Paso 2 hasta que las inconsistencias estén resueltas en el output del discovery.

PASO 2 — REDACCIÓN DE LOS 7 DOCUMENTOS:

Redactá los 7 documentos completos de una sola vez, usando los templates como esqueleto y el output del discovery como contenido.

Los 7 documentos a redactar son:

1. **PRODUCT.md** — usa template `product-spec.template.md`. Información viene principalmente de Bloque 1 (Visión) y Bloque 2 (Usuarios) del discovery.

2. **ARCHITECTURE.md** — usa template `architecture.template.md`. Información viene principalmente de Bloque 4 (Arquitectura) del discovery. La Parte 2 del template (Por qué se eligió esta arquitectura) se llena con las decisiones identificadas y sus alternativas si están en el discovery.

3. **DOMAIN_MODEL.md** — usa template `domain-model.template.md`. Información viene principalmente de Bloque 3 (Dominio) del discovery.

4. **CONVENTIONS.md** — usa template `conventions.template.md`. Si el discovery no cubrió convenciones específicas, redactar las secciones con valores por defecto del stack declarado en Bloque 4, marcándolas como "Decisiones tomadas por defecto" en la sección correspondiente.

5. **GLOSSARY.md** — usa template `glossary.template.md`. Información viene del Bloque 3 (términos del dominio) y de términos específicos que aparecieron en otros bloques.

6. **PRINCIPLES.md** — usa template `principles.template.md`. Información viene principalmente de Bloque 4 (restricciones de seguridad, compliance) y Bloque 6 (restricciones generales) del discovery. Si el discovery no cubrió políticas específicas, redactar con valores por defecto razonables marcándolos como "Decisiones tomadas por defecto".

7. **ROADMAP.md** — usa template `project-roadmap.template.md`. Información viene del Bloque 5 (Roadmap inicial) del discovery, complementada con visión del Bloque 1.

Reglas de redacción:

- Respetá la información del discovery exactamente. No la "mejores", no la sintetices creativamente, no la parafrasees.
- Tu trabajo es traducir formato (de respuestas crudas a documentos estructurados), no interpretar contenido.
- Si una respuesta del discovery es ambigua o admite varias interpretaciones: NO la "aclarés" por tu cuenta. Esto es un gap real (ver "Manejo de gaps" abajo). Parate y avisame.
- Lenguaje preciso. NO uses "podría", "idealmente", "es deseable", "sería bueno". Usá "debe", "es", "tiene".
- Densidad sobre volumen. Si una sección de un template no aplica al proyecto, escribir "No aplica porque..." con justificación. NO inflar contenido.
- Consistencia entre documentos. Las entidades en DOMAIN_MODEL.md deben coincidir con términos del GLOSSARY.md. La arquitectura en ARCHITECTURE.md debe ser compatible con principios de PRINCIPLES.md. El roadmap en ROADMAP.md debe ser consistente con el producto en PRODUCT.md.

Reglas específicas para ROADMAP.md:

- Los IDs de specs en el roadmap son **orientativos**, NO definitivos. Usá identificadores tipo "Spec A1", "Spec A2", "Spec B1" sin formato real de ID (no uses `<DOMINIO>-001`).
- Cuando arranque cada spec real, el ID definitivo se asigna usando el INDEX del proyecto (creado al inicio de Fase 1).
- El roadmap es planificación estratégica, no operativa.

PASO 3 — SECCIÓN "DECISIONES TOMADAS POR DEFECTO":

Al final del output, antes de los 7 documentos, generá una sección llamada "Decisiones tomadas por defecto durante la redacción".

Esta sección documenta cualquier decisión que hayas tenido que tomar durante la redacción que no estaba explícita en el discovery.

Reglas:
- Solo decisiones operativas menores: formato de tabla, agrupación de elementos, terminología neutra, valores por defecto razonables para CONVENTIONS o PRINCIPLES que el discovery no cubrió específicamente.
- NUNCA decisiones de producto, arquitectura o dominio (ver "Regla fundamental" arriba).
- Por cada decisión:
  - Decisión tomada.
  - Documento donde aparece.
  - Justificación.
  - Estado: "Pendiente de validación".
- Si no hay decisiones por defecto, escribir literalmente: "Sin decisiones por defecto. Todo proviene del discovery."

MANEJO DE GAPS DURANTE LA REDACCIÓN:

Si durante la redacción encontrás un problema que requiere mi decisión (no solo operativa, sino de fondo):

1. Parate y avisame inmediatamente.
2. Mostrame qué descubriste.
3. NO redactes el documento afectado con una decisión inventada.
4. NO inscribas la decisión en "Decisiones tomadas por defecto" disfrazada de operativa.
5. Esperá que yo resuelva el gap.

Casos típicos de gaps:
- Una respuesta del discovery es ambigua y admite varias interpretaciones.
- Un template requiere información que el discovery no cubrió.
- Detectás que algo del discovery contradice algo del setup foundacional que estás redactando (a pesar de la verificación de consistencia del Paso 1).

OUTPUT FINAL:

Generá tres bloques en el mismo mensaje, separados por delimitadores visuales claros:

Primer bloque — Resumen ejecutivo (10-15 líneas):
- Nombre del proyecto.
- Cantidad de specs identificadas en el roadmap por fase.
- Tamaño total estimado del proyecto (S/M/L sumados).
- Stack tecnológico declarado.
- Decisiones por defecto tomadas (cantidad).
- Puntos críticos que sugieren revisar antes de aprobar el setup foundacional (hasta 3).

Segundo bloque — Decisiones tomadas por defecto:

═══════════════════════════════════════════════
DECISIONES TOMADAS POR DEFECTO POR LA IA
═══════════════════════════════════════════════

[Lista completa según Paso 3.]

Tercer bloque — Los 7 documentos:

═══════════════════════════════════════════════
SETUP FOUNDACIONAL + ROADMAP
═══════════════════════════════════════════════

Cada documento precedido por su nombre como encabezado:

--- PRODUCT.md ---
[contenido completo]

--- ARCHITECTURE.md ---
[contenido completo]

--- DOMAIN_MODEL.md ---
[contenido completo]

--- CONVENTIONS.md ---
[contenido completo]

--- GLOSSARY.md ---
[contenido completo]

--- PRINCIPLES.md ---
[contenido completo]

--- ROADMAP.md ---
[contenido completo]

Cada documento debe poder guardarse directamente como archivo en el repo del proyecto sin necesidad de editar nada.

NO hagas pasada adversaria en este paso. Si surgen problemas en revisión, vuelvo al discovery o pido cambios quirúrgicos.

¿Listo? Empezá ejecutando el Paso 0 (las cuatro verificaciones).
```
