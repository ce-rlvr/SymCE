import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        if isinstance(witness, dict):
            p = witness['p']
            G = witness['G']
        else:
            p, G = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(G, PermutationGroup)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = not bool(G.is_abelian)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a group",
    "¬Q: G is not an abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2