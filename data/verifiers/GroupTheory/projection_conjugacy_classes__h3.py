import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (G, N, x, y), checks the hypotheses and the negated conclusion.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 4:
            return [False, False, False, False]
        G, N, x, y = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: N is a normal subgroup of G
    try:
        h2_ok = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2_ok = False

    # H_3: x and y are conjugate in G
    try:
        h3_ok = False
        if isinstance(x, Permutation) and isinstance(y, Permutation):
            if G.contains(x) and G.contains(y):
                for g in G.elements:
                    if g * y * (~g) == x:
                        h3_ok = True
                        break
    except Exception:
        h3_ok = False

    # ¬Q: The images xN and yN are NOT conjugate in the quotient group G/N
    try:
        q_ok = False
        if isinstance(x, Permutation) and isinstance(y, Permutation):
            if G.contains(x) and G.contains(y):
                # xN and yN are conjugate in G/N iff there exists g in G such that g*y*g^-1 * x^-1 is in N
                for g in G.elements:
                    if N.contains((~x) * g * y * (~g)):
                        q_ok = True
                        break
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: x and y are conjugate in G",
    "¬Q: The images xN and yN are not conjugate in the quotient group G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3