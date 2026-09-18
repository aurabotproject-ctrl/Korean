#!/usr/bin/env python3
"""
Builds one printable practice sheet (PDF) per stage of 한글 Quest.

Each sheet has:
  • a title block with name/date lines
  • a letter section: model letter, stroke-order numbers, ghost letters to trace, empty boxes
  • a word section: each word written once as a model, once as a ghost, then blank boxes
  • the picture clue beside each letter, so the paper matches the app

Run:  python3 tools/make_printables.py
Out:  assets/printables/stage-1.pdf … stage-9.pdf
"""
import json, os, math
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import Color, HexColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open('/tmp/claude-0/hq.json'))
OUT = os.path.join(ROOT, 'assets', 'printables')
os.makedirs(OUT, exist_ok=True)

# ---- fonts -----------------------------------------------------------------
# Noto Sans CJK ships as OpenType/CFF, which reportlab can't embed, so the fonts are
# subset to the characters this app uses and converted to TrueType by tools/make_fonts.py.
TMP = '/tmp/claude-0/fonts'
pdfmetrics.registerFont(TTFont('KO', os.path.join(TMP, 'ko-regular.ttf')))
pdfmetrics.registerFont(TTFont('KO-B', os.path.join(TMP, 'ko-bold.ttf')))

INK   = HexColor('#2A2238')
MUTED = HexColor('#6C6480')
LINE  = HexColor('#D9D2E6')
GHOST = Color(0.72, 0.70, 0.78)
CON   = HexColor('#E0483D')
VOW   = HexColor('#2A74CF')
FIN   = HexColor('#E9A21B')
SOFT  = HexColor('#F6F2FA')

W, H = A4
M = 34                      # page margin
BOX = 38                    # writing square
GAP = 5
LABEL = 104                 # width of the left-hand label column

def letter_colour(ch):
    d = DATA['letters'].get(ch)
    if not d: return FIN
    return VOW if d['type'] == 'vow' else CON

# ---- drawing helpers -------------------------------------------------------
def box(c, x, y, size=BOX, cross=True):
    """One writing square with faint centre guides, like Korean squared paper."""
    c.setStrokeColor(LINE); c.setLineWidth(0.8)
    c.rect(x, y, size, size, stroke=1, fill=0)
    if cross:
        c.setStrokeColor(HexColor('#EDE8F3')); c.setLineWidth(0.6)
        c.setDash(1.5, 2.5)
        c.line(x + size / 2, y + 3, x + size / 2, y + size - 3)
        c.line(x + 3, y + size / 2, x + size - 3, y + size / 2)
        c.setDash()

def glyph(c, ch, x, y, size, colour, font='KO'):
    """Draw one Korean character centred in a square."""
    fs = size * 0.78
    c.setFont(font, fs); c.setFillColor(colour)
    w = pdfmetrics.stringWidth(ch, font, fs)
    c.drawString(x + (size - w) / 2, y + size * 0.24, ch)

def stroke_numbers(c, ch, x, y, size):
    """Little numbered dots showing where each stroke starts (same data as the app)."""
    d = DATA['letters'].get(ch)
    if not d: return
    for i, s in enumerate(d['strokes']):
        sx, sy = s[0]
        px = x + (sx / 100) * size
        py = y + size - (sy / 100) * size
        c.setFillColor(letter_colour(ch)); c.circle(px, py, 5.2, stroke=0, fill=1)
        c.setFillColor(HexColor('#FFFFFF')); c.setFont('Helvetica-Bold', 6.5)
        c.drawCentredString(px, py - 2.3, str(i + 1))

_thumbs = {}
def thumb(img):
    """Small flattened copy of a picture clue, so the PDFs stay light and print cleanly."""
    if img in _thumbs: return _thumbs[img]
    from PIL import Image
    for ext in ('webp', 'png'):
        p = os.path.join(ROOT, 'assets', 'mnemonics', f'{img}.{ext}')
        if os.path.exists(p):
            im = Image.open(p).convert('RGBA')
            im.thumbnail((150, 150), Image.LANCZOS)
            flat = Image.new('RGB', im.size, (255, 255, 255))
            flat.paste(im, (0, 0), im)
            out = f'/tmp/claude-0/thumbs/{img}.png'
            os.makedirs('/tmp/claude-0/thumbs', exist_ok=True)
            flat.save(out, optimize=True)
            _thumbs[img] = out
            return out
    _thumbs[img] = None
    return None

def picture(c, ch, x, y, size):
    d = DATA['letters'].get(ch)
    if not d: return False
    p = thumb(d['img'])
    if not p: return False
    try:
        c.drawImage(ImageReader(p), x, y, size, size, mask='auto',
                    preserveAspectRatio=True, anchor='c')
        return True
    except Exception:
        return False

def header(c, stage, page, pages):
    c.setFillColor(INK); c.setFont('Helvetica-Bold', 17)
    c.drawString(M, H - M - 6, f"Hangul Quest — Stage {stage['id']}")
    c.setFont('KO-B', 15); c.setFillColor(letter_colour(stage['letters'][0]) if stage['letters'] else FIN)
    c.drawRightString(W - M, H - M - 6, ' '.join(stage['letters']) if stage['letters'] else stage['ko'])
    c.setFont('Helvetica', 10.5); c.setFillColor(MUTED)
    c.drawString(M, H - M - 22, stage['title'])
    c.setStrokeColor(LINE); c.setLineWidth(1); c.line(M, H - M - 30, W - M, H - M - 30)
    c.setFont('Helvetica', 9); c.setFillColor(MUTED)
    c.drawString(M, H - M - 44, 'Name: ______________________       Date: ______________')
    c.drawRightString(W - M, H - M - 44, f'Page {page} of {pages}')
    c.setFont('Helvetica-Oblique', 8.6)
    c.drawString(M, M - 14, 'Say each sound out loud as you write it. Trace the grey ones first, then write your own.')
    c.setFont('Helvetica-Oblique', 8.6)
    c.drawRightString(W - M, M - 14, ' Quest')
    c.setFont('KO', 8.6)
    c.drawRightString(W - M - pdfmetrics.stringWidth(' Quest', 'Helvetica-Oblique', 8.6), M - 14, '한글')

def section(c, y, title, sub=''):
    c.setFillColor(INK)
    if '(' in title and any('\uac00' <= ch <= '\ud7a3' for ch in title):   # e.g. "Bottom letters (받침)"
        latin, ko = title.split('(')[0], title.split('(')[1].rstrip(')')
        c.setFont('Helvetica-Bold', 11.5); c.drawString(M, y, latin + '(')
        wdt = pdfmetrics.stringWidth(latin + '(', 'Helvetica-Bold', 11.5)
        c.setFont('KO-B', 11.5); c.drawString(M + wdt, y, ko)
        c.setFont('Helvetica-Bold', 11.5); c.drawString(M + wdt + pdfmetrics.stringWidth(ko, 'KO-B', 11.5), y, ')')
        title = latin + '(' + ko + ')'
    else:
        c.setFont('Helvetica-Bold', 11.5); c.drawString(M, y, title)
    if sub:
        c.setFont('Helvetica', 9); c.setFillColor(MUTED)
        c.drawString(M + pdfmetrics.stringWidth(title, 'Helvetica-Bold', 11.5) + 8, y, sub)
    return y - 12

# ---- page content ----------------------------------------------------------
def letter_row(c, ch, y):
    """Picture + model + stroke order, then 3 ghosts and the rest blank."""
    d = DATA['letters'][ch]
    col = letter_colour(ch)
    top = y - BOX
    if picture(c, ch, M, top - 2, BOX + 4):
        pass
    else:
        c.setFillColor(SOFT); c.rect(M, top, BOX, BOX, stroke=0, fill=1)
    lx = M + BOX + 10
    c.setFillColor(col); c.setFont('KO-B', 13)
    c.drawString(lx, top + BOX - 13, ch)
    c.setFillColor(INK); c.setFont('Helvetica-Bold', 9.5)
    c.drawString(lx + 15, top + BOX - 12, f"“{d['rom']}”")
    c.setFillColor(MUTED); c.setFont('Helvetica', 7.6)
    c.drawString(lx, top + BOX - 24, 'name')
    c.setFont('KO', 8.6)
    c.drawString(lx + 21, top + BOX - 24, d['name'])
    x = M + LABEL
    n = int((W - M - x) // (BOX + GAP))
    for i in range(n):
        box(c, x, top)
        if i == 0:
            glyph(c, ch, x, top, BOX, col); stroke_numbers(c, ch, x, top, BOX)
        elif i < 4:
            glyph(c, ch, x, top, BOX, GHOST)
        x += BOX + GAP
    return top - 14

def word_rows(c, w, y):
    """One line per word: model, ghost, then blanks."""
    ko = w['ko']; n = len(ko)
    top = y - BOX
    c.setFillColor(INK); c.setFont('KO-B', 13)
    c.drawString(M, top + BOX - 14, ko)
    c.setFillColor(MUTED); c.setFont('Helvetica', 8)
    c.drawString(M, top + BOX - 26, w['rom'][:16])
    c.setFont('Helvetica-Oblique', 7.6)
    c.drawString(M, top + BOX - 35, w['en'][:20])
    x = M + LABEL
    per = n * BOX + GAP * (n - 1)
    slots = max(1, int((W - M - x + 10) // (per + 14)))
    for s in range(slots):
        for i, ch in enumerate(ko):
            bx = x + i * (BOX + GAP)
            box(c, bx, top)
            if s == 0:
                glyph(c, ch, bx, top, BOX, INK, 'KO-B')
            elif s == 1:
                glyph(c, ch, bx, top, BOX, GHOST)
        x += per + 14
    return top - 14

def build(stage):
    sid = stage['id']
    path = os.path.join(OUT, f'stage-{sid}.pdf')
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle(f"Hangul Quest — Stage {sid} practice sheet")
    letters = [l for l in stage['letters'] if l in DATA['letters']]
    words = [w for w in DATA['words'] if w['stage'] == sid]
    # page 1 = letters (+ words that fit), then word pages
    pages = 1 + max(0, math.ceil(max(0, len(words) - 6) / 13))
    page = 1
    header(c, stage, page, pages)
    y = H - M - 62
    if letters:
        y = section(c, y, 'Letters', '— trace the grey ones, then write your own')
        for ch in letters:
            if y < M + 70:
                c.showPage(); page += 1; header(c, stage, page, pages); y = H - M - 62
            y = letter_row(c, ch, y)
        y -= 6
    if stage.get('kind') == 'finals':
        y = section(c, y, 'Bottom letters (받침)', '— the 7 ending sounds')
        c.setFont('KO-B', 20); c.setFillColor(FIN)
        c.drawString(M, y - 20, '  '.join(f['f'] for f in DATA['finals']))
        c.setFillColor(MUTED); fx = M
        for f in DATA['finals']:
            c.setFont('KO', 10); c.drawString(fx, y - 34, f['f'])
            fx += 13
            c.setFont('Helvetica', 9); lbl = f"= “{f['rom']}”"
            c.drawString(fx, y - 34, lbl)
            fx += pdfmetrics.stringWidth(lbl, 'Helvetica', 9) + 14
        y -= 48
    if words:
        y = section(c, y, 'Words', '— write each word until the line is full')
        for w in words:
            if y < M + 70:
                c.showPage(); page += 1; header(c, stage, page, pages); y = H - M - 62
                y = section(c, y, 'Words (continued)')
            y = word_rows(c, w, y)
    c.showPage()
    c.save()
    return path, pages

if __name__ == '__main__':
    for stage in DATA['stages']:
        p, pages = build(stage)
        print(f"stage {stage['id']}: {os.path.basename(p)}  ({os.path.getsize(p)//1024} KB)")
