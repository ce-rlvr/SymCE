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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            G = witness.get('G')
        else:
            p, G = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    try:
        h2 = isinstance(G, PermutationGroup) and not G.is_abelian
    except Exception:
        h2 = False

    try:
        if isinstance(G, PermutationGroup):
            center = G.center()
            neg_q = center.order() != p
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a non-abelian group",
    "¬Q: The center Z(G) does not have order exactly p"
]

N_HYP = 2
NEG_Q_INDEX = 2