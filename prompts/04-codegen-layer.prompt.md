# Prompt — Generación de Código por Capas (Fase 6)

> **Versión:** 20260610-v5 · historia en `/CHANGELOG.md`
> **Uso:** Después de que la spec pasó verificación pre-generación (`prompts/06-spec-verification.prompt.md`) con veredicto VERDE o AMARILLO aceptado. Se ejecuta una vez por capa, con contexto incremental.
> **Dónde se ejecuta:** Vía el comando `/sdd-codegen` en Claude Code. La generación escribe los archivos directamente con herramientas (Write/Edit), así que esta fase requiere Claude Code; el camino Claude.ai del modelo híbrido (WORKFLOW.md §11.1) aplica a las fases de pensamiento (1–3), no a la generación.

---

## Cuándo usar este prompt

Este prompt se ejecuta **4 veces por feature**, una por capa:

| Capa | Qué genera | Prerequisito |
|------|-----------|--------------|
| 1 — Modelo de datos | Entidades, schemas, migraciones de DB | Nada (es la primera) |
| 2 — Lógica de negocio | Servicios, reglas de dominio, integraciones | Código de Capa 1 aprobado |
| 3 — API / Capa de acceso | Endpoints, rutas, validaciones de entrada | Código de Capas 1 y 2 aprobados |
| 4 — UI | Componentes, páginas, flujos de interfaz | Código de Capas 1, 2 y 3 aprobados |

**No pasar a la siguiente capa hasta completar el checklist de verificación entre capas** (WORKFLOW.md sección 7.4). El prompt de pasada adversaria de código (`prompts/05-adversarial-code.prompt.md`) se ejecuta después de cada capa, antes de tildar el checklist.

---

## Cómo usar este prompt

1. Verificar que la spec pasó el prompt de verificación pre-generación con veredicto VERDE o AMARILLO aceptado.

2. Abrir conversación nueva (o sesión nueva en Claude Code).

3. **Adjuntar como archivos** (no pegar como texto plano):

   **Siempre:**
   - Spec aprobada (`<spec-id>.md`).
   - `ARCHITECTURE.md`
   - `DOMAIN_MODEL.md`
   - `CONVENTIONS.md`
   - `PRINCIPLES.md`
   - `GLOSSARY.md`
   - Specs declaradas como dependencias en sección 12 (primer nivel directo).

   **A partir de Capa 2:** agregar también:
   - Código generado y aprobado de todas las capas anteriores.
   - Schema real de la base de datos (dump del schema vivo o migraciones ejecutadas).

   **Carga selectiva en modificaciones (hay CHANGE-SET; WORKFLOW.md 8.3.2):** en vez de los 6 documentos foundacionales, cargar según el delta — siempre `CONVENTIONS.md` + `PRINCIPLES.md`; `DOMAIN_MODEL.md` si el delta toca Capa 1 o 2; `ARCHITECTURE.md` si toca Capa 2 o 3 o introduce integraciones; `GLOSSARY.md` solo si el delta introduce términos nuevos; `PRODUCT.md` solo en T3. En builds iniciales se carga todo, como siempre.

4. Reemplazar los placeholders `{CAPA}`, `{NUMERO-CAPA}`, `{SPEC-ID}` y `{SPEC-VERSION}` en el prompt antes de pegar.

5. Pegar el prompt (solo el bloque delimitado por ` ``` `) y enviar.

---

## Prompt

```
Necesito que actúes como Generador de código para la Capa {NUMERO-CAPA} — {CAPA} de la feature {SPEC-ID} versión {SPEC-VERSION}.

CONTEXTO QUE TE PASO:
- Spec aprobada de la feature.
- Setup foundacional del proyecto: ARCHITECTURE, DOMAIN_MODEL, CONVENTIONS, PRINCIPLES, GLOSSARY.
- Specs dependientes declaradas en sección 12 de la spec (primer nivel directo).
[Si es una MODIFICACIÓN agregar: - CHANGE-SET de /sdd-modify-spec (delta ADDED/MODIFIED/REMOVED con capa por ítem y tier en el header). Si NO te paso CHANGE-SET, es un build inicial: generá la capa completa. Si durante la generación detectás que el delta toca modelo de datos, reglas de negocio o seguridad que el tier declarado no admite, PARÁ y avisame: el tier debe subir (válvula de escape, WORKFLOW.md 8.3.2).]
[A partir de Capa 2 agregar: - Código de capas anteriores ya generadas y aprobadas.]
[A partir de Capa 2 agregar: - Schema real de la base de datos (migraciones ejecutadas).]

QUÉ GENERAR EN ESTA CAPA:

Capa 1 — Modelo de datos:
- Definición de entidades con todos sus atributos, tipos y restricciones declarados en sección 6 de la spec.
- Schemas de validación (Pydantic o equivalente según ARCHITECTURE.md).
- Migraciones de base de datos (append-only; nunca modificar migraciones existentes).
- Tests de modelo: constraints, relaciones, validaciones de tipo.

Capa 2 — Lógica de negocio:
- Servicios que implementan los requerimientos funcionales (sección 4) y las reglas de negocio (sección 7).
- Manejo de todos los casos borde declarados en sección 9.
- Integraciones con servicios externos declarados en sección 12.
- Tests de lógica: happy paths, reglas de negocio, casos borde, errores de integración.

Capa 3 — API / Capa de acceso:
- Endpoints o rutas según el patrón arquitectónico de ARCHITECTURE.md.
- Validación de inputs en la capa de entrada.
- Manejo de errores HTTP según criterios de aceptación (sección 8).
- Aplicación de políticas de autenticación y autorización de PRINCIPLES.md.
- Tests de endpoints: status codes, payloads, autenticación, autorización, validaciones.

Capa 4 — UI:
- Componentes y páginas según los flujos descritos en sección 13 (Notas de implementación).
- Estados de carga, error, vacío y éxito para cada flujo.
- Validaciones en cliente declaradas en sección 13.
- Tests de componentes o e2e según criterios de aceptación (sección 8).

REGLAS DE GENERACIÓN:

Regla 1 — La spec es el contrato. Implementá exactamente lo que dice la spec, no lo que "tiene sentido" agregar.

Regla 2 — Tabla comparativa antes del código. Antes de generar el código, generá una tabla con este formato:

| Requerimiento / Criterio en spec | Implementación en esta capa | Estado | Estado en el cambio |
|---|---|---|---|
| [Sección X, ítem Y: texto exacto] | [Dónde y cómo se implementa] | Cubierto / Parcial / No aplica en esta capa | Nuevo / Modificado / Sin cambios — no regenerar / (vacío si es build inicial) |

Si algún requerimiento queda "Parcial", explicá por qué y en qué capa se completa.
Si algún requerimiento no está cubierto en esta capa (aplica a otra), marcalo como "No aplica en esta capa".

La columna "Estado en el cambio" solo aplica cuando esta generación viene de una MODIFICACIÓN (recibiste un CHANGE-SET de `/sdd-modify-spec`). En un build inicial dejala vacía. En una modificación:
- "Nuevo" = ítem ADDED en el CHANGE-SET → generalo.
- "Modificado" = ítem MODIFIED → ajustá el código existente solo en lo que cambió.
- "Sin cambios — no regenerar" = está en la spec pero NO en el CHANGE-SET → NO lo toques. Su código ya existe y aprobado.

Regla 3 — No sobre-ingenieriar. No agregués atributos, validaciones, restricciones, relaciones, endpoints, componentes, capas de abstracción, o patrones que no estén explícitamente en la spec o requeridos por CONVENTIONS.md o PRINCIPLES.md.

Regla 4 — No tomes decisiones de producto. Si durante la generación encontrás algo que la spec no especifica y que requiere una decisión de producto (no solo técnica), parate y avisame. No lo implementés con tu criterio.

Regla 5 — Consistencia con capas anteriores. El código de esta capa debe ser coherente con el código ya generado y aprobado de capas anteriores. Si hay inconsistencia entre lo que las capas anteriores implementaron y lo que la spec pide para esta capa, avisame antes de generar.

Regla 6 — Convenciones siempre. Naming, estructura de carpetas, patrones y estilo según CONVENTIONS.md. Sin excepciones.

Regla 7 — Seguridad transversal. Las políticas de PRINCIPLES.md aplican en todas las capas. No delegues seguridad a "la capa siguiente". Si esta capa maneja datos sensibles, autenticación, o autorización, implementá las políticas correspondientes acá.

Regla 8 — Migraciones append-only (solo Capa 1). Nunca modificar migraciones ya ejecutadas. Si la spec requiere cambios al schema, generá una nueva migración que referencia la versión de spec que la requirió.

Regla 9 — Modificación: regenerá solo el delta, preservá el resto (solo si recibiste un CHANGE-SET). Si esta generación viene de una modificación de spec, recibís un CHANGE-SET con secciones ADDED / MODIFIED / REMOVED y la capa que toca cada ítem. En ese caso:
- Generá o ajustá SOLO los ítems del CHANGE-SET que aplican a esta capa. El código de los requerimientos que NO están en el CHANGE-SET ya existe, está aprobado y revisado: NO lo regenerés ni lo reformatees.
- Para ítems MODIFIED, hacé el cambio quirúrgico sobre el código existente; no reescribas el archivo entero si solo cambia una función.
- Para ítems REMOVED, eliminá el código y los tests correspondientes (en Capa 1, vía nueva migración append-only que dropea, nunca editando una migración corrida).
- Si la capa actual no tiene NINGÚN ítem en el CHANGE-SET, avisame: esta capa no debería regenerarse en este cambio.
- Esta regla NO aplica en builds iniciales (sin CHANGE-SET): ahí sí generás la capa completa.

PASO 0 — ANTES DE GENERAR:

1. Leé la spec completa. Si recibiste un CHANGE-SET (modificación), leelo también e identificá qué ítems de esta capa son ADDED / MODIFIED / REMOVED.
2. Identificá todos los requerimientos funcionales (sección 4), reglas de negocio (sección 7), criterios de aceptación (sección 8) y casos borde (sección 9) que aplican a esta capa.
3. Generá la tabla comparativa (Regla 2) con todos los ítems identificados. En una modificación, completá la columna "Estado en el cambio" para cada fila (Nuevo / Modificado / Sin cambios — no regenerar).
4. Esperá mi confirmación: "tabla ok, generá el código". No generés código hasta que yo confirme la tabla.

PASO 1 — GENERACIÓN DE CÓDIGO:

Después de mi confirmación de la tabla:
- Escribí cada archivo de código y de tests directamente en disco con las herramientas Write/Edit, en la ruta que define CONVENTIONS.md. NO vuelques el contenido de los archivos en el chat.
- Archivos nuevos: usá Write. Archivos existentes (modificación con CHANGE-SET): usá Edit con cambios quirúrgicos, sin reescribir el archivo entero.
- Incluí los tests de la capa (ver "QUÉ GENERAR EN ESTA CAPA"), también escritos en disco.
- Al terminar, reportá solo la lista de archivos creados/modificados (ruta + una línea de qué hace cada uno). El código ya quedó en disco; no lo repitas en el chat.

PASO 2 — DECISIONES IMPLÍCITAS:

Después del código, generá un bloque con este formato exacto:

DECISIONES TÉCNICAS TOMADAS POR DEFECTO
========================================
[Lista numerada de decisiones técnicas que tomaste durante la generación que no estaban explícitas en la spec ni en CONVENTIONS.md. Solo decisiones técnicas operativas (nombre de función, estructura de módulo, tipo de excepción, patrón de manejo de error). NUNCA decisiones de producto.]

Si no tomaste ninguna: escribir "Sin decisiones por defecto. Todo proviene de la spec o de CONVENTIONS.md."

MANEJO DE GAPS DURANTE LA GENERACIÓN:

Si durante la generación encontrás cualquiera de estas situaciones:
1. La spec dice X pero ARCHITECTURE.md o CONVENTIONS.md dice algo incompatible.
2. Un requerimiento de la spec es ambiguo y admite implementaciones distintas con consecuencias reales.
3. Una regla de negocio no es implementable con el stack declarado sin decisión arquitectónica.
4. El código de una capa anterior es inconsistente con lo que la spec pide para esta capa.

Hacé esto:
- PARATE. No implementés con tu criterio.
- Describí el gap encontrado con cita textual de la spec y del documento que entra en conflicto.
- Esperá mi decisión antes de continuar.

Esto es crítico. Un gap ignorado en Capa 1 se propaga a Capa 4. El costo de corregirlo tarde es alto (WORKFLOW.md sección 8.3.1).

¿Listo para empezar? Confirmame que tenés todo el contexto cargado y ejecutá el Paso 0 (tabla comparativa).
```
