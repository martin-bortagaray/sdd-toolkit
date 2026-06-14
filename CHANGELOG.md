# CHANGELOG — sdd-toolkit

> Historia de versiones centralizada de los artefactos operativos del toolkit (workflow, prompts, protocolos).
> Antes vivía embebida en cada archivo; se centralizó acá para reducir el contexto que el agente carga en cada invocación (ver `docs/PLAYBOOK.md` / optimización de tokens). Cada artefacto conserva solo su `Versión:` actual en el header.
>
> Los `templates/` mantienen su propio changelog inline (no se cargan en cada invocación del flujo).

---

## workflow/WORKFLOW.md

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260520-v1 | 2026-05-20 | Versión inicial del documento. |
| 20260520-v2 | 2026-05-20 | Resultados de primera pasada adversaria. |
| 20260521-v3 | 2026-05-21 | Resultados de segunda pasada adversaria. |
| 20260522-v4 | 2026-05-22 | Cambios incorporados del análisis del ebook "Agentic Engineer" de LIDR: nueva sección 2.6 sobre riesgo de validación circular; nueva sub-sección 6.4.2 con la lista explícita de lo que la pasada adversaria del código NO puede validar; nuevo antipatrón "validación circular silenciosa" en 10.1. Cambios pendientes incorporados de pasada adversaria del WORKFLOW v2: agregado item en checklist 10.3 sobre "modifiqué el contenido o solo le di la razón en el chat". |
| 20260523-v5 | 2026-05-23 | Calibración de Regla 4 (sección 2.2): diferencia explícita entre specs de feature (pasada adversaria obligatoria) y artefactos del toolkit (opcional según criterio del autor). Nueva sección INDEX en 9.5: referencia a project-index.template.md como fuente única de verdad para asignación de IDs, estado de specs y grafo de dependencias. |
| 20260523-v6 | 2026-05-23 | Nueva sección 9.6: gestión de ramas. Modelo GitHub Flow simplificado con rama staging dedicada. Cubre estructura de ramas (main, staging, feature/*, hotfix/*), naming conectado a spec IDs, flujo de feature normal, flujo de hotfix, y evolución futura hacia CI/CD y equipos. |
| 20260524-v7 | 2026-05-24 | Nueva sección 5: Fase 0 — Inicio del proyecto. Documenta los 3 pasos (discovery inicial, redacción setup + roadmap, diseño de prototipo) con sus prompts asociados. Renumeración de secciones 6-14 (antes 5-13) y todas las sub-secciones y referencias cruzadas. Sección 4.2 actualizada para reflejar que el setup foundacional se produce automáticamente en Fase 0 (antes era reactivo). Sección 5.4 nueva: design system del autor como transversal a todos los proyectos. Sección 10.5 ampliada: agregada referencia al ROADMAP junto al INDEX, con su rol distintivo. |
| 20260525-v8 | 2026-05-25 | Corrección de 3 referencias cruzadas residuales del renumerado v7. Línea 350: "protocolo de 6.4.1" → "protocolo de 7.4.1". Línea 473: "checklist de 6.4" → "checklist de 7.4". Línea 525 (sección 9.4, diagrama de estados): "ver 7.3.1" → "ver 8.3.1". Corrección de fecha del v3 en el changelog: 20260520-v3 → 20260521-v3 (fecha real de redacción). Detectadas vía verificación con checklist desde Claude Code. Aplica Regla 5 (Errores en spec aprobada: subir versión, documentar). |
| 20260526-v9 | 2026-05-26 | Agregada sección 9: Tratamiento de Bugs (clasificación A/B/C, artefacto bugfix-XXX.md, flujo por severidad, protocolo de generación de fix con IA, test de regresión, impacto en specs existentes). Agregados antipatrones específicos de bugs en sección 12.2. Agregada nota sobre bugfixes en sección 10.4 (ciclo de vida de specs). Renumeradas secciones 9-14 → 10-15 para incorporar la nueva sección 9. Actualizadas todas las referencias cruzadas afectadas. |
| 20260602-v10 | 2026-06-02 | Modelo de roles→herramientas pasado a **híbrido** (sección 11.1): Fases 1-3 en Claude.ai o Claude Code; de Fase 4 en adelante (adversario de spec, verificación, codegen, adversario de código) en Claude Code. Las pasadas adversarias corren en **subagente con contexto limpio**, cumpliendo la regla de "conversación nueva" (sección 3) sin cambiar de herramienta. Empaquetado del proceso como **plugin de Claude Code** (`sdd-toolkit`) con un comando `/sdd-*` por fase, cada uno leyendo su prompt canónico de `prompts/`. Motivación: reducir la fricción de copiar/pegar entre herramientas y aprovechar que Claude Code lee los archivos reales del repo, el schema vivo de la DB y corre los tests directamente. Decisión tomada tras tener el proceso estable y al menos una serie de features as-built (coherente con el principio de sección 11.5 de decidir herramientas después de uso real). |
| 20260602-v11 | 2026-06-02 | Resuelta contradicción interna sobre granularidad de commits en Fase 6 (aplica Regla 5): §7.5 decía "un commit por feature" mientras §11.6 decía "un commit por capa". Se unifica a favor de §7.5 — **un solo commit por feature completa y verificada**. Corregido el paso 2 del flujo de feature en §11.6 y alineados `protocols/codegen-protocol.md` y `prompts/04-codegen-layer.prompt.md`. |
| 20260607-v12 | 2026-06-07 | §8.3: documentado el **CHANGE-SET** (delta estructurado `ADDED/MODIFIED/REMOVED` con capa por ítem) como la señal que acota el codegen en modificaciones, extendiendo a capas 2–4 la protección que la Capa 1 tenía por append-only. Documentado el **riesgo conocido de propagación entre capas** y su mitigación. Alineados `prompts/07-modify-spec.prompt.md` (v2), `prompts/04-codegen-layer.prompt.md` (v3), `protocols/codegen-protocol.md` (v5) y los comandos `/sdd-modify-spec` y `/sdd-codegen`. Diseño adoptado de las delta specs de OpenSpec, adaptado al modelo de spec-única-viva. |
| 20260610-v13 | 2026-06-10 | Nuevo **gate de prueba manual antes del commit** en Fase 6 (nueva sección 7.5; la antigua "Commits" pasa a 7.6). Los tests automáticos validan que el código cumple la spec; la prueba manual valida que la experiencia real es la esperada. El gate deriva un plan de prueba concreto de los criterios de aceptación (sección 8) y casos borde (sección 9) y bloquea el commit hasta confirmación explícita del autor. Extendido a bugs (§9.4 paso 7, §9.6 regla de cierre: reproducir el caso a mano además del test de regresión). Output de Fase 6 y flujo de ramas §11.6 actualizados. Alineados los comandos `/sdd-commit` (nuevo Paso 4 — gate, con override `sin-prueba` para commits de solo docs/chore), `/sdd-codegen` (nuevo Paso 6) y `/sdd-bugfix` (nuevo Paso 5), más `protocols/codegen-protocol.md` (v6) y `prompts/04-codegen-layer.prompt.md` (v4). Motivación: el proceso commiteaba en automático sin verificación manual del autor. |
| 20260613-v15 | 2026-06-13 | Nueva sección 8.7: **Registro de pendientes diferidos (`DEBT.md`)**. Formaliza el archivo `sdd/DEBT.md` (antes solo referenciado ad-hoc en 7.4.1 y 8.4, sin estructura): registro único y acumulativo de ideas, deuda técnica y decisiones que se difieren a propósito durante una sesión, clasificadas por tipo (`deuda-tecnica` / `idea-producto` / `decision-diferida`) y con ciclo de vida (Abierto → Promovido / Resuelto / Descartado). Codifica la **regla de captura "lo dejo registrado obliga a una escritura"** (deja de ser frase conversacional). Nuevo template `templates/debt.template.md` y dos comandos: `/sdd-defer` (captura barata sin frenar la sesión) y `/sdd-debt-review` (revisión periódica que mantiene el estado de cada entrada al día y sincroniza la tabla de índice), ambos registrados en `plugin.json`. Catálogo de `docs/artifacts-usage-guide.md` y guía de bolsillo `docs/PLAYBOOK.md` actualizados. Motivación: las ideas/decisiones diferidas no tenían un destino canónico; "lo dejo registrado" no garantizaba ninguna escritura. |
| 20260614-v16 | 2026-06-14 | **Optimización de eficiencia de las pasadas adversarias** (tiempo y tokens), sin tocar las garantías del método. §8.3.2 "Carga selectiva de contexto": la **pasada adversaria de código pasa a cargar contexto por capa también en builds iniciales** (antes recargaba los 6 documentos foundacionales + la spec completa en cada una de las 4 capas). La carga ahora se acota a lo que la capa bajo revisión toca, según una nueva matriz por capa en `protocols/tier-routing.md`; `PRODUCT.md` deja de cargarse en la pasada de código (es racional de producto, no contrato). La independencia de contexto (separación del generador) se conserva — lo que se reduce es el volumen, no la separación. Alineados `prompts/03-adversarial-spec` (v4), `prompts/05-adversarial-code` (v6), `protocols/tier-routing.md`, y los comandos `/sdd-adversarial-spec` y `/sdd-adversarial-code`. Motivación: la pasada de código era el costo dominante del ciclo (multiplicador ×4 capas) y casi todo era recarga de contexto estático. |
| 20260610-v14 | 2026-06-10 | **Tiers de modificación** (nueva sección 8.3.2): el costo del proceso se vuelve proporcional al radio de daño del cambio, extendiendo a las modificaciones el principio que la sección 9 ya aplicaba a bugs. T1 (cosmético) / T2 (lógica acotada) / T3 (estructural), derivados mecánicamente del CHANGE-SET, con regla de duda hacia arriba y válvula de escape que re-eleva el tier y ejecuta los pasos salteados. Segunda excepción codificada a **Regla 4**: las modificaciones T1 omiten la pasada adversaria de spec (sin riesgo de diseño que auditar; el riesgo de implementación lo cubren tests + checks inline + gate de prueba manual, que no se relaja en ningún tier). **Pasada adversaria 2 ahora condicional** (13.2): solo si la Pasada 1 tuvo bloqueantes — aplica a todo el ciclo, no solo a modificaciones. **Carga selectiva de documentos foundacionales** según el CHANGE-SET en modificaciones. Checklist 7.4 y pre-requisitos de Fase 5 actualizados con las excepciones T1. Alineados `prompts/07-modify-spec` (v3: clasificación de tier en el flujo + fin de la re-emisión de la spec completa cuando corre en Claude Code — edición quirúrgica directa del archivo), `03-adversarial-spec` (v3), `06-spec-verification` (v3: modos delta/express), `04-codegen-layer` (v5), `05-adversarial-code` (v5), `protocols/codegen-protocol.md` (v7) y los comandos `/sdd-modify-spec`, `/sdd-adversarial-spec`, `/sdd-verify`, `/sdd-codegen`, `/sdd-adversarial-code`. Motivación: una modificación cosmética real costó ~1 hora y ~60% de la ventana de tokens recorriendo el mismo camino que un cambio estructural. |

---

## protocols/codegen-protocol.md

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260523-v1 | 2026-05-23 | Versión inicial. |
| 20260523-v2 | 2026-05-23 | Agregados pasos de merge a staging y producción en "Al terminar Fase 6". Agregada regla 6 (no pushear directo a main). Coherente con WORKFLOW.md sección 9.6. |
| 20260525-v3 | 2026-05-25 | Corrección de referencias cruzadas residuales del renumerado v7→v8 del WORKFLOW. Línea 106: "sección 7.2" → "sección 8.2". Línea 113: "sección 7.3.1" → "sección 8.3.1". Línea 118: "sección 7.3.1" → "sección 8.3.1". |
| 20260602-v4 | 2026-06-02 | Granularidad de commits corregida a "un commit por feature" (resolución de la contradicción §7.5 vs §11.6 del WORKFLOW a favor de §7.5): el paso COMMITEAR sale del loop por capa y pasa a ejecutarse al completar las 4 capas. Actualizado el checklist "Al terminar Fase 6". Mención de subagente como opción para las pasadas adversarias (WORKFLOW v10/v11). |
| 20260607-v5 | 2026-06-07 | Soporte de modificaciones acotadas al delta vía CHANGE-SET (pareja de 04-codegen-layer v3 y 07-modify-spec v2). Agregado ítem en "Antes de empezar Fase 6" y dos ítems en el checklist "Siempre": no tocar filas "Sin cambios — no regenerar", y chequeo de RIESGO DE PROPAGACIÓN entre capas. |
| 20260610-v6 | 2026-06-10 | Agregado el **gate de prueba manual** antes del COMMITEAR en el "Flujo por capa" y un ítem en el checklist "Al terminar Fase 6" (WORKFLOW.md sección 7.5 v13). Referencias de granularidad de commit actualizadas a sección 7.6. |
| 20260610-v7 | 2026-06-10 | Soporte de **tiers de modificación** (WORKFLOW v14, 8.3.2): el paso 4 del flujo por capa pasa a "verificación adversaria según tier" (completa T3/builds, acotada al diff T2, checks inline T1); ítems de "Antes de empezar Fase 6" verifican tier en el CHANGE-SET y verify en el modo correcto (con D3); regla 1 de "no se relajan" calibrada — T1 reemplaza (no omite) la pasada por checks inline, con criterio objetivo, sin habilitar el "es una capa simple". |

---

## prompts/00-project-discovery.prompt.md

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260524-v1 | 2026-05-24 | Versión inicial. |

---

## prompts/00b-setup-foundation.prompt.md

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260524-v1 | 2026-05-24 | Versión inicial. |

---

## prompts/00c-design-prototype.prompt.md

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260524-v1 | 2026-05-24 | Versión inicial. |

---

## prompts/01-discovery.prompt.md

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260522-v1 | 2026-05-22 | Versión inicial. |
| 20260523-v2 | 2026-05-23 | Cambios de primera pasada adversaria: volumen reducido a 20-30 para complejas con sugerencia de partir feature (1.1); ejemplo concreto de estructurar vs redactar en output (1.2); detección de feature que debería partirse (3.1); validación circular en discovery (6.1); decisiones por defecto reforzadas sin prohibición absoluta (8.1); continuación de sesiones interrumpidas (Q crítica); pregunta de cierre cambiada a "hasta 3 puntos críticos" (4.1); manejo de setup foundacional incompleto simplificado (3.2); separador visual de notas operativas reforzado (5.1). |
| 20260523-v3 | 2026-05-23 | Quitada toda referencia a "Modo B" del prompt y de las notas operativas, ya que es terminología interna del WORKFLOW que la IA no conoce en conversación nueva. Reemplazado por descripción directa de las reglas. El término "Modo B" se mantiene solo en WORKFLOW.md. |
| 20260602-v4 | 2026-06-02 | Header "Dónde se ejecuta" actualizado al modelo híbrido v10: ejecutable vía comando `/sdd-discovery` en Claude Code, o Claude.ai en conversación nueva. |

---

## prompts/02-draft-spec.prompt.md

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260523-v1 | 2026-05-23 | Versión inicial. |
| 20260523-v2 | 2026-05-23 | Cambios de primera pasada adversaria: alineada nomenclatura "Recomendación de dependencias" con prompt 01 (1.1); aclaración de adjuntar archivos en lugar de pegar texto (2.1); instrucción explícita para sub-sección 10.2 al redactar primer draft (3.2); regla específica para sección 13 con prohibición de eliminar (3.1); verificación 2 en Paso 0 sobre decisiones por defecto del discovery validadas (3.3); regla de adaptación al template sin "mejorar" contenido (4.1); placeholders {TOOLKIT-VERSION} y {NEXT-SPEC-ID} al inicio del prompt (2.2); resumen y documento separados por delimitador visual (5.1); verificación 3 de conversación limpia con confirmación explícita del usuario (6.1); regla fundamental sobre decisiones de producto consolidada al inicio del prompt. Agregado proceso de asignación de ID usando INDEX del proyecto. |
| 20260523-v3 | 2026-05-23 | Quitada referencia a "Modo B" del prompt, ya que es terminología interna del WORKFLOW que la IA no conoce en conversación nueva. Reemplazado por descripción directa de las reglas. El término "Modo B" se mantiene solo en WORKFLOW.md. |
| 20260602-v4 | 2026-06-02 | Header "Dónde se ejecuta" actualizado al modelo híbrido v10: ejecutable vía comando `/sdd-spec` en Claude Code, o Claude.ai en conversación nueva separada del discovery. |

---

## prompts/03-adversarial-spec.prompt.md

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260523-v1 | 2026-05-23 | Versión inicial. |
| 20260602-v2 | 2026-06-02 | Header "Dónde se ejecuta" actualizado al modelo híbrido v10: ejecutable vía comando `/sdd-adversarial-spec` en Claude Code, que corre en subagente con contexto limpio (cumple la regla de conversación nueva sin cambiar de herramienta). |
| 20260614-v4 | 2026-06-14 | **Optimización de eficiencia** (WORKFLOW v16). La **guide (`feature-spec.guide.md`) pasa a ser carga opcional**: la taxonomía de 10 casos borde que esta pasada audita ya está embebida en la categoría 6 del prompt, así que no hace falta adjuntar la guide completa solo por eso (se carga únicamente si hace falta el detalle de qué va en cada sección). **Formato de salida**: el adversario reporta solo las categorías con hallazgos y cierra con una única línea de cobertura listando las categorías revisadas sin hallazgos, en vez de un párrafo "sin hallazgos" por cada una de las 10 — reduce tokens de salida sin perder la constancia de cobertura. |
| 20260610-v3 | 2026-06-10 | **Pasada 2 condicional** codificada (WORKFLOW v14, 13.2): solo si la Pasada 1 tuvo bloqueantes; antes era el camino por defecto. Soporte de **tiers de modificación** (WORKFLOW 8.3.2): T1 no ejecuta este prompt (excepción de Regla 4); T2 corre en nuevo **MODO ACOTADO AL DELTA** (la spec completa es contexto de coherencia, los hallazgos se reportan solo sobre lo que el delta introduce o toca, con foco en propagación; problemas pre-existentes van en una línea a "FUERA DE SCOPE"); T3 pasada completa. **Carga selectiva de contexto** en T2 según el CHANGE-SET (CONVENTIONS+PRINCIPLES siempre; DOMAIN_MODEL/ARCHITECTURE/GLOSSARY según capas tocadas). Corregidas 4 referencias residuales del renumerado v9 del WORKFLOW: 11.2→13.2, 11.3→13.3, 11.1→13.1 (×2, las de calidad de hallazgos; las de "sección 11.1 modelo híbrido" eran correctas). |

---

## prompts/04-codegen-layer.prompt.md

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260523-v1 | 2026-05-23 | Versión inicial. |
| 20260602-v2 | 2026-06-02 | Header "Dónde se ejecuta" actualizado al modelo híbrido v10 (comando `/sdd-codegen`). Nota operativa "Después de cada capa": corregido a "no commitees por capa" — el commit es uno por feature completa y verificada, resolviendo la contradicción §7.5 vs §11.6 a favor de §7.5. |
| 20260607-v3 | 2026-06-07 | Soporte de modificaciones acotadas al delta. Nueva Regla 9 (regenerar solo el delta, preservar el resto cuando hay CHANGE-SET). Columna "Estado en el cambio" en la tabla comparativa (Regla 2). CHANGE-SET agregado como input opcional en CONTEXTO. Paso 0 lee el CHANGE-SET. Cierra el hueco de scope en capas 2–4: antes el prompt pedía "generá la capa completa" también en modificaciones, sin instrucción de preservar lo existente; ahora el comportamiento queda tan acotado como ya lo estaba la Capa 1 por append-only. Pareja de 07-modify-spec.prompt.md v2. |
| 20260610-v4 | 2026-06-10 | Regla 6 actualizada: el commit único exige, además de la verificación de las 4 capas, la **prueba manual del autor** (gate previo al commit, WORKFLOW.md sección 7.5 v13). Referencia de granularidad de commit movida a sección 7.6. |
| 20260610-v5 | 2026-06-10 | Soporte de **tiers de modificación** (WORKFLOW v14, 8.3.2): carga selectiva de documentos foundacionales según el CHANGE-SET (CONVENTIONS+PRINCIPLES siempre; DOMAIN_MODEL/ARCHITECTURE/GLOSSARY/PRODUCT según capas tocadas y tier). El CHANGE-SET ahora trae el tier en el header; instrucción de **válvula de escape** durante la generación (si el delta excede su tier, parar y subir el tier). Pasada adversaria de código post-capa ruteada por tier: checks inline en T1, subagente acotado en T2, completa en T3/builds. Corregidas 3 referencias residuales del renumerado v9 del WORKFLOW: 6.4→7.4 (×2), 7.3.1→8.3.1. |

---

## prompts/05-adversarial-code.prompt.md

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260521-v1 | 2026-05-21 | Versión inicial. |
| 20260522-v2 | 2026-05-22 | Cambios incorporados del análisis del ebook "Agentic Engineer" de LIDR: nueva sección "Advertencia sobre límites" antes del prompt; bloque "ALCANCE DE TU REVISIÓN" dentro del prompt; restricción al final del prompt sobre no cuestionar la spec; nota sobre validación circular en notas operativas. |
| 20260523-v3 | 2026-05-23 | Quitada referencia a "Modo B" de la advertencia sobre validación circular. Reemplazado por "durante el discovery". El término "Modo B" se mantiene solo en WORKFLOW.md. |
| 20260602-v4 | 2026-06-02 | Header "Dónde se ejecuta" actualizado al modelo híbrido v10: ejecutable vía comando `/sdd-adversarial-code` en Claude Code, que corre en subagente con contexto limpio (cumple la regla de conversación nueva sin cambiar de herramienta). |
| 20260614-v6 | 2026-06-14 | **Optimización de eficiencia** (WORKFLOW v16) — el costo dominante del ciclo. **Carga selectiva por capa para todos los builds** (antes solo T2): "Cómo usar" reemplaza la lista fija de 5 docs + spec completa por una matriz capa→foundation/secciones (Capa 1: DOMAIN_MODEL+CONVENTIONS+PRINCIPLES, §6/7/9; Capa 2: +ARCHITECTURE, §4/7/8/9/12; Capa 3: ARCHITECTURE+CONVENTIONS+PRINCIPLES, §4/5/8/9/12; Capa 4: CONVENTIONS+DESIGN_SYSTEM+PRINCIPLES, §4/5/8/13). `PRODUCT.md` deja de cargarse (ya no estaba en la lista, ahora explícito el porqué). **Formato de salida**: reportar solo las categorías con hallazgos + una línea de cobertura final, en vez de un párrafo "sin hallazgos" por cada una de las 8. Motivación: la pasada corre ×4 capas y recargaba todo el foundation estático en cada una. |
| 20260610-v5 | 2026-06-10 | Nueva sección "Cuándo se ejecuta según el tier" (WORKFLOW v14, 8.3.2): en modificaciones **T1** la pasada se reemplaza por checks inline (tests + typecheck + diff contra CONVENTIONS) — el gate de prueba manual sigue siendo obligatorio; en **T2** corre acotada al diff con contexto selectivo según el CHANGE-SET; en **T3 y builds iniciales** corre completa como siempre. Documentada la válvula de escape (hallazgo que excede el tier = bloqueante + tier sube). Corregidas 2 referencias residuales del renumerado v9 del WORKFLOW: 6.4.1→7.4.1, 6.4→7.4. |

---

## prompts/06-spec-verification.prompt.md

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260523-v1 | 2026-05-23 | Versión inicial. |
| 20260602-v2 | 2026-06-02 | Header "Dónde se ejecuta" actualizado al modelo híbrido v10: ejecutable vía comando `/sdd-verify` en Claude Code, o Claude.ai en conversación nueva. |
| 20260610-v3 | 2026-06-10 | Tres **modos de ejecución por tier** (WORKFLOW v14, 8.3.2): COMPLETO (specs nuevas y T3), DELTA (T2: F/C acotados a los ítems del CHANGE-SET, sin re-verificar la base ya aprobada), EXPRESS (T1: solo F1-F3 + chequeos delta + C3/C4/C5 acotados). Nuevos **chequeos delta D1-D3** para modificaciones: versión+changelog con tier, coherencia CHANGE-SET↔spec en ambas direcciones, y **verificación del tier declarado contra el contenido del CHANGE-SET** (D3) — si el delta excede su tier, es bloqueante y dispara la válvula de escape. El verify pasa a ser el punto de control de honestidad de la clasificación. Corregida 1 referencia residual del renumerado v9 del WORKFLOW: 7.3.1→8.3.1. |

---

## prompts/07-modify-spec.prompt.md

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260602-v1 | 2026-06-02 | Versión inicial. Cubre el flujo de WORKFLOW.md sección 8.3 (Modificar spec) con foco en specs Implemented y As-built. |
| 20260607-v2 | 2026-06-07 | Agregado Bloque 3 — CHANGE-SET ESTRUCTURADO (delta machine-readable con secciones ADDED/MODIFIED/REMOVED y etiqueta de capa por ítem). Cierra el hueco de scope en codegen de capas 2–4: el codegen consume el change-set para regenerar solo lo que cambió y preservar el resto. Inspirado en el modelo de delta specs de OpenSpec, adaptado al modelo de spec-única-viva del toolkit (no se crea carpeta de cambio separada). |
| 20260610-v3 | 2026-06-10 | Nuevo **Paso 2 — Clasificación del tier** (T1/T2/T3, WORKFLOW.md 8.3.2): la IA propone con justificación contra criterios objetivos, el autor confirma antes de editar; el tier va al header del CHANGE-SET y al changelog de la spec (Pasos 3-5 renumerados de 2-4). **Bloque 2 deja de re-emitir la spec completa cuando corre en Claude Code:** las ediciones se aplican quirúrgicamente sobre el archivo y el bloque reporta la lista de ediciones; la emisión completa queda solo para el camino Claude.ai. Era el mayor costo de output del flujo de modificación, de cualquier tier. "Después de la modificación" y notas operativas actualizadas con el ruteo por tier y la válvula de escape. |
