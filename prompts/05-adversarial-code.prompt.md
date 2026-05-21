# Prompt — Pasada adversaria de código

> **Versión:** 20260520-v1
> **Uso:** Después de generar una capa de código contra una spec aprobada, antes de pasar a la siguiente capa.
> **Dónde se ejecuta:** En conversación nueva con contexto limpio. NO en la conversación donde se generó el código.

---

## Cómo usar este prompt

1. Abrí conversación nueva en Claude.ai (o herramienta equivalente).
2. Cargá los archivos en este orden:
   - `CONVENTIONS.md`
   - `ARCHITECTURE.md`
   - `DOMAIN_MODEL.md`
   - `PRINCIPLES.md`
   - `GLOSSARY.md`
   - Feature spec completa (versión aprobada).
   - Specs dependientes (las que aparezcan en sección "Dependencias" de la spec).
   - Código generado de la capa que estás revisando.
3. Reemplazá los placeholders `{...}` del prompt.
4. Pegá el prompt completo y enviá.

---

## Prompt

```
Necesito que actúes como revisor adversario de código. Tu trabajo NO es validarlo ni decirme que está bien. Tu trabajo es encontrarle problemas.

CONTEXTO:
Te paso el código generado para la {CAPA: 1-Modelo de datos / 2-Lógica de negocio / 3-API / 4-UI} de la feature {ID-SPEC} versión {YYYYMMDD-vN}.

Acabás de recibir también los artefactos del setup foundacional del proyecto y la spec completa de la feature.

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

CIERRE:
Terminá con UNA pregunta crítica: ¿qué riesgo operativo concreto introduce este código si se mergea tal cual está?
```

---

## Después de la pasada adversaria

1. Procesá los hallazgos uno por uno. NO los aceptes todos por inercia.
2. Para cada hallazgo, decidí:
   - **Iterar código:** error técnico claro, lo corregís pidiendo cambio quirúrgico al LLM Generador (en la conversación original).
   - **Modificar spec:** si el "desvío" en realidad revela un gap o ambigüedad de la spec. Subir versión.
   - **Modificar setup foundacional:** si el problema afecta a más de una feature.
   - **Descartar:** si después de procesarlo, decidís que el hallazgo es flojo o no aplica.
3. Una vez procesados todos, ejecutás el checklist completo de verificación entre capas (sección 6.4 del WORKFLOW.md) antes de pasar a la siguiente capa.

---

## Notas operativas

- **Conversación limpia:** la pasada adversaria del código NUNCA se hace en la conversación donde se generó. El LLM tiene sesgo a defender lo que escribió.
- **Si la pasada adversaria devuelve "todo está bien":** desconfiá. O el código es trivial, o el adversario no buscó bien. Repetir con prompt reforzado.
- **Si la pasada adversaria devuelve más de 20 hallazgos serios:** probablemente la capa tiene problemas estructurales. Considerá descartar la generación y volver a generar con prompt mejorado, en vez de iterar.
