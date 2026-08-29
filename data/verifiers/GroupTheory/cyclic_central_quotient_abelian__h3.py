import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.perm_groups import PermutationGroup

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
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if h1:
            _ = witness.center()
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1:
            neg_q = not witness.is_abelian
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: G is a group",
    "H_2: Z(G) is the center of G",
    "¬Q: G is not an abelian group"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2