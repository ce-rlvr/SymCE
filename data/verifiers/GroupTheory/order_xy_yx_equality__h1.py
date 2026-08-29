import sympy
from sympy import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools
import z3

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

def is_equal(a, b):
    try:
        res = (a == b)
        if isinstance(res, bool):
            return res
        return bool(res)
    except Exception:
        return False

def get_order(elem, max_order=1000):
    if hasattr(elem, 'order') and callable(elem.order):
        try:
            o = elem.order()
            if o is not None and o != float('inf'):
                return int(o)
        except Exception:
            pass
            
    I = None
    try:
        if hasattr(elem, 'is_Matrix') and elem.is_Matrix:
            if elem.rows != elem.cols:
                return None
            I = eye(elem.rows)
        else:
            I = elem ** 0
    except Exception:
        pass

    curr = elem
    for i in range(1, max_order + 1):
        if I is not None:
            if is_equal(curr, I):
                return i
        
        if is_equal(curr, 1) or is_equal(curr, sympy.S.One):
            return i
            
        try:
            if hasattr(curr, 'is_identity') and curr.is_identity:
                return i
        except Exception:
            pass

        try:
            curr = curr * elem
        except Exception:
            break

    return None

def conditions(witness):
    try:
        x, y = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: x is an element of G
    try:
        # In a valid magma/semigroup/monoid, elements must be composable with themselves
        _ = x * x
        h1 = True
    except Exception:
        h1 = False
        
    # H2: y is an element of G
    try:
        _ = y * y
        # Also ensure x and y belong to the same structure (cross-multiplication is valid)
        _ = x * y
        _ = y * x
        h2 = True
    except Exception:
        h2 = False
        
    # H3: xy has a finite order n
    try:
        xy = x * y
        order_xy = get_order(xy)
        h3 = order_xy is not None
    except Exception:
        h3 = False
        
    # neg_Q: yx does not have finite order n
    try:
        if not h3:
            neg_q = False
        else:
            yx = y * x
            order_yx = get_order(yx)
            # The conclusion fails if yx does not have the SAME finite order n
            neg_q = order_yx != order_xy
    except Exception:
        # If yx cannot be evaluated or its order cannot be determined, it doesn't have finite order n
        neg_q = True
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "H_2: y is an element of G",
    "H_3: the product xy has a finite order n",
    "¬Q: The product yx does not have finite order n"
]

N_HYP = 3
NEG_Q_INDEX = 3