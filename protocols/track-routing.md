# Track Routing — referencia única (todo trabajo)

> Fuente operativa compacta para clasificar **cualquier trabajo** (feature nueva o modificación) y rutear los pasos del ciclo. Los comandos `/sdd-*` referencian este archivo en vez de duplicar la matriz. Detalle conceptual en `workflow/WORKFLOW.md` §8.3.2.
> Desde WORKFLOW v20 reemplaza a los tiers T1/T2/T3 (solo modificaciones) y a los tamaños S/M/L (solo features nuevas): una sola clasificación por riesgo. Equivalencias aproximadas: T1 ≈ Rápido · T2 ≈ Estándar · T3 ≈ Estándar/Completo.

## Clasificación (por riesgo, no por sensación)

- **Rápido:** NO toca modelo de datos (§6), NI reglas de negocio (§7), NI permisos/seguridad/datos sensibles, NI dinero o cálculos económicos, NI contratos externos (integraciones, APIs o formatos que consume otro sistema), NI nada irreversible (borrado o migración de datos), NI un componente compartido o artefacto foundacional (un override local sí califica). Alcance chico: una capacidad, pocos archivos. *Ej: layout, textos, un filtro u orden sobre datos existentes, una vista de solo lectura, validación de formato en un formulario.*
- **Estándar:** toca §6 o §7, o introduce un flujo o una entidad nueva, dentro de una capacidad, sin ningún disparador de Completo. *Ej: campo nuevo persistido, regla nueva o modificada, entidad nueva simple, flujo nuevo de una pantalla.*
- **Completo:** cualquiera de estos disparadores — permisos/seguridad/datos sensibles, dinero o cálculos económicos, contrato externo nuevo o modificado, operación irreversible sobre datos, o tamaño grande (varias entidades nuevas, >~30 decisiones). Si mezcla más de una capacidad funcional → proponer partirla.

**Regla de duda: si dudás entre dos tracks, es el superior.** La IA propone el track con justificación contra estos criterios ("es chico" no es justificación); el autor lo confirma en el primer gate (Modo B). El track va al changelog de la spec y, en modificaciones, al header del CHANGE-SET.

## Qué recorre cada track

| Paso | Rápido | Estándar | Completo |
|------|--------|----------|----------|
| Spec | **Mini-spec** (feature nueva) o **delta** sobre la spec existente + 1 línea de changelog; CHANGE-SET mínimo | Spec-first en lote (`08`) · modificación con `07` + CHANGE-SET | Discovery profundo (`01` → `02`) · modificación con `07` + CHANGE-SET |
| Preguntas de producto | Solo alto impacto (Regla 1) — normalmente ninguna, por definición del track | Lote (G1) | Discovery sección por sección (G1) |
| Revisión de spec | **Ninguna** (Regla 4) — solo checks formales inline (verify **EXPRESS**) | Revisión unificada en subagente: adversaria + verify (**COMPLETO** en nueva; **DELTA** y adversaria acotada al delta en modificación) | Revisión unificada **COMPLETA**; pasada 2 solo si la 1 tuvo bloqueantes |
| Gates humanos | **2:** aprobación única (track + spec/delta + plan) · prueba manual | **3:** G1 · G2+G3 (spec + plan juntos) · G4 | **4:** G1 · G2 · G3 · G4 |
| Código | Tests primero + gate automático entre capas | Ídem | Ídem |
| Revisión de código | Subagente acotado al diff · solo presentación → checks inline (tests + typecheck + diff vs `CONVENTIONS.md`) | Subagente sobre el diff de la feature (acotado al diff del cambio en modificación) | Subagente sobre el diff completo; 2 en paralelo (capas 1-3 / 4) si es grande |
| Prueba manual (§7.5) | Sí, acotada a lo que los tests no cubren | Ídem | Ídem |

**Mini-spec (Rápido, feature nueva):** archivo normal en `sdd/specs/` con ID e INDEX, pero solo §1, §2 en dos líneas, §4, §8 (son los tests), §9 aplicable, §14 y §15 (changelog: una línea con versión y track). Las demás secciones se omiten. Si para escribirla hace falta §6 o §7, no es Rápido.

## Carga selectiva de foundation

### Revisión de spec

Feature nueva Estándar/Completo: todo el foundation. Modificación: siempre `CONVENTIONS.md` + `PRINCIPLES.md`; `DOMAIN_MODEL.md` si el delta toca Capa 1/2; `ARCHITECTURE.md` si toca Capa 2/3 o integraciones; `GLOSSARY.md` solo con términos nuevos; `PRODUCT.md` solo en Completo.

### Revisión de código (una pasada por feature)

La pasada corre **una vez sobre el diff completo**: el contexto es la **unión** de las filas de esta matriz para las capas tocadas (cada documento una sola vez). En el modo manual por capa, una fila por pasada. Nunca se recarga el foundation completo ni la spec completa.

| Capa bajo revisión | Foundation a cargar | Secciones de spec |
|---|---|---|
| 1 — Modelo de datos | `DOMAIN_MODEL`, `CONVENTIONS`, `PRINCIPLES` | §6, §7, §9 |
| 2 — Lógica de negocio | `DOMAIN_MODEL`, `ARCHITECTURE`, `CONVENTIONS`, `PRINCIPLES` | §4, §7, §8, §9, §12 |
| 3 — API / acceso | `ARCHITECTURE`, `CONVENTIONS`, `PRINCIPLES` | §4, §5, §8, §9, §12 |
| 4 — UI | `CONVENTIONS`, `DESIGN_SYSTEM` (si existe), `PRINCIPLES` | §4, §5, §8, §13 |

Transversal: `GLOSSARY.md` solo si se usan/introducen términos nuevos; specs dependientes de §12, solo las relevantes. **`PRODUCT.md` no se carga en la revisión de código.** En modificaciones, acotado al diff del cambio.

## Válvula de escape

El track es una hipótesis, no un permiso. Si en cualquier paso (revisión, codegen, prueba manual) aparece evidencia de que el trabajo toca algo que su track no admite: el track **sube en el acto**, se ejecutan los pasos salteados antes de continuar (ej: Rápido → Estándar en pleno codegen: se frena, se completa la spec, corre la revisión unificada y se aprueba), y la re-clasificación queda en el changelog de la spec con qué la disparó (Regla 5).
