import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: Let G be a finite group
    try:
        h1_ok = isinstance(witness, PermutationGroup) and witness.order() > 0
    except Exception:
        h1_ok = False

    # ¬Q: The natural homomorphism from G to Aut(G) is NOT injective, 
    # OR G is NOT isomorphic to Inn(G).
    # The natural homomorphism g -> (x -> g*x*g^-1) has kernel Z(G).
    # It is injective iff Z(G) is trivial.
    # Also, Inn(G) is isomorphic to G/Z(G). For finite groups, G is isomorphic to Inn(G) iff Z(G) is trivial.
    # Therefore, the conclusion fails (¬Q is True) iff the center of G is non-trivial.
    try:
        neg_q_ok = witness.center().order() > 1
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The natural homomorphism to Aut(G) is not injective, or G is not isomorphic to Inn(G) (i.e., Z(G) is non-trivial)"
]

N_HYP = 1
NEG_Q_INDEX = 1