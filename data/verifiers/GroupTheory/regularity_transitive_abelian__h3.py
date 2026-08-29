import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H1: G is a finite abelian group
    try:
        h1 = bool(witness.is_abelian)
    except Exception:
        h1 = False

    # H2: G acts faithfully on a set \Omega
    # In sympy, a PermutationGroup acts faithfully on its domain {0, 1, ..., degree-1}
    try:
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    # ¬Q: The action of G on \Omega is not regular
    # A regular action is both transitive and free (stabilizer of any point is trivial).
    # The conclusion fails if the group is not transitive OR if any stabilizer is non-trivial.
    try:
        transitive = witness.is_transitive() if callable(witness.is_transitive) else witness.is_transitive
        free = all(witness.stabilizer(i).order() == 1 for i in range(witness.degree))
        neg_q = not (transitive and free)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite abelian group",
    "H_2: G acts faithfully on a set \\Omega",
    "¬Q: The action of G on \\Omega is not regular"
]

N_HYP = 2
NEG_Q_INDEX = 2