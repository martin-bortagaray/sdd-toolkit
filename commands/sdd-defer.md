---
description: "WORKFLOW 8.7 — Registrar un pendiente diferido en DEBT.md. Para ideas, deuda técnica o decisiones que surgen y se difieren a propósito. Captura barata, sin frenar la sesión."
argument-hint: "[qué difiero] [tipo opcional: deuda-tecnica|idea-producto|decision-diferida]"
---

Vas a registrar un **pendiente diferido** en `DEBT.md` siguiendo la **Sección 8.7 del WORKFLOW**. Principio: esto es captura barata para no perder algo que decidimos diferir a propósito. **No frena lo que estábamos haciendo** — registrás y seguimos. Si "lo dejo registrado" se dijo en esta sesión, este es el acto concreto que lo cumple.

El pendiente es: **$ARGUMENTS**

## Paso 1 — Clasificá el tipo

Asigná uno de los tres tipos (si te lo pasé en los argumentos, respetalo; si no, inferilo y decímelo):

| Tipo | Cuándo |
|------|--------|
| **deuda-tecnica** | Refactor postergado, hallazgo NO bloqueante de pasada adversaria, spec `Implemented` afectada por un cambio de setup que no corrijo ya. |
| **idea-producto** | Funcionalidad nueva que se charló y se difirió. Su destino natural es el `ROADMAP.md` o el ciclo SDD vía `/sdd-discovery`. |
| **decision-diferida** | Una decisión técnica o de producto que conscientemente posterga para tomar con más contexto. |

**Frenos (no van a DEBT.md):** si es un **bug**, esto es `/sdd-bugfix`, no defer. Si es un hallazgo **bloqueante** de una pasada adversaria, se corrige ahora, no se difiere. Si cae en uno de estos casos, decímelo y paramos acá.

## Paso 2 — Asegurá que DEBT.md existe

1. `DEBT.md` vive en `sdd/DEBT.md` (raíz del directorio SDD, es transversal al proyecto — no por-spec).
2. Si no existe, crealo desde `${CLAUDE_PLUGIN_ROOT}/templates/debt.template.md` (completá header: proyecto, fecha, versión `YYYYMMDD-v1`) y dejalo sin la entrada de ejemplo `DEBT-001`.

## Paso 3 — Agregá la entrada

1. **ID secuencial:** mirá las entradas existentes en `sdd/DEBT.md` y tomá el próximo `DEBT-NNN`.
2. Agregá la entrada completa en la sección **Pendientes**, con estado inicial **Abierto**, usando el bloque del template: Qué es / Por qué se difirió / Destino propuesto. Redactá el "Qué es" para que se entienda **en frío** dentro de seis meses, sin el contexto de esta sesión.
3. Agregá la fila correspondiente en la **tabla de índice** (ID, fecha, tipo, título, Estado=Abierto, Destino=—).
4. Si el origen es claro (ej: "pasada adversaria de código de tal capa", "discovery de tal feature"), anotalo en el campo **Origen**.

## Paso 4 — Confirmá y seguí

Decime en una línea qué registraste (`DEBT-NNN — título`, tipo) y **retomamos lo que estábamos haciendo**. No commitees ni cambies de tarea por esto.

> **Más adelante:** los pendientes `Abierto` se promueven (a spec vía `/sdd-discovery`, a `ROADMAP.md`, o a `bugfix-NNN.md`), se resuelven o se descartan. La revisión periódica que mantiene esos estados al día es `/sdd-debt-review`.
