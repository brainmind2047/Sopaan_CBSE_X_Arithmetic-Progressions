# Helpers for level-wise sheets. Rule: number of blanks in a question = its marks.
def S(t, a, expr=None, part=None, accept=None):
    """One step line. t contains __B1__, __B2__ ...; a = {'B1': '12', ...}."""
    d = {"t": t, "a": a}
    if expr is not None: d["expr"] = expr
    if part: d["partLabel"] = part
    if accept: d["accept"] = accept
    return d

def B(src, p, steps, sol, marks=None, lo=None):
    q = {"kind": "blank", "src": src, "p": p, "flat": steps, "sol": sol, "tag": "", "marks": ""}
    n = sum(len(s["a"]) for s in steps)
    if marks is not None: assert n == marks, "%s: %d blanks but %d marks" % (src, n, marks)
    if lo: q["lo"] = lo
    return q

def CASE(src, title, body, steps, sol, lo=None):
    q = {"kind": "case", "src": src, "title": title, "body": body, "flat": steps, "sol": sol, "tag": "", "marks": ""}
    n = sum(len(s["a"]) for s in steps)
    assert n == 4, "%s: case study needs 4 blanks, has %d" % (src, n)
    if lo: q["lo"] = lo
    return q

def MCQ(src, text, opts, correct, sol, lo=None):
    assert len(opts) == 4 and 0 <= correct < 4
    q = {"kind": "mcq", "src": src, "text": text, "opts": opts, "correct": correct, "sol": sol, "tag": "", "marks": ""}
    if lo: q["lo"] = lo
    return q

def AR(src, a, r, correct, sol, lo=None):
    """correct: 0 = both true, R explains A · 1 = both true, R does not explain · 2 = A true, R false · 3 = A false, R true"""
    q = {"kind": "ar", "src": src, "a": a, "r": r, "correct": correct, "sol": sol, "tag": "", "marks": ""}
    if lo: q["lo"] = lo
    return q

def check(content):
    """Sanity checks used by every level file."""
    want = {'m2': 2, 'm3': 3, 'c4': 4, 'm5': 5}
    for lv, secs in content.items():
        for k, qs in secs.items():
            if k == 'm1':
                for q in qs: assert q['kind'] in ('mcq', 'ar'), '%s/m1 %s must be MCQ or A-R' % (lv, q['src'])
                continue
            for q in qs:
                n = sum(len(s["a"]) for s in q["flat"])
                assert n == want[k], "%s/%s %s: %d blanks, needs %d" % (lv, k, q["src"], n, want[k])
