# Tier Routing — referencia única (modificaciones)

> Fuente operativa compacta para clasificar una modificación y rutear los pasos del ciclo. Los comandos `/sdd-*` referencian este archivo en vez de duplicar la matriz. Detalle conceptual completo en `workflow/WORKFLOW.md` §8.3.2.
> Aplica **solo a modificaciones** (flujo `/sdd-modify-spec`, hay CHANGE-SET). Builds iniciales (sin CHANGE-SET) = ciclo completo, sin tiers.

## Clasificación (derivada del CHANGE-SET, no de la sensación)

- **T1 — Cosmético / presentación:** NO toca modelo de datos (§6), NI reglas de negocio (§7), NI seguridad, NI introduce entidades/flujos/integraciones. El comportamiento observable cambia solo en presentación: layout, textos, colores, orden visual, formato de salida.
- **T2 — Lógica acotada:** toca comportamiento (§4/7/8/9) en funciones existentes; sin §6, sin entidades/flujos/integraciones nuevas, sin seguridad.
- **T3 — Estructural:** toca §6 (modelo de datos), introduce entidad/flujo/integración nueva, o toca superficie de seguridad.

**Regla de duda: si dudás entre dos tiers, es el superior.** La IA propone el tier con justificación contra estos criterios objetivos ("es un cambio chico" no es justificación); el autor confirma (Modo B). El tier va al header del CHANGE-SET y al changelog de la spec.

## Pasos por tier

| Paso | T1 | T2 | T3 |
|------|----|----|----|
| Revisión de spec (adversaria + verify en un subagente, Fase B de `/sdd-feature`) | **Omitida** — solo D1–D3 + C3/C4/C5 inline | Acotada al delta | Completa |
| Pasada adversaria 2 | — | Solo si P1 tuvo bloqueantes | Solo si P1 tuvo bloqueantes |
| Modo del checklist de verify (dentro de la revisión) | **Express** | **Delta** | **Completo** |
| Codegen (`/sdd-codegen`) | Solo capas del CHANGE-SET | Solo capas del CHANGE-SET | Solo capas del CHANGE-SET |
| Adversaria de código (una pasada por feature) | **Checks inline** (tests + typecheck + diff vs `CONVENTIONS.md`) | Subagente acotado al diff | Subagente sobre el diff completo |
| Gate de prueba manual (§7.5) | **Sí** | Sí | Sí |

## T1 — carril rápido

T1 ya omite la adversaria de spec; el carril rápido reduce también la **ceremonia**. **Entrada (todo debe cumplirse):** es T1 por los criterios de arriba, no cambia ningún contrato ya documentado (RF/CA/regla/nota §13), y **no toca un componente compartido/foundacional** (si el fix sería editar algo compartido → §8.4 o sube de tier; un override **local** sí califica). **Flujo:** una sola aprobación al inicio (tier + enfoque + delta en 1 línea) → discovery/CHANGE-SET **opcionales**, spec = **1 línea de changelog** (+ nota de sección solo si llena un hueco de doc) → código → checks inline → gate de prueba manual → commit. **Innegociables:** gate de prueba manual y válvula de escape. Detalle en `workflow/WORKFLOW.md` §8.3.2.

## Carga selectiva de foundation

### Pasada adversaria de spec (modificaciones)

Siempre `CONVENTIONS.md` + `PRINCIPLES.md`. `DOMAIN_MODEL.md` si el delta toca Capa 1/2. `ARCHITECTURE.md` si toca Capa 2/3 o introduce integraciones. `GLOSSARY.md` solo con términos nuevos. `PRODUCT.md` solo en T3. (Specs nuevas / T3: se carga todo.)

### Pasada adversaria de código (todos los builds)

Por defecto (v19) la pasada corre **una vez por feature sobre el diff completo**: el contexto es la **unión** de las filas de esta matriz para las capas que la feature tocó (cada documento una sola vez). Con diff grande que toca backend y UI, dos subagentes en paralelo (capas 1-3 / capa 4), cada uno con su fila. En el modo manual por capa, una fila por pasada. Nunca se recarga el foundation completo ni la spec completa: solo lo que las capas bajo revisión tocan. Vale para **builds iniciales y modificaciones** por igual (la independencia de contexto se conserva; lo que se acota es el volumen, no la separación del generador).

| Capa bajo revisión | Foundation a cargar | Secciones de spec |
|---|---|---|
| 1 — Modelo de datos | `DOMAIN_MODEL`, `CONVENTIONS`, `PRINCIPLES` | §6, §7, §9 |
| 2 — Lógica de negocio | `DOMAIN_MODEL`, `ARCHITECTURE`, `CONVENTIONS`, `PRINCIPLES` | §4, §7, §8, §9, §12 |
| 3 — API / acceso | `ARCHITECTURE`, `CONVENTIONS`, `PRINCIPLES` | §4, §5, §8, §9, §12 |
| 4 — UI | `CONVENTIONS`, `DESIGN_SYSTEM` (si existe), `PRINCIPLES` | §4, §5, §8, §13 |

Transversal a todas las capas: `GLOSSARY.md` solo si la capa usa/introduce términos nuevos; specs dependientes de §12, solo las relevantes a la capa. **`PRODUCT.md` no se carga en la pasada de código** (es racional de producto, no contrato de implementación). En modificaciones T2, además: acotado al diff de la capa, no a todo su código.

## Válvula de escape

El tier es una hipótesis, no un permiso. Si en cualquier paso (adversaria, verify, codegen, prueba manual) aparece evidencia de que el delta toca modelo de datos, reglas de negocio o seguridad fuera de su tier: el tier **sube en el acto**, se actualiza el header del CHANGE-SET, se ejecutan los pasos salteados antes de continuar, y la re-clasificación queda en el changelog de la spec (espíritu de Regla 5).
