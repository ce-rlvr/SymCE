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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    # H_1: G is an abelian group.
    try:
        h1 = bool(witness.is_abelian)
    except Exception:
        h1 = False

    # H_2: G acts on X.
    try:
        # A PermutationGroup inherently acts on its domain {0, 1, ..., degree-1}
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    # H_3: The action of G on X is faithful.
    try:
        # The natural action of a PermutationGroup on its domain is always faithful.
        h3 = isinstance(witness, PermutationGroup)
    except Exception:
        h3 = False

    # H_4: The action of G on X is transitive.
    try:
        h4 = bool(witness.is_transitive())
    except Exception:
        h4 = False

    # ¬Q: The action of G on X is NOT regular.
    # A regular action is both transitive and free (all point stabilizers are trivial).
    try:
        if not witness.is_transitive():
            neg_q = True
        else:
            # The action is not regular if there is any point with a non-trivial stabilizer.
            neg_q = any(witness.stabilizer(i).order() > 1 for i in range(witness.degree))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: G acts on X",
    "H_3: The action of G on X is faithful",
    "H_4: The action of G on X is transitive",
    "¬Q: The action of G on X is not regular"
]

N_HYP = 4
NEG_Q_INDEX = 4