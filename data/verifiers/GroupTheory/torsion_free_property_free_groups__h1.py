import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness):
    h1, h2, neg_q = False, False, False
    
    if isinstance(witness, tuple) and len(witness) == 2:
        F, x = witness
    else:
        F, x = None, witness

    try:
        if F is not None:
            if hasattr(F, 'contains'):
                h1 = bool(F.contains(x))
            elif hasattr(F, 'elements'):
                h1 = x in list(F.elements)
            elif isinstance(F, (list, tuple, set)):
                h1 = x in F
            else:
                h1 = False
        else:
            h1 = hasattr(x, 'order') or hasattr(x, 'is_Identity')
    except Exception:
        h1 = False

    try:
        if F is not None and hasattr(F, 'identity'):
            h2 = bool(x != F.identity)
        else:
            if hasattr(x, 'is_Identity'):
                h2 = not bool(x.is_Identity)
            elif hasattr(x, 'order'):
                h2 = bool(x.order() != 1)
            else:
                h2 = False
    except Exception:
        h2 = False

    try:
        if hasattr(x, 'order'):
            ord_x = x.order()
            neg_q = (ord_x != sympy.oo) and (ord_x > 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of F",
    "H_2: x is not the identity element of F",
    "¬Q: The element x has finite order"
]

N_HYP = 2
NEG_Q_INDEX = 2