#!/usr/bin/env python3
"""
Assembles every practice sheet into one printable booklet.

  cover  →  contents  →  Part 1: the nine Hangul Path sheets
         →  Part 2: Level 2 unit sheets (as units are built)
         →  back page: the "Can I…?" confidence checklist

Run:  python3 tools/make_booklet.py     (after make_printables.py)
Out:  assets/printables/booklet.pdf
"""
import os, io, json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
import pikepdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'printables')
DATA = json.load(open('/tmp/claude-0/hq.json'))
L2 = json.load(open('/tmp/claude-0/hq-l2.json')) if os.path.exists('/tmp/claude-0/hq-l2.json') else {'units': []}

TMP = '/tmp/claude-0/fonts'
pdfmetrics.registerFont(TTFont('KO', os.path.join(TMP, 'ko-regular.ttf')))
pdfmetrics.registerFont(TTFont('KO-B', os.path.join(TMP, 'ko-bold.ttf')))

W, H = A4
M = 40
INK = HexColor('#1A1030')
MUTED = HexColor('#6A5A86')
LINE = HexColor('#D5C7EA')
PLUM = HexColor('#7B2CBF')
CON = HexColor('#E8175D')

CAN_DO = [
    'I can say hello to a friend and to a grown-up',
    'I can read any Korean word, out loud',
    'I can write all 40 letters from memory',
    'I can give my name, my age and where I am from',
    'I can name everyone in my family',
    'I can order food and ask what something costs',
    'I can ask where something is, and understand the answer',
    'I can ask a Korean child to play with me',
    'I can say what I did yesterday',
    'I can say what I am going to do tomorrow',
    'I can ask for help if I am lost',
]


def cover(c):
    art = os.path.join(OUT, 'booklet-cover.webp')
    if os.path.exists(art):
        # embed the cover as a JPEG: a lossless copy triples the size of the whole booklet
        from PIL import Image
        jpg = '/tmp/claude-0/booklet-cover.jpg'
        if not os.path.exists(jpg):
            Image.open(art).convert('RGB').save(jpg, 'JPEG', quality=82, optimize=True)
        c.drawImage(ImageReader(jpg), 0, 0, W, H, mask=None)
        # the artwork leaves a banner at the top and another at the foot for these
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 40)
        c.drawCentredString(W / 2, H - 104, 'Practice Booklet')
        # the KO font carries only the Korean subset, so the Latin half needs Helvetica
        ko, latin = '한글', ' Quest'
        wk = pdfmetrics.stringWidth(ko, 'KO-B', 34)
        wl = pdfmetrics.stringWidth(latin, 'Helvetica-Bold', 34)
        x = (W - wk - wl) / 2
        c.setFillColor(CON); c.setFont('KO-B', 34); c.drawString(x, H - 152, ko)
        c.setFont('Helvetica-Bold', 34); c.drawString(x + wk, H - 152, latin)
        c.setFillColor(INK); c.setFont('Helvetica', 13)
        c.drawCentredString(W / 2, 128, 'Name: ______________________________')
        c.setFont('Helvetica', 11); c.setFillColor(MUTED)
        c.drawCentredString(W / 2, 106, 'Letters · Words · Conversations')
    else:
        c.setFont('Helvetica-Bold', 40); c.setFillColor(INK)
        c.drawCentredString(W / 2, H / 2, 'Hangul Quest — Practice Booklet')
    c.showPage()


def contents(c, rows):
    c.setFillColor(INK); c.setFont('Helvetica-Bold', 26)
    c.drawString(M, H - M - 18, 'Contents')
    c.setStrokeColor(LINE); c.setLineWidth(1); c.line(M, H - M - 32, W - M, H - M - 32)
    y = H - M - 62
    for title, sub, page in rows:
        if title.startswith('PART'):
            y -= 8
            c.setFont('Helvetica-Bold', 12); c.setFillColor(PLUM)
            c.drawString(M, y, title.replace('PART ', 'Part '))
            y -= 18
            continue
        c.setFont('Helvetica-Bold', 11.5); c.setFillColor(INK)
        c.drawString(M + 10, y, title)
        wdt = pdfmetrics.stringWidth(title, 'Helvetica-Bold', 11.5)
        if sub:
            c.setFont('Helvetica', 10); c.setFillColor(MUTED)
            c.drawString(M + 16 + wdt, y, sub)
        c.setFillColor(MUTED); c.setFont('Helvetica', 10)
        c.drawRightString(W - M, y, str(page))
        c.setStrokeColor(LINE); c.setLineWidth(.4); c.setDash(1, 3)
        c.line(M + 24 + wdt + (pdfmetrics.stringWidth(sub or '', 'Helvetica', 10)), y + 3,
               W - M - 18, y + 3)
        c.setDash()
        y -= 19
        if y < M + 60:
            c.showPage(); y = H - M - 40
    c.showPage()


def back_page(c):
    c.setFillColor(INK); c.setFont('Helvetica-Bold', 26)
    c.drawString(M, H - M - 18, 'Can I…?')
    c.setFont('Helvetica', 11); c.setFillColor(MUTED)
    c.drawString(M, H - M - 38, 'Tick each one the day you do it for real — with a real person, out loud.')
    c.setStrokeColor(LINE); c.setLineWidth(1); c.line(M, H - M - 50, W - M, H - M - 50)
    y = H - M - 92
    for item in CAN_DO:
        c.setStrokeColor(LINE); c.setLineWidth(1.4)
        c.rect(M, y - 4, 18, 18, stroke=1, fill=0)
        c.setFillColor(INK); c.setFont('Helvetica-Bold', 12)
        c.drawString(M + 30, y, item)
        c.setFillColor(MUTED); c.setFont('Helvetica', 9)
        c.drawRightString(W - M, y, 'date: ____________')
        y -= 34
    c.setFillColor(MUTED); c.setFont('Helvetica-Oblique', 10)
    c.drawCentredString(W / 2, M + 30, 'Every one of these is a real conversation you can have in Korea.')
    ko, latin = '화이팅!', ' You can do it!'
    wk = pdfmetrics.stringWidth(ko, 'KO-B', 11)
    wl = pdfmetrics.stringWidth(latin, 'Helvetica-Bold', 11)
    x = (W - wk - wl) / 2
    c.setFillColor(CON); c.setFont('KO-B', 11); c.drawString(x, M + 12, ko)
    c.setFont('Helvetica-Bold', 11); c.drawString(x + wk, M + 12, latin)
    c.showPage()


def pages_in(path):
    with pikepdf.open(path) as p:
        return len(p.pages)


def build():
    parts = []                                    # (label, sub, pdf path, page count)
    for st in DATA['stages']:
        p = os.path.join(OUT, f"stage-{st['id']}.pdf")
        if os.path.exists(p):
            parts.append(('l1', f"Stage {st['id']}", st['title'], p, pages_in(p)))
    for u in L2['units']:
        p = os.path.join(OUT, f"unit-{u['id']}.pdf")
        if os.path.exists(p):
            parts.append(('l2', f"Unit {u['id']}", u['title'], p, pages_in(p)))

    # page numbers: cover(1) + contents(n) come first, so work out the contents length first
    rows_n = len(parts) + 2 + (1 if any(k == 'l2' for k, *_ in parts) else 0)
    contents_pages = 1 if rows_n <= 32 else 2
    page = 1 + contents_pages + 1               # cover + contents, 1-indexed for the first sheet
    rows = [('PART 1 — Hangul Path: letters and words', '', '')]
    for kind, label, title, path, n in parts:
        if kind == 'l2' and rows[-1][0] != 'PART 2 — Talking with friends and family':
            rows.append(('PART 2 — Talking with friends and family', '', ''))
        rows.append((label, '· ' + title, page))
        page += n
    rows.append(('PART 3 — Check yourself', '', ''))
    rows.append(('Can I…? checklist', '', page))

    front = io.BytesIO()
    c = canvas.Canvas(front, pagesize=A4)
    c.setTitle('한글 Quest — Practice Booklet')
    cover(c)
    contents(c, rows)
    c.save()

    back = io.BytesIO()
    c2 = canvas.Canvas(back, pagesize=A4)
    back_page(c2)
    c2.save()

    out = pikepdf.Pdf.new()
    front.seek(0); back.seek(0)
    with pikepdf.open(front) as f:
        out.pages.extend(f.pages)
    for _, _, _, path, _ in parts:
        with pikepdf.open(path) as src:
            out.pages.extend(src.pages)
    with pikepdf.open(back) as b:
        out.pages.extend(b.pages)
    with out.open_metadata() as meta:
        meta['dc:title'] = 'Hangul Quest — Practice Booklet'
    dest = os.path.join(OUT, 'booklet.pdf')
    out.save(dest)
    print(f"booklet.pdf — {len(out.pages)} pages, {os.path.getsize(dest)//1024} KB")


if __name__ == '__main__':
    build()
