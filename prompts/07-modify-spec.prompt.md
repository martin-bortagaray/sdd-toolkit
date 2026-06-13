# Prompt — Modificación de Spec Existente (Fase 3 sobre feature ya implementada)

> **Versión:** 20260610-v3 · historia en `/CHANGELOG.md`
> **Uso:** Cuando una feature ya implementada (o una spec as-built) necesita agregar o cambiar funcionalidad. Es el rol Redactor (WORKFLOW.md sección 3) aplicado a una spec que **ya existe**, no a una nueva. Cubre el flujo de WORKFLOW.md sección 8.3 (Modificar spec).
> **Dónde se ejecuta:** Claude Code (preferido) o conversación nueva con contexto limpio.

---

## Cuándo usar este prompt

- La feature existe y querés **agregar o cambiar** comportamiento, y el sistema hoy se comporta como la spec dice (no es un bug).
- La spec a tocar puede estar en estado **Implemented** o **As-built** (ingeniería inversa).

**Cuándo NO usar este prompt:**
- El sistema no hace lo que la spec dice → es un **bug** → `prompts` de bugfix / `/sdd-bugfix` (Tipo A o B).
- Es una capacidad funcional **nueva e independiente** → es una **spec nueva** → `02-draft-spec.prompt.md`.
- El cambio se repite en varias features o es arquitectónico/de modelo/de principio → primero **modificar el setup foundacional** (WORKFLOW.md sección 8.4), después volver acá.

Si dudás entre "modificación de esta spec" y "spec nueva": si el comportamiento nuevo no tiene sentido sin la feature existente y comparte su modelo de datos, es modificación. Si es una capacidad que pararía sola, es spec nueva.

---

## Pre-requisitos antes de usar este prompt

1. **Discovery del delta hecho** (`01-discovery.prompt.md` / `/sdd-discovery`), acotado a lo que se agrega o cambia — no re-discovery de toda la feature.
2. El output del discovery del delta **no tiene `[PENDIENTE]` sin resolver ni decisiones por defecto sin validar** (mismos pre-requisitos que `02-draft-spec`).
3. Tenés identificada la spec exacta a modificar (su ID y archivo).

---

## Prompt

```
Necesito que actúes como Redactor para MODIFICAR una spec existente, no para crear una nueva. Seguí las reglas de abajo.

CONTEXTO QUE TE PASO:
1. La spec existente a modificar (estado Implemented o As-built), en su versión actual.
2. El output del discovery del delta (qué se agrega o cambia).
3. Setup foundacional del proyecto (PRODUCT, ARCHITECTURE, DOMAIN_MODEL, CONVENTIONS, GLOSSARY, PRINCIPLES).
4. Specs dependientes de primer nivel declaradas en la sección 12 de la spec.
5. La guide del toolkit (feature-spec.guide.md).

REGLA FUNDAMENTAL: NO TOMES DECISIONES DE PRODUCTO. Las decisiones del delta ya están en el discovery. Tu trabajo es trasladarlas a la spec existente, editando con cirugía, no reescribir.

PASO 0 — VERIFICACIONES:

V1 — Sin pendientes en el discovery del delta: buscá "[PENDIENTE". Si hay alguno sin resolver, NO edites. Devolveme "MODIFICACIÓN BLOQUEADA" listando los pendientes (coherente con WORKFLOW.md 2.3 y 5).

V2 — Decisiones por defecto del discovery validadas: cada una debe tener nota "Validado por autor: aceptada / reemplazada por: ...". Si falta alguna, NO edites. Devolveme "MODIFICACIÓN BLOQUEADA" listándolas (WORKFLOW.md Regla 2).

V3 — ¿Es realmente modificación de esta spec? Verificá que el delta:
   - No sea un bug (el sistema hace lo que la spec dice).
   - No sea una capacidad independiente que debería ser spec nueva.
   - No sea un cambio que afecta a varias features (eso va primero al setup foundacional).
   Si detectás cualquiera de estos casos, PARÁ y avisame antes de editar.

PASO 1 — LECTURA CRÍTICA DE LA SPEC EXISTENTE:

Antes de editar, leé la spec existente completa y respondeme en 3-5 líneas:
   - ¿Refleja con precisión el comportamiento actual de la feature?
   - ¿Hay secciones débiles, incompletas o ambiguas (frecuente en specs as-built de ingeniería inversa)?

Si encontrás que la spec existente está incompleta o no captura bien el comportamiento actual: marcámelo. Completar/corregir esa base es parte de esta modificación (espíritu de WORKFLOW.md Regla 5). No construyas el delta encima de una descripción as-built floja sin avisarme.

PASO 2 — CLASIFICACIÓN DEL TIER DE LA MODIFICACIÓN (WORKFLOW.md sección 8.3.2):

Antes de editar, clasificá el delta en un tier y proponémelo con justificación. El tier determina qué pasos del ciclo se ejecutan después (adversaria, verify, adversaria de código).

- T1 — Cosmético/presentación: el delta NO toca el modelo de datos (sección 6), NO toca reglas de negocio (sección 7), NO toca superficie de seguridad (auth, permisos, datos sensibles), NO introduce entidades, flujos ni integraciones. El comportamiento observable cambia solo en presentación: layout, textos, colores, orden visual, formato de salida. Puede tocar cualquier capa de código (un layout de PDF vive en Capa 2): lo que define T1 es la naturaleza del cambio, no la capa.
- T2 — Lógica acotada: toca comportamiento (secciones 4/7/8/9) en funciones existentes, pero NO la sección 6, NO entidades/flujos/integraciones nuevas, NO seguridad.
- T3 — Estructural: toca la sección 6, introduce entidad/flujo/integración nueva, o toca superficie de seguridad.

Reglas de clasificación:
- Si dudás entre dos tiers, proponé el superior (espejo de la regla de bugs: si dudo entre A y B, es B).
- La justificación tiene que citar los criterios objetivos ("no toca sección 6 porque...", "no hay superficie de seguridad porque..."). "Es un cambio chico" no es una justificación.
- Esperá mi confirmación del tier antes de editar (Modo B: vos proponés, yo decido). El tier confirmado va al header del CHANGE-SET (Bloque 3) y a la entrada del changelog.

PASO 3 — EDICIÓN QUIRÚRGICA:

- Editá SOLO las secciones afectadas por el delta. No reescribas secciones que no cambian.
- Para cada sección que tocás, mantené la coherencia con el resto de la spec y con el setup foundacional.
- Lenguaje preciso: "debe/es/tiene", nunca "podría/idealmente". Densidad sobre volumen.
- Si el delta toca el modelo de datos (sección 6): describí el cambio de schema. Recordá que en código se traduce a una NUEVA migración append-only (nunca editar una migración ejecutada).
- Casos borde (sección 9) y criterios de aceptación (sección 8): agregá los que el delta introduce. No borres los existentes salvo que el delta los invalide explícitamente (y si los invalida, decímelo).

PASO 4 — VERSIÓN Y CHANGELOG:

- Subí la versión de la spec: nueva entrada con formato AAAAMMDD-vN (incrementá N respecto a la versión actual).
- Actualizá el campo "Versión" y "Fecha última modificación" de la sección 1 (Metadata).
- Agregá una entrada al changelog (sección 15) que diga: qué secciones cambiaron, qué se agregó/modificó, por qué, y el **tier confirmado** del cambio. Sé concreto: el changelog es la trazabilidad del cambio, incluido qué camino del proceso recorrió.
- Si la spec estaba en estado "As-built", proponé pasarla a "Implemented" con la nueva versión (decisión final del autor).

PASO 5 — DECISIONES POR DEFECTO (sección 14):

Si durante la edición tomaste alguna decisión operativa menor (formato, orden, terminología), listala en sección 14 con estado "Pendiente de validación". NUNCA decisiones de producto. Si no hubo, escribilo literal.

MANEJO DE GAPS:

Si durante la edición descubrís que el delta requiere una decisión de producto que el discovery no cubrió, o entra en conflicto con el setup foundacional o con una spec dependiente: PARÁ, citá el conflicto, y esperá mi decisión. No lo resuelvas con tu criterio.

OUTPUT FINAL — tres bloques separados por delimitador visual:

Bloque 1 — RESUMEN DEL CAMBIO:
   - Tier confirmado y su justificación.
   - Secciones modificadas (lista).
   - Qué se agregó / cambió / quitó en cada una.
   - Versión nueva de la spec.
   - Si detectaste debilidades en la spec existente que corregiste de paso.
   - Hasta 3 puntos a revisar en la pasada adversaria (Fase 4) — omitir si el tier es T1 (la pasada se omite, WORKFLOW.md 8.3.2).

Bloque 2 — EDICIONES APLICADAS:
   - Si estás corriendo en Claude Code (tenés acceso al archivo): aplicá las ediciones quirúrgicas DIRECTAMENTE sobre el archivo de la spec con tu herramienta de edición, y en este bloque reportá la lista de ediciones aplicadas (sección tocada + qué cambió, 1-2 líneas por edición). NO re-emitas la spec completa: ya está en el disco; re-emitir cientos de líneas que no cambiaron es puro costo de output sin valor.
   - Solo si estás en una conversación sin acceso al archivo (Claude.ai): emití la spec modificada completa en markdown, lista para guardar reemplazando el archivo existente.

Bloque 3 — CHANGE-SET ESTRUCTURADO (delta machine-readable para el codegen):

   Este bloque NO es el changelog (el changelog es prosa para humanos y auditoría). El CHANGE-SET es la señal de scope que consume `/sdd-codegen` para regenerar SOLO lo que cambió y preservar el resto. Generalo con este formato exacto:

   ```
   CHANGE-SET — {SPEC-ID} {VERSION-ANTERIOR} → {VERSION-NUEVA}
   Tier: {T1 | T2 | T3} — {justificación en una línea contra los criterios de WORKFLOW.md 8.3.2}

   ## ADDED
   - [Capa N | Sección X, ítem Y] <texto preciso de lo que se agrega>

   ## MODIFIED
   - [Capa N | Sección X, ítem Y] <qué cambia respecto del comportamiento anterior>

   ## REMOVED
   - [Capa N | Sección X, ítem Y] <qué deja de existir>
   ```

   Reglas del CHANGE-SET:
   - Cada ítem se etiqueta con la(s) capa(s) que toca: 1 (datos), 2 (lógica), 3 (API/acceso), 4 (UI). Un ítem puede tocar varias.
   - Solo entran requerimientos (sección 4), reglas de negocio (7), criterios de aceptación (8), casos borde (9) y atributos/relaciones del modelo (6). No metas decisiones operativas menores.
   - Si una capa NO aparece en ningún ítem, esa capa NO se regenera en Fase 6. Decilo explícito al cierre: "Capas sin cambios: [lista]".
   - Si una sección es ADDED o MODIFIED pero el resto de su capa no cambia, el codegen debe preservar lo existente y tocar solo estos ítems (ver Regla 9 de 04-codegen-layer.prompt.md).

NO hagas pasada adversaria en este paso. Eso es Fase 4, con otro prompt.

¿Listo? Empezá por el Paso 0 (verificaciones), el Paso 1 (lectura crítica) y el Paso 2 (propuesta de tier). No edites hasta que yo confirme el tier.
```

---

> **Nota: lo que sigue NO es parte del prompt. Es para mí, no para copiar en la conversación con la IA.**

## Después de la modificación

1. **Lectura crítica de la spec modificada** completa, no solo del delta (Regla 3). Un cambio puede romper coherencia con secciones que no tocaste.
2. **Validar la sección 14** (decisiones por defecto).
3. **Pasada adversaria según tier** (WORKFLOW.md 8.3.2): **T1 la omite** (excepción codificada de Regla 4 — no hay riesgo de diseño que auditar); **T2** corre `/sdd-adversarial-spec` acotada al delta con contexto selectivo; **T3** la corre completa. En T2/T3, la pasada 2 solo se ejecuta si la pasada 1 tuvo bloqueantes (WORKFLOW.md 13.2).
4. **Actualizar el INDEX** del proyecto si cambió el estado de la spec.
5. **Verificación pre-generación** (`/sdd-verify`) en el modo del tier: **express** para T1, **delta** para T2, **completo** para T3.
6. **Codegen del delta** (`/sdd-codegen`): solo las capas que el cambio toca. Si el delta no afecta el modelo de datos, no se regenera Capa 1. **Pasale el CHANGE-SET (Bloque 3) como contexto:** es lo que hace que el codegen regenere solo los ítems ADDED/MODIFIED y preserve el resto del código existente, en vez de reconstruir la capa completa. El tier del header decide además la adversaria de código: checks inline en T1, subagente acotado en T2, completo en T3.

## Notas operativas

- **Specs as-built:** la primera modificación de cada spec reverse-engineered suele revelar que la descripción as-built tiene huecos. Es esperable. Completar esa base es parte del trabajo, no una distracción.
- **No infles el changelog ni la spec.** El cambio se documenta con densidad: qué y por qué, sin relleno.
- **Si el delta crece:** si al editar descubrís que el "cambio chico" toca media spec, pará y reconsiderá si no es en realidad una feature nueva o un cambio que debía ir al setup foundacional.
- **Válvula de escape del tier (WORKFLOW.md 8.3.2):** el tier es una hipótesis, no un permiso. Si en cualquier paso posterior (adversaria, verify, codegen, prueba manual) aparece evidencia de que el delta toca modelo de datos, reglas de negocio o seguridad: el tier sube en el acto, se actualiza el header del CHANGE-SET, se ejecutan los pasos salteados antes de continuar, y la re-clasificación queda en el changelog de la spec.
- **Antipatrón:** clasificar hacia abajo por ansiedad o cansancio. Si la justificación del tier no cita los criterios objetivos, la clasificación está mal hecha.
