import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
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
    try:
        G, N, p = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        if isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup):
            is_sub = all(g in G for g in N.generators)
            is_norm = N.is_normal(G)
            h2 = bool(is_sub and is_norm)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: p is a prime number
    try:
        h3 = isinstance(p, (int, sympy.Integer)) and isprime(p)
    except Exception:
        h3 = False

    # ¬Q: The order of the subgroup N is equal to p
    try:
        neg_q = bool(N.order() == p)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: p is a prime number",
    "¬Q: The order of the subgroup N is equal to p"
]

N_HYP = 3
NEG_Q_INDEX = 3