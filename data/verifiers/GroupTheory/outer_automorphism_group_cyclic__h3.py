import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, PermutationGroup):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a cyclic group
    try:
        if hasattr(witness, 'is_cyclic'):
            h1 = bool(witness.is_cyclic)
        else:
            h1 = False
            if witness.is_abelian:
                order = witness.order()
                for g in witness.elements:
                    if g.order() == order:
                        h1 = True
                        break
    except Exception:
        h1 = False

    # H_2: Inn(G) is the group of inner automorphisms of G
    # This is a definitional hypothesis; we simply verify the witness is a valid group.
    try:
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    # ¬Q: Out(G) is not isomorphic to the full automorphism group Aut(G)
    # For finite groups, Out(G) = Aut(G) / Inn(G).
    # Out(G) is isomorphic to Aut(G) if and only if Inn(G) is trivial.
    # Inn(G) is trivial if and only if G is abelian (i.e., G = Z(G)).
    # Therefore, the conclusion fails (Out(G) is NOT isomorphic to Aut(G)) iff G is NOT abelian.
    try:
        neg_q = not witness.is_abelian
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "H_2: Inn(G) is the group of inner automorphisms of G",
    "¬Q: Out(G) is not isomorphic to the full automorphism group Aut(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2