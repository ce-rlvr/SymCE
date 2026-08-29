import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
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
    # H_1: G is a permutation group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The degree p of G is a prime number
    try:
        h2 = False
        if h1:
            h2 = isprime(witness.degree)
    except Exception:
        h2 = False

    # H_3: G acts transitively on its domain
    try:
        h3 = False
        if h1:
            trans = witness.is_transitive
            if callable(trans):
                h3 = bool(trans())
            else:
                h3 = bool(trans)
    except Exception:
        h3 = False

    # ¬Q: G is not equal to the symmetric group S_p
    try:
        neg_q = False
        if h1:
            order = witness.order
            if callable(order):
                order = order()
            neg_q = order != math.factorial(witness.degree)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a permutation group",
    "H_2: The degree p of G is a prime number",
    "H_3: G acts transitively on its domain",
    "¬Q: G is not equal to the symmetric group S_p"
]

N_HYP = 3
NEG_Q_INDEX = 3