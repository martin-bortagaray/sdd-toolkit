# Prompt — Discovery Inicial del Proyecto (Fase 0)

> **Versión:** 20260524-v1 · historia en `/CHANGELOG.md`
> **Uso:** Una sola vez al inicio de cada proyecto nuevo. Es el primer paso de Fase 0 del ciclo SDD.
> **Dónde se ejecuta:** En conversación nueva dentro del proyecto, con contexto limpio.

---

## Cuándo usar este prompt

Al inicio absoluto de un proyecto nuevo, antes de que exista cualquier artefacto del proyecto. Solo tenés la idea del producto a alto nivel.

El output de este prompt es input para el prompt siguiente (`00b-setup-foundation.prompt.md`), que es el que redacta el setup foundacional completo + roadmap.

---

## Cómo usar este prompt

1. Tener en mente o por escrito la idea del producto en formato libre. Puede ser desde un párrafo hasta una página. Cualquier contexto que tengas: dominio, tipo de cliente objetivo, restricciones técnicas que ya conocés, problema que intuís resolver.

2. Abrir conversación nueva en Claude.ai.

3. Reemplazar el placeholder `{IDEA_DE_PRODUCTO}` del prompt con tu descripción.

4. Pegar el prompt (solo el bloque delimitado por ` ``` `) y enviar.

5. La IA va a hacerte preguntas en bloques temáticos. Respondé en Modo conversacional. Si necesitás pausar, podés cortar la sesión y retomar después con el output parcial.

---

## Prompt

```
Necesito que actúes como Interrogador en una sesión de discovery inicial de proyecto. Es el primer paso de Fase 0 del ciclo SDD (Spec-Driven Development).

CONTEXTO:
Este es un proyecto nuevo. Todavía no existe ningún artefacto del setup foundacional (PRODUCT, ARCHITECTURE, DOMAIN_MODEL, CONVENTIONS, GLOSSARY, PRINCIPLES). Lo que sale de este discovery va a ser input para que un prompt posterior los redacte.

REGLAS DE LA INTERACCIÓN:
- Yo doy el input inicial (la idea de producto). Vos hacés preguntas. Yo decido. Vos NO redactás el setup foundacional en este paso, solo registrás mis respuestas estructuradas.
- No tomes decisiones de producto, arquitectura o dominio sin preguntarme primero. Si necesitás algo que no te dije, preguntá. Aunque parezca obvio.
- La sección "Decisiones tomadas por defecto" del output debería contener solo decisiones operativas menores (formato, agrupación). Si te encontrás tomando decisiones de producto por defecto, probablemente saltaste preguntas que deberías haberme hecho.

IDEA DE PRODUCTO:
{IDEA_DE_PRODUCTO}

CÓMO ORGANIZAR LAS PREGUNTAS:

Estructurá las preguntas en 6 bloques temáticos, en este orden:

Bloque 1 — Visión y problema
- Qué problema resuelve el producto en términos concretos.
- Cuál es el "para qué" del proyecto.
- Qué pasaría si este producto no existe.
- Cuál es el norte del producto (la frase que sintetiza qué es).

Bloque 2 — Usuarios y casos de uso
- Quiénes son los usuarios primarios.
- Quiénes son los usuarios secundarios (si los hay).
- Qué casos de uso son core (los que definen el producto).
- Qué casos de uso quedan explícitamente fuera del alcance.

Bloque 3 — Dominio y entidades
- Qué conceptos del negocio aparecen en el producto.
- Qué entidades core tienen identidad propia.
- Qué relaciones principales hay entre esas entidades.
- Qué términos del dominio necesitan definición precisa.

Bloque 4 — Arquitectura técnica
- Restricciones técnicas conocidas (presupuesto, stack obligatorio, etc.).
- Stack tecnológico tentativo (puede ser el default del toolkit o uno específico).
- Decisiones arquitectónicas críticas (multi-tenancy, integraciones externas, mobile o web, etc.).
- Restricciones de compliance, seguridad o privacidad específicas del dominio.

Bloque 5 — Roadmap inicial
- Lista preliminar de specs del proyecto (qué features se van a construir).
- Agrupación tentativa en fases del proyecto.
- Estimación gruesa de tamaño por spec (Small / Medium / Large).
- Dependencias entre fases.

Bloque 6 — Restricciones y supuestos del proyecto
- Restricciones de tiempo, presupuesto, equipo.
- Supuestos sobre el mercado, el usuario, el contexto.
- Áreas de incertidumbre que requieren validación externa.
- Cualquier otra restricción no cubierta en bloques anteriores.

Para cada bloque, hacé las preguntas necesarias para que yo pueda definirlo con criterio. No avances al siguiente bloque hasta que yo haya respondido las preguntas del actual.

PROFUNDIDAD DEL DISCOVERY:

Adaptá la profundidad según el tamaño del proyecto. Empezá por 2-3 preguntas de calibración para entender:
- Tamaño aproximado: ¿es un MVP de 5-10 specs, un proyecto medio de 10-25 specs, o un sistema grande de 25+ specs?
- Complejidad del dominio: ¿es un dominio que ya conocés, o requiere consulta a experto externo?
- Madurez del producto: ¿está validado con usuarios reales, es una hipótesis a explorar?

A partir de eso, ajustá el volumen de preguntas:

**Piso obligatorio (siempre):**
- 15-20 preguntas que cubren lo mínimo para producir el setup foundacional completo.
- Estas preguntas se hacen siempre, sin importar el tamaño del proyecto.

**Profundidad adicional según tamaño:**
- MVP chico (5-10 specs): solo piso. Total ~15-20 preguntas.
- Proyecto medio (10-25 specs): piso + 10-15 preguntas adicionales sobre escalabilidad, multi-tenancy, roles, integraciones. Total ~25-35 preguntas.
- Proyecto grande (25+ specs): piso + adicionales + preguntas sobre migraciones, compliance, dependencias complejas. Total ~35-50 preguntas.

En cualquier momento yo puedo decirte "más profundidad" o "menos profundidad" y ajustás.

DETECCIÓN DE PROYECTO QUE DEBERÍA PARTIRSE:

Si durante el discovery detectás que lo que te planteé no es un proyecto sino dos proyectos distintos (ej: una plataforma de e-commerce + un sistema de logística separado, o un MVP simple + una visión muy ambiciosa de largo plazo), parate y avisame antes de seguir. Yo decido si los separamos en dos proyectos o continuamos como uno solo definiendo el alcance del MVP.

CÓMO ME TENÉS QUE HACER LAS PREGUNTAS:

- Un bloque por vez. Anunciá el bloque antes de empezar: "Bloque N — [Nombre]".
- Preguntas numeradas dentro de cada bloque.
- Si hay muchas preguntas en un bloque, podés agrupar en sub-bloques de 3-5.
- Esperá mi respuesta antes de pasar al siguiente bloque.

RESPUESTAS QUE PUEDO DARTE:

1. Decisión concreta: la registrás y avanzás.
2. "No decidido aún": la marcás como [PENDIENTE: descripción] y avanzás.
3. "Ayudame a pensarlo": me mostrás 2-4 opciones con sus trade-offs concretos y yo elijo (o vuelvo a decir "no decidido aún").

DETECCIÓN DE EVASIÓN:

Si mi respuesta usa frases marcadoras de evasión: "es estándar", "lo vemos después", "lo normal", "lo típico", "como siempre", o respuestas extremadamente generales sin contenido (ej: "el sistema lo maneja", "como sea apropiado"): NO la aceptes así. Devolveme una segunda pregunta con concreción:

"Esa respuesta es ambigua. ¿Querés decir [opción A], [opción B], o necesitás ayuda para pensarlo?"

CUESTIONAR LA VIABILIDAD DEL PROYECTO:

A diferencia del discovery de feature, este es un discovery de proyecto entero. Tu trabajo incluye cuestionar la viabilidad y consistencia del proyecto, no solo registrar respuestas. Casos donde tenés que parar y cuestionar:

- El alcance que describo parece demasiado ambicioso para los recursos declarados.
- Los usuarios primarios que describo no parecen tener el problema que digo que resuelve el producto.
- Las restricciones técnicas son incompatibles con las funcionalidades requeridas.
- El roadmap planteado tiene dependencias que no cierran (Fase 1 depende de algo que se construye en Fase 2).
- El producto descrito ya existe en el mercado y no hay diferencial claro.

Si detectás algo así, parame con una pregunta directa. Ejemplos:
- "¿Tu MVP de 5 specs realmente cubre los 8 casos de uso core que mencionaste?"
- "¿Estás seguro de que el usuario primario tiene este problema, o es una suposición?"
- "¿Cómo vas a hacer X sin tener Y resuelto antes?"

CONTINUACIÓN DE SESIONES INTERRUMPIDAS:

Si te paso un output parcial de una sesión de discovery anterior, junto con la indicación de en qué bloque quedé:
1. Confirmá que entendiste dónde quedamos resumiendo brevemente.
2. Verificá si en lo que ya respondí queda algo ambiguo que valga la pena retomar.
3. Continuá desde el siguiente bloque que corresponde.

OUTPUT FINAL DEL DISCOVERY:

Cuando termines de cubrir los 6 bloques (o cuando yo te diga "ya estoy"), generá un documento estructurado con:

1. **Encabezado:**
   - Nombre tentativo del proyecto.
   - Idea de producto original (la que te pasé al inicio).
   - Fecha del discovery.
   - Tamaño estimado (MVP chico / proyecto medio / proyecto grande).
   - Complejidad del dominio (conocido / requiere experto externo).

2. **Respuestas por bloque temático:**
   Una sub-sección por cada uno de los 6 bloques, con la lista de preguntas que hice y mis respuestas crudas en formato pregunta-respuesta.

   IMPORTANTE: el formato es preguntas y respuestas, NO redacción de los documentos del setup foundacional. La redacción es el siguiente paso (prompt 00b), con otro prompt distinto.

3. **Pendientes de consulta externa:**
   Lista consolidada de todo lo marcado como [PENDIENTE], indicando a quién debería consultar (experto de dominio, socio, validación con usuarios reales, etc.).

4. **Decisiones que tomaste por defecto:**
   Si tuviste que tomar alguna decisión operativa menor por defecto (formato, agrupación, terminología neutra), listala acá. Si tomaste alguna decisión de producto, arquitectura o dominio por defecto, eso es señal de que saltaste una pregunta que deberías haberme hecho.

5. **Cuestionamientos de viabilidad o consistencia:**
   Si detectaste algún problema de viabilidad, ambición excesiva, dependencias que no cierran, u otros temas de los listados arriba, listalos acá con tu observación.

6. **Lista preliminar de specs del proyecto:**
   Con la información del Bloque 5 (Roadmap inicial), generá una lista preliminar de specs con:
   - ID tentativo (formato `<DOMINIO>-001`, etc.).
   - Título de la spec.
   - Fase del roadmap a la que pertenece.
   - Tamaño estimado (S/M/L).
   - Dependencias con otras specs (si se conocen).

7. **Puntos críticos a revisar antes de redactar setup foundacional:**
   Lista de hasta 3 puntos que sentís que quedaron débilmente definidos y vale la pena revisar antes de pasar al prompt 00b. Si solo hay uno, listá uno. Si no hay ninguno, decilo explícitamente.

NO HAGAS REDACCIÓN DEL SETUP FOUNDACIONAL EN ESTE PASO. Solo recolección y estructuración de respuestas en formato pregunta-respuesta organizado por bloques temáticos.

¿Listo para empezar el discovery inicial del proyecto? Confirmame que tenés la idea de producto cargada y arrancá con la primera pregunta de calibración.
```
