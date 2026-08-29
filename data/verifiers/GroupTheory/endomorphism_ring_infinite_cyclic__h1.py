import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    # H_1: End(G) is the ring of group endomorphisms of G with pointwise addition and function composition.
    # This forms a ring if and only if G is an abelian group.
    try:
        if isinstance(witness, PermutationGroup):
            h1_ok = bool(witness.is_abelian)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # neg_Q: End(G) is NOT isomorphic to the ring of integers Z.
    # The ring of integers Z is infinite. For any finite group G, End(G) is finite.
    # Since all PermutationGroup objects in sympy are finite, End(G) cannot be isomorphic to Z.
    try:
        if isinstance(witness, PermutationGroup):
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: End(G) is a ring with pointwise addition (G is abelian)",
    "¬Q: End(G) is not isomorphic to Z"
]

N_HYP = 1
NEG_Q_INDEX = 1