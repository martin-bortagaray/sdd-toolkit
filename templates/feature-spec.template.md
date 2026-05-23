# Spec: [Nombre de la feature]

---

## 1. Metadata

- **ID:** [<dominio>-<numero>]
- **Versión:** [YYYYMMDD-vN]
- **Estado:** [Draft / Review / Approved / Implemented / Deprecated]
- **Autor:** [nombre]
- **Fecha última modificación:** [YYYY-MM-DD HH:MM]
- **Toolkit usado:** [versión del toolkit]

---

## 2. Contexto y propósito

[Por qué existe esta feature. Qué problema resuelve. A qué objetivo de PRODUCT.md responde.]

---

## 3. Usuarios y casos de uso

### Roles

[Lista de roles con definición de qué hace cada uno.]

### Escenarios principales

[Lista numerada de happy paths.]

### Escenarios secundarios

[Lista numerada de casos válidos menos frecuentes.]

### No-objetivos

[Lista numerada de casos que NO cubre esta feature.]

---

## 4. Requerimientos funcionales

[Lista numerada de afirmaciones precisas sobre qué debe hacer el sistema.]

---

## 5. Requerimientos no funcionales

### Performance

[Tiempos de respuesta esperados, carga esperada, o "No aplica porque...".]

### Disponibilidad / offline

[Requiere conexión / funciona offline / qué pasa si se pierde conexión, o "No aplica porque...".]

### Seguridad

[Si esta feature respeta TODAS las políticas globales de PRINCIPLES.md sin extender ni diferir, escribir: "Aplican las políticas de PRINCIPLES.md sin extensiones." Si esta feature requiere algo específico, documentarlo aquí.]

### Internacionalización

[Idiomas, formatos, unidades, o "No aplica porque...".]

### Otros (accesibilidad, privacidad, compatibilidad)

[Contenido relevante, o "No aplica porque...".]

---

## 6. Modelo de datos

[Entidades involucradas con todos sus atributos finales, tipos, restricciones y relaciones. Consistente con DOMAIN_MODEL.md.]

---

## 7. Reglas de negocio

[Lista numerada de reglas del dominio no obvias desde el modelo de datos.]

---

## 8. Criterios de aceptación

[Lista de escenarios verificables en formato Given/When/Then o checklist de comportamientos.]

---

## 9. Casos borde y manejo de errores

[Lista numerada de casos borde según taxonomía obligatoria condicional. Ver guide sección 9 para las 10 categorías a considerar.]

---

## 10. Decisiones explícitas y trade-offs

### 10.1 Decisiones del autor

[Lista numerada de decisiones tomadas durante el discovery, con alternativa descartada, razonamiento y trade-off aceptado.]

### 10.2 Decisiones derivadas de pasadas adversarias

[Lista de hallazgos de pasadas adversarias que se resolvieron o descartaron, con el razonamiento. Para que el adversario en pasada 2 sepa qué ya está cerrado y no lo re-marque.]

| Pasada | Hallazgo | Resolución |
|--------|----------|------------|
| 1 | [Descripción breve] | [Aceptado / Descartado / Modificado] — [razonamiento] |

[Si no hubo pasadas adversarias previas, escribir "Pendiente — sin pasadas adversarias todavía".]

---

## 11. Fuera de alcance

[Lista numerada de qué EXPLÍCITAMENTE no hace esta feature.]

---

## 12. Dependencias y supuestos

### Depende de

[Specs de primer nivel directo de las que depende esta. Sin transitividad.]

### Consumida por

[Specs que dependen de esta, si aplica.]

### Supuestos

[Supuestos sobre el contexto del producto asumidos sin verificar.]

---

## 13. Notas de implementación

[Sección con dos modos de uso:

- **Modo obligatorio:** si la feature tiene UI compleja (flujos multi-paso, interacciones no triviales, estados visuales relevantes para el negocio), esta sección debe documentar comportamiento de interfaz: flujos, estados visuales, transiciones, validaciones en cliente.

- **Modo opcional:** para CRUDs simples u otras features sin UI compleja, puede contener pistas técnicas que orientan al LLM Generador sin ser requerimientos. Si queda vacía, eliminarla.]

---

## 14. Decisiones tomadas por defecto por la IA

[Lista numerada de decisiones que la IA en rol Redactor tomó por su cuenta porque no estaban en el discovery con el autor. Cada item debe incluir:

- Decisión tomada.
- En qué sección de la spec aparece.
- Por qué la IA la tomó así (justificación).

El autor revisa esta sección antes de pasar la spec a Review. Cada decisión se valida (la IA la mantiene), se rechaza (se reemplaza por la decisión del autor), o se marca como pendiente.

Si la IA no tomó ninguna decisión por defecto, escribir: "Sin decisiones por defecto. Todas las decisiones provienen del discovery con el autor."]

---

## 15. Changelog de esta spec

| Versión | Fecha | Cambios |
|---------|-------|---------|
| YYYYMMDD-v1 | YYYY-MM-DD | Versión inicial. |
