# CODEGEN PROTOCOL — Protocolo de Generación de Código por Capas

> **Versión:** 20261101-v9 · historia en `/CHANGELOG.md`
> **Toolkit:** sdd-toolkit
> **Propósito:** Referencia rápida para usar durante Fase 6 (generación de código). No es un prompt para la IA. Es el checklist operativo del autor para ejecutar Fase 6 correctamente.

---

## Antes de empezar Fase 6

- [ ] La spec tiene estado `Approved`.
- [ ] El checklist de verificación pre-codegen (`06-spec-verification.prompt.md`, dentro de la revisión unificada de `/sdd-feature` o vía `/sdd-verify`) dio **VERDE** o **AMARILLO aceptado conscientemente** (con decisión registrada en sección 10.1 de la spec).
- [ ] El INDEX del proyecto (`specs/INDEX.md`) tiene la spec en estado `Approved`.
- [ ] **Si es una modificación** (la spec viene de `/sdd-modify-spec`): tenés el **CHANGE-SET** a mano (delta `ADDED/MODIFIED/REMOVED` con capa por ítem y **track en el header**, WORKFLOW.md sección 8.3.2; en track Rápido, uno mínimo: ítems + capa). Solo se generan las capas que el delta toca; las demás no se tocan. Build inicial = sin CHANGE-SET = las 4 capas completas.
- [ ] **Si es una modificación:** el checklist de verify se corrió en el modo del track (express Rápido / delta Estándar / completo Completo) y el chequeo D3 confirmó que el track declarado es consistente con el delta.

---

## Flujo de Fase 6 (MODO FEATURE, por defecto desde WORKFLOW v19)

```
  0. PLAN ÚNICO  (único gate humano antes del código)
     Prompt 04 en MODO FEATURE: una tabla para todas las capas del plan
     (requerimiento/CA → capa → archivos → test que lo cubre) + migraciones
     + archivos existentes que se tocan. Confirmo "plan ok" una vez.
     En track Rápido y Estándar, el plan viene en el mismo gate que la aprobación de spec.

  Para cada capa del plan (1 → 2 → 3 → 4), SIN gate humano entre capas:
     a. Tests de los CA (§8) y casos borde (§9) que tocan la capa → fallan.
     b. Código de la capa (Write/Edit a disco).
     c. GATE AUTOMÁTICO: tests de la capa + suite previa + typecheck/lint/build
        en verde. Máx. 2 intentos de corrección; al tercero, frenar (WORKFLOW 8.2).
     d. Decisiones técnicas por defecto → a la lista acumulada.
     Interrupción solo por: gap de producto, conflicto con foundation,
     válvula de escape de track.

  REVISIÓN DE CÓDIGO — UNA PASADA POR FEATURE (según track)
     Completo / feature nueva Estándar: prompt 05 sobre el diff completo
       (subagente, Sonnet); backend + UI con diff grande → 2 en paralelo.
     Modificación Estándar / Rápido con lógica: subagente acotado al diff.
     Rápido de pura presentación: checks inline.
     Bloqueantes → corregir + re-correr gate automático.
     No bloqueantes → DEBT.md.

  PRUEBA MANUAL (gate, WORKFLOW 7.5) — junto con la validación de las
     decisiones técnicas por defecto acumuladas. Mi "ok" autoriza el commit.

  COMMIT único de la feature: feat(<spec-id>): <descripción>
```

**MODO CAPA (manual):** el flujo anterior sigue disponible con `/sdd-codegen <ID> <capa>` — tabla de la capa → confirmación → código → checklist → pasada adversaria de esa capa → siguiente capa.

---

## Checklist de verificación entre capas

En MODO FEATURE, los ítems mecánicos (tests en verde, typecheck/build) los cubre el **gate automático entre capas**, y el resto se verifica **una vez al cierre de la feature** (lo audita la pasada adversaria de código sobre el diff completo + la validación de decisiones por defecto en G4). En MODO CAPA, ejecutar por capa, antes de la pasada adversaria. **No tildar hasta verificar.**

### Siempre (todas las capas)

- [ ] Tabla comparativa spec vs. código revisada. Todos los ítems de esta capa en estado "Cubierto".
- [ ] **Solo en modificaciones (hay CHANGE-SET):** las filas marcadas "Sin cambios — no regenerar" NO fueron tocadas; el diff solo contiene ítems ADDED/MODIFIED/REMOVED del delta.
- [ ] **Solo en modificaciones — RIESGO DE PROPAGACIÓN:** verificá que ningún ítem "Sin cambios" de esta capa dependa de un ítem MODIFIED/REMOVED de otra capa (ej: lógica de Capa 2 que consume un campo cuyo tipo cambió en Capa 1). Si lo hay, ese ítem dejó de ser "sin cambios": agregalo al CHANGE-SET y regeneralo. Ver WORKFLOW.md sección 8.3.
- [ ] Naming y estructura coinciden con `CONVENTIONS.md`.
- [ ] Entidades usadas coinciden con `DOMAIN_MODEL.md`.
- [ ] Políticas de `PRINCIPLES.md` aplicadas en esta capa (autenticación, autorización, validación, logging, manejo de errores).
- [ ] Decisiones técnicas tomadas por defecto revisadas. Cada una aceptada o reemplazada explícitamente.
- [ ] No hay sobre-ingeniería: todo lo generado tiene justificación en spec o convenciones.
- [ ] Tests de esta capa generados, ejecutados y pasan.
- [ ] Revisión de código ejecutada según track: diff completo (Completo / feature nueva Estándar), subagente acotado al diff (modificación Estándar / Rápido con lógica), o checks inline — tests + typecheck + diff vs CONVENTIONS (Rápido de pura presentación).
- [ ] Hallazgos de pasada adversaria procesados (bloqueantes resueltos, no bloqueantes a DEBT.md o descartados).

### Capa 1 — Modelo de datos

- [ ] Todos los atributos de la spec tienen tipo de dato exacto en el código.
- [ ] Restricciones (obligatorio/opcional, único, longitud) implementadas en el modelo.
- [ ] Relaciones con cardinalidad correcta según spec.
- [ ] Migración generada es append-only (no modifica migraciones existentes).
- [ ] Migración referencia el ID y versión de la spec que la requirió.
- [ ] Schema real de DB después de migración coincide con modelo conceptual de spec.

### Capa 2 — Lógica de negocio

- [ ] Código de Capa 1 cargado como contexto.
- [ ] Schema real de DB cargado como contexto.
- [ ] Cada regla de negocio de sección 7 de la spec tiene implementación verificable.
- [ ] Todos los casos borde de sección 9 tienen manejo explícito en el código.
- [ ] Integraciones externas declaradas en sección 12 implementadas con manejo de error (retry, fallback, o error controlado según `PRINCIPLES.md`).

### Capa 3 — API / Capa de acceso

- [ ] Código de Capas 1 y 2 cargado como contexto.
- [ ] Schema real de DB cargado como contexto.
- [ ] Todos los criterios de aceptación (sección 8) que involucran respuestas HTTP tienen tests de status code y payload.
- [ ] Validación de inputs en capa de entrada (no delegada a capa de servicio).
- [ ] Autenticación y autorización implementadas según `PRINCIPLES.md` y sección 5 de la spec.
- [ ] Errores devuelven estructura consistente definida en `PRINCIPLES.md`.

### Capa 4 — UI

- [ ] Código de Capas 1, 2 y 3 cargado como contexto.
- [ ] Todos los flujos de sección 13 (Notas de implementación) tienen implementación.
- [ ] Estados de carga, error, vacío y éxito implementados para cada flujo.
- [ ] Validaciones en cliente declaradas en sección 13 implementadas.
- [ ] Componentes siguen convenciones de `CONVENTIONS.md`.

---

## Manejo de problemas durante generación

### Si el LLM se desvía de la spec

1. Apuntar a la sección exacta de la spec que se está violando.
2. Pedir cambio quirúrgico, no rehacer.
3. Límite: 2 intentos. Al tercero, revisar si el problema es la spec (WORKFLOW.md sección 8.2).

### Si la spec necesita modificarse durante Fase 6

1. **Frenar generación inmediatamente.**
2. Modificar la spec. Subir versión.
3. Documentar qué cambió y por qué en el changelog de la spec.
4. Si el cambio afecta capas ya generadas: evaluar impacto (WORKFLOW.md sección 8.3.1).
5. Reanudar generación con la spec nueva en contexto.

### Si se encuentra un error estructural en la spec durante Fase 6

Ver WORKFLOW.md sección 8.3.1:
1. La spec retrocede de `Approved` a `Review` con nueva versión.
2. Evaluar si capas ya generadas están afectadas.
3. Si no afectadas: continuar desde capa actual con spec nueva.
4. Si afectadas: revertir código de capas afectadas.
5. Completar Fase 5 nuevamente sobre la nueva versión antes de continuar Fase 6.

### Si la pasada adversaria devuelve hallazgos bloqueantes

1. Corregir en la conversación original de generación (cambio quirúrgico).
2. Re-verificar checklist de la capa afectada.
3. Si el hallazgo afecta una capa anterior ya verificada: volver a esa capa, corregir, re-verificar.

---

## Al terminar Fase 6

- [ ] Las 4 capas tienen todos los ítems del checklist tildados.
- [ ] **Prueba manual del autor realizada y confirmada** (gate previo al commit, WORKFLOW.md sección 7.5): seguí el plan de prueba derivado de los criterios de aceptación y casos borde y el cambio funciona en la experiencia real.
- [ ] El commit de la feature (completa, verificada y probada manualmente) está en el branch `feature/<SPEC-ID>`.
- [ ] Mergear a staging para validación del cliente:
  ```
  git checkout staging && git pull origin staging
  git merge feature/<SPEC-ID>
  git push origin staging
  ```
  → Deploy manual a staging. Notificar al cliente para que valide.
- [ ] Cliente valida en staging y aprueba.
- [ ] Mergear a producción:
  ```
  git checkout main && git pull origin main
  git merge feature/<SPEC-ID>
  git push origin main
  ```
  → Deploy manual a producción.
  ```
  git branch -d feature/<SPEC-ID>
  ```
- [ ] Actualizar INDEX del proyecto: cambiar estado de la spec de `Approved` a `Implemented`.
- [ ] Si durante Fase 6 se modificó el setup foundacional (ARCHITECTURE, DOMAIN_MODEL, CONVENTIONS, PRINCIPLES): evaluar qué otras specs `Implemented` están afectadas y registrar en `DEBT.md` si no se van a corregir de inmediato.

---

## Reglas que no se relajan bajo ninguna circunstancia

1. **No saltar la pasada adversaria de código** por "es una capa simple". Única excepción codificada: track **Rápido de pura presentación** (WORKFLOW.md 8.3.2), donde se **reemplaza** —no se omite— por checks inline (tests + typecheck + diff vs `CONVENTIONS.md`). La diferencia: el track es una clasificación con criterio objetivo verificado por D3, no una sensación de "es simple".
2. **No pasar a la siguiente capa con tests en rojo.** En MODO FEATURE el gate entre capas es automático (tests + typecheck/build); en MODO CAPA, el checklist completo.
3. **No commitear hasta que los tests pasen.**
4. **No modificar el código sin modificar la spec primero** si el cambio es de producto.
5. **No sobre-ingenieriar.** Si no está en la spec, no va.
6. **No pushear directo a main.** Todo pasa por rama de feature o hotfix.
