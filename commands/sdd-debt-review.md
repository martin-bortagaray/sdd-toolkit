---
description: "WORKFLOW 8.7 — Revisar el registro de pendientes diferidos (DEBT.md): recorrer las entradas, actualizar el estado de cada una (implementado / sigue pendiente / promovido / descartado) y mantener la tabla de índice al día."
argument-hint: "[filtro opcional: tipo o estado, ej. idea-producto | Abierto]"
---

Vas a hacer la **revisión periódica del registro de pendientes diferidos** (`sdd/DEBT.md`), siguiendo la **Sección 8.7 del WORKFLOW**. Objetivo: que el estado de cada entrada refleje la realidad — qué se implementó, qué sigue pendiente, qué se promovió a otro artefacto y qué se descartó. Un registro sin cosecha se vuelve un cementerio; este comando es la cosecha.

Como en el resto del SDD: **no decido por vos**. Propongo un estado para cada entrada con la evidencia que encuentro, y vos confirmás o corregís.

## Paso 1 — Cargá el registro

1. Leé `sdd/DEBT.md`. Si no existe, no hay nada que revisar: avisame y paramos.
2. Si en **$ARGUMENTS** me pasaste un filtro (un tipo como `idea-producto`, o un estado como `Abierto`), acotá la revisión a esas entradas. Sin filtro, revisamos todas las que no estén ya en estado terminal (`Resuelto` / `Descartado`).

## Paso 2 — Recorré entrada por entrada

Para cada entrada en revisión, presentame una fila con: **ID, tipo, título, estado actual** y mi **propuesta de estado nuevo** con su justificación. Para proponer, buscá evidencia barata en el repo:

| Señal que busco | Estado que propongo |
|-----------------|---------------------|
| Existe una spec / código / migración que claramente implementa el pendiente | **Resuelto** (anotar qué lo resolvió) |
| Se convirtió en una spec (`sdd/specs/`), una entrada de `ROADMAP.md` o un `bugfix-NNN.md` | **Promovido** (anotar el destino concreto) |
| No encuentro rastro de que se haya abordado | Sigue **Abierto** |
| Vos me indicás que ya no tiene sentido | **Descartado** (te pido el motivo — el descarte también es trazabilidad) |

> "Si ya se implementó" → normalmente **Resuelto**; o **Promovido** si pasó por una spec que después se implementó (en ese caso el seguimiento fino vive en el INDEX de esa spec, no acá).

No infieras un estado terminal sin evidencia. Ante la duda, lo dejás **Abierto** y me lo marcás para decidir.

## Paso 3 — Aplicá los cambios confirmados

Con mi confirmación, actualizá `sdd/DEBT.md`:

1. En cada entrada tocada: cambiá el campo **Estado** y agregá una línea de **Resolución** (qué lo resolvió / a dónde se promovió / por qué se descartó, con fecha).
2. **Sincronizá la tabla de índice** de arriba: el estado y el destino de cada fila deben coincidir con el detalle. Esta consistencia es el punto del registro.
3. Subí la **versión** de `DEBT.md` y agregá una fila a su changelog resumiendo la revisión (ej: "Revisión: 2 resueltos, 1 promovido a spec LOTES-004, 1 descartado").

## Paso 4 — Resumen

Devolveme un resumen corto: cuántas entradas quedaron en cada estado y cuáles siguen **Abierto** (son las que reclaman acción). Si alguna entrada `Abierto` ya madura para convertirse en trabajo real, recordame el camino: `/sdd-discovery` (feature), entrada de `ROADMAP.md`, o `/sdd-bugfix`.
