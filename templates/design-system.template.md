# DESIGN SYSTEM — Sistema de Diseño del Autor

> **Versión:** 20260524-v1
> **Autor:** Martin Bortagaray
> **Propósito:** Sistema de diseño reutilizable para todos los proyectos del autor. Define la identidad visual, decisiones técnicas de UI y componentes base.
>
> **Ubicación:** `templates/design-system.template.md` en el toolkit. Se referencia desde el prompt `00c-design-prototype.prompt.md` y desde los prompts de generación de código de UI (Capa 4 del codegen).
>
> **Cuándo modificar:** evolución del autor. Cambios en el design system aplican a proyectos futuros, no a los ya implementados (salvo refactor explícito).

---

## 1. Tono visual

**Moderno / Minimalista.**

Referencias visuales: Vercel, Cal.com, Resend, Linear.

Principios:
- Colores monocromáticos con acento sutil.
- Mucho contraste entre fondo y contenido.
- Espacios generosos donde no compiten con densidad de información.
- Sensación de "tecnología premium" sin caer en lo corporativo aburrido ni en lo friendly demasiado cálido.

---

## 2. Modo y colores

### Modo de visualización

**Modo oscuro como default. Modo claro como variación opcional.**

Esto significa:
- Toda app construida con este design system inicia en modo oscuro al cargar por primera vez.
- El usuario puede cambiar a modo claro si lo prefiere (toggle accesible).
- Los componentes se diseñan pensando en modo oscuro primero, claro como derivado.

### Color de acento

**Default: Indigo.**

Específicamente: `indigo-500` de Tailwind (`#6366F1`) como color principal de marca.
Variantes en escala: `indigo-400` (hover), `indigo-600` (pressed), `indigo-950` (background sutil).

**Override por proyecto:**
Cuando un proyecto requiere color corporativo del cliente, el color de acento se reemplaza por el del cliente. El resto del design system se mantiene. La regla operativa:

- Si el proyecto es propio o MVP sin cliente fijo: indigo.
- Si el proyecto es para un cliente con marca: color del cliente.

### Colores funcionales (no negociables por proyecto)

Estos colores tienen significado funcional y se mantienen iguales en todos los proyectos:

- **Success / Confirmación:** `green-500` / `green-600`
- **Warning / Atención:** `amber-500` / `amber-600`
- **Destructive / Error:** `red-500` / `red-600`
- **Info / Neutro:** `blue-500` / `blue-600`

### Escala de grises (neutrals)

Modo oscuro (default):
- Background base: `zinc-950` (casi negro pero no puro)
- Background elevado: `zinc-900`
- Borde sutil: `zinc-800`
- Texto principal: `zinc-50`
- Texto secundario: `zinc-400`
- Texto deshabilitado: `zinc-600`

Modo claro:
- Background base: `white`
- Background elevado: `zinc-50`
- Borde sutil: `zinc-200`
- Texto principal: `zinc-900`
- Texto secundario: `zinc-600`
- Texto deshabilitado: `zinc-400`

---

## 3. Tipografía

### Fuente principal

**Inter.**

Se carga desde Google Fonts o como variable font local. Variantes:
- Regular (400)
- Medium (500)
- Semibold (600)
- Bold (700)

Tracking ajustado: ligeramente apretado en titulares grandes para que se vea moderno (`tracking-tight` de Tailwind en h1/h2).

### Fuente monoespaciada

**JetBrains Mono.**

Para mostrar:
- IDs de registros (ej: `Lote ID: 12345`)
- Datos técnicos (tokens, hashes, JSON)
- Números importantes que requieren alineación vertical
- Código embebido si aplica

Variantes:
- Regular (400)
- Medium (500)

### Escala tipográfica

Usar la escala default de Tailwind sin modificaciones:
- `text-xs` (12px) — metadata, labels pequeños
- `text-sm` (14px) — body por defecto, UI interactiva
- `text-base` (16px) — body largo, lectura cómoda
- `text-lg` (18px) — subtítulos, párrafos destacados
- `text-xl` a `text-3xl` — titulares de sección
- `text-4xl` a `text-6xl` — titulares de landing/hero

---

## 4. Espaciados y proporciones

**Espaciado balanceado (default de shadcn/ui).**

Usar la escala de Tailwind sin modificaciones (`space-1` = 4px, `space-2` = 8px, ..., `space-12` = 48px, etc.).

### Padding base de componentes

- Botones: `px-4 py-2` (md), `px-3 py-1.5` (sm), `px-6 py-3` (lg)
- Inputs: `px-3 py-2`
- Cards: `p-6`
- Sections: `py-12 lg:py-16`

### Gaps en layouts

- Entre elementos relacionados: `gap-2` o `gap-3`
- Entre grupos: `gap-6` o `gap-8`
- Entre secciones: `gap-12` o `gap-16`

---

## 5. Bordes y elevación

### Radios de bordes

**Radio pequeño: 6px (`rounded-md` de Tailwind).**

Aplicar consistentemente:
- Botones, inputs, badges, tags: `rounded-md` (6px)
- Cards, dialogs, popovers: `rounded-lg` (8px) — ligeramente más para contenedores grandes
- Avatares circulares: `rounded-full`
- Imágenes en cards: `rounded-md`

### Bordes

- Espesor: `border` (1px) por defecto.
- Color: `border-zinc-800` (modo oscuro) / `border-zinc-200` (modo claro).
- Usar bordes para separación, no sombras pesadas.

### Elevación / Sombras

Modo oscuro: usar background diferenciado en lugar de sombras (las sombras no se ven bien en oscuro).
- Card normal: `bg-zinc-900` sobre `bg-zinc-950`.
- Card elevado (dialog, popover): `bg-zinc-800` sobre `bg-zinc-950` + `border border-zinc-700`.

Modo claro: sombras sutiles permitidas.
- Card normal: `shadow-sm` o sin sombra, solo border.
- Card elevado: `shadow-md`.
- Modal/Dialog: `shadow-lg`.

---

## 6. Componentes base

### Stack base de componentes

**shadcn/ui core + extensiones para SaaS B2B.**

shadcn/ui core (instalación inicial):
- Button, Input, Textarea, Label, Select
- Dialog, Sheet, Popover, Tooltip
- Card, Tabs, Accordion
- Toast / Sonner para notificaciones
- Avatar, Badge, Separator
- Form (con react-hook-form + zod)
- Table base
- Checkbox, Radio, Switch
- Skeleton (loading states)

Extensiones para SaaS B2B (agregar según necesite cada proyecto):
- **DataTable** con filtros, ordenamiento, paginación, selección múltiple. Es el componente más importante para apps de gestión.
- **DateRangePicker** para selección de rangos de fecha (típico en reportes).
- **Combobox** (Select con búsqueda) para listas largas.
- **MultiSelect** para selección múltiple con tags.
- **Command** (paleta de comandos tipo Linear/Notion) para acciones rápidas y navegación por teclado.

### Reglas de uso

- No mezclar librerías de componentes. shadcn/ui es la única fuente.
- Si una funcionalidad no está en shadcn/ui, agregar usando los primitives de Radix UI (la base de shadcn/ui) antes de buscar en otras librerías.
- Customizaciones específicas de un proyecto van en el repo del proyecto, no en este design system.

---

## 7. Iconos

**Lucide.**

Instalación: `lucide-react`.

Reglas de uso:
- Tamaño default: `size-4` (16px) para iconos inline, `size-5` (20px) para iconos en botones, `size-6` (24px) para iconos destacados.
- Stroke width: 2 (default de Lucide).
- Color: heredar del texto contextual (`currentColor`).

Si un icono específico no está en Lucide:
- Verificar si está en variantes (Lucide tiene ~1500 iconos, suele cubrir todo).
- Si realmente no está, evaluar si la funcionalidad necesita ese icono o si hay otra forma de expresarla.

---

## 8. Logo

**Logo variable por proyecto.**

Cada proyecto tiene su logo (cliente o producto propio). El logo NO es parte de este design system.

Reglas operativas:
- Ubicación estándar: top-left de la barra de navegación principal.
- Tamaño base: 24-32px de alto.
- Soporte para versión modo oscuro y modo claro si el logo lo requiere.
- Formato: SVG preferido, PNG con transparencia como fallback.

---

## 9. Patrones de UX

Decisiones de comportamiento que se aplican consistentemente en todos los proyectos:

### Navegación

- Sidebar fijo en desktop para apps de gestión con muchas secciones.
- Bottom navigation o drawer en mobile.
- Breadcrumbs para navegación jerárquica de 3+ niveles.

### Formularios

- Labels arriba de los inputs (no inline a la izquierda).
- Validación inline al perder foco (no en cada keystroke).
- Mensajes de error debajo del input, en rojo.
- Botón primario a la derecha del botón secundario en footers de formulario.

### Estados

Toda lista, tabla o grid debe contemplar 4 estados visualmente diferenciados:
- **Loading:** skeleton, no spinner centralizado.
- **Empty:** mensaje + ilustración simple + CTA si aplica.
- **Error:** mensaje + acción de retry.
- **Success / Content:** la vista normal.

### Feedback

- Acciones destructivas (delete, archivar): confirmación con dialog.
- Acciones de éxito: toast no intrusivo (esquina inferior derecha).
- Operaciones largas (>2 segundos): indicador de progreso visible.

### Atajos de teclado

Para apps con uso intensivo (gestión, dashboards):
- `Cmd/Ctrl + K`: abrir paleta de comandos.
- `Cmd/Ctrl + Enter`: submit de formularios.
- `Esc`: cerrar dialogs y popovers.
- `/`: enfocar search si la página tiene búsqueda principal.

---

## 10. Cómo se usa este design system

### Al iniciar un proyecto nuevo

1. El prompt `00c-design-prototype.prompt.md` carga este archivo como contexto cuando genera el brief para Claude Design.
2. El brief le indica a Claude Design que use este sistema como base.
3. Si el proyecto tiene cliente con marca propia, el override de color y logo se documenta en `ARCHITECTURE.md` del proyecto.

### Al generar código de UI (Capa 4)

1. El prompt `04-codegen-layer.prompt.md` carga este archivo como contexto adicional cuando la capa generada es UI.
2. El código generado usa los componentes, colores, tipografía y patrones definidos acá.

### Al evolucionar el design system

- Cambios en este archivo aplican a **proyectos futuros**.
- Proyectos ya implementados no se actualizan automáticamente.
- Si querés migrar un proyecto existente al nuevo design system, eso es trabajo explícito (refactor de UI).

---

## 11. Limitaciones declaradas

Este design system tiene foco específico. Vale declarar qué NO cubre:

- **Animaciones complejas:** no se definen animaciones más allá de transiciones simples (`transition-colors`, `transition-transform`). Para animaciones complejas, cada proyecto decide caso por caso.
- **Iconografía custom:** todo va con Lucide. No se diseñan iconos propios.
- **Ilustraciones:** no se definen. Si un proyecto necesita ilustraciones (empty states, landing pages), se usan recursos externos (unDraw, Storyset) o se decide caso por caso.
- **Branding extenso:** este no es un brand system completo. Define identidad visual técnica suficiente para apps de SaaS, no para web marketing pesado o materiales impresos.

---

## Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 20260524-v1 | 2026-05-24 | Versión inicial. Decisiones del autor consolidadas en 11 secciones. |
