import sympy
from sympy import Reals, Interval, Union, Intersection, FiniteSet, ProductSet, EmptySet, oo
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def is_subset_of_Rn(S):
    from sympy import Set, Reals, ProductSet, Union, Intersection
    try:
        if not isinstance(S, Set):
            return False
        if S.is_EmptySet:
            return True
        for n in range(1, 11):
            if S.is_subset(Reals ** n) == True:
                return True
        if S.is_subset(Reals) == True:
            return True
        if isinstance(S, ProductSet):
            return all(is_subset_of_Rn(arg) for arg in S.args)
        if isinstance(S, Union):
            return all(is_subset_of_Rn(arg) for arg in S.args)
        if isinstance(S, Intersection):
            return any(is_subset_of_Rn(arg) for arg in S.args)
        return False
    except Exception:
        return False

def is_bounded(S):
    from sympy import Set, Reals, ProductSet, Union, Intersection, Interval
    try:
        if S.is_EmptySet:
            return True
    except Exception:
        pass
    try:
        if S.is_FiniteSet:
            return True
    except Exception:
        pass
    try:
        if S.is_subset(Reals) == True:
            return S.inf.is_finite and S.sup.is_finite
    except Exception:
        pass
    if isinstance(S, ProductSet):
        try:
            return all(is_bounded(arg) for arg in S.args)
        except Exception:
            pass
    if isinstance(S, Union):
        try:
            return all(is_bounded(arg) for arg in S.args)
        except Exception:
            pass
    if isinstance(S, Intersection):
        try:
            return any(is_bounded(arg) for arg in S.args)
        except Exception:
            pass
    return False

def is_closed(S):
    from sympy import Set, Reals, ProductSet, Union, Intersection, Interval
    try:
        if S.is_EmptySet:
            return True
    except Exception:
        pass
    try:
        bnd = S.boundary
        subset_check = bnd.is_subset(S)
        if subset_check == True:
            return True
        if subset_check == False:
            return False
    except Exception:
        pass
    if isinstance(S, Interval):
        try:
            left_ok = (not S.inf.is_finite) or (not S.left_open)
            right_ok = (not S.sup.is_finite) or (not S.right_open)
            return left_ok and right_ok
        except Exception:
            pass
    if isinstance(S, ProductSet):
        try:
            return all(is_closed(arg) for arg in S.args)
        except Exception:
            pass
    if isinstance(S, Union) or isinstance(S, Intersection):
        try:
            return all(is_closed(arg) for arg in S.args)
        except Exception:
            pass
    return False

def conditions(witness):
    try:
        h1 = is_subset_of_Rn(witness)
    except Exception:
        h1 = False
        
    try:
        closed = is_closed(witness)
        bounded = is_bounded(witness)
        neg_q = not (closed and bounded)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: S is a subset of R^n",
    "¬Q: S is not closed or S is not bounded"
]

N_HYP = 1
NEG_Q_INDEX = 1