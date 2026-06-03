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

## Paso 4 — Redactar el mensaje y pedir confirmación

Sugerí un mensaje de commit completo siguiendo el formato:

```
prefijo: descripción en infinitivo, concisa (máx 72 chars)
```

Usá el mismo idioma que predomina en el proyecto (detectalo de los archivos de código o commits anteriores con `git log --oneline -5`).

Mostrá el mensaje sugerido claramente y esperá confirmación explícita antes de commitear. Si el usuario propone un mensaje diferente, usá el suyo.

## Paso 5 — Ejecutar el commit

Hacé el commit con el mensaje confirmado usando:

```bash
git commit -m "mensaje aquí"
```

Confirmá que el commit se creó con `git log --oneline -1`.

## Paso 6 — Push (opcional)

- Si el usuario pasó "push" en los argumentos (`$ARGUMENTS` contiene "push") → hacé el push directamente sin preguntar.
- Si no → preguntá: "¿Hacemos push también?" y esperá respuesta.

Al hacer push, usá `git push`. Si la rama no tiene upstream configurado, usá `git push -u origin <rama-actual>`.

---

Argumentos opcionales: $ARGUMENTS
