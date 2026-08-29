import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            p, G = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(isinstance(G, PermutationGroup))
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = bool(G.center().order() <= 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite group",
    "¬Q: The center of G, Z(G), contains at most one element"
]

N_HYP = 2
NEG_Q_INDEX = 2