# WORKFLOW — Mi Proceso de Desarrollo de Software con IA

> **Versión:** 20260520-v3
> **Autor:** Martin Bortagaray
> **Estado:** Approved

---

## 1. Propósito de este documento

Este documento es la guía operativa de mi proceso personal de desarrollo de software asistido por IA, basado en **Spec Driven Development (SDD)** adaptado a mi forma de trabajar.

**Lo uso cuando:**
- Arranco un proyecto nuevo y necesito recordar por dónde empezar.
- Quiero incorporar algo nuevo o modificar algo en mi proceso de desarrollo.
- Necesito consultar cómo encarar una situación concreta (qué hacer si el LLM se desvía, cuándo modificar una spec, etc.).

**Audiencia actual:** yo mismo. Pensado para que en el futuro un socio o colaborador pueda leerlo y entender mi proceso sin que yo se lo explique.

---

## 2. Principios fundacionales

### 2.1 Modo B — Cómo trabajo con la IA

Mi proceso se basa en el **Modo B** de interacción con la IA:

> **Yo doy el input inicial. La IA me hace preguntas. Yo decido. La IA redacta. Yo reviso y adapto.**

No delego decisiones de producto en la IA. Uso la IA como acelerador en redacción, estructura, detección de ambigüedades y generación de código. Las decisiones siguen siendo mías por construcción.

### 2.2 Las 5 reglas no negociables

Estas reglas aplican en todo el proceso. No se relajan por urgencia ni por cansancio.

**Regla 1.** La IA nunca toma decisiones de producto sin preguntarme primero. Si tiene que decidir algo que no le dije, me pregunta. Aunque parezca obvio.

**Regla 2.** La IA marca explícitamente cada decisión que toma por defecto. En cada artefacto generado, hay una sección clara que enumera las decisiones tomadas por defecto, para que yo las valide.

**Regla 3.** Leo la spec entera antes de aprobarla. No "le doy una mirada". Lectura completa, con cabeza fresca.

**Regla 4.** Toda spec aprobada pasa por una pasada adversaria. No se salta ese paso.

**Regla 5.** Si descubro que una spec aprobada estaba mal después de aprobarla, no lo escondo. Subo versión, documento el cambio, entiendo por qué se me escapó.

### 2.3 Principios personales

- **Si dudo dos veces en una decisión, la dejo abierta y consulto** al ingeniero agrónomo, a mi socio, o al experto de dominio que corresponda. No fuerzo una decisión apresurada. **Importante:** estas decisiones abiertas deben resolverse y escribirse en la spec ANTES del paso a estado Approved (ver Fase 5).
- **Prefiero specs cortas y completas a specs largas con detalle innecesario.** Densidad sobre volumen.

### 2.4 Jerarquía de artefactos

Cuando hay un conflicto o algo está mal, la jerarquía para decidir dónde corregir es:

```
Setup foundacional (Product, Architecture, Domain Model, Conventions, Glossary, Principles)
        ↑
        ↑ (gobierna)
        ↑
    Feature Spec
        ↑
        ↑ (gobierna)
        ↑
       Código
```

**Implicancia:** el código nunca contradice a la spec. La spec nunca contradice al setup foundacional. Si el código contradice la spec, se corrige el código. Si la spec necesita contradecir al setup foundacional, se actualiza primero el setup.

### 2.5 Seguridad como preocupación transversal

La seguridad no es una fase ni una capa. Es una preocupación transversal que se aborda en dos lugares complementarios:

1. **`PRINCIPLES.md`** (setup foundacional): políticas de seguridad globales del proyecto (autenticación, autorización, manejo de datos sensibles, logging, validación, manejo de errores).
2. **Feature Specs** (sección de Requerimientos no funcionales): **solo si una feature difiere o extiende las políticas globales**. Si no hay cambios respecto a `PRINCIPLES.md`, la sección se omite.

La verificación de cumplimiento ocurre en el checklist entre capas (sección 6.4) contra `PRINCIPLES.md` directamente, más cualquier extensión específica declarada en la spec.

---

## 3. Roles de la IA en mi proceso

Diferencio cuatro roles. Conviene tenerlos separados en la cabeza y, cuando es posible, en conversaciones distintas dentro de un mismo proyecto.

| Rol | Qué hace | Riesgo |
|-----|----------|--------|
| **Interrogador** | Me hace preguntas para extraer decisiones que no anticipé. | Bajo |
| **Redactor** | Redacta el draft de un artefacto usando mis respuestas, marcando lo que decidió por defecto. | Medio |
| **Adversario** | Lee un artefacto y busca ambigüedades, contradicciones, gaps. | Muy bajo |
| **Generador** | Toma una spec y produce código que la implementa. | Alto |

**Regla operativa:** uso la IA en todos los pasos de mi proceso. No hay tarea de la que la excluya por defecto. Pero pongo más disciplina en el rol Generador, que es donde se concentran los riesgos.

**Organización de conversaciones:** uso varias conversaciones dentro del mismo proyecto de Claude.ai, una por rol activo. Esto evita contaminación de contexto entre tareas (especialmente entre redacción y pasada adversaria).

---

## 4. Setup foundacional de un proyecto nuevo

### 4.1 Artefactos del setup foundacional

Todo proyecto nuevo arranca creando estos seis artefactos, en este orden:

1. **`PRODUCT.md`** — Spec de producto. Qué es, para quién, qué problema resuelve, qué no es.
2. **`ARCHITECTURE.md`** — Stack tecnológico, patrón arquitectónico, capas, restricciones.
3. **`DOMAIN_MODEL.md`** — Entidades core del dominio y sus relaciones principales.
4. **`CONVENTIONS.md`** — Naming, estructura de carpetas, patrones de código, convenciones técnicas.
5. **`GLOSSARY.md`** — Términos del dominio con definición precisa.
6. **`PRINCIPLES.md`** — Principios y políticas transversales (incluye seguridad).

### 4.2 Criterio de "suficientemente completo" para empezar specs

No necesito que los seis artefactos estén completos para empezar a escribir specs de feature. **El setup foundacional es vivo y evoluciona.**

**Mínimo necesario para arrancar la primera spec de feature:**
- `PRODUCT.md`: versión draft con norte y no-objetivos.
- `ARCHITECTURE.md`: stack + patrón arquitectónico base.
- `DOMAIN_MODEL.md`: 4-6 entidades core con sus relaciones principales.

**Los otros tres** (`CONVENTIONS.md`, `GLOSSARY.md`, `PRINCIPLES.md`) pueden empezar como esqueleto vacío (o template base) y se llenan reactivamente:
- Agrego al `GLOSSARY.md` cuando aparece un término que necesita definición.
- Agrego a `CONVENTIONS.md` cuando tomo una decisión técnica que aplica a más de una feature.
- Agrego a `PRINCIPLES.md` cuando defino una política transversal.

**Riesgo a vigilar:** la tentación de "completar todo antes de avanzar". El setup foundacional es base viva, no requisito de perfección anticipada.

### 4.3 Stack base por defecto

Cuando no hay restricciones particulares, mis proyectos usan:

```
Backend: Python + FastAPI + SQLModel
Frontend: Next.js + TypeScript + Tailwind CSS
DB y Auth: Supabase (PostgreSQL managed)
```

**Nota sobre Supabase:** introduce decisión arquitectónica sobre dónde vive la lógica (backend Python vs. RLS/funciones/triggers en Supabase). Esta decisión se documenta explícitamente en `ARCHITECTURE.md` de cada proyecto.

---

## 5. Ciclo SDD por feature

Cada feature pasa por estas seis fases. **Cualquier cambio futuro a una feature implementada vuelve a Fase 1.**

### Fase 1 — Definir necesidad

- Describo el problema o la necesidad en 1-2 líneas.
- Discovery breve: notas crudas sobre restricciones, dependencias con otras specs, decisiones de producto pendientes.

**Output:** descripción corta + notas de discovery.

### Fase 2 — Discovery con IA (Modo B)

- Tiro el problema a la IA con un prompt de discovery.
- La IA me hace preguntas dirigidas (bloque por bloque si son muchas).
- Respondo: decisión concreta / "ayudame a pensarlo" / "no decidido aún" / "no aplica".

**Output:** decisiones tomadas + pendientes explícitos + dependencias identificadas.

### Fase 3 — Draft de spec

- La IA redacta el draft de la spec usando mis respuestas de Fase 2.
- Marca explícitamente cualquier decisión tomada por defecto (Regla 2).
- Marca explícitamente lo pendiente.

**Output:** archivo `feature-XXX.md` en estado Draft.

### Fase 4 — Pasada adversaria + ajustes

- Inicio conversación nueva (contexto limpio).
- Cargo el draft + **todos los archivos del setup foundacional que existan en el proyecto** + las **specs declaradas en la sección "Dependencias" del draft** (solo primer nivel directo; ver sección 6.2).
- La IA en rol Adversario busca ambigüedades, contradicciones internas, gaps, casos borde no cubiertos.
- Resuelvo los puntos identificados.
- La IA redacta versión actualizada con mis resoluciones.
- La spec pasa a estado **Review**.

**Output:** spec en estado Review, lista para aprobación.

### Fase 5 — Aprobación y congelado

- Leo la spec entera, con cabeza fresca (Regla 3).
- **Pre-requisitos obligatorios para pasar a Approved:**
  - No quedan en la spec decisiones marcadas como abiertas, pendientes de consulta, o "TBD".
  - Todas las dudas externas (al agrónomo, socio, expertos de dominio) fueron resueltas y escritas en la spec.
  - La pasada adversaria fue ejecutada al menos una vez (máximo dos veces, ver sección 11).
- **Estado Review es iterativo:** la spec puede permanecer en Review mientras itero ajustes y, si fuera necesario, mientras ejecuto una segunda pasada adversaria. Solo paso a Approved cuando los pre-requisitos están cumplidos y mi lectura crítica de la spec entera es satisfactoria.
- Si paso a **Approved**, registro fecha/hora + versión. La spec queda congelada durante la implementación.

**Señales de que estoy aprobando con criterio (no por inercia):**
- Puedo nombrar las 3 decisiones más importantes de la spec sin releerlas.
- Identifico al menos un trade-off explícito que tomé.
- Sé qué partes son las más débiles y por qué las acepto así.

**Señales de que estoy aprobando por inercia (PARAR):**
- No recuerdo qué decisiones se tomaron.
- "Se ve bien" como única justificación.
- Estoy cansado o apurado.

### Fase 6 — Generación de código por capas + verificación

Cuatro capas, tests intercalados después de cada una:

```
Capa 1 — Modelo de datos + tests
Capa 2 — Lógica de negocio (incluye integraciones) + tests
Capa 3 — API / Capa de acceso + tests
Capa 4 — UI + tests (si aplica)
```

Protocolo detallado en sección 6.

**Output:** código verificado contra spec, commit único con la feature completa.

---

## 6. Generación de código por capas

### 6.1 Modelo de 4 capas con tests intercalados

```
Capa 1 — Modelo de datos
   └── tests de modelo (constraints, relaciones)
Capa 2 — Lógica de negocio
   └── tests de lógica de negocio
Capa 3 — API / Capa de acceso
   └── tests de endpoints
Capa 4 — UI
   └── tests de componentes / e2e (si aplica)
```

**Nota:** el mapeo concreto de cada capa a estructura de código depende de la arquitectura definida en el `ARCHITECTURE.md` del proyecto. Por ejemplo, una arquitectura Next.js + Supabase directo puede mapear "Capa 3 — API" a políticas RLS y funciones de DB en Supabase, no a endpoints FastAPI. Esa decisión vive en `ARCHITECTURE.md`, no en este workflow.

### 6.2 Carga de contexto para cada capa

Para cada capa, cargo en contexto del LLM, en este orden:

1. `CONVENTIONS.md` — reglas de naming y estructura.
2. `ARCHITECTURE.md` — patrón arquitectónico y restricciones.
3. `DOMAIN_MODEL.md` — entidades del dominio.
4. `PRINCIPLES.md` — políticas transversales (especialmente seguridad).
5. `GLOSSARY.md` — términos del dominio.
6. **Feature spec completa** (no por secciones).
7. **Specs declaradas en la sección "Dependencias"** de la spec actual, **solo primer nivel directo**. Si una dependencia transitiva (Feature A depende de B, B depende de C) fuera necesaria, esa información debe estar consolidada en `DOMAIN_MODEL.md` o `ARCHITECTURE.md`, no en la cadena de specs.
8. Código de capas anteriores ya generadas (si aplica).
9. **A partir de Capa 2 inclusive:** schema real actual de la base de datos (migraciones ejecutadas o dump del schema vivo). El modelo conceptual solo no alcanza: el LLM necesita ver los nombres y tipos exactos desplegados para evitar divergencias.

### 6.3 Instrucciones contra los tres saboteos

En cada prompt de generación incluyo:

**Contra código que no cumple spec:**
> "Antes de generar código, generá una tabla comparativa de lo que pide la spec vs. lo que vas a implementar. Si detectás algo de la spec que no podés implementar, detenete y preguntá."

**Contra decisiones implícitas:**
> "Si tenés que tomar una decisión que no está en la spec, listala bajo 'DECISIONES TOMADAS POR DEFECTO' y esperá mi aprobación antes de escribir el código final."

**Contra sobre-ingeniería:**
> "No agregues atributos, validaciones, restricciones, relaciones o capas de abstracción que no estén explícitamente en la spec o requeridos por las convenciones / principios del setup foundacional."

### 6.4 Verificación entre capas

**No paso a la siguiente capa hasta cumplir todo este checklist:**

- [ ] Tabla comparativa Spec vs. Código revisada y consistente.
- [ ] Naming y estructura coinciden con `CONVENTIONS.md`.
- [ ] Entidades usadas coinciden con `DOMAIN_MODEL.md` y schema real (si aplica).
- [ ] Políticas de seguridad de `PRINCIPLES.md` (más extensiones específicas de la spec, si las hay) aplicadas a esta capa.
- [ ] Requerimientos no funcionales relevantes de la spec verificados.
- [ ] Decisiones tomadas por defecto por el LLM revisadas y aprobadas o rechazadas explícitamente.
- [ ] **Pasada adversaria del código realizada** (en conversación separada, usando el prompt `prompts/05-adversarial-code.prompt.md` del toolkit).
- [ ] Hallazgos de la pasada adversaria de código procesados según protocolo de 6.4.1.
- [ ] Tests de esta capa generados, ejecutados y pasan.
- [ ] No hay sobre-ingeniería: todo lo generado tiene justificación en spec o convenciones.

### 6.4.1 Protocolo de hallazgos de pasada adversaria de código

Los hallazgos se clasifican en dos categorías:

- **Bloqueantes:** vulnerabilidades de seguridad, bugs lógicos severos, violaciones a `PRINCIPLES.md`, desvíos directos de la spec. **Exigen corrección inmediata antes de tildar el checklist de la capa.**
- **No bloqueantes:** refactors cosméticos, sugerencias estilísticas, optimizaciones menores. **Se ignoran o se registran como deuda en `DEBT.md`** (sin frenar el avance).

**Caso especial — hallazgo que afecta una capa previa ya verificada:**
Si la pasada adversaria de Capa N encuentra un problema bloqueante en código de una capa anterior (N-1, N-2…) que ya pasó verificación:
- Vuelvo a la capa afectada.
- Corrijo el código.
- Re-verifico el checklist completo de esa capa.
- Recién entonces continúo con la capa actual.

### 6.5 Commits

**Commiteo cuando la feature está completa y verificada**, no capa por capa. Un solo commit por feature, con mensaje que referencia el ID y versión de la spec.

Formato sugerido del mensaje de commit:
```
feat(<id-spec>): <descripción corta>

Implementa <id-spec> versión <YYYYMMDD-vN>.
<descripción breve de qué incluye>
```

---

## 7. Manejo de modificaciones

### 7.1 Regla operativa: ¿dónde corrijo?

Pregunta mental cuando aparece un problema:

> **¿Esto que estoy resolviendo es solo de esta feature, o se repite en otras?**
> - Si es solo de esta feature → modifico spec.
> - Si se repite → modifico setup foundacional.

### 7.2 Iterar código

**Cuándo:**
- Error técnico de implementación (tipo de dato incorrecto, naming wrong, estructura equivocada).
- El LLM se desvía de algo claramente especificado en la spec.

**Cómo:**
- Apunto a la sección específica de la spec que se está violando.
- Pido cambios quirúrgicos, no rehacer.
- Límite: 2 intentos. En el tercero, freno y reviso si el problema es la spec.

### 7.3 Modificar spec

**Cuándo:**
- Después de 2-3 iteraciones, releo la spec y detecto que es ambigua o contradictoria.
- Durante la generación, descubro un requerimiento, caso borde o regla de negocio no contemplada.
- El LLM hace una pregunta razonable que la spec debería haber respondido.

**Cómo:**
- **Freno la generación de código.**
- Modifico la spec.
- **Subo versión** (`YYYYMMDD-vN`).
- Documento qué cambió y por qué.
- Reanudo la generación con la spec nueva en contexto.

### 7.3.1 Caso especial: error estructural descubierto en plena Fase 6

Si durante la generación de código (Fase 6) descubro un error estructural que invalida una spec ya Approved:

1. **La spec retrocede de Approved a Review** con nueva versión (`YYYYMMDD-vN+1`).
2. **Evalúo si las capas previas ya generadas están afectadas** por el cambio:
   - Si **no** están afectadas: mantengo el código generado y continúo desde la capa actual con la nueva versión de spec.
   - Si **sí** están afectadas: reverto solo el código de las capas afectadas (git stash o commit de rollback).
3. **Prohibido continuar generación en la capa actual** hasta haber completado nuevamente Fase 5 sobre la nueva versión de spec.
4. Documento qué cambió y por qué en el changelog de la spec.

### 7.4 Modificar setup foundacional

**Cuándo:**
- El problema afecta a varias specs presentes o futuras.
- Es una decisión arquitectónica, de modelo conceptual, convención técnica o principio.
- Intuición de "esto va a volver a aparecer en otras features".

**Cómo:**
- **Freno la generación.**
- Modifico el artefacto del setup que corresponda.
- Subo versión.
- **Listo las specs en estado `Implemented` que se ven afectadas por el cambio.**
- Para cada spec afectada, decido: la actualizo ahora, o la registro como **deuda explícita** (en un archivo `DEBT.md` o issue en GitHub) para abordar más adelante. La decisión queda documentada.

### 7.5 Regla estricta: spec antes que código

**Siempre actualizo la spec antes de cambiar el código.** No al revés. No "lo arreglo en el código y después documento". Sin excepciones.

### 7.6 Migración de código tras modificación de spec

Cuando una spec aprobada se modifica y hay código generado contra la versión anterior:

- Le paso al LLM la spec nueva + spec anterior + código actual.
- Le pido que actualice el código basándose en el diff entre versiones.
- Verifico contra la spec nueva con el mismo checklist de 6.4.

**Caso especial — migraciones de base de datos:**
Las migraciones de DB son **append-only**. Nunca se editan migraciones ya ejecutadas.

Si una modificación de spec afecta el modelo de datos (cambio de columna, nueva restricción, tabla nueva, etc.):
- Se genera una **nueva migración** que referencia la versión de spec que la requirió.
- La migración nueva **altera** el schema existente (no reescribe la migración vieja).
- El historial de migraciones representa la evolución real de la base de datos.

---

## 8. Versionado

### 8.1 Versionado de specs

**Formato:** `YYYYMMDD-vN`
- `YYYYMMDD`: fecha del cambio (ej: `20260520`).
- `vN`: número correlativo simple (`v1`, `v2`, `v3`...).

**Ejemplo:** `20260520-v1`, `20260603-v2`.

Cada cambio de spec incrementa N. La fecha refleja el último cambio.

### 8.2 Identificación de specs

**Formato del archivo:** `<dominio>-<numero>.md`

**Ejemplos:**
- `lotes-001.md`
- `aplicaciones-002.md`
- `cosechas-003.md`

Los IDs son secuenciales por proyecto, no por dominio.

### 8.3 Versionado del toolkit

El toolkit en sí también se versiona con `YYYYMMDD-vN`.

**Cuándo subir versión del toolkit:**
- Cambio en alguna plantilla del setup foundacional.
- Modificación de este `WORKFLOW.md`.
- Cambio en algún prompt reutilizable.
- Cambio en el protocolo de generación.

Los proyectos creados desde el toolkit guardan referencia a la versión del toolkit que usaron.

### 8.4 Estados de una spec

```
Draft → Review → Approved → Implemented → [Deprecated]
                    ↓
       (Approved → Review si surge error estructural en Fase 6, ver 7.3.1)
```

- **Draft:** en escritura inicial.
- **Review:** iniciada tras la pasada adversaria 1. **Estado iterativo** donde se procesan hallazgos, se ejecuta la pasada adversaria 2 si fuera necesario (ver sección 11), se resuelven decisiones abiertas y se hace lectura crítica final.
- **Approved:** congelada, lista para implementación. Solo se pasa a este estado cuando los pre-requisitos de Fase 5 están cumplidos.
- **Implemented:** ya en código.
- **Deprecated:** la feature fue eliminada o reemplazada.

---

## 9. Herramientas que uso

### 9.1 Asignación de roles a herramientas

| Rol | Herramienta |
|-----|-------------|
| Interrogador | Claude.ai |
| Redactor | Claude.ai |
| Adversario | Claude.ai |
| Generador | Claude Code |

### 9.2 Editor / IDE

**Visual Studio Code** para edición y trabajo con el repo.

### 9.3 Repositorios

- **Toolkit:** template repository en GitHub (`sdd-toolkit`).
- **Proyectos:** repos creados desde el template, uno por proyecto.

### 9.4 Stack técnico base de proyectos

Definido en sección 4.3.

### 9.5 Gestión de specs

En esta versión del workflow, la gestión de specs (estados, versiones, changelogs, dependencias) se mantiene **manualmente** en archivos `.md` en el repo. Es posible que en versiones futuras se incorpore una herramienta de gestión (ej: Notion con sincronización a GitHub) para automatizar el bookkeeping. Esa decisión se tomará después de haber ejecutado al menos una feature completa con flujo manual.

---

## 10. Antipatrones a evitar

### 10.1 Antipatrones generales del proceso SDD

- **Vibe coding:** generar código sin spec previa.
- **Spec retroactiva:** escribir spec después del código.
- **Spec sin actualizar tras cambio de código:** el código y la spec divergen sin que lo note.
- **Saltar la pasada adversaria** por "está chiquita la feature".
- **Modificar spec en pleno desarrollo sin frenar generación.**
- **Aceptar código que "funciona" sin verificar que cumple spec.**
- **Generar todas las capas de una sola vez** en vez de capa por capa con verificación.
- **Mezclar capacidades funcionales** en una sola spec (violación de granularidad).
- **Dejar decisiones implícitas** del LLM sin validar.
- **Sobre-ingeniería silenciosa** que se acumula sin que lo note.
- **Iteración adversaria infinita:** seguir iterando contra hallazgos cada vez más menores en vez de aprobar con criterio (máximo 2 pasadas, ver sección 11).
- **Reabrir decisiones de pasadas adversarias anteriores sin nuevo criterio:** la IA repite hallazgos entre pasadas porque no tiene memoria; mi trabajo es reconocerlos y mantener decisiones cerradas.

### 10.2 Mis zonas de riesgo personales

Estas son mis tendencias específicas. Las nombro explícitamente para vigilarlas activamente:

- **Soy ansioso:** tiendo a querer avanzar rápido y cerrar incomodidad procesando poco.
- **Tendencia a cerrar feedback rápido:** cuando alguien (o yo mismo en relectura) me marca algo, mi reflejo es "ya lo entendí, avancemos" en lugar de procesarlo en profundidad.
- **Sub-especificación de criterios de aceptación y casos borde:** consistentemente los dejo más cortos de lo que deberían.
- **Esquivar decisiones con "es estándar" o "lo definimos después":** cuando una decisión me da incomodidad, tiendo a posponerla.
- **No relectura antes de cerrar:** mando o cierro sin releer.
- **Trabajar cansado y de noche aumenta el riesgo de aprobación apresurada.** No tengo barrera operativa de tiempo entre Fase 4 y Fase 5; la disciplina depende solo de mí. Cuando aparezca un caso de spec mal aprobada por cansancio, activo Regla 5 y revisito esta decisión.

### 10.3 Checklist de auto-check

Antes de aprobar una spec o cerrar una capa de código, recorro esta checklist:

- [ ] **¿Releí completo?** No "le di una mirada".
- [ ] **¿Esquivé alguna decisión?** ¿Hay algún "lo definimos después" o "es estándar" que en realidad necesita decisión ahora?
- [ ] **¿Quedan decisiones abiertas o pendientes de consulta?** Si sí, NO apruebo. Resuelvo primero.
- [ ] **¿Criterios de aceptación y casos borde están suficientemente detallados?** Si me parece que están justos, sumo 50% más.
- [ ] **¿Procesé el feedback recibido o lo cerré rápido?** ¿Estoy aprobando con criterio o con ansiedad?
- [ ] **¿Las decisiones del LLM tomadas por defecto fueron revisadas y validadas explícitamente?**
- [ ] **¿La pasada adversaria se hizo o la salté?**
- [ ] **¿Estoy cansado?** Si sí, el riesgo de aprobación apresurada es mayor. Considero esperar.

Si alguna respuesta es "no" o "no estoy seguro", freno y resuelvo antes de avanzar.

---

## 11. Pasadas adversarias: cuántas veces iterar

La IA en rol Adversario siempre va a encontrar algo. Si itero indefinidamente, nunca apruebo. Las siguientes reglas evitan caer en el loop adversario infinito.

### 11.1 Calidad de los hallazgos, no cantidad

No cuento cuántos hallazgos hay. Evalúo **qué tipo** son.

**Itero si los hallazgos son:**
- Contradicciones internas reales.
- Gaps operativos concretos (situaciones que voy a enfrentar y no están cubiertas).
- Violaciones a las reglas no negociables o al setup foundacional.
- Decisiones implícitas no marcadas.

**NO itero si los hallazgos son:**
- Sugerencias estilísticas o "podría ser mejor".
- Casos teóricos que probablemente no enfrente.
- Sugerencias de sobre-especificación.
- Preferencias del adversario disfrazadas de problemas.

### 11.2 Regla práctica: máximo 2 pasadas adversarias

- **Pasada 1:** sobre el draft (estado Draft). Procesa hallazgos, genera nueva versión, la spec pasa a Review.
- **Pasada 2:** sobre la nueva versión (durante estado Review). Procesa hallazgos serios.
- **Aprobación:** después de pasada 2, la spec pasa a Approved si los pre-requisitos de Fase 5 están cumplidos.

Si la pasada 2 sigue revelando hallazgos estructurales serios, la spec tiene problemas de fondo, no de iteración. Parar y reconsiderar de raíz.

### 11.3 Hallazgos repetidos entre pasadas

**Importante:** la IA en rol Adversario no tiene memoria de pasadas anteriores. Es esperable que en la Pasada 2 vuelvan a aparecer hallazgos ya resueltos en Pasada 1.

**Regla operativa:** los hallazgos repetidos se descartan automáticamente, **salvo que aparezca nuevo criterio** (nueva evidencia, nueva información, cambio en circunstancias) que justifique reabrir la decisión.

Esto previene caer en loop infinito reabriendo en cada pasada las mismas discusiones.

### 11.4 Pregunta de corte

Después de cada pasada adversaria:

> *"Si apruebo esta spec hoy y aparece un problema en la práctica, ¿voy a poder decir que aprobé con criterio o me voy a arrepentir?"*

- Aprobé con criterio, sabía los trade-offs → **apruebo**.
- Me voy a arrepentir, debí haber visto X → **itero una vez más sobre X específicamente**.

### 11.5 Principio de fondo

Las specs no se aprueban porque son perfectas. Se aprueban porque son **suficientemente buenas para el riesgo que asumo**.

Una spec con 3 imperfecciones menores conocidas y documentadas es mejor que una spec sometida a 5 pasadas adversarias buscando perfección.

---

## 12. Cambios a este documento

Este `WORKFLOW.md` evoluciona. Las modificaciones siguen las reglas de versionado de sección 8.3 (toolkit).

**Cuándo lo modifico:**
- Cuando incorporo aprendizaje de un proyecto real.
- Cuando una regla muestra no funcionar en la práctica y necesita ajuste.
- Cuando agrego un principio personal nuevo.
- Cuando cambia mi stack base por defecto.
- Cuando incorporo una nueva herramienta al flujo (ej: gestión de specs en Notion).

**Cómo lo modifico:**
- Edito el documento.
- Incremento versión (`YYYYMMDD-vN`).
- Registro brevemente al final del documento qué cambió.

---

## 13. Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260520-v1 | 2026-05-20 | Versión inicial del documento. |
| 20260520-v2 | 2026-05-20 | Resultados de primera pasada adversaria: Review como estado iterativo (1.1); carga de contexto en pasada adversaria como "todos los archivos existentes del setup" (2.1); specs dependientes como "las declaradas en sección Dependencias" (2.2); protocolo de impacto en specs Implemented al modificar setup (3.1); referencia al prompt de pasada adversaria de código (6.1); nota sobre mapeo de capas dependiente de ARCHITECTURE.md (7.1); prohibición de aprobar con decisiones abiertas (8.1); carga de schema real a partir de Capa 2; nueva sección 11 sobre cuántas veces iterar; nota en zonas de riesgo sobre trabajo nocturno (10.2). |
| 20260520-v3 | 2026-05-20 | Resultados de segunda pasada adversaria: alineación de sección 8.4 con sección 11 sobre estado Review (1.1); restricción de specs dependientes a primer nivel directo (2.2); nueva sub-sección 7.3.1 sobre error estructural descubierto en Fase 6 (rollback de capas afectadas + retorno a Review); nueva sub-sección 6.4.1 con protocolo de hallazgos bloqueantes/no bloqueantes en pasada adversaria de código (6.1); nueva regla en 7.6 sobre migraciones de DB append-only (pregunta crítica final); simplificación de sección 2.5 sobre seguridad (eliminada duplicación en Feature Specs); nueva sub-sección 11.3 sobre hallazgos repetidos entre pasadas; nuevo antipatrón en 10.1 sobre reabrir decisiones cerradas. |
