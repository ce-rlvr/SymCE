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
    try:
        # H_1: Z is the trivial G-module.
        # This is a contextual assumption about the module action. 
        # We simply verify that the witness is a valid finite group.
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        # ¬Q: The second cohomology group H^2(G; Z) is NOT isomorphic to G.
        # By the Universal Coefficient Theorem, for a finite group G with trivial action on Z,
        # H^2(G; Z) is isomorphic to the abelianization G/[G,G].
        # Therefore, H^2(G; Z) is isomorphic to G if and only if G is abelian.
        # The conclusion fails (neg_q is True) if and only if G is NOT abelian.
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            neg_q = not witness.is_abelian
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Z is the trivial G-module",
    "¬Q: H^2(G; Z) is not isomorphic to G"
]

N_HYP = 1
NEG_Q_INDEX = 1