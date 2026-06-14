# Prompt — Pasada Adversaria de Spec (Fase 4)

> **Versión:** 20260614-v4 · historia en `/CHANGELOG.md`
> **Uso:** Después de Fase 3 (Redacción del draft) y antes de Fase 5 (Aprobación). Es el prompt que ejecuta el rol Adversario de la IA (WORKFLOW.md sección 3) sobre una spec de feature.
> **Dónde se ejecuta:** Vía el comando `/sdd-adversarial-spec` en Claude Code (corre en subagente con contexto limpio), o en conversación nueva en Claude.ai. NUNCA en la conversación donde se redactó la spec (WORKFLOW.md sección 11.1, modelo híbrido v10).

---

## Cuándo usar este prompt

- **Pasada 1:** sobre spec en estado Draft, recién salida de Fase 3. Después de procesar hallazgos, la spec pasa a Review.
- **Pasada 2 — condicional (WORKFLOW.md 13.2, v14):** solo se ejecuta si la Pasada 1 produjo **al menos un hallazgo bloqueante** (contradicción real, gap operativo concreto, violación al setup foundacional, decisión implícita sin marcar). Si la Pasada 1 fue limpia o solo dejó hallazgos descartables/estilísticos, NO hay Pasada 2: se pasa directo a Fase 5.
- **Máximo 2 pasadas** (WORKFLOW.md sección 13.2). Si después de Pasada 2 siguen apareciendo hallazgos estructurales serios, la spec tiene problemas de fondo. Parar y reconsiderar.

**Modificaciones de specs existentes (vienen de `/sdd-modify-spec` con CHANGE-SET y tier, WORKFLOW.md 8.3.2):**

- **Tier T1 (cosmético):** este prompt NO se ejecuta. Excepción codificada de Regla 4: no hay riesgo de diseño que auditar. El riesgo de implementación lo cubren tests + checks inline + gate de prueba manual.
- **Tier T2 (lógica acotada):** se ejecuta en **modo acotado al delta** — la spec completa se lee como contexto de coherencia, pero los hallazgos se reportan solo sobre lo que el delta introduce o toca (ver bloque MODO ACOTADO del prompt). Contexto selectivo según el CHANGE-SET (ver "Cómo usar").
- **Tier T3 (estructural):** pasada completa, igual que una spec nueva.

---

## Cómo usar este prompt

1. Abrir conversación nueva en Claude.ai. **No usar la conversación de redacción ni una conversación previa de pasada adversaria.**

2. **Adjuntar como archivos** (no pegar como texto plano):
   - La spec a revisar (`<spec-id>.md` en su versión actual).
   - Setup foundacional del proyecto que exista: `PRODUCT.md`, `ARCHITECTURE.md`, `DOMAIN_MODEL.md`, `CONVENTIONS.md`, `GLOSSARY.md`, `PRINCIPLES.md`.
   - Specs declaradas en la sección 12 "Dependencias y supuestos" de la spec a revisar (primer nivel directo, no transitivas).
   - `templates/feature-spec.guide.md` del toolkit — **opcional**. Solo si necesitás el detalle de qué va en cada sección. La taxonomía de 10 casos borde que esta pasada audita ya está embebida en la categoría 6 del prompt; no cargues la guide solo por eso.

   **Carga selectiva en modificaciones T2 (WORKFLOW.md 8.3.2):** en vez de los 6 documentos foundacionales, cargar según el CHANGE-SET — siempre `CONVENTIONS.md` + `PRINCIPLES.md`; `DOMAIN_MODEL.md` si el delta toca Capa 1 o 2; `ARCHITECTURE.md` si toca Capa 2 o 3 o introduce integraciones; `GLOSSARY.md` solo si el delta introduce términos nuevos. Adjuntar también el **CHANGE-SET**. En T3 y en specs nuevas se carga todo, como siempre.

3. Identificar si es Pasada 1 o Pasada 2 (el placeholder `{PASADA}` del prompt).

4. Pegar el prompt (solo el bloque delimitado por ` ``` `) y enviar.

---

## Prompt

```
Necesito que actúes como Adversario en la Fase 4 del ciclo SDD (Spec-Driven Development).

CONTEXTO:
Te paso una spec de feature en estado {Draft / Review} para que la revises críticamente. Esta es la Pasada {PASADA} de un máximo de 2 (WORKFLOW.md sección 13.2).

Adjunté también:
- Setup foundacional del proyecto (PRODUCT, ARCHITECTURE, DOMAIN_MODEL, CONVENTIONS, GLOSSARY, PRINCIPLES) — los archivos que existan.
- Specs declaradas como dependencias en la sección 12 de la spec a revisar (primer nivel directo).
- Opcionalmente, la guide del toolkit (feature-spec.guide.md) si necesitás el detalle de qué va en cada sección.

TU TRABAJO:

No es validar la spec ni felicitar lo que está bien. Tu trabajo es encontrar problemas, gaps, ambigüedades, contradicciones, decisiones sin marcar.

ANTES DE GENERAR HALLAZGOS — LECTURA OBLIGATORIA DE SUB-SECCIÓN 10.2:

La spec contiene una sub-sección 10.2 "Decisiones derivadas de pasadas adversarias". Esta sub-sección documenta:
- Qué hallazgos se generaron en pasadas adversarias anteriores.
- Cómo se resolvieron (aceptados, descartados, modificados) y la justificación.

Leé esta sub-sección antes de generar cualquier hallazgo. Si un hallazgo que vas a generar coincide con uno ya resuelto/descartado en pasada anterior, NO lo re-marques.

Excepción: solo re-marques un hallazgo ya cerrado si tenés nuevo criterio basado en información que la decisión anterior no tuvo en cuenta. En ese caso, explicitá cuál es la información nueva.

Esto evita el loop adversario infinito donde cada pasada vuelve a marcar lo mismo (WORKFLOW.md sección 13.3).

MODO ACOTADO AL DELTA (solo si te pasé un CHANGE-SET con Tier T2):

Si esta revisión es sobre una MODIFICACIÓN de una spec existente (te adjunté un CHANGE-SET con tier T2), tu alcance cambia:

- Leé la spec completa como contexto de coherencia, pero reportá SOLO hallazgos que el delta introduce o toca: problemas dentro de los ítems ADDED/MODIFIED/REMOVED, o incoherencias NUEVAS entre el delta y el resto de la spec / el setup foundacional / las dependencias.
- NO reportes problemas pre-existentes de la spec que el delta no toca: esa spec ya fue aprobada con su propia pasada adversaria en su momento. Si encontrás un problema pre-existente grave (contradicción real o riesgo de seguridad), mencionalo en UNA línea al final bajo "FUERA DE SCOPE", sin desarrollarlo.
- Prestá especial atención a la PROPAGACIÓN: ítems del delta que invalidan comportamiento declarado en secciones que el CHANGE-SET no lista (ej: una condición nueva en sección 7 que contradice un criterio de aceptación existente en sección 8). Eso SÍ es hallazgo, y de los importantes.

Si NO te pasé CHANGE-SET (spec nueva o tier T3), ignorá este bloque: la revisión es completa.

LO QUE QUIERO QUE BUSQUES (en orden de prioridad):

1. CONTRADICCIONES INTERNAS
   La spec dice X en una sección y algo incompatible en otra. Citá las dos secciones y el conflicto.

2. CONTRADICCIONES CON SETUP FOUNDACIONAL
   La spec contradice algo de PRODUCT, ARCHITECTURE, DOMAIN_MODEL, CONVENTIONS, GLOSSARY o PRINCIPLES. Citá el documento del setup, el fragmento, y la sección de la spec que lo contradice.

3. CONTRADICCIONES CON SPECS DEPENDIENTES
   La spec contradice una spec aprobada de la que declara depender. Citá la spec dependiente, su fragmento, y la sección de la spec actual que lo contradice.

4. AMBIGÜEDADES EN REQUERIMIENTOS FUNCIONALES
   Lenguaje vago en sección 4: "podría", "idealmente", "es estándar", "lo típico", "el usuario debería poder...". Cualquier requerimiento que un LLM tendría que interpretar para implementar es ambigüedad. Citá el requerimiento exacto.

5. SUB-ESPECIFICACIÓN DE CRITERIOS DE ACEPTACIÓN (sección 8)
   - Menos de 5 escenarios para una feature de complejidad media.
   - Criterios no verificables ("debe ser fácil de usar", "tiene que ser intuitivo").
   - Happy path cubierto pero sin escenarios secundarios o de validación.
   - Criterios que repiten requerimientos funcionales sin agregar verificabilidad.

6. SUB-ESPECIFICACIÓN DE CASOS BORDE (sección 9)
   La guide define una taxonomía obligatoria de 10 categorías de casos borde (concurrencia, límites, inconsistencia de estado, falla externa, datos vacíos, datos malformados, conexión perdida, sesión expirada, permisos, entidad inexistente). Para cada categoría:
   - Si aplica a la feature pero NO está cubierta en la spec: marcalo como sub-especificación crítica.
   - Si la spec dice "No aplica porque..." sin justificación clara: marcalo como justificación débil.

7. DECISIONES IMPLÍCITAS NO MARCADAS EN SECCIÓN 10
   Decisiones que aparecen en el modelo de datos (sección 6), reglas de negocio (sección 7), o flujos descritos en otras secciones, pero que NO están listadas explícitamente en sección 10.1 "Decisiones del autor".
   Ejemplos típicos:
   - Soft delete vs hard delete en una entidad.
   - Decisión de auditoría (qué se loguea, qué no).
   - Estrategia de cache.
   - Multi-tenancy o single-tenancy.

8. MODELO DE DATOS INCOMPLETO O INCONSISTENTE (sección 6)
   - Atributos sin tipo declarado.
   - Restricciones faltantes (obligatorio / opcional, único, longitudes).
   - Relaciones sin cardinalidad explícita.
   - Entidades del DOMAIN_MODEL con atributos divergentes (la spec lista atributos que el modelo conceptual no tiene, o viceversa).
   - Falta de campos de auditoría cuando la naturaleza de la entidad los requeriría.

9. DECISIONES DE LA IA NO VALIDADAS (sección 14)
   La spec tiene sección 14 "Decisiones tomadas por defecto por la IA". Verificar:
   - Si la sección está vacía: la spec debe decir literalmente "Sin decisiones por defecto..." (si solo dice "—" o está en blanco, marcarlo).
   - Si tiene decisiones, verificar que cada una tenga estado "Validada por autor" o "Reemplazada". Si alguna tiene estado "Pendiente de validación", marcarlo como bloqueante para aprobación.

10. DEPENDENCIAS O SUPUESTOS NO DECLARADOS (sección 12)
    La spec usa información de otra spec o asume contexto sin listarlo en sección 12:
    - Referencia entidades que vienen de specs no listadas en "Depende de".
    - Asume comportamiento de auth, roles, permisos sin declararlo como dependencia.
    - Asume contexto del producto que no está en supuestos.

FORMATO DE TU RESPUESTA:

Listá hallazgos agrupados por las 10 categorías, en orden. Para cada categoría:

- Si encontraste hallazgos: numeralos dentro de la categoría (1.1, 1.2, 2.1, 2.2, etc.). Para cada hallazgo:
  - Cita textual del fragmento problemático de la spec, con sección.
  - Cita textual del documento referencia (setup foundacional, spec dependiente, o guide) si aplica.
  - Por qué es un problema.
  - Sugerencia quirúrgica de resolución. NO propongas reescritura completa.

- Reportá SOLO las categorías con hallazgos. Al final, agregá UNA línea que liste por número las categorías que revisaste y quedaron sin hallazgos (ej: "Revisadas sin hallazgos: 2, 3, 8, 9") — constancia de que cubriste las 10 sin gastar un párrafo por categoría vacía.

RESTRICCIONES:

- No felicites nada de la spec. No me digas qué está bien.
- No suavices el lenguaje. Si algo es grave, decilo grave.
- Si dudás si algo es problema, marcalo como "zona gris".
- Tu opinión sobre estilo de redacción sin base en la guide, el setup foundacional o la coherencia interna no cuenta como hallazgo.
- No inventes hallazgos para llenar categorías vacías.
- No re-marques hallazgos ya resueltos en pasadas anteriores (regla de sub-sección 10.2).

CIERRE:

Terminá con UNA pregunta crítica: ¿qué decisión importante sobre esta feature NO está tomada explícitamente y va a aparecer recién cuando empiece la generación de código en Fase 6?
```
