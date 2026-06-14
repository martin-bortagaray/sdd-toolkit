# DEBT — Registro de pendientes diferidos del proyecto

> **Versión:** [YYYYMMDD-vN]
> **Proyecto:** [nombre del proyecto]
> **Última modificación:** [YYYY-MM-DD]

---

## Propósito de este documento

Libro único de **pendientes diferidos** del proyecto: cosas que surgieron durante una sesión de trabajo y que **decidí no abordar en el momento**, pero que no quiero perder.

Es un artefacto **acumulativo** (una sola lista que crece) y **operativo**, no estratégico. Captura tres clases de pendientes:

- **Deuda técnica de código** (`deuda-tecnica`): hallazgos NO bloqueantes de las pasadas adversarias, refactors postergados, specs `Implemented` afectadas por un cambio de setup que no corrijo de inmediato (WORKFLOW 7.4.1 y 8.4).
- **Ideas de producto** (`idea-producto`): funcionalidad nueva que se charló a mitad de sesión y se difirió. Cuando madura, se promueve al `ROADMAP.md` o entra al ciclo SDD vía `/sdd-discovery`.
- **Decisiones diferidas** (`decision-diferida`): una decisión (técnica o de producto) que conscientemente se posterga para tomar con más contexto o información.

**Qué NO va acá:**

- Bugs → `sdd/bugs/bugfix-NNN.md` (`/sdd-bugfix`).
- Hallazgos **bloqueantes** de una pasada adversaria → se corrigen en el momento, no se difieren.
- Features ya planificadas del proyecto → `ROADMAP.md`.
- Exclusiones de alcance de una feature → sección 11 de su spec.

> **Regla de captura (WORKFLOW 8.7):** "lo dejo registrado" no es una frase conversacional. Obliga a una entrada concreta en este archivo. Si no quedó acá, no quedó registrado.

---

## Estados de una entrada

| Estado | Significado |
|--------|-------------|
| **Abierto** | Pendiente sin resolver. Estado inicial de toda entrada. |
| **Promovido** | Se convirtió en otro artefacto: spec (`/sdd-discovery`), entrada de `ROADMAP.md`, o `bugfix-NNN.md`. Anotar el destino. |
| **Resuelto** | Se abordó directamente (ej: la deuda técnica se pagó en una sesión posterior). |
| **Descartado** | Se decidió no hacerlo. Anotar por qué — el descarte también es trazabilidad. |

---

## Índice de pendientes

> Tabla de barrido rápido. Una fila por entrada. El detalle vive más abajo.

| ID | Fecha | Tipo | Título | Estado | Destino / Resolución |
|----|-------|------|--------|--------|----------------------|
| DEBT-001 | YYYY-MM-DD | idea-producto | [título corto] | Abierto | — |

---

## Pendientes

### DEBT-001 — [Título corto del pendiente]

> **Fecha:** [YYYY-MM-DD]
> **Tipo:** deuda-tecnica | idea-producto | decision-diferida
> **Estado:** Abierto
> **Origen:** [dónde surgió: ej. "pasada adversaria de código LOTES-003 capa 2", "sesión de codegen", "charla de discovery"]

**Qué es:**
[Descripción del pendiente. Suficiente para que se entienda en frío, dentro de seis meses, sin el contexto de la sesión en que surgió.]

**Por qué se difirió:**
[La razón de no hacerlo ahora. Ej: "fuera del scope de la feature actual", "requiere decidir X primero", "optimización sin impacto inmediato".]

**Destino propuesto:**
[Dónde debería terminar si se aborda: spec nueva, entrada de roadmap, refactor, etc. Si todavía no se sabe, escribir "Por definir".]

---

<!-- Plantilla para nuevas entradas (copiar y completar):

### DEBT-NNN — [Título corto]

> **Fecha:** YYYY-MM-DD
> **Tipo:** deuda-tecnica | idea-producto | decision-diferida
> **Estado:** Abierto
> **Origen:** [...]

**Qué es:**
[...]

**Por qué se difirió:**
[...]

**Destino propuesto:**
[...]

-->

---

## Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| YYYYMMDD-v1 | YYYY-MM-DD | Creación del registro. |
