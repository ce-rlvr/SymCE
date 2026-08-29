import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, p = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    try:
        order = G.order() if callable(G.order) else G.order
        h3 = (order % p == 0)
    except Exception:
        h3 = False

    try:
        count = 0
        ident = G.identity
        elements = G.elements() if callable(G.elements) else G.elements
        for x in elements:
            if x**p == ident:
                count += 1
        neg_q = (count % p != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: p divides the order of G",
    "¬Q: The number of elements x in G such that x^p = e is not a multiple of p"
]

N_HYP = 3
NEG_Q_INDEX = 3