# Sopaan · CBSE Class 10 · Arithmetic Progressions

Interactive learning sheets for CBSE Class 10 Mathematics, Chapter 5, by Brain & Mind Academy.

**Live sheet:** https://brainmind2047.github.io/Sopaan_CBSE_X_Arithmetic-Progressions/

| File | What it is |
| --- | --- |
| `index.html` | Level-wise learning sheet: theory, 5 levels unlocking in order, each with 1, 2, 3, case-based 4 and 5-mark sections (one blank = one mark), marking schemes, "Come back to" list, 24-mark 45-minute chapter test, report, and a "Next chapter →" button |
| `mcq-sheet.html` | MCQ sheet: topic → learning objective → MCQs, 15-minute chapter test |
| `worksheets/` | Printable worksheet text for Levels 1–5 (`l1.md` … `l5.md`) and the answer key (`key.md`) |
| `source/` | Everything needed to rebuild the pages |

The whole series: Chapters 1–14 each have their own repo, `brainmind2047/Sopaan_CBSE_X_<Chapter-Name>`.

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
Each question must have as many blanks as marks; the build stops otherwise. `source/tools/chain.json` sets the "Next chapter" links.
