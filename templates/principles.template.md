# PRINCIPLES — Principios y Políticas Transversales

> **Versión:** [YYYYMMDD-vN]
> **Proyecto:** [nombre del proyecto]
> **Última modificación:** [YYYY-MM-DD]

---

## Propósito de este documento

Define los principios y políticas que aplican a todas las features del proyecto sin excepción. Cuando una feature spec dice "Aplican las políticas de PRINCIPLES.md sin extensiones", este documento es la referencia.

Las políticas aquí son **no negociables por feature**. Si una feature necesita diferir de alguna política, debe declararlo explícitamente en su sección de Requerimientos no funcionales y justificarlo.

---

## Autenticación y autorización

- **Autenticación requerida:** [ej: todos los endpoints excepto los listados en "endpoints públicos" requieren usuario autenticado]
- **Mecanismo:** [ej: JWT via Supabase Auth, token en header Authorization: Bearer]
- **Endpoints públicos:** [lista de endpoints que no requieren autenticación — ej: /health, /auth/login]
- **Expiración de sesión:** [ej: tokens expiran en 24h, refresh automático si la sesión está activa]
- **Autorización:** [modelo de autorización — ej: RBAC con roles definidos en DOMAIN_MODEL.md, RLS en Supabase para aislamiento de datos]

---

## Manejo de datos sensibles

- **Datos que nunca se loguean:** [ej: passwords, tokens, datos personales identificables]
- **Datos que se enmascaran en respuestas:** [ej: emails parciales, últimos 4 dígitos de tarjeta]
- **Retención de datos:** [ej: logs se retienen 30 días, datos de usuario se retienen mientras la cuenta esté activa]
- **Encriptación en tránsito:** [ej: HTTPS obligatorio en producción, HTTP solo permitido en desarrollo local]
- **Encriptación en reposo:** [ej: datos sensibles encriptados a nivel de columna en DB — listar cuáles]

---

## Validación de inputs

- **Dónde se valida:** [ej: siempre en la capa de entrada (schema Pydantic o formulario), nunca asumir input válido en capa de servicio]
- **Qué se valida:** [ej: tipos de dato, longitudes, rangos, formatos, caracteres permitidos]
- **Sanitización:** [ej: strings siempre trimmados, HTML escapado si se renderiza en UI]
- **Respuesta a input inválido:** [ej: HTTP 422 con detalle del campo y error, nunca 500 por input inválido]

---

## Manejo de errores

- **Errores de cliente (4xx):** [ej: respuesta con código específico + mensaje legible para el usuario + campo afectado si aplica]
- **Errores de servidor (5xx):** [ej: respuesta genérica sin detalle técnico, detalle en logs internos]
- **Errores de integración externa:** [ej: retry con backoff exponencial máximo 3 intentos, luego fallback o error controlado]
- **Qué se expone al cliente:** [ej: nunca stack traces, nunca nombres de tablas o campos internos]
- **Qué se loguea:** [ej: todos los 5xx con stack trace completo, 4xx solo si son recurrentes]

---

## Logging

- **Nivel de log en producción:** [ej: INFO para operaciones normales, ERROR para excepciones]
- **Nivel de log en desarrollo:** [ej: DEBUG]
- **Formato de logs:** [ej: JSON estructurado con timestamp, nivel, servicio, mensaje, context]
- **Qué se loguea siempre:** [ej: inicio y fin de requests, errores, operaciones críticas de negocio]
- **Qué nunca se loguea:** [ver "Manejo de datos sensibles"]

---

## Multi-tenancy y aislamiento de datos

- **Modelo:** [ej: single-tenant por instancia / multi-tenant con RLS en Supabase / otro]
- **Aislamiento:** [ej: cada usuario solo puede acceder a sus propios datos — aplicado via RLS en DB y verificado en capa de servicio]
- **Datos compartidos:** [ej: catálogos globales (tipos de cultivo, productos) son compartidos entre usuarios]

---

## Performance

- **Tiempo de respuesta objetivo:** [ej: P95 < 500ms para endpoints de lectura, P95 < 1s para escrituras]
- **Paginación:** [ej: obligatoria para listas de más de 50 elementos, default 50, máximo 100]
- **Queries prohibidas:** [ej: nunca SELECT * en producción, nunca N+1 queries sin eager loading]

---

## Principios de diseño de API

- **Versionado:** [ej: prefijo `/api/v1/` en todos los endpoints]
- **Naming de recursos:** [ej: sustantivos en plural — `/lotes`, `/aplicaciones`]
- **Métodos HTTP:** [ej: GET para lectura, POST para creación, PUT para reemplazo completo, PATCH para actualización parcial, DELETE para eliminación]
- **Soft delete:** [ej: las entidades nunca se borran físicamente, se marcan como `deleted_at` timestamp]
- **Respuestas:** [ej: siempre JSON, siempre con estructura `{data: ..., error: ...}`]

---

## Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| YYYYMMDD-v1 | YYYY-MM-DD | Versión inicial. |
