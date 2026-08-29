import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        # The second hypothesis is definitional in this context.
        # We just require the witness to be a valid group.
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    try:
        if callable(witness.is_nilpotent):
            neg_q = not witness.is_nilpotent()
        else:
            neg_q = not bool(witness.is_nilpotent)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: Phi(G) is the Frattini subgroup of G",
    "¬Q: G is not nilpotent"
]

N_HYP = 2
NEG_Q_INDEX = 2