import sys, os, re, json, importlib.util
sys.path.insert(0, 'tools'); sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else 'level-series/ch05')
sp = importlib.util.spec_from_file_location('c', os.path.join(sys.argv[1] if len(sys.argv) > 1 else 'level-series/ch05', 'content.py')); C = importlib.util.module_from_spec(sp); sp.loader.exec_module(C)
SUP = str.maketrans('0123456789+−-n', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁻ⁿ'); SUB = str.maketrans('0123456789+−-nmkr', '₀₁₂₃₄₅₆₇₈₉₊₋₋ₙₘₖᵣ')
VUL={('1','2'):'½',('1','4'):'¼',('3','4'):'¾',('1','3'):'⅓',('2','3'):'⅔'}
def tx(s):
    s = re.sub(r'(\d)\[\[(\d+)\|\|(\d+)\]\]', lambda m: m.group(1) + (VUL.get((m.group(2), m.group(3))) or (' ' + m.group(2) + '/' + m.group(3))), s)
    s = re.sub(r'\[\[(.+?)\|\|(.+?)\]\]', lambda m: (m.group(1) if re.fullmatch(r'[\w.²³−-]+', m.group(1)) else '(' + m.group(1) + ')') + '/' + (m.group(2) if re.fullmatch(r'[\w.²³−-]+', m.group(2)) else '(' + m.group(2) + ')'), s)
    s = re.sub(r'<sup>(.*?)</sup>', lambda m: m.group(1).translate(SUP) if all(ch in '0123456789+−-n' for ch in m.group(1)) else '^(' + m.group(1) + ')', s)
    s = re.sub(r'<sub>(.*?)</sub>', lambda m: m.group(1).translate(SUB) if all(ch in '0123456789+−-nmkr' for ch in m.group(1)) else '_' + m.group(1), s)
    s = re.sub(r'</?b>', '**', s); s = re.sub(r'</?i>', '*', s); s = re.sub(r'<br\s*/?>', ' ', s); s = re.sub(r'</?(?:span|small|u|em|strong|div|p)\b[^>]*>', '', s)
    s = s.replace('|', '∣')
    return s.strip()
def blanks(t): return re.sub(r'__B\d+__', '\\_\\_\\_\\_\\_\\_', tx(t))
def ans(v):
    v = str(v).replace('^2', '²').replace('^3', '³')
    v = re.sub(r'(?<=[\w)])\*(?=[a-z(])', '', v)
    v = v.replace('*', '×')
    v = re.sub(r'(?<=[\w)²])([+\-])(?=[\w(])', lambda m: ' ' + ('−' if m.group(1) == '-' else '+') + ' ', v)
    v = v.replace('-', '−')
    return v
AR_OPT = ['Both A and R are true, and R is the correct explanation of A.', 'Both A and R are true, but R is not the correct explanation of A.', 'A is true, but R is false.', 'A is false, but R is true.']
SECT = [('m1', 'A', '1 mark each'), ('m2', 'B', '2 marks each'), ('m3', 'C', '3 marks each'), ('c4', 'D', 'Case study · 4 marks each'), ('m5', 'E', '5 marks each')]
def level_md(i, lv):
    secs = C.CONTENT[lv['id']]; out = ['## Level %d · %s' % (i + 1, lv['short']), lv['text'] + ' Each blank in the guided steps carries 1 mark.', '']
    key = []; qn = 0; total = 0
    for k, letter, lab in SECT:
        qs = secs.get(k, [])
        if not qs: continue
        out.append('### Section %s · %s' % (letter, lab)); out.append('')
        for q in qs:
            qn += 1
            src = q.get('src', '')
            tag = ' *(%s)*' % src if src.startswith('CBSE') else ''
            if q['kind'] == 'mcq':
                out.append('%d. %s%s' % (qn, tx(q['text']), tag))
                out.append('    - ' + '   '.join('(%s) %s' % ('abcd'[j], tx(o)) for j, o in enumerate(q['opts'])))
                key.append((qn, '(%s) %s' % ('abcd'[q['correct']], tx(q['opts'][q['correct']])), 1)); total += 1
            elif q['kind'] == 'ar':
                out.append('%d. **Assertion (A):** %s **Reason (R):** %s%s' % (qn, tx(q['a']), tx(q['r']), tag))
                for j, o in enumerate(AR_OPT): out.append('    - (%s) %s' % ('abcd'[j], o))
                key.append((qn, '(%s)' % 'abcd'[q['correct']], 1)); total += 1
            else:
                head = ('**%s.** %s' % (tx(q['title']), tx(q['body']))) if q['kind'] == 'case' else tx(q['p'])
                out.append('%d. %s%s' % (qn, head, tag))
                for st in q['flat']:
                    out.append('    - %s%s' % ((st.get('partLabel') + ' ') if st.get('partLabel') else '', blanks(st['t'])))
                m = sum(len(s['a']) for s in q['flat']); total += m
                key.append((qn, '; '.join(('%s ' % s['partLabel'] if s.get('partLabel') else '') + ', '.join(ans(s['a'][b]) for b in sorted(s['a'])) for s in q['flat']), m))
            out.append('')
    return '\n'.join(out).rstrip() + '\n', key, total
md = {}; keys = {}
for i, lv in enumerate(C.LEVELS):
    m, k, t = level_md(i, lv); md[lv['id']] = m; keys[lv['id']] = (k, t)
kmd = ['## Answer key and marking scheme', 'Each blank carries 1 mark; MCQ and assertion–reason questions carry 1 mark. Answers are listed in the order of the blanks, step by step.', '']
for i, lv in enumerate(C.LEVELS):
    k, t = keys[lv['id']]
    kmd += ['### Level %d · %s · %d marks' % (i + 1, lv['short'], t), '', '| Q | Answers (in order of the blanks) | Marks |', '| --- | --- | --- |']
    kmd += ['| %d | %s | %d |' % (a, b.replace('|', '∣'), c) for a, b, c in k] + ['']
md['key'] = '\n'.join(kmd)
OUTD = os.path.join('dist', 'worksheets', os.path.basename((sys.argv[1] if len(sys.argv) > 1 else 'level-series/ch05').rstrip('/')))
os.makedirs(OUTD, exist_ok=True)
for k, v in md.items(): open(os.path.join(OUTD, k + '.md'), 'w', encoding='utf8').write(v)
for k, v in md.items(): print(k, len(v))
