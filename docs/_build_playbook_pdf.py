"""Convierte PLAYBOOK.md a PDF imprimible (A4) usando markdown + xhtml2pdf.
Uso: python _build_playbook_pdf.py
"""
import os
import markdown
from xhtml2pdf import pisa
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

FONTS = r"C:\Windows\Fonts"


def register_fonts():
    pdfmetrics.registerFont(TTFont("Body", os.path.join(FONTS, "arial.ttf")))
    pdfmetrics.registerFont(TTFont("Body-Bold", os.path.join(FONTS, "arialbd.ttf")))
    pdfmetrics.registerFont(TTFont("Mono", os.path.join(FONTS, "consola.ttf")))
    registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body", boldItalic="Body-Bold")
    registerFontFamily("Mono", normal="Mono", bold="Mono", italic="Mono", boldItalic="Mono")

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "PLAYBOOK.md")
OUT = os.path.join(HERE, "PLAYBOOK.pdf")

CSS = """
@page { size: A4; margin: 1.8cm 1.6cm; }
body { font-family: "Body"; font-size: 9.5pt; line-height: 1.4; color: #1a1a1a; }
h1 { font-family: "Body"; font-weight: bold; font-size: 20pt; color: #1b1b3a; border-bottom: 2px solid #4f46e5; padding-bottom: 4px; }
h2 { font-family: "Body"; font-weight: bold; font-size: 14pt; color: #312e81; background: #eef2ff; padding: 5px 8px; margin-top: 14px;
     page-break-before: always; page-break-after: avoid; }
h3 { font-family: "Body"; font-weight: bold; font-size: 11pt; color: #3730a3; margin-top: 10px; page-break-after: avoid; }
p, li { font-size: 9.5pt; }
ul { margin: 4px 0 8px 0; }
li { margin-bottom: 2px; }
code { font-family: "Mono"; background: #f1f1f4; font-size: 8.7pt; padding: 1px 3px; }
pre { background: #1e1e2e; color: #e4e4e7; font-family: "Mono"; font-size: 8.3pt;
      padding: 8px 10px; margin: 6px 0; }
pre code { background: transparent; color: #e4e4e7; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 6px 0; }
th { background: #4f46e5; color: #ffffff; font-weight: bold; font-size: 8.7pt; padding: 5px 6px; text-align: left; }
td { border: 0.5px solid #c7c7d1; font-size: 8.7pt; padding: 4px 6px; vertical-align: top; }
tr:nth-child(even) td { background: #f7f7fb; }
blockquote { background: #fffbeb; border-left: 3px solid #f59e0b; padding: 5px 10px; margin: 6px 0;
             color: #4a3a00; font-size: 9pt; }
hr { border: none; border-top: 0.5px solid #ddd; margin: 8px 0; }
"""

# Caracteres de dibujo de caja → ASCII garantizado en cualquier fuente (solo para el PDF).
BOX_TO_ASCII = [
    ("└─", "\\-"), ("├─", "+-"), ("┌─", "+-"), ("┐", "+"), ("┘", "+"),
    ("├", "+"), ("└", "\\"), ("┌", "+"), ("│", "|"), ("─", "-"),
]


def sanitize_for_pdf(text):
    for uni, ascii_ in BOX_TO_ASCII:
        text = text.replace(uni, ascii_)
    return text


def main():
    register_fonts()
    with open(SRC, encoding="utf-8") as f:
        text = sanitize_for_pdf(f.read())
    html_body = markdown.markdown(
        text, extensions=["tables", "fenced_code", "sane_lists"]
    )
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html_body}</body></html>"
    with open(OUT, "wb") as out:
        result = pisa.CreatePDF(html, dest=out, encoding="utf-8")
    if result.err:
        raise SystemExit(f"Errores al generar PDF: {result.err}")
    size = os.path.getsize(OUT)
    print(f"OK -> {OUT} ({size/1024:.0f} KB)")

if __name__ == "__main__":
    main()
