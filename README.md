# sdd-toolkit

Toolkit personal de Martin Bortagaray para desarrollo de software asistido por IA, basado en **Spec Driven Development (SDD)**.

---

## Qué es esto

Un conjunto de prompts, templates y documentos de gobierno que estructura el proceso de construcción de software con IA como copiloto. Pensado para uso personal, en proyectos SaaS B2B/B2G donde la velocidad del solo-emprendedor se combina con la disciplina del proceso formal.

**No es un framework reutilizable de la comunidad.** Es un toolkit personal. Refleja decisiones y zonas de riesgo del autor. Si alguien más lo adopta, va a necesitar adaptarlo.

---

## Estructura del repo

```
workflow/        → WORKFLOW.md, el documento que gobierna todo el proceso
prompts/         → 10 prompts del proceso (Fase 0 + ciclo de feature + modificación)
templates/       → 12 templates para instanciar proyectos y specs
protocols/       → Protocolos operativos (codegen)
docs/            → Documentación del proceso (diagramas, guías)
commands/        → Comandos del plugin de Claude Code (uno por fase)
.claude-plugin/  → Manifiestos del plugin y del marketplace
```

---

## Por dónde empezar

Si querés entender el proceso:

1. `docs/process-overview.md` — vista rápida del flujo completo.
2. `workflow/WORKFLOW.md` — el documento maestro con reglas y antipatrones.
3. `docs/artifacts-usage-guide.md` — qué artefacto usar en cada momento.

Si querés ejecutar el proceso en un proyecto nuevo:

1. Leer Fase 0 en `workflow/WORKFLOW.md` (sección 5).
2. Ejecutar `prompts/00-project-discovery.prompt.md` para el discovery inicial.
3. Seguir el flujo desde ahí.

---

## Plugin de Claude Code

El proceso está empaquetado como plugin de Claude Code: un comando por fase, cada uno lee su prompt canónico de `prompts/` (fuente única de verdad) y carga el contexto del proyecto automáticamente.

Instalación:

```
/plugin marketplace add martin-bortagaray/sdd-toolkit
/plugin install sdd-toolkit@sdd-toolkit
```

Comandos disponibles:

| Comando | Fase | Qué hace |
|---------|------|----------|
| `/sdd-discovery` | 2 | Discovery de feature (rol Interrogador) |
| `/sdd-spec` | 3 | Redacción del draft de spec nueva (rol Redactor) |
| `/sdd-modify-spec` | 3 (sobre feature existente) | Modificar una spec Implemented/As-built (agregar/cambiar funcionalidad) |
| `/sdd-adversarial-spec` | 4 | Pasada adversaria de spec (subagente, contexto limpio) |
| `/sdd-verify` | 5→6 | Verificación pre-generación (semáforo VERDE/AMARILLO/ROJO) |
| `/sdd-codegen` | 6 | Generación de código por capas (rol Generador) |
| `/sdd-adversarial-code` | 6 | Pasada adversaria de código (subagente, contexto limpio) |
| `/sdd-bugfix` | §9 | Tratamiento de bug con trazabilidad (clasifica A/B/C) |
| `/sdd-commit` | — | Commit inteligente que detecta convenciones SDD |

El modelo de roles→herramientas es **híbrido** desde WORKFLOW v10 (ver sección 11.1): las fases de pensamiento pueden hacerse en cualquier herramienta; de Fase 4 en adelante el trabajo vive en Claude Code, con las pasadas adversarias corriendo en subagente con contexto limpio.

---

## Versión

WORKFLOW v11 (junio 2026). El toolkit evoluciona con experiencia de uso real. Cada artefacto tiene su propio changelog.
