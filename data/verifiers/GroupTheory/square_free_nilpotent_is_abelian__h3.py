import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _eval_prop(obj, prop):
    attr = getattr(obj, prop)
    if callable(attr):
        return attr()
    return attr

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = bool(_eval_prop(witness, 'is_nilpotent'))
    except Exception:
        h2 = False

    try:
        neg_q = not bool(_eval_prop(witness, 'is_abelian'))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a nilpotent group",
    "¬Q: G is not an abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2