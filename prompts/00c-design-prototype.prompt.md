# Prompt — Diseño de Prototipo UI (Fase 0)

> **Versión:** 20260524-v1 · historia en `/CHANGELOG.md`
> **Uso:** Tercer y último paso de Fase 0 del ciclo SDD. Se ejecuta después del prompt 00b-setup-foundation.
> **Dónde se ejecuta:** Flujo híbrido en dos sesiones separadas:
> 1. **Sesión 1 — Claude.ai:** generación del brief estructurado.
> 2. **Sesión 2 — Claude Design:** uso del brief para generar prototipo navegable.

---

## Cuándo usar este prompt

Después de tener el setup foundacional + roadmap completos y validados. Antes de la propuesta al cliente.

El output final de este prompt (el prototipo navegable en Claude Design) es input para la propuesta comercial al cliente.

---

## Cómo usar este prompt

### Pre-requisitos

1. Setup foundacional del proyecto completo y validado (output del prompt 00b).
2. Design system del autor cargado (`templates/design-system.template.md`).
3. ROADMAP del proyecto generado y validado.

### Sesión 1 — Claude.ai (generar brief)

1. Abrir conversación nueva en Claude.ai.
2. **Adjuntar como archivos:**
   - `PRODUCT.md` del proyecto.
   - `DOMAIN_MODEL.md` del proyecto.
   - `GLOSSARY.md` del proyecto.
   - `ROADMAP.md` del proyecto.
   - `design-system.template.md` del toolkit (con override de color del proyecto si aplica).
3. Pegar el prompt y enviar.
4. La IA va a proponer una lista de pantallas para el prototipo. Vos validás o ajustás.
5. La IA genera el brief estructurado final.
6. Guardar el brief en una nota local.

### Sesión 2 — Claude Design (generar prototipo)

1. Abrir Claude Design desde tu cuenta de Claude.ai.
2. Pegar el brief generado en la Sesión 1 como primer mensaje.
3. Iterar con Claude Design hasta tener un prototipo navegable de las pantallas aprobadas.
4. Guardar el output (URL compartible, export, screenshots) en el repo del proyecto bajo `docs/prototype/`.

---

## Prompt para Sesión 1 (Claude.ai)

```
Necesito que actúes como Generador de brief para diseño de prototipo UI. Es el tercer paso de Fase 0 del ciclo SDD (Spec-Driven Development).

CONTEXTO QUE TE PASO:
1. PRODUCT.md: spec del producto del proyecto.
2. DOMAIN_MODEL.md: entidades del dominio.
3. GLOSSARY.md: términos del dominio.
4. ROADMAP.md: lista de specs agrupadas por fase.
5. design-system.template.md: design system del autor que aplica a todos sus proyectos.

TU TRABAJO:

Producir un brief estructurado que el autor va a copiar y pegar en Claude Design para generar un prototipo navegable. El brief debe ser autocontenido: Claude Design no va a tener acceso a los archivos del setup foundacional, solo al brief.

REGLA FUNDAMENTAL: NO TOMES DECISIONES DE PRODUCTO.

Las decisiones de producto ya están en el setup foundacional. Tu trabajo es seleccionar qué pantallas incluir en el prototipo y redactar el brief usando la información del setup foundacional. NO inventes funcionalidades que no están en PRODUCT.md ni en ROADMAP.md.

PASO 0 — VERIFICACIÓN DE PRE-REQUISITOS:

Verificar que tenés los 5 archivos cargados. Si falta alguno, parate y pediles que adjunte el que falta.

Verificar que el design system declara un color de acento. Si declara que es variable por proyecto, preguntale al autor cuál color usar para este proyecto específico.

Verificar conversación limpia con una pregunta de confirmación:

"Antes de generar el brief, confirmame: ¿esta conversación es nueva, adjuntaste PRODUCT, DOMAIN_MODEL, GLOSSARY, ROADMAP y design-system, y el color de acento para este proyecto está claro? (sí/no)"

Si responde "no", parate. Si "sí", continuar al Paso 1.

PASO 1 — PROPONER LISTA DE PANTALLAS:

Basándote en PRODUCT.md (casos de uso core) y ROADMAP.md (specs de Fase 1), proponé una lista de 4 a 8 pantallas a incluir en el prototipo.

Criterio de inclusión (del WORKFLOW del autor):

**Incluir:**
- Pantallas que muestren los casos de uso core del producto (sección 5 de PRODUCT.md).
- Pantallas que tengan decisiones de UI no triviales (flujos multi-paso, dashboards, vistas complejas).

**Excluir:**
- CRUDs administrativos sin lógica de negocio relevante (usuarios, configuraciones, catálogos genéricos).
- Pantallas de autenticación estándar (login, registro, recuperación de contraseña).
- Páginas legales o de soporte.

Para cada pantalla propuesta, dame:
- Nombre de la pantalla.
- Justificación de por qué la incluís (qué caso de uso core cubre o qué decisión de UI no trivial tiene).
- Spec del roadmap a la que corresponde (si aplica).

Esperá mi confirmación de la lista antes de generar el brief. Yo puedo:
- Aprobar la lista completa.
- Pedirte agregar pantallas que faltan.
- Pedirte quitar pantallas que no aportan.

PASO 2 — GENERAR EL BRIEF ESTRUCTURADO:

Una vez aprobada la lista de pantallas, generá el brief con esta estructura exacta:

═══════════════════════════════════════════════
BRIEF PARA CLAUDE DESIGN
═══════════════════════════════════════════════

Proyecto: [nombre del proyecto]
Fecha: [hoy]

## 1. Producto

[Síntesis del producto en 2-3 párrafos. Qué es, qué problema resuelve, para quién es. Tomado de PRODUCT.md secciones 1, 2 y 3.]

## 2. Usuarios principales

[Lista de roles principales con descripción operativa. Tomado de PRODUCT.md sección 3 y DOMAIN_MODEL.md.]

## 3. Casos de uso core

[Lista de los 3-5 casos de uso core del producto. Tomado de PRODUCT.md sección 5.]

## 4. Entidades del dominio relevantes para UI

[Lista de las entidades principales con sus atributos visibles en UI. Tomado de DOMAIN_MODEL.md. Solo entidades que aparecen en alguna pantalla del prototipo.]

## 5. Pantallas a diseñar

[Lista de las 4-8 pantallas aprobadas en el Paso 1. Para cada pantalla:]

### Pantalla N: [Nombre]

**Propósito:** [Qué objetivo tiene esta pantalla para el usuario.]

**Caso de uso que cubre:** [Referencia al caso de uso core correspondiente.]

**Información principal que muestra:**
- [Lista de los elementos de información que aparecen en pantalla.]

**Acciones principales disponibles:**
- [Lista de acciones que el usuario puede ejecutar desde la pantalla.]

**Estados a contemplar:**
- [Loading, empty, error, success — según corresponda. Si alguna no aplica, omitir.]

**Navegación:**
- Llega desde: [pantalla previa típica]
- Lleva a: [pantalla siguiente típica]

## 6. Estilo visual

**Design system:** moderno/minimalista, modo oscuro como default.

**Paleta:**
- Color de acento: [INDIGO por defecto, o el color del cliente si aplica].
- Backgrounds: zinc-950 base, zinc-900 elevado.
- Textos: zinc-50 principal, zinc-400 secundario.
- Colores funcionales: green-500 (success), amber-500 (warning), red-500 (error), blue-500 (info).

**Tipografía:**
- Principal: Inter.
- Monoespaciada: JetBrains Mono (para IDs y datos técnicos).

**Componentes:**
- Botones, inputs, cards con `rounded-md` (6px de radio).
- Bordes 1px en `zinc-800` para separación.
- Sin sombras pesadas (usar background diferenciado para elevación).

**Iconos:**
- Lucide. Tamaño base 16px para inline, 20px para botones.

**Patrones de UX:**
- Sidebar fijo en desktop para navegación principal.
- Labels arriba de inputs en formularios.
- Toast en esquina inferior derecha para feedback.
- Confirmación con dialog para acciones destructivas.

## 7. Restricciones

[Cualquier restricción específica del proyecto que afecte el diseño visual. Tomado de PRODUCT.md sección 8 y PRINCIPLES.md si aplica. Ejemplos:
- "Apps que se usan en exteriores con luz fuerte: priorizar contraste alto."
- "Usuarios mayores: tamaños de fuente más grandes."
- "Requisitos de compliance WCAG AA en todos los componentes."
Si no hay restricciones específicas, omitir esta sección.]

## 8. Lo que NO incluir

[Funcionalidades o pantallas que parecerían naturales pero están explícitamente fuera del alcance del producto. Tomado de PRODUCT.md sección 6.]

═══════════════════════════════════════════════
FIN DEL BRIEF
═══════════════════════════════════════════════

PASO 3 — INSTRUCCIONES OPERATIVAS PARA EL AUTOR:

Después del brief, agregá esta sección con instrucciones para que el autor sepa qué hacer con el brief:

═══════════════════════════════════════════════
SIGUIENTES PASOS PARA EL AUTOR
═══════════════════════════════════════════════

1. Copiar el brief completo (todo lo que está entre los marcadores "BRIEF PARA CLAUDE DESIGN" y "FIN DEL BRIEF").

2. Abrir Claude Design desde tu cuenta de Claude.ai.

3. Pegar el brief como primer mensaje en Claude Design.

4. Pedir explícitamente: "Generá un prototipo navegable con las [N] pantallas descritas, conectadas con navegación funcional. Modo oscuro como vista principal."

5. Iterar con Claude Design para refinar pantallas individuales. Mantener el design system declarado en el brief en todas las iteraciones.

6. Cuando el prototipo esté listo, guardar el output (URL compartible, export, screenshots) en el repo del proyecto bajo `docs/prototype/`.

7. El prototipo es input para la propuesta comercial al cliente. NO es la implementación final.

OUTPUT FINAL:

Generá dos bloques en el mismo mensaje:

Primer bloque — Resumen breve (5-10 líneas):
- Cantidad de pantallas incluidas en el prototipo.
- Cobertura de casos de uso core (cuántos de los listados en PRODUCT.md cubre el prototipo).
- Si alguna pantalla quedó débilmente definida y vale revisar antes de pasar a Claude Design.

Segundo bloque — Brief + instrucciones (lo que el autor va a usar):

[El brief estructurado según Paso 2, seguido de las instrucciones operativas según Paso 3, ambos con sus delimitadores visuales claros.]

¿Listo? Empezá ejecutando el Paso 0 (verificaciones) y después Paso 1 (proponer lista de pantallas).
```
