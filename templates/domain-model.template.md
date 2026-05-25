# DOMAIN MODEL — Modelo Conceptual del Dominio

> **Versión:** [YYYYMMDD-vN]
> **Proyecto:** [nombre del proyecto]
> **Última modificación:** [YYYY-MM-DD]

---

## Propósito de este documento

Define las entidades core del dominio del negocio, sus atributos principales y sus relaciones. Es el vocabulario conceptual del proyecto: cuando la spec de una feature menciona "Lote" o "Aplicación", este documento define qué es cada uno.

**No es un schema de base de datos.** Los tipos de dato exactos, restricciones técnicas y decisiones de implementación viven en cada feature spec. Este documento captura el modelo conceptual, no el modelo físico.

---

## Entidades core

> Una entidad core es una entidad que tiene identidad propia en el negocio (existe independientemente de otras entidades) y que múltiples features del producto van a referenciar.
>
> Formato de cada entidad:
> - **Nombre:** en singular, en el idioma del dominio.
> - **Definición:** qué es en términos de negocio, no técnicos.
> - **Atributos principales:** los que definen la identidad de la entidad en el negocio (no todos los atributos de DB). Incluir tipo conceptual: texto, número, fecha, booleano, enum (con valores), referencia a otra entidad.
> - **Relaciones:** con qué otras entidades se relaciona, con qué cardinalidad y qué significa esa relación en el negocio.

---

### [Nombre de entidad 1]

**Definición:** [qué es en el negocio]

**Atributos principales:**
- `nombre_atributo`: [tipo conceptual] — [qué representa]
- `nombre_atributo`: [tipo conceptual] — [qué representa]

**Relaciones:**
- Tiene N → [Entidad X]: [qué significa esta relación en el negocio]
- Pertenece a 1 → [Entidad Y]: [qué significa esta relación en el negocio]

---

### [Nombre de entidad 2]

**Definición:** [qué es en el negocio]

**Atributos principales:**
- `nombre_atributo`: [tipo conceptual] — [qué representa]

**Relaciones:**
- [cardinalidad] → [Entidad X]: [qué significa]

---

## Mapa de relaciones

[Descripción textual o diagrama simple (puede ser ASCII art) del grafo de relaciones entre entidades core. El objetivo es poder ver de un vistazo cómo se conecta el dominio.]

```
[Entidad A] 1 ──── N [Entidad B]
                        │
                        N
                        │
                   [Entidad C]
```

---

## Entidades auxiliares

[Entidades que no tienen identidad propia pero aparecen frecuentemente en el dominio. Ejemplos: tabla de relación N:M, entidad de auditoría global, entidad de configuración. Si no hay, eliminar esta sección.]

---

## Glosario de términos del dominio

[Términos específicos del dominio que tienen un significado preciso en este negocio y que todo el equipo (humano o IA) debe interpretar de la misma manera. Para glosario técnico detallado, ver GLOSSARY.md.]

| Término | Definición |
|---------|------------|
| [término] | [definición precisa en el contexto del negocio] |

---

## Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| YYYYMMDD-v1 | YYYY-MM-DD | Versión inicial. |
