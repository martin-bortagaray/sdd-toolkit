# WORKFLOW — Mi Proceso de Desarrollo de Software con IA

> **Versión:** 20261101-v20 · historia en `/CHANGELOG.md`
> **Autor:** Martin Bortagaray
> **Estado:** Review (pendiente aprobación final)

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

**Regla 1 (v20).** La IA nunca toma una **decisión de producto de alto impacto** sin preguntarme primero. Alto impacto = modelo de datos, reglas de negocio, permisos / seguridad / datos sensibles, dinero o cálculos económicos, contratos externos (integraciones, APIs o formatos que consume otro sistema) y todo lo irreversible o caro de revertir. Las decisiones de **bajo impacto** (textos, orden, defaults de presentación, mensajes, valores de configuración reversibles) las toma con su mejor recomendación y las marca (Regla 2). **Si duda si algo es de alto impacto, pregunta.**

**Regla 2.** La IA marca explícitamente cada decisión que toma por defecto. En cada artefacto generado, hay una sección clara que enumera las decisiones tomadas por defecto, para que yo las valide (en lote). Es la red que hace segura la Regla 1: nada decidido por la IA queda invisible.

**Regla 3 (v20).** Apruebo una spec leyendo **completa su superficie de decisión**: §4 requerimientos funcionales, §6 modelo de datos, §7 reglas de negocio, §8 criterios de aceptación, §10 decisiones y trade-offs, §14 decisiones por defecto (en una modificación, el delta de esas secciones). Lectura completa de esas secciones, con cabeza fresca — no "le doy una mirada". El resto de la spec (contexto, no funcionales, notas, dependencias) lo auditan la revisión y los tests: los criterios de §8 se convierten en tests ejecutables.

**Regla 4 (v20).** Toda spec de **track Estándar o Completo** (§8.3.2) pasa por una revisión adversaria con contexto limpio antes de aprobarse. No se salta ese paso. En **track Rápido** — que por definición no toca modelo de datos, reglas de negocio, seguridad, dinero, contratos externos ni nada irreversible — la reemplaza la revisión de código sobre el diff, más los tests y la prueba manual; la válvula de escape sube el track si aparece riesgo. Para artefactos del toolkit (prompts, templates, protocolos), la pasada adversaria es recomendada pero opcional según criterio del autor: el toolkit evoluciona con la experiencia de uso real, y cuando un artefacto muestre problema en uso real, se itera con Regla 5.

> **Por qué cambiaron las Reglas 1, 3 y 4 (v20):** en uso real, el proceso no era sostenible trabajando fuera de horario. La evidencia externa (benchmark Uvik 2026, críticas de Böckeler/Fowler y Thoughtworks Radar a SDD, BMAD Quick Flow, Kiro Quick Spec) coincide: la ceremonia rinde en cambios con riesgo de diseño y no aporta en cambios chicos; las specs largas generan fatiga de revisión. Las garantías se movieron de "más lectura y más preguntas" a mecanismos que escalan: decisiones marcadas (Regla 2), criterios de aceptación ejecutables, revisión proporcional al riesgo y válvula de escape.

**Regla 5.** Si descubro que una spec aprobada estaba mal después de aprobarla, no lo escondo. Subo versión, documento el cambio, entiendo por qué se me escapó.

### 2.3 Principios personales

- **Si dudo dos veces en una decisión, la dejo abierta y consulto** al ingeniero agrónomo, a mi socio, o al experto de dominio que corresponda. No fuerzo una decisión apresurada. **Importante:** estas decisiones abiertas deben resolverse y escribirse en la spec ANTES del paso a estado Approved (ver Fase 5).
- **Prefiero specs cortas y completas a specs largas con detalle innecesario.** Densidad sobre volumen. Desde v19 es regla de formato ("spec compacta", guide regla global 4): lo que no aplica se omite, y el largo orientativo depende del track (§8.3.2): mini-spec Rápido ≈ ½ página, Estándar ≈ 1-2, Completo ≈ 2-4. Cada línea que no decide nada es tiempo de lectura en la aprobación (Regla 3).

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

La verificación de cumplimiento ocurre en el checklist entre capas (sección 7.4) contra `PRINCIPLES.md` directamente, más cualquier extensión específica declarada en la spec.

### 2.6 Riesgo de validación circular

**Riesgo identificado:** la IA genera la spec (en Modo B con mis respuestas), genera el código a partir de la spec, y verifica el código contra la misma spec. Si la spec capturó mal el requisito del negocio, el código y los tests serán **consistentes entre sí pero incorrectos respecto al problema real**. La pasada adversaria del código pasará porque el código cumple la spec — aunque la spec no captura bien la realidad.

**Por qué este riesgo es mayor en mi caso:**
Trabajo solo. Soy a la vez PM, autor de la spec, y verificador. No hay otro humano que cuestione si el criterio de aceptación capturó la necesidad real.

**Mitigaciones existentes en mi proceso:**
1. Modo B: yo defino los criterios, no la IA. Reduce el riesgo en origen.
2. Pasada adversaria de la spec (Regla 4): cuestiona la spec antes de aprobar.
3. Principio personal de consultar a experto de dominio cuando dudo dos veces (sección 2.3).
4. Pasada adversaria del código tiene límites declarados (sección 7.4.1).

**Lo que estas mitigaciones NO cubren completamente:**
Que el criterio de aceptación, aunque verificable y completo, **capture mal la necesidad real del negocio**. Eso solo lo detectaría un usuario real del producto, no la IA. Por eso ningún proceso SDD reemplaza el contacto con el usuario.

---

## 3. Roles de la IA en mi proceso

Diferencio cuatro roles. Conviene tenerlos separados en la cabeza; el Adversario, además, siempre en contexto separado (subagente).

| Rol | Qué hace | Riesgo |
|-----|----------|--------|
| **Interrogador** | Me hace preguntas para extraer decisiones que no anticipé. | Bajo |
| **Redactor** | Redacta el draft de un artefacto usando mis respuestas, marcando lo que decidió por defecto. | Medio |
| **Adversario** | Lee un artefacto y busca ambigüedades, contradicciones, gaps. | Muy bajo |
| **Generador** | Toma una spec y produce código que la implementa. | Alto |

**Regla operativa:** uso la IA en todos los pasos de mi proceso. No hay tarea de la que la excluya por defecto. Pero pongo más disciplina en el rol Generador, que es donde se concentran los riesgos.

**Organización de conversaciones (v19):** la separación de contexto que importa es la del **Adversario** respecto de quien redactó o generó — y esa la garantiza el subagente con contexto limpio (§11.1), sin que yo cambie de sesión. Interrogador y Redactor pueden ir en la misma sesión (spec-first, §6.0): el sesgo de "completar lo que yo mismo pregunté" lo audita la revisión adversaria. Cambiar de conversación a mano entre roles era fricción sin garantía adicional.

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

### 4.2 Cómo se produce el setup foundacional

**El setup foundacional se produce en Fase 0** (ver sección 5) a través de los prompts `00-project-discovery.prompt.md` y `00b-setup-foundation.prompt.md`. Esos prompts producen los 6 artefactos completos + el `ROADMAP.md` del proyecto en un solo flujo.

**Esto cambia respecto a versiones anteriores del workflow.** En versiones previas, el setup foundacional se llenaba reactivamente arrancando con esqueletos vacíos. En v7, el setup foundacional sale completo de Fase 0.

**Lo que sigue siendo cierto:** el setup foundacional sigue siendo **vivo y evoluciona**. Los 6 artefactos producidos en Fase 0 son la base inicial. A medida que el proyecto avanza, se actualizan reactivamente cuando:
- Aparece un término nuevo que necesita definición precisa (actualiza `GLOSSARY.md`).
- Aparece una decisión técnica que aplica a más de una feature (actualiza `CONVENTIONS.md`).
- Aparece una política transversal nueva (actualiza `PRINCIPLES.md`).
- Aparece un cambio arquitectónico importante (actualiza `ARCHITECTURE.md`).
- Cambia el alcance del producto (actualiza `PRODUCT.md` y posiblemente `ROADMAP.md`).

**Riesgo a vigilar:** la tentación de regenerar el setup foundacional cada vez que algo cambia. Las actualizaciones son **quirúrgicas y reactivas**, no regeneraciones completas.

### 4.3 Stack base por defecto

Cuando no hay restricciones particulares, mis proyectos usan:

```
Backend: Python + FastAPI + SQLModel
Frontend: Next.js + TypeScript + Tailwind CSS
DB y Auth: Supabase (PostgreSQL managed)
```

**Nota sobre Supabase:** introduce decisión arquitectónica sobre dónde vive la lógica (backend Python vs. RLS/funciones/triggers en Supabase). Esta decisión se documenta explícitamente en `ARCHITECTURE.md` de cada proyecto.

---

## 5. Fase 0 — Inicio del proyecto

Fase 0 es el flujo de inicio que se ejecuta **una sola vez por proyecto**, antes del primer ciclo de feature. Produce el setup foundacional completo, el roadmap inicial y un prototipo visual del producto.

### 5.1 Pasos de Fase 0

Tres pasos secuenciales:

**Paso 1 — Discovery inicial del proyecto.**
- Prompt: `00-project-discovery.prompt.md`.
- Input: idea de producto a alto nivel (texto libre del autor).
- Output: documento estructurado por 6 bloques temáticos con decisiones estratégicas crudas.
- Duración esperada: 1-4 horas según tamaño del proyecto.

**Paso 2 — Redacción del setup foundacional + roadmap.**
- Prompt: `00b-setup-foundation.prompt.md`.
- Input: output del Paso 1.
- Output: 7 archivos completos del proyecto (los 6 del setup foundacional + `ROADMAP.md`).
- Pre-requisito: el output del discovery no puede tener pendientes ni decisiones por defecto sin validar ni cuestionamientos de viabilidad sin resolver.

**Paso 3 — Diseño de prototipo UI.**
- Prompt: `00c-design-prototype.prompt.md`.
- Flujo híbrido: brief en Claude.ai + prototipo en Claude Design.
- Output: prototipo navegable de 4-8 pantallas principales.
- Input: setup foundacional completo + design system del autor.

### 5.2 Después de Fase 0

Al terminar los 3 pasos, el autor tiene:
- Repo del proyecto creado con setup foundacional commiteado.
- `INDEX.md` del proyecto creado (de `templates/project-index.template.md`).
- Prototipo guardado en `docs/prototype/` del repo.
- Roadmap con specs orientativas listas para arrancar la primera feature.

El paso siguiente es la **propuesta al cliente** (cotización), que se hace **fuera del SDD**. Ver sección 11.5 para más detalle.

Cuando el cliente aprueba la propuesta, arranca **Fase 1 del ciclo de feature** sobre la primera spec del roadmap.

### 5.3 Cuándo NO ejecutar Fase 0

Fase 0 se ejecuta una sola vez por proyecto. No se vuelve a ejecutar para:

- Nuevas features (esas van por el ciclo de feature, Fase 1).
- Cambios en el setup foundacional (esos se hacen de forma reactiva, ver sección 4.2).
- Refactor del producto (eso requiere decisión explícita de "nuevo proyecto" vs "evolución del proyecto actual").

Si el proyecto cambia tanto que requiere repensar el setup foundacional desde cero, evaluar si es realmente el mismo proyecto. Si lo es, ejecutar Fase 0 nuevamente con versión incrementada. Si no lo es, crear un proyecto nuevo.

### 5.4 Design System del autor

El autor mantiene un **design system propio** en `templates/design-system.template.md` del toolkit. Es transversal a todos los proyectos: define identidad visual, tipografía, componentes base, patrones de UX.

Decisiones del design system del autor (versión actual):
- Tono visual: moderno/minimalista.
- Modo: oscuro como default, claro como variación.
- Color de acento: indigo por defecto, **variable por proyecto** cuando el cliente requiere su marca corporativa.
- Tipografía: Inter (principal) + JetBrains Mono (monoespaciada).
- Componentes: shadcn/ui core + extensiones para SaaS B2B.
- Iconos: Lucide.
- Logo: variable por proyecto.

El design system se carga como contexto en el prompt 00c-design-prototype y en los prompts de generación de UI (Capa 4 del codegen).

---

## 6. Ciclo SDD por feature

Cada feature pasa por estas seis fases. **Cualquier cambio futuro a una feature implementada vuelve a Fase 1.**

### 6.0 Modo Flow — cómo se ejecutan las fases (por defecto desde v19, tracks desde v20)

Las seis fases son el modelo conceptual; **cómo se ejecutan** cambió en v19. Antes, cada fase era un comando que yo invocaba y cada paso intermedio esperaba mi confirmación: una feature nueva de 4 capas recorría ~11 comandos y ~30 interacciones. La mayoría de esas esperas no decidían nada.

El comando `/sdd-feature` orquesta el ciclo completo — para features nuevas **y** modificaciones — y **avanza solo**. Primero clasifica el trabajo en un **track** (§8.3.2: Rápido / Estándar / Completo) y el track define cuántas veces me frena:

| Gate | Qué decido | Rápido | Estándar | Completo |
|------|-----------|:------:|:--------:|:--------:|
| **G1 — Preguntas** | Decisiones de producto de alto impacto (Regla 1), en lote con opciones y recomendación; confirmo el track. | fusionado en un único gate de aprobación | ✔ | ✔ (discovery profundo) |
| **G2 — Aprobación de spec** | Leo la superficie de decisión (Regla 3), valido §14 en lote, apruebo con `leí, apruebo`. Si mis respuestas cambian la spec, veo el diff. | ⤷ | ✔ + plan | ✔ |
| **G3 — Plan único** | Una tabla para todas las capas. | ⤷ | fusionado con G2 | ✔ |
| **G4 — Prueba manual** | Pruebo lo que los tests no cubren y respondo `ok` (autoriza el commit) u `ok push`. | ✔ | ✔ | ✔ |
| **Total de gates** | | **2** | **3** | **4** |

**Interrupciones legítimas** (fuera de los gates): decisión de producto de alto impacto no prevista (Regla 1), válvula de escape de track, conflicto spec vs foundation, tests en rojo tras 2 intentos, semáforo ROJO.

**Cómo funciona:**
- **Spec-first:** la IA redacta la spec de entrada (o el delta, o la mini-spec en Rápido) y cada decisión de alto impacto faltante queda como `[DECIDIR-N]`, que se responde en lote (`prompts/08-spec-first.prompt.md`). Las de bajo impacto las decide y las marca en §14. En track Completo, discovery sección por sección (`/sdd-discovery` → `/sdd-spec`).
- **Revisión unificada** (Estándar y Completo): pasada adversaria + verificación pre-codegen en un solo subagente. Los hallazgos sin decisión de producto se aplican sin esperarme y quedan en §10.2 (y en §14 si definen comportamiento); los que requieren decisión llegan en lote a G2. La pasada 2 (si corresponde por §13.2) corre automáticamente antes de G2. En Rápido no hay revisión de spec (Regla 4): solo checks formales inline.
- **Código en MODO FEATURE:** plan único → tests de §8 primero → capas en orden con **gate automático** (tests + typecheck/build) → **una** revisión de código sobre el diff (§7.4).
- **Bookkeeping automático:** estado de la spec, versión, changelog e INDEX los actualiza el orquestador.
- **Reanudable:** lo que no vive en la spec ni en git (track, plan confirmado, decisiones técnicas acumuladas, estado de la revisión de código) se persiste en un archivo efímero `sdd/specs/<ID>.flow.md`; el orquestador deduce la fase desde ese archivo + spec + rama, y lo borra en el commit.
- **Hallazgos aplicados sin esperarme quedan auditables:** todo arreglo que define comportamiento va a §14 ("Pendiente de validación") y se valida en G2; los descartados quedan listados en una línea cada uno y puedo reabrirlos.

**Lo que no cambia:** la Regla 2 (todo lo decidido por la IA queda marcado), la Regla 5, el gate de prueba manual, la válvula de escape, el máximo de 2 pasadas adversarias. Los comandos por fase siguen disponibles como camino manual.

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
- Cargo el draft + **todos los archivos del setup foundacional que existan en el proyecto** + las **specs declaradas en la sección "Dependencias" del draft** (solo primer nivel directo; ver sección 7.2).
- La IA en rol Adversario busca ambigüedades, contradicciones internas, gaps, casos borde no cubiertos.
- Resuelvo los puntos identificados.
- La IA redacta versión actualizada con mis resoluciones.
- La spec pasa a estado **Review**.

**Output:** spec en estado Review, lista para aprobación.

> En Modo Flow (§6.0) esta pasada corre fusionada con el checklist de verificación pre-codegen (`06-spec-verification`, sin F1/F3) en un solo subagente, antes de G2.

### Fase 5 — Aprobación y congelado

- Leo completa la superficie de decisión de la spec (§4, §6, §7, §8, §10, §14), con cabeza fresca (Regla 3).
- **Pre-requisitos obligatorios para pasar a Approved:**
  - No quedan en la spec decisiones marcadas como abiertas, pendientes de consulta, o "TBD".
  - Todas las dudas externas (al agrónomo, socio, expertos de dominio) fueron resueltas y escritas en la spec.
  - La revisión adversaria fue ejecutada al menos una vez (máximo dos veces, ver sección 13) — en track Estándar y Completo. En track Rápido no corresponde (Regla 4, §8.3.2).
- **Estado Review es iterativo:** la spec puede permanecer en Review mientras itero ajustes y, si fuera necesario, mientras ejecuto una segunda pasada adversaria. Solo paso a Approved cuando los pre-requisitos están cumplidos y mi lectura crítica de la superficie de decisión es satisfactoria.
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

Protocolo detallado en sección 7.

**Output:** código verificado contra spec, **probado manualmente por mí**, commit único con la feature completa.

---

## 7. Generación de código por capas

### 7.1 Modelo de 4 capas con tests intercalados

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

### 7.2 Carga de contexto para cada capa

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

### 7.3 Instrucciones contra los tres saboteos

En cada prompt de generación incluyo:

**Contra código que no cumple spec:**
> "Antes de generar código, generá una tabla comparativa de lo que pide la spec vs. lo que vas a implementar. Si detectás algo de la spec que no podés implementar, detenete y preguntá."

Desde v19 (MODO FEATURE) es **una sola tabla para todas las capas** (con columnas `Capa` y `Test que lo cubre`), confirmada una vez. Los criterios de aceptación de §8 se escriben **primero como tests** que fallan: la spec se vuelve ejecutable y el gate entre capas es automático.

**Contra decisiones implícitas:**
> "Si tenés que tomar una decisión que no está en la spec, listala bajo 'DECISIONES TOMADAS POR DEFECTO' y esperá mi aprobación antes de escribir el código final."

En MODO FEATURE (v19) las decisiones **técnicas** se acumulan durante la generación y se validan en lote en G4, antes del commit (§7.4); una decisión que no sea puramente técnica sigue siendo interrupción inmediata (Regla 1).

**Contra sobre-ingeniería:**
> "No agregues atributos, validaciones, restricciones, relaciones o capas de abstracción que no estén explícitamente en la spec o requeridos por las convenciones / principios del setup foundacional."

### 7.4 Verificación entre capas

**MODO FEATURE (por defecto desde v19):** entre capas el gate es **automático** — tests de la capa + suite previa + typecheck/lint/build en verde; máximo 2 intentos de corrección, al tercero se frena (§8.2). No hay confirmación humana entre capas. El checklist de abajo se verifica **una vez al cierre de la feature**: la pasada adversaria de código corre **una sola vez sobre el diff completo** (no ×4), con contexto = unión de la matriz por capa de `protocols/track-routing.md`, y las decisiones técnicas por defecto acumuladas se validan junto con la prueba manual (G4). Con backend + UI y diff grande, la pasada se parte en dos subagentes en paralelo.

**Red automática recomendada (hook):** en cada proyecto conviene un hook `Stop` de Claude Code que corra tests + typecheck y bloquee el cierre del turno si fallan. Convierte el gate entre capas en una garantía determinista en vez de una instrucción del prompt. Es configuración del proyecto (depende de su comando de tests), no del toolkit.

**MODO CAPA (manual, `/sdd-codegen <ID> <capa>`):** no paso a la siguiente capa hasta cumplir todo este checklist:

- [ ] Tabla comparativa Spec vs. Código revisada y consistente.
- [ ] Naming y estructura coinciden con `CONVENTIONS.md`.
- [ ] Entidades usadas coinciden con `DOMAIN_MODEL.md` y schema real (si aplica).
- [ ] Políticas de seguridad de `PRINCIPLES.md` (más extensiones específicas de la spec, si las hay) aplicadas a esta capa.
- [ ] Requerimientos no funcionales relevantes de la spec verificados.
- [ ] Decisiones tomadas por defecto por el LLM revisadas y aprobadas o rechazadas explícitamente.
- [ ] **Pasada adversaria del código realizada** (en conversación separada, usando el prompt `prompts/05-adversarial-code.prompt.md` del toolkit). **Excepción — track Rápido de pura presentación (sección 8.3.2):** se reemplaza por checks inline en la misma sesión: tests + typecheck/build + revisión del diff contra `CONVENTIONS.md`.
- [ ] Hallazgos de la pasada adversaria de código procesados según protocolo de 7.4.1.
- [ ] Tests de esta capa generados, ejecutados y pasan.
- [ ] No hay sobre-ingeniería: todo lo generado tiene justificación en spec o convenciones.

### 7.4.1 Protocolo de hallazgos de pasada adversaria de código

Los hallazgos se clasifican en dos categorías:

- **Bloqueantes:** vulnerabilidades de seguridad, bugs lógicos severos, violaciones a `PRINCIPLES.md`, desvíos directos de la spec. **Exigen corrección inmediata antes de tildar el checklist de la capa.**
- **No bloqueantes:** refactors cosméticos, sugerencias estilísticas, optimizaciones menores. **Se ignoran o se registran como deuda en `DEBT.md`** (sin frenar el avance).

**Caso especial — hallazgo que afecta una capa previa ya verificada:**
Si la pasada adversaria de Capa N encuentra un problema bloqueante en código de una capa anterior (N-1, N-2…) que ya pasó verificación:
- Vuelvo a la capa afectada.
- Corrijo el código.
- Re-verifico el checklist completo de esa capa.
- Recién entonces continúo con la capa actual.

### 7.4.2 Lo que la pasada adversaria de código NO puede validar

La pasada adversaria del código tiene límites claros. **Es la primera línea de defensa técnica, no la única.**

**El adversario SÍ valida:**
- Que cada criterio de aceptación de la spec tiene un test que lo cubre.
- Que el código no modifica módulos marcados como "sin tocar" en restricciones.
- Que los nombres, patrones y convenciones siguen lo definido en `CONVENTIONS.md` y la spec.
- Que todos los casos de error definidos en la spec tienen manejo explícito en el código.
- Que la estructura de archivos sigue lo definido en el proyecto.

**El adversario NO puede validar (estos riesgos quedan en mi responsabilidad):**
- Que el criterio de aceptación captura correctamente la necesidad real del negocio.
- Que la restricción declarada en la spec era la correcta en primer lugar.
- Que la arquitectura elegida es la más adecuada para el problema.
- Que no existen casos de error que la spec no contemplaba.
- Que el diseño de la spec es técnicamente óptimo.

**Implicancia operativa:**
Pasar la pasada adversaria del código significa que **el código cumple la spec**, no que **la spec es correcta**. Si tengo dudas sobre si la spec captura bien la realidad del negocio, ninguna pasada adversaria de código va a resolverlas. La validación de la spec en sí ocurre antes, en Fase 4, y depende del contacto con el experto de dominio (sección 2.3).

### 7.5 Prueba manual antes del commit (gate)

Los tests automáticos (intercalados por capa, sección 7.4) validan que **el código cumple la spec**. No validan que **la experiencia real sea la esperada** — eso solo lo confirma probar el cambio a mano. Por eso, antes de commitear, hay un gate de prueba manual, **acotado a lo que los tests automáticos no cubren (v20)**:

1. La IA arma un **plan de prueba manual concreto** derivado de los criterios de aceptación (§8) y casos borde (§9) — en una modificación, acotado al delta. El plan separa: (a) los criterios **ya cubiertos por tests automáticos** — se listan con el test que los cubre, **no se repiten a mano**; (b) lo que **se prueba a mano**: experiencia y aspecto visual, integraciones reales, flujos end-to-end no automatizados, datos reales. Siempre incluye al menos **un recorrido del happy path en el entorno real**. Pasos numerados, con datos/precondición y resultado esperado — no instrucciones genéricas.
2. **Pruebo el cambio yo mismo** siguiendo esos pasos.
3. **Solo con mi confirmación explícita de que funciona, se commitea.** Si algo falla, no se commitea: vuelve a iteración de código (sección 8.2) o, si corresponde, se abre un bug.

**Mi `ok` a la prueba manual es también la autorización del commit (v19):** no se vuelve a preguntar por el gate ni por el mensaje (`/sdd-commit` detecta que el gate ya se confirmó en la sesión). `ok push` además pushea la rama.

Este gate vive en el cierre de `/sdd-feature` / `/sdd-codegen` / `/sdd-bugfix`; `/sdd-commit` lo ofrece solo si no se confirmó antes en la sesión. Aplica solo a commits que tocan código; los commits de solo documentación o artefactos del toolkit lo saltan.

### 7.6 Commits

**Commiteo cuando la feature está completa, verificada y probada manualmente**, no capa por capa. Un solo commit por feature, con mensaje que referencia el ID y versión de la spec.

Formato sugerido del mensaje de commit:
```
feat(<id-spec>): <descripción corta>

Implementa <id-spec> versión <YYYYMMDD-vN>.
<descripción breve de qué incluye>
```

---

## 8. Manejo de modificaciones

### 8.1 Regla operativa: ¿dónde corrijo?

Pregunta mental cuando aparece un problema:

> **¿Esto que estoy resolviendo es solo de esta feature, o se repite en otras?**
> - Si es solo de esta feature → modifico spec.
> - Si se repite → modifico setup foundacional.

### 8.2 Iterar código

**Cuándo:**
- Error técnico de implementación (tipo de dato incorrecto, naming wrong, estructura equivocada).
- El LLM se desvía de algo claramente especificado en la spec.

**Cómo:**
- Apunto a la sección específica de la spec que se está violando.
- Pido cambios quirúrgicos, no rehacer.
- Límite: 2 intentos. En el tercero, freno y reviso si el problema es la spec.

### 8.3 Modificar spec

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

**Caso frecuente — agregar/cambiar funcionalidad en una feature ya implementada (o spec as-built):** cuando el cambio es de producto (no un bug) y el sistema hoy se comporta como la spec dice, la modificación re-entra al ciclo acotada al delta y **clasificada por track (sección 8.3.2)**, que determina qué pasos se ejecutan. El camino por defecto es `/sdd-feature <ID> "cambio"`, que usa `prompts/07-modify-spec.prompt.md` (edición quirúrgica de la spec existente + versión + changelog + CHANGE-SET en Estándar/Completo) y luego genera solo las capas afectadas. Para specs as-built, la primera modificación suele revelar huecos de la descripción reverse-engineered: completarlos es parte del cambio (espíritu de Regla 5).

**CHANGE-SET — cómo el codegen sabe que NO debe reconstruir todo.** La modificación produce, además del changelog (prosa, para humanos), un **CHANGE-SET estructurado**: el delta en formato `ADDED / MODIFIED / REMOVED`, con cada ítem etiquetado con la(s) capa(s) que toca. Es la señal que consume `/sdd-codegen` (Regla 9 de `04-codegen-layer.prompt.md`) para regenerar solo los ítems del delta y **preservar el resto del código existente** — en vez de regenerar la capa completa. Capas que no aparecen en el CHANGE-SET no se generan. **Toda modificación lleva CHANGE-SET** (en track Rápido, uno mínimo: ítems + capa, sin prosa). Esto extiende a las capas 2–4 la protección que la Capa 1 ya tenía por las migraciones append-only. Diseño adoptado del modelo de *delta specs* de OpenSpec, adaptado al modelo de spec-única-viva de este proceso (no se crea una carpeta de cambio separada; el CHANGE-SET es efímero y vive durante el cambio).

> **⚠️ Riesgo conocido — propagación entre capas.** El CHANGE-SET acota el scope según el juicio del autor al redactarlo. El punto débil es la **propagación**: un ítem `MODIFIED`/`REMOVED` en una capa puede invalidar código de otra capa que NO figura en el delta (ej: cambio el tipo de un campo en Capa 1 → la lógica de Capa 2 que lo consume queda inconsistente, pero el codegen la marca "Sin cambios — no regenerar" y la deja intacta → **gap silencioso**). Las herramientas grandes (Kiro) lo atacan con cascada automática de dependencias; este proceso lo deja en manos de (a) el autor al etiquetar las capas afectadas por ricochet, no solo las editadas a mano, y (b) el chequeo de propagación del checklist entre capas (`codegen-protocol.md`) y la pasada adversaria de código. **Al modificar, verificá siempre que el CHANGE-SET capture las capas afectadas por propagación, no solo las que tocaste.** Si esto se vuelve recurrente, el siguiente incremento natural es un chequeo en el Paso 0 del codegen: "¿algún ítem 'Sin cambios' depende de un ítem MODIFIED/REMOVED?".

### 8.3.1 Caso especial: error estructural descubierto en plena Fase 6

Si durante la generación de código (Fase 6) descubro un error estructural que invalida una spec ya Approved:

1. **La spec retrocede de Approved a Review** con nueva versión (`YYYYMMDD-vN+1`).
2. **Evalúo si las capas previas ya generadas están afectadas** por el cambio:
   - Si **no** están afectadas: mantengo el código generado y continúo desde la capa actual con la nueva versión de spec.
   - Si **sí** están afectadas: reverto solo el código de las capas afectadas (git stash o commit de rollback).
3. **Prohibido continuar generación en la capa actual** hasta haber completado nuevamente Fase 5 sobre la nueva versión de spec.
4. Documento qué cambió y por qué en el changelog de la spec.

### 8.3.2 Tracks — proporcionalidad del proceso (features y modificaciones, v20)

**Principio:** el costo del proceso debe ser proporcional al radio de daño del trabajo. La sección 9 ya aplica esto a bugs (clasificación A/B/C + flujo por severidad). Desde v20, una **sola clasificación por riesgo** aplica a **todo trabajo** — features nuevas y modificaciones — y reemplaza a los tiers T1/T2/T3 (v14–v19, solo modificaciones) y a los tamaños S/M/L (v19, solo features nuevas). Referencia operativa compacta: `protocols/track-routing.md`.

#### Clasificación

| Track | Criterio objetivo | Ejemplos |
|-------|-------------------|----------|
| **Rápido** | NO toca §6 (modelo de datos), NI §7 (reglas de negocio), NI permisos / seguridad / datos sensibles, NI dinero o cálculos económicos, NI contratos externos, NI nada irreversible, NI un componente compartido o artefacto foundacional (un override local sí califica). Alcance chico: una capacidad, pocos archivos. | Layout, textos, filtro u orden sobre datos existentes, vista de solo lectura, validación de formato. |
| **Estándar** | Toca §6 o §7, o introduce un flujo o una entidad nueva, dentro de una capacidad, sin disparadores de Completo. | Campo nuevo persistido, regla nueva o modificada, entidad nueva simple. |
| **Completo** | Cualquier disparador: permisos / seguridad / datos sensibles, dinero o cálculos económicos, contrato externo nuevo o modificado, operación irreversible sobre datos, o tamaño grande (varias entidades nuevas, >~30 decisiones). Más de una capacidad funcional → proponer partir. | Cambio de permisos, cálculo de precios, integración nueva, migración de datos. |

**Reglas de clasificación:**

- **Si dudo entre dos tracks, es el superior.** Espejo de la regla de bugs ("si dudo entre Tipo A y B, casi siempre es B", sección 9.2).
- La IA propone el track **con justificación contra los criterios objetivos**; yo lo confirmo en el primer gate (Modo B). Un track sin justificación citando los criterios no es una clasificación, es una sensación.
- El track queda registrado en el **changelog de la spec** y, en modificaciones, en el **header del CHANGE-SET**.

#### Qué recorre cada track

| Paso | Rápido | Estándar | Completo |
|------|--------|----------|----------|
| Spec | **Mini-spec** (feature nueva) o **delta** + 1 línea de changelog; CHANGE-SET mínimo | Spec-first en lote · modificación con CHANGE-SET | Discovery profundo · modificación con CHANGE-SET |
| Revisión de spec | **No** (Regla 4) — checks formales inline (verify express) | Revisión unificada (adversaria + verify); acotada al delta en modificaciones | Revisión unificada completa; pasada 2 si la 1 tuvo bloqueantes |
| Gates humanos (§6.0) | 2 | 3 | 4 |
| Codegen | Tests primero + gate automático; solo las capas del delta en modificaciones | Ídem | Ídem |
| Revisión de código | Subagente acotado al diff (checks inline si es solo presentación) | Subagente sobre el diff | Subagente sobre el diff completo (2 en paralelo si es grande) |
| Gate de prueba manual (7.5) | **Sí** | Sí | Sí |
| Commit único | Sí | Sí | Sí |

**Mini-spec (Rápido, feature nueva):** archivo normal en `sdd/specs/` con ID e INDEX, pero solo §1, §2 en dos líneas, §4, §8 (son los tests), §9 aplicable, §14 y §15 (changelog: una línea con versión y track). Si para escribirla hace falta §6 o §7, no es Rápido. El "spec antes que código" (§8.5) se mantiene en todos los tracks: lo que cambia es el tamaño de la spec, no su existencia.

El gate de prueba manual **no se relaja en ningún track**: en Rápido es la red principal junto con la revisión de código, porque el riesgo es de implementación y experiencia, no de diseño.

#### Carga selectiva de contexto

En modificaciones, las revisiones y el codegen cargan los documentos foundacionales según lo que el delta toca, no siempre los 6: siempre `CONVENTIONS.md` + `PRINCIPLES.md`; `DOMAIN_MODEL.md` si toca Capa 1 o 2; `ARCHITECTURE.md` si toca Capa 2 o 3 o integraciones; `GLOSSARY.md` si introduce términos nuevos; `PRODUCT.md` solo en Completo. Las features nuevas Estándar/Completo cargan todo para la revisión de spec y el codegen (sección 7.2). **La revisión de código** corre una vez por feature sobre el diff completo (por capa solo en MODO CAPA) y carga solo el foundation y las secciones de spec que las capas tocadas usan — la unión de las filas de la matriz de `protocols/track-routing.md`. Recargar los 6 documentos completos multiplica el costo sin agregar señal; la independencia de contexto (separación del generador) se conserva igual.

#### Válvula de escape — el track es una hipótesis, no un permiso

Si durante cualquier paso posterior a la clasificación (revisión, codegen, prueba manual) aparece evidencia de que el trabajo toca algo que su track no admite:

1. **El track sube en el acto** (Rápido → Estándar o Estándar → Completo) y se actualiza el header del CHANGE-SET si lo hay.
2. **Se ejecutan los pasos salteados antes de continuar.** Ejemplo: si un Rápido sube a Estándar en pleno codegen, se frena la generación, se completa la spec (secciones que faltan), corre la revisión unificada y se aprueba; recién después se reanuda.
3. La re-clasificación queda registrada en el changelog de la spec, con qué la disparó (espíritu de Regla 5: entender por qué se me escapó).

**Antipatrón a vigilar:** clasificar hacia abajo por ansiedad o cansancio (zona de riesgo personal, sección 12.3). Si el argumento para Rápido es "es chiquito" y no "no toca §6, §7, seguridad, dinero, contratos ni nada irreversible", la clasificación está mal hecha.

### 8.4 Modificar setup foundacional

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

### 8.5 Regla estricta: spec antes que código

**Siempre actualizo la spec antes de cambiar el código.** No al revés. No "lo arreglo en el código y después documento". Sin excepciones.

### 8.6 Migración de código tras modificación de spec

Cuando una spec aprobada se modifica y hay código generado contra la versión anterior:

- Le paso al LLM la spec nueva + spec anterior + código actual.
- Le pido que actualice el código basándose en el diff entre versiones.
- Verifico contra la spec nueva con el mismo checklist de 7.4.

**Caso especial — migraciones de base de datos:**
Las migraciones de DB son **append-only**. Nunca se editan migraciones ya ejecutadas.

Si una modificación de spec afecta el modelo de datos (cambio de columna, nueva restricción, tabla nueva, etc.):
- Se genera una **nueva migración** que referencia la versión de spec que la requirió.
- La migración nueva **altera** el schema existente (no reescribe la migración vieja).
- El historial de migraciones representa la evolución real de la base de datos.

### 8.7 Registro de pendientes diferidos (`DEBT.md`)

Durante una sesión de trabajo aparecen ideas nuevas, deuda técnica y decisiones que conscientemente difiero para otro momento. Para que no se pierdan, cada proyecto tiene un archivo único y acumulativo `sdd/DEBT.md` (generado desde `templates/debt.template.md`).

**Regla de captura — "lo dejo registrado" obliga a una escritura.** No es una frase conversacional: si algo se difiere, queda como entrada concreta en `DEBT.md`. Si no quedó en el archivo, no quedó registrado. La forma operativa de cumplir esto es el comando `/sdd-defer`.

**Qué va a `DEBT.md`** (tres tipos):
- `deuda-tecnica`: hallazgos NO bloqueantes de pasadas adversarias (7.4.1), refactors postergados, specs `Implemented` afectadas por un cambio de setup que no corrijo de inmediato (8.4).
- `idea-producto`: funcionalidad nueva charlada a mitad de sesión y diferida. Su destino natural es el `ROADMAP.md` o el ciclo SDD vía discovery.
- `decision-diferida`: una decisión que posterga para tomar con más contexto.

**Qué NO va a `DEBT.md`:** bugs (→ `bugfix-NNN.md`, sección 9), hallazgos **bloqueantes** (se corrigen en el momento), features ya planificadas (→ `ROADMAP.md`), exclusiones de alcance de una feature (→ sección 11 de la spec).

**Ciclo de vida de una entrada:** `Abierto` → `Promovido` (a spec / roadmap / bugfix, anotando destino) | `Resuelto` | `Descartado` (anotando por qué). El estado de cada entrada se mantiene al día con la revisión periódica `/sdd-debt-review`, que recorre el registro, propone el estado nuevo de cada pendiente con evidencia del repo y sincroniza la tabla de índice. Las referencias a `DEBT.md` en 7.4.1 y 8.4 apuntan a este registro.

---

## 9. Tratamiento de Bugs

### 9.1 Principio fundamental

Un bug no interrumpe la regla de "spec antes que código". Lo que cambia es la velocidad y la forma del artefacto. La trazabilidad no se negocia ni bajo presión.

### 9.2 Clasificación obligatoria: primer paso siempre

Antes de tocar una línea de código, clasifico el bug en uno de tres tipos. La clasificación determina qué corrijo y dónde.

| Tipo | Definición | Qué corrijo |
|------|-----------|-------------|
| **Tipo A — Fallo de implementación** | El código no cumple lo que la spec dice explícitamente. La spec estaba bien. | Solo el código. La spec no cambia. |
| **Tipo B — Fallo de spec** | La spec no contempló el caso, era ambigua, o modeló mal el comportamiento. El código hizo lo que la spec decía. | Primero la spec (nueva versión). Luego el código. |
| **Tipo C — Cambio de negocio** | El sistema se comporta exactamente como la spec dice, pero el negocio cambió de opinión. | No es un bug. Es una feature nueva. Se trata con el ciclo SDD completo. |

**Señal de alerta:** si dudo entre Tipo A y Tipo B, casi siempre es Tipo B. La ambigüedad en la spec es la causa más frecuente de bugs.

### 9.3 Artefacto bugfix-XXX.md

Todo bug queda trazado. **Desde v20 el artefacto `bugfix-XXX.md` es obligatorio solo cuando amerita:**

- **Tipo B** (la spec cambia), o
- **Severidad Crítica o Alta**, o
- **Root cause no obvio** (requirió investigación, o puede reaparecer en otra forma).

**Fuera de esos casos** (Tipo A, severidad Media/Baja, causa clara), la trazabilidad es el **test de regresión + un commit `fix(<spec-id>): …`** cuyo cuerpo registra observado vs esperado, causa y nombre del test. Si durante el fix la causa resulta no obvia o aparece que es Tipo B, se crea el artefacto en el acto (válvula de escape).

**Formato del archivo:** `bugfix-<numero>.md`
- Numeración secuencial por proyecto, reinicia en cada proyecto.
- Ejemplos: `bugfix-001.md`, `bugfix-002.md`.

**Ciclo de vida del artefacto:**

```
Abierto → En fix → Cerrado
```

- **Abierto:** bug identificado y clasificado.
- **En fix:** spec actualizada (si Tipo B), código en corrección, test de regresión escrito.
- **Cerrado:** fix verificado, test de regresión pasando, spec original actualizada si correspondía.

**Estructura del artefacto:**

```markdown
# bugfix-XXX — [Título corto del bug]
**Versión:** YYYYMMDD-v1
**Estado:** Abierto | En fix | Cerrado
**Severidad:** Crítico | Alto | Medio | Bajo
**Tipo:** A (implementación) | B (spec) | C (negocio → reclasificar como feature)
**Spec afectada:** [nombre-spec.md versión YYYYMMDD-vN]

## Descripción del bug
[Qué ocurre. Comportamiento observado vs. comportamiento esperado.]

## Reproducción
[Pasos mínimos para reproducir. Sin ambigüedad.]

## Root cause
[Causa raíz identificada: dónde y por qué falló.]

## Criterio de aceptación del fix
[Cómo verifico que el bug está corregido. Redactado como criterio testeable.]

## Test de regresión
[Descripción del test que se agrega a la suite. El test debe fallar antes del fix y pasar después.]

## Cambios en spec original
[Solo si Tipo B. Qué sección se modifica y por qué. Nueva versión de la spec.]

## Decisiones tomadas
[Cualquier decisión no obvia que tomé al resolver el bug.]
```

### 9.4 Flujo por severidad

#### Severidad Crítica — producción caída o dato corrupto

La única situación donde el fix puede preceder al artefacto completo, con condiciones estrictas.

1. **Fix mínimo:** el cambio más pequeño posible que restaura funcionamiento. Sin refactoring, sin mejoras aprovechando el momento.
2. **Deuda técnica registrada:** ese mismo día, antes de cerrar la sesión, creo el `bugfix-XXX.md` con estado **Abierto** y el campo de root cause como pendiente explícito.
3. **Completar el artefacto:** en las próximas 24 horas, completo la clasificación, el root cause, el criterio de aceptación y el test de regresión.
4. **Actualizar spec si es Tipo B:** en la sesión siguiente, la spec original recibe su nueva versión.

**Regla personal:** dado que soy ansioso y tiendo a no volver sobre cosas "ya resueltas", el `bugfix-XXX.md` en estado Abierto es mi mecanismo de compromiso. No cierro el bug hasta que el artefacto esté completo y el test de regresión esté en la suite.

#### Severidad Alta — funcionalidad rota, workaround posible

Proceso completo sin atajos:

1. Clasifico el tipo.
2. Creo `bugfix-XXX.md` con la estructura completa.
3. Si es Tipo B: actualizo la spec original (nueva versión) antes de tocar código.
4. Escribo el test de regresión (debe fallar).
5. Genero el fix con la IA, pasando el `bugfix-XXX.md` como contexto.
6. Verifico que el test de regresión pasa.
7. **Pruebo manualmente:** reproduzco el caso original del bug y confirmo que ya no ocurre (el test de regresión automático no reemplaza esta verificación en la experiencia real).
8. Cierro el `bugfix-XXX.md` y commiteo con `/sdd-commit`.

#### Severidad Media / Baja

Tipo B o causa no obvia: idéntico a Alta, sin urgencia de tiempo. Tipo A con causa clara: test de regresión (debe fallar) → fix mínimo → test en verde → prueba manual acotada (§7.5) → commit `fix(<spec-id>):` con observado/esperado, causa y test en el cuerpo. Sin `bugfix-XXX.md`.

### 9.5 Protocolo de generación del fix con IA

El prompt de generación del fix siempre incluye:
- El `bugfix-XXX.md` completo (o, sin artefacto, la descripción observado/esperado + causa).
- La spec afectada (versión actualizada si Tipo B, versión original si Tipo A).
- El setup foundacional relevante (`CONVENTIONS.md`, `ARCHITECTURE.md`).
- El código actual del módulo afectado.

Instrucción explícita contra sobre-ingeniería:

> "Generá el fix mínimo que resuelve el bug descrito. No refactorices, no mejores, no agregues nada que no esté en el bugfix spec. Si detectás algo fuera del scope del bug que debería corregirse, listalo como observación separada."

### 9.6 Test de regresión y prueba manual: regla de cierre

**Un bug no está cerrado hasta que el test de regresión existe y pasa, y yo confirmé a mano que el bug ya no ocurre** — reproduciendo el caso original en el entorno real cuando el test de regresión no ejercita ese camino real (UI, integración, datos reales); si el test ya lo ejercita de punta a punta, alcanza con el recorrido mínimo de §7.5.

El test de regresión:
- Se escribe antes del fix (debe fallar con el código actual).
- Reproduce el caso exacto que falló en producción.
- Se incorpora a la suite de tests existente de la feature afectada.
- Se referencia en el `bugfix-XXX.md` (o en el cuerpo del commit `fix:` si no hay artefacto) con el nombre del test y el archivo.

### 9.7 Impacto en specs existentes

| Tipo de bug | Spec original | Acción |
|-------------|--------------|--------|
| Tipo A | No cambia | El test de regresión se incorpora a la suite existente |
| Tipo B | Nueva versión | Se sube versión, se documenta el cambio en el changelog de la spec |
| Tipo C | No cambia | Se abre nueva spec de feature con el ciclo completo |

**Regla:** nunca edito una spec archivada sin subirle versión. El historial es la trazabilidad.

---

## 10. Versionado

### 10.1 Versionado de specs

**Formato:** `YYYYMMDD-vN`
- `YYYYMMDD`: fecha del cambio (ej: `20260520`).
- `vN`: número correlativo simple (`v1`, `v2`, `v3`...).

**Ejemplo:** `20260520-v1`, `20260603-v2`.

Cada cambio de spec incrementa N. La fecha refleja el último cambio.

### 10.2 Identificación de specs

**Formato del archivo:** `<dominio>-<numero>.md`

**Ejemplos:**
- `lotes-001.md`
- `aplicaciones-002.md`
- `cosechas-003.md`

Los IDs son secuenciales por proyecto, no por dominio.

### 10.3 Versionado del toolkit

El toolkit en sí también se versiona con `YYYYMMDD-vN`.

**Cuándo subir versión del toolkit:**
- Cambio en alguna plantilla del setup foundacional.
- Modificación de este `WORKFLOW.md`.
- Cambio en algún prompt reutilizable.
- Cambio en el protocolo de generación.

Los proyectos creados desde el toolkit guardan referencia a la versión del toolkit que usaron.

### 10.4 Estados de una spec

```
Draft → Review → Approved → Implemented → [Deprecated]
                    ↓
       (Approved → Review si surge error estructural en Fase 6, ver 8.3.1)

Track Rápido (v20):  Draft → Approved → Implemented   (sin Review: no hay revisión adversaria de spec)
Modificación:        Implemented/As-built → [Review] → Approved → Implemented   (la fase en curso se sigue en sdd/specs/<ID>.flow.md)
```

- **Draft:** en escritura inicial.
- **Review:** iniciada tras la pasada adversaria 1 (tracks Estándar y Completo; el track Rápido no pasa por Review). **Estado iterativo** donde se procesan hallazgos, se ejecuta la pasada adversaria 2 si fuera necesario (ver sección 13), se resuelven decisiones abiertas y se hace lectura crítica final.
- **Approved:** congelada, lista para implementación. Solo se pasa a este estado cuando los pre-requisitos de Fase 5 están cumplidos.
- **Implemented:** ya en código.
- **Deprecated:** la feature fue eliminada o reemplazada.

**Nota sobre bugfixes:** los artefactos `bugfix-XXX.md` tienen su propio ciclo de vida simplificado. Ver sección 9 (Tratamiento de Bugs).

---

## 11. Herramientas que uso

### 11.1 Asignación de roles a herramientas

Modelo **híbrido** (desde v10). Las fases de pensamiento puro (sin código) pueden hacerse en cualquier herramienta; de Fase 4 en adelante el trabajo vive en Claude Code, donde leo los archivos reales del repo, el schema vivo de la DB y corro los tests.

| Rol | Fase | Herramienta |
|-----|------|-------------|
| Orquestador (Modo Flow, §6.0) | Fases 2→6 + commit | Claude Code (`/sdd-feature`) |
| Interrogador + Redactor (spec-first) | Fases 2+3 | Claude Code (`/sdd-feature`, prompt 08) |
| Interrogador (modo profundo) | Fase 2 (discovery) | Claude.ai o Claude Code (`/sdd-discovery`) |
| Redactor | Fase 3 (draft de spec) | Claude.ai o Claude Code (`/sdd-spec`) |
| Adversario (spec) | Fase 4 | Claude Code, en subagente con contexto limpio (`/sdd-adversarial-spec`) |
| Verificador pre-codegen | Fase 5→6 | Claude Code (`/sdd-verify`) |
| Generador | Fase 6 | Claude Code (`/sdd-codegen`) |
| Adversario (código) | Fase 6 | Claude Code, en subagente con contexto limpio (`/sdd-adversarial-code`) |

**Contexto limpio sin cambiar de herramienta:** la regla de "conversación nueva" para las pasadas adversarias (sección 3) se cumple en Claude Code lanzando un **subagente dedicado** — arranca con contexto propio, aislado del rol que redactó la spec o generó el código. No requiere abrir otra ventana ni otra herramienta.

**Modelo del subagente adversario (desde v18):** los subagentes de las dos pasadas adversarias (`/sdd-adversarial-spec` y `/sdd-adversarial-code`) corren en **Sonnet** por defecto, fijado en la propia llamada a la tool `Agent` de cada comando. La pasada adversaria es razonamiento estructurado (contradicciones, ambigüedades, decisiones no marcadas, desvíos de spec) donde Sonnet rinde a una fracción del costo y la latencia de Opus; la de código fue históricamente el costo dominante del ciclo (corría ×4 capas; desde v19 corre una vez por feature). **No afecta el modelo de la sesión principal** — solo el del subagente. El default es una hipótesis de calidad-costo, no un dogma: si al medir una pasada real Sonnet se pierde hallazgos que Opus sí encuentra, se sube a `opus` en la línea correspondiente del comando (espíritu de Regla 5 — revisar la decisión cuando aparezca evidencia). Como el subagente arranca con contexto limpio de otro modelo distinto del generador, esto además agrega una capa de **independencia de modelo** sobre la independencia de contexto que ya daba la separación.

**Empaquetado:** el proceso está disponible como plugin de Claude Code (`sdd-toolkit`), instalable desde el repo del toolkit. Cada comando `/sdd-*` lee su prompt canónico de `prompts/` (fuente única de verdad) y carga el contexto del proyecto automáticamente.

### 11.2 Editor / IDE

**Visual Studio Code** para edición y trabajo con el repo.

### 11.3 Repositorios

- **Toolkit:** template repository en GitHub (`sdd-toolkit`).
- **Proyectos:** repos creados desde el template, uno por proyecto.

### 11.4 Stack técnico base de proyectos

Definido en sección 4.3.

### 11.5 Gestión de specs

En esta versión del workflow, la gestión de specs (estados, versiones, changelogs, dependencias) se mantiene **manualmente** en archivos `.md` en el repo. Es posible que en versiones futuras se incorpore una herramienta de gestión (ej: Notion con sincronización a GitHub) para automatizar el bookkeeping. Esa decisión se tomará después de haber ejecutado al menos una feature completa con flujo manual.

**INDEX del proyecto:** cada proyecto tiene un archivo `specs/INDEX.md` generado desde `templates/project-index.template.md`. Es la fuente única de verdad para:
- Asignar IDs de specs (secuenciales por proyecto, no por dominio).
- Conocer el estado actual de cada spec.
- Ver el grafo de dependencias entre specs (primer nivel directo).

El INDEX se actualiza en cuatro momentos clave (en Modo Flow lo hace el orquestador; en el camino manual, a mano) del ciclo de vida de cada spec: creación (Draft), aprobación (Approved), implementación (Implemented) y deprecación (Deprecated). La transición Draft → Review no requiere actualización del INDEX.

**ROADMAP del proyecto:** cada proyecto tiene un archivo `ROADMAP.md` generado desde `templates/project-roadmap.template.md` durante Fase 0 (paso 2). Es el documento de visión estratégica que complementa al INDEX:

- **INDEX:** bookkeeping operativo. Cambia cuando una spec cambia de estado.
- **ROADMAP:** planificación estratégica. Cambia solo con cambios estructurales (se agrega/elimina una feature, se reordena el plan, cambia la visión).

El ROADMAP incluye specs agrupadas por fase, con estimación gruesa (S/M/L) y dependencias entre fases. Es input para la cotización al cliente (que se maneja fuera del SDD). Los IDs de specs en el ROADMAP son **orientativos**, no definitivos: los IDs reales se asignan vía el INDEX cuando arranca cada spec.

### 11.6 Gestión de ramas

**Modelo:** GitHub Flow simplificado con rama de staging dedicada.

#### Estructura de ramas

```
main        → producción. Siempre estable. Nunca se pushea directo.
staging     → validación del cliente. Se actualiza cuando yo decido.
feature/*   → desarrollo de features. Una rama por spec.
hotfix/*    → fixes urgentes en producción.
```

**Regla operativa:** nadie pushea directo a `main`, ni yo mismo. Todo pasa por merge desde rama de feature o hotfix.

#### Naming de ramas

```
feature/<SPEC-ID>       → ej: feature/LOTES-001
feature/<SPEC-ID>-v2    → si la spec tuvo revisión mayor durante Fase 6
hotfix/<descripcion>    → ej: hotfix/login-token-expiry
```

El ID de la spec en el nombre de la rama conecta la rama con el INDEX del proyecto, los commits y la spec misma.

#### Flujo de feature normal

```
1. Crear rama al iniciar Fase 6:
   git checkout main && git pull origin main
   git checkout -b feature/SPEC-ID

2. Desarrollar por capas (Fase 6):
   Antes del commit, prueba manual del cambio (gate, sección 7.5).
   Un solo commit cuando la feature está completa, verificada y probada manualmente (no capa por capa; ver secciones 7.5 y 7.6).
   Formato: feat(SPEC-ID): descripción de la feature

3. Feature completa → staging para validación del cliente:
   git checkout staging && git pull origin staging
   git merge feature/SPEC-ID
   git push origin staging
   → Deploy manual a staging.
   → Cliente valida.

4. Cliente aprueba → mergear a producción:
   git checkout main && git pull origin main
   git merge feature/SPEC-ID
   git push origin main
   → Deploy manual a producción.
   git branch -d feature/SPEC-ID

5. Actualizar INDEX:
   Cambiar estado de la spec de Approved a Implemented.
```

#### Flujo de hotfix

```
git checkout main && git pull origin main
git checkout -b hotfix/descripcion-corta

[fix el bug]
git commit -m "fix(AREA): descripción del problema"

git checkout main
git merge hotfix/descripcion-corta && git push origin main
→ Deploy a producción.

git checkout staging
git merge hotfix/descripcion-corta && git push origin staging
→ Staging sincronizado.

git branch -d hotfix/descripcion-corta
```

#### Evolución futura

Cuando se incorpore CI/CD, el deploy manual se reemplaza por trigger automático en merge a `main` (producción) y merge a `staging`. El modelo de ramas no cambia.

Cuando se incorpore gente al equipo, agregar branch protection en `main` en GitHub (Settings → Branches → Branch protection rules): Pull Requests obligatorios, mínimo 1 aprobación. El modelo de ramas no cambia.

---

## 12. Antipatrones a evitar

### 12.1 Antipatrones generales del proceso SDD

- **Vibe coding:** generar código sin spec previa.
- **Spec retroactiva:** escribir spec después del código.
- **Spec sin actualizar tras cambio de código:** el código y la spec divergen sin que lo note.
- **Saltar la revisión que el track exige** o **clasificar el track hacia abajo** porque "está chiquita la feature" (el track se decide por los criterios objetivos de §8.3.2, no por tamaño percibido).
- **Modificar spec en pleno desarrollo sin frenar generación.**
- **Aceptar código que "funciona" sin verificar que cumple spec.**
- **Generar todas las capas sin verificación entre ellas.** Desde v19 las capas se generan seguidas en una sola ejecución, pero en orden y con gate automático (tests + typecheck/build) entre cada una; el antipatrón es saltar ese gate, no ahorrarse la confirmación humana.
- **Confirmaciones que no deciden nada:** pedir "¿sigo?", re-confirmar un gate ya confirmado, o presentar hallazgos descartables uno por uno. Cada espera innecesaria cuesta más que lo que protege (§6.0).
- **Mezclar capacidades funcionales** en una sola spec (violación de granularidad).
- **Dejar decisiones implícitas** del LLM sin validar.
- **Sobre-ingeniería silenciosa** que se acumula sin que lo note.
- **Iteración adversaria infinita:** seguir iterando contra hallazgos cada vez más menores en vez de aprobar con criterio (máximo 2 pasadas, ver sección 13).
- **Reabrir decisiones de pasadas adversarias anteriores sin nuevo criterio:** la IA repite hallazgos entre pasadas porque no tiene memoria; mi trabajo es reconocerlos y mantener decisiones cerradas.
- **Validación circular silenciosa:** asumir que porque el código pasa la pasada adversaria contra la spec, la spec es correcta. Ver sección 2.6 y 7.4.2.

### 12.2 Antipatrones específicos de bugs

- **Fix sin clasificar:** corregir un bug sin determinar primero si es Tipo A, B o C. La corrección que corresponde es diferente según el origen.
- **Parchear código sin trazabilidad:** ni `bugfix-XXX.md` (cuando corresponde, §9.3) ni commit `fix:` con observado/esperado, causa y test. No se puede saber qué causó el cambio meses después.
- **Tratar un Tipo C como bug:** si el comportamiento es correcto según la spec pero el negocio cambió de opinión, es un cambio de requerimiento. Tratarlo como bug corrompe la trazabilidad.
- **Fix de emergencia sin deuda técnica registrada:** el "lo especifico después" que nunca llega. Si el fix urgente se hace sin spec, la deuda técnica se registra ese mismo día, no "cuando haya tiempo".
- **No escribir el test de regresión:** el bug se cierra, el test no existe, el bug vuelve. El test de regresión es parte del cierre, no un opcional.
- **Actualizar la spec original sin subirle versión:** la spec queda con cambio invisible. La trazabilidad se rompe.

### 12.3 Mis zonas de riesgo personales

Estas son mis tendencias específicas. Las nombro explícitamente para vigilarlas activamente:

- **Soy ansioso:** tiendo a querer avanzar rápido y cerrar incomodidad procesando poco.
- **Tendencia a cerrar feedback rápido:** cuando alguien (o yo mismo en relectura) me marca algo, mi reflejo es "ya lo entendí, avancemos" en lugar de procesarlo en profundidad.
- **Sub-especificación de criterios de aceptación y casos borde:** consistentemente los dejo más cortos de lo que deberían.
- **Esquivar decisiones con "es estándar" o "lo definimos después":** cuando una decisión me da incomodidad, tiendo a posponerla.
- **No relectura antes de cerrar:** mando o cierro sin releer.
- **Trabajar cansado y de noche aumenta el riesgo de aprobación apresurada.** No tengo barrera operativa de tiempo entre Fase 4 y Fase 5; la disciplina depende solo de mí. Cuando aparezca un caso de spec mal aprobada por cansancio, activo Regla 5 y revisito esta decisión.

### 12.4 Checklist de auto-check

Antes de aprobar una spec o cerrar una capa de código, recorro esta checklist:

- [ ] **¿Leí completa la superficie de decisión (§4, §6, §7, §8, §10, §14)?** No "le di una mirada".
- [ ] **¿Esquivé alguna decisión?** ¿Hay algún "lo definimos después" o "es estándar" que en realidad necesita decisión ahora?
- [ ] **¿Quedan decisiones abiertas o pendientes de consulta?** Si sí, NO apruebo. Resuelvo primero.
- [ ] **¿Criterios de aceptación y casos borde están suficientemente detallados?** Si me parece que están justos, releo y aplico la taxonomía obligatoria de la guide.
- [ ] **¿Procesé el feedback recibido o lo cerré rápido?** ¿Estoy aprobando con criterio o con ansiedad?
- [ ] **¿Modifiqué el contenido real de la spec para reflejar lo procesado de la pasada adversaria, o solo le di la razón al adversario en el chat sin trasladarlo al documento?**
- [ ] **¿Las decisiones del LLM tomadas por defecto (§14) fueron revisadas y validadas explícitamente?** Con la Regla 1 v20 son más: ¿alguna es en realidad de alto impacto y debió preguntarse?
- [ ] **¿El track está bien clasificado y se hizo la revisión que exige?**
- [ ] **¿Estoy cansado?** Si sí, el riesgo de aprobación apresurada es mayor. Considero esperar.

Si alguna respuesta es "no" o "no estoy seguro", freno y resuelvo antes de avanzar.

---

## 13. Pasadas adversarias: cuántas veces iterar

La IA en rol Adversario siempre va a encontrar algo. Si itero indefinidamente, nunca apruebo. Las siguientes reglas evitan caer en el loop adversario infinito.

### 13.1 Calidad de los hallazgos, no cantidad

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

### 13.2 Regla práctica: máximo 2 pasadas adversarias

- **Pasada 1:** sobre el draft (estado Draft). Procesa hallazgos, genera nueva versión, la spec pasa a Review.
- **Pasada 2 — condicional (desde v14):** solo se ejecuta si la Pasada 1 produjo **al menos un hallazgo bloqueante** (contradicción real, gap operativo concreto, violación al setup foundacional, decisión implícita sin marcar — los criterios de 13.1). Si la Pasada 1 fue limpia o solo dejó hallazgos descartables/estilísticos, se pasa directo a Fase 5 sin segunda pasada. Antes la pasada 2 era el camino por defecto; el costo de una pasada completa no se justifica cuando la primera no encontró nada que itere.
- **Aprobación:** la spec pasa a Approved cuando los pre-requisitos de Fase 5 están cumplidos, con 1 o 2 pasadas según lo anterior.

Si la pasada 2 sigue revelando hallazgos estructurales serios, la spec tiene problemas de fondo, no de iteración. Parar y reconsiderar de raíz.

### 13.3 Hallazgos repetidos entre pasadas

**Importante:** la IA en rol Adversario no tiene memoria de pasadas anteriores. Es esperable que en la Pasada 2 vuelvan a aparecer hallazgos ya resueltos en Pasada 1.

**Regla operativa:** los hallazgos repetidos se descartan automáticamente, **salvo que aparezca nuevo criterio** (nueva evidencia, nueva información, cambio en circunstancias) que justifique reabrir la decisión.

Esto previene caer en loop infinito reabriendo en cada pasada las mismas discusiones.

### 13.4 Pregunta de corte

Después de cada pasada adversaria:

> *"Si apruebo esta spec hoy y aparece un problema en la práctica, ¿voy a poder decir que aprobé con criterio o me voy a arrepentir?"*

- Aprobé con criterio, sabía los trade-offs → **apruebo**.
- Me voy a arrepentir, debí haber visto X → **itero una vez más sobre X específicamente**.

### 13.5 Principio de fondo

Las specs no se aprueban porque son perfectas. Se aprueban porque son **suficientemente buenas para el riesgo que asumo**.

Una spec con 3 imperfecciones menores conocidas y documentadas es mejor que una spec sometida a 5 pasadas adversarias buscando perfección.

---

## 14. Cambios a este documento

Este `WORKFLOW.md` evoluciona. Las modificaciones siguen las reglas de versionado de sección 10.3 (toolkit).

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
