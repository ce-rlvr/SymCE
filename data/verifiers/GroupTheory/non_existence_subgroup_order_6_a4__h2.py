import sympy
from sympy.combinatorics import (
    Permutation, PermutationGroup, AlternatingGroup, SymmetricGroup,
    CyclicGroup, DihedralGroup
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

def conditions(witness) -> list[bool]:
    # H_1: A_4 is the alternating group on 4 letters
    # This is a definitional context hypothesis, inherently true in our setup.
    try:
        h1 = True
    except Exception:
        h1 = False

    # H_2: The cardinality of H is 6
    try:
        if hasattr(witness, 'order'):
            h2 = bool(witness.order() == 6)
        elif hasattr(witness, 'cardinality'):
            h2 = bool(witness.cardinality() == 6)
        else:
            h2 = bool(len(witness) == 6)
    except Exception:
        h2 = False

    # neg_Q: H is a subgroup of A_4
    try:
        if isinstance(witness, PermutationGroup):
            neg_q = True
            # A_4 consists of all even permutations on {0, 1, 2, 3}.
            # We check if all generators of H are even and only move elements < 4.
            for g in witness.generators:
                if not g.is_even:
                    neg_q = False
                    break
                if any(i >= 4 for i in g.support()):
                    neg_q = False
                    break
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A_4 is the alternating group on 4 letters",
    "H_2: The cardinality of H is 6",
    "¬Q: H is a subgroup of A_4"
]

N_HYP = 2
NEG_Q_INDEX = 2