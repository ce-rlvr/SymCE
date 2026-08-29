import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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
    if isinstance(witness, tuple) and len(witness) > 0:
        witness = witness[0]

    # H1: X is a non-empty set
    try:
        h1 = hasattr(witness, 'degree') and witness.degree > 0
    except Exception:
        h1 = False

    # H2: G acts on X
    try:
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    # H3: The action of G on X is faithful
    try:
        # A PermutationGroup acts faithfully on its domain by definition.
        h3 = isinstance(witness, PermutationGroup)
    except Exception:
        h3 = False

    # H4: The action of G on X is transitive
    try:
        if callable(witness.is_transitive):
            transitive = witness.is_transitive()
        else:
            transitive = witness.is_transitive
        h4 = bool(transitive)
    except Exception:
        h4 = False

    # neg_Q: The action of G on X is NOT regular
    try:
        if callable(witness.is_transitive):
            transitive = witness.is_transitive()
        else:
            transitive = witness.is_transitive
            
        if not transitive:
            is_regular = False
        else:
            order = witness.order() if callable(witness.order) else witness.order
            # By the Orbit-Stabilizer Theorem, a transitive action is regular
            # if and only if the order of the group equals the size of the domain.
            is_regular = (order == witness.degree)
            
        neg_q = not is_regular
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: X is a non-empty set",
    "H_2: G acts on X",
    "H_3: The action of G on X is faithful",
    "H_4: The action of G on X is transitive",
    "¬Q: The action of G on X is not regular"
]

N_HYP = 4
NEG_Q_INDEX = 4