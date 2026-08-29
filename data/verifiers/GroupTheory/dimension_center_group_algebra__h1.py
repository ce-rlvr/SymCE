import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import FreeGroup, FpGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        h1 = False
        if hasattr(witness, 'generators') or type(witness).__name__ in ('PermutationGroup', 'FreeGroup', 'FpGroup'):
            h1 = True
    except Exception:
        h1 = False

    try:
        h2 = h1
    except Exception:
        h2 = False

    try:
        neg_q = False
        t_name = type(witness).__name__
        if t_name == 'FreeGroup':
            neg_q = len(witness.generators) > 1
        elif t_name == 'FpGroup':
            if len(witness.relators) == 0 and len(witness.generators) > 1:
                neg_q = True
        elif t_name == 'PermutationGroup':
            neg_q = False
        else:
            if hasattr(witness, 'is_finite') and not witness.is_finite:
                if hasattr(witness, 'is_abelian') and not witness.is_abelian:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: C(G) is the group algebra of G over the complex numbers",
    "H_2: Z(C(G)) is the center of C(G)",
    "¬Q: The dimension of Z(C(G)) as a complex vector space is not exactly equal to the number of conjugacy classes of G"
]

N_HYP = 2
NEG_Q_INDEX = 2