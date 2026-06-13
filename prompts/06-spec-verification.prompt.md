# Prompt — Verificación de Spec Pre-Generación (Fase 5 → Fase 6)

> **Versión:** 20260610-v3 · historia en `/CHANGELOG.md`
> **Uso:** Después de que la spec está en estado Approved y antes de iniciar Fase 6 (generación de código por capas). Es el "semáforo de salida" del ciclo de especificación.
> **Dónde se ejecuta:** Vía el comando `/sdd-verify` en Claude Code, o en conversación nueva en Claude.ai. Contexto limpio (WORKFLOW.md sección 11.1, modelo híbrido v10).

---

## Cuándo usar este prompt

Este prompt se ejecuta **una sola vez** por spec, después de Fase 5 (aprobación) y antes de Fase 6 (generación). No es una pasada adversaria (eso ya ocurrió en Fase 4). Es verificación de preparación operativa para codegen.

Si el prompt devuelve bloqueantes, resolverlos y volver a ejecutar antes de iniciar generación. Si devuelve solo advertencias, decidir conscientemente si avanzar o resolver primero.

**Tiene tres modos según el tier (WORKFLOW.md 8.3.2):** COMPLETO para specs nuevas y modificaciones T3, DELTA para modificaciones T2, EXPRESS para modificaciones T1. En modificaciones, adjuntar también el CHANGE-SET (con su tier en el header) y aplicar la carga selectiva de documentos foundacionales de 8.3.2.

---

## Cómo usar este prompt

1. Abrir conversación nueva en Claude.ai.

2. **Adjuntar como archivos** (no pegar como texto plano):
   - La spec en estado Approved (`<spec-id>.md`).
   - Setup foundacional del proyecto que exista: `PRODUCT.md`, `ARCHITECTURE.md`, `DOMAIN_MODEL.md`, `CONVENTIONS.md`, `GLOSSARY.md`, `PRINCIPLES.md`.
   - Specs declaradas en la sección 12 "Dependencias y supuestos" de la spec (primer nivel directo).
   - `templates/feature-spec.guide.md` del toolkit (referencia de qué va en cada sección).

3. Pegar el prompt (solo el bloque delimitado por ` ``` `) y enviar.

---

## Prompt

```
Necesito que actúes como verificador de preparación para generación de código. Tu trabajo es determinar si esta spec está lista para iniciar Fase 6 (generación de código por capas) del ciclo SDD.

Este NO es una pasada adversaria. No buscás problemas de contenido ni sugerís mejoras. Verificás que la spec cumple los pre-requisitos formales y que tiene suficiente detalle técnico para que el LLM Generador pueda empezar sin hacer preguntas.

CONTEXTO QUE TE PASO:
1. Spec en estado Approved.
2. Setup foundacional del proyecto (PRODUCT, ARCHITECTURE, DOMAIN_MODEL, CONVENTIONS, GLOSSARY, PRINCIPLES) — los archivos que existan.
3. Specs declaradas como dependencias en sección 12 de la spec (primer nivel directo).
4. Guide del toolkit (feature-spec.guide.md) — referencia de qué va en cada sección.
5. Si es una MODIFICACIÓN: el CHANGE-SET (delta ADDED/MODIFIED/REMOVED con tier en el header).

MODO DE EJECUCIÓN (según tier, WORKFLOW.md sección 8.3.2):

Si te pasé un CHANGE-SET, el modo lo decide su tier. Si no hay CHANGE-SET (spec nueva / build inicial), el modo es COMPLETO.

- MODO COMPLETO (specs nuevas y modificaciones T3): ejecutá Parte 1 (F1-F8) y Parte 2 (C1-C6) completas sobre toda la spec. En modificaciones, ejecutá además los chequeos delta D1-D3.

- MODO DELTA (modificaciones T2): ejecutá F1, F2, F3 y los chequeos delta D1-D3. Ejecutá F5, F6, F7 y C1-C6 ACOTADOS al delta: valen solo sobre los ítems del CHANGE-SET y las secciones que tocan. La base de la spec ya pasó verificación cuando se aprobó; no la re-verifiques entera. En F5/F6 no apliques el mínimo global de 5 escenarios: verificá que cada comportamiento nuevo del delta tenga al menos un criterio de aceptación verificable y sus casos borde aplicables cubiertos.

- MODO EXPRESS (modificaciones T1): ejecutá SOLO F1, F2, F3, los chequeos delta D1-D3, y C3/C4/C5 acotados a los ítems del delta. F4-F8 y C1/C2/C6 se omiten: un delta cosmético no toca modelo, reglas ni stack, y la base ya está verificada.

CHEQUEOS DELTA (solo modificaciones — los tres modos cuando hay CHANGE-SET):

D1. Versión y changelog:
¿La versión de la spec subió respecto a la anterior, y el changelog (sección 15) tiene una entrada que dice qué cambió, por qué, y el tier del cambio?
PASA / FALLA con detalle.

D2. CHANGE-SET coherente con la spec:
¿Cada ítem del CHANGE-SET corresponde a una edición real en la spec, y cada edición sustantiva de la spec está reflejada en el CHANGE-SET? ¿Las capas etiquetadas por ítem son plausibles?
PASA / FALLA listando los desajustes en ambas direcciones.

D3. Tier verificado contra el CHANGE-SET:
¿El contenido del CHANGE-SET respeta los criterios objetivos del tier declarado en su header?
- T1: NO toca sección 6 (modelo) ni sección 7 (reglas de negocio) ni superficie de seguridad, NO introduce entidades/flujos/integraciones.
- T2: NO toca sección 6 ni superficie de seguridad, NO introduce entidades/flujos/integraciones.
PASA si el tier declarado es consistente con el contenido.
FALLA — BLOQUEANTE si el delta excede su tier: el tier debe subir (válvula de escape de WORKFLOW.md 8.3.2) y los pasos salteados (ej: pasada adversaria de spec) deben ejecutarse antes de continuar a Fase 6.

PARTE 1 — CHECKLIST FORMAL:

Verificá cada ítem. Resultado: PASA o FALLA con justificación.

F1. Estado de la spec:
¿El campo "Estado" en la sección 1 (Metadata) dice exactamente "Approved"?
PASA si: dice "Approved".
FALLA si: dice cualquier otra cosa (Draft, Review, Implemented, Deprecated, o está vacío).

F2. Sin pendientes abiertos:
¿La spec contiene alguna aparición de "[PENDIENTE" o "TBD" o "[BLOQUEADO"?
PASA si: no hay ninguna aparición.
FALLA si: hay al menos una aparición. Listá cada una con su sección.

F3. Sección 14 (Decisiones por defecto de la IA) validada:
¿Todas las decisiones en sección 14 tienen estado "Validada por autor" o "Reemplazada"?
PASA si: la sección dice "Sin decisiones por defecto..." O todas las decisiones listadas tienen estado de validación explícito.
FALLA si: alguna decisión tiene estado "Pendiente de validación".

F4. Sección 10.1 (Decisiones explícitas del autor) no vacía:
¿La sección 10.1 tiene al menos una decisión documentada con trade-off?
PASA si: hay al menos una decisión con alternativa descartada y razonamiento.
FALLA si: la sección está vacía, dice "N/A", o tiene solo placeholder.

F5. Criterios de aceptación verificables (sección 8):
¿La sección 8 tiene al menos 5 escenarios en formato Given/When/Then o equivalente verificable?
PASA si: hay 5 o más escenarios verificables.
FALLA si: hay menos de 5, o los criterios no son verificables (no tienen condición + acción + resultado esperado).

F6. Taxonomía de casos borde cubierta (sección 9):
Verificá las 10 categorías de la taxonomía obligatoria (guide §9): concurrencia, límites numéricos, inconsistencia de estado, falla de integración externa, datos vacíos, datos malformados, conexión perdida, sesión expirada, permisos insuficientes, entidad inexistente.
PASA si: cada categoría que aplica tiene al menos un caso documentado, y cada categoría que no aplica tiene "No aplica porque..." con justificación.
FALLA si: alguna categoría aplicable no está cubierta, o alguna exclusión no tiene justificación.

F7. Consistencia con setup foundacional:
¿Las entidades declaradas en sección 6 (Modelo de datos) coinciden con DOMAIN_MODEL.md?
¿La arquitectura asumida en la spec coincide con ARCHITECTURE.md?
¿Los principios de seguridad de la spec respetan PRINCIPLES.md?
PASA si: no hay contradicciones en ninguno de los tres puntos.
FALLA si: hay al menos una contradicción. Citá el fragmento de la spec y el del documento de setup que se contradicen.

F8. Dependencias declaradas son reales:
¿Las specs listadas en sección 12 "Depende de" existen como archivos adjuntos y están en estado Approved o Implemented?
PASA si: todas las dependencias declaradas existen y están en estado correcto.
FALLA si: alguna dependencia declarada no existe, o existe pero está en Draft o Review.

PARTE 2 — VERIFICACIÓN DE PREPARACIÓN PARA CODEGEN:

Verificá cada ítem. Resultado: LISTO, ADVERTENCIA o BLOQUEANTE.

C1. Modelo de datos suficientemente detallado (sección 6):
¿Cada entidad tiene: todos los atributos con nombre exacto, tipo de dato concreto (string, integer, decimal, UUID, timestamp, enum con valores, etc.), restricciones (obligatorio/opcional, único, longitud máxima si aplica), y cardinalidad de todas las relaciones?
LISTO si: todo lo anterior está presente.
ADVERTENCIA si: faltan restricciones menores o longitudes en campos no críticos.
BLOQUEANTE si: faltan tipos de dato, faltan atributos que las reglas de negocio mencionan, o las relaciones no tienen cardinalidad.

C2. Reglas de negocio implementables (sección 7):
¿Cada regla de negocio está expresada con suficiente precisión para traducirla a código sin interpretación?
LISTO si: todas las reglas son precisas y sin ambigüedad.
ADVERTENCIA si: alguna regla menciona conceptos del dominio que no están en GLOSSARY.md (posible ambigüedad).
BLOQUEANTE si: alguna regla usa lenguaje vago ("razonable", "apropiado", "según el caso") sin criterio concreto.

C3. Requerimientos funcionales sin ambigüedad (sección 4):
¿Cada requerimiento funcional es implementable directamente sin interpretación del LLM?
LISTO si: todos los requerimientos son precisos.
ADVERTENCIA si: algún requerimiento tiene alcance ambiguo pero inferible del contexto.
BLOQUEANTE si: algún requerimiento usa "podría", "idealmente", "es estándar", o similar sin concretar.

C4. Casos de error tienen comportamiento definido (sección 9):
¿Para cada caso borde documentado, está definido el comportamiento exacto del sistema (mensaje de error, código HTTP si aplica, estado resultante de la entidad)?
LISTO si: todos los casos tienen comportamiento definido.
ADVERTENCIA si: algún caso tiene comportamiento parcialmente definido (ej: dice que falla pero no el mensaje).
BLOQUEANTE si: algún caso dice "el sistema maneja el error" sin definir cómo.

C5. Notas de implementación suficientes para UI compleja (sección 13):
Si la feature tiene UI compleja (flujos multi-paso, estados visuales, transiciones): ¿la sección 13 describe el comportamiento de interfaz con suficiente detalle?
LISTO si: la feature no tiene UI compleja, o la tiene y sección 13 cubre flujos, estados y transiciones.
ADVERTENCIA si: la feature tiene UI compleja y sección 13 tiene algunas lagunas menores.
BLOQUEANTE si: la feature tiene UI compleja y sección 13 está vacía o dice "No aplica".

C6. Stack tecnológico compatible con la spec:
¿Lo que pide la spec es implementable con el stack declarado en ARCHITECTURE.md (Python + FastAPI + SQLModel / Next.js + TypeScript + Tailwind / Supabase por defecto)?
LISTO si: todo lo que pide la spec es compatible con el stack.
ADVERTENCIA si: algún requerimiento requiere una librería no estándar que habría que agregar.
BLOQUEANTE si: algún requerimiento es incompatible con el stack declarado o requiere cambio arquitectónico.

OUTPUT FINAL:

Generá el reporte en este formato:

---
REPORTE DE VERIFICACIÓN PRE-GENERACIÓN
Spec: [ID y versión]
Modo: [COMPLETO / DELTA / EXPRESS] — [tier, si es modificación]
Fecha: [hoy]
---

PARTE 1 — CHECKLIST FORMAL

[Para cada ítem ejecutado según el modo (F1-F8 y, en modificaciones, D1-D3): "✓ PASA" o "✗ FALLA — [justificación concreta]". Los ítems omitidos por el modo: listalos en una línea como "Omitidos por modo [X]: ..."]

RESULTADO FORMAL: [APROBADO / BLOQUEADO]
Si BLOQUEADO: lista consolidada de ítems que fallaron.

---

PARTE 2 — PREPARACIÓN PARA CODEGEN

[Para cada ítem C1-C6 ejecutado según el modo: "✓ LISTO", "⚠ ADVERTENCIA — [detalle]", o "✗ BLOQUEANTE — [detalle]". En modos DELTA/EXPRESS, acotados al delta.]

RESULTADO CODEGEN: [LISTO PARA INICIAR / INICIAR CON ADVERTENCIAS / BLOQUEADO]

Si BLOQUEADO: no podés iniciar Fase 6 hasta resolver los bloqueantes listados.
Si INICIAR CON ADVERTENCIAS: podés iniciar Fase 6 pero vas a encontrar fricción en [lista de capas afectadas]. Decidí conscientemente.
Si LISTO PARA INICIAR: podés proceder a Fase 6 con `prompts/04-codegen-layer.prompt.md`.

---

VEREDICTO FINAL: [VERDE — listo para Fase 6 / AMARILLO — advertencias, decidir conscientemente / ROJO — bloqueado, resolver antes de iniciar]
```

---

> **Nota: lo que sigue NO es parte del prompt. Es para mí, no para copiar en la conversación con la IA.**

## Después de la verificación

### Si el veredicto es VERDE
Procedé a Fase 6 con `prompts/04-codegen-layer.prompt.md`.

### Si el veredicto es AMARILLO
Leé cada advertencia. Para cada una decidí:
- **Resolver antes de generar:** modificá la spec (sube versión), volvé a ejecutar este prompt.
- **Aceptar conscientemente:** registrá en sección 10.1 de la spec la decisión de avanzar con la advertencia y por qué la aceptás. Procedé a Fase 6.

No avancés con AMARILLO por inercia. La decisión de aceptar una advertencia tiene que ser explícita.

### Si el veredicto es ROJO
Resolvé los bloqueantes antes de continuar. Según la naturaleza del bloqueante:
- **Bloqueante formal (F1-F8):** modificá la spec (sube versión) y volvé a ejecutar.
- **Bloqueante de codegen (C1-C6):** puede requerir volver a Fase 2 (discovery adicional) si el problema es falta de información del negocio, o solo modificar la spec si es gap de redacción.

---

## Notas operativas

- **Este prompt no reemplaza la pasada adversaria de spec (Fase 4).** Son distintos: la pasada adversaria busca problemas de contenido y diseño; este verifica preparación operativa para generación.

- **Si el veredicto es VERDE pero tenés dudas:** las dudas sobre la spec se resuelven acá, antes de generar. Una vez que empezás Fase 6, cambiar la spec tiene costo (volver a generar capas, ver WORKFLOW.md sección 8.3.1).

- **Si una advertencia se repite en varias capas:** es señal de que el problema está en la spec, no en el código. Resolverlo en la spec antes de generar.
