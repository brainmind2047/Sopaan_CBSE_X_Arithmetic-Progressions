# Level 1 · Foundation — every exercise question of the chapter (5.1, 5.2, 5.3 and 5.4), re-worded.
# Mapping (not shown to students): m2 Q1–Q4 = Ex 5.1 Q1(i)–(iv); Q5–Q9 = 5.1 Q2(i)–(v); Q10–Q13 = 5.1 Q3(i)–(iv);
# Q14–Q28 = 5.1 Q4(i)–(xv); Q29–Q33 = 5.2 Q1(i)–(v); Q34–Q35 = 5.2 Q2(i)–(ii); Q36–Q40 = 5.2 Q3(i)–(v);
# Q41 = 5.2 Q4; Q42–Q43 = 5.2 Q5(i)–(ii); Q44 = 5.2 Q6; Q45 = 5.2 Q10; Q46 = 5.2 Q12; Q47 = 5.2 Q15; Q48 = 5.2 Q17;
# Q49 = 5.2 Q20; Q50–Q53 = 5.3 Q1(i)–(iv); Q54–Q55 = 5.3 Q2(ii)–(iii); Q56–Q65 = 5.3 Q3(i)–(x); Q66 = 5.3 Q5;
# Q67 = 5.3 Q7; Q68 = 5.3 Q12; Q69 = 5.3 Q13; Q70 = 5.3 Q14; Q71 = 5.3 Q17.
# m3: Q1 = 5.2 Q7; Q2 = 5.2 Q8; Q3 = 5.2 Q9; Q4 = 5.2 Q11; Q5 = 5.2 Q13; Q6 = 5.2 Q14; Q7 = 5.2 Q16; Q8 = 5.2 Q18;
# Q9 = 5.2 Q19; Q10 = 5.3 Q2(i); Q11 = 5.3 Q4; Q12 = 5.3 Q6; Q13 = 5.3 Q8; Q14 = 5.3 Q10(i); Q15 = 5.3 Q10(ii);
# Q16 = 5.3 Q15; Q17 = 5.3 Q16; Q18 = 5.3 Q18; Q19 = 5.3 Q20; Q20 = 5.4 Q1; Q21 = 5.4 Q3.
# c4: Case 1 = 5.2 Q20 context (Ramkali); Case 2 = 5.2 Q19 context (Subba Rao); Case 3 = 5.4 Q5 (terrace); Case 4 = 5.4 Q4 (houses).
# m5: Q1 = 5.3 Q9; Q2 = 5.3 Q11; Q3 = 5.3 Q19; Q4 = 5.4 Q2.
from lvlib import *

YES = dict(expr='words', accept=['y', 'yes it is', 'it is'])
NO = dict(expr='words', accept=['n', 'no it is not', 'not'])

def yes(t): return S(t, {"B1": "yes"}, **YES)
def no(t): return S(t, {"B1": "no"}, **NO)

m2 = []
def add(p, steps, sol): m2.append(B("Q%d" % (len(m2) + 1), p, steps, sol, marks=2))

# ---- situations (is it an AP?) ----
add("A taxi charges ₹15 for the first km and ₹8 for every further km. Does the list of fares for 1 km, 2 km, 3 km, … form an AP?",
    [S("Fare for 2 km = ₹__B1__", {"B1": "23"}), yes("Do the fares form an AP? __B1__ (yes / no)")],
    "Fares: 15, 23, 31, 39, …\nEach fare is ₹8 more than the one before, so the fares form an AP with d = 8.")
add("A vacuum pump removes [[1||4]] of the air left in a cylinder each time it runs. Does the amount of air left after each run form an AP?",
    [S("If the cylinder starts with 1 unit of air, the air left after the first run = __B1__ unit", {"B1": "3/4"}, expr='fv'),
     no("Does the list 1, [[3||4]], [[9||16]], … form an AP? __B1__ (yes / no)")],
    "After each run [[3||4]] of the air remains: 1, [[3||4]], [[9||16]], [[27||64]], …\nDifferences: [[3||4]] − 1 = −[[1||4]], but [[9||16]] − [[3||4]] = −[[3||16]].\nThe differences are not equal, so it is not an AP. (Each term is multiplied by [[3||4]].)")
add("Digging a well costs ₹150 for the first metre and the cost rises by ₹50 for each further metre. Does the cost of digging after each metre form an AP?",
    [S("Cost after digging 2 metres = ₹__B1__", {"B1": "200"}), yes("Does the list of costs form an AP? __B1__ (yes / no)")],
    "Costs after each metre: 150, 200, 250, 300, …\nEach is ₹50 more than the one before, so it is an AP with d = 50.")
add("₹10000 is deposited at 8% per annum compound interest. Does the amount in the account at the end of each year form an AP?",
    [S("Amount after 1 year = ₹__B1__", {"B1": "10800"}), no("Does the list of amounts form an AP? __B1__ (yes / no)")],
    "Year 1: 10000 × 1.08 = 10800. Year 2: 10800 × 1.08 = 11664.\nIncreases: 800, then 864. They are not equal, so it is not an AP.\nCommon mistake: compound interest multiplies each year; only simple interest adds a fixed amount.")

# ---- first four terms ----
for a, d, t2, rest, dexpr, sol in [
    ("10", "10", "20", "30, 40", None, "a₂ = 10 + 10 = 20, a₃ = 30, a₄ = 40."),
    ("−2", "0", "-2", "-2, -2", None, "With d = 0 every term equals a: −2, −2, −2, −2."),
    ("4", "−3", "1", "-2, -5", None, "a₂ = 4 − 3 = 1, a₃ = −2, a₄ = −5."),
    ("−1", "[[1||2]]", "-1/2", None, 'fv', "a₂ = −1 + [[1||2]] = −[[1||2]], a₃ = 0, a₄ = [[1||2]]."),
    ("−1.25", "−0.25", "-1.5", "-1.75, -2", None, "a₂ = −1.25 − 0.25 = −1.5, a₃ = −1.75, a₄ = −2.\nCommon mistake: adding 0.25 instead of subtracting."),
]:
    if rest is None:
        steps = [S("a₂ = __B1__", {"B1": t2}, expr='fv'), S("a₄ = __B1__", {"B1": "1/2"}, expr='fv')]
    else:
        steps = [S("a₂ = __B1__", {"B1": t2}), S("a₃ and a₄ = __B1__ (write both, separated by a comma)", {"B1": rest}, expr='list')]
    add("Write the first four terms of the AP with first term a = %s and common difference d = %s." % (a, d), steps, sol)

# ---- first term and common difference ----
for seq, a, d, ex, sol in [
    ("3, 1, −1, −3, …", "3", "-2", None, "a = 3; d = 1 − 3 = −2."),
    ("−5, −1, 3, 7, …", "-5", "4", None, "a = −5; d = −1 − (−5) = 4.\nCommon mistake: −1 − (−5) is +4, not −6."),
    ("[[1||3]], [[5||3]], [[9||3]], [[13||3]], …", "1/3", "4/3", 'fv', "a = [[1||3]]; d = [[5||3]] − [[1||3]] = [[4||3]]."),
    ("0.6, 1.7, 2.8, 3.9, …", "0.6", "1.1", None, "a = 0.6; d = 1.7 − 0.6 = 1.1."),
]:
    st = dict(expr=ex) if ex else {}
    add("Write the first term and the common difference of the AP %s" % seq,
        [S("First term a = __B1__", {"B1": a}, **st), S("Common difference d = __B1__", {"B1": d}, **st)], sol)

# ---- which lists are APs? (AP: d and next term · not AP: second difference, then decision) ----
AP = [  # (list, d, d expr, next-term label, next term, next expr, solution)
]
def ap_q(seq, d, nxt, sol, dex=None, nex=None, dlabel="Common difference d = __B1__", nlabel="Next (5th) term = __B1__"):
    a = {} if dex is None else {"expr": dex}
    b = {} if nex is None else {"expr": nex}
    add("Is %s an AP? It is — find its common difference and the next term." % seq,
        [S(dlabel, {"B1": d}, **a), S(nlabel, {"B1": nxt}, **b)], sol)
def not_ap(seq, d1, d2, sol, ex=None):
    a = {} if ex is None else {"expr": ex}
    add("Check whether %s is an AP." % seq,
        [S("a₂ − a₁ = %s and a₃ − a₂ = __B1__" % d1, {"B1": d2}, **a), no("So is it an AP? __B1__ (yes / no)")], sol)

not_ap("2, 4, 8, 12, …", "2", "4", "4 − 2 = 2 but 8 − 4 = 4.\nThe differences are not equal, so it is not an AP.")
ap_q("2, [[5||2]], 3, [[7||2]], …", "1/2", "4", "d = [[5||2]] − 2 = [[1||2]], and every difference is [[1||2]].\nNext three terms: 4, [[9||2]], 5.", dex='fv')
ap_q("−1.2, −3.2, −5.2, −7.2, …", "-2", "-9.2", "d = −3.2 − (−1.2) = −2.\nNext three terms: −9.2, −11.2, −13.2.")
ap_q("−10, −6, −2, 2, …", "4", "6", "d = −6 − (−10) = 4.\nNext three terms: 6, 10, 14.")
ap_q("3, 3 + √2, 3 + 2√2, 3 + 3√2, …", "2", "4", "Each term adds √2, so d = √2.\nNext three terms: 3 + 4√2, 3 + 5√2, 3 + 6√2.",
     dlabel="Common difference d = √__B1__", nlabel="Next term = 3 + __B1__√2")
not_ap("0.2, 0.22, 0.222, 0.2222, …", "0.02", "0.002", "0.22 − 0.2 = 0.02 but 0.222 − 0.22 = 0.002.\nNot equal, so it is not an AP.")
ap_q("0, −4, −8, −12, …", "-4", "-16", "d = −4 − 0 = −4.\nNext three terms: −16, −20, −24.")
ap_q("−[[1||2]], −[[1||2]], −[[1||2]], −[[1||2]], …", "0", "-1/2", "Every difference is 0, so it is an AP with d = 0.\nNext three terms: −[[1||2]], −[[1||2]], −[[1||2]].", nex='fv')
not_ap("1, 3, 9, 27, …", "2", "6", "3 − 1 = 2 but 9 − 3 = 6.\nEach term is multiplied by 3, so it is not an AP.")
ap_q("a, 2a, 3a, 4a, …", "a", "5a", "d = 2a − a = a.\nNext three terms: 5a, 6a, 7a.", dex=True, nex=True)
not_ap("a, a², a³, a⁴, … (a ≠ 1)", "a² − a", "a^3-a^2", "a² − a and a³ − a² = a(a² − a) are different unless a = 1 (or a = 0).\nSo in general it is not an AP.", ex=True)
ap_q("√2, √8, √18, √32, …", "2", "5", "√8 = 2√2, √18 = 3√2, √32 = 4√2, so the terms are √2, 2√2, 3√2, 4√2.\nd = √2. Next three terms: 5√2 (= √50), 6√2 (= √72), 7√2 (= √98).",
     dlabel="Common difference d = √__B1__", nlabel="Next term = __B1__√2")
add("Check whether √3, √6, √9, √12, … is an AP.",
    [S("√9 = __B1__", {"B1": "3"}), no("Is √6 − √3 equal to 3 − √6, so that the list is an AP? __B1__ (yes / no)")],
    "√6 − √3 ≈ 2.449 − 1.732 = 0.717, while 3 − √6 ≈ 0.551.\nThe differences are not equal, so it is not an AP.")
not_ap("1², 3², 5², 7², …", "8", "16", "The list is 1, 9, 25, 49, …\n9 − 1 = 8 but 25 − 9 = 16, so it is not an AP.\nCommon mistake: 1, 3, 5, 7 is an AP, but their squares are not.")
ap_q("1², 5², 7², 73, …", "24", "97", "The list is 1, 25, 49, 73, …\nEvery difference is 24, so it is an AP.\nNext three terms: 97, 121, 145.")

# ---- nth term table ----
add("For an AP, a = 7, d = 3 and n = 8. Find aₙ.",
    [S("a₈ = 7 + (8 − 1) × 3 = 7 + __B1__", {"B1": "21"}), S("a₈ = __B1__", {"B1": "28"})], "aₙ = a + (n − 1)d.\na₈ = 7 + 7 × 3 = 28.")
add("For an AP, a = −18, n = 10 and aₙ = 0. Find d.",
    [S("0 = −18 + 9d, so 9d = __B1__", {"B1": "18"}), S("d = __B1__", {"B1": "2"})], "a₁₀ = a + 9d.\n0 = −18 + 9d ⇒ d = 2.")
add("For an AP, d = −3, n = 18 and aₙ = −5. Find a.",
    [S("17d = __B1__", {"B1": "-51"}), S("−5 = a + 17d gives a = __B1__", {"B1": "46"})], "a₁₈ = a + 17d = a − 51.\n−5 = a − 51 ⇒ a = 46.")
add("For an AP, a = −18.9, d = 2.5 and aₙ = 3.6. Find n.",
    [S("3.6 = −18.9 + (n − 1) × 2.5, so (n − 1) × 2.5 = __B1__", {"B1": "22.5"}), S("n = __B1__", {"B1": "10"})],
    "(n − 1) × 2.5 = 3.6 + 18.9 = 22.5.\nn − 1 = 9 ⇒ n = 10.")
add("For an AP, a = 3.5, d = 0 and n = 105. Find aₙ.",
    [S("a₁₀₅ = 3.5 + 104 × __B1__", {"B1": "0"}), S("a₁₀₅ = __B1__", {"B1": "3.5"})], "With d = 0 every term equals a.\na₁₀₅ = 3.5.")
add("Find the 30th term of the AP 10, 7, 4, …",
    [S("d = __B1__", {"B1": "-3"}), S("a₃₀ = 10 + 29d = __B1__", {"B1": "-77"})], "d = 7 − 10 = −3.\na₃₀ = 10 + 29 × (−3) = 10 − 87 = −77.")
add("Find the 11th term of the AP −3, −[[1||2]], 2, …",
    [S("d = __B1__", {"B1": "5/2"}, expr='fv'), S("a₁₁ = −3 + 10d = __B1__", {"B1": "22"})], "d = −[[1||2]] − (−3) = [[5||2]].\na₁₁ = −3 + 10 × [[5||2]] = −3 + 25 = 22.")

# ---- missing terms ----
add("Fill in the missing term of the AP: 2, ☐, 26.",
    [S("2d = 26 − 2 = __B1__", {"B1": "24"}), S("Missing term = __B1__", {"B1": "14"})], "2 + 2d = 26 ⇒ d = 12.\nMissing term = 2 + 12 = 14 (also the average of 2 and 26).")
add("Fill in the missing terms of the AP: ☐, 13, ☐, 3.",
    [S("13 + 2d = 3 gives d = __B1__", {"B1": "-5"}), S("Missing terms, in order = __B1__", {"B1": "18, 8"}, expr='list')],
    "From 13 to 3 is two steps: 2d = −10, d = −5.\nFirst term = 13 + 5 = 18; third term = 13 − 5 = 8.")
add("Fill in the missing terms of the AP: 5, ☐, ☐, 9[[1||2]].",
    [S("3d = 9.5 − 5, so d = __B1__", {"B1": "1.5"}), S("Missing terms, in order = __B1__", {"B1": "6.5, 8"}, expr='list')],
    "From 5 to 9.5 is three steps: 3d = 4.5, d = 1.5.\nMissing terms: 6.5 and 8.")
add("Fill in the missing terms of the AP: −4, ☐, ☐, ☐, ☐, 6.",
    [S("5d = 6 − (−4), so d = __B1__", {"B1": "2"}), S("Missing terms, in order = __B1__", {"B1": "-2, 0, 2, 4"}, expr='list')],
    "From −4 to 6 is five steps: 5d = 10, d = 2.\nMissing terms: −2, 0, 2, 4.")
add("Fill in the missing terms of the AP: ☐, 38, ☐, ☐, ☐, −22.",
    [S("38 + 4d = −22 gives d = __B1__", {"B1": "-15"}), S("Missing terms, in order = __B1__", {"B1": "53, 23, 8, -7"}, expr='list')],
    "From 38 to −22 is four steps: 4d = −60, d = −15.\nFirst term = 38 + 15 = 53; then 23, 8, −7.")

# ---- which term / how many terms ----
add("Which term of the AP 3, 8, 13, 18, … is 78?",
    [S("78 = 3 + (n − 1) × 5, so (n − 1) × 5 = __B1__", {"B1": "75"}), S("n = __B1__", {"B1": "16"})], "a = 3, d = 5.\n(n − 1) × 5 = 75 ⇒ n − 1 = 15 ⇒ n = 16. 78 is the 16th term.")
add("Find the number of terms in the AP 7, 13, 19, …, 205.",
    [S("205 = 7 + (n − 1) × 6, so n − 1 = __B1__", {"B1": "33"}), S("n = __B1__", {"B1": "34"})], "a = 7, d = 6.\n(n − 1) × 6 = 198 ⇒ n − 1 = 33 ⇒ n = 34.")
add("Find the number of terms in the AP 18, 15[[1||2]], 13, …, −47.",
    [S("d = __B1__", {"B1": "-2.5"}), S("−47 = 18 + (n − 1)d gives n = __B1__", {"B1": "27"})], "d = 15.5 − 18 = −2.5.\n(n − 1)(−2.5) = −65 ⇒ n − 1 = 26 ⇒ n = 27.")
add("Is −150 a term of the AP 11, 8, 5, 2, …?",
    [S("Solving −150 = 11 + (n − 1)(−3) gives n = __B1__", {"B1": "164/3"}, expr='fv'), no("Is −150 a term of the AP? __B1__ (yes / no)")],
    "(n − 1)(−3) = −161 ⇒ n − 1 = [[161||3]] ⇒ n = [[164||3]].\nn must be a natural number, so −150 is not a term.")
add("The 17th term of an AP is 7 more than its 10th term. Find the common difference.",
    [S("a₁₇ − a₁₀ = (a + 16d) − (a + 9d) = __B1__d", {"B1": "7"}), S("d = __B1__", {"B1": "1"})], "a₁₇ − a₁₀ = 7d = 7 ⇒ d = 1.")
add("Two APs have the same common difference. The difference between their 100th terms is 100. What is the difference between their 1000th terms?",
    [S("a₁₀₀ − b₁₀₀ = (a + 99d) − (b + 99d) = a − b = __B1__", {"B1": "100"}), S("a₁₀₀₀ − b₁₀₀₀ = __B1__", {"B1": "100"})],
    "With the same d, the d-terms cancel: any pair of nth terms differs by a − b.\nSo the 1000th terms also differ by 100.")
add("For what value of n are the nth terms of the APs 63, 65, 67, … and 3, 10, 17, … equal?",
    [S("63 + (n − 1)2 = 3 + (n − 1)7 simplifies to 61 + 2n = __B1__", {"B1": "7n-4"}, expr=True), S("n = __B1__", {"B1": "13"})],
    "First AP: aₙ = 61 + 2n. Second AP: aₙ = 7n − 4.\n61 + 2n = 7n − 4 ⇒ 5n = 65 ⇒ n = 13.")
add("Find the 20th term from the last term of the AP 3, 8, 13, …, 253.",
    [S("Reading from the end, the common difference is __B1__", {"B1": "-5"}), S("20th term from the end = 253 + 19 × (−5) = __B1__", {"B1": "158"})],
    "From the end the AP is 253, 248, 243, … with d = −5.\n20th term = 253 − 95 = 158.")
add("Ramkali saved ₹5 in the first week and increased her weekly saving by ₹1.75 each week. In which week will her saving be ₹20.75?",
    [S("5 + (n − 1) × 1.75 = 20.75, so (n − 1) × 1.75 = __B1__", {"B1": "15.75"}), S("n = __B1__", {"B1": "10"})],
    "a = 5, d = 1.75.\n(n − 1) × 1.75 = 15.75 ⇒ n − 1 = 9 ⇒ n = 10. She saves ₹20.75 in the 10th week.")

# ---- sums ----
add("Find the sum of the first 10 terms of 2, 7, 12, …",
    [S("S₁₀ = 5(2 × 2 + 9 × __B1__)", {"B1": "5"}), S("S₁₀ = __B1__", {"B1": "245"})], "a = 2, d = 5.\nS₁₀ = [[10||2]](4 + 45) = 5 × 49 = 245.")
add("Find the sum of the first 12 terms of −37, −33, −29, …",
    [S("S₁₂ = 6(2 × (−37) + 11 × __B1__)", {"B1": "4"}), S("S₁₂ = __B1__", {"B1": "-180"})], "a = −37, d = 4.\nS₁₂ = 6(−74 + 44) = 6 × (−30) = −180.")
add("Find the sum of the first 100 terms of 0.6, 1.7, 2.8, …",
    [S("S₁₀₀ = 50(1.2 + 99 × __B1__)", {"B1": "1.1"}), S("S₁₀₀ = __B1__", {"B1": "5505"})], "a = 0.6, d = 1.1.\nS₁₀₀ = 50(1.2 + 108.9) = 50 × 110.1 = 5505.")
add("Find the sum of the first 11 terms of [[1||15]], [[1||12]], [[1||10]], …",
    [S("d = __B1__", {"B1": "1/60"}, expr='fv'), S("S₁₁ = __B1__", {"B1": "33/20"}, expr='fv')],
    "d = [[1||12]] − [[1||15]] = [[5 − 4||60]] = [[1||60]].\nS₁₁ = [[11||2]]([[2||15]] + [[10||60]]) = [[11||2]] × [[9||30]] = [[33||20]].")
add("Find the sum 34 + 32 + 30 + … + 10.",
    [S("Number of terms n = __B1__", {"B1": "13"}), S("Sum = __B1__", {"B1": "286"})], "10 = 34 + (n − 1)(−2) ⇒ n − 1 = 12 ⇒ n = 13.\nSum = [[13||2]](34 + 10) = 13 × 22 = 286.")
add("Find the sum −5 + (−8) + (−11) + … + (−230).",
    [S("Number of terms n = __B1__", {"B1": "76"}), S("Sum = __B1__", {"B1": "-8930"})], "d = −3. −230 = −5 + (n − 1)(−3) ⇒ n − 1 = 75 ⇒ n = 76.\nSum = 38 × (−5 − 230) = 38 × (−235) = −8930.")

for p, s1, a1, e1, s2, a2, e2, sol in [
    ("a = 5, d = 3, aₙ = 50. Find n and Sₙ.", "n = __B1__", "16", None, "Sₙ = __B1__", "440", None, "50 = 5 + 3(n − 1) ⇒ n = 16.\nS₁₆ = 8(5 + 50) = 440."),
    ("a = 7, a₁₃ = 35. Find d and S₁₃.", "d = __B1__", "7/3", 'fv', "S₁₃ = __B1__", "273", None, "35 = 7 + 12d ⇒ d = [[28||12]] = [[7||3]].\nS₁₃ = [[13||2]](7 + 35) = 273."),
    ("a₁₂ = 37, d = 3. Find a and S₁₂.", "a = __B1__", "4", None, "S₁₂ = __B1__", "246", None, "37 = a + 33 ⇒ a = 4.\nS₁₂ = 6(4 + 37) = 246."),
    ("a₃ = 15, S₁₀ = 125. Find d and a₁₀.", "d = __B1__", "-1", None, "a₁₀ = __B1__", "8", None, "a + 2d = 15 and 5(2a + 9d) = 125 ⇒ 2a + 9d = 25.\n2a + 4d = 30, so 5d = −5, d = −1, a = 17.\na₁₀ = 17 − 9 = 8."),
    ("d = 5, S₉ = 75. Find a and a₉.", "a = __B1__", "-35/3", 'fv', "a₉ = __B1__", "85/3", 'fv', "[[9||2]](2a + 40) = 75 ⇒ 2a + 40 = [[50||3]] ⇒ a = −[[35||3]].\na₉ = a + 40 = [[85||3]]."),
    ("a = 2, d = 8, Sₙ = 90. Find n and aₙ.", "n = __B1__", "5", None, "aₙ = __B1__", "34", None, "[[n||2]](4 + 8(n − 1)) = 90 ⇒ 4n² − 2n − 90 = 0 ⇒ 2n² − n − 45 = 0.\n(n − 5)(2n + 9) = 0 ⇒ n = 5 (n cannot be negative).\na₅ = 2 + 32 = 34."),
    ("a = 8, aₙ = 62, Sₙ = 210. Find n and d.", "n = __B1__", "6", None, "d = __B1__", "54/5", 'fv', "[[n||2]](8 + 62) = 210 ⇒ 35n = 210 ⇒ n = 6.\n62 = 8 + 5d ⇒ d = [[54||5]]."),
    ("aₙ = 4, d = 2, Sₙ = −14. Find n and a.", "n = __B1__", "7", None, "a = __B1__", "-8", None, "a = 4 − 2(n − 1) = 6 − 2n.\nSₙ = [[n||2]](a + 4) = n(5 − n) = −14 ⇒ n² − 5n − 14 = 0 ⇒ n = 7.\na = 6 − 14 = −8."),
    ("a = 3, n = 8, S = 192. Find d.", "4(6 + 7d) = 192, so 6 + 7d = __B1__", "48", None, "d = __B1__", "6", None, "S₈ = [[8||2]](2 × 3 + 7d) = 192 ⇒ 6 + 7d = 48 ⇒ d = 6."),
    ("l = 28, S = 144 and there are 9 terms. Find a.", "[[9||2]](a + 28) = 144, so a + 28 = __B1__", "32", None, "a = __B1__", "4", None, "Sₙ = [[n||2]](a + l).\n[[9||2]](a + 28) = 144 ⇒ a + 28 = 32 ⇒ a = 4."),
]:
    x1 = {} if e1 is None else {"expr": e1}; x2 = {} if e2 is None else {"expr": e2}
    add("In an AP, " + p, [S(s1, {"B1": a1}, **x1), S(s2, {"B1": a2}, **x2)], sol)

add("The first term of an AP is 5, the last term is 45 and the sum is 400. Find the number of terms and the common difference.",
    [S("[[n||2]](5 + 45) = 400 gives n = __B1__", {"B1": "16"}), S("45 = 5 + 15d gives d = __B1__", {"B1": "8/3"}, expr='fv')],
    "25n = 400 ⇒ n = 16.\nl = a + (n − 1)d ⇒ 45 = 5 + 15d ⇒ d = [[40||15]] = [[8||3]].")
add("Find the sum of the first 22 terms of an AP in which d = 7 and the 22nd term is 149.",
    [S("149 = a + 21 × 7 gives a = __B1__", {"B1": "2"}), S("S₂₂ = __B1__", {"B1": "1661"})], "a = 149 − 147 = 2.\nS₂₂ = 11(2 + 149) = 11 × 151 = 1661.")
add("Find the sum of the first 40 positive integers divisible by 6.",
    [S("S = 6(1 + 2 + … + 40) = 6 × __B1__", {"B1": "820"}), S("S = __B1__", {"B1": "4920"})], "The numbers are 6, 12, …, 240.\n1 + 2 + … + 40 = [[40 × 41||2]] = 820, so S = 4920.")
add("Find the sum of the first 15 multiples of 8.",
    [S("S = 8(1 + 2 + … + 15) = 8 × __B1__", {"B1": "120"}), S("S = __B1__", {"B1": "960"})], "8, 16, …, 120.\n1 + 2 + … + 15 = 120, so S = 960.")
add("Find the sum of the odd numbers between 0 and 50.",
    [S("1, 3, 5, …, 49 has n = __B1__ terms", {"B1": "25"}), S("Sum = __B1__", {"B1": "625"})], "49 = 1 + 2(n − 1) ⇒ n = 25.\nSum = [[25||2]](1 + 49) = 625 (= 25²).")
add("In a school, each section of every class plants as many trees as the class number (Class 1 plants 1 tree per section, …, Class 12 plants 12). Each of the 12 classes has 3 sections. How many trees are planted?",
    [S("1 + 2 + … + 12 = __B1__", {"B1": "78"}), S("Total trees = 3 × 78 = __B1__", {"B1": "234"})], "Trees per set of sections: 1 + 2 + … + 12 = 78.\nThree sections each ⇒ 3 × 78 = 234 trees.")

# ===================== 3 marks =====================
m3 = []
def add3(p, steps, sol): m3.append(B("Q%d" % (len(m3) + 1), p, steps, sol, marks=3))
add3("The 11th term of an AP is 38 and the 16th term is 73. Find its 31st term.",
     [S("5d = 73 − 38, so d = __B1__", {"B1": "7"}), S("a = __B1__", {"B1": "-32"}), S("a₃₁ = __B1__", {"B1": "178"})],
     "a + 10d = 38 and a + 15d = 73 ⇒ 5d = 35 ⇒ d = 7.\na = 38 − 70 = −32.\na₃₁ = −32 + 30 × 7 = 178.")
add3("An AP has 50 terms. Its 3rd term is 12 and its last term is 106. Find its 29th term.",
     [S("47d = 106 − 12, so d = __B1__", {"B1": "2"}), S("a = __B1__", {"B1": "8"}), S("a₂₉ = __B1__", {"B1": "64"})],
     "a + 2d = 12 and a + 49d = 106 ⇒ 47d = 94 ⇒ d = 2.\na = 8.\na₂₉ = 8 + 28 × 2 = 64.")
add3("The 3rd and 9th terms of an AP are 4 and −8. Which term of this AP is zero?",
     [S("d = __B1__", {"B1": "-2"}), S("a = __B1__", {"B1": "8"}), S("0 = a + (n − 1)d gives n = __B1__", {"B1": "5"})],
     "a + 2d = 4 and a + 8d = −8 ⇒ 6d = −12 ⇒ d = −2.\na = 8.\n0 = 8 − 2(n − 1) ⇒ n = 5. The 5th term is zero.")
add3("Which term of the AP 3, 15, 27, 39, … is 132 more than its 54th term?",
     [S("a₅₄ = __B1__", {"B1": "639"}), S("Required term = a₅₄ + 132 = __B1__", {"B1": "771"}), S("It is the term number n = __B1__", {"B1": "65"})],
     "d = 12. a₅₄ = 3 + 53 × 12 = 639.\n639 + 132 = 771 = 3 + (n − 1) × 12 ⇒ n − 1 = 64 ⇒ n = 65.\nShortcut: 132 ÷ 12 = 11 terms later, 54 + 11 = 65.")
add3("How many three-digit numbers are divisible by 7?",
     [S("Smallest such number = __B1__", {"B1": "105"}), S("Largest such number = __B1__", {"B1": "994"}), S("Number of terms = __B1__", {"B1": "128"})],
     "105, 112, …, 994 is an AP with d = 7.\n994 = 105 + (n − 1) × 7 ⇒ n − 1 = 127 ⇒ n = 128.")
add3("How many multiples of 4 lie between 10 and 250?",
     [S("First multiple = __B1__", {"B1": "12"}), S("Last multiple = __B1__", {"B1": "248"}), S("Number of multiples = __B1__", {"B1": "60"})],
     "12, 16, …, 248 with d = 4.\n248 = 12 + (n − 1) × 4 ⇒ n − 1 = 59 ⇒ n = 60.")
add3("The 3rd term of an AP is 16 and its 7th term is 12 more than its 5th term. Find the AP.",
     [S("a₇ − a₅ = 2d = 12, so d = __B1__", {"B1": "6"}), S("a + 2d = 16 gives a = __B1__", {"B1": "4"}), S("First three terms = __B1__", {"B1": "4, 10, 16"}, expr='list')],
     "2d = 12 ⇒ d = 6.\na = 16 − 12 = 4.\nThe AP is 4, 10, 16, 22, …")
add3("The sum of the 4th and 8th terms of an AP is 24 and the sum of its 6th and 10th terms is 44. Find its first three terms.",
     [S("(2a + 14d) − (2a + 10d) = 44 − 24 gives d = __B1__", {"B1": "5"}), S("a = __B1__", {"B1": "-13"}), S("First three terms = __B1__", {"B1": "-13, -8, -3"}, expr='list')],
     "2a + 10d = 24 and 2a + 14d = 44 ⇒ 4d = 20 ⇒ d = 5.\n2a = 24 − 50 = −26 ⇒ a = −13.\nTerms: −13, −8, −3.")
add3("Subba Rao started work in 1995 at an annual salary of ₹5000 and got an increment of ₹200 every year. In which year did his income reach ₹7000?",
     [S("5000 + (n − 1) × 200 = 7000, so (n − 1) × 200 = __B1__", {"B1": "2000"}), S("n = __B1__", {"B1": "11"}), S("Year = __B1__", {"B1": "2005"})],
     "a = 5000 (year 1 = 1995), d = 200.\nn − 1 = 10 ⇒ n = 11.\nThe 11th year is 1995 + 10 = 2005.\nCommon mistake: answering 1995 + 11 = 2006.")
add3("Find the sum 7 + 10[[1||2]] + 14 + … + 84.",
     [S("d = __B1__", {"B1": "3.5"}), S("Number of terms n = __B1__", {"B1": "23"}), S("Sum = __B1__", {"B1": "1046.5"})],
     "d = 3.5. 84 = 7 + 3.5(n − 1) ⇒ n − 1 = 22 ⇒ n = 23.\nSum = [[23||2]](7 + 84) = [[23 × 91||2]] = 1046.5.")
add3("How many terms of the AP 9, 17, 25, … must be taken to give a sum of 636?",
     [S("[[n||2]](18 + 8(n − 1)) = 636 simplifies to 4n² + 5n − __B1__ = 0", {"B1": "636"}),
      S("n = __B1__", {"B1": "12"}), S("The other root, which is rejected, is __B1__", {"B1": "-53/4"}, expr='fv')],
     "[[n||2]](8n + 10) = 636 ⇒ n(4n + 5) = 636 ⇒ 4n² + 5n − 636 = 0.\n(n − 12)(4n + 53) = 0 ⇒ n = 12 or n = −[[53||4]].\nn must be a natural number, so 12 terms.")
add3("The first and last terms of an AP are 17 and 350, and the common difference is 9. How many terms are there and what is their sum?",
     [S("350 = 17 + (n − 1) × 9, so n − 1 = __B1__", {"B1": "37"}), S("n = __B1__", {"B1": "38"}), S("Sum = __B1__", {"B1": "6973"})],
     "(n − 1) × 9 = 333 ⇒ n − 1 = 37 ⇒ n = 38.\nSum = [[38||2]](17 + 350) = 19 × 367 = 6973.")
add3("The 2nd and 3rd terms of an AP are 14 and 18. Find the sum of its first 51 terms.",
     [S("d = __B1__", {"B1": "4"}), S("a = __B1__", {"B1": "10"}), S("S₅₁ = __B1__", {"B1": "5610"})],
     "d = 18 − 14 = 4, a = 14 − 4 = 10.\nS₅₁ = [[51||2]](20 + 50 × 4) = [[51||2]] × 220 = 5610.")
add3("Show that aₙ = 3 + 4n defines an AP, and find the sum of its first 15 terms.",
     [S("a₁ = __B1__", {"B1": "7"}), S("aₙ₊₁ − aₙ = __B1__ (a constant, so it is an AP)", {"B1": "4"}), S("S₁₅ = __B1__", {"B1": "525"})],
     "a₁ = 7, a₂ = 11, a₃ = 15; aₙ₊₁ − aₙ = 4 for every n.\na₁₅ = 63.\nS₁₅ = [[15||2]](7 + 63) = 525.")
add3("Show that aₙ = 9 − 5n defines an AP, and find the sum of its first 15 terms.",
     [S("a₁ = __B1__", {"B1": "4"}), S("aₙ₊₁ − aₙ = __B1__ (a constant, so it is an AP)", {"B1": "-5"}), S("S₁₅ = __B1__", {"B1": "-465"})],
     "a₁ = 4, a₂ = −1, a₃ = −6; the difference is always −5.\na₁₅ = 9 − 75 = −66.\nS₁₅ = [[15||2]](4 − 66) = −465.")
add3("A contractor is fined ₹200 for the first day of delay, ₹250 for the second, ₹300 for the third, and so on. How much does he pay for a 30-day delay?",
     [S("d = __B1__", {"B1": "50"}), S("Fine for the 30th day = __B1__", {"B1": "1650"}), S("Total fine = ₹__B1__", {"B1": "27750"})],
     "a = 200, d = 50.\na₃₀ = 200 + 29 × 50 = 1650.\nS₃₀ = 15(200 + 1650) = ₹27750.")
add3("₹700 is to be given as seven prizes, each prize ₹20 less than the one before it. Find the value of each prize.",
     [S("[[7||2]](2a − 120) = 700 gives the first prize a = ₹__B1__", {"B1": "160"}),
      S("Smallest prize = ₹__B1__", {"B1": "40"}), S("All seven prizes, largest first = __B1__", {"B1": "160, 140, 120, 100, 80, 60, 40"}, expr='list')],
     "d = −20, n = 7: [[7||2]](2a − 120) = 700 ⇒ 2a − 120 = 200 ⇒ a = 160.\nPrizes: 160, 140, 120, 100, 80, 60, 40.")
add3("A spiral is made of successive semicircles with radii 0.5 cm, 1.0 cm, 1.5 cm, 2.0 cm, … What is the total length of 13 such semicircles? (Take π = [[22||7]].)",
     [S("Radius of the 13th semicircle = __B1__ cm", {"B1": "6.5"}), S("Sum of the 13 radii = __B1__ cm", {"B1": "45.5"}), S("Total length = π × 45.5 = __B1__ cm", {"B1": "143"})],
     "Length of a semicircle = πr.\nRadii: 0.5, 1, …, 6.5; sum = [[13||2]](0.5 + 6.5) = 45.5.\nLength = [[22||7]] × 45.5 = 143 cm.")
add3("In a potato race, a bucket is at the start. The first potato is 5 m from the bucket and each next potato is 3 m further, with 10 potatoes in a line. A runner fetches each potato separately and brings it back to the bucket. Find the total distance run.",
     [S("Distance from the bucket to the 10th potato = __B1__ m", {"B1": "32"}), S("5 + 8 + … + 32 = __B1__", {"B1": "185"}), S("Total distance run = __B1__ m", {"B1": "370"})],
     "Distances: 5, 8, …, 32 (a₁₀ = 5 + 27).\nSum = [[10||2]](5 + 32) = 185.\nEach trip is there and back, so total = 2 × 185 = 370 m.")
add3("Which term of the AP 121, 117, 113, … is its first negative term?",
     [S("121 − 4(n − 1) < 0 gives n > __B1__", {"B1": "31.25"}), S("The first negative term is term number __B1__", {"B1": "32"}), S("Its value = __B1__", {"B1": "-3"})],
     "aₙ = 121 − 4(n − 1) = 125 − 4n < 0 ⇒ n > 31.25.\nSo n = 32, and a₃₂ = 125 − 128 = −3.")
add3("The rungs of a ladder are 25 cm apart. The rungs shrink evenly from 45 cm at the bottom to 25 cm at the top, and the top and bottom rungs are 2[[1||2]] m apart. How much wood is needed for the rungs?",
     [S("Number of rungs = __B1__", {"B1": "11"}), S("Each rung is shorter than the one below by __B1__ cm", {"B1": "2"}), S("Total length of wood = __B1__ cm", {"B1": "385"})],
     "250 cm ÷ 25 cm = 10 gaps, so 11 rungs.\n25 = 45 + 10d ⇒ d = −2.\nTotal = [[11||2]](45 + 25) = 385 cm.\nCommon mistake: counting 10 rungs instead of 11.")

# ===================== case studies (4 marks) =====================
c4 = [
 CASE("Case 1", "Ramkali's piggy bank",
      "Ramkali wants to save for her daughter's school fees. She saves ₹5 in the first week and then ₹1.75 more each week than the week before: ₹5, ₹6.75, ₹8.50, …",
      [S("The common difference of her weekly savings is ₹__B1__", {"B1": "1.75"}, part="(i)"),
       S("Her saving in the 10th week = ₹__B1__", {"B1": "20.75"}, part="(ii)"),
       S("Total saved in the first 10 weeks = ₹__B1__, and she saves ₹13.75 in week number __B2__", {"B1": "128.75", "B2": "6"}, part="(iii)")],
      "d = 6.75 − 5 = 1.75.\na₁₀ = 5 + 9 × 1.75 = 20.75.\nS₁₀ = 5(5 + 20.75) = 128.75.\n13.75 = 5 + (n − 1)1.75 ⇒ n − 1 = 5 ⇒ n = 6."),
 CASE("Case 2", "Subba Rao's salary",
      "Subba Rao joined a company in 1995 with an annual salary of ₹5000. Every year his salary rises by ₹200.",
      [S("His salary in 2000 = ₹__B1__", {"B1": "6000"}, part="(i)"),
       S("The year in which his salary is ₹6400 = __B1__", {"B1": "2002"}, part="(ii)"),
       S("His salary in 2004 = ₹__B1__, and his total earnings from 1995 to 2004 = ₹__B2__", {"B1": "6800", "B2": "59000"}, part="(iii)")],
      "2000 is the 6th year: 5000 + 5 × 200 = 6000.\n6400 = 5000 + (n − 1)200 ⇒ n = 8 ⇒ 1995 + 7 = 2002.\n2004 is the 10th year: 5000 + 9 × 200 = 6800.\nTotal = [[10||2]](5000 + 6800) = 59000."),
 CASE("Case 3", "Building a terrace",
      "A terrace around a football ground has 15 concrete steps, each 50 m long. Each step rises [[1||4]] m and has a tread of [[1||2]] m. The first step is a block 50 m × [[1||2]] m × [[1||4]] m; the second is 50 m × [[1||2]] m × [[1||2]] m, and so on — each step rests on the ground.",
      [S("Volume of concrete in the first step = __B1__ m³", {"B1": "6.25"}, part="(i)"),
       S("Volume in the second step = __B1__ m³", {"B1": "12.5"}, part="(ii)"),
       S("Volume in the 15th step = __B1__ m³, and the total volume for all 15 steps = __B2__ m³", {"B1": "93.75", "B2": "750"}, part="(iii)")],
      "Step 1: 50 × 0.5 × 0.25 = 6.25 m³. Step 2: 50 × 0.5 × 0.5 = 12.5 m³.\nThe volumes form an AP with a = d = 6.25.\na₁₅ = 15 × 6.25 = 93.75; S₁₅ = [[15||2]](6.25 + 93.75) = 750 m³."),
 CASE("Case 4", "The house in the middle",
      "The houses in a row are numbered 1, 2, 3, …, 49. There is a house x such that the sum of the house numbers before it equals the sum of the house numbers after it.",
      [S("Sum of the numbers 1 to 49 = __B1__", {"B1": "1225"}, part="(i)"),
       S("Sum of the house numbers before x, in terms of x = __B1__", {"B1": "x(x-1)/2"}, expr=True, part="(ii)"),
       S("Setting [[x(x − 1)||2]] = 1225 − [[x(x + 1)||2]] gives x² = __B1__, so x = __B2__", {"B1": "1225", "B2": "35"}, part="(iii)")],
      "1 + 2 + … + 49 = [[49 × 50||2]] = 1225.\nBefore x: 1 + … + (x − 1) = [[x(x − 1)||2]]. After x: 1225 − [[x(x + 1)||2]].\nEquating: x² − x = 2450 − x² − x ⇒ 2x² = 2450 ⇒ x² = 1225 ⇒ x = 35."),
]

# ===================== 5 marks =====================
m5 = [
 B("Q1", "The sum of the first 7 terms of an AP is 49 and the sum of its first 17 terms is 289. Find the sum of its first n terms.",
   [S("[[7||2]](2a + 6d) = 49 gives a + 3d = __B1__", {"B1": "7"}), S("[[17||2]](2a + 16d) = 289 gives a + 8d = __B1__", {"B1": "17"}),
    S("So d = __B1__ and a = __B2__", {"B1": "2", "B2": "1"}), S("Sₙ = __B1__", {"B1": "n^2"}, expr=True)],
   "a + 3d = 7 and a + 8d = 17 ⇒ 5d = 10 ⇒ d = 2, a = 1.\nSₙ = [[n||2]](2 + 2(n − 1)) = [[n||2]] × 2n = n².", marks=5),
 B("Q2", "The sum of the first n terms of an AP is Sₙ = 4n − n². Find the first term, the sum of the first two terms, the second term, the nth term and the 10th term.",
   [S("a₁ = S₁ = __B1__", {"B1": "3"}), S("S₂ = __B1__", {"B1": "4"}), S("a₂ = S₂ − S₁ = __B1__", {"B1": "1"}),
    S("aₙ = Sₙ − Sₙ₋₁ = __B1__", {"B1": "5-2n"}, expr=True), S("a₁₀ = __B1__", {"B1": "-15"})],
   "S₁ = 4 − 1 = 3; S₂ = 8 − 4 = 4; a₂ = 1.\naₙ = (4n − n²) − (4(n − 1) − (n − 1)²) = 5 − 2n.\nCheck: a₃ = −1 = S₃ − S₂ = 3 − 4.\na₁₀ = 5 − 20 = −15.", marks=5),
 B("Q3", "200 logs are stacked with 20 logs in the bottom row, 19 in the next, 18 in the next, and so on. In how many rows are the 200 logs placed, and how many logs are in the top row?",
   [S("[[n||2]](40 + (n − 1)(−1)) = 200 simplifies to n² − 41n + __B1__ = 0", {"B1": "400"}),
    S("Its roots are n = __B1__ (both values)", {"B1": "16, 25"}, expr='set'),
    S("For n = 25 the top row would have 20 − 24 = __B1__ logs, which is impossible", {"B1": "-4"}),
    S("Number of rows = __B1__", {"B1": "16"}), S("Logs in the top row = __B1__", {"B1": "5"})],
   "a = 20, d = −1: [[n||2]](41 − n) = 200 ⇒ n² − 41n + 400 = 0 ⇒ (n − 16)(n − 25) = 0.\nn = 25 gives a negative top row, so reject it.\nn = 16 rows; top row a₁₆ = 20 − 15 = 5 logs.", marks=5),
 B("Q4", "The sum of the 3rd and 7th terms of an AP is 6 and their product is 8. Find the sum of the first 16 terms of the AP.",
   [S("a₃ + a₇ = 2a + 8d = 6 gives a + 4d = __B1__", {"B1": "3"}),
    S("Writing a₃ = 3 − 2d and a₇ = 3 + 2d, the product gives 9 − 4d² = __B1__", {"B1": "8"}),
    S("d² = __B1__", {"B1": "1/4"}, expr='fv'),
    S("When d = [[1||2]] (so a = 1), S₁₆ = __B1__", {"B1": "76"}),
    S("When d = −[[1||2]] (so a = 5), S₁₆ = __B1__", {"B1": "20"})],
   "a + 4d = 3, so a₃ = a + 2d = 3 − 2d and a₇ = a + 6d = 3 + 2d.\n(3 − 2d)(3 + 2d) = 8 ⇒ 9 − 4d² = 8 ⇒ d = ±[[1||2]].\nd = [[1||2]]: a = 1, S₁₆ = 8(2 + 7.5) = 76.\nd = −[[1||2]]: a = 5, S₁₆ = 8(10 − 7.5) = 20.\nBoth answers are correct; don't drop one.", marks=5),
]

m1 = [
 MCQ("Q1", "Which of these lists is an AP?", ["1, 4, 9, 16, …", "2, 4, 8, 16, …", "3, 7, 11, 15, …", "1, 3, 6, 10, …"], 2,
     "An AP adds the same number each time.\n3, 7, 11, 15: each step is +4, so it is an AP.\nThe others have changing differences (3, 5, 7 · ×2 · 2, 3, 4)."),
 MCQ("Q2", "The common difference of the AP 3, −1, −5, −9, … is:", ["4", "−4", "−3", "2"], 1,
     "d = a₂ − a₁ = −1 − 3 = −4.\nCommon mistake: subtracting the wrong way round (3 − (−1) = 4)."),
 MCQ("Q3", "The 30th term of the AP 10, 7, 4, … is:", ["97", "77", "−77", "−87"], 2,
     "a = 10, d = −3.\na₃₀ = a + 29d = 10 + 29 × (−3) = 10 − 87 = −77."),
 MCQ("Q4", "The 11th term of the AP −3, −[[1||2]], 2, … is:", ["28", "22", "−38", "−48[[1||2]]"], 1,
     "a = −3, d = −[[1||2]] − (−3) = [[5||2]].\na₁₁ = a + 10d = −3 + 10 × [[5||2]] = −3 + 25 = 22."),
 MCQ("Q5", "Which term of the AP 3, 8, 13, 18, … is 78?", ["14th", "15th", "16th", "17th"], 2,
     "a = 3, d = 5, aₙ = 78.\n3 + (n − 1) × 5 = 78 ⇒ (n − 1) = 15 ⇒ n = 16.\nCommon mistake: stopping at n − 1 = 15."),
 MCQ("Q6", "The sum of the first 20 odd natural numbers is:", ["200", "210", "380", "400"], 3,
     "Sum of the first n odd numbers = n².\n20² = 400.\nCheck: 1 + 3 + … + 39, with Sₙ = [[20||2]](1 + 39) = 400."),
 MCQ("Q7", "If 2p, p + 10 and 3p + 2 are three consecutive terms of an AP, then p is:", ["6", "−6", "4", "18"], 0,
     "Middle term rule: 2b = a + c.\n2(p + 10) = 2p + (3p + 2) ⇒ 2p + 20 = 5p + 2 ⇒ 3p = 18 ⇒ p = 6.\nCheck: 12, 16, 20 is an AP with d = 4."),
 AR("Q8", "The sum of the first 100 natural numbers is 5050.", "Sₙ = [[n||2]](a + l), where l is the last term.", 0,
    "S₁₀₀ = [[100||2]](1 + 100) = 50 × 101 = 5050, so A is true.\nR is the correct formula and it is exactly what gives A, so R explains A."),
 AR("Q9", "The numbers 5, 9, 13, 17, … form an AP.", "In an AP the terms keep increasing.", 2,
    "9 − 5 = 13 − 9 = 17 − 13 = 4, so A is true.\nR is false: an AP can decrease (d < 0) or stay constant (d = 0), e.g. 10, 7, 4, …"),
 AR("Q10", "The 10th term of the AP 2, 7, 12, … is 50.", "The nth term of an AP is aₙ = a + (n − 1)d.", 3,
    "R is the correct formula.\na₁₀ = 2 + 9 × 5 = 47, not 50, so A is false.\nCommon mistake: using a + nd = 2 + 10 × 5 = 52 or similar."),
]

SEC = {'m1': m1, 'm2': m2, 'm3': m3, 'c4': c4, 'm5': m5}
