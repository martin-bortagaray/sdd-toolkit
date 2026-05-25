# INDEX — Specs del proyecto

> **Propósito:** registro centralizado de todas las specs del proyecto. Fuente única de verdad para asignar IDs y para conocer el estado del grafo de specs.
>
> **Ubicación:** `specs/INDEX.md` (un archivo por proyecto, no por dominio).
>
> **Mantenimiento:** manual. El autor lo actualiza en cuatro momentos clave del ciclo de vida de cada spec:
> 1. Al crear la spec (fila nueva con estado `Draft`).
> 2. Al aprobarla (cambiar estado de `Review` a `Approved`).
> 3. Al implementarla (cambiar estado de `Approved` a `Implemented`).
> 4. Al deprecarla (cambiar estado a `Deprecated`).
>
> Las transiciones intermedias (`Draft → Review`) no requieren actualización del INDEX. La spec puede estar varios días en Review mientras se procesa la pasada adversaria; durante ese tiempo, el INDEX la sigue mostrando como `Draft` y eso es aceptable.

---

## Tabla de specs

| ID | Dominio | Título | Estado | Versión | Fecha modificación | Autor | Dependencias directas |
|----|---------|--------|--------|---------|--------------------|----|-----------------------|
| <DOMINIO>-001 | <dominio> | <Título de la feature> | Draft | YYYYMMDD-v1 | YYYY-MM-DD | <autor> | <ID-X>, <ID-Y> |

---

## Convenciones de uso

### Asignación de ID

- Los IDs son secuenciales por proyecto, **no** por dominio. Si la última spec creada es `LOTES-007` y la nueva es de dominio "aplicaciones", el próximo ID es `APLICACIONES-008`.
- Formato del número: 3 dígitos con ceros a la izquierda (`001`, `002`, ..., `099`, `100`).
- Dominio en mayúsculas. Ejemplos: `LOTES`, `APLICACIONES`, `COSECHAS`, `AUTH`, `REPORTES`.

### Estado

Los estados válidos son: `Draft`, `Review`, `Approved`, `Implemented`, `Deprecated`.

Definidos en `WORKFLOW.md` sección 8.4. La columna del INDEX se actualiza al cambiar de estado en los cuatro momentos clave indicados arriba.

### Versión

Formato `YYYYMMDD-vN`. Refleja la última versión de la spec que existe (la del archivo `<id>.md`, no la última que se aprobó).

### Fecha modificación

Fecha del último cambio significativo en la spec (creación, aprobación, modificación post-Implemented). Formato `YYYY-MM-DD`.

### Dependencias directas

- Lista separada por comas: `LOTES-001, AUTH-002, UI-003`.
- **Solo primer nivel directo.** Si esta spec depende de `LOTES-001` y `LOTES-001` depende de `AUTH-002`, esta spec lista solo `LOTES-001`, no `AUTH-002`. (Coherente con WORKFLOW.md sección 6.2.7.)
- Si no tiene dependencias declaradas, dejar vacío o escribir `—`.

---

## Cómo crear este archivo en un proyecto nuevo

1. Copiar este template a `specs/INDEX.md` en el repo del proyecto.
2. Eliminar este bloque "Cómo crear este archivo" y la fila de ejemplo de la tabla.
3. Guardar.
4. La primera spec del proyecto va a llevar número `001`.

---

## Notas operativas

- **Si te olvidás de actualizar el INDEX en una transición clave:** activá Regla 5 del WORKFLOW. Sincronizá el INDEX con el estado real del repo (releer los archivos de `specs/`), documentá la desincronización y entendé por qué pasó.

- **No usar este INDEX para resolver dependencias transitivas.** Si necesitás ver "todas las specs que indirectamente dependen de X", el INDEX no es la herramienta. Esa información, si es importante, vive en `DOMAIN_MODEL.md` o `ARCHITECTURE.md`.

- **No commitear specs hasta que estén en estado `Approved`.** El INDEX solo debe contener referencias a archivos que existen en el repo. Las specs en `Draft` y `Review` viven como archivos locales hasta aprobarse, y al aprobarse se commitean junto con la actualización del INDEX.

- **Specs deprecadas:** se mantienen en el INDEX con estado `Deprecated`. No se borran. La trazabilidad histórica importa.
