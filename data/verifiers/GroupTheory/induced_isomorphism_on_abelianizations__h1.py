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
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        # Witness is expected to be a pair of groups (G, H)
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    # H_1: G is isomorphic to H
    try:
        h1_ok = bool(G.is_isomorphic(H))
    except Exception:
        h1_ok = False

    # ¬Q: The abelianization of G is NOT isomorphic to the abelianization of H
    # Two finitely generated abelian groups are isomorphic iff their invariant factors match.
    try:
        inv_G = sorted(G.abelian_invariants())
        inv_H = sorted(H.abelian_invariants())
        neg_q_ok = bool(inv_G != inv_H)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is isomorphic to H",
    "¬Q: The abelianization of G is not isomorphic to the abelianization of H"
]

N_HYP = 1
NEG_Q_INDEX = 1