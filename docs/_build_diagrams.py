"""Genera los diagramas SVG del proceso SDD (WORKFLOW v20).

Uso:  python docs/_build_diagrams.py
Salida: docs/process-diagram.svg, docs/flow_ciclo_feature.svg, docs/flow_codegen_y_deploy.svg

Los diagramas se describen como datos (cajas, rombos, flechas) para que actualizarlos sea
editar este archivo y volver a correrlo, no retocar SVG a mano. flow_fase_0_inicio_proyecto.svg
no se genera acá (Fase 0 no cambió).
"""
import os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))

STYLE = """
<style>
  text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }
  .t { font-size: 14px; font-weight: 400; }
  .th { font-size: 13px; font-weight: 600; }
  .ts { font-size: 11px; font-weight: 400; }
  .tt { font-size: 18px; font-weight: 700; fill: #2C2C2A; }
  .tsub { font-size: 12px; fill: #5F5E5A; }
  .tag { font-size: 9px; font-weight: 700; letter-spacing: 0.6px; }
  .c-gray rect, .c-gray polygon { fill: #F1EFE8; stroke: #5F5E5A; }
  .c-gray .th { fill: #2C2C2A; } .c-gray .ts, .c-gray .tag { fill: #5F5E5A; }
  .c-purple rect, .c-purple polygon { fill: #EEEDFE; stroke: #534AB7; }
  .c-purple .th { fill: #3C3489; } .c-purple .ts, .c-purple .tag { fill: #534AB7; }
  .c-teal rect, .c-teal polygon { fill: #E1F5EE; stroke: #0F6E56; }
  .c-teal .th { fill: #085041; } .c-teal .ts, .c-teal .tag { fill: #0F6E56; }
  .c-blue rect, .c-blue polygon { fill: #E6F1FB; stroke: #185FA5; }
  .c-blue .th { fill: #0C447C; } .c-blue .ts, .c-blue .tag { fill: #185FA5; }
  .c-amber rect, .c-amber polygon { fill: #FAEEDA; stroke: #854F0B; }
  .c-amber .th { fill: #633806; } .c-amber .ts, .c-amber .tag { fill: #854F0B; }
  .c-coral rect, .c-coral polygon { fill: #FAECE7; stroke: #993C1D; }
  .c-coral .th { fill: #712B13; } .c-coral .ts, .c-coral .tag { fill: #993C1D; }
  .c-pink rect, .c-pink polygon { fill: #FBEAF0; stroke: #993556; }
  .c-pink .th { fill: #72243E; } .c-pink .ts, .c-pink .tag { fill: #993556; }
  .arr { stroke: #5F5E5A; stroke-width: 1.4; fill: none; }
  .lbl { font-size: 10px; fill: #5F5E5A; font-weight: 600; }
</style>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#5F5E5A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>
"""


class Diagram:
    def __init__(self, width, title, desc):
        self.w = width
        self.title = title
        self.desc = desc
        self.parts = []
        self.max_y = 0

    def _track(self, y):
        self.max_y = max(self.max_y, y)

    def heading(self, x, y, text, sub=None):
        self.parts.append(f'<text class="tt" x="{x}" y="{y}">{escape(text)}</text>')
        if sub:
            self.parts.append(f'<text class="tsub" x="{x}" y="{y + 20}">{escape(sub)}</text>')

    def box(self, x, y, w, h, cls, title, lines=(), tag=None, rx=8):
        """Caja centrada: título + líneas. tag = etiqueta chica arriba a la izquierda (ej. GATE)."""
        cx = x + w / 2
        out = [f'<g class="{cls}">', f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" stroke-width="0.8"/>']
        n = 1 + len(lines)
        line_h = 15
        top = y + h / 2 - (n - 1) * line_h / 2
        out.append(f'<text class="th" x="{cx}" y="{top}" text-anchor="middle" dominant-baseline="central">{escape(title)}</text>')
        for i, ln in enumerate(lines):
            out.append(f'<text class="ts" x="{cx}" y="{top + (i + 1) * line_h}" text-anchor="middle" dominant-baseline="central">{escape(ln)}</text>')
        if tag:
            out.append(f'<text class="tag" x="{x + 8}" y="{y + 11}">{escape(tag)}</text>')
        out.append('</g>')
        self.parts.append('\n'.join(out))
        self._track(y + h)
        return (x, y, w, h)

    def diamond(self, cx, cy, w, h, cls, lines):
        pts = f"{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}"
        out = [f'<g class="{cls}">', f'<polygon points="{pts}" stroke-width="0.8"/>']
        n = len(lines)
        for i, ln in enumerate(lines):
            yy = cy - (n - 1) * 7.5 + i * 15
            out.append(f'<text class="th" x="{cx}" y="{yy}" text-anchor="middle" dominant-baseline="central">{escape(ln)}</text>')
        out.append('</g>')
        self.parts.append('\n'.join(out))
        self._track(cy + h / 2)

    def arrow(self, *pts, label=None, label_at=None):
        d = ' '.join(f"{x},{y}" for x, y in pts)
        self.parts.append(f'<polyline points="{d}" class="arr" marker-end="url(#arrow)"/>')
        if label:
            lx, ly = label_at if label_at else pts[0]
            self.parts.append(f'<text class="lbl" x="{lx}" y="{ly}">{escape(label)}</text>')

    def text(self, x, y, s, cls="ts", fill="#5F5E5A", anchor="start"):
        self.parts.append(f'<text class="{cls}" x="{x}" y="{y}" fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')
        self._track(y)

    def save(self, name, pad=30):
        h = int(self.max_y + pad)
        svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n'
               f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {self.w} {h}" role="img" aria-labelledby="title desc">\n'
               f'<title id="title">{escape(self.title)}</title>\n<desc id="desc">{escape(self.desc)}</desc>\n'
               f'{STYLE}\n<rect x="0" y="0" width="{self.w}" height="{h}" fill="#FFFFFF"/>\n'
               + '\n\n'.join(self.parts) + '\n</svg>\n')
        with open(os.path.join(HERE, name), 'w', encoding='utf-8') as f:
            f.write(svg)
        print(f"OK -> docs/{name} ({self.w}x{h})")


def bottom(b):
    x, y, w, h = b
    return (x + w / 2, y + h)


def top(b):
    x, y, w, h = b
    return (x + w / 2, y)


def down(d, a, b):
    d.arrow(bottom(a), top(b))


# ---------------------------------------------------------------- ciclo de feature
def ciclo_feature():
    d = Diagram(780, "Flujo del ciclo de feature — Modo Flow (WORKFLOW v20)",
                "Ciclo SDD por feature ejecutado con /sdd-feature: clasificación por track (Rápido, Estándar, "
                "Completo), gates humanos por track, implementación autónoma con gate automático, revisión de "
                "código única y prueba manual que autoriza el commit.")
    d.heading(30, 36, "Ciclo de feature — Modo Flow",
              "Una invocación de /sdd-feature recorre el ciclo. Frena solo en los gates (ámbar) del track: Rápido 2 · Estándar 3 · Completo 4.")

    start = d.box(190, 76, 400, 44, "c-gray", "Necesidad o cambio",
                  ['/sdd-feature "necesidad"   ·   /sdd-feature <ID> "cambio"'], rx=22)
    p0 = d.box(140, 142, 500, 62, "c-purple", "Paso 0 — ¿Qué es? (reanudable desde .flow.md)",
               ["Bug → /sdd-bugfix (Flujo C)  ·  Modificación → prompt 07  ·  Feature nueva → prompt 08",
                "La propuesta de track va dentro del primer gate"])
    down(d, start, p0)
    d.diamond(390, 262, 250, 74, "c-gray", ["Track", "(criterios de riesgo)"])
    d.arrow(bottom(p0), (390, 225))

    lanes = [
        (25, "c-teal", "RÁPIDO — 2 gates", ["Sin modelo, reglas, seguridad, dinero,", "contratos, irreversible ni compartidos"]),
        (277, "c-blue", "ESTÁNDAR — 3 gates", ["Toca modelo de datos o reglas,", "o agrega un flujo / entidad"]),
        (529, "c-coral", "COMPLETO — 4 gates", ["Seguridad, dinero, contrato externo,", "irreversible o grande"]),
    ]
    LW = 226
    heads = []
    for x, cls, t, ls in lanes:
        heads.append(d.box(x, 338, LW, 58, cls, t, ls))
    d.arrow((265, 262), (138, 262), (138, 336))
    d.arrow((390, 299), (390, 336))
    d.arrow((515, 262), (642, 262), (642, 336))

    G = "c-amber"
    A = "c-purple"
    BH, GAP = 58, 22
    y0 = 418

    def col(x, steps):
        boxes = []
        y = y0
        for cls, t, ls, tag in steps:
            boxes.append(d.box(x, y, LW, BH, cls, t, ls, tag=tag))
            y += BH + GAP
        return boxes

    r = col(25, [
        (A, "Mini-spec o delta", ["§1, 2, 4, 8, 9, 14, 15", "modificación: CHANGE-SET mínimo"], None),
        (A, "Checks express inline", ["verify EXPRESS (F2, F5, F6, C3–C5)", "sin revisión adversaria (Regla 4)"], None),
        (G, "Aprobación única", ["track + spec/delta + plan", "leí, apruebo"], "GATE"),
    ])
    e = col(277, [
        (A, "Spec-first en lote", ["prompt 08 (modif.: 07 + CHANGE-SET)", "alto impacto → [DECIDIR-N]"], None),
        (G, "G1 · Preguntas en lote", ["confirmo track · opciones + recomendación", "ok · ok salvo 3:B"], "GATE"),
        (A, "Revisión unificada", ["subagente: adversaria + verify", "modificación: acotada al delta"], None),
        (G, "G2 + G3 · Spec y plan", ["superficie de decisión (§4,6,7,8,10,14)", "leí, apruebo"], "GATE"),
    ])
    c = col(529, [
        (G, "G1 · Discovery profundo", ["track confirmado al abrir", "prompts 01 → 02, por sección"], "GATE"),
        (A, "Revisión unificada completa", ["adversaria + verify COMPLETO", "pasada 2 solo si hubo bloqueantes"], None),
        (G, "G2 · Aprobación de spec", ["superficie de decisión", "leí, apruebo · §14 en lote"], "GATE"),
        (G, "G3 · Plan único", ["una tabla para todas las capas", "plan ok"], "GATE"),
    ])
    for h, lane in ((heads[0], r), (heads[1], e), (heads[2], c)):
        down(d, h, lane[0])
        for a, b in zip(lane, lane[1:]):
            down(d, a, b)

    impl = d.box(140, 770, 500, 66, "c-blue", "Implementación autónoma (rama feature/<ID>)",
                 ["Tests de §8/§9 primero → capas 1→4 del plan", "Gate automático entre capas: tests + typecheck · sin gates humanos"])
    # flechas de convergencia
    d.arrow(bottom(r[-1]), (138, 752), (200, 752), (200, 768))
    d.arrow(bottom(e[-1]), (390, 768))
    d.arrow(bottom(c[-1]), (642, 752), (580, 752), (580, 768))
    d.text(760, 851, "detalle: flow_codegen_y_deploy.svg", cls="ts", anchor="end")

    rev = d.box(140, 858, 500, 66, "c-purple", "Revisión de código — una por feature",
                ["Completo / nueva Estándar: diff completo (2 subagentes si es grande)",
                 "Modif. Estándar / Rápido con lógica: acotada al diff · pura presentación: inline"])
    down(d, impl, rev)
    g4 = d.box(140, 946, 500, 66, G, "G4 · Prueba manual acotada → commit",
               ["Lo cubierto por tests no se repite · a mano: experiencia, integraciones, happy path real",
                "ok = commit único · ok push · falla → vuelve a código"], tag="GATE")
    down(d, rev, g4)
    end = d.box(190, 1034, 400, 44, "c-gray", "Commit feat(<ID>) → deploy staging → main",
                ["tras el merge a main: spec e INDEX → Implemented"], rx=22)
    down(d, g4, end)

    d.box(25, 1100, 360, 96, "c-coral", "Válvula de escape",
          ["Si aparece riesgo que el track no admite,", "el track sube en el acto y se ejecutan", "los pasos salteados antes de seguir.", "Queda en el changelog de la spec (Regla 5)."])
    d.box(395, 1100, 360, 96, "c-gray", "Interrupciones legítimas (fuera de gates)",
          ["Decisión de alto impacto no prevista · válvula", "Conflicto spec vs foundation · semáforo ROJO",
           "Tests en rojo tras 2 intentos de corrección", "Nada más frena el flujo."])
    d.save("flow_ciclo_feature.svg")


# ---------------------------------------------------------------- codegen y deploy
def codegen_deploy():
    d = Diagram(780, "Flujo de codegen (MODO FEATURE) y deploy — WORKFLOW v20",
                "Fase 6 en MODO FEATURE: plan único, generación capa por capa con tests primero y gate automático, "
                "una revisión de código por feature, prueba manual que autoriza el commit, y deploy a staging y producción.")
    d.heading(30, 36, "Fase 6 — Codegen (MODO FEATURE) y deploy",
              "Un plan, capas seguidas con gate automático, una revisión de código, una prueba manual, un commit.")
    G, A = "c-amber", "c-purple"
    s = d.box(190, 76, 400, 48, "c-gray", "Spec Approved + plan confirmado",
              ["G2/G3 (Completo) · plan junto a la aprobación (Rápido / Estándar)"], rx=22)
    br = d.box(190, 146, 400, 48, A, "Rama feature/<ID> desde main", ["git checkout main && git pull && git checkout -b feature/<ID>"])
    down(d, s, br)

    d.box(20, 216, 740, 446, "c-gray", "", [], rx=12)
    d.text(36, 236, "LOOP por capa", cls="th", fill="#2C2C2A")
    d.text(744, 236, "capas del plan: 1 Datos → 2 Negocio → 3 API → 4 UI · sin gates humanos", cls="ts", anchor="end")
    d.arrow(bottom(br), (390, 248))
    t1 = d.box(190, 250, 400, 52, A, "Tests primero", ["CA de §8 y casos borde de §9 que tocan la capa → fallan"])
    t2 = d.box(190, 322, 400, 52, A, "Implementar la capa", ["Write/Edit a disco · modificación: solo ítems del CHANGE-SET"])
    down(d, t1, t2)
    d.diamond(390, 430, 300, 76, "c-gray", ["Gate automático", "tests + suite + typecheck/build"])
    d.arrow(bottom(t2), (390, 392))
    fix = d.box(574, 404, 172, 52, "c-coral", "Corregir", ["máx. 2 intentos; al 3º frenar:", "revisar la spec (§8.2)"])
    d.arrow((540, 430), (572, 430), label="rojo", label_at=(544, 424))
    d.arrow((660, 404), (660, 336), (592, 336))
    d.diamond(390, 540, 220, 64, "c-gray", ["¿Última capa", "del plan?"])
    d.arrow((390, 468), (390, 508), label="verde", label_at=(396, 492))
    d.arrow((280, 540), (110, 540), (110, 276), (188, 276), label="no → siguiente capa", label_at=(118, 532))
    dec = d.box(190, 590, 400, 52, A, "Decisiones técnicas por defecto", ["se acumulan en una lista (se validan en G4)"])
    d.arrow((390, 572), (390, 588), label="sí", label_at=(396, 584))

    rev = d.box(140, 684, 500, 66, A, "Revisión de código — una por feature (según track)",
                ["Completo / nueva Estándar: diff completo · grande: 2 subagentes en paralelo",
                 "Modif. Estándar / Rápido con lógica: acotada al diff · pura presentación: inline"])
    d.arrow(bottom(dec), top(rev))
    d.diamond(390, 800, 230, 64, "c-gray", ["¿Bloqueantes?"])
    d.arrow(bottom(rev), (390, 768))
    bl = d.box(574, 774, 172, 52, "c-coral", "Corregir + re-gate", ["decisión de alto impacto →", "interrupción"])
    d.arrow((505, 800), (572, 800), label="sí", label_at=(520, 794))
    debt = d.box(190, 852, 400, 44, A, "No bloqueantes → sdd/DEBT.md", ["formato /sdd-defer, tipo deuda-tecnica"])
    d.arrow((390, 832), (390, 850), label="no", label_at=(396, 846))
    g4 = d.box(140, 918, 500, 66, G, "G4 · Prueba manual acotada",
               ["Ya cubierto por tests: listado, no se repite · a mano: experiencia,", "integraciones reales, ≥1 happy path en el entorno real"], tag="GATE")
    down(d, debt, g4)
    d.diamond(390, 1036, 220, 64, "c-gray", ["¿Funciona?"])
    d.arrow(bottom(g4), (390, 1004))
    d.arrow((280, 1036), (70, 1036), (70, 348), (188, 348), label="no → volver a código", label_at=(78, 1028))
    cm = d.box(190, 1090, 400, 48, A, "Commit único: feat(<ID>): …", ["ok = autoriza el commit · ok push = también pushea"])
    d.arrow((390, 1068), (390, 1088), label="ok", label_at=(396, 1082))

    stg = d.box(190, 1162, 400, 52, "c-blue", "Deploy a staging", ["git checkout staging && git merge feature/<ID> && git push"])
    down(d, cm, stg)
    d.diamond(390, 1270, 230, 64, "c-gray", ["¿Cliente aprueba", "en staging?"])
    d.arrow(bottom(stg), (390, 1238))
    d.box(574, 1244, 172, 52, "c-coral", "Ajustes", ["cambio de producto →", "/sdd-feature <ID> \"cambio\""])
    d.arrow((505, 1270), (572, 1270), label="no", label_at=(520, 1264))
    prod = d.box(190, 1324, 400, 52, "c-teal", "Deploy a producción", ["git checkout main && git merge feature/<ID> && git push"])
    d.arrow((390, 1302), (390, 1322), label="sí", label_at=(396, 1316))
    idx = d.box(190, 1398, 400, 48, A, "Spec e INDEX → Implemented", ["git branch -d feature/<ID>"])
    down(d, prod, idx)
    end = d.box(240, 1468, 300, 40, "c-gray", "Siguiente feature del roadmap", [], rx=20)
    down(d, idx, end)
    d.save("flow_codegen_y_deploy.svg")


# ---------------------------------------------------------------- mapa general
def process_overview():
    d = Diagram(700, "Proceso SDD completo — toolkit detallado (WORKFLOW v20)",
                "Mapa del proceso SDD: Fase 0, ciclo de feature en Modo Flow con tracks, bugs, deploy, artefactos "
                "de gobierno e inventario del toolkit.")
    d.heading(30, 36, "Proceso SDD completo",
              "WORKFLOW v20 · Modo Flow (/sdd-feature) · tracks Rápido / Estándar / Completo")
    P, T, G = "c-purple", "c-teal", "c-amber"

    d.box(30, 76, 640, 46, "c-gray", "Fase 0 — Inicio del proyecto (una vez)", ["Output: setup foundacional + roadmap + prototipo"])
    a = d.box(30, 138, 152, 62, P, "1. Discovery", ["00-project-discovery", "idea → decisiones"])
    b = d.box(193, 138, 152, 62, P, "2. Setup + roadmap", ["00b-setup-foundation", "6 docs + ROADMAP"])
    c = d.box(356, 138, 152, 62, P, "3. Prototipo UI", ["00c-design-prototype", "Claude Design"])
    e = d.box(519, 138, 151, 62, "c-gray", "4. Propuesta", ["fuera del SDD", "roadmap + prototipo"])
    for x1, x2 in ((182, 193), (345, 356), (508, 519)):
        d.arrow((x1, 169), (x2 - 2, 169))

    d.box(30, 224, 640, 46, "c-gray", "Ciclo de feature — Modo Flow: /sdd-feature",
          ["Se repite por cada feature o cambio. Clasificación por riesgo (protocols/track-routing.md)"])
    d.arrow((350, 200), (350, 222))
    d.box(30, 284, 206, 58, "c-teal", "Rápido — 2 gates", ["mini-spec o delta", "sin revisión de spec"])
    d.box(247, 284, 206, 58, "c-blue", "Estándar — 3 gates", ["spec-first en lote", "G2 + G3 fusionados"])
    d.box(464, 284, 206, 58, "c-coral", "Completo — 4 gates", ["discovery profundo", "G1 · G2 · G3 · G4"])

    rows = [
        (P, "Spec", ["08-spec-first · 07-modify-spec", "Completo: 01 → 02"], T, "Spec Draft", ["alto impacto → [DECIDIR-N]", "bajo impacto → §14"], "G1"),
        (P, "Revisión unificada", ["03-adversarial-spec + 06-verification", "subagente · no en Rápido"], T, "Spec en Review", ["§10.2 + semáforo", "pasada 2 si bloqueantes"], None),
        (G, "Aprobación (G2)", ["superficie de decisión", "leí, apruebo"], T, "Spec Approved", ["INDEX actualizado", "§14 validada"], None),
        (P, "Plan + código", ["04-codegen-layer MODO FEATURE", "tests 1º · gate automático"], T, "Código + tests", ["rama feature/<ID>", "capas 1→4 del plan"], "G3"),
        (P, "Revisión de código", ["05-adversarial-code", "una por feature, según track"], T, "Hallazgos procesados", ["bloqueantes corregidos", "resto → DEBT.md"], None),
        (G, "Prueba manual (G4)", ["acotada a lo no cubierto", "ok = commit"], T, "Commit único", ["feat(<ID>): …", "→ deploy"], None),
    ]
    y = 362
    prev = None
    for lc, lt, ll, rc, rt, rl, tag in rows:
        lb = d.box(30, y, 300, 58, lc, lt, ll, tag=("GATE " + tag) if tag else ("GATE" if lc == G else None))
        d.box(370, y, 300, 58, rc, rt, rl)
        d.arrow((330, y + 29), (368, y + 29))
        if prev:
            d.arrow(bottom(prev), top(lb))
        prev = lb
        y += 76

    d.box(30, y + 4, 310, 74, "c-pink", "Bugs — /sdd-bugfix", ["A código · B spec (primero spec) · C negocio", "test de regresión antes del fix",
                                                               "bugfix-NNN.md solo si B, Crítico/Alto o causa no obvia"])
    d.box(360, y + 4, 310, 74, "c-gray", "Deploy y ramas", ["feature/<ID> → staging → cliente valida", "→ main → Implemented",
                                                            "hotfix/* → main + staging"])
    y += 98
    d.text(30, y + 8, "Artefactos de gobierno", cls="th", fill="#2C2C2A")
    gov = [("WORKFLOW.md", ["5 reglas (v20) · tracks", "antipatrones"]), ("INDEX", ["estado de cada spec", "asignación de IDs"]),
           ("ROADMAP", ["specs por fase", "estimación gruesa"]), ("DEBT.md", ["pendientes diferidos", "/sdd-defer · review"])]
    for i, (t, ls) in enumerate(gov):
        d.box(30 + i * 162, y + 20, 154, 58, "c-amber", t, ls)
    y += 100
    d.text(30, y + 8, "Inventario del toolkit", cls="th", fill="#2C2C2A")
    inv = [("12 comandos", ["/sdd-feature por defecto", "+ camino manual por fase"]), ("11 prompts", ["3 de Fase 0", "8 del ciclo de feature"]),
           ("14 templates", ["foundation, spec, bugfix,", "debt, ADR, design system"]), ("2 protocolos", ["track-routing", "codegen-protocol"])]
    for i, (t, ls) in enumerate(inv):
        d.box(30 + i * 162, y + 20, 154, 58, "c-purple", t, ls)
    y += 100
    d.text(30, y + 6, "Leyenda:  violeta = la IA ejecuta (prompt/comando) · verde = artefacto producido · ámbar = gate humano o documento", cls="ts")
    d.text(30, y + 22, "de gobierno · celeste/coral = tracks · rosa = bugs · gris = fases y deploy", cls="ts")
    d.save("process-diagram.svg")


if __name__ == "__main__":
    ciclo_feature()
    codegen_deploy()
    process_overview()
