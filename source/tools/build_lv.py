# Sopaan · Class 10 level-wise learning sheets (sections by marks, Levels 1-5, gated, solid colours)
import json, re, sys, importlib.util, os

chdir = sys.argv[1]                      # e.g. lv05
spec = importlib.util.spec_from_file_location('content', os.path.join(chdir, 'content.py'))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
notes = open(os.path.join(chdir, 'notes.html'), encoding='utf8').read()

src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'engine', 'c01.html'), encoding='utf8').read()          # engine base (dusty-blue skin, re-skinned below)
src = src[src.index('<!DOCTYPE html>'):]
if src.rstrip().endswith('</body></html>'): src = src[:src.rindex('</body></html>')]

ch = C.CHAPTER; n = ch['num']; title = ch['title']
CHAIN_F = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chain.json')
CHAIN = json.load(open(CHAIN_F)) if os.path.exists(CHAIN_F) else {}
NEXT = None
for k in sorted(int(x) for x in CHAIN if CHAIN[x].get('url')):
    if k > n: NEXT = {"url": CHAIN[str(k)]['url'], "title": 'Ch %d %s' % (k, CHAIN[str(k)]['title'])}; break

# ---------- solid standard colours ----------
LEVEL_COL = ["#16A34A", "#2563EB", "#7C3AED", "#EA580C", "#DC2626"]   # green, blue, violet, orange, red
SKIN = {  # dusty-blue skin hex -> solid standard hex (light + dark)
    '#EDF2F7': '#EFF6FF', '#D9E3EE': '#DBEAFE', '#9BB2CB': '#93C5FD', '#4E6E91': '#2563EB', '#2E435A': '#1E3A8A',
    '#6582A2': '#3B82F6', '#3E5876': '#1D4ED8', '#7893B1': '#60A5FA', '#27394C': '#172554', '#CFD7EA': '#DBEAFE',
    '#F7F5EF': '#F8FAFC', '#FFFDF8': '#FFFFFF', '#2F2C27': '#0F172A', '#6B6559': '#475569', '#E6E0D3': '#E2E8F0',
    '#5B8C5A': '#16A34A', '#E8F0E4': '#DCFCE7', '#B8893B': '#D97706', '#F6EDD9': '#FEF3C7', '#B5654A': '#DC2626', '#F5E4DD': '#FEE2E2',
    '#1B1A17': '#0B1220', '#23211D': '#111827', '#E9E4D8': '#E5E7EB', '#B3AB9A': '#9CA3AF', '#38342D': '#1F2937',
    '#8DB58A': '#4ADE80', '#24301F': '#052E16', '#D9B36A': '#FBBF24', '#352B17': '#422006', '#D69580': '#F87171', '#3A2520': '#450A0A',
}
for a, b in SKIN.items():
    src = re.sub(re.escape(a), b, src, flags=re.I)
src = src.replace('rgba(46,67,90,', 'rgba(15,23,42,')

def colours(h):
    h = h.replace('{C800}', '#1E3A8A').replace('{C600}', '#2563EB')
    for i, c in enumerate(LEVEL_COL + LEVEL_COL): h = h.replace('{C%d}' % (i + 1), c)
    return h
notes = colours(notes)

SECS = [('m1', '1 mark', '1-mark questions · MCQ and assertion–reason'), ('m2', '2 marks', '2-mark questions'), ('m3', '3 marks', '3-mark questions'),
        ('c4', 'Case study · 4 marks', 'Case-based questions · 4 marks'), ('m5', '5 marks', '5-mark questions')]
SECNAME = {k: v for k, v, _ in SECS}

# ---------- data ----------
los, sections = [], []
for i, lv in enumerate(C.LEVELS):
    code = 'Level %d' % (i + 1)
    secs = [(k, C.CONTENT[lv['id']].get(k, [])) for k, _, _ in SECS]
    secs = [(k, sl) for k, sl in secs if sl]
    los.append({"id": lv['id'], "code": code, "short": lv['short'], "text": lv['text'],
                "practice": "p_%s_%s" % (lv['id'], secs[0][0]), "test": "x_chap"})
    for k, sl in secs:
        for j, q in enumerate(sl):
            q.setdefault('tag', ''); q.setdefault('marks', ''); q['book'] = k
            q['src'] = q.get('src') or ('Q%d' % (j + 1))
        sections.append({"id": "p_%s_%s" % (lv['id'], k), "label": "%s · %s" % (code, SECNAME[k]), "sub": lv['text'],
                         "kind": "practice", "book": k, "lo": lv['id'], "slides": sl})
TEST = C.TEST
for q in TEST: q['book'] = 'test'
# The engine escapes HTML in question text: move data tables into 'fig' (rendered as HTML).
_TBL = re.compile(r'(?:<div class="tscroll">\s*)?<table.*?</table>(?:\s*</div>)?', re.S)
def _lift_tables(q):
    for k in ('p', 'text', 'body'):
        v = q.get(k)
        if isinstance(v, str) and '<table' in v:
            tabs = _TBL.findall(v)
            if tabs:
                q[k] = _TBL.sub(' ', v).strip()
                q['fig'] = (q.get('fig') or '') + ''.join(t if t.startswith('<div') else '<div class="tscroll">%s</div>' % t for t in tabs)
for _s in sections:
    for _q in _s['slides']: _lift_tables(_q)
for _q in TEST: _lift_tables(_q)
def qmarks(q):
    if q['kind'] in ('mcq', 'ar'): return 1
    return sum(len(s['a']) for s in q['flat'])
tmarks = sum(qmarks(q) for q in TEST)
sections.append({"id": "x_chap", "label": "Chapter test", "sub": "All levels · %d questions · %d marks · %d minutes" % (len(TEST), tmarks, C.TEST_MINUTES),
                 "kind": "test", "lo": "chap", "slides": TEST})
nprac = sum(len(s['slides']) for s in sections if s['kind'] == 'practice')

# ---------- theory hub ----------
hub = '<div class="hub">'
hub += '<div class="hub-card" style="--hc:#1E3A8A"><h3>📖 Theory notes</h3><p>Key ideas, tips, common mistakes and worked examples for every topic. Read them before Level 1.</p><div class="hub-btns">'
for t in C.TOPICS:
    hub += '<button class="hub-btn" style="--bc:#1E3A8A" data-jump="n_%s">%s %s</button>' % (t['id'], t['num'], t['title'])
hub += '</div></div>'
hub += '<div class="hub-card" style="--hc:#2563EB"><h3>🪜 Five levels, one step at a time</h3><p>Each level has five sections: <b>1 mark</b> (MCQ and assertion–reason), <b>2 marks</b>, <b>3 marks</b>, <b>case study (4 marks)</b> and <b>5 marks</b>. Every blank you fill is worth one mark. Finish a level to unlock the next one.</p><div class="hub-btns">'
for i, lo in enumerate(los):
    hub += '<button class="hub-btn" style="--bc:%s" data-go="%s">%s · %s</button>' % (LEVEL_COL[i], lo['practice'], lo['code'], lo['short'])
hub += '</div></div>'
hub += '<div class="hub-card" style="--hc:#0F172A"><h3>🧪 Chapter test · %d marks · %d minutes</h3><p>Unlocks after Level 5. A board-style paper with every type of question: MCQ, assertion–reason, 2, 3, case-based 4 and 5 marks. One attempt; it submits itself at 00:00 and shows your marks.</p><div class="hub-btns"><button class="hub-btn" style="--bc:#0F172A" data-go="x_chap">🧪 Chapter test</button><button class="hub-btn primary" data-go="report">📊 My report</button></div></div>' % (tmarks, C.TEST_MINUTES)
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
setvar('THEORY', THEORY); setvar('SECTIONS', sections); setvar('LOS', los); setvar('CHAPTER', ch); setvar('TEST_MINUTES', C.TEST_MINUTES)
src = '\n'.join(lines)

def rep(old, new):
    global src
    if old not in src: raise SystemExit('not found: ' + old[:90])
    src = src.replace(old, new, 1)
def sub1(pat, new, flags=0):
    global src
    src2, k = re.subn(pat, lambda m: new, src, count=1, flags=flags)
    if not k: raise SystemExit('pattern not found: ' + pat)
    src = src2

src = re.sub(r'LO_COL=\[[^\]]*\]', 'LO_COL=' + json.dumps(LEVEL_COL + LEVEL_COL), src, count=1)
# case-study passages: render fractions/sup/sub like other question text
assert src.count('esc(slide.body)') == 1
src = src.replace('esc(slide.body)', 'fr(esc(slide.body))')
sub1(r"var SHEET_KEY='[^']*';", "var SHEET_KEY='sopaan-cbse10-lv-ch%02d';" % n)
sub1(r'<title>[^<]*</title>', '<title>Sopaan · Class 10 · Ch %d %s · Levels</title>' % (n, title))
sub1(r'<div class="chapter-eyebrow">[^<]*</div>', '<div class="chapter-eyebrow">CBSE Class 10 Mathematics · Level-wise learning sheets · Chapter %d</div>' % n)
sub1(r'<div class="chapter-title">[^<]*</div>', '<div class="chapter-title">%s</div>' % title)
sub1(r'<div class="chapter-sub">.*?</div><div class="chapter-credit">.*?</div>',
     '<div class="chapter-sub">Theory · 5 levels · 1, 2, 3, 4 (case) and 5-mark sections · %d questions · %d-mark chapter test</div>' % (nprac, tmarks))
sub1(r'<footer class="brandfoot">.*?</footer>',
     '<footer class="brandfoot">Brain &amp; Mind Academy · Sopaan Practice Series · CBSE Class 10 Mathematics · Chapter %d<br>Questions are re-worded for interactive practice; each blank carries one mark. Theory notes, the chapter test and all worked solutions are written by Brain &amp; Mind Academy.</footer>' % n, re.S)

# sections inside a level (the engine's "book" strip)
rep("var BOOK_META={ls:{ic:'📘',name:'Learning sheet · worked examples step by step',sh:'Learning sheet'},ps:{ic:'📗',name:'Practice sheet · exercise questions',sh:'Practice sheet'}};",
    "var BOOK_META={m1:{ic:'①',name:'1-mark questions · MCQ and assertion–reason',sh:'1 mark'},m2:{ic:'②',name:'2-mark questions',sh:'2 marks'},m3:{ic:'③',name:'3-mark questions',sh:'3 marks'},c4:{ic:'📋',name:'Case-based questions · 4 marks',sh:'Case · 4 marks'},m5:{ic:'⑤',name:'5-mark questions',sh:'5 marks'},ls:{ic:'📘',name:'Learning sheet',sh:'Learning sheet'},ps:{ic:'📗',name:'Practice sheet',sh:'Practice sheet'}};")
rep("test:['test','🧪 LO test']", "test:['test','🧪 Chapter test'],m1:['m1','① 1 mark'],m2:['m2','② 2 marks'],m3:['m3','③ 3 marks'],c4:['c4','📋 Case study · 4 marks'],m5:['m5','⑤ 5 marks']")
rep("'<span class=\"bs-l\">Sheets for '+esc(lo.code||'')+'</span>'", "'<span class=\"bs-l\">Sections in '+esc(lo.code||'')+'</span>'")
rep("b('theory','📖 Theory','notes','', '#1E3A8A')+'<span class=\"tab-btn tab-sep\">Practice</span>'", "b('theory','📖 Theory','notes','', '#1E3A8A')+'<span class=\"tab-btn tab-sep\">Levels</span>'")
rep("(ps.length>1?' <small style=\"opacity:.7\">('+ps.length+' sheets)</small>':'')", "''")
src = src.replace("+nb+' questions for '", "+nb+(nb===1?' question for ':' questions for ')")

# chapter test = pseudo level; per-level scores from tagged test questions
src = re.sub(r"(var LOMAP=\{\}; LOS\.forEach\(function\(lo,i\)\{[^\n]*?\}\);)",
    r"\1 LOMAP.chap={id:'chap',code:'Chapter test',short:'All levels',text:'All levels · %d questions · %d marks · %d minutes',col:'#0F172A'};" % (len(TEST), tmarks, C.TEST_MINUTES), src, count=1)
rep("function loTestStats(id){ var ts=tsOf(id), n=SLIDES[id].length, c=0, w=0, u=0; if(!ts) return {n:n,c:0,w:0,u:n,done:false,started:false};",
    "function loTestStats(id,loId){ var ts=tsOf(id), n=SLIDES[id].filter(function(q){ return !loId||q.lo===loId; }).length, c=0, w=0, u=0; if(!ts) return {n:n,c:0,w:0,u:n,done:false,started:false};")
rep("try{ for(var i=0;i<n;i++){ if(isSlideCorrect(id,i)) c++; else if(isSlideAttempted(id,i)) w++; else u++; } }catch(e){}",
    "try{ for(var i=0;i<SLIDES[id].length;i++){ if(loId&&SLIDES[id][i].lo!==loId) continue; if(isSlideCorrect(id,i)) c++; else if(isSlideAttempted(id,i)) w++; else u++; } }catch(e){}")
rep("t:lo.test?loTestStats(lo.test):null", "t:lo.test?loTestStats(lo.test,lo.id):null")
rep("var t=loTestStats(lo.test); if(t&&t.started)", "var t=loTestStats(lo.test,lo.id); if(t&&t.started)")

# wording
for a, b in [
    ("'<span class=\"tab-btn tab-sep\">LO tests · '+TEST_MINUTES+' min</span>'", "'<span class=\"tab-btn tab-sep\">Chapter test · '+TEST_MINUTES+' min</span>'"),
    ("h2.textContent='LO test submitted'", "h2.textContent='Chapter test submitted'"),
    ("🔒 This LO test has been submitted.", "🔒 This chapter test has been submitted."),
    ("b.textContent='🧪 LO test · Quiz mode'", "b.textContent='🧪 Chapter test · Quiz mode'"),
    ("showToast('LO tests always run in Quiz mode.')", "showToast('The chapter test always runs in Quiz mode.')"),
    ("<h2>📊 Learning-objective report</h2>", "<h2>📊 Level report</h2>"),
    ("Each LO has a practice sheet (Learning mode) and a '+TEST_MINUTES+'-minute LO test (always Quiz mode). Mastery bands use the LO test score:",
     "Each level has five mark-wise sections. The '+TEST_MINUTES+'-minute chapter test has questions from every level; each card shows that level\\'s share of it. Mastery bands use the chapter-test score for that level:"),
    ('<div class="rep-cap">Marks earned in submitted LO tests</div>', '<div class="rep-cap">Chapter-test questions correct, by level</div>'),
    ("<div>🧪 Test: <b>", "<div>🧪 Chapter test: <b>"),
    ("tq?'test marks'", "tq?'questions right'"),
    ("Test scores are recorded once, when the test is submitted.", "The chapter test is recorded once, when it is submitted."),
    ("(t.done?'Review test':'Take test')", "(t.done?'Review chapter test':'Take chapter test')"),
    ("📘 Practice</button>", "🪜 Open level</button>"),
    ("'LO report — practice accuracy and LO test results'", "'Level report — practice accuracy and chapter-test results'"),
    ("b('report','📊 LO Report','pie'", "b('report','📊 Report','pie'"),
]:
    rep(a, b)
src = re.sub(r'var GNAV=\{[^\n]*?\};', 'var GNAV=%s;' % json.dumps({"home": None, "prev": None, "next": None}), src, count=1)
rep("function gnavHTML(){ var h=", "function gnavHTML(){ if(!GNAV.home) return ''; var h=")
rep("if(w&&!w.querySelector('.gnav')){ var d=document.createElement('div'); d.innerHTML=gnavHTML();", "if(w&&!w.querySelector('.gnav')&&gnavHTML()){ var d=document.createElement('div'); d.innerHTML=gnavHTML();")
rep("function renderGate(id){", "function renderGate(id){ var _bs=document.getElementById('bookStrip'); if(_bs) _bs.style.display='none';")

# ---------- CSS: solid section badges and level tabs ----------
rep("</style>\n</head>", """  .src-badge.m1,.src-badge.m2,.src-badge.m3,.src-badge.c4,.src-badge.m5{background:var(--lo,#1E3A8A);color:#fff;}
  .book-head.m1,.book-head.m2,.book-head.m3,.book-head.c4,.book-head.m5{background:var(--lo,#1E3A8A);color:#fff;}
  .bs-b.bk-m1,.bs-b.bk-m2,.bs-b.bk-m3,.bs-b.bk-c4,.bs-b.bk-m5{background:#fff;color:#0F172A;border:2px solid var(--lo,#1E3A8A);}
  .bs-b.on{background:var(--lo,#1E3A8A)!important;color:#fff!important;}
  .tab-btn.lv-locked{opacity:.55;}
  .tab-btn.lv-locked::after{content:' 🔒';}
  .fig .tscroll{max-width:100%;overflow-x:auto;display:block;} .fig table{border-collapse:collapse;font-size:15px;margin:4px auto;} .fig table th,.fig table td{border:1px solid var(--rule,#CBD5E1);padding:6px 10px;text-align:center;white-space:nowrap;} .fig table th{background:var(--paper-2,#F1F5F9);font-weight:700;}
  .marks-chip{display:inline-block;margin-left:8px;padding:2px 9px;border-radius:999px;background:#0F172A;color:#fff;font:700 12.5px 'Source Sans 3',sans-serif;vertical-align:middle;}
  .lv-lock-card{text-align:center;padding:28px 18px;}
  .lv-lock-card .big{font-size:44px;}
  .tst-marks{font-weight:800;}
  .subpart-label{text-transform:none!important;}
  .next-ch-wrap{display:flex;justify-content:center;margin:16px 0;}
  a.next-ch{text-decoration:none;display:inline-flex;align-items:center;gap:6px;background:#1E3A8A!important;color:#fff!important;}
  .markscheme{margin:14px 0 10px;border:2px solid #0F172A;border-radius:12px;overflow:hidden;background:var(--card);}
  .markscheme .sm-h{background:#0F172A;color:#fff;font:700 14px 'Source Sans 3',sans-serif;padding:7px 12px;}
  .markscheme table{width:100%;border-collapse:collapse;font-size:15.5px;}
  .markscheme th,.markscheme td{padding:7px 12px;border-top:1px solid var(--rule);text-align:left;vertical-align:top;}
  .markscheme th{font-size:12.5px;text-transform:uppercase;letter-spacing:.04em;color:var(--ink-soft);}
  .markscheme .sm-m{width:64px;text-align:center;font-weight:800;}
  .markscheme .sm-a{color:#16A34A;}
  .markscheme .sm-t td{font-weight:800;background:#F1F5F9;}
  .cb-card{margin:16px 0 0;padding:14px 16px;border-radius:14px;border:2px solid #EA580C;background:#FFF7ED;text-align:left;display:flex;flex-direction:column;gap:6px;}
  .cb-card.cb-ok{border-color:#16A34A;background:#F0FDF4;}
  .cb-card b{font-size:16px;color:#0F172A;} .cb-card span{font-size:14.5px;color:#334155;}
  .cb-list{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px;}
  .cb-b{border:0;border-radius:999px;background:#EA580C;color:#fff;font:700 13.5px 'Source Sans 3',sans-serif;padding:6px 12px;cursor:pointer;}
  .cb-b:focus-visible{outline:3px solid #0F172A;outline-offset:2px;}
  @media (prefers-color-scheme: dark){ :root:not([data-theme="light"]) .cb-card{background:#2A1606;} :root:not([data-theme="light"]) .cb-card.cb-ok{background:#052E16;} :root:not([data-theme="light"]) .cb-card b,:root:not([data-theme="light"]) .cb-card span{color:#E5E7EB;} :root:not([data-theme="light"]) .markscheme .sm-t td{background:#1F2937;} }
  :root[data-theme="dark"] .cb-card{background:#2A1606;} :root[data-theme="dark"] .cb-card.cb-ok{background:#052E16;} :root[data-theme="dark"] .cb-card b,:root[data-theme="dark"] .cb-card span{color:#E5E7EB;} :root[data-theme="dark"] .markscheme .sm-t td{background:#1F2937;}
</style>
</head>""")

# ---------- gating + marks: appended before the final renderLogin() ----------
GATE = r"""
/* ================= levels unlock in order; the chapter test unlocks after the last level ================= */
var UNLOCK_PCT=%d;
function lvSlides(loId){ var out=[]; loPractices(loId).forEach(function(p){ SLIDES[p.id].forEach(function(sl,i){ out.push([p.id,i]); }); }); return out; }
function lvDoneCount(loId){ var L=appState.learning, Q=appState.quiz, done=0, all=lvSlides(loId);
  all.forEach(function(x){ var ok=false;
    try{ var it=L&&L.tabs[x[0]]&&L.tabs[x[0]].items[x[1]]; if(it&&(it.status==='correct'||it.status==='revealed')) ok=true; }catch(e){}
    if(!ok&&Q&&Q.tabs[x[0]]){ var keep=state, km=MODE; state=Q; MODE='quiz'; try{ if(isSlideAttempted(x[0],x[1])) ok=true; }catch(e){} state=keep; MODE=km; }
    if(ok) done++; });
  return {done:done,total:all.length}; }
function lvComplete(loId){ var c=lvDoneCount(loId); return c.total===0||c.done*100>=c.total*UNLOCK_PCT; }
function lvIndex(loId){ for(var i=0;i<LOS.length;i++) if(LOS[i].id===loId) return i; return -1; }
function tabLockedBy(tabId){ var s=SECMAP[tabId]; if(!s) return null;
  if(s.kind==='test'){ for(var i=0;i<LOS.length;i++) if(!lvComplete(LOS[i].id)) return LOS[i]; return null; }
  var k=lvIndex(s.lo); for(var j=0;j<k;j++) if(!lvComplete(LOS[j].id)) return LOS[j]; return null; }
function lockMsg(tabId){ var lo=tabLockedBy(tabId); if(!lo) return ''; var c=lvDoneCount(lo.id);
  return 'Finish '+lo.code+' first: '+c.done+' of '+c.total+' questions done.'; }
(function(){ var _bt=buildTabbar; buildTabbar=function(){ _bt.apply(this,arguments);
  document.querySelectorAll('#tabbar .tab-btn[data-tab]').forEach(function(b){ b.classList.toggle('lv-locked', !!tabLockedBy(b.dataset.tab)); }); }; })();
document.addEventListener('click',function(e){ var t=e.target.closest&&e.target.closest('[data-tab],[data-go]'); if(!t) return;
  var id=t.dataset.tab||t.dataset.go; if(!id||!SECMAP[id]) return; var m=lockMsg(id); if(m){ e.preventDefault(); e.stopImmediatePropagation(); showToast('🔒 '+m); } },true);
(function(){ var _rs=renderSlide; renderSlide=function(){ if(MODE&&SECMAP[activeTab]&&tabLockedBy(activeTab)){ var lo=tabLockedBy(activeTab); showToast('🔒 '+lockMsg(activeTab)); activeTab=lo.practice; for(var i=0;i<SLIDES[activeTab].length;i++){} buildTabbar(); }
  var r=_rs.apply(this,arguments); try{ marksChip(); }catch(e){} return r; }; })();
(function(){ var _ss=saveState; saveState=function(){ _ss.apply(this,arguments); try{ var before=document.querySelectorAll('#tabbar .lv-locked').length; buildTabbarLocks(before); }catch(e){} }; })();
function buildTabbarLocks(before){ var els=document.querySelectorAll('#tabbar .tab-btn[data-tab]'), now=0;
  els.forEach(function(b){ var l=!!tabLockedBy(b.dataset.tab); if(l) now++; b.classList.toggle('lv-locked',l); });
  if(now<before) showToast('🔓 Next step unlocked!'); }
/* marks: every blank is one mark, MCQ and A–R are one mark */
function qMarks(sl){ if(sl.kind==='mcq'||sl.kind==='ar') return 1; return sl.flat.reduce(function(a,s){ return a+Object.keys(s.a).length; },0); }
function qScore(tabId,i){ var sl=SLIDES[tabId][i], it=state.tabs[tabId].items[i];
  if(sl.kind==='mcq'||sl.kind==='ar') return it.choice===sl.correct?1:0;
  var m=0; sl.flat.forEach(function(step,si){ var ss=it.stepStates[si]; Object.keys(step.a).forEach(function(k){ if(answerMatches(ss.inputs[k],step.a[k],step.accept,step.expr)) m++; }); }); return m; }
function marksChip(){ var s=SECMAP[activeTab]; if(!s||!state||!state.tabs[activeTab]) return; var sl=SLIDES[activeTab][state.tabs[activeTab].idx]; var h=document.querySelector('#wrap .qcard .qhead'); if(!sl||!h||h.querySelector('.marks-chip')) return;
  var c=document.createElement('span'); c.className='marks-chip'; var mk=qMarks(sl); c.textContent=mk+(mk===1?' mark':' marks'); h.appendChild(c); }
(function(){ var _rq=renderQuizResults; renderQuizResults=function(){ var r=_rq.apply(this,arguments); try{ if(isTestTab(activeTab)){ var tot=0, got=0; SLIDES[activeTab].forEach(function(sl,i){ tot+=qMarks(sl); got+=qScore(activeTab,i); });
  var meta=document.querySelector('#wrap .tst-done-meta'); if(meta&&!meta.querySelector('.tst-marks')){ var sp=document.createElement('span'); sp.className='tst-marks'; sp.textContent='📝 '+got+' / '+tot+' marks'; meta.insertBefore(sp, meta.firstChild); } } }catch(e){ console.log('marks',e); } return r; }; })();

/* ================= step marks in every solution ================= */
function smFill(t,a){ return t.replace(/__(B\d+)__/g,function(m,k){ var v=String(a[k]==null?'':a[k]); v=v.replace(/\^2/g,'²').replace(/\^3/g,'³').replace(/\*/g,'×'); return '⟦'+v+'⟧'; }); }
(function(){ var _sh=solutionHTML; solutionHTML=function(slide){ var base=_sh(slide); if(!slide) return base; var rows='';
  if(slide.kind==='mcq'||slide.kind==='ar'){ rows='<tr><td>Correct option</td><td class="sm-m">1</td></tr>'; }
  else if(slide.flat){ slide.flat.forEach(function(st){ var k=Object.keys(st.a).length; var txt=smFill(st.t,st.a).replace(/<[^>]*>/g,'');
    rows+='<tr><td>'+(st.partLabel?'<b>'+esc(st.partLabel)+'</b> ':'')+fr(esc(txt)).replace(/⟦([^⟧]*)⟧/g,'<b class="sm-a">$1</b>')+'</td><td class="sm-m">'+k+'</td></tr>'; }); }
  if(!rows) return base; var tot=(slide.kind==='mcq'||slide.kind==='ar')?1:slide.flat.reduce(function(a,st){ return a+Object.keys(st.a).length; },0);
  return '<div class="markscheme"><div class="sm-h">📝 Marking scheme</div><table><tr><th>Step</th><th>Marks</th></tr>'+rows+'<tr class="sm-t"><td>Total</td><td class="sm-m">'+tot+'</td></tr></table></div>'+base; }; })();

/* ================= "Come back to": missed questions of a level, with a fresh try ================= */
function cbItems(loId){ var out=[]; if(!state) return out;
  loPractices(loId).forEach(function(p){ var st=state.tabs[p.id]; if(!st) return; SLIDES[p.id].forEach(function(sl,i){ var it=st.items[i]; if(!it) return;
    var missed = MODE==='quiz' ? (st.submitted||st.done||it.status!=='unanswered') && isSlideAttempted(p.id,i) && !isSlideCorrect(p.id,i) : it.status==='revealed';
    if(missed) out.push({tab:p.id,i:i,sec:(BOOK_META[p.book]||{}).sh||p.book,q:i+1}); }); });
  return out; }
function cbCard(loId){ var lo=LOMAP[loId]; if(!lo) return ''; var L=cbItems(loId);
  if(!L.length) return '<div class="cb-card cb-ok"><b>🔁 Come back to</b><span>No missed questions in '+esc(lo.code)+' so far.</span></div>';
  return '<div class="cb-card"><b>🔁 Come back to · '+esc(lo.code)+'</b><span>'+L.length+' question'+(L.length>1?'s':'')+' where the answer had to be shown. Try each one again from the start.</span><div class="cb-list">'+
    L.map(function(x){ return '<button type="button" class="cb-b" data-cbt="'+x.tab+'" data-cbi="'+x.i+'">'+esc(x.sec)+' · Q'+x.q+'</button>'; }).join('')+'</div></div>'; }
function cbWire(root){ (root||document).querySelectorAll('[data-cbt]').forEach(function(b){ b.onclick=function(){ var id=b.dataset.cbt, i=+b.dataset.cbi;
  if(MODE==='quiz'){ activeTab=id; state.tabs[id]=defaultState().tabs[id]; } else { state.tabs[id].items[i]=blankItem(SLIDES[id][i]); }
  activeTab=id; state.tabs[id].idx=i; saveState(); buildTabbar(); renderSlide(); window.scrollTo({top:0,behavior:'smooth'}); }; }); }
function cbInject(){ var s=SECMAP[activeTab]; if(!s||s.kind!=='practice') return; var done=document.querySelector('#wrap .done-card'); if(!done||done.querySelector('.cb-card')) return;
  var d=document.createElement('div'); d.innerHTML=cbCard(s.lo); done.appendChild(d.firstChild); cbWire(done); }
(function(){ var _rf=renderFinished; renderFinished=function(){ var r=_rf.apply(this,arguments); try{ cbInject(); }catch(e){ console.log('cb',e); } return r; }; })();
(function(){ var _rq=renderQuizResults; renderQuizResults=function(){ var r=_rq.apply(this,arguments); try{ if(!isTestTab(activeTab)) cbInject(); }catch(e){ console.log('cb',e); } return r; }; })();
(function(){ var _rr=renderReport; renderReport=function(){ var r=_rr.apply(this,arguments); try{ document.querySelectorAll('#wrap .lor-card').forEach(function(c,k){ var lo=LOS[k]; if(!lo) return; var d=document.createElement('div'); d.innerHTML=cbCard(lo.id); c.appendChild(d.firstChild); }); cbWire(document.getElementById('wrap')); }catch(e){ console.log('cbr',e); } return r; }; })();

/* ================= next sheet respects the level order; next chapter after the test ================= */
v4NextTab=function(){ var cur=secOf(activeTab);
  if(cur&&cur.kind==='practice'){ var ps=loPractices(cur.lo);
    for(var k=0;k<ps.length;k++){ var st=state&&state.tabs[ps[k].id]; if(ps[k].id===activeTab) continue;
      var left=st?st.items.some(function(it){ return it.status==='unanswered'||it.status==='skipped'; }):true; if(left) return TAB_DEFS.find(function(t){ return t.id===ps[k].id; }); } }
  var i=TAB_DEFS.findIndex(function(t){return t.id===activeTab;});
  for(var j=i+1;j<TAB_DEFS.length;j++){ var id=TAB_DEFS[j].id; if(id!=='theory'&&SLIDES[id]&&SLIDES[id].length&&!tabLockedBy(id)) return TAB_DEFS[j]; }
  return null; };
var NEXT_CH=__NEXTCH__;
function nextChBtn(){ if(!NEXT_CH||!NEXT_CH.url) return null; var a=document.createElement('a'); a.className='btn btn-primary next-ch'; a.href=NEXT_CH.url; a.target='_blank'; a.rel='noopener'; a.textContent='Next chapter: '+NEXT_CH.title+' →'; return a; }
(function(){ var _rq=renderQuizResults; renderQuizResults=function(){ var r=_rq.apply(this,arguments); try{ if(isTestTab(activeTab)){ var card=document.querySelector('#wrap .done-card'); if(card&&!card.querySelector('.next-ch')){ var b=nextChBtn(); if(b){ var w=document.createElement('div'); w.className='next-ch-wrap'; w.appendChild(b); card.insertBefore(w, card.firstChild.nextSibling); } } } }catch(e){ console.log('nc',e); } return r; }; })();
(function(){ var _rr=renderReport; renderReport=function(){ var r=_rr.apply(this,arguments); try{ var w=document.getElementById('wrap'); var b=nextChBtn(); if(w&&b&&!w.querySelector('.next-ch')){ var d=document.createElement('div'); d.className='next-ch-wrap'; d.appendChild(b); w.appendChild(d); } }catch(e){} return r; }; })();
window.__sopaanQA={SECTIONS:SECTIONS,SLIDES:SLIDES,lvDoneCount:lvDoneCount,answerMatches:answerMatches,go:function(id){ activeTab=id; buildTabbar(); renderSlide(); }};
""".replace("__NEXTCH__", json.dumps(NEXT)) % C.UNLOCK_PCT
rep("\nrenderLogin();\n})();", GATE + "\nrenderLogin();\n})();")

OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join('dist', 'levels', os.path.basename(chdir.rstrip('/')) + '.html')
open(OUT, 'w', encoding='utf8').write(src)
print('built', OUT, len(src), 'bytes;', nprac, 'practice +', len(TEST), 'test (', tmarks, 'marks )')
