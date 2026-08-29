import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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
        G, p, q = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(hasattr(G, 'order') and G.order() > 0)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(isprime(p) and isprime(q) and p != q)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = bool(not getattr(G, 'is_solvable', True))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS: list[str] = [
    "H_1: G is a finite group",
    "H_2: p and q are distinct prime numbers",
    "¬Q: G is not a solvable group"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2