import math
from sympy.ntheory import isprime
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        G, p = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    try:
        order = G.order()
        if order == 1:
            h2 = True
        elif p > 1:
            k = round(math.log(order, p))
            h2 = bool(order == p**k)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: The order of G is a power of p",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2