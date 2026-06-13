# Prompt — Pasada adversaria de código

> **Versión:** 20260610-v5 · historia en `/CHANGELOG.md`
> **Uso:** Después de generar una capa de código contra una spec aprobada, antes de pasar a la siguiente capa.
> **Dónde se ejecuta:** Vía el comando `/sdd-adversarial-code` en Claude Code (corre en subagente con contexto limpio), o en conversación nueva en Claude.ai. NUNCA en la conversación donde se generó el código (WORKFLOW.md sección 11.1, modelo híbrido v10).

---

## Cuándo se ejecuta según el tier (modificaciones, WORKFLOW.md 8.3.2)

En **builds iniciales y modificaciones T3**, este prompt se ejecuta completo, como siempre. En modificaciones con CHANGE-SET:

- **T1 (cosmético): este prompt NO se ejecuta.** Se reemplaza por **checks inline** en la misma sesión de generación: tests de la capa + typecheck/build + revisión del diff contra `CONVENTIONS.md`. El valor del subagente es la independencia de contexto, y sobre un diff cosmético esa independencia compra poco; el riesgo real lo cubren los tests y el gate de prueba manual (que no se relaja en ningún tier).
- **T2 (lógica acotada): se ejecuta acotado al diff, con contexto selectivo.** El subagente recibe: el diff de la capa (no todo el código), las secciones de la spec que el CHANGE-SET toca + el CHANGE-SET, `CONVENTIONS.md` + `PRINCIPLES.md` siempre, y `DOMAIN_MODEL.md`/`ARCHITECTURE.md` solo según las capas tocadas (8.3.2). Los hallazgos se reportan solo sobre el código del delta y su interacción con el código existente que toca.
- **Válvula de escape:** si la revisión revela que el cambio toca modelo/reglas/seguridad que el tier no admite, el hallazgo es bloqueante y el tier sube (WORKFLOW.md 8.3.2).

## Cómo usar este prompt

1. Abrí conversación nueva en Claude.ai (o herramienta equivalente).
2. Cargá los archivos en este orden:
   - `CONVENTIONS.md`
   - `ARCHITECTURE.md`
   - `DOMAIN_MODEL.md`
   - `PRINCIPLES.md`
   - `GLOSSARY.md`
   - Feature spec completa (versión aprobada).
   - Specs dependientes (primer nivel directo, las que aparezcan en sección "Dependencias" de la spec).
   - Código generado de la capa que estás revisando.

   **En modificaciones T2:** aplicá la carga selectiva de arriba en vez de la lista completa.
3. Reemplazá los placeholders `{...}` del prompt.
4. Pegá el prompt completo y enviá.

---

## Advertencia sobre límites de la pasada adversaria del código

Antes de ejecutar este prompt, recordá que esta pasada adversaria **tiene límites definidos**:

**SÍ valida:**
- Que cada criterio de aceptación de la spec tiene un test que lo cubre.
- Que el código no modifica módulos marcados como "sin tocar".
- Que naming, patrones y convenciones siguen lo definido en CONVENTIONS.md y la spec.
- Que los casos de error definidos en la spec tienen manejo explícito.
- Que la estructura de archivos sigue lo definido en el proyecto.

**NO valida:**
- Que el criterio de aceptación captura correctamente la necesidad real del negocio.
- Que la restricción declarada en la spec era la correcta en primer lugar.
- Que la arquitectura elegida es la más adecuada para el problema.
- Que no existen casos de error que la spec no contemplaba.
- Que el diseño de la spec es técnicamente óptimo.

**Riesgo a tener presente — validación circular:** la IA generó la spec (a partir de mis respuestas durante el discovery), generó el código contra esa spec, y ahora va a verificar el código contra la misma spec. Si la spec capturó mal el requisito de negocio, el código y los tests serán consistentes entre sí pero incorrectos respecto al problema real. **La pasada adversaria del código no detecta este caso.** Si tengo dudas sobre si la spec captura bien la realidad del negocio, esas dudas se resuelven antes (en Fase 4, con consulta a experto de dominio si corresponde), no con esta pasada.

---

## Prompt

```
Necesito que actúes como revisor adversario de código. Tu trabajo NO es validarlo ni decirme que está bien. Tu trabajo es encontrarle problemas.

CONTEXTO:
Te paso el código generado para la {CAPA: 1-Modelo de datos / 2-Lógica de negocio / 3-API / 4-UI} de la feature {ID-SPEC} versión {YYYYMMDD-vN}.

Acabás de recibir también los artefactos del setup foundacional del proyecto y la spec completa de la feature.

ALCANCE DE TU REVISIÓN:
Tu validación es contra la spec. Asumí la spec como contrato dado. No cuestiones si el criterio de aceptación captura bien la realidad del negocio, ni si la arquitectura elegida es óptima, ni si la spec en sí está bien diseñada. Esas validaciones ocurren en otras fases del proceso. Tu trabajo es verificar que el código cumple lo que la spec dice.

LO QUE QUIERO QUE BUSQUES (en orden de prioridad):

1. Desvíos respecto a la spec: el código no implementa exactamente lo que la spec pide. Listame cada desvío con cita textual de la sección de la spec violada y cita textual del código que la viola.

2. Decisiones implícitas no marcadas: el código toma decisiones que la spec no especifica (tipos de datos, validaciones, manejo de errores, defaults). Listámelas. NO me digas si son razonables o no — solo listámelas para que yo decida.

3. Violaciones de convenciones (CONVENTIONS.md): naming wrong, estructura de carpetas, patrones declarados que no se respetan. Cita textual de la convención violada + cita del código.

4. Violaciones de principios (PRINCIPLES.md): especialmente seguridad. Falta de autenticación donde la política la exige, validación faltante, manejo de errores que expone información sensible, logging que no respeta política de datos sensibles, etc.

5. Inconsistencias con el modelo conceptual (DOMAIN_MODEL.md): entidades con atributos o relaciones que no coinciden con el modelo declarado. Esto es especialmente crítico en Capa 1.

6. Bugs lógicos: errores que harían que el código no funcione correctamente en casos válidos según la spec. NO bugs hipotéticos en casos fuera de spec.

7. Casos borde no cubiertos: casos borde explícitamente declarados en la sección 9 de la spec (Casos borde y manejo de errores) que el código no maneja correctamente.

8. Sobre-ingeniería: cosas que el código agrega y que NO están en la spec ni requeridas por convenciones/principios. Validaciones de más, atributos adicionales, relaciones no pedidas, capas de abstracción innecesarias, manejo de casos no declarados.

FORMATO DE TU RESPUESTA:

Listá hallazgos numerados, agrupados por las 8 categorías. Para cada hallazgo:
- Cita textual del código problemático (con ruta de archivo y línea aproximada si es posible).
- Cita textual de la spec / convención / principio violado.
- Por qué es un problema.
- NO propongas reescritura. Sugerencia quirúrgica.

Si no encontrás problemas en alguna categoría, decilo explícitamente. NO inventes hallazgos para llenar categorías vacías.

RESTRICCIONES:
- No felicites nada del código. No me digas qué está bien.
- No suavices el lenguaje.
- Si dudás si algo es problema, marcalo como "zona gris".
- Tu opinión sobre estilo de código sin base en CONVENTIONS.md no cuenta como hallazgo.
- No cuestiones la spec en sí. Tu validación es contra la spec, asumida como contrato dado.

CIERRE:
Terminá con UNA pregunta crítica: ¿qué riesgo operativo concreto introduce este código si se mergea tal cual está?
```
