# CODEGEN PROTOCOL — Protocolo de Generación de Código por Capas

> **Versión:** 20260602-v4
> **Toolkit:** sdd-toolkit
> **Propósito:** Referencia rápida para usar durante Fase 6 (generación de código). No es un prompt para la IA. Es el checklist operativo del autor para ejecutar Fase 6 correctamente.

---

## Antes de empezar Fase 6

- [ ] La spec tiene estado `Approved`.
- [ ] El prompt `06-spec-verification.prompt.md` fue ejecutado con veredicto **VERDE** o **AMARILLO aceptado conscientemente** (con decisión registrada en sección 10.1 de la spec).
- [ ] El INDEX del proyecto (`specs/INDEX.md`) tiene la spec en estado `Approved`.

---

## Flujo por capa

```
Para cada capa (1 → 2 → 3 → 4):

  1. GENERAR
     Ejecutar prompt 04-codegen-layer.prompt.md en conversación nueva.
     Cargar: spec + setup foundacional + dependencias + código capas anteriores (si aplica).

  2. REVISAR TABLA COMPARATIVA
     Confirmar tabla antes de pedir que genere código.
     ¿Todos los requerimientos de esta capa están en la tabla?
     Si falta alguno → pedirlo antes de confirmar.

  3. REVISAR CÓDIGO Y TESTS
     Ejecutar checklist de verificación entre capas (abajo).

  4. PASADA ADVERSARIA
     Ejecutar prompt 05-adversarial-code.prompt.md en conversación nueva (o subagente).
     Procesar hallazgos: bloqueantes antes de avanzar, no bloqueantes a DEBT.md.

  5. PASAR A SIGUIENTE CAPA
     Adjuntar código de esta capa como contexto adicional en la siguiente.

Al completar las 4 capas (no capa por capa; ver WORKFLOW.md sección 7.5):

  COMMITEAR la feature completa y verificada.
  Un solo commit por feature, con referencia a spec ID y versión.
  Formato: feat(<spec-id>): <descripción de la feature>
```

---

## Checklist de verificación entre capas

Ejecutar después de revisar el código y antes de la pasada adversaria. **No tildar hasta verificar.**

### Siempre (todas las capas)

- [ ] Tabla comparativa spec vs. código revisada. Todos los ítems de esta capa en estado "Cubierto".
- [ ] Naming y estructura coinciden con `CONVENTIONS.md`.
- [ ] Entidades usadas coinciden con `DOMAIN_MODEL.md`.
- [ ] Políticas de `PRINCIPLES.md` aplicadas en esta capa (autenticación, autorización, validación, logging, manejo de errores).
- [ ] Decisiones técnicas tomadas por defecto revisadas. Cada una aceptada o reemplazada explícitamente.
- [ ] No hay sobre-ingeniería: todo lo generado tiene justificación en spec o convenciones.
- [ ] Tests de esta capa generados, ejecutados y pasan.
- [ ] Pasada adversaria de código ejecutada (en conversación separada).
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
- [ ] El commit de la feature (completa y verificada) está en el branch `feature/<SPEC-ID>`.
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

1. **No saltar la pasada adversaria de código** por "es una capa simple".
2. **No pasar a la siguiente capa hasta que el checklist esté completo.**
3. **No commitear hasta que los tests pasen.**
4. **No modificar el código sin modificar la spec primero** si el cambio es de producto.
5. **No sobre-ingenieriar.** Si no está en la spec, no va.
6. **No pushear directo a main.** Todo pasa por rama de feature o hotfix.

---

## Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260523-v1 | 2026-05-23 | Versión inicial. |
| 20260523-v2 | 2026-05-23 | Agregados pasos de merge a staging y producción en "Al terminar Fase 6". Agregada regla 6 (no pushear directo a main). Coherente con WORKFLOW.md sección 9.6. |
| 20260525-v3 | 2026-05-25 | Corrección de referencias cruzadas residuales del renumerado v7→v8 del WORKFLOW. Línea 106: "sección 7.2" → "sección 8.2". Línea 113: "sección 7.3.1" → "sección 8.3.1". Línea 118: "sección 7.3.1" → "sección 8.3.1". |
| 20260602-v4 | 2026-06-02 | Granularidad de commits corregida a "un commit por feature" (resolución de la contradicción §7.5 vs §11.6 del WORKFLOW a favor de §7.5): el paso COMMITEAR sale del loop por capa y pasa a ejecutarse al completar las 4 capas. Actualizado el checklist "Al terminar Fase 6". Mención de subagente como opción para las pasadas adversarias (WORKFLOW v10/v11). |
