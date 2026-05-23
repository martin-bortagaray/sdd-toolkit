# Guide — Feature Spec

> **Toolkit:** sdd-toolkit
> **Versión de la guía:** 20260520-v2
> **Propósito:** Documento de referencia para completar `feature-spec.template.md`. Define qué va en cada sección, qué no va, cómo redactar y pregunta guía para verificar suficiencia.
>
> **Audiencias:**
> - **IA en rol Redactor:** consume esta guía junto con el template para redactar specs a partir del discovery (Modo B). El prompt de redacción (`prompts/02-draft-spec.prompt.md`) referencia este documento.
> - **Autor (yo):** consulta esta guía cuando reviso una spec o cuando dudo qué va en una sección.

---

## 1. Metadata

**Qué va:**
- ID: `<dominio>-<numero>` (ej: `LOTES-001`). Secuencial por proyecto, no por dominio.
- Versión: formato `YYYYMMDD-vN`. Cada cambio incrementa N.
- Estado: uno de `Draft / Review / Approved / Implemented / Deprecated`.
- Autor, fecha última modificación, versión del toolkit usado.

**Qué NO va:**
- Historial de cambios extenso (eso va en sección 15).

**Validación:**
- Todos los campos presentes.
- Versión y fecha sincronizadas con el último cambio real.

---

## 2. Contexto y propósito

**Qué va:**
- Por qué existe esta feature.
- Qué problema concreto resuelve.
- A qué objetivo de `PRODUCT.md` responde.
- Contexto del negocio que justifica la existencia (1-2 líneas máximo).

**Qué NO va:**
- Cómo se va a resolver (eso es otras secciones).
- Marketing, justificación inflada, frases de relleno.

**Pregunta guía:**
Si dentro de un año alguien lee solo esta sección, ¿entiende por qué la feature existe y qué pasaría si no existiera?

---

## 3. Usuarios y casos de uso

**Qué va:**
- **Roles:** quiénes interactúan con la feature. Cada rol con definición operativa de qué hace, no solo el nombre.
- **Escenarios principales (happy path):** 2 a 4 escenarios concretos descritos en lenguaje natural.
- **Escenarios secundarios:** casos válidos pero menos frecuentes.
- **No-objetivos:** qué casos NO cubre esta feature explícitamente.

**Qué NO va:**
- Detalle de implementación de cada escenario (eso es criterios de aceptación — sección 8).
- Reglas de UI específicas (sección 13 si aplica, o spec técnica separada).

**Pregunta guía:**
Si una feature nueva quiere usar esta, ¿está claro qué tipos de usuarios y qué casos están cubiertos?

---

## 4. Requerimientos funcionales

**Qué va:**
- Afirmaciones precisas y desambiguadas sobre qué debe hacer el sistema.
- Lista numerada, cada ítem auto-contenido (se entiende sin leer los demás).
- Volumen esperado cuando afecta decisiones (ej: "hasta 5000 registros por usuario").

**Cómo redactar:**

❌ Mal: "El usuario debería poder ver sus lotes."

✅ Bien: "El sistema debe mostrar la lista de lotes del usuario autenticado, ordenados por nombre, paginada de 50 en 50, con búsqueda por nombre y filtros por tipo de tenencia."

**Qué NO va:**
- Lenguaje vago ("podría", "idealmente", "es deseable", "sería bueno").
- Decisiones técnicas de implementación (van implícitas o en spec técnica).

**Pregunta guía:**
¿Hay alguna palabra que un LLM tendría que interpretar para implementar?

---

## 5. Requerimientos no funcionales

**Qué va (pensar cada uno aunque no aplique):**

- **Performance:** tiempos de respuesta esperados, carga esperada, volumen máximo soportado sin degradación.
- **Disponibilidad / offline:** ¿requiere conexión? ¿funciona offline? ¿qué pasa si se pierde conexión durante la operación?
- **Seguridad:** ver regla específica abajo.
- **Internacionalización:** idiomas, formatos de fecha/número, unidades.
- **Otros:** accesibilidad (estándares mínimos), privacidad (retención, regulaciones), compatibilidad (dispositivos, navegadores, OS objetivo).

**Regla específica de seguridad:**
- Si esta feature respeta **todas** las políticas globales de `PRINCIPLES.md` sin extender ni diferir, escribir literalmente: *"Aplican las políticas de PRINCIPLES.md sin extensiones."*
- Si esta feature requiere algo específico (ej: 2FA para operaciones críticas, encriptación adicional, política de retención distinta), documentarlo explícitamente.

**Qué NO va:**
- "TBD" o "a definir". Si no aplica, escribir "No aplica porque..." con justificación.
- Duplicar políticas globales que ya están en `PRINCIPLES.md`.

**Pregunta guía:**
Si esta feature se rompe por una razón NO funcional, ¿está prevista la respuesta del sistema?

---

## 6. Modelo de datos

**Qué va:**
- Entidades involucradas con todos sus atributos finales (no solo los conceptuales).
- Tipos de dato concretos (string, integer, decimal, enum, UUID, timestamp, etc.).
- Restricciones: obligatorio / opcional, único, rangos válidos, longitudes máximas.
- Relaciones con otras entidades, con cardinalidad explícita (1:1, 1:N, N:M, FK).
- Campos de auditoría si aplican (created_at, updated_at, created_by, updated_by).

**Formato sugerido:**

```
Entidad:
  - campo: tipo, restricciones, descripción
  - ...
```

**Consistencia con DOMAIN_MODEL.md:**
- Las entidades core deben ser consistentes con `DOMAIN_MODEL.md`.
- Si esta spec introduce una entidad core nueva al dominio, primero se actualiza `DOMAIN_MODEL.md`.
- Si la spec introduce entidades auxiliares específicas (tabla de auditoría, tabla de relación N:M), pueden vivir solo aquí sin subir al modelo conceptual.

**Qué NO va:**
- Detalles de implementación de DB (índices, particionamiento, optimizaciones de query).
- Decisiones de storage (eso es spec técnica).

**Pregunta guía:**
Si un LLM tuviera que generar las migraciones de base de datos, ¿tiene toda la información que necesita?

---

## 7. Reglas de negocio

**Qué va:**
- Lógica del dominio que NO es obvia desde el modelo de datos.
- Validaciones que cruzan múltiples campos o entidades.
- Restricciones temporales, condicionales, contextuales.
- Cualquier "regla del negocio" que un dev no podría inventar correctamente sin conocer el dominio.

**Ejemplos del estilo:**
- "Un lote no puede darse de baja si tiene operaciones registradas en los últimos 30 días."
- "El total de superficie aplicada no puede superar la superficie del lote."
- "Al editar una entidad, debe quedar registro del cambio en su historial."

**Qué NO va:**
- Reglas obvias ya capturadas en el modelo de datos (ej: "el ID es único" si ya está marcado como PK).
- Reglas de UI (van en sección 13 si aplica, o spec técnica).

**Pregunta guía:**
Si quito esta sección, ¿el LLM podría hacer una implementación que "funcione" pero rompa el negocio?

---

## 8. Criterios de aceptación

**Qué va:**
- Cómo sabemos que la feature está terminada.
- Formato Given/When/Then (Gherkin) o checklist de comportamientos verificables.
- Cada criterio debe ser **verificable**: alguien puede ejecutarlo y decir sí/no.

**Densidad esperada:**
- Feature de complejidad media: 6-10 escenarios.
- Si tenés menos de 5, probablemente está sub-especificado.
- Cubrir: happy path + escenarios secundarios + escenarios de validación + escenarios de error.

**Formato sugerido:**

```
Escenario: [nombre corto descriptivo]
  Dado [precondición]
  Cuando [acción]
  Entonces [resultado esperado]
  Y [resultado adicional si aplica]
```

**Qué NO va:**
- Repetir requerimientos funcionales tal cual (los criterios son verificables, los requerimientos son descriptivos).
- Criterios vagos ("debe ser fácil de usar").

**Pregunta guía:**
¿Podría un tester (o yo mismo) tomar esta lista y decir "esta feature está lista" o "le falta X"?

---

## 9. Casos borde y manejo de errores

**Qué va:**
Casos borde que el sistema debe manejar correctamente. Cada caso documenta:
- Condición que activa el caso.
- Comportamiento esperado del sistema.
- Mensaje al usuario si aplica.

**Taxonomía obligatoria condicional:**

Para cada categoría siguiente, si la condición se cumple en esta feature, **debe haber al menos un caso documentado**. Si no aplica, **debe haber justificación explícita "No aplica porque..."**.

| # | Categoría | Cuándo aplica |
|---|-----------|---------------|
| 1 | **Concurrencia** | Si hay escritura sobre entidad compartida (dos usuarios podrían editar o operar sobre lo mismo). |
| 2 | **Límites numéricos extremos** | Si la feature maneja cantidades, importes, medidas o conteos. |
| 3 | **Inconsistencia de estado** | Si hay flujos de estado (ej: intentar modificar algo en estado Approved o Implemented). |
| 4 | **Falla de integración externa** | Si la feature consume APIs de terceros o servicios externos. |
| 5 | **Datos vacíos o nulos** | Siempre. Toda feature procesa datos. |
| 6 | **Datos malformados / caracteres especiales** | Si hay input de texto libre del usuario. |
| 7 | **Conexión perdida** | Si la feature requiere conexión (cliente, servidor, DB) durante operaciones. |
| 8 | **Token / sesión expirada** | Si la feature requiere autenticación. |
| 9 | **Permisos insuficientes** | Si hay autorización por roles. |
| 10 | **Operación sobre entidad inexistente o borrada** | Siempre. |

**Cómo redactar:**

```
Caso 1 — Concurrencia
  Condición: dos usuarios intentan modificar el mismo lote simultáneamente.
  Comportamiento: el segundo en guardar recibe un error 409 Conflict
                  con el detalle del cambio del primero. La UI ofrece
                  refrescar o sobrescribir.
  Mensaje al usuario: "Este lote fue modificado por otro usuario.
                       Refrescá para ver los cambios."
```

**Qué NO va:**
- Repetir requerimientos no funcionales (esos hablan de expectativa general, esto habla de respuesta concreta del sistema en cada caso).

**Pregunta guía:**
Si un usuario hace algo "raro" (sin mala intención), ¿está definido qué pasa?

---

## 10. Decisiones explícitas y trade-offs

Esta sección tiene **dos sub-secciones**: decisiones del autor y decisiones derivadas de pasadas adversarias.

### 10.1 Decisiones del autor

**Qué va:**
- Decisiones tomadas durante el discovery (Modo B) donde había alternativas válidas.
- Qué se eligió, qué se descartó, qué se gana, qué se pierde.
- Trade-offs aceptados conscientemente.

**Estructura sugerida por decisión:**

- **Decisión:** [qué elegí]
- **Alternativa descartada:** [qué descarté]
- **Por qué:** [razonamiento]
- **Trade-off:** [qué gano / qué pierdo y por qué lo acepto]

**Regla importante:**
Cualquier decisión que aparezca implícitamente en otras secciones debe subir aquí explícitamente con su justificación.

**Señal de sub-especificación:**
Si no hay trade-offs identificados, probablemente no estás tomando decisiones reales. Una feature de complejidad media tiene 2-4 decisiones con trade-offs.

### 10.2 Decisiones derivadas de pasadas adversarias

**Qué va:**
Registro de cada pasada adversaria ejecutada sobre esta spec, y qué hallazgos se resolvieron o descartaron.

**Propósito operativo:**
El adversario en pasada N+1 no tiene memoria de la pasada N. Sin este registro, vuelve a marcar hallazgos ya resueltos. Esta sub-sección le da contexto y evita falsas alarmas.

**Formato:**

| Pasada | Hallazgo | Resolución |
|--------|----------|------------|
| 1 | [Descripción breve del hallazgo] | [Aceptado: descripción del cambio] / [Descartado: razonamiento] / [Modificado: descripción] |

**Si no hubo pasadas adversarias todavía:**
Escribir: *"Pendiente — sin pasadas adversarias todavía."*

**Pregunta guía:**
Si dentro de 6 meses alguien (o yo) pregunta "¿por qué decidiste X y no Y?" o "¿por qué descartaste lo que sugirió el adversario?", ¿está acá la respuesta?

---

## 11. Fuera de alcance

**Qué va:**
- Qué EXPLÍCITAMENTE no hace esta feature.
- Funcionalidades que podrían parecer naturales pero no se incluyen (todavía o nunca).
- Cosas que un LLM podría "agregar de más" pensando que ayuda.

**Ejemplos del estilo:**
- "Esta feature no incluye [X]. Se contempla en spec futura [Y-XXX]."
- "Esta feature no contempla [caso Z]. El productor lo resuelve manualmente fuera del sistema."

**Qué NO va:**
- Cosas obviamente fuera del producto entero.
- Lista exhaustiva de "todo lo que no es esto".

**Pregunta guía:**
¿Le estoy diciendo al LLM "no inventes esto"?

---

## 12. Dependencias y supuestos

**Qué va:**

- **Depende de:** specs que deben existir o estar resueltas para implementar esta. **Solo primer nivel directo.** Si Feature A depende de B, y B depende de C, esta sección lista solo B, no C. (Regla del WORKFLOW.md, sección 6.2.7.)
- **Consumida por:** specs que dependen de esta (consumidores planificados).
- **Supuestos:** asunciones sobre el contexto del producto que se aceptan sin verificar.

**Formato sugerido:**

```
Depende de:
- AUTH-001 (autenticación) — asume usuario autenticado en todos los flujos.
- LOTES-001 (catálogo de lotes) — referencia entidad Lote.

Consumida por:
- APLICACIONES-002, COSECHAS-003 (planificadas).

Supuestos:
- Se asume estructura organizativa plana del usuario (sin multi-empresa).
```

**Qué NO va:**
- Dependencias transitivas (de segundo nivel o más profundo). Esa información, si fuera necesaria, vive consolidada en `DOMAIN_MODEL.md` o `ARCHITECTURE.md`.
- Supuestos no nombrados (esos son el problema).

**Pregunta guía:**
Si esta spec se le diera a alguien que no conoce el resto del sistema, ¿sabría qué necesita estar resuelto antes?

---

## 13. Notas de implementación

Esta sección tiene **dos modos de uso** según el tipo de feature:

### Modo obligatorio — Features con UI compleja

Si la feature tiene UI no trivial (flujos multi-paso, interacciones complejas, estados visuales relevantes para el negocio, drag and drop, gráficos interactivos, etc.), **esta sección es obligatoria** y debe documentar comportamiento de interfaz:

- Flujos visuales paso a paso.
- Estados de carga, error, vacío, éxito.
- Transiciones entre estados o pantallas.
- Validaciones en cliente (qué se valida antes de enviar al servidor).
- Comportamiento en distintos breakpoints (desktop / mobile) si afecta funcionalidad.

**Por qué obligatoria:** sin esto, el LLM en Capa 4 (UI) programa a ciegas basándose solo en los requerimientos funcionales puros, y termina inventando comportamiento.

### Modo opcional — Features sin UI compleja

Para CRUDs simples, features de backend puro, o features sin interfaz compleja, esta sección puede contener pistas técnicas que orientan al LLM Generador sin ser requerimientos:

- Notas sobre patrones específicos del proyecto.
- Pistas sobre cómo se mapean las capas del WORKFLOW para esta feature (especialmente decisiones Supabase / RLS).
- Referencias a librerías específicas si la spec lo requiere.

**Si esta sección queda vacía, eliminarla del documento final.**

**Qué NO va (en ningún modo):**
- Decisiones de producto disfrazadas de notas técnicas (van en sección 10).
- Requerimientos funcionales escondidos aquí (van en sección 4).

---

## 14. Decisiones tomadas por defecto por la IA

**Qué va:**
Lista de decisiones que la IA en rol Redactor tomó por su cuenta porque no estaban explícitas en el discovery con el autor.

**Propósito operativo:**
Permitir al autor revisar rápidamente qué partes de la spec son decisiones suyas y cuáles son inferencias o defaults de la IA. Es barrera contra la Regla 1 del WORKFLOW (la IA nunca decide producto sin preguntar).

**Estructura por decisión:**

- **Decisión:** [qué decidió la IA]
- **Sección de la spec donde aparece:** [ej: sección 6 — Modelo de datos]
- **Justificación de la IA:** [por qué la IA tomó esa decisión por defecto]
- **Estado:** [Pendiente de validación / Validada por autor / Rechazada y reemplazada]

**Regla de la IA en rol Redactor:**
- Si la IA tiene que decidir algo que no está en el discovery, **debe** listarlo aquí.
- No filtrar decisiones por "parecer obvias". Aunque parezca obvio, va.
- La sección no puede quedar incompleta: si la IA tomó 5 decisiones por defecto, las 5 deben estar listadas.

**Si la IA no tomó ninguna decisión por defecto:**
Escribir literalmente: *"Sin decisiones por defecto. Todas las decisiones provienen del discovery con el autor."*

**Regla del autor:**
- El autor revisa esta sección **antes** de que la spec pase a estado Review.
- Cada decisión se valida (mantener), rechaza (reemplazar por decisión propia), o marca como pendiente.
- Una spec no puede pasar a Approved con decisiones por defecto en estado "Pendiente de validación".

---

## 15. Changelog de esta spec

**Qué va:**
- Una línea por cambio de versión relevante.
- Versión, fecha, descripción breve del cambio.

**Formato:**

| Versión | Fecha | Cambios |
|---------|-------|---------|
| YYYYMMDD-v1 | YYYY-MM-DD | Versión inicial. |
| YYYYMMDD-v2 | YYYY-MM-DD | [Resumen breve de cambios.] |

---

## Reglas globales de redacción

Estas reglas aplican a todas las secciones cuando la IA redacta una spec en Modo B:

1. **Decisiones tomadas por defecto.** Si la IA tiene que tomar una decisión que no está en el discovery con el autor, listarla en la sección 14 del documento. No omitir ninguna, aunque parezca obvia.

2. **Decisiones marcadas como pendientes.** Si el autor dijo "no decidido aún" o "ayudame a pensarlo" sobre algún punto durante el discovery, marcarlo en la spec con `[PENDIENTE: descripción de la decisión a tomar]`. La spec con pendientes no puede pasar a Approved (regla del WORKFLOW.md, Fase 5).

3. **Lenguaje preciso.** Evitar "podría", "idealmente", "es deseable", "sería bueno". Usar "debe", "es", "tiene".

4. **Densidad sobre volumen.** Una spec corta y completa es preferible a una larga con relleno. Si una sección no aplica, escribir "No aplica porque..." con justificación, no inflar contenido.

5. **Consistencia con setup foundacional.** Las entidades, términos, principios y decisiones técnicas deben ser consistentes con `DOMAIN_MODEL.md`, `GLOSSARY.md`, `CONVENTIONS.md`, `PRINCIPLES.md` y `ARCHITECTURE.md`. Si la spec necesita contradecir alguno, primero se actualiza el setup foundacional, no se contradice silenciosamente.

---

## Changelog de esta guide

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260520-v1 | 2026-05-20 | Versión inicial. |
| 20260520-v2 | 2026-05-20 | Resultados de primera pasada adversaria: agregada sección 14 dedicada para decisiones por defecto de la IA (hallazgo 1.1); reestructurada sección 10 con sub-secciones 10.1 (decisiones del autor) y 10.2 (decisiones derivadas de pasadas adversarias) (hallazgo 2.1); reemplazado "sumá 50% más" por taxonomía obligatoria condicional de 10 categorías en sección 9 (hallazgo 3.1); modo obligatorio / opcional en sección 13 según complejidad de UI (hallazgo 2.2 zona gris). |
