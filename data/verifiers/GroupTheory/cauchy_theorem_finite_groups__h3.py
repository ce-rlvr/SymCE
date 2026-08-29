import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: p is a prime number
    try:
        h2_ok = bool(isprime(p))
    except Exception:
        h2_ok = False

    # ¬Q: There does not exist an element x in G such that the order of x is p
    try:
        if h1_ok and h2_ok:
            # By Cauchy's and Lagrange's theorems, a finite group has an element
            # of prime order p if and only if p divides the order of the group.
            order = G.order() if callable(G.order) else G.order
            neg_q_ok = bool(order % p != 0)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "¬Q: There does not exist an element x in G such that the order of x is p"
]

N_HYP = 2
NEG_Q_INDEX = 2