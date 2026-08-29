import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.matrices import *
import math
import itertools
import functools

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Parse witness
    if isinstance(witness, tuple) and len(witness) == 2:
        R, a = witness
    else:
        a = witness
        R = getattr(a, 'ring', getattr(a, 'parent', None))
        if R is None:
            if hasattr(a, 'det'):
                R = 'MatrixRing'
            else:
                R = 'UnknownRing'

    # H1: R is a right Artinian ring
    h1_ok = False
    try:
        if hasattr(R, 'is_right_Artinian'):
            val = R.is_right_Artinian
            h1_ok = bool(val() if callable(val) else val)
        elif hasattr(R, 'is_Artinian'):
            val = R.is_Artinian
            h1_ok = bool(val() if callable(val) else val)
        elif hasattr(R, 'is_Field') and hasattr(R, 'is_Domain'):
            val_f = R.is_Field() if callable(R.is_Field) else R.is_Field
            val_d = R.is_Domain() if callable(R.is_Domain) else R.is_Domain
            if val_f:
                h1_ok = True
            elif val_d:
                h1_ok = False
            else:
                h1_ok = True
        elif str(R) in ['ZZ', 'QQ', 'RR', 'CC']:
            h1_ok = (str(R) != 'ZZ')
        elif hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing:
            h1_ok = False
        elif isinstance(R, (list, tuple, set)):
            h1_ok = True
        elif R == 'MatrixRing':
            h1_ok = True
        elif hasattr(R, 'is_finite'):
            val = R.is_finite
            h1_ok = bool(val() if callable(val) else val)
        else:
            h1_ok = True
    except Exception:
        h1_ok = False

    # H2: a is a regular element
    h2_ok = False
    try:
        if hasattr(a, 'is_regular'):
            val = a.is_regular
            h2_ok = bool(val() if callable(val) else val)
        elif hasattr(R, 'is_Domain'):
            val_d = R.is_Domain() if callable(R.is_Domain) else R.is_Domain
            if val_d:
                h2_ok = (a != 0)
            else:
                h2_ok = True
        elif str(R) in ['ZZ', 'QQ', 'RR', 'CC']:
            h2_ok = (a != 0)
        elif isinstance(R, (list, tuple, set)):
            zero = getattr(R, 'zero', 0)
            is_reg = True
            for x in R:
                if a * x == zero and x != zero:
                    is_reg = False
                    break
                if x * a == zero and x != zero:
                    is_reg = False
                    break
            h2_ok = is_reg
        elif R == 'MatrixRing':
            h2_ok = bool(a.det() != 0)
        else:
            h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: a is not a unit in R
    neg_q = False
    try:
        if hasattr(a, 'is_unit'):
            val = a.is_unit
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(a, 'is_invertible'):
            val = a.is_invertible
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(R, 'is_Field'):
            val_f = R.is_Field() if callable(R.is_Field) else R.is_Field
            if val_f:
                neg_q = (a == 0)
            else:
                neg_q = True
        elif str(R) == 'ZZ':
            neg_q = (a not in [1, -1])
        elif str(R) in ['QQ', 'RR', 'CC']:
            neg_q = (a == 0)
        elif isinstance(R, (list, tuple, set)):
            one = getattr(R, 'one', 1)
            is_u = False
            for x in R:
                if a * x == one and x * a == one:
                    is_u = True
                    break
            neg_q = not is_u
        elif R == 'MatrixRing':
            neg_q = not bool(a.det() != 0)
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "H_2: a is a regular element",
    "¬Q: a is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2