import json, re, sys, importlib.util, os

chdir = sys.argv[1]            # e.g. ch01
spec = importlib.util.spec_from_file_location('content', os.path.join(chdir, 'content.py'))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
notes = open(os.path.join(chdir, 'notes.html'), encoding='utf8').read()

HUE = {1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:1,14:2}
REF = 'engine/c%02d.html' % HUE[C.CHAPTER['num']]
if not os.path.exists(REF): raise SystemExit('no colour reference for ' + REF)
src = open(REF, encoding='utf8').read()
# drop the publish skeleton that wraps the stored copy
src = src[src.index('<!DOCTYPE html>'):]
src = src[:src.rindex('</body></html>')] if src.rstrip().endswith('</body></html>') else src

ch = C.CHAPTER; n = ch['num']; title = ch['title']
LO_COL = json.loads(re.search(r'LO_COL=(\[[^\]]*\])', src).group(1))
C800 = re.search(r'--c-800:(#[0-9A-Fa-f]{6})', src).group(1)
C600 = re.search(r'--c-600:(#[0-9A-Fa-f]{6})', src).group(1)
def colours(h):
    h = h.replace('{C800}', C800).replace('{C600}', C600)
    for i, c in enumerate(LO_COL): h = h.replace('{C%d}' % (i + 1), c)
    return h
notes = colours(notes)
TOP = {t['id']: t for t in C.TOPICS}

# ---------- data ----------
los, sections = [], []
for i, lo in enumerate(C.LOS):
    code = 'LO %d' % (i + 1)
    t = TOP[lo['topic']]
    los.append({"id": lo['id'], "code": code, "short": t['num'] + ' ' + lo['short'], "text": lo['text'],
                "practice": "p_" + lo['id'], "test": "x_chap"})
    sl = C.PRACTICE[lo['id']]
    opg = [s for s in sl if s['book'] == 'opg']; xp = [s for s in sl if s['book'] == 'xp']
    sections.append({"id": "p_" + lo['id'], "label": code + " · OP Gupta MCQs", "sub": lo['text'],
                     "kind": "practice", "book": "opg", "lo": lo['id'], "slides": opg + xp})
nt = len(C.TEST)
sections.append({"id": "x_chap", "label": "Chapter test", "sub": "All learning objectives · %d MCQs · 15 minutes" % nt,
                 "kind": "test", "lo": "chap", "slides": C.TEST})
nprac = sum(len(s['slides']) for s in sections if s['kind'] == 'practice')
nopg = sum(1 for s in sections for q in s['slides'] if q['book'] == 'opg')

# ---------- theory hub ----------
hub = '<div class="hub">'
hub += '<div class="hub-card" style="--hc:'+C800+'"><h3>📖 Theory notes</h3><p>One note per topic, built the same way every time: <b>I can…</b>, a quick recall, 🔑 key ideas, ✨ tips, ⚠️ common mistakes, ✏️ worked examples and 🧠 <b>Remember in 3 lines</b>.</p><div class="hub-btns">'
for i, t in enumerate(C.TOPICS):
    hub += '<button class="hub-btn" style="--bc:%s" data-jump="n_%s">%s %s</button>' % (LO_COL[i], t['id'], t['num'], t['title'])
hub += '</div></div>'
hub += '<div class="hub-card" style="--hc:'+C600+'"><h3>📒 MCQs, topic by topic, LO by LO</h3><p>Each learning objective has one sheet: the <b>O.P. Gupta MCQs</b> for it, then a few <b>📙 extra practice</b> MCQs. Choose Learning Sheet mode (two tries, then the answer) or Quiz mode.</p><div class="hub-btns">'
for i, lo in enumerate(los):
    hub += '<button class="hub-btn" style="--bc:%s" data-go="%s">%s · %s</button>' % (LO_COL[i], lo['practice'], lo['code'], lo['short'])
hub += '</div></div>'
WORDS = {2:'both',3:'all three',4:'all four',5:'all five',6:'all six',7:'all seven',8:'all eight'}
hub += '<div class="hub-card" style="--hc:%s"><h3>🧪 Chapter test · 15 minutes</h3><p>When %s sheets feel easy, take the timed chapter test: %d MCQs from every LO. It runs in Quiz mode, submits itself at 00:00 and can be taken once. Your report shows the score for each LO.</p><div class="hub-btns"><button class="hub-btn" style="--bc:%s" data-go="x_chap">🧪 Start the chapter test</button><button class="hub-btn primary" data-go="report">📊 View my report</button></div></div>' % (LO_COL[3], WORDS.get(len(los),'the'), nt, LO_COL[3])
hub += '</div>'
THEORY = hub + notes

def jsline(name, val):
    return ('var %s = %s;' % (name, json.dumps(val, ensure_ascii=False))).replace('</', '<\\/')

lines = src.split('\n')
def setvar(name, val):
    for k, l in enumerate(lines):
        if l.startswith('var %s =' % name):
            lines[k] = jsline(name, val); return
    raise SystemExit('missing ' + name)
setvar('THEORY', THEORY)
setvar('SECTIONS', sections)
setvar('LOS', los)
setvar('CHAPTER', ch)
setvar('TEST_MINUTES', 15)
src = '\n'.join(lines)

def rep(old, new, count=1):
    global src
    if old not in src: raise SystemExit('not found: ' + old[:80])
    src = src.replace(old, new) if count == 0 else src.replace(old, new, count)

def sub1(pat, new, flags=0):
    global src
    src2, k = re.subn(pat, lambda m: new, src, count=1, flags=flags)
    if not k: raise SystemExit('pattern not found: ' + pat)
    src = src2
sub1(r"var SHEET_KEY='[^']*';", "var SHEET_KEY='sopaan-cbse10-opg-ch%02d';" % n)
sub1(r'<title>Sopaan · Pure Year 2[^<]*</title>', '<title>Sopaan · Class 10 · Ch %d %s</title>' % (n, title))
sub1(r'<div class="chapter-eyebrow">[^<]*</div>', '<div class="chapter-eyebrow">CBSE Class 10 Mathematics · MCQ series · Chapter %d</div>' % n)
sub1(r'<div class="chapter-title">[^<]*</div>', '<div class="chapter-title">%s</div>' % title.replace('&','&amp;'))
src = re.sub(r'<div class="chapter-sub">.*?</div><div class="chapter-credit">.*?</div>',
    '<div class="chapter-sub">Theory · %d topics · %d learning objectives · %d MCQs · 15-minute chapter test</div><div class="chapter-credit">MCQs from O.P. Gupta, <i>Mathematicia: MCQ in Mathematics (Class 10)</i></div>' % (len(C.TOPICS), len(los), nprac), src, count=1)
src = re.sub(r'<footer class="brandfoot">.*?</footer>',
    '<footer class="brandfoot">Brain &amp; Mind Academy · Sopaan Practice Series · CBSE Class 10 Mathematics · Chapter %d<br>Questions marked 📒 are from O.P. Gupta, <i>Mathematicia: MCQ in Mathematics (Class 10)</i>, re-worded for interactive practice. Theory notes, extra practice, the chapter test and all worked solutions are written by Brain &amp; Mind Academy.</footer>' % n, src, count=1, flags=re.S)

# books
rep("var BOOK_META={ls:{ic:'📘',name:'Learning sheet · worked examples step by step',sh:'Learning sheet'},ps:{ic:'📗',name:'Practice sheet · exercise questions',sh:'Practice sheet'}};",
    "var BOOK_META={opg:{ic:'📒',name:'O.P. Gupta · MCQ in Mathematics',sh:'OP Gupta MCQs'},ls:{ic:'📘',name:'Learning sheet',sh:'Learning sheet'},ps:{ic:'📗',name:'Practice sheet',sh:'Practice sheet'}};")
rep("test:['test','🧪 LO test']", "test:['test','🧪 Chapter test'],opg:['opg','📒 O.P. Gupta']")
rep("var bm=BOOK_META[s.book]||BOOK_META.ps; bh.innerHTML=", "var bm=BOOK_META[s.book]||BOOK_META.ps; bh.innerHTML=")
rep("</style>\n</head>", "  .src-badge.opg,.book-head.opg,.bs-b.bk-opg{background:var(--ps-soft);color:var(--ps);box-shadow:inset 0 0 0 1px var(--c-300);}\n</style>\n</head>")

# the chapter test is one pseudo-LO
src = re.sub(r"(var LOMAP=\{\}; LOS\.forEach\(function\(lo,i\)\{[^\n]*?\}\);)",
    r"\1 LOMAP.chap={id:'chap',code:'Chapter test',short:'All LOs',text:'All learning objectives of the chapter · %d MCQs · 15 minutes',col:'%s'};" % (nt, LO_COL[3]), src, count=1)
# per-LO scores from the chapter test
rep("function loTestStats(id){ var ts=tsOf(id), n=SLIDES[id].length, c=0, w=0, u=0; if(!ts) return {n:n,c:0,w:0,u:n,done:false,started:false};",
    "function loTestStats(id,loId){ var ts=tsOf(id), n=SLIDES[id].filter(function(q){ return !loId||q.lo===loId; }).length, c=0, w=0, u=0; if(!ts) return {n:n,c:0,w:0,u:n,done:false,started:false};")
rep("try{ for(var i=0;i<n;i++){ if(isSlideCorrect(id,i)) c++; else if(isSlideAttempted(id,i)) w++; else u++; } }catch(e){}",
    "try{ for(var i=0;i<SLIDES[id].length;i++){ if(loId&&SLIDES[id][i].lo!==loId) continue; if(isSlideCorrect(id,i)) c++; else if(isSlideAttempted(id,i)) w++; else u++; } }catch(e){}")
rep("t:lo.test?loTestStats(lo.test):null", "t:lo.test?loTestStats(lo.test,lo.id):null")
rep("var t=loTestStats(lo.test); if(t&&t.started)", "var t=loTestStats(lo.test,lo.id); if(t&&t.started)")

# wording: LO tests -> chapter test
rep("'<span class=\"tab-btn tab-sep\">LO tests · '+TEST_MINUTES+' min</span>'", "'<span class=\"tab-btn tab-sep\">Chapter test · '+TEST_MINUTES+' min</span>'")
rep("h2.textContent='LO test submitted'", "h2.textContent='Chapter test submitted'")
rep("🔒 This LO test has been submitted.", "🔒 This chapter test has been submitted.")
rep("b.textContent='🧪 LO test · Quiz mode'", "b.textContent='🧪 Chapter test · Quiz mode'")
rep("showToast('LO tests always run in Quiz mode.')", "showToast('The chapter test always runs in Quiz mode.')")
rep("Each LO has a practice sheet (Learning mode) and a '+TEST_MINUTES+'-minute LO test (always Quiz mode). Mastery bands use the LO test score:",
    "Each LO has an MCQ sheet (Learning mode). The '+TEST_MINUTES+'-minute chapter test (always Quiz mode) has questions from every LO, and each LO card shows its share of that test. Mastery bands use the chapter-test score for that LO:")
rep('<div class="rep-cap">Marks earned in submitted LO tests</div>', '<div class="rep-cap">Chapter-test marks, by LO</div>')
rep("<div>🧪 Test: <b>", "<div>🧪 Chapter test: <b>")
rep("Test scores are recorded once, when the test is submitted.", "The chapter test is recorded once, when it is submitted.")
rep("(t.done?'Review test':'Take test')", "(t.done?'Review chapter test':'Take chapter test')")
rep("📘 Practice</button>", "📒 MCQ sheet</button>")
rep("'LO report — practice accuracy and LO test results'", "'Report — MCQ accuracy and chapter-test results'")
rep("b('report','📊 LO Report','pie'", "b('report','📊 Report','pie'")

src = src.replace("+nb+' questions for '", "+nb+(nb===1?' question for ':' questions for ')")
# standalone pilot: no series links until a main page exists
src = re.sub(r'var GNAV=\{[^\n]*?\};', 'var GNAV=%s;' % json.dumps(getattr(C, 'GNAV', {"home": None, "prev": None, "next": None})), src, count=1)
rep("function gnavHTML(){ var h=", "function gnavHTML(){ if(!GNAV.home) return ''; var h=")
rep("if(w&&!w.querySelector('.gnav')){ var d=document.createElement('div'); d.innerHTML=gnavHTML();", "if(w&&!w.querySelector('.gnav')&&gnavHTML()){ var d=document.createElement('div'); d.innerHTML=gnavHTML();")
# hide the book strip on the test gate
rep("function renderGate(id){", "function renderGate(id){ var _bs=document.getElementById('bookStrip'); if(_bs) _bs.style.display='none';")
open(os.path.join('dist', 'mcq', os.path.basename(chdir.rstrip('/')) + '.html'), 'w', encoding='utf8').write(src)
print('built', chdir, len(src), 'bytes;', nprac, 'practice (', nopg, 'OP Gupta ) +', nt, 'test')
