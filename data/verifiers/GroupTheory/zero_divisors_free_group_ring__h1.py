import sympy
from sympy import oo
from sympy.combinatorics import PermutationGroup, FpGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: The ring is the group ring of F over K",
    "¬Q: The group ring has non-zero zero divisors"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) >= 2:
                K = witness[0]
                F = witness[1]
            else:
                K = sympy.QQ
                F = witness[0]
        else:
            K = sympy.QQ
            F = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = False
        if hasattr(K, 'is_Field') and getattr(K, 'is_Field'):
            h1 = True
        elif hasattr(K, 'is_field') and getattr(K, 'is_field'):
            h1 = True
        elif K in [sympy.QQ, sympy.RR, sympy.CC]:
            h1 = True
        elif hasattr(K, '__class__') and 'Field' in K.__class__.__name__:
            h1 = True
    except Exception:
        h1 = False

    try:
        h2 = isinstance(F, (PermutationGroup, FpGroup))
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h2:
            order = F.order()
            if order != oo and order > 1:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]