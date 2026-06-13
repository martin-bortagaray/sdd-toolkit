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
| Adversaria de spec (`/sdd-adversarial-spec`) | **Omitida** (excepción Regla 4) | Acotada al delta | Completa |
| Pasada adversaria 2 | — | Solo si P1 tuvo bloqueantes | Solo si P1 tuvo bloqueantes |
| Verify (`/sdd-verify`) | Modo **express** | Modo **delta** | **Completo** |
| Codegen (`/sdd-codegen`) | Solo capas del CHANGE-SET | Solo capas del CHANGE-SET | Solo capas del CHANGE-SET |
| Adversaria de código | **Checks inline** (tests + typecheck + diff vs `CONVENTIONS.md`) | Subagente acotado al diff | Subagente completo |
| Gate de prueba manual (§7.5) | **Sí** | Sí | Sí |

## Carga selectiva de foundation (modificaciones)

Siempre `CONVENTIONS.md` + `PRINCIPLES.md`. `DOMAIN_MODEL.md` si el delta toca Capa 1/2. `ARCHITECTURE.md` si toca Capa 2/3 o introduce integraciones. `GLOSSARY.md` solo con términos nuevos. `PRODUCT.md` solo en T3. (Builds iniciales: se carga todo.)

## Válvula de escape

El tier es una hipótesis, no un permiso. Si en cualquier paso (adversaria, verify, codegen, prueba manual) aparece evidencia de que el delta toca modelo de datos, reglas de negocio o seguridad fuera de su tier: el tier **sube en el acto**, se actualiza el header del CHANGE-SET, se ejecutan los pasos salteados antes de continuar, y la re-clasificación queda en el changelog de la spec (espíritu de Regla 5).
