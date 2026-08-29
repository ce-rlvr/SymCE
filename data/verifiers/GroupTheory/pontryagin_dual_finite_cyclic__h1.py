import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.combinatorics.perm_groups import PermutationGroup

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
    # H_1: \mathbb{T} is the circle group (contextual definition)
    # We simply verify the witness is a valid group.
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: \widehat{G} is the Pontryagin dual of G (contextual definition)
    # We simply verify the witness is a valid group.
    try:
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    # ¬Q: \widehat{G} is NOT isomorphic to G
    # For a finite group G, the Pontryagin dual \widehat{G} is isomorphic to its abelianization G/[G,G].
    # Therefore, |\widehat{G}| = |G| / |[G,G]|.
    # \widehat{G} is isomorphic to G if and only if |[G,G]| = 1, which means G is abelian.
    # The conclusion fails (is NOT isomorphic) if and only if G is NOT abelian.
    try:
        neg_q = not witness.is_abelian
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: T is the circle group",
    "H_2: G^ is the Pontryagin dual of G",
    "¬Q: G^ is not isomorphic to G"
]

N_HYP = 2
NEG_Q_INDEX = 2