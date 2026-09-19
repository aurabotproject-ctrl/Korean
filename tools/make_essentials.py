#!/usr/bin/env python3
"""
Builds assets/printables/essentials.pdf — the survival-vocabulary workbook.

Laid out exactly like the Essentials section in the app: four groups, each with its
lists. Every word gets its meaning, its romanisation, a grey copy to trace and squares
to write it in. Two reference charts at the front (numbers and opposites) because those
are the two things a child will flip back to.

Run:  python3 tools/make_essentials.py
"""
import json, os, textwrap
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color, HexColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'printables')
os.makedirs(OUT, exist_ok=True)
ESS = json.load(open('/tmp/claude-0/hq-ess.json'))

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
SOFT = HexColor('#F2ECFA')


def is_ko(ch):
    return '가' <= ch <= '힣' or '㄰' <= ch <= '㆏' or ch in '○·…'


def runs(text):
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
    latin = 'Helvetica-Bold' if bold else ('Helvetica-Oblique' if italic else 'Helvetica')
    korean = 'KO-B' if bold else 'KO'
    c.setFillColor(colour)
    for chunk, ko in runs(text):
        font = korean if ko else latin
        w = pdfmetrics.stringWidth(chunk, font, size)
        if max_w is not None and (x + w) > max_w:
            while chunk and pdfmetrics.stringWidth(chunk + '…', font, size) > (max_w - x):
                chunk = chunk[:-1]
            if not chunk:
                return x
            chunk += '…'
            w = pdfmetrics.stringWidth(chunk, font, size)
        c.setFont(font, size); c.drawString(x, y, chunk)
        x += w
    return x


def ko_w(t, size, bold=False):
    return pdfmetrics.stringWidth(t, 'KO-B' if bold else 'KO', size)


def box(c, x, y, size, cross=True):
    c.setStrokeColor(LINE); c.setLineWidth(0.8)
    c.rect(x, y, size, size, stroke=1, fill=0)
    if cross:
        c.setStrokeColor(HexColor('#EFE9F8')); c.setLineWidth(0.6); c.setDash(1.5, 2.5)
        c.line(x + size / 2, y + 3, x + size / 2, y + size - 3)
        c.line(x + 3, y + size / 2, x + size - 3, y + size / 2)
        c.setDash()


def glyph(c, ch, x, y, size, colour):
    fs = size * 0.76
    c.setFont('KO-B', fs); c.setFillColor(colour)
    c.drawString(x + (size - pdfmetrics.stringWidth(ch, 'KO-B', fs)) / 2, y + size * 0.24, ch)


def header(c, title, sub):
    rich(c, M, H - M - 6, title, 16, INK, bold=True)
    c.setFont('KO-B', 13); c.setFillColor(CON)
    c.drawRightString(W - M, H - M - 6, '꼭 필요한 말')
    c.setFont('Helvetica', 10); c.setFillColor(MUTED)
    c.drawString(M, H - M - 21, sub)
    c.setStrokeColor(LINE); c.setLineWidth(1); c.line(M, H - M - 29, W - M, H - M - 29)
    c.setFont('Helvetica', 9); c.setFillColor(MUTED)
    c.drawString(M, H - M - 43, 'Name: ______________________       Date: ______________')
    c.setFont('Helvetica-Oblique', 8.4); c.setFillColor(MUTED)
    c.drawString(M, M - 16, 'Say each word out loud as you write it.')
    c.setFont('Helvetica-Oblique', 8.4)
    c.drawRightString(W - M, M - 16, ' Quest · Essentials')
    c.setFont('KO', 8.4)
    c.drawRightString(W - M - pdfmetrics.stringWidth(' Quest · Essentials', 'Helvetica-Oblique', 8.4),
                      M - 16, '한글')


def cover(c):
    c.setFillColor(SOFT); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(PLUM); c.rect(0, H - 140, W, 10, stroke=0, fill=1)
    c.setFillColor(INK); c.setFont('Helvetica-Bold', 42)
    c.drawCentredString(W / 2, H - 230, 'Essentials')
    ko, latin = '꼭 필요한 말', ''
    c.setFont('KO-B', 26); c.setFillColor(CON)
    c.drawCentredString(W / 2, H - 272, ko)
    c.setFillColor(MUTED); c.setFont('Helvetica', 13)
    c.drawCentredString(W / 2, H - 306, 'The survival vocabulary workbook')
    y = H - 380
    for g in ESS['groups']:
        c.setFillColor(PLUM); c.setFont('Helvetica-Bold', 14)
        c.drawString(M + 40, y, f"{g['title']}")
        c.setFillColor(MUTED); c.setFont('Helvetica', 10.5)
        c.drawString(M + 40, y - 15, g['blurb'][:88])
        c.setFillColor(MUTED); c.setFont('Helvetica-Bold', 10)
        c.drawRightString(W - M - 40, y, ' · '.join(s['kind'] for s in g['sections'][:3])[:46])
        y -= 52
    n = sum(len(s['words']) for g in ESS['groups'] for s in g['sections'])
    c.setFillColor(INK); c.setFont('Helvetica-Bold', 12)
    c.drawCentredString(W / 2, 150, f'{n} words · {len(ESS["sections"])} lists')
    c.setFillColor(MUTED); c.setFont('Helvetica', 11)
    c.drawCentredString(W / 2, 128, 'Name: ______________________________')
    c.showPage()


def chart_numbers(c):
    header(c, 'Numbers — the two sets', 'Korean counts with two different number systems. This page is worth keeping open.')
    y = H - M - 70
    a = next(s for s in ESS['sections'] if s['id'] == 'num1')
    b = next(s for s in ESS['sections'] if s['id'] == 'num2')
    colw = (W - 2 * M - 20) / 2
    for i, (s, label, use) in enumerate([(a, 'Korean numbers', 'ages · hours · counting things'),
                                         (b, 'Sino-Korean numbers', 'money · minutes · dates · floors')]):
        x = M + i * (colw + 20)
        c.setFillColor(PLUM); c.setFont('Helvetica-Bold', 12)
        c.drawString(x, y, label)
        c.setFillColor(MUTED); c.setFont('Helvetica', 9)
        c.drawString(x, y - 13, use)
        yy = y - 34
        for w in s['words'][:12]:
            c.setFillColor(SOFT); c.rect(x, yy - 5, colw, 22, stroke=0, fill=1)
            c.setFont('KO-B', 14); c.setFillColor(INK)
            c.drawString(x + 8, yy, w['ko'])
            rich(c, x + 8 + ko_w(w['ko'], 14, True) + 8, yy + 1, w['rom'], 8.5, MUTED)
            rich(c, x + colw - 8 - pdfmetrics.stringWidth(w['en'], 'Helvetica-Bold', 10), yy, w['en'], 10, VOW, bold=True)
            yy -= 26
    y = yy - 20
    c.setFillColor(PLUM); c.setFont('Helvetica-Bold', 12)
    c.drawString(M, y, 'Counters — the little word that follows a number')
    y -= 18
    counters = [w for w in a['words'] if 'counter' in w['en'] or w['ko'] in ('시', '번')]
    x = M
    for w in counters:
        c.setFillColor(SOFT); c.roundRect(x, y - 22, 116, 30, 6, stroke=0, fill=1)
        c.setFont('KO-B', 15); c.setFillColor(CON)
        c.drawString(x + 10, y - 12, w['ko'])
        lx = x + 10 + ko_w(w['ko'], 15, True) + 8      # clear of the Korean, whatever its width
        rich(c, lx, y - 11, w['en'].replace('counter for ', ''), 8.6, INK, max_w=x + 112)
        x += 126
        if x + 116 > W - M:
            x = M; y -= 38
    c.showPage()


def chart_opposites(c):
    header(c, 'Opposites', 'Learn them in pairs — half the work, twice the memory.')
    y = H - M - 74
    s = next(x for x in ESS['sections'] if x['id'] == 'adj1')
    ws = s['words']
    pairs = [(ws[i], ws[i + 1]) for i in range(0, len(ws) - 1, 2)]
    for left, right in pairs:
        c.setFillColor(SOFT); c.roundRect(M, y - 26, W - 2 * M, 38, 8, stroke=0, fill=1)
        c.setFont('KO-B', 17); c.setFillColor(VOW)
        c.drawString(M + 14, y - 12, left['ko'])
        rich(c, M + 14, y - 26, left['en'], 9, MUTED)
        c.setFillColor(MUTED); c.setFont('Helvetica-Bold', 13)
        c.drawCentredString(W / 2, y - 12, '↔')
        c.setFont('KO-B', 17); c.setFillColor(CON)
        wd = ko_w(right['ko'], 17, True)
        c.drawString(W - M - 14 - wd, y - 12, right['ko'])
        rich(c, W - M - 14 - pdfmetrics.stringWidth(right['en'], 'Helvetica', 9), y - 26, right['en'], 9, MUTED)
        y -= 46
    c.setFillColor(MUTED); c.setFont('Helvetica-Oblique', 10)
    c.drawCentredString(W / 2, y - 6, 'Remember: in Korean these are already verbs. 커요 means “is big”, not just “big”.')
    c.showPage()


ROW_H = 70      # word, meaning, example sentence, then the writing squares
HEAD_H = 22


def word_pages(c):
    col_w = (W - 2 * M - 20) / 2
    top = H - M - 62
    bottom = M + 6
    state = {'col': 0, 'y': top, 'title': '', 'sub': ''}

    def new_page():
        c.showPage(); header(c, state['title'], state['sub'])
        state['col'] = 0; state['y'] = top

    def x_now():
        return M + state['col'] * (col_w + 20)

    def room(h):
        if state['y'] - h >= bottom:
            return
        if state['col'] == 0:
            state['col'] = 1; state['y'] = top
        else:
            new_page()

    for g in ESS['groups']:
        state['title'] = g['title']
        state['sub'] = g['sub'] + ' — ' + g['blurb']
        header(c, state['title'], state['sub'][:110])
        state['col'] = 0; state['y'] = top
        for s in g['sections']:
            room(HEAD_H + ROW_H)
            x = x_now()
            c.setFillColor(PLUM); c.setFont('Helvetica-Bold', 10.5)
            c.drawString(x, state['y'], s['title'][:38])
            c.setFillColor(MUTED); c.setFont('Helvetica', 8)
            c.drawString(x, state['y'] - 11, s['kind'])
            state['y'] -= HEAD_H
            for w in s['words']:
                room(ROW_H)
                x = x_now(); right = x + col_w
                c.setFont('KO-B', 13); c.setFillColor(INK)
                c.drawString(x, state['y'], w['ko'])
                rich(c, x + ko_w(w['ko'], 13, True) + 8, state['y'] + 1, w['rom'], 7.4, MUTED, max_w=right)
                rich(c, x, state['y'] - 10, w['en'], 7.6, MUTED, italic=True, max_w=right)
                # the word doing its job, so the page teaches use and not just meaning
                ex = w.get('ex')
                if ex:
                    c.setFillColor(SOFT); c.rect(x, state['y'] - 38, col_w, 25, stroke=0, fill=1)
                    rich(c, x + 5, state['y'] - 23, ex['ko'], 8.8, PLUM, bold=True, max_w=right - 5)
                    rich(c, x + 5, state['y'] - 34, ex['en'], 7.2, MUTED, italic=True, max_w=right - 5)
                letters = [ch for ch in w['ko'] if ch != ' ']
                sz = 20 if len(letters) <= 5 else 15
                bx, yb = x, state['y'] - 58
                for ch in letters:
                    if bx + sz > right:
                        break
                    box(c, bx, yb, sz); glyph(c, ch, bx, yb, sz, GHOST)
                    bx += sz + 3
                bx += 8
                while bx + sz <= right:
                    box(c, bx, yb, sz)
                    bx += sz + 3
                state['y'] -= ROW_H
        c.showPage()


def back_page(c):
    header(c, 'My own top twenty', 'The words YOU keep needing. Write them here as you find them.')
    y = H - M - 74
    c.setFillColor(MUTED); c.setFont('Helvetica', 10)
    c.drawString(M, y, 'Every traveller ends up with their own list. Add a word whenever you have to look one up twice.')
    y -= 24
    colw = (W - 2 * M - 20) / 2
    for i in range(20):
        col, row = i // 10, i % 10
        x = M + col * (colw + 20)
        yy = y - row * 60
        c.setFillColor(MUTED); c.setFont('Helvetica-Bold', 9)
        c.drawString(x, yy, str(i + 1))
        c.setStrokeColor(LINE); c.setLineWidth(0.9)
        c.line(x + 16, yy - 2, x + colw, yy - 2)          # the Korean word
        c.line(x + 16, yy - 22, x + colw, yy - 22)        # what it means
        c.setFillColor(HexColor('#B7A8D4')); c.setFont('Helvetica-Oblique', 7)
        c.drawString(x + 18, yy - 32, 'meaning')
        bx = x + 16
        while bx + 20 <= x + colw:
            box(c, bx, yy - 52, 20)
            bx += 23
    c.showPage()


def build():
    path = os.path.join(OUT, 'essentials.pdf')
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle('한글 Quest — Essentials workbook')
    cover(c)
    chart_numbers(c)
    chart_opposites(c)
    word_pages(c)
    back_page(c)
    c.save()
    import pikepdf
    with pikepdf.open(path) as f:
        n = len(f.pages)
    print(f'essentials.pdf — {n} pages, {os.path.getsize(path)//1024} KB')


if __name__ == '__main__':
    build()
