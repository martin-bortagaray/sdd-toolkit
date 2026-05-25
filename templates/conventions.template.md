# CONVENTIONS — Convenciones Técnicas del Proyecto

> **Versión:** [YYYYMMDD-vN]
> **Proyecto:** [nombre del proyecto]
> **Última modificación:** [YYYY-MM-DD]

---

## Propósito de este documento

Define las convenciones técnicas que aplican a todo el código del proyecto. Cuando un LLM genera código para cualquier feature, este documento es la referencia de naming, estructura y patrones. Las convenciones aquí tienen precedencia sobre las preferencias del LLM.

Este documento es **vivo**: se actualiza reactivamente cuando se toma una decisión técnica que aplica a más de una feature. No se llena de forma anticipada.

---

## Naming

### General

- [Regla de naming para variables, funciones, clases, etc.]
- [Idioma del código: español, inglés, o mixto y cuándo]

### Backend (Python / FastAPI / SQLModel)

- Modelos SQLModel: [convención, ej: PascalCase singular — `Lote`, `Aplicacion`]
- Schemas Pydantic: [convención, ej: `LoteCreate`, `LoteRead`, `LoteUpdate`]
- Nombres de funciones: [convención, ej: snake_case — `get_lote_by_id`]
- Nombres de endpoints: [convención, ej: kebab-case — `/api/v1/lotes/{lote_id}`]
- Nombres de archivos: [convención, ej: snake_case — `lote_service.py`]
- Nombres de tests: [convención, ej: `test_<función_que_testea>.py`]

### Frontend (Next.js / TypeScript / Tailwind)

- Componentes: [convención, ej: PascalCase — `LoteCard`, `ApplicationForm`]
- Hooks: [convención, ej: `use` prefix — `useLotes`, `useApplicationForm`]
- Páginas: [convención, ej: kebab-case en carpetas — `app/lotes/[id]/page.tsx`]
- Tipos e interfaces: [convención, ej: PascalCase con I prefix o sin — `LoteType`]
- Nombres de archivos: [convención, ej: PascalCase para componentes, kebab-case para utils]

---

## Estructura de carpetas

### Backend

```
[estructura de carpetas del backend con descripción de qué va en cada una]

ejemplo:
app/
  models/       → Modelos SQLModel (entidades de DB)
  schemas/      → Schemas Pydantic (validación de inputs/outputs)
  services/     → Lógica de negocio
  routers/      → Endpoints FastAPI
  tests/        → Tests por módulo
```

### Frontend

```
[estructura de carpetas del frontend]

ejemplo:
app/
  (routes)/     → Páginas de Next.js App Router
  components/   → Componentes reutilizables
  hooks/        → Custom hooks
  lib/          → Utilidades y clientes de API
  types/        → TypeScript types e interfaces
```

---

## Patrones de código

### Backend

- **Patrón de servicio:** [cómo se estructura un servicio — ej: clase con métodos estáticos vs. funciones sueltas vs. instancias]
- **Manejo de errores:** [cómo se lanzan y manejan errores — ej: HTTPException con status codes específicos]
- **Validación de inputs:** [dónde y cómo se validan — ej: siempre en el schema Pydantic, nunca en el servicio]
- **Queries a la DB:** [patrón de acceso — ej: siempre a través de servicio, nunca query directa en router]
- **Autenticación:** [cómo se inyecta el usuario en los endpoints — ej: dependency injection con `get_current_user`]

### Frontend

- **Fetching de datos:** [patrón — ej: Server Components para datos iniciales, SWR/React Query para mutaciones]
- **Manejo de estado:** [cuándo usar useState vs. contexto vs. URL state]
- **Formularios:** [librería y patrón — ej: React Hook Form con Zod]
- **Estilos:** [convención de Tailwind — ej: clases utilitarias directas, sin CSS modules, cn() para condicionales]

---

## Convenciones de tests

- **Framework:** [ej: pytest para backend, Vitest para frontend]
- **Cobertura mínima esperada:** [ej: happy path + casos de error para toda función de negocio]
- **Datos de test:** [fixtures vs. factories vs. datos inline — cuál usar y cuándo]
- **Naming de tests:** [ej: `test_<función>_<condición>_<resultado_esperado>`]
- **Mocks:** [qué se mockea y qué no — ej: siempre mockear integraciones externas, nunca la lógica de negocio propia]

---

## Convenciones de commits

- **Formato:** [ej: Conventional Commits — `feat(spec-id): descripción`]
- **Cuándo commitear:** [ej: un commit por feature completa (todas las capas), no por archivo]
- **Referencia a spec:** [ej: incluir ID de spec en el mensaje de commit]

---

## Decisiones técnicas transversales

[Decisiones que aplican a todo el proyecto y que el LLM debe respetar. Se agregan acá cuando una decisión se toma durante el desarrollo de una feature y se decide que aplica globalmente.]

| Decisión | Alternativa descartada | Por qué |
|----------|----------------------|---------|
| [decisión tomada] | [qué se descartó] | [razonamiento] |

---

## Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| YYYYMMDD-v1 | YYYY-MM-DD | Versión inicial. |
