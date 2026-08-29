import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    try:
        is_group = hasattr(witness, 'is_abelian') and hasattr(witness, 'order') and hasattr(witness, 'center')
        if not is_group:
            h1 = False
        else:
            n = witness.order()
            if not isinstance(n, (int, sympy.Integer)) or n < 1:
                h1 = False
            else:
                p = 1
                while p**3 < n:
                    p += 1
                h1 = bool((not witness.is_abelian) and (p**3 == n))
    except Exception:
        h1 = False

    try:
        is_group = hasattr(witness, 'is_abelian') and hasattr(witness, 'order') and hasattr(witness, 'center')
        if not is_group:
            neg_q = False
        else:
            n = witness.order()
            if not isinstance(n, (int, sympy.Integer)) or n < 1:
                neg_q = False
            else:
                p = 1
                while p**3 < n:
                    p += 1
                if p**3 == n:
                    c_order = len(witness.center())
                    neg_q = bool(c_order != p)
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a non-abelian group of order p^3",
    "¬Q: The center Z(G) does not have order exactly p"
]

N_HYP = 1
NEG_Q_INDEX = 1