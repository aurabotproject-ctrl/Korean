#!/usr/bin/env python3
"""
Noto Sans CJK ships as OpenType/CFF, which reportlab cannot embed. This subsets the
Korean face down to the characters the app actually uses and converts it to TrueType,
so the practice sheets carry a ~30 KB font instead of a 20 MB one.

Run:  python3 tools/make_fonts.py      (needs /tmp/claude-0/hq.json from data.js)
Out:  /tmp/claude-0/fonts/ko-regular.ttf, ko-bold.ttf
"""
import json, os, subprocess
from fontTools.ttLib import TTCollection
from fontTools import subset

DATA = json.load(open('/tmp/claude-0/hq.json'))
OUT = '/tmp/claude-0/fonts'
os.makedirs(OUT, exist_ok=True)

chars = set(' ')
for ch, d in DATA['letters'].items():
    chars.add(ch)
    chars.update(d['name'])          # 기역, 디귿 …
    chars.update(d['sample'])
for w in DATA['words']:
    chars.update(w['ko'])
for s in DATA['stages']:
    chars.update(s['ko']); chars.update(''.join(s['letters']))
    for l in s.get('lessons') or []:
        for b in (l.get('build') or []):
            chars.update(b)
for f in DATA['finals']:
    chars.add(f['f']); chars.update(f['ex'])
    chars.update((f.get('family') or '').replace(' ', ''))
    for k, _ in f['words']:
        chars.update(k)
for r in DATA['rules'].values():
    chars.update(r['ko'])
    for item in r['items']:
        chars.update(item[0]); chars.update(item[1])
        for wrong in item[3]:
            chars.update(wrong)
chars.update('한글')                  # the app's own name, used in the footer

for src, out in [('NotoSansCJK-Regular.ttc', 'ko-regular'), ('NotoSansCJK-Bold.ttc', 'ko-bold')]:
    coll = TTCollection('/usr/share/fonts/opentype/noto/' + src)
    font = next(f for f in coll.fonts
                if any('Noto Sans CJK KR' in r.toUnicode()
                       for r in f['name'].names if r.nameID == 1))
    otf = f'{OUT}/{out}.otf'
    opts = subset.Options(); opts.glyph_names = True; opts.notdef_outline = True
    sub = subset.Subsetter(options=opts)
    sub.populate(text=''.join(sorted(chars)))
    sub.subset(font)
    font.save(otf)
    subprocess.run(['otf2ttf', otf, '-o', f'{OUT}/{out}.ttf'], check=True, capture_output=True)
    print(out, len(chars), 'characters,', os.path.getsize(f'{OUT}/{out}.ttf') // 1024, 'KB')
