import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            g = witness.get('g')
            n = witness.get('n')
        elif hasattr(witness, 'G') and hasattr(witness, 'g') and hasattr(witness, 'n'):
            G = witness.G
            g = witness.g
            n = witness.n
        else:
            G, g, n = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: g is an element of G
    try:
        h2 = g in G
    except Exception:
        h2 = False

    # H3: \phi_g is the inner automorphism defined by \phi_g(x) = gxg^{-1}
    # We check if n is an integer, as it is required to evaluate the conclusion.
    try:
        h3 = isinstance(n, (int, sympy.Integer))
    except Exception:
        h3 = False

    # neg_Q: The order of \phi_g in Aut(G) does not divide n
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            Z = G.center()
            k = 1
            current = g
            while current not in Z:
                current = current * g
                k += 1
            neg_q = bool(n % k != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: g is an element of G",
    "H_3: \phi_g is the inner automorphism defined by \phi_g(x) = gxg^{-1}",
    "¬Q: The order of \phi_g in Aut(G) does not divide n"
]

N_HYP = 3
NEG_Q_INDEX = 3