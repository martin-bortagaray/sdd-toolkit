# Checklist de verificación del toolkit SDD

> **Propósito:** verificar que el repo `sdd-toolkit` refleja correctamente todas las decisiones tomadas durante la sesión de construcción del toolkit base (Bloque A).
>
> **Cómo usar:** abrir Claude Code en el directorio del repo y pegar este checklist con la instrucción: *"Recorré este checklist contra el repo. Para cada ítem, indicá si PASA, FALLA o REQUIERE REVISIÓN MANUAL. Al final, dame un resumen consolidado de qué necesita corregirse, si algo."*

---

## Parte 1 — Estructura del repo

### 1.1 Carpetas raíz

Verificar que existen exactamente estas carpetas en la raíz del repo:

- [ ] `workflow/`
- [ ] `prompts/`
- [ ] `templates/`
- [ ] `protocols/`
- [ ] `docs/`

NO deberían existir otras carpetas en la raíz (salvo `.git/` y archivos de configuración como `.gitignore` si aplica).

### 1.2 Archivos en la raíz

Verificar que existe en la raíz:

- [ ] `README.md`

NO deberían existir otros archivos `.md` en la raíz.

### 1.3 Archivos en `workflow/`

Verificar que existe exactamente:

- [ ] `workflow/WORKFLOW.md`

NO deberían existir otros archivos en esta carpeta.

### 1.4 Archivos en `prompts/`

Verificar que existen exactamente estos 9 archivos:

- [ ] `prompts/00-project-discovery.prompt.md`
- [ ] `prompts/00b-setup-foundation.prompt.md`
- [ ] `prompts/00c-design-prototype.prompt.md`
- [ ] `prompts/01-discovery.prompt.md`
- [ ] `prompts/02-draft-spec.prompt.md`
- [ ] `prompts/03-adversarial-spec.prompt.md`
- [ ] `prompts/04-codegen-layer.prompt.md`
- [ ] `prompts/05-adversarial-code.prompt.md`
- [ ] `prompts/06-spec-verification.prompt.md`

NO deberían existir otros archivos en esta carpeta.

### 1.5 Archivos en `templates/`

Verificar que existen exactamente estos 12 archivos:

- [ ] `templates/feature-spec.template.md`
- [ ] `templates/feature-spec.guide.md`
- [ ] `templates/project-index.template.md`
- [ ] `templates/project-roadmap.template.md`
- [ ] `templates/product-spec.template.md`
- [ ] `templates/architecture.template.md`
- [ ] `templates/domain-model.template.md`
- [ ] `templates/conventions.template.md`
- [ ] `templates/glossary.template.md`
- [ ] `templates/principles.template.md`
- [ ] `templates/adr.template.md`
- [ ] `templates/design-system.template.md`

NO deberían existir otros archivos en esta carpeta.

### 1.6 Archivos en `protocols/`

Verificar que existe exactamente:

- [ ] `protocols/codegen-protocol.md`

NO deberían existir otros archivos en esta carpeta.

### 1.7 Archivos en `docs/`

Verificar que existen exactamente estos 6 archivos:

- [ ] `docs/process-overview.md`
- [ ] `docs/process-diagram.svg`
- [ ] `docs/flow-fase-0.svg`
- [ ] `docs/flow-ciclo-feature.svg`
- [ ] `docs/flow-codegen-deploy.svg`
- [ ] `docs/artifacts-usage-guide.md`

NO deberían existir otros archivos en esta carpeta.

### 1.8 Conteo total

- [ ] Total de archivos en el repo: **30** archivos (1 README + 1 WORKFLOW + 9 prompts + 12 templates + 1 protocolo + 6 docs).

---

## Parte 2 — Versiones de cada artefacto

Cada archivo `.md` debe tener una línea de versión en su encabezado. Verificar las versiones esperadas:

### 2.1 Workflow

- [ ] `workflow/WORKFLOW.md`: versión `20260524-v7`.

### 2.2 Prompts

- [ ] `prompts/00-project-discovery.prompt.md`: versión `20260524-v1`.
- [ ] `prompts/00b-setup-foundation.prompt.md`: versión `20260524-v1`.
- [ ] `prompts/00c-design-prototype.prompt.md`: versión `20260524-v1`.
- [ ] `prompts/01-discovery.prompt.md`: versión `v3` (chequear formato real de fecha).
- [ ] `prompts/02-draft-spec.prompt.md`: versión `v3`.
- [ ] `prompts/03-adversarial-spec.prompt.md`: versión `v1`.
- [ ] `prompts/04-codegen-layer.prompt.md`: versión `20260523-v1`.
- [ ] `prompts/05-adversarial-code.prompt.md`: versión `v3`.
- [ ] `prompts/06-spec-verification.prompt.md`: versión `20260523-v1`.

### 2.3 Templates

- [ ] `templates/feature-spec.template.md`: versión `v2`.
- [ ] `templates/feature-spec.guide.md`: versión `v3`.
- [ ] `templates/project-index.template.md`: versión `v1`.
- [ ] `templates/project-roadmap.template.md`: versión inicial.
- [ ] `templates/product-spec.template.md`: versión inicial.
- [ ] `templates/architecture.template.md`: versión inicial.
- [ ] `templates/domain-model.template.md`: versión inicial.
- [ ] `templates/conventions.template.md`: versión inicial.
- [ ] `templates/glossary.template.md`: versión inicial.
- [ ] `templates/principles.template.md`: versión inicial.
- [ ] `templates/adr.template.md`: versión inicial.
- [ ] `templates/design-system.template.md`: versión `20260524-v1`.

### 2.4 Protocolo

- [ ] `protocols/codegen-protocol.md`: versión `20260523-v2`.

### 2.5 Docs

- [ ] `docs/process-overview.md`: versión `20260523-v1`.
- [ ] `docs/artifacts-usage-guide.md`: versión `20260524-v1`.

---

## Parte 3 — Contenido clave del WORKFLOW v7

Abrir `workflow/WORKFLOW.md` y verificar:

### 3.1 Estructura de secciones

Verificar que existen exactamente estas 14 secciones principales (`## N. ...`):

- [ ] `## 1. Propósito de este documento`
- [ ] `## 2. Principios fundacionales`
- [ ] `## 3. Roles de la IA en mi proceso`
- [ ] `## 4. Setup foundacional de un proyecto nuevo`
- [ ] `## 5. Fase 0 — Inicio del proyecto`
- [ ] `## 6. Ciclo SDD por feature`
- [ ] `## 7. Generación de código por capas`
- [ ] `## 8. Manejo de modificaciones`
- [ ] `## 9. Versionado`
- [ ] `## 10. Herramientas que uso`
- [ ] `## 11. Antipatrones a evitar`
- [ ] `## 12. Pasadas adversarias: cuántas veces iterar`
- [ ] `## 13. Cambios a este documento`
- [ ] `## 14. Changelog`

NO deberían existir secciones con numeración fuera de este rango (no debe haber `## 0`, `## 15`, etc.).

### 3.2 Sub-secciones de Fase 0

Verificar que la sección 5 tiene exactamente estas 4 sub-secciones:

- [ ] `### 5.1 Pasos de Fase 0`
- [ ] `### 5.2 Después de Fase 0`
- [ ] `### 5.3 Cuándo NO ejecutar Fase 0`
- [ ] `### 5.4 Design System del autor`

### 3.3 Sección 10.5 ampliada con ROADMAP

Verificar que la sección 10.5 incluye:

- [ ] Mención explícita al INDEX del proyecto.
- [ ] Mención explícita al ROADMAP del proyecto.
- [ ] Distinción entre INDEX (operativo) y ROADMAP (estratégico).
- [ ] Aclaración de que los IDs en ROADMAP son orientativos.

### 3.4 Las 5 reglas no negociables

Buscar en la sección 2.2 las 5 reglas. Verificar:

- [ ] Regla 1: "IA nunca decide producto sin preguntar primero".
- [ ] Regla 2: "IA marca explícitamente decisiones por defecto".
- [ ] Regla 3: "Leer spec entera antes de aprobar".
- [ ] Regla 4: tiene calibración explícita entre specs de feature (obligatoria) y artefactos del toolkit (opcional).
- [ ] Regla 5: "Errores en spec aprobada: subir versión, documentar".

### 3.5 Changelog

Verificar que el changelog tiene entradas para todas estas versiones:

- [ ] `20260520-v1` (versión inicial)
- [ ] `20260520-v2`
- [ ] `20260521-v3`
- [ ] `20260522-v4`
- [ ] `20260523-v5`
- [ ] `20260523-v6`
- [ ] `20260524-v7`

---

## Parte 4 — Consistencia entre artefactos

### 4.1 Referencias cruzadas en el WORKFLOW

Verificar que NO existen en `WORKFLOW.md` referencias a secciones inexistentes:

- [ ] No hay referencias del tipo "sección 6.4" (debería ser 7.4 después del renumerado).
- [ ] No hay referencias del tipo "sección 6.2" (debería ser 7.2).
- [ ] No hay referencias del tipo "sección 9.5" (debería ser 10.5).
- [ ] No hay referencias del tipo "sección 11" cuando habla de pasadas adversarias (debería ser 12).
- [ ] No hay referencias del tipo "sección 8.3" cuando habla de versionado del toolkit (debería ser 9.3).

Búsqueda sugerida: `grep -n "sección [0-9]" workflow/WORKFLOW.md` y verificar que cada referencia apunta a una sección que existe con ese número.

### 4.2 Prompts del ciclo de feature referencian artefactos correctos

Abrir cada prompt del ciclo y verificar que las referencias a templates existen:

- [ ] `01-discovery.prompt.md` referencia setup foundacional correctamente.
- [ ] `02-draft-spec.prompt.md` referencia `feature-spec.template.md` y `feature-spec.guide.md`.
- [ ] `03-adversarial-spec.prompt.md` referencia `feature-spec.guide.md`.
- [ ] `04-codegen-layer.prompt.md` referencia el setup foundacional y `codegen-protocol.md` indirectamente.
- [ ] `05-adversarial-code.prompt.md` referencia el setup foundacional.
- [ ] `06-spec-verification.prompt.md` referencia `feature-spec.guide.md`.

### 4.3 Prompts de Fase 0 referencian artefactos correctos

- [ ] `00-project-discovery.prompt.md` NO referencia templates específicos (es discovery puro).
- [ ] `00b-setup-foundation.prompt.md` referencia los 7 templates del setup foundacional + roadmap.
- [ ] `00c-design-prototype.prompt.md` referencia `PRODUCT.md`, `DOMAIN_MODEL.md`, `GLOSSARY.md`, `ROADMAP.md` y `design-system.template.md`.

### 4.4 Templates del setup foundacional

Verificar que los 6 templates del setup foundacional tienen:

- [ ] Encabezado con propósito del documento.
- [ ] Estructura con secciones numeradas o subtituladas.
- [ ] Placeholders claros (`[descripción]`, `[YYYYMMDD-vN]`, etc.) que indican qué llenar.
- [ ] Changelog al final con tabla de versiones.

### 4.5 Design system

Abrir `templates/design-system.template.md` y verificar:

- [ ] Sección de tono visual: "Moderno / Minimalista".
- [ ] Modo oscuro como default declarado explícitamente.
- [ ] Color de acento default: indigo, con override por proyecto.
- [ ] Tipografía: Inter (principal) + JetBrains Mono (monoespaciada).
- [ ] Componentes: shadcn/ui core + extensiones para SaaS B2B.
- [ ] Iconos: Lucide.
- [ ] Logo: variable por proyecto.
- [ ] Sección de patrones de UX (navegación, formularios, estados, feedback, atajos de teclado).

### 4.6 Codegen protocol

Abrir `protocols/codegen-protocol.md` y verificar:

- [ ] Sección "Antes de empezar Fase 6" con 3 pre-condiciones.
- [ ] Sección "Flujo por capa" con 6 pasos (generar, revisar tabla, verificar checklist, pasada adversaria, commit, pasar a siguiente capa).
- [ ] Checklist de verificación entre capas con sección "Siempre" + 4 secciones específicas por capa.
- [ ] Sección "Al terminar Fase 6" con pasos de merge a staging y producción.
- [ ] 6 reglas que no se relajan (incluyendo "No pushear directo a main").

---

## Parte 5 — Coherencia con decisiones de diseño

### 5.1 Modo B en prompts

Los prompts del ciclo de feature NO deberían mencionar la terminología "Modo B" en el texto que se pega al LLM (es terminología interna del autor que vive solo en el WORKFLOW). Verificar:

- [ ] El bloque de prompt (entre ` ``` `) de `01-discovery.prompt.md` no menciona "Modo B".
- [ ] El bloque de prompt de `02-draft-spec.prompt.md` no menciona "Modo B".
- [ ] El bloque de prompt de `03-adversarial-spec.prompt.md` no menciona "Modo B".
- [ ] El bloque de prompt de `04-codegen-layer.prompt.md` no menciona "Modo B".
- [ ] El bloque de prompt de `05-adversarial-code.prompt.md` no menciona "Modo B".

El término "Modo B" sí debe aparecer en el WORKFLOW (sección 2.1).

### 5.2 Idempotencia y verificaciones de pre-requisitos

Verificar que estos prompts incluyen verificación de pre-requisitos (Paso 0 o Paso de verificación):

- [ ] `02-draft-spec.prompt.md` verifica que el output del discovery no tiene pendientes.
- [ ] `00b-setup-foundation.prompt.md` verifica que el output del discovery inicial no tiene pendientes ni decisiones por defecto sin validar ni cuestionamientos sin resolver.
- [ ] `06-spec-verification.prompt.md` verifica formalmente la spec.

### 5.3 Estados de spec

El WORKFLOW define 5 estados: Draft, Review, Approved, Implemented, Deprecated. Verificar:

- [ ] Sección 9.4 del WORKFLOW define los 5 estados.
- [ ] `templates/project-index.template.md` referencia estos 5 estados.
- [ ] Prompts de feature mencionan transiciones de estado consistentes (`02-draft-spec` → Draft, `03-adversarial-spec` → Review, `06-spec-verification` → Approved).

### 5.4 IDs orientativos en roadmap

Abrir `templates/project-roadmap.template.md` y verificar:

- [ ] Existe nota explícita de que los IDs son orientativos, no definitivos.
- [ ] Sugiere formato tipo "Spec A1", "Spec A2" (no formato `<DOMINIO>-001`).

Abrir `prompts/00b-setup-foundation.prompt.md` y verificar:

- [ ] Sección sobre ROADMAP indica que los IDs son orientativos.

---

## Parte 6 — Calidad del repo

### 6.1 README

Abrir `README.md` y verificar:

- [ ] Existe y tiene contenido significativo (no es placeholder).
- [ ] Describe qué es el toolkit en máximo 2 párrafos al inicio.
- [ ] Tiene sección "Estructura del repo" con descripción de cada carpeta.
- [ ] Tiene sección "Por dónde empezar" que apunta a archivos clave.
- [ ] Menciona la versión del WORKFLOW.

### 6.2 Tag de versión

Verificar:

- [ ] Existe tag `v1.0.0` en el repo (`git tag -l`).
- [ ] El tag apunta a un commit que incluye todos los archivos del toolkit.

Si no existe el tag, ejecutar:
```bash
git tag -a v1.0.0 -m "Toolkit base v1 — Bloque A completo"
git push origin v1.0.0
```

### 6.3 Diagramas SVG

Verificar que los 4 SVG en `docs/` se renderizan correctamente al abrirlos:

- [ ] `docs/process-diagram.svg` muestra el diagrama del proceso completo con colores.
- [ ] `docs/flow-fase-0.svg` muestra el flujo de Fase 0.
- [ ] `docs/flow-ciclo-feature.svg` muestra el flujo del ciclo de feature.
- [ ] `docs/flow-codegen-deploy.svg` muestra el flujo de codegen y deploy.

### 6.4 Mermaid en GitHub

Si el repo está en GitHub:

- [ ] Abrir `docs/process-overview.md` en GitHub y verificar que el diagrama Mermaid se renderiza inline.

---

## Parte 7 — Reporte final

Después de recorrer todos los ítems, generá un reporte consolidado con esta estructura:

```
═══════════════════════════════════════════════
REPORTE DE VERIFICACIÓN DEL TOOLKIT SDD
═══════════════════════════════════════════════

Total de ítems verificados: [N]
Ítems PASA: [N]
Ítems FALLA: [N]
Ítems REQUIEREN REVISIÓN MANUAL: [N]

═══════════════════════════════════════════════
ÍTEMS QUE FALLARON
═══════════════════════════════════════════════

[Lista de cada ítem que falló con descripción concreta de qué se encontró vs qué se esperaba]

═══════════════════════════════════════════════
ÍTEMS QUE REQUIEREN REVISIÓN MANUAL
═══════════════════════════════════════════════

[Lista de ítems que no pueden verificarse automáticamente y requieren ojo humano]

═══════════════════════════════════════════════
VEREDICTO
═══════════════════════════════════════════════

[VERDE / AMARILLO / ROJO]

- VERDE: todo está en orden, el toolkit refleja las decisiones de la sesión.
- AMARILLO: hay diferencias menores que vale revisar pero no bloquean uso del toolkit.
- ROJO: hay diferencias estructurales o de contenido que vale corregir antes de usar el toolkit.

═══════════════════════════════════════════════
SUGERENCIAS DE CORRECCIÓN
═══════════════════════════════════════════════

[Para cada ítem que falló o requiere atención, sugerencia concreta de qué hacer]
```

---

## Notas operativas

**Sobre falsos positivos:**
Si algún ítem aparece como "FALLA" pero después de revisar manualmente se ve que el contenido es correcto pero está expresado distinto a lo que el checklist espera, marcarlo como "PASA con observación".

**Sobre actualizaciones futuras del checklist:**
Este checklist refleja el estado del toolkit al cierre del Bloque A (versión inicial). Cuando se agreguen artefactos o se modifique la estructura, actualizar este checklist en consecuencia.

**Sobre qué hacer si hay muchas fallas:**
Si el reporte devuelve veredicto ROJO con muchas fallas estructurales, NO empezar a corregir uno por uno. Volver a esta conversación con el reporte y vemos cómo resolver de forma consolidada.
