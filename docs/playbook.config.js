// Config para generar PLAYBOOK.pdf con md-to-pdf.
// Uso:  md-to-pdf --config-file docs/playbook.config.js docs/PLAYBOOK.md
// (Chromium renderiza Unicode nativo: flechas, cajas y emoji salen perfectos,
//  por eso acá NO hace falta sanitizar nada como con el approach anterior.)
module.exports = {
  pdf_options: {
    format: 'A4',
    margin: { top: '18mm', right: '16mm', bottom: '18mm', left: '16mm' },
    printBackground: true,
  },
  css: `
    .markdown-body { font-size: 11px; }
    h2 { page-break-before: always; }            /* cada flujo en su propia hoja */
    h1, h2, h3 { page-break-after: avoid; }
    pre, table, blockquote { page-break-inside: avoid; }
    h1 { border-bottom: 2px solid #4f46e5; }
    h2 { background: #eef2ff; padding: 6px 10px; border: 0; color: #312e81; }
    table th { background: #4f46e5; color: #fff; }
    blockquote { background: #fffbeb; border-left: 3px solid #f59e0b; color: #4a3a00; }
  `,
};
