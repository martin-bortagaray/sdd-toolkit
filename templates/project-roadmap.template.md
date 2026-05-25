# ROADMAP — Roadmap del Proyecto

> **Versión:** [YYYYMMDD-vN]
> **Proyecto:** [nombre del proyecto]
> **Última modificación:** [YYYY-MM-DD]

---

## Propósito de este documento

Define la visión estratégica del proyecto: qué features se van a construir, en qué orden, agrupadas en fases con objetivos claros, con estimación gruesa de tamaño.

Es un documento **vivo pero no operativo**: se actualiza cuando hay cambios estratégicos (se agrega/elimina una feature, se reordena el plan), no cuando cambia el estado operativo de una spec individual. Para bookkeeping operativo, ver `INDEX.md`.

**Audiencia:** el autor (para mantener foco estratégico) y el cliente (para entender el plan).

**Relación con la cotización:** este roadmap es input para cotizar fuera del SDD. La cotización formal con precios y condiciones comerciales vive en un documento separado.

---

## Visión del producto

[Una frase que sintetiza el producto. Debe ser consistente con PRODUCT.md sección 1.]

---

## Objetivo del roadmap

[Qué se busca lograr con este plan en términos de producto y negocio. Sin esto, las fases siguientes pierden sentido.]

---

## Convención de tamaño

Las estimaciones de tamaño son gruesas. Sirven para planificación y cotización inicial, no para compromiso temporal preciso.

| Tamaño | Equivalencia aproximada |
|--------|-------------------------|
| Small (S)  | 1 spec simple ~ 4-8 horas de trabajo |
| Medium (M) | 1 spec media ~ 8-16 horas |
| Large (L)  | 1 spec compleja ~ 16-32 horas |

La estimación detallada para cotización formal se hace en documento aparte tomando este roadmap como input.

---

## Fases del proyecto

> **Nota sobre los IDs:** los identificadores de specs en este roadmap son **orientativos**, no definitivos. Se usan etiquetas tipo "Spec A1", "Spec A2", "Spec B1" para mantener el roadmap como documento estratégico independiente de la asignación operativa de IDs.
>
> Los IDs reales (con formato `<DOMINIO>-001`, etc.) se asignan vía el INDEX del proyecto cuando arranca cada spec. Esto evita confusiones cuando una spec real difiere de lo que el roadmap previó al inicio.

### Fase 1 — [Nombre descriptivo de la fase]

**Objetivo:** [En una frase. Qué va a poder hacer el usuario o el sistema al terminar esta fase.]

**Entregable:** [Qué se entrega concretamente al final de la fase. Debe ser algo que el cliente pueda validar.]

**Specs incluidas:**

| Tamaño | Spec | Descripción breve |
|--------|------|-------------------|
| M | Spec A1 | Autenticación de usuarios |
| S | Spec A2 | Gestión de perfiles |
| L | Spec A3 | Dashboard principal |

**Estimación gruesa:** [Total de tamaños sumados, ej: "2S + 3M + 1L"]

**Dependencias:** [Otras fases o factores externos de los que depende esta fase. Si es la primera y no depende de nada, escribir "Ninguna".]

---

### Fase 2 — [Nombre descriptivo]

**Objetivo:** [...]

**Entregable:** [...]

**Specs incluidas:**

| Tamaño | Spec | Descripción breve |
|--------|------|-------------------|
| ... | ... | ... |

**Estimación gruesa:** [...]

**Dependencias:** [Ej: "Requiere Fase 1 completa porque las features de esta fase usan el sistema de auth."]

---

### Fase [N] — [...]

[Mismo formato.]

---

## Resumen total

| Métrica | Valor |
|---------|-------|
| Cantidad de fases | [N] |
| Cantidad total de specs | [N] |
| Tamaño total estimado | [Ej: "8S + 12M + 4L"] |
| Equivalencia en horas (rango) | [Ej: "200-330 horas"] |

---

## Versiones futuras (opcional)

[Features que NO están planeadas para este proyecto pero que pueden ser parte de una versión futura. Documentar acá evita scope creep durante el desarrollo del proyecto actual.]

- [Feature posible para v2]
- [Feature posible para v3]

---

## Cuándo modificar este documento

**Modificar cuando:**

- Se agrega una feature nueva al alcance del proyecto.
- Se elimina una feature planificada.
- Se reordena el plan (una fase pasa antes que otra, una spec cambia de fase).
- Cambia el tamaño estimado de una fase de forma significativa.
- Se actualiza la visión del producto.

**NO modificar cuando:**

- Una spec cambia de estado (Draft → Approved, etc.). Eso es INDEX.
- Se aprueba o se implementa una spec. Eso es INDEX.
- Hay cambios menores en una spec individual.

## Trazabilidad de cambios

Cada cambio significativo al roadmap se registra en el changelog con descripción de qué cambió y por qué. Esto permite ver la evolución del plan a lo largo del proyecto.

---

## Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| YYYYMMDD-v1 | YYYY-MM-DD | Versión inicial. |
