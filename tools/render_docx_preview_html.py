from __future__ import annotations

from html import escape
from pathlib import Path

from docx import Document
from docx.document import Document as DocumentType
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph


ROOT = Path(__file__).resolve().parents[1]
DOCX_PATH = ROOT / "reports" / "human" / "M55_Vega_Coordination_Ledger.docx"
HTML_PATH = ROOT / "reports" / "human" / "M55_Vega_Coordination_Ledger.html"


def iter_blocks(parent):
    if isinstance(parent, DocumentType):
        parent_elm = parent.element.body
    else:
        parent_elm = parent._tc

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def paragraph_html(paragraph: Paragraph) -> str:
    text = paragraph.text.strip()
    if not text:
        return ""

    style = paragraph.style.name if paragraph.style is not None else ""
    if style == "Heading 1":
        return f"<h2>{escape(text)}</h2>"
    if style == "Heading 2":
        return f"<h3>{escape(text)}</h3>"
    if style == "Heading 3":
        return f"<h4>{escape(text)}</h4>"
    if text == "M55 + Vega Coordination Ledger":
        return f"<h1>{escape(text)}</h1>"
    if text.startswith("Human-facing checkpoint"):
        return f"<p class=\"subtitle\">{escape(text)}</p>"
    return f"<p>{escape(text)}</p>"


def table_html(table: Table) -> str:
    rows = []
    for row_index, row in enumerate(table.rows):
        cells = []
        tag = "th" if row_index == 0 else "td"
        for cell in row.cells:
            text = " ".join(p.text.strip() for p in cell.paragraphs if p.text.strip())
            class_name = ""
            upper = text.upper()
            if row_index > 0 and any(word in upper for word in ("WAITING", "WORKING", "DONE", "BLOCKED", "DECIDED")):
                class_name = " status"
            if row_index > 0 and "WAITING" in upper:
                class_name += " waiting"
            elif row_index > 0 and any(word in upper for word in ("WORKING", "DONE", "DECIDED")):
                class_name += " done"
            elif row_index > 0 and "BLOCKED" in upper:
                class_name += " blocked"
            cells.append(f"<{tag} class=\"{class_name.strip()}\">{escape(text)}</{tag}>")
        rows.append(f"<tr>{''.join(cells)}</tr>")
    return f"<table>{''.join(rows)}</table>"


def build_html(docx_path: Path, html_path: Path) -> Path:
    document = Document(docx_path)
    body = []
    for block in iter_blocks(document):
        if isinstance(block, Paragraph):
            html = paragraph_html(block)
        else:
            html = table_html(block)
        if html:
            body.append(html)

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>M55 + Vega Coordination Ledger</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #0b2545;
      --muted: #5b677a;
      --line: #b9c3cf;
      --header: #e8eef5;
      --surface: #ffffff;
      --page: #f5f7fa;
      --blue: #2e74b5;
      --waiting: #fff4cc;
      --done: #eaf6ef;
      --blocked: #fce8e6;
    }}
    body {{
      margin: 0;
      background: var(--page);
      color: #1f2937;
      font: 15px/1.5 Calibri, Arial, sans-serif;
    }}
    main {{
      max-width: 980px;
      margin: 24px auto;
      padding: 36px 44px 48px;
      background: var(--surface);
      border: 1px solid #d7dde5;
      box-shadow: 0 18px 50px rgba(31, 41, 55, 0.10);
    }}
    h1 {{
      margin: 0 0 2px;
      color: var(--ink);
      font-size: 34px;
      line-height: 1.12;
    }}
    .subtitle {{
      margin: 0 0 18px;
      color: var(--muted);
      font-size: 14px;
    }}
    h2 {{
      margin: 28px 0 12px;
      color: var(--blue);
      font-size: 22px;
    }}
    h3, h4 {{
      color: #1f4d78;
    }}
    p {{
      margin: 0 0 12px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 8px 0 20px;
      table-layout: fixed;
    }}
    th, td {{
      border: 1px solid var(--line);
      padding: 9px 10px;
      vertical-align: middle;
      overflow-wrap: anywhere;
    }}
    th {{
      background: var(--header);
      color: var(--ink);
      text-align: center;
      font-weight: 700;
    }}
    td.status {{
      text-align: center;
      color: var(--ink);
      font-weight: 700;
    }}
    td.waiting {{
      background: var(--waiting);
    }}
    td.done {{
      background: var(--done);
    }}
    td.blocked {{
      background: var(--blocked);
    }}
    @media (max-width: 760px) {{
      main {{
        margin: 0;
        padding: 22px 16px 32px;
        border: 0;
        box-shadow: none;
      }}
      h1 {{
        font-size: 28px;
      }}
      table {{
        display: block;
        overflow-x: auto;
        table-layout: auto;
      }}
      th, td {{
        min-width: 140px;
      }}
    }}
  </style>
</head>
<body>
  <main>
    {''.join(body)}
  </main>
</body>
</html>
"""
    html_path.write_text(html, encoding="utf-8")
    return html_path


if __name__ == "__main__":
    print(build_html(DOCX_PATH, HTML_PATH))
