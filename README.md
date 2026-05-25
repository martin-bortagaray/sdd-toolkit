# sdd-toolkit

Toolkit personal de Martin Bortagaray para desarrollo de software asistido por IA, basado en **Spec Driven Development (SDD)**.

---

## Qué es esto

Un conjunto de prompts, templates y documentos de gobierno que estructura el proceso de construcción de software con IA como copiloto. Pensado para uso personal, en proyectos SaaS B2B/B2G donde la velocidad del solo-emprendedor se combina con la disciplina del proceso formal.

**No es un framework reutilizable de la comunidad.** Es un toolkit personal. Refleja decisiones y zonas de riesgo del autor. Si alguien más lo adopta, va a necesitar adaptarlo.

---

## Estructura del repo

```
workflow/   → WORKFLOW.md, el documento que gobierna todo el proceso
prompts/    → 9 prompts del proceso (Fase 0 + ciclo de feature)
templates/  → 12 templates para instanciar proyectos y specs
protocols/  → Protocolos operativos (codegen)
docs/       → Documentación del proceso (diagramas, guías)
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

## Versión

WORKFLOW v7 (mayo 2026). El toolkit evoluciona con experiencia de uso real. Cada artefacto tiene su propio changelog.
