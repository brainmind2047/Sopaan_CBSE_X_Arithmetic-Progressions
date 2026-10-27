# Sopaan · CBSE Class 10 · Arithmetic Progressions

Interactive learning sheets for CBSE Class 10 Mathematics, Chapter 5, by Brain & Mind Academy.

| File | What it is |
| --- | --- |
| `index.html` | Level-wise learning sheet: theory, 5 levels unlocking in order, each with 1, 2, 3, case-based 4 and 5-mark sections (one blank = one mark), marking schemes, "Come back to" list, 24-mark 45-minute chapter test, report |
| `chapter-05-arithmetic-progressions-levels.html` | Same sheet (original upload name) |
| `mcq-sheet.html` | MCQ sheet: topic → learning objective → MCQs, 15-minute chapter test |
| `worksheets/` | Printable worksheet text for Levels 1–5 (`l1.md` … `l5.md`) and the answer key (`key.md`) |
| `source/` | Everything needed to rebuild the pages |

Open `index.html` in a browser, or turn on GitHub Pages (Settings → Pages → branch `main`, folder `/`) to get a link.

## Rebuild

Run from `source/` (Python 3.9+; Node 18+ for the check):

```bash
cd source
python3 tools/build_lv.py level-series/ch05 ../index.html     # level sheet
python3 tools/ws.py level-series/ch05                          # worksheets → dist/worksheets/ch05/
python3 tools/build_mcq.py mcq-series/ch05                     # MCQ sheet → dist/mcq/ch05.html
npm install && npx playwright install chromium
node tools/qa.js ../index.html                                 # every answer accepted, no page errors
```

Questions live in `source/level-series/ch05/l1.py` … `l5.py` and `test.py`; settings (test minutes, unlock rule) in `content.py`.
Each question must have as many blanks as marks — the build stops otherwise.
