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
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, g = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(g, Permutation) and (g in G)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(G.is_transitive)
    except Exception:
        h2_ok = False

    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            degree = G.degree
            fixed_count = sum(1 for i in range(degree) if g(i) == i)
            neg_q_ok = (fixed_count > 0) and (fixed_count < degree)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: witness is a tuple (G, g) where G is a PermutationGroup and g is an element of G",
    "H_2: G acts transitively on its domain",
    "¬Q: g fixes at least one point but does not fix all points in the domain"
]

N_HYP = 2
NEG_Q_INDEX = 2