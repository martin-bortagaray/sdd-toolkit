# bugfix-XXX — [Título corto del bug]

> **Versión:** YYYYMMDD-v1
> **Estado:** Abierto
> **Severidad:** Crítico | Alto | Medio | Bajo
> **Tipo:** A (implementación) | B (spec) | C (negocio → reclasificar como feature)
> **Spec afectada:** [nombre-spec.md versión YYYYMMDD-vN]

---

## Descripción del bug

[Qué ocurre. Comportamiento observado vs. comportamiento esperado.]

**Comportamiento observado:**
[Lo que hace el sistema.]

**Comportamiento esperado:**
[Lo que debería hacer según la spec.]

---

## Reproducción

[Pasos mínimos para reproducir. Sin ambigüedad.]

1. [Paso 1]
2. [Paso 2]
3. [Resultado que se obtiene]

---

## Root cause

[Causa raíz identificada: dónde y por qué falló.]

> Si aún no está identificada (ej: bug crítico recién registrado), escribir: "**Pendiente. A completar antes de cerrar este bugfix.**"

---

## Criterio de aceptación del fix

[Cómo verifico que el bug está corregido. Redactado como criterio testeable.]

- [ ] [Criterio 1 — verificable]
- [ ] [Criterio 2 — verificable]

---

## Test de regresión

[Descripción del test que se agrega a la suite.]

- **Nombre del test:** `[nombre del test]`
- **Archivo:** `[ruta del archivo de test]`
- **Descripción:** [Qué reproduce y qué verifica. El test debe fallar antes del fix y pasar después.]

> Si aún no está escrito (ej: bug crítico recién registrado), escribir: "**Pendiente. Requerido antes de cerrar este bugfix.**"

---

## Cambios en spec original

> Completar solo si el bug es **Tipo B**. Si es Tipo A, eliminar esta sección.

- **Spec afectada:** [nombre-spec.md]
- **Sección modificada:** [número y título de la sección]
- **Qué cambió:** [descripción del cambio]
- **Nueva versión de la spec:** YYYYMMDD-vN+1

---

## Decisiones tomadas

[Cualquier decisión no obvia que tomé al resolver el bug. Si no hubo decisiones relevantes, escribir "Ninguna".]

---

## Changelog del bugfix

| Versión | Fecha | Cambios |
|---------|-------|---------|
| YYYYMMDD-v1 | YYYY-MM-DD | Creación. Bug identificado y clasificado. |
