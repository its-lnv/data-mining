"""Render the Markdown final report to PDF using installed Microsoft Edge.

This helper uses only the Python standard library. Edge is an optional system
tool for PDF export and is not needed to run the data-mining workflow.
"""

import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_PATH = PROJECT_ROOT / "docs" / "final_project_report.md"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "submission"
HTML_PATH = OUTPUT_DIR / "Cervical_Cancer_Data_Mining_Report.html"
PDF_PATH = OUTPUT_DIR / "Cervical_Cancer_Data_Mining_Report.pdf"


def browser_executable():
    """Find an installed Chromium-based browser without installing software."""
    found = (
        shutil.which("msedge")
        or shutil.which("msedge.exe")
        or shutil.which("chrome")
        or shutil.which("chrome.exe")
    )
    if found:
        return Path(found)
    candidates = []
    for env_name in ("ProgramFiles(x86)", "ProgramFiles"):
        base = os.environ.get(env_name)
        if not base:
            continue
        candidates.extend(
            [
                Path(base) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
                Path(base) / "Google" / "Chrome" / "Application" / "chrome.exe",
            ]
        )
    local_data = os.environ.get("LOCALAPPDATA")
    if local_data:
        candidates.extend(
            [
                Path(local_data) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
                Path(local_data) / "Google" / "Chrome" / "Application" / "chrome.exe",
            ]
        )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        "Microsoft Edge or Google Chrome was not found. Install no packages for this step; "
        "open the Markdown report in another PDF-capable application and export it manually."
    )


def inline_markup(text, source_dir):
    """Convert a small safe subset of Markdown inline syntax to HTML."""
    escaped = html.escape(text, quote=True)
    placeholders = []

    def hold(value):
        token = f"@@INLINE{len(placeholders)}@@"
        placeholders.append(value)
        return token

    image_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    def image_replacement(match):
        image_path = (source_dir / html.unescape(match.group(2))).resolve()
        # Keep report figures portable: the HTML lives in outputs/submission
        # and the PNGs live in outputs/graphs, so use a relative URL between
        # those directories instead of an absolute file:/// URL tied to this PC.
        if image_path.is_file():
            relative_path = os.path.relpath(image_path, OUTPUT_DIR).replace(os.sep, "/")
            uri = quote(relative_path, safe="/")
        else:
            uri = ""
        return hold(
            f'<figure><img src="{html.escape(uri, quote=True)}" '
            f'alt="{html.escape(match.group(1), quote=True)}"></figure>'
        )

    escaped = image_pattern.sub(image_replacement, escaped)

    def link_replacement(match):
        target = html.unescape(match.group(2))
        if target.startswith(("https://", "http://", "mailto:")):
            href = target
        else:
            local_path = (source_dir / target).resolve()
            href = local_path.as_uri() if local_path.exists() else target
        return hold(
            f'<a href="{html.escape(href, quote=True)}">{match.group(1)}</a>'
        )

    escaped = link_pattern.sub(link_replacement, escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    for index, value in enumerate(placeholders):
        escaped = escaped.replace(f"@@INLINE{index}@@", value)
    return escaped


def markdown_to_html(markdown_text):
    """Render report headings, paragraphs, tables, lists, images, and code."""
    lines = markdown_text.splitlines()
    output = []
    paragraph = []
    list_kind = None
    code_lines = []
    table_lines = []
    in_title_section = False
    in_cover_page = False
    source_dir = MARKDOWN_PATH.parent

    def flush_paragraph():
        if paragraph:
            output.append("<p>" + inline_markup(" ".join(paragraph), source_dir) + "</p>")
            paragraph.clear()

    def close_list():
        nonlocal list_kind
        if list_kind:
            output.append(f"</{list_kind}>")
            list_kind = None

    def flush_table():
        if not table_lines:
            return
        parsed = []
        for table_line in table_lines:
            cells = [cell.strip() for cell in table_line.strip().strip("|").split("|")]
            if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                continue
            parsed.append(cells)
        if parsed:
            header = parsed[0]
            output.append('<table><thead><tr>')
            output.extend(f"<th>{inline_markup(cell, source_dir)}</th>" for cell in header)
            output.append("</tr></thead><tbody>")
            for row in parsed[1:]:
                output.append("<tr>")
                for index, cell in enumerate(row):
                    tag = "th" if index == 0 else "td"
                    output.append(f"<{tag}>{inline_markup(cell, source_dir)}</{tag}>")
                output.append("</tr>")
            output.append("</tbody></table>")
        table_lines.clear()

    def flush_blocks():
        flush_paragraph()
        close_list()
        flush_table()

    for line in lines:
        if line.startswith("```"):
            if code_lines:
                output.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines.clear()
            else:
                flush_blocks()
                code_lines.append("__CODE_BLOCK_OPEN__")
            continue
        if code_lines:
            if code_lines == ["__CODE_BLOCK_OPEN__"]:
                code_lines.clear()
            code_lines.append(line)
            continue

        if not line.strip():
            flush_blocks()
            continue

        if in_title_section and line.startswith("## "):
            output.append("</section>")
            in_title_section = False
            if in_cover_page:
                output.append("</section>")
                in_cover_page = False

        if line.startswith("|"):
            flush_paragraph()
            close_list()
            table_lines.append(line)
            continue
        flush_table()

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading_match:
            flush_paragraph()
            close_list()
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2)
            if level == 1 and not in_cover_page:
                output.append('<section class="cover-page">')
                in_cover_page = True
            if level == 2 and heading_text == "Title Page":
                output.append('<section class="title-page">')
                in_title_section = True
            output.append(f"<h{level}>{inline_markup(heading_text, source_dir)}</h{level}>")
            continue

        if line.startswith("> "):
            flush_paragraph()
            close_list()
            output.append(f"<blockquote>{inline_markup(line[2:], source_dir)}</blockquote>")
            continue

        if line.startswith("!["):
            flush_paragraph()
            close_list()
            output.append(inline_markup(line, source_dir))
            continue

        ordered = re.match(r"^\s*\d+\.\s+(.*)$", line)
        bullet = re.match(r"^\s*[-*]\s+(.*)$", line)
        if ordered or bullet:
            flush_paragraph()
            wanted = "ol" if ordered else "ul"
            if list_kind != wanted:
                close_list()
                output.append(f"<{wanted}>")
                list_kind = wanted
            text = ordered.group(1) if ordered else bullet.group(1)
            output.append(f"<li>{inline_markup(text, source_dir)}</li>")
            continue

        close_list()
        hard_break = line.endswith("  ")
        paragraph.append(line.rstrip())
        if hard_break:
            flush_paragraph()

    flush_blocks()
    if in_title_section:
        output.append("</section>")
    if in_cover_page:
        output.append("</section>")
    return "\n".join(output)


def main():
    if not MARKDOWN_PATH.is_file():
        raise FileNotFoundError(f"Final Markdown report not found: {MARKDOWN_PATH}")
    browser = browser_executable()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    body = markdown_to_html(MARKDOWN_PATH.read_text(encoding="utf-8"))
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Cervical Cancer Data Mining Report</title>
<style>
@page {{ size: A4; margin: 17mm 16mm 18mm; }}
* {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; background:#edf2f7; }}
body {{ max-width:980px; margin:36px auto; padding:64px 76px; background:#fff; color:#243247; font-family:Inter, 'Segoe UI', Arial, sans-serif; font-size:16px; line-height:1.72; box-shadow:0 18px 55px rgba(24,45,70,.13); border:1px solid #dce5ef; }}
h1 {{ text-align:center; font-size:clamp(2rem,4vw,3rem); line-height:1.15; letter-spacing:-.035em; margin:0 0 38px; padding:30px 12px 26px; color:#12345a; border-bottom:4px solid #3b82a0; }}
.title-page {{ padding:24px 34px 28px; margin:0 0 38px; border:1px solid #d8e4ef; border-top:5px solid #3b82a0; border-radius:12px; background:linear-gradient(145deg,#f8fbff,#eef5fa); }}
.cover-page {{ break-inside:avoid; page-break-inside:avoid; }}
.title-page h2 {{ margin:0 0 24px; color:#39718d; border:0; font-size:13px; letter-spacing:.14em; text-transform:uppercase; }}
.title-page p {{ margin:0; padding:9px 0; border-bottom:1px solid #dce6ee; font-size:15px; }}
.title-page p strong {{ display:inline-block; min-width:190px; color:#34516b; }}
.title-page p:last-of-type {{ border-bottom:0; }}
.title-page a {{ display:inline-block; padding:4px 10px; border:1px solid #a7c8d8; border-radius:6px; background:#e8f3f8; color:#125879; font-size:14px; font-weight:700; text-decoration:none; }}
.title-page blockquote {{ margin:25px 0 0; }}
h2 {{ color:#173d63; font-size:25px; line-height:1.3; margin:52px 0 18px; padding-bottom:10px; border-bottom:2px solid #dce8f1; page-break-after:avoid; }}
h3 {{ color:#2d6983; font-size:19px; line-height:1.35; margin:34px 0 12px; page-break-after:avoid; }}
p {{ margin:14px 0; text-align:left; }}
ul,ol {{ margin:12px 0 20px; padding-left:28px; }}
li {{ margin:7px 0; padding-left:3px; }}
blockquote {{ border-left:4px solid #3b82a0; background:#edf5f8; color:#304a5d; margin:22px 0; padding:16px 20px; border-radius:0 8px 8px 0; }}
table {{ width:100%; border-collapse:separate; border-spacing:0; margin:22px 0 30px; table-layout:fixed; font-size:13px; overflow:hidden; border:1px solid #d7e1ea; border-radius:8px; page-break-inside:auto; }}
thead {{ display:table-header-group; }}
tr {{ page-break-inside:avoid; }}
th,td {{ border-right:1px solid #e0e7ed; border-bottom:1px solid #e0e7ed; padding:11px 12px; vertical-align:top; overflow-wrap:anywhere; }}
th:last-child,td:last-child {{ border-right:0; }}
tbody tr:last-child td {{ border-bottom:0; }}
th {{ background:#e8f1f7; color:#173d63; text-align:left; font-weight:700; }}
tbody tr:nth-child(even) {{ background:#f8fafc; }}
figure {{ margin:26px 0 12px; text-align:center; page-break-inside:avoid; }}
img {{ max-width:100%; max-height:118mm; object-fit:contain; border:1px solid #dce5ed; border-radius:8px; box-shadow:0 5px 18px rgba(24,45,70,.10); }}
code {{ font-family:Consolas, 'SFMono-Regular', monospace; font-size:.88em; color:#214e69; background:#edf3f7; padding:2px 5px; border-radius:4px; overflow-wrap:anywhere; }}
pre {{ white-space:pre-wrap; overflow-wrap:anywhere; background:#f2f6f9; border:1px solid #dce5ed; border-radius:8px; padding:16px; font-size:13px; page-break-inside:avoid; }}
a {{ color:#176b91; text-decoration-thickness:1px; text-underline-offset:3px; }}
a:hover {{ color:#0d4967; }}
@media (max-width:760px) {{ body {{ width:auto; margin:0; padding:30px 22px; border:0; box-shadow:none; font-size:15px; }} h1 {{ font-size:2rem; padding:20px 4px; }} h2 {{ font-size:22px; margin-top:38px; }} h3 {{ font-size:18px; }} .title-page {{ padding:20px; }} .title-page p strong {{ display:block; min-width:0; }} table {{ display:block; overflow-x:auto; white-space:normal; }} th,td {{ min-width:100px; padding:9px; }} }}
@media print {{ html {{ background:#fff; }} body {{ width:auto; max-width:none; margin:0; padding:0; border:0; box-shadow:none; color:#202124; font-size:9.2pt; line-height:1.42; }} .cover-page {{ min-height:258mm; display:flex; flex-direction:column; break-inside:avoid; page-break-inside:avoid; break-after:page; page-break-after:always; }} h1 {{ font-size:22pt; margin:4mm 0 7mm; padding:4mm 0; }} .title-page {{ flex:1; display:flex; flex-direction:column; justify-content:space-around; padding:7mm 10mm; margin:0; border:1px solid #d8e4ef; border-top:3px solid #3b82a0; border-radius:0; }} .title-page h2 {{ margin:0; }} .title-page p {{ padding:2mm 0; font-size:10.5pt; }} .title-page p strong {{ min-width:48mm; }} .title-page a {{ padding:2mm 3mm; border:1px solid #a7c8d8; border-radius:2mm; background:#e8f3f8; color:#125879; font-size:9.5pt; font-weight:700; }} h2 {{ font-size:15pt; margin-top:8mm; }} h3 {{ font-size:11.5pt; margin-top:6mm; }} p {{ margin:3mm 0; text-align:justify; }} ul,ol {{ margin:2mm 0 4mm 7mm; padding-left:5mm; }} li {{ margin:1mm 0; }} blockquote {{ margin:5mm 0; padding:3mm 5mm; }} table {{ border-radius:0; font-size:7.3pt; }} th,td {{ padding:2.2mm 1.7mm; }} figure {{ margin:4mm 0 1mm; }} img {{ box-shadow:none; border-radius:0; }} a {{ color:#1a5d87; text-decoration:none; }} }}
</style></head><body>{body}</body></html>"""
    HTML_PATH.write_text(page, encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="cervical_report_edge_") as profile:
        command = [
            str(browser),
            "--headless",
            "--disable-gpu",
            "--disable-gpu-compositing",
            "--disable-software-rasterizer",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--no-first-run",
            "--no-default-browser-check",
            f"--user-data-dir={profile}",
            "--no-pdf-header-footer",
            f"--print-to-pdf={PDF_PATH}",
            HTML_PATH.resolve().as_uri(),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if result.returncode != 0 or not PDF_PATH.is_file() or PDF_PATH.stat().st_size < 10_000:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"Edge PDF export failed (exit {result.returncode}). {detail}")
    print(f"Browser: {browser}")
    print(f"HTML report: {HTML_PATH.relative_to(PROJECT_ROOT)}")
    print(f"PDF report: {PDF_PATH.relative_to(PROJECT_ROOT)} ({PDF_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
