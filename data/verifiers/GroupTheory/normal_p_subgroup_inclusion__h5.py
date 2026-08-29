import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime, factorint
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1), Permutation(2, 3)) # Klein four-group
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
        if len(witness) != 4:
            return [False, False, False, False, False]
        G, p, N, P = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: N is a normal subgroup of G
    try:
        h3 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h3 = False

    # H_4: The order of N is a power of p
    try:
        order = N.order()
        if order == 1:
            h4 = True
        else:
            factors = factorint(order)
            h4 = (list(factors.keys()) == [p])
    except Exception:
        h4 = False

    # ¬Q: N is not a subgroup of P
    try:
        if not isinstance(P, PermutationGroup):
            neg_q = True
        else:
            neg_q = not bool(N.is_subgroup(P))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: N is a normal subgroup of G",
    "H_4: The order of N is a power of p",
    "¬Q: N is not a subgroup of P"
]

N_HYP = 4
NEG_Q_INDEX = 4