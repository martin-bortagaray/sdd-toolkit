# Guía de uso de artefactos del toolkit SDD

> **Toolkit:** sdd-toolkit
> **Versión:** 20260524-v1
> **Propósito:** Referencia rápida de qué artefacto usar en cada momento del proceso y catálogo completo del toolkit.

Este documento es complemento del WORKFLOW.md y de los diagramas de flujo. Tiene dos vistas:

- **Vista 1 — Cronológica:** "estoy en X momento del proceso, ¿qué artefacto necesito?"
- **Vista 2 — Catálogo:** "tengo este artefacto, ¿para qué sirve y cuándo lo uso?"

---

## Vista 1 — Artefactos por momento del proceso

Esta tabla recorre el proceso completo de inicio a fin, indicando para cada momento qué prompts y templates están involucrados.

### Fase 0 — Inicio del proyecto

| Momento | Prompt que ejecuto | Templates / archivos que adjunto | Output |
|---------|-------------------|----------------------------------|--------|
| **Paso 1 — Discovery inicial** | `00-project-discovery.prompt.md` | Ninguno. Solo idea de producto en texto libre. | Documento de discovery con 7 secciones (respuestas por bloque + pendientes + decisiones por defecto + cuestionamientos + lista preliminar de specs). |
| **Paso 2 — Redacción setup + roadmap** | `00b-setup-foundation.prompt.md` | Los 7 templates del setup: `product-spec.template.md`, `architecture.template.md`, `domain-model.template.md`, `conventions.template.md`, `glossary.template.md`, `principles.template.md`, `project-roadmap.template.md`. Más el output del Paso 1. | 7 archivos del proyecto: `PRODUCT.md`, `ARCHITECTURE.md`, `DOMAIN_MODEL.md`, `CONVENTIONS.md`, `GLOSSARY.md`, `PRINCIPLES.md`, `ROADMAP.md`. |
| **Paso 3.1 — Brief para Claude Design** | `00c-design-prototype.prompt.md` | `PRODUCT.md`, `DOMAIN_MODEL.md`, `GLOSSARY.md`, `ROADMAP.md` del proyecto + `design-system.template.md` del toolkit. | Brief estructurado en 8 secciones, listo para pegar en Claude Design. |
| **Paso 3.2 — Prototipo en Claude Design** | No es prompt. Sesión en Claude Design. | El brief generado en Paso 3.1. | Prototipo navegable de 4-8 pantallas, guardado en `docs/prototype/` del proyecto. |
| **Paso 4 — Propuesta al cliente** | No es prompt. Fuera del SDD. | `ROADMAP.md` + prototipo como inputs. | Documento de propuesta comercial (formato propio del autor, no es parte del toolkit). |

Al terminar Fase 0, crear `INDEX.md` del proyecto usando `templates/project-index.template.md`. El INDEX queda vacío hasta que arranque la primera spec.

### Ciclo de feature (se repite por cada feature del roadmap)

| Momento | Prompt que ejecuto | Templates / archivos que adjunto | Output |
|---------|-------------------|----------------------------------|--------|
| **Fase 1 — Definir necesidad** | Ninguno. Escribo notas crudas. | Ninguno. | Notas internas, sin formato. |
| **Fase 2 — Discovery de feature** | `01-discovery.prompt.md` | Setup foundacional completo del proyecto (6 archivos). Specs Approved que sean dependencias directas (primer nivel). | Documento estructurado por secciones con respuestas + pendientes + decisiones por defecto + lista de dependencias. |
| **Fase 3 — Redacción de spec** | `02-draft-spec.prompt.md` | Output de Fase 2 + setup foundacional + dependencias + `feature-spec.template.md` + `feature-spec.guide.md` + `INDEX.md` (para asignar ID). | Spec en estado Draft. Archivo `specs/<SPEC-ID>.md`. Actualizo INDEX. |
| **Fase 4 — Pasada adversaria de spec** | `03-adversarial-spec.prompt.md` | Spec Draft + setup foundacional + dependencias + `feature-spec.guide.md`. | Hallazgos clasificados (bloqueantes / mejoras / preguntas). Yo proceso hallazgos y actualizo la spec. Estado: Review. |
| **Fase 5 — Aprobación + verificación** | `06-spec-verification.prompt.md` | Spec Approved + setup foundacional + dependencias + `feature-spec.guide.md`. | Veredicto VERDE / AMARILLO / ROJO con checklist completo. |
| **Fase 6 — Codegen Capa 1 (Datos)** | `04-codegen-layer.prompt.md` con `{CAPA}` = "Modelo de datos" | Spec Approved + setup foundacional + dependencias. | Código + tests + tabla comparativa + decisiones técnicas tomadas. |
| **Fase 6 — Pasada adversaria Capa 1** | `05-adversarial-code.prompt.md` | Código generado + spec + setup. | Hallazgos clasificados. Yo proceso bloqueantes inmediatamente, no bloqueantes a `DEBT.md`. |
| **Fase 6 — Codegen Capa 2 (Negocio)** | `04-codegen-layer.prompt.md` con `{CAPA}` = "Lógica de negocio" | Lo anterior + código aprobado de Capa 1 + schema real de DB. | Idem Capa 1 pero para lógica de negocio. |
| **Fase 6 — Pasada adversaria Capa 2** | `05-adversarial-code.prompt.md` | Código de Capa 2 + spec + setup. | Idem. |
| **Fase 6 — Codegen Capa 3 (API)** | `04-codegen-layer.prompt.md` con `{CAPA}` = "API / Capa de acceso" | Lo anterior + código aprobado de Capas 1 y 2. | Idem Capa 1 pero para API. |
| **Fase 6 — Pasada adversaria Capa 3** | `05-adversarial-code.prompt.md` | Código de Capa 3 + spec + setup. | Idem. |
| **Fase 6 — Codegen Capa 4 (UI)** | `04-codegen-layer.prompt.md` con `{CAPA}` = "UI" | Lo anterior + código aprobado de Capas 1, 2, 3 + `design-system.template.md`. | Idem Capa 1 pero para UI. |
| **Fase 6 — Pasada adversaria Capa 4** | `05-adversarial-code.prompt.md` | Código de Capa 4 + spec + setup. | Idem. |
| **Deploy a staging** | No es prompt. Comandos git. | Ninguno. | Feature en ambiente staging. Cliente notificado para validar. |
| **Cliente valida en staging** | No aplica. Es un waitstate. | Ninguno. | Feedback del cliente: aprueba o pide ajustes. |
| **Deploy a producción** | No es prompt. Comandos git. | Ninguno. | Feature en producción. Actualizo INDEX (Approved → Implemented). |

Durante todo el ciclo, los siguientes artefactos están como referencia constante:

- `WORKFLOW.md`: para consultar reglas, antipatrones, pasos detallados.
- `protocols/codegen-protocol.md`: para el checklist operativo de Fase 6.
- `INDEX.md` del proyecto: para asignar IDs y consultar estados.
- `ROADMAP.md` del proyecto: para saber qué feature viene después.

---

## Vista 2 — Catálogo completo del toolkit

Esta tabla lista los 25 artefactos del toolkit organizados por tipo.

### Workflow (1 artefacto)

| Artefacto | Tipo | Cuándo se usa | Para qué sirve |
|-----------|------|---------------|----------------|
| `workflow/WORKFLOW.md` | Documento de gobierno | Siempre. Referencia constante. | Define reglas no negociables, fases del proceso, antipatrones, criterios de decisión. Es la fuente de verdad del proceso. |

### Prompts de Fase 0 (3 artefactos)

| Artefacto | Tipo | Cuándo se usa | Para qué sirve |
|-----------|------|---------------|----------------|
| `prompts/00-project-discovery.prompt.md` | Prompt | Una sola vez por proyecto, al inicio. | Discovery inicial del proyecto. La IA hace preguntas en 6 bloques temáticos para entender qué construir. |
| `prompts/00b-setup-foundation.prompt.md` | Prompt | Una sola vez por proyecto, después del Paso 1 de Fase 0. | Redacta los 6 archivos del setup foundacional + ROADMAP en un solo flujo, usando el output del discovery como input. |
| `prompts/00c-design-prototype.prompt.md` | Prompt | Una sola vez por proyecto, después del Paso 2 de Fase 0. | Genera un brief estructurado para pegar en Claude Design y producir el prototipo navegable. |

### Prompts del ciclo de feature (6 artefactos)

| Artefacto | Tipo | Cuándo se usa | Para qué sirve |
|-----------|------|---------------|----------------|
| `prompts/01-discovery.prompt.md` | Prompt | Una vez por feature, al iniciar Fase 2. | Discovery de feature. La IA hace preguntas estructuradas por secciones para preparar la redacción de la spec. |
| `prompts/02-draft-spec.prompt.md` | Prompt | Una vez por feature, en Fase 3. | Redacta la spec completa usando el output del discovery + setup foundacional + dependencias. |
| `prompts/03-adversarial-spec.prompt.md` | Prompt | Una o dos veces por feature, en Fase 4. | Cuestiona la spec en busca de ambigüedades, gaps, supuestos no declarados, casos borde olvidados. |
| `prompts/04-codegen-layer.prompt.md` | Prompt | 4 veces por feature (una por capa), en Fase 6. | Genera el código de una capa específica (datos, negocio, API o UI) usando un protocolo de 3 pasos. |
| `prompts/05-adversarial-code.prompt.md` | Prompt | 4 veces por feature (una por capa), en Fase 6. | Cuestiona el código generado contra la spec y contra principios de seguridad y diseño. |
| `prompts/06-spec-verification.prompt.md` | Prompt | Una vez por feature, en Fase 5 (entre aprobación y codegen). | Verifica preparación operativa de la spec antes de empezar codegen. Devuelve veredicto VERDE / AMARILLO / ROJO. |

### Templates de setup foundacional (6 artefactos)

Estos templates se usan principalmente durante Fase 0 paso 2. Definen la estructura de los 6 archivos del setup foundacional. Después del setup, se actualizan reactivamente cuando algo cambia en el proyecto.

| Artefacto | Tipo | Cuándo se usa | Para qué sirve |
|-----------|------|---------------|----------------|
| `templates/product-spec.template.md` | Template | Cargado en prompt 00b. | Esqueleto del `PRODUCT.md`. Define qué es el producto, para quién, qué problema resuelve. |
| `templates/architecture.template.md` | Template | Cargado en prompt 00b. | Esqueleto del `ARCHITECTURE.md`. Define stack, patrón arquitectónico, decisiones técnicas. Híbrido: parte descriptiva + parte decisional. |
| `templates/domain-model.template.md` | Template | Cargado en prompt 00b. | Esqueleto del `DOMAIN_MODEL.md`. Define entidades core del dominio, atributos y relaciones. |
| `templates/conventions.template.md` | Template | Cargado en prompt 00b. | Esqueleto del `CONVENTIONS.md`. Define naming, estructura de carpetas, patrones de código. |
| `templates/glossary.template.md` | Template | Cargado en prompt 00b. | Esqueleto del `GLOSSARY.md`. Define términos del dominio con definición precisa. |
| `templates/principles.template.md` | Template | Cargado en prompt 00b. | Esqueleto del `PRINCIPLES.md`. Define políticas transversales (seguridad, logging, performance, etc.). |

### Templates de spec de feature (2 artefactos)

| Artefacto | Tipo | Cuándo se usa | Para qué sirve |
|-----------|------|---------------|----------------|
| `templates/feature-spec.template.md` | Template | Cargado en prompts 02, 03, 06. | Esqueleto de una spec de feature. 15 secciones estandarizadas. |
| `templates/feature-spec.guide.md` | Template auxiliar | Cargado en prompts 02, 03, 06. | Guía detallada de qué contenido va en cada sección de la spec. Es la referencia conceptual del template. |

### Templates de proyecto (2 artefactos)

| Artefacto | Tipo | Cuándo se usa | Para qué sirve |
|-----------|------|---------------|----------------|
| `templates/project-index.template.md` | Template | Una vez al inicio del proyecto, después de Fase 0. | Esqueleto del `INDEX.md` del proyecto. Bookkeeping operativo: asignación de IDs, estados de specs, dependencias. |
| `templates/project-roadmap.template.md` | Template | Cargado en prompt 00b. | Esqueleto del `ROADMAP.md`. Visión estratégica del proyecto: specs agrupadas por fase con estimación gruesa. |

### Template de ADR (1 artefacto, uso reactivo)

| Artefacto | Tipo | Cuándo se usa | Para qué sirve |
|-----------|------|---------------|----------------|
| `templates/adr.template.md` | Template | Reactivo. Cuando aparece una decisión arquitectónica importante durante el desarrollo. | Esqueleto de un ADR (Architecture Decision Record). Documenta decisiones arquitectónicas individuales con contexto, alternativas y consecuencias. NO se usa en Fase 0 (esas decisiones viven en `ARCHITECTURE.md`). |

### Template de design system (1 artefacto, transversal)

| Artefacto | Tipo | Cuándo se usa | Para qué sirve |
|-----------|------|---------------|----------------|
| `templates/design-system.template.md` | Documento transversal | Cargado en prompt 00c y en codegen de Capa 4 (UI). | Define el design system del autor: identidad visual, tipografía, componentes base, patrones de UX. Es transversal a todos los proyectos. Las decisiones del autor están consolidadas; no se "instancia" por proyecto. |

### Protocolos (1 artefacto)

| Artefacto | Tipo | Cuándo se usa | Para qué sirve |
|-----------|------|---------------|----------------|
| `protocols/codegen-protocol.md` | Protocolo operativo | Referencia constante durante Fase 6. | Checklist operativo de las 4 capas, manejo de problemas, pasos de deploy. Es el "checklist físico" que el autor consulta durante codegen. |

### Documentación del proceso (5 artefactos)

| Artefacto | Tipo | Cuándo se usa | Para qué sirve |
|-----------|------|---------------|----------------|
| `docs/process-overview.md` | Documento de referencia | Cuando se necesita una vista rápida del proceso. | Mermaid simplificado del proceso completo. Renderiza inline en GitHub. |
| `docs/process-diagram.svg` | Documento de referencia | Cuando se necesita la vista detallada del proceso. | SVG completo con los 21 artefactos del proceso, colores por categoría, información operativa por paso. |
| `docs/flow-fase-0.svg` | Documento de referencia | Cuando se ejecuta Fase 0. | Diagrama de flujo paso a paso de Fase 0. |
| `docs/flow-ciclo-feature.svg` | Documento de referencia | Cuando se ejecuta el ciclo de una feature. | Diagrama de flujo paso a paso del ciclo de feature (Fases 1-5). |
| `docs/flow-codegen-deploy.svg` | Documento de referencia | Cuando se ejecuta Fase 6 y deploy. | Diagrama de flujo paso a paso de codegen por capas + deploy a staging y producción. |
| `docs/artifacts-usage-guide.md` | Documento de referencia | Cuando se necesita consultar qué artefacto usar en cada momento. | Este mismo documento. |

---

## Notas operativas

**Sobre adjuntar archivos en cada conversación:**

Los prompts del toolkit están diseñados asumiendo que cada conversación es nueva y aislada. La IA no tiene memoria entre sesiones. Por eso cada prompt declara explícitamente qué archivos hay que adjuntar.

Regla general:
- **Prompts de Fase 0:** se adjuntan templates del toolkit.
- **Prompts del ciclo de feature:** se adjuntan archivos del proyecto (spec, setup foundacional, dependencias).
- **Para codegen (Capas 2-4):** se adjunta también el código aprobado de capas anteriores.

**Sobre conversaciones nuevas vs continuación:**

Casi todos los prompts requieren conversación NUEVA, sin contexto previo. La razón: cuando una misma conversación tiene varios roles (Interrogador, Redactor, Adversario, Generador), el LLM mantiene sesgo del rol anterior. Sesiones aisladas mantienen objetividad.

**Excepción:** durante codegen, las 4 capas pueden hacerse en una misma sesión si se usa Claude Code (que mantiene contexto del proyecto). Si se usa Claude.ai, cada capa requiere su propia sesión con el código de capas anteriores adjuntado.

**Sobre el design system:**

A diferencia de los otros templates, `design-system.template.md` NO se instancia por proyecto. Es un archivo transversal que el autor mantiene en el toolkit y referencia desde los proyectos. Si en algún momento un proyecto requiere override (ej: color corporativo del cliente), ese override se documenta en `ARCHITECTURE.md` del proyecto, no en el design system.

---

## Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260524-v1 | 2026-05-24 | Versión inicial. |
