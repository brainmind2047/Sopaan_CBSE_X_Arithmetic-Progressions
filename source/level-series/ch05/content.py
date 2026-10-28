import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from lvlib import *

CHAPTER = {"num": 5, "part": "CBSE Class 10", "title": "Arithmetic Progressions"}
TEST_MINUTES = 45
UNLOCK_PCT = int(os.environ.get('LV_UNLOCK', '100'))
TOPICS = [{"id": "t1", "num": "5.2", "title": "Arithmetic progressions"},
          {"id": "t2", "num": "5.3", "title": "nth term of an AP"},
          {"id": "t3", "num": "5.4", "title": "Sum of the first n terms"}]
LEVELS = [
 {"id": "l1", "short": "Foundation", "text": "Core questions: the skills every student must have."},
 {"id": "l2", "short": "Practice plus", "text": "The same ideas asked in new ways, with more thinking per step."},
 {"id": "l3", "short": "Challenge", "text": "Well-crafted questions a step above the core level."},
 {"id": "l4", "short": "HOTS", "text": "Higher-order thinking: hard, multi-step and unfamiliar questions."},
 {"id": "l5", "short": "Board PYQs", "text": "Previous CBSE board questions from the last ten years, within the current syllabus."},
]
ONLY = os.environ.get('LV_ONLY')
if ONLY: LEVELS = [l for l in LEVELS if l['id'] == ONLY]
CONTENT = {}
for lv in [l['id'] for l in LEVELS]:
    p = os.path.join(HERE, lv + '.py')
    sp = importlib.util.spec_from_file_location(lv, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    CONTENT[lv] = m.SEC
check(CONTENT)
sp = importlib.util.spec_from_file_location('test', os.path.join(HERE, 'test.py')); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
TEST = m.TEST
