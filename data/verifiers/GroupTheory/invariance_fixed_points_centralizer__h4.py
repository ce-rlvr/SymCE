import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings for witness expressions
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
    """
    Given a witness tuple (G, g, h, x), checks if it is a valid counterexample.
    G is a PermutationGroup acting on {0, 1, ..., G.degree - 1}.
    g, h are Permutations in G.
    x is a point in the domain.
    """
    try:
        G, g, h, x = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group acting on a set X (represented by PermutationGroup and a point x in its domain)
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(x, (int, sympy.Integer)) and 0 <= x < G.degree
    except Exception:
        h1_ok = False

    # H_2: g is an element of G
    try:
        h2_ok = g in G
    except Exception:
        h2_ok = False

    # H_3: h is an element of the centralizer C_G(g)
    try:
        h3_ok = h in G and h * g == g * h
    except Exception:
        h3_ok = False

    # neg_Q: The element h \cdot x is NOT a fixed point of g
    try:
        hx = h(x)
        neg_q_ok = g(hx) != hx
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X (x is in the domain)",
    "H_2: g is an element of G",
    "H_3: h is an element of the centralizer C_G(g)",
    "¬Q: h \cdot x is not a fixed point of g"
]

N_HYP = 3
NEG_Q_INDEX = 3