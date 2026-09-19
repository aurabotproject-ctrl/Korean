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
chars.update('한글화이팅')            # the app's name and the booklet's sign-off

# Level 2 adds whole sentences, so every character in its content has to be in the subset
import os
if os.path.exists('/tmp/claude-0/hq-l2.json'):
    L2 = json.load(open('/tmp/claude-0/hq-l2.json'))
    for u in L2['units']:
        chars.update(u['ko']); chars.update(u['title'])
        for st in u['sets']:
            for w in st['words']:
                chars.update(w['ko']); chars.update(w['en']); chars.update(w.get('note') or '')
        for d in u['dialogues']:
            for t in d['turns']:
                chars.update(t.get('ko') or '')
                q = t.get('q') or {}
                chars.update(q.get('ko') or ''); chars.update(q.get('prompt') or ''); chars.update(q.get('tip') or '')
                for o in (q.get('options') or []):
                    chars.update(o.get('ko') or ''); chars.update(o.get('en') or '')
    for pat in L2['patterns'].values():
        chars.update(pat['ko']); chars.update(pat['teach'])
        for ex in pat['examples']:
            chars.update(ex[0])
        chars.update(''.join(pat['build']['tiles']))
    for c in L2['cast'].values():
        chars.update(c['name'])
# Essentials repeats most of the vocabulary but adds its own headings and phrases
if os.path.exists('/tmp/claude-0/hq-ess.json'):
    E = json.load(open('/tmp/claude-0/hq-ess.json'))
    for g in E['groups']:
        for sec in g['sections']:
            chars.update(sec.get('note') or '')
            for w in sec['words']:
                chars.update(w['ko']); chars.update(w['en']); chars.update(w.get('note') or '')
chars.update('꼭 필요한 말')
chars = set(ch for ch in chars if ch.isprintable())

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
