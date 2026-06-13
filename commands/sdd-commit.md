---
description: Commit y push inteligente — detecta si el proyecto usa metodología SDD y aplica las convenciones correspondientes
---

Ejecutá un commit (y opcionalmente push) de los cambios actuales. El comportamiento se adapta automáticamente según si el proyecto usa SDD (Spec Driven Development) o no.

## Paso 1 — Detectar el contexto del proyecto

Verificá si existe la carpeta `sdd/` en el directorio raíz del repo actual.

- Si existe `sdd/` → **Modo SDD** (el proyecto usa Spec Driven Development)
- Si no existe → **Modo estándar** (usá Conventional Commits genéricos)

Informale al usuario cuál modo activaste.

## Paso 2 — Ver el estado actual

Corré `git status` y `git diff --staged` en paralelo.

- Si **no hay nada staged**: corré también `git diff` (unstaged) y mostrá un resumen de qué archivos cambiaron. Preguntale al usuario qué quiere incluir en el commit antes de continuar. No asumas staging automático.
- Si **hay archivos staged**: continuá al Paso 3. Si hay unstaged relacionados con lo staged, mencionálos como "también hay cambios sin stagear en X, ¿los incluís?".

## Paso 3 — Determinar el prefijo del mensaje de commit

### Modo SDD

Analizá los archivos staged para elegir el prefijo más apropiado:

| Archivos staged | Prefijo sugerido |
|-----------------|-----------------|
| `sdd/bugs/bugfix-NNN.md` (nuevo o modificado) + código relacionado | `fix(bugfix-NNN):` — tomá el ID exacto del nombre del archivo |
| `sdd/specs/spec-NNN-*.md` nuevo(s) + código de la misma feature | `feat(spec-NNN):` — tomá el ID del nombre del archivo |
| Solo archivos en `sdd/specs/` o `sdd/README.md` (sin código) | `docs(sdd):` |
| Solo `sql/migrations/` | `feat(db):` |
| Solo código de app (`frontend/`, `parser-service/`) sin sdd/ | `feat(nombre-feature):` — inferí el nombre desde el path más representativo |
| Mezcla de `sdd/` + código | Usá el prefijo del cambio principal; si hay un bugfix ID, ese tiene prioridad |

### Modo estándar (Conventional Commits)

| Tipo de cambio | Prefijo |
|----------------|---------|
| Nueva funcionalidad | `feat:` |
| Corrección de bug | `fix:` |
| Solo documentación | `docs:` |
| Refactor sin cambio funcional | `refactor:` |
| Tests | `test:` |
| Mantenimiento / config | `chore:` |

## Paso 4 — Verificación manual ANTES de commitear (gate)

**Regla:** un cambio que toca código no se commitea hasta que yo lo probé manualmente y confirmé que funciona. Los tests automáticos no reemplazan esta prueba: validan que el código cumple la spec, no que la experiencia real es la esperada.

### Cuándo aplica el gate

- **Aplica** cuando el commit incluye código: prefijos `feat(spec-NNN):`, `fix(bugfix-NNN):`, `feat(db):`, `feat(nombre-feature):`, o cualquier mezcla con código.
- **NO aplica** (saltá el gate directo al Paso 5) cuando el commit es **solo documentación o artefactos del toolkit sin código**: `docs(sdd):`, `docs:`, `chore:`, o cambios que solo tocan `sdd/` / `.md`.
- **Override manual:** si `$ARGUMENTS` contiene `sin-prueba` o `skip-test`, saltá el gate, pero avisame explícitamente que se commiteó **sin verificación manual** y por qué (lo dejo registrado conscientemente).

### Qué hacer cuando aplica

1. **Derivá los pasos de prueba** del artefacto que se está commiteando, sin inventar:
   - `feat(spec-NNN)` o modificación → leé la spec staged. Tomá los **criterios de aceptación (sección 8)** y los **casos borde (sección 9)**. En una modificación, restringí los pasos a lo que el **CHANGE-SET** tocó (no toda la feature).
   - `fix(bugfix-NNN)` → leé el `bugfix-NNN.md`. Tomá los **pasos de reproducción** y el **criterio de aceptación del fix**: la prueba es reproducir el caso original y confirmar que ahora se comporta bien.
2. **Presentame un plan de prueba manual concreto y ejecutable**, no genérico. Para cada paso: qué hacer, con qué datos/precondición, y **qué resultado esperar**. Numerado. Si hace falta levantar el entorno (servidor, seed de datos), incluilo como precondición.
3. **Esperá mi confirmación explícita** de que probé y funciona (ej: "probado, OK"). No commitees antes.
4. **Si reporto que algo falla:** NO commitees. Según el flujo, eso vuelve a iteración de código (codegen) o abre un bug nuevo. Frená y avisame.

## Paso 5 — Redactar el mensaje y pedir confirmación

Sugerí un mensaje de commit completo siguiendo el formato:

```
prefijo: descripción en infinitivo, concisa (máx 72 chars)
```

Usá el mismo idioma que predomina en el proyecto (detectalo de los archivos de código o commits anteriores con `git log --oneline -5`).

Mostrá el mensaje sugerido claramente y esperá confirmación explícita antes de commitear. Si el usuario propone un mensaje diferente, usá el suyo.

## Paso 6 — Ejecutar el commit

Hacé el commit con el mensaje confirmado usando:

```bash
git commit -m "mensaje aquí"
```

Confirmá que el commit se creó con `git log --oneline -1`.

## Paso 7 — Push (opcional)

- Si el usuario pasó "push" en los argumentos (`$ARGUMENTS` contiene "push") → hacé el push directamente sin preguntar.
- Si no → preguntá: "¿Hacemos push también?" y esperá respuesta.

Al hacer push, usá `git push`. Si la rama no tiene upstream configurado, usá `git push -u origin <rama-actual>`.

---

Argumentos opcionales: $ARGUMENTS
