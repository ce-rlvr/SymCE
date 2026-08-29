import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
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
        if isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            order = G.order() if callable(G.order) else G.order
            p = int(round(float(order) ** (1.0 / 3.0)))
    except Exception:
        return [False, False, False]

    # H1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H2: The order of G is p^3
    try:
        order = G.order() if callable(G.order) else G.order
        h2 = bool(order == p**3)
    except Exception:
        h2 = False

    # neg_Q: The center Z(G) does not have order exactly p
    try:
        C = G.center() if callable(G.center) else G.center
        if isinstance(C, (list, set, tuple)):
            c_order = len(C)
        else:
            c_order = C.order() if callable(C.order) else C.order
        neg_q = bool(c_order != p)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: The order of G is p^3",
    "¬Q: The center Z(G) does not have order exactly p"
]

N_HYP = 2
NEG_Q_INDEX = 2