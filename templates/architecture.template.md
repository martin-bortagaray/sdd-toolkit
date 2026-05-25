# ARCHITECTURE — Arquitectura del Proyecto

> **Versión:** [YYYYMMDD-vN]
> **Proyecto:** [nombre del proyecto]
> **Última modificación:** [YYYY-MM-DD]

---

## Propósito de este documento

Define la arquitectura del sistema: qué tecnologías se usan, cómo está organizado el código, qué patrones se aplican, y por qué se tomaron las decisiones que llevaron a esta arquitectura.

Es referencia obligatoria para todos los prompts del ciclo de feature (Fases 2 a 6). El LLM Generador lo carga como contexto para generar código que respete la arquitectura definida.

Este documento se actualiza cuando hay un cambio arquitectónico importante (cambio de stack, nuevo componente core, cambio de patrón). Cambios menores van en `CONVENTIONS.md`.

---

# PARTE 1 — QUÉ TIENE EL SISTEMA

Esta parte describe la arquitectura actual. Es la "foto" que el LLM consume para generar código.

---

## 1. Stack tecnológico

### Backend

- **Lenguaje:** [ej: Python 3.12+]
- **Framework:** [ej: FastAPI 0.110+]
- **ORM:** [ej: SQLModel 0.0.16+]
- **Validación:** [ej: Pydantic 2.x]
- **Tests:** [ej: pytest, pytest-asyncio]
- **Otros:** [librerías clave específicas del proyecto]

### Frontend

- **Framework:** [ej: Next.js 14+ con App Router]
- **Lenguaje:** [ej: TypeScript 5.x]
- **Estilos:** [ej: Tailwind CSS 3.x]
- **Componentes UI:** [ej: shadcn/ui, lucide-react]
- **Estado:** [ej: Zustand para estado global, React Query para data fetching]
- **Formularios:** [ej: React Hook Form + Zod]
- **Tests:** [ej: Vitest + React Testing Library]

### Base de datos y servicios externos

- **DB principal:** [ej: PostgreSQL via Supabase]
- **Auth:** [ej: Supabase Auth]
- **Storage:** [ej: Supabase Storage]
- **Otros servicios:** [ej: SendGrid para emails, Stripe para pagos]

### Infraestructura

- **Hosting backend:** [ej: Railway / Render / Fly.io]
- **Hosting frontend:** [ej: Vercel]
- **CI/CD:** [ej: GitHub Actions / manual al inicio]
- **Monitoreo:** [ej: Sentry / no aplica al inicio]

---

## 2. Patrón arquitectónico

### Capas del sistema

```
┌─────────────────────────────────────┐
│  Frontend (Next.js)                 │
│  - Server Components                │
│  - Client Components                │
│  - API Routes (si aplica)           │
└────────────────┬────────────────────┘
                 │ HTTP/REST
┌────────────────▼────────────────────┐
│  Backend API (FastAPI)              │
│  - Routers (Capa 3)                 │
│  - Services (Capa 2)                │
│  - Models (Capa 1)                  │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│  Base de datos (Supabase/Postgres) │
│  - Tablas y relaciones              │
│  - RLS policies                     │
│  - Funciones de DB (si aplica)     │
└─────────────────────────────────────┘
```

[Adaptar el diagrama según el stack real del proyecto.]

### Mapeo a las 4 capas de generación (WORKFLOW.md sección 6.1)

| Capa SDD | Implementación en este proyecto |
|----------|--------------------------------|
| Capa 1 — Modelo de datos | Modelos SQLModel + migraciones + políticas RLS si aplica |
| Capa 2 — Lógica de negocio | Servicios en `app/services/` |
| Capa 3 — API | Routers FastAPI en `app/routers/` |
| Capa 4 — UI | Componentes y páginas Next.js |

---

## 3. Estructura del repositorio

```
[Estructura de carpetas del proyecto.]

Ejemplo:
project/
├── backend/
│   ├── app/
│   │   ├── models/         → Modelos SQLModel
│   │   ├── schemas/        → Schemas Pydantic
│   │   ├── services/       → Lógica de negocio
│   │   ├── routers/        → Endpoints FastAPI
│   │   └── tests/          → Tests
│   └── migrations/         → Migraciones append-only
├── frontend/
│   ├── app/                → Páginas Next.js App Router
│   ├── components/         → Componentes
│   ├── hooks/              → Custom hooks
│   ├── lib/                → Clientes de API, utilidades
│   └── types/              → TypeScript types
├── specs/                  → Specs de features (SDD)
├── docs/                   → Documentación adicional
└── README.md
```

---

## 4. Comunicación entre componentes

- **Frontend ↔ Backend:** [ej: REST sobre HTTPS. Versionado `/api/v1/`. JSON.]
- **Backend ↔ DB:** [ej: ORM SQLModel via Supabase client. Connection pooling.]
- **Backend ↔ servicios externos:** [ej: HTTP cliente con retry y timeout configurables. Errores capturados y mapeados a errores de dominio.]

---

## 5. Multi-tenancy y aislamiento

[Modelo de aislamiento de datos:
- Single-tenant por instancia
- Multi-tenant con RLS de Supabase
- Multi-tenant con tenant_id en aplicación
- Otro]

[Cómo se implementa:
- Dónde vive la lógica de aislamiento (DB, aplicación, ambos)
- Qué se hace si una request no tiene contexto de tenant claro]

---

## 6. Autenticación y autorización

[Resumen de cómo funciona auth en el sistema. Detalle de políticas vive en PRINCIPLES.md.]

- **Mecanismo:** [ej: JWT via Supabase Auth]
- **Donde se valida:** [ej: middleware FastAPI + RLS en DB]
- **Modelo de autorización:** [ej: RBAC con roles definidos en DOMAIN_MODEL.md]

---

## 7. Manejo de errores

[Resumen del flujo de errores entre capas. Detalle de políticas vive en PRINCIPLES.md.]

- **Errores de dominio:** se lanzan en services, se capturan en routers, se mapean a HTTP.
- **Errores no manejados:** se capturan en middleware global, se loguean, se devuelven como 500 sin detalle técnico.
- **Errores de cliente:** se mapean a 4xx con detalle específico del campo afectado.

---

## 8. Restricciones y módulos sin tocar

[Áreas del sistema que NO se modifican durante el desarrollo de features. Si una feature necesita tocar uno de estos módulos, requiere decisión arquitectónica explícita.]

- [Ejemplo: "El módulo de autenticación no se modifica por feature. Cambios al auth requieren ADR."]
- [Ejemplo: "Las migraciones existentes no se editan. Cambios al schema generan migración nueva."]

---

# PARTE 2 — POR QUÉ SE ELIGIÓ ESTA ARQUITECTURA

Esta parte documenta las decisiones arquitectónicas importantes que llevaron a la arquitectura actual. Es la trazabilidad histórica del proyecto.

Las decisiones se documentan con formato simplificado de ADR. Si una decisión es muy compleja o tiene mucho contexto, se mueve a un ADR separado (ver `adr.template.md`) y acá queda solo la referencia.

---

## Decisión 1 — Stack tecnológico principal

**Contexto:** [Qué necesidades del proyecto llevaron a elegir este stack. Restricciones. Conocimiento del autor. Tiempo disponible.]

**Decisión:** [Stack elegido en una frase. Ej: "Backend Python con FastAPI + SQLModel, frontend Next.js con TypeScript, DB Supabase."]

**Alternativas consideradas:**

- **Alternativa 1:** [ej: "Backend Node.js con NestJS"] — descartada porque [razón concreta].
- **Alternativa 2:** [ej: "Stack monolítico Django"] — descartada porque [razón concreta].

**Consecuencias:**

- **Positivas:** [qué se gana con esta decisión]
- **Negativas:** [qué se pierde o complica]

---

## Decisión 2 — [Próxima decisión arquitectónica importante]

[Mismo formato que Decisión 1.]

[Ejemplos típicos de decisiones arquitectónicas que pueden ir acá:
- Por qué Supabase vs. backend de auth propio
- Por qué multi-tenancy con RLS vs. tenant_id en aplicación
- Por qué REST vs. GraphQL
- Por qué Server Components vs. SPA tradicional
- Por qué deploy en X plataforma vs. otras]

---

## Decisión [N] — [Última decisión documentada]

[Mismo formato.]

---

# PARTE 3 — EVOLUCIÓN

## Cuándo modificar este documento

- Cambio de stack tecnológico (cualquier capa).
- Nuevo componente core agregado al sistema.
- Cambio de patrón arquitectónico.
- Decisión arquitectónica importante nueva que afecta el proyecto entero.

**No se modifica para:**
- Decisiones de implementación de una feature específica (esas viven en la spec de feature).
- Convenciones de código (esas viven en `CONVENTIONS.md`).
- Políticas transversales sin cambio arquitectónico (esas viven en `PRINCIPLES.md`).

## Relación con otros documentos

- **`PRINCIPLES.md`:** políticas transversales que aplican a esta arquitectura (seguridad, logging, performance).
- **`CONVENTIONS.md`:** convenciones de código que implementan esta arquitectura.
- **`DOMAIN_MODEL.md`:** entidades del dominio que esta arquitectura soporta.
- **ADRs separados:** decisiones arquitectónicas individuales con detalle extenso que no caben acá.

---

## Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| YYYYMMDD-v1 | YYYY-MM-DD | Versión inicial. |
