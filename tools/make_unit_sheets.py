#!/usr/bin/env python3
"""
Builds one printable pack per Level 2 unit: assets/printables/unit-1.pdf, unit-2.pdf …

Each pack is:
  • vocabulary sheets — every word in the unit, model → trace → copy, grouped by set
  • two dialogue worksheets, two pages each:
        A "Read it"  — the conversation with gaps, a word bank, matching, new words to trace
        B "Use it"   — your own true answers, a 반말/존댓말 rewrite, cut-out role-play cards
  • an answer key, so a grown-up can mark it without reading Korean

Run:  python3 tools/make_unit_sheets.py     (needs /tmp/claude-0/hq-l2.json and the fonts)
"""
import json, os, textwrap
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import Color, HexColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'printables')
os.makedirs(OUT, exist_ok=True)
L2 = json.load(open('/tmp/claude-0/hq-l2.json'))
CAST = L2['cast']

TMP = '/tmp/claude-0/fonts'
pdfmetrics.registerFont(TTFont('KO', os.path.join(TMP, 'ko-regular.ttf')))
pdfmetrics.registerFont(TTFont('KO-B', os.path.join(TMP, 'ko-bold.ttf')))

W, H = A4
M = 34
INK = HexColor('#1A1030')
MUTED = HexColor('#6A5A86')
LINE = HexColor('#D5C7EA')
GHOST = Color(0.72, 0.70, 0.78)
PLUM = HexColor('#7B2CBF')
CON = HexColor('#E8175D')
VOW = HexColor('#1E7FD6')
GREEN = HexColor('#12A57E')
SOFT = HexColor('#F2ECFA')
BOX = 30
GAP = 4


# ---- small drawing helpers -------------------------------------------------
def ko_width(t, size, bold=False):
    return pdfmetrics.stringWidth(t, 'KO-B' if bold else 'KO', size)


def is_ko(ch):
    # Hangul syllables, jamo, and the ○ the app uses as a "your name here" blank —
    # all of which exist in the Korean font and in none of the Latin ones.
    return ('\uac00' <= ch <= '\ud7a3' or '\u3130' <= ch <= '\u318f'
            or ch in '○△□·…')


def runs(text):
    """Split a string into Korean and non-Korean stretches."""
    out, cur, cur_ko = [], '', None
    for ch in text:
        k = is_ko(ch)
        if cur_ko is None or k == cur_ko:
            cur += ch; cur_ko = k
        else:
            out.append((cur, cur_ko)); cur, cur_ko = ch, k
    if cur:
        out.append((cur, cur_ko))
    return out


def rich(c, x, y, text, size, colour=INK, bold=False, italic=False, max_w=None):
    """Draw text that may mix English and Hangul. Helvetica has no Hangul, and the
       subset Korean font has no Latin, so each stretch needs its own font."""
    latin = 'Helvetica-Bold' if bold else ('Helvetica-Oblique' if italic else 'Helvetica')
    korean = 'KO-B' if bold else 'KO'
    c.setFillColor(colour)
    for chunk, ko in runs(text):
        font = korean if ko else latin
        w = pdfmetrics.stringWidth(chunk, font, size)
        if max_w is not None and (x + w) > max_w:
            # trim the run to fit rather than spilling into the next column
            while chunk and pdfmetrics.stringWidth(chunk + '…', font, size) > (max_w - x):
                chunk = chunk[:-1]
            if not chunk:
                return x
            chunk += '…'
            w = pdfmetrics.stringWidth(chunk, font, size)
        c.setFont(font, size)
        c.drawString(x, y, chunk)
        x += w
    return x


def rich_w(text, size, bold=False, italic=False):
    latin = 'Helvetica-Bold' if bold else ('Helvetica-Oblique' if italic else 'Helvetica')
    korean = 'KO-B' if bold else 'KO'
    return sum(pdfmetrics.stringWidth(ch, korean if ko else latin, size) for ch, ko in runs(text))


def wrap_en(c, x, y, text, width, size=9.5, leading=12, colour=MUTED, font='Helvetica'):
    chars = max(10, int(width / (size * 0.5)))
    for ln in textwrap.wrap(text, chars):
        rich(c, x, y, ln, size, colour, italic=(font == 'Helvetica-Oblique'))
        y -= leading
    return y


def box(c, x, y, size=BOX, cross=True):
    c.setStrokeColor(LINE); c.setLineWidth(0.8)
    c.rect(x, y, size, size, stroke=1, fill=0)
    if cross:
        c.setStrokeColor(HexColor('#EFE9F8')); c.setLineWidth(0.6); c.setDash(1.5, 2.5)
        c.line(x + size / 2, y + 3, x + size / 2, y + size - 3)
        c.line(x + 3, y + size / 2, x + size - 3, y + size / 2)
        c.setDash()


def glyph(c, ch, x, y, size, colour, bold=True):
    fs = size * 0.76
    font = 'KO-B' if bold else 'KO'
    c.setFont(font, fs); c.setFillColor(colour)
    c.drawString(x + (size - pdfmetrics.stringWidth(ch, font, fs)) / 2, y + size * 0.24, ch)


def writing_row(c, word, x, y, size=BOX, models=1, ghosts=1):
    """The word written once in ink, once in grey, then empty squares to the margin."""
    n = len(word)
    i = 0
    slots = int((W - M - x + GAP) // ((size + GAP) * n + 12))
    for s in range(max(1, slots)):
        for k, ch in enumerate(word):
            bx = x + s * ((size + GAP) * n + 12) + k * (size + GAP)
            if bx + size > W - M:
                return
            box(c, bx, y, size)
            if s < models:
                glyph(c, ch, bx, y, size, INK)
            elif s < models + ghosts:
                glyph(c, ch, bx, y, size, GHOST)


def header(c, unit, title, page_label):
    rich(c, M, H - M - 6, f"Unit {unit['id']} — {title}", 16, INK, bold=True)
    c.setFont('KO-B', 14); c.setFillColor(CON)
    c.drawRightString(W - M, H - M - 6, unit['ko'])
    c.setFont('Helvetica', 10); c.setFillColor(MUTED)
    c.drawString(M, H - M - 21, page_label)
    c.setStrokeColor(LINE); c.setLineWidth(1); c.line(M, H - M - 29, W - M, H - M - 29)
    c.setFont('Helvetica', 9); c.setFillColor(MUTED)
    c.drawString(M, H - M - 43, 'Name: ______________________       Date: ______________')
    c.setFont('Helvetica-Oblique', 8.4); c.setFillColor(MUTED)
    c.drawString(M, M - 16, 'Say every Korean line out loud as you write it.')
    c.setFont('Helvetica-Oblique', 8.4)
    c.drawRightString(W - M, M - 16, ' Quest · Level 2')
    c.setFont('KO', 8.4)
    c.drawRightString(W - M - pdfmetrics.stringWidth(' Quest · Level 2', 'Helvetica-Oblique', 8.4), M - 16, '한글')


def section(c, y, title, sub=''):
    c.setFillColor(PLUM); c.setFont('Helvetica-Bold', 11.5)
    c.drawString(M, y, title)
    if sub:
        c.setFont('Helvetica', 9); c.setFillColor(MUTED)
        c.drawString(M + pdfmetrics.stringWidth(title, 'Helvetica-Bold', 11.5) + 8, y, sub)
    return y - 14


# ---- vocabulary sheets -----------------------------------------------------
ROW_H = 46          # one word: Korean + romanisation + meaning, then a row of squares
HEAD_H = 20


def vocab_pages(c, unit):
    """Every word in the unit, two columns to a page: trace the grey copy, then write your own."""
    col_w = (W - 2 * M - 20) / 2
    top = H - M - 62
    bottom = M + 6
    page = [1]
    col = [0]
    y = [top]

    def new_page():
        c.showPage(); page[0] += 1
        header(c, unit, 'Words', f"Vocabulary sheet {page[0]} — trace the grey word, then write your own")
        col[0] = 0; y[0] = top

    def x_now():
        return M + col[0] * (col_w + 20)

    def room(h):
        """Make sure h points of space exist in the current column, moving on if not."""
        if y[0] - h >= bottom:
            return
        if col[0] == 0:
            col[0] = 1; y[0] = top
        else:
            new_page()

    header(c, unit, 'Words', 'Vocabulary sheet 1 — trace the grey word, then write your own')
    for st in unit['sets']:
        room(HEAD_H + ROW_H)                       # never strand a heading at the foot
        x = x_now()
        c.setFillColor(PLUM); c.setFont('Helvetica-Bold', 10.5)
        c.drawString(x, y[0], st['title'])
        c.setFillColor(MUTED); c.setFont('Helvetica', 8)
        c.drawString(x + pdfmetrics.stringWidth(st['title'], 'Helvetica-Bold', 10.5) + 6, y[0], f"set {st['id']}")
        y[0] -= HEAD_H
        for w in st['words']:
            room(ROW_H)
            x = x_now(); right = x + col_w
            ko = w['ko']
            c.setFont('KO-B', 13); c.setFillColor(INK)
            c.drawString(x, y[0], ko)
            rich(c, x + ko_width(ko, 13, True) + 8, y[0] + 1, w['rom'], 7.4, MUTED, max_w=right)
            rich(c, x, y[0] - 10, w['en'], 7.6, MUTED, italic=True, max_w=right)
            letters = [ch for ch in ko if ch != ' ']
            sz = 20 if len(letters) <= 5 else 15
            bx, yb = x, y[0] - 32
            for ch in letters:
                if bx + sz > right:
                    break
                box(c, bx, yb, sz); glyph(c, ch, bx, yb, sz, GHOST)
                bx += sz + 3
            bx += 8
            while bx + sz <= right:
                box(c, bx, yb, sz)
                bx += sz + 3
            y[0] -= ROW_H
    c.showPage()


# ---- dialogue worksheets ---------------------------------------------------
def script_lines(d):
    """The conversation as it is spoken, alternating between them and the child."""
    out = []
    lead = d['with'][0]
    for t in d['turns']:
        if t.get('ko'):
            out.append((CAST[t['who']]['name'], t['ko'], t['rom'], t['en'], False))
        q = t.get('q') or {}
        if q.get('kind') == 'say':
            out.append(('You', q['ko'], q['rom'], q['en'], True))
        elif q.get('kind') == 'listen':
            if not t.get('ko'):
                ok = next((o for o in q['options'] if o.get('ok')), {})
                out.append((CAST[t.get('who') or lead]['name'], q['ko'], q['rom'], ok.get('en', ''), False))
        else:
            ok = next((o for o in q.get('options', []) if o.get('ok')), None)
            if ok and ok.get('ko'):
                out.append(('You', ok['ko'], ok['rom'], ok['en'], True))
    return out


def scene_thumb(scene):
    src = os.path.join(ROOT, 'assets', 'scenes', f'{scene}.webp')
    if not os.path.exists(src):
        return None
    out = f'/tmp/claude-0/thumbs/scene-{scene}.jpg'
    os.makedirs('/tmp/claude-0/thumbs', exist_ok=True)
    if not os.path.exists(out):
        from PIL import Image
        im = Image.open(src).convert('RGB')
        im.thumbnail((420, 420), Image.LANCZOS)
        im.save(out, 'JPEG', quality=76, optimize=True)
    return out


def dialogue_page_a(c, unit, d, gaps):
    talk = '반말 (to a friend)' if d['talk'] == 'banmal' else '존댓말 (polite)'
    header(c, unit, d['title'], 'Worksheet A — read it')
    y = H - M - 62
    th = scene_thumb(d['scene'])
    if th:
        c.drawImage(ImageReader(th), W - M - 150, y - 76, 150, 84, mask=None,
                    preserveAspectRatio=True, anchor='ne')
    c.setFillColor(MUTED); c.setFont('Helvetica', 9)
    c.drawString(M, y, 'You are speaking ')
    wdt = pdfmetrics.stringWidth('You are speaking ', 'Helvetica', 9)
    ko_part, en_part = talk.split(' ', 1)
    c.setFont('KO-B', 9.5); c.setFillColor(CON); c.drawString(M + wdt, y, ko_part)
    wdt += ko_width(ko_part, 9.5, True)
    c.setFont('Helvetica', 9); c.setFillColor(MUTED); c.drawString(M + wdt + 3, y, en_part)
    y -= 12
    y = wrap_en(c, M, y, d['intro'], W - 2 * M - 170, 9.5, 12)
    y -= 6

    y = section(c, y, '1. The conversation', '— fill each gap from the word bank')
    lines = script_lines(d)
    for i, (who, ko, rom, en, mine) in enumerate(lines):
        if y < M + 150:
            break
        c.setFillColor(CON if not mine else VOW); c.setFont('KO-B', 8.5)
        label = who if not mine else 'You'
        if mine:
            c.setFont('Helvetica-Bold', 8.5)
        c.drawString(M, y, label)
        x = M + 62
        if i in gaps:
            # blank out the last word of the line, leaving a ruled space
            bits = ko.split(' ')
            head, tail = ' '.join(bits[:-1]), bits[-1]
            if head:
                c.setFont('KO-B', 12); c.setFillColor(INK); c.drawString(x, y, head)
                x += ko_width(head, 12, True) + 5
            c.setStrokeColor(CON); c.setLineWidth(1.1)
            gw = max(54, ko_width(tail, 12, True) + 14)
            c.line(x, y - 2, x + gw, y - 2)
            x += gw + 4
        else:
            c.setFont('KO-B', 12); c.setFillColor(INK); c.drawString(x, y, ko)
            x += ko_width(ko, 12, True) + 6
        rich(c, M + 62, y - 11, en, 8, MUTED, italic=True, max_w=W - M)
        y -= 26

    y -= 2
    bank = [lines[i][1].split(' ')[-1] for i in gaps]
    c.setFillColor(SOFT); c.rect(M, y - 26, W - 2 * M, 30, stroke=0, fill=1)
    c.setFillColor(PLUM); c.setFont('Helvetica-Bold', 9)
    c.drawString(M + 8, y - 8, 'WORD BANK')
    bx = M + 88
    for wrd in sorted(set(bank)):
        c.setFont('KO-B', 12); c.setFillColor(INK)
        c.drawString(bx, y - 10, wrd)
        bx += ko_width(wrd, 12, True) + 20
    y -= 46

    y = section(c, y, '2. Match them up', '— draw a line from the Korean to what it means')
    pairs = [(l[1], l[3]) for l in lines if l[3]][:4]
    shuffled = list(reversed(pairs))
    for i, (ko, _) in enumerate(pairs):
        yy = y - i * 22
        c.setFont('KO-B', 12); c.setFillColor(INK); c.drawString(M + 6, yy, ko[:22])
        c.setFillColor(LINE); c.circle(M + 190, yy + 4, 2.4, stroke=0, fill=1)
    for i, (_, en) in enumerate(shuffled):
        yy = y - i * 22
        c.setFillColor(LINE); c.circle(M + 250, yy + 4, 2.4, stroke=0, fill=1)
        rich(c, M + 262, yy, en, 9.5, INK, max_w=W - M)
    y -= len(pairs) * 22 + 12

    y = section(c, y, '3. New words', '— trace the grey one, then write it yourself')
    words = []
    for t in d['turns']:
        q = t.get('q') or {}
        for o in q.get('options', []):
            if o.get('ok') and o.get('ko'):
                words.append(o['ko'])
        if q.get('kind') == 'say':
            words.append(q['ko'])
    seen, picks = set(), []
    for wd in words:
        wd = wd.strip()
        if wd and wd not in seen:
            seen.add(wd); picks.append(wd)
    for wd in picks[:3]:
        if y < M + 46:
            break
        rich(c, M, y - 16, wd, 12, INK, bold=True, max_w=M + 112)
        letters = [ch for ch in wd if ch not in ' !?.,○']
        bx, sz = M + 120, 24
        for ch in letters[:8]:
            box(c, bx, y - 24, sz); glyph(c, ch, bx, y - 24, sz, GHOST); bx += sz + 3
        bx += 10
        while bx + sz <= W - M:
            box(c, bx, y - 24, sz); bx += sz + 3
        y -= 36
    c.showPage()


def dialogue_page_b(c, unit, d):
    header(c, unit, d['title'], 'Worksheet B — use it')
    y = H - M - 62
    lines = script_lines(d)
    asks = [l for l in lines if not l[4]][:4]

    y = section(c, y, '4. Your turn', '— answer these about yourself, in Korean')
    for who, ko, rom, en, _ in asks:
        c.setFont('KO-B', 12); c.setFillColor(INK); c.drawString(M, y, ko[:34])
        rich(c, M, y - 11, en, 8.4, MUTED, italic=True, max_w=W - M)
        c.setStrokeColor(LINE); c.setLineWidth(0.9)
        c.line(M + 14, y - 30, W - M, y - 30)
        y -= 46

    y -= 4
    other = '존댓말 (polite)' if d['talk'] == 'banmal' else '반말 (to a friend)'
    ko_part, en_part = other.split(' ', 1)
    yy = section(c, y, '5. Say it the other way', '')
    c.setFont('Helvetica', 9); c.setFillColor(MUTED)
    x = M + pdfmetrics.stringWidth('5. Say it the other way', 'Helvetica-Bold', 11.5) + 8
    c.drawString(x, y, '— now rewrite each line in ')
    x += pdfmetrics.stringWidth('— now rewrite each line in ', 'Helvetica', 9)
    c.setFont('KO-B', 9.5); c.setFillColor(CON); c.drawString(x, y, ko_part)
    x += ko_width(ko_part, 9.5, True)
    c.setFont('Helvetica', 9); c.setFillColor(MUTED); c.drawString(x + 3, y, en_part)
    y = yy
    mine = [l for l in lines if l[4]][:3]
    for who, ko, rom, en, _ in mine:
        c.setFont('KO-B', 12); c.setFillColor(VOW); c.drawString(M, y, ko[:34])
        c.setFillColor(MUTED); c.setFont('Helvetica', 11); c.drawString(M + 250, y, '→')
        c.setStrokeColor(LINE); c.setLineWidth(0.9)
        c.line(M + 272, y - 3, W - M, y - 3)
        y -= 32

    y -= 6
    y = section(c, y, '6. Act it out', '— cut along the dotted line and take a card each')
    c.setStrokeColor(MUTED); c.setLineWidth(0.8); c.setDash(3, 3)
    c.line(M, y + 4, W - M, y + 4); c.setDash()
    c.setFont('Helvetica', 7.5); c.setFillColor(MUTED)
    c.drawRightString(W - M, y + 8, '✂')
    y -= 8
    cards = [(CAST[d['with'][0]]['name'], [l for l in lines if not l[4]]),
             ('You', [l for l in lines if l[4]])]
    cw = (W - 2 * M - 14) / 2
    top = y
    card_h = min(190, 34 + 20 * max(len(ls) for _, ls in cards))
    for ci, (name, ls) in enumerate(cards):
        cx = M + ci * (cw + 14)
        ch = card_h
        c.setStrokeColor(LINE); c.setLineWidth(1.2)
        c.roundRect(cx, top - ch, cw, ch, 8, stroke=1, fill=0)
        c.setFillColor(SOFT); c.roundRect(cx, top - 24, cw, 24, 8, stroke=0, fill=1)
        if name == 'You':
            c.setFont('Helvetica-Bold', 10); c.setFillColor(VOW)
            c.drawString(cx + 10, top - 16, 'YOU')
        else:
            c.setFont('KO-B', 11); c.setFillColor(CON)
            c.drawString(cx + 10, top - 16, name)
        yy = top - 40
        for _, ko, rom, en, _m in ls:
            if yy < top - ch + 10:
                break
            c.setFont('KO-B', 10); c.setFillColor(INK)
            c.drawString(cx + 10, yy, ko[:26])
            yy -= 20
    y = top - card_h - 26

    y = section(c, y, '7. Say it to a real person', '— tick each one once you have said it out loud')
    said = [l[1] for l in lines if l[4]][:4]
    for line in said:
        c.setStrokeColor(LINE); c.setLineWidth(1.2)
        c.rect(M, y - 4, 14, 14, stroke=1, fill=0)
        c.setFont('KO-B', 11); c.setFillColor(INK)
        c.drawString(M + 24, y, line[:40])
        y -= 24
    c.showPage()


def answer_key(c, unit, gap_map):
    header(c, unit, 'Answer key', 'For a grown-up — you do not need to read Korean')
    y = H - M - 62
    for d in unit['dialogues']:
        lines = script_lines(d)
        y = section(c, y, d['title'], '· 반말' if d['talk'] == 'banmal' else '· 존댓말')
        c.setFont('Helvetica-Bold', 9); c.setFillColor(MUTED)
        c.drawString(M, y, 'Gaps, in order:')
        y -= 14
        for i in gap_map[d['id']]:
            who, ko, rom, en, mine = lines[i]
            c.setFont('KO-B', 12); c.setFillColor(CON)
            word = ko.split(' ')[-1]
            c.drawString(M + 10, y, word)
            x = M + 10 + ko_width(word, 12, True) + 10
            rich(c, x, y, f'(whole line: “{en}”)', 9, MUTED, max_w=W - M)
            y -= 18
        y -= 6
        c.setFont('Helvetica-Bold', 9); c.setFillColor(MUTED)
        c.drawString(M, y, 'The whole conversation:'); y -= 14
        for who, ko, rom, en, mine in lines:
            if y < M + 40:
                c.showPage(); header(c, unit, 'Answer key', 'continued'); y = H - M - 62
            rich(c, M, y, 'You' if mine else who, 8, VOW if mine else CON, bold=True)
            c.setFont('KO-B', 11); c.setFillColor(INK)
            c.drawString(M + 58, y, ko)
            rich(c, M + 58, y - 10, en, 8, MUTED, italic=True, max_w=W - M)
            y -= 24
        y -= 10
        if y < M + 120:
            c.showPage(); header(c, unit, 'Answer key', 'continued'); y = H - M - 62
    c.showPage()


def build(unit):
    path = os.path.join(OUT, f"unit-{unit['id']}.pdf")
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle(f"한글 Quest — Unit {unit['id']}: {unit['title']}")
    vocab_pages(c, unit)
    gap_map = {}
    for d in unit['dialogues']:
        n = len(script_lines(d))
        gaps = sorted(set(range(1, n, 2)))[:3] + sorted(set(range(0, n, 3)))[:3]
        gaps = sorted(set(g for g in gaps if g < n))[:6]
        gap_map[d['id']] = gaps
        dialogue_page_a(c, unit, d, gaps)
        dialogue_page_b(c, unit, d)
    answer_key(c, unit, gap_map)
    c.save()
    return path


if __name__ == '__main__':
    import pikepdf
    for u in L2['units']:
        p = build(u)
        with pikepdf.open(p) as f:
            n = len(f.pages)
        print(f"unit {u['id']}: {os.path.basename(p)}  ({n} pages, {os.path.getsize(p)//1024} KB)")
