"""Create a DOCX copy of the final report using only the Python standard library."""
from pathlib import Path
import html
import re
import struct
import zipfile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "final_project_report.md"
OUTDIR = ROOT / "outputs" / "submission"
OUTPUT = OUTDIR / "Cervical_Cancer_Data_Mining_Report.docx"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC = "http://schemas.openxmlformats.org/drawingml/2006/picture"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
for prefix, uri in (("w", W), ("r", R), ("wp", WP), ("a", A), ("pic", PIC)):
    ET.register_namespace(prefix, uri)

def q(ns, name):
    return f"{{{ns}}}{name}"

def xml(element):
    return ET.tostring(element, encoding="utf-8", xml_declaration=True)

def add_run(parent, value, bold=False, italic=False, code=False):
    run = ET.SubElement(parent, q(W, "r"))
    props = ET.SubElement(run, q(W, "rPr"))
    if bold:
        ET.SubElement(props, q(W, "b"))
    if italic:
        ET.SubElement(props, q(W, "i"))
    if code:
        fonts = ET.SubElement(props, q(W, "rFonts"))
        fonts.set(q(W, "ascii"), "Consolas")
        fonts.set(q(W, "hAnsi"), "Consolas")
        ET.SubElement(props, q(W, "color")).set(q(W, "val"), "365F91")
    text = ET.SubElement(run, q(W, "t"))
    if value[:1].isspace() or value[-1:].isspace():
        text.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    text.text = value

class Renderer:
    def __init__(self):
        self.doc = ET.Element(q(W, "document"))
        self.body = ET.SubElement(self.doc, q(W, "body"))
        self.rels = []
        self.media = []
        self.rid = 2
        self.image_no = 0
        self.paragraph_count = 0
        self.table_count = 0
        self.tick = chr(96)

    def add_link(self, parent, label, target):
        if not target.startswith(("https://", "http://", "mailto:")):
            add_run(parent, label)
            return
        rid = f"rId{self.rid}"
        self.rid += 1
        self.rels.append((rid, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", target, "External"))
        link = ET.SubElement(parent, q(W, "hyperlink"))
        link.set(q(R, "id"), rid)
        run = ET.SubElement(link, q(W, "r"))
        pr = ET.SubElement(run, q(W, "rPr"))
        ET.SubElement(pr, q(W, "color")).set(q(W, "val"), "0563C1")
        ET.SubElement(pr, q(W, "u"))
        t = ET.SubElement(run, q(W, "t"))
        t.text = label

    def inline(self, parent, source):
        t = self.tick
        pattern = re.compile(r"(!\[([^\]]*)\]\(([^)]+)\))|(\[([^\]]+)\]\(([^)]+)\))|(\*\*([^*]+)\*\*)|(" + re.escape(t) + r"([^" + re.escape(t) + r"]+)" + re.escape(t) + r")|(\*([^*]+)\*)")
        pos = 0
        for m in pattern.finditer(source):
            if m.start() > pos:
                add_run(parent, html.unescape(source[pos:m.start()]))
            if m.group(1):
                self.image(m.group(3), m.group(4))
            elif m.group(4):
                self.add_link(parent, html.unescape(m.group(5)), html.unescape(m.group(6)))
            elif m.group(7):
                add_run(parent, html.unescape(m.group(8)), bold=True)
            elif m.group(9):
                add_run(parent, html.unescape(m.group(10)), code=True)
            elif m.group(11):
                add_run(parent, html.unescape(m.group(12)), italic=True)
            pos = m.end()
        if pos < len(source):
            add_run(parent, html.unescape(source[pos:]))

    def para(self, text, style=None, kind=None):
        p = ET.SubElement(self.body, q(W, "p"))
        pp = ET.SubElement(p, q(W, "pPr"))
        if style:
            ET.SubElement(pp, q(W, "pStyle")).set(q(W, "val"), style)
        if kind:
            np = ET.SubElement(pp, q(W, "numPr"))
            ET.SubElement(np, q(W, "ilvl")).set(q(W, "val"), "0")
            ET.SubElement(np, q(W, "numId")).set(q(W, "val"), "1" if kind == "bullet" else "2")
        self.inline(p, text)
        self.paragraph_count += 1

    def image(self, ref, alt):
        path = (SOURCE.parent / ref).resolve()
        p = ET.SubElement(self.body, q(W, "p"))
        if not path.is_file() or path.suffix.lower() != ".png":
            add_run(p, f"[Figure unavailable: {ref}]")
            return
        data = path.read_bytes()
        width, height = struct.unpack(">II", data[16:24])
        max_cx = int(6.7 * 914400)
        cx = max_cx
        cy = int(cx * height / max(width, 1))
        max_cy = int(5.5 * 914400)
        if cy > max_cy:
            cx, cy = int(cx * max_cy / cy), max_cy
        rid = f"rId{self.rid}"
        self.rid += 1
        self.image_no += 1
        name = f"image{self.image_no}.png"
        self.rels.append((rid, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image", f"media/{name}", None))
        self.media.append((name, data))
        drawing = ET.SubElement(ET.SubElement(p, q(W, "r")), q(W, "drawing"))
        inline = ET.SubElement(drawing, q(WP, "inline"))
        for attr in ("distT", "distB", "distL", "distR"):
            inline.set(attr, "0")
        ET.SubElement(inline, q(WP, "extent")).attrib.update({"cx": str(cx), "cy": str(cy)})
        ET.SubElement(inline, q(WP, "docPr")).attrib.update({"id": str(self.image_no), "name": f"Figure {self.image_no}", "descr": alt})
        ET.SubElement(inline, q(WP, "graphicFrameLocks")).set("noChangeAspect", "1")
        graphic = ET.SubElement(inline, q(A, "graphic"))
        gd = ET.SubElement(graphic, q(A, "graphicData"))
        gd.set("uri", PIC)
        pic = ET.SubElement(gd, q(PIC, "pic"))
        nv = ET.SubElement(pic, q(PIC, "nvPicPr"))
        ET.SubElement(nv, q(PIC, "cNvPr")).attrib.update({"id": str(self.image_no), "name": name})
        ET.SubElement(nv, q(PIC, "cNvPicPr"))
        fill = ET.SubElement(pic, q(PIC, "blipFill"))
        ET.SubElement(fill, q(A, "blip")).set(q(R, "embed"), rid)
        ET.SubElement(ET.SubElement(fill, q(A, "stretch")), q(A, "fillRect"))
        shape = ET.SubElement(pic, q(PIC, "spPr"))
        xfrm = ET.SubElement(shape, q(A, "xfrm"))
        ET.SubElement(xfrm, q(A, "off")).attrib.update({"x": "0", "y": "0"})
        ET.SubElement(xfrm, q(A, "ext")).attrib.update({"cx": str(cx), "cy": str(cy)})
        geom = ET.SubElement(shape, q(A, "prstGeom"))
        geom.set("prst", "rect")
        ET.SubElement(geom, q(A, "avLst"))
        self.paragraph_count += 1
        self.para(alt, "Caption")

    def table(self, rows):
        columns = max(map(len, rows))
        wide = columns >= 7
        if wide:
            # Put wide metric tables on a landscape page so their columns can
            # be read without shrinking the type to an illegible size.
            self.section_break("portrait")
        tbl = ET.SubElement(self.body, q(W, "tbl"))
        pr = ET.SubElement(tbl, q(W, "tblPr"))
        table_width = 14000 if wide else 10440
        ET.SubElement(pr, q(W, "tblW")).attrib.update({q(W, "w"): str(table_width), q(W, "type"): "dxa"})
        margins = ET.SubElement(pr, q(W, "tblCellMar"))
        for side, amount in (("top", "55"), ("bottom", "55"), ("left", "75"), ("right", "75")):
            ET.SubElement(margins, q(W, side)).attrib.update({q(W, "w"): amount, q(W, "type"): "dxa"})
        borders = ET.SubElement(pr, q(W, "tblBorders"))
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            ET.SubElement(borders, q(W, edge)).attrib.update({"val": "single", "sz": "4", "color": "B7C9D6"})
        cols = columns
        colw = table_width // cols
        grid = ET.SubElement(tbl, q(W, "tblGrid"))
        for _ in range(cols):
            ET.SubElement(grid, q(W, "gridCol")).set(q(W, "w"), str(colw))
        for index, row in enumerate(rows):
            tr = ET.SubElement(tbl, q(W, "tr"))
            trpr = ET.SubElement(tr, q(W, "trPr"))
            ET.SubElement(trpr, q(W, "cantSplit"))
            if index == 0:
                ET.SubElement(trpr, q(W, "tblHeader")).set(q(W, "val"), "true")
            for value in row:
                tc = ET.SubElement(tr, q(W, "tc"))
                tcpr = ET.SubElement(tc, q(W, "tcPr"))
                ET.SubElement(tcpr, q(W, "tcW")).attrib.update({"w": str(colw), "type": "dxa"})
                if index == 0:
                    ET.SubElement(tcpr, q(W, "shd")).set(q(W, "fill"), "EAF1F7")
                p = ET.SubElement(tc, q(W, "p"))
                ppr = ET.SubElement(p, q(W, "pPr"))
                ET.SubElement(ppr, q(W, "spacing")).attrib.update({q(W, "after"): "20", q(W, "line"): "220"})
                self.inline(p, value)
                for run in p.findall(f".//{q(W, 'r')}"):
                    rpr = run.find(q(W, "rPr"))
                    if rpr is None:
                        rpr = ET.SubElement(run, q(W, "rPr"))
                    ET.SubElement(rpr, q(W, "sz")).set(q(W, "val"), "16" if wide else "18")
                    if index == 0:
                        ET.SubElement(rpr, q(W, "b"))
        self.table_count += 1
        if wide:
            self.section_break("landscape")

    def section_break(self, preceding_orientation):
        p = ET.SubElement(self.body, q(W, "p"))
        ppr = ET.SubElement(p, q(W, "pPr"))
        section = ET.SubElement(ppr, q(W, "sectPr"))
        ET.SubElement(section, q(W, "type")).set(q(W, "val"), "nextPage")
        if preceding_orientation == "landscape":
            ET.SubElement(section, q(W, "pgSz")).attrib.update({q(W, "w"): "15840", q(W, "h"): "12240", q(W, "orient"): "landscape"})
            ET.SubElement(section, q(W, "pgMar")).attrib.update({q(W, "top"): "600", q(W, "right"): "600", q(W, "bottom"): "600", q(W, "left"): "600"})
        else:
            ET.SubElement(section, q(W, "pgSz")).attrib.update({q(W, "w"): "12240", q(W, "h"): "15840"})
            ET.SubElement(section, q(W, "pgMar")).attrib.update({q(W, "top"): "720", q(W, "right"): "900", q(W, "bottom"): "720", q(W, "left"): "900"})

    def parse(self, markdown):
        lines = markdown.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if not line.strip() or line.strip() in ("---", "***", "___"):
                i += 1
                continue
            if line.startswith("~~~"):
                i += 1
                block = []
                while i < len(lines) and not lines[i].startswith("~~~"):
                    block.append(lines[i])
                    i += 1
                self.para("\n".join(block), "CodeBlock")
                i += 1
                continue
            heading = re.match(r"^(#{1,6})\s+(.+)$", line)
            if heading:
                level = len(heading.group(1))
                self.para(heading.group(2), "Title" if level == 1 else f"Heading{min(level - 1, 3)}")
                i += 1
                continue
            if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?[\s:|-]+\|?$", lines[i + 1]):
                rows = []
                while i < len(lines) and lines[i].startswith("|"):
                    cells = [cell.strip() for cell in lines[i].strip().strip("|").split("|")]
                    if not all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
                        rows.append(cells)
                    i += 1
                if rows:
                    self.table(rows)
                continue
            bullet = re.match(r"^\s*[-*]\s+(.+)$", line)
            numbered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
            if bullet or numbered:
                self.para((bullet or numbered).group(1), kind="bullet" if bullet else "number")
                i += 1
                continue
            img = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", line)
            if img:
                self.image(img.group(2), img.group(1))
                i += 1
                continue
            parts = [line.strip()]
            i += 1
            while i < len(lines) and lines[i].strip():
                nxt = lines[i]
                if nxt.startswith(("#", "|", "~~~", "![")) or re.match(r"^\s*[-*]\s+|^\s*\d+[.)]\s+", nxt):
                    break
                parts.append(nxt.strip())
                i += 1
            self.para(" ".join(parts))

    def save(self):
        sec = ET.SubElement(self.body, q(W, "sectPr"))
        ET.SubElement(sec, q(W, "pgSz")).attrib.update({q(W, "w"): "12240", q(W, "h"): "15840"})
        ET.SubElement(sec, q(W, "pgMar")).attrib.update({q(W, "top"): "720", q(W, "right"): "900", q(W, "bottom"): "720", q(W, "left"): "900", q(W, "header"): "360", q(W, "footer"): "360"})
        rels = ET.Element(q(REL, "Relationships"))
        sr = ET.SubElement(rels, q(REL, "Relationship"))
        sr.attrib.update({"Id": "rId1", "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles", "Target": "styles.xml"})
        for rid, typ, target, mode in self.rels:
            attrs = {"Id": rid, "Type": typ, "Target": target}
            if mode:
                attrs["TargetMode"] = mode
            ET.SubElement(rels, q(REL, "Relationship")).attrib.update(attrs)
        types = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="{CT}">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''
        rootrels = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{REL}"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'''
        OUTDIR.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", types)
            z.writestr("_rels/.rels", rootrels)
            z.writestr("word/document.xml", xml(self.doc))
            z.writestr("word/_rels/document.xml.rels", xml(rels))
            z.writestr("word/styles.xml", xml(styles()))
            z.writestr("word/numbering.xml", xml(numbering()))
            for name, data in self.media:
                z.writestr("word/media/" + name, data)

def styles():
    root = ET.Element(q(W, "styles"))
    default = ET.SubElement(root, q(W, "style"))
    default.attrib.update({"{"+W+"}type": "paragraph", "{"+W+"}default": "1", "{"+W+"}styleId": "Normal"})
    ET.SubElement(default, q(W, "name")).set(q(W, "val"), "Normal")
    rpr = ET.SubElement(default, q(W, "rPr"))
    ET.SubElement(rpr, q(W, "sz")).set(q(W, "val"), "21")
    for sid, name, size, color in (("Title","Title","36","17365D"),("Heading1","Heading 1","30","17365D"),("Heading2","Heading 2","25","2F75B5"),("Heading3","Heading 3","22","365F91"),("Caption","Caption","18","595959"),("CodeBlock","Code Block","18","333333")):
        s = ET.SubElement(root, q(W, "style"))
        s.attrib.update({"{"+W+"}type": "paragraph", "{"+W+"}styleId": sid})
        ET.SubElement(s, q(W, "name")).set(q(W, "val"), name)
        p = ET.SubElement(s, q(W, "rPr"))
        ET.SubElement(p, q(W, "color")).set(q(W, "val"), color)
        ET.SubElement(p, q(W, "sz")).set(q(W, "val"), size)
        if sid != "Caption":
            ET.SubElement(p, q(W, "b"))
        if sid == "CodeBlock":
            f = ET.SubElement(p, q(W, "rFonts"))
            f.set(q(W, "ascii"), "Consolas")
            f.set(q(W, "hAnsi"), "Consolas")
    return root

def numbering():
    root = ET.Element(q(W, "numbering"))
    for aid, fmt, text in ((0, "bullet", "•"), (1, "decimal", "%1.")):
        a = ET.SubElement(root, q(W, "abstractNum"))
        a.set(q(W, "abstractNumId"), str(aid))
        level = ET.SubElement(a, q(W, "lvl"))
        level.set(q(W, "ilvl"), "0")
        ET.SubElement(level, q(W, "start")).set(q(W, "val"), "1")
        ET.SubElement(level, q(W, "numFmt")).set(q(W, "val"), fmt)
        ET.SubElement(level, q(W, "lvlText")).set(q(W, "val"), text)
    for nid, aid in ((1, 0), (2, 1)):
        n = ET.SubElement(root, q(W, "num"))
        n.set(q(W, "numId"), str(nid))
        ET.SubElement(n, q(W, "abstractNumId")).set(q(W, "val"), str(aid))
    return root

def main():
    if not SOURCE.is_file():
        raise FileNotFoundError(f"Report source not found: {SOURCE}")
    render = Renderer()
    render.parse(SOURCE.read_text(encoding="utf-8"))
    if render.paragraph_count < 20 or render.table_count == 0:
        raise RuntimeError("Report parsing produced too little content.")
    render.save()
    with zipfile.ZipFile(OUTPUT) as z:
        ET.fromstring(z.read("word/document.xml"))
        if len([n for n in z.namelist() if n.startswith("word/media/")]) != render.image_no:
            raise RuntimeError("Not all report figures were embedded.")
    print(f"Created: {OUTPUT}")
    print(f"Paragraphs: {render.paragraph_count}; tables: {render.table_count}; embedded figures: {render.image_no}")
    print(f"Size: {OUTPUT.stat().st_size:,} bytes")

if __name__ == "__main__":
    main()

