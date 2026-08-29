import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Interval, Union, FiniteSet, ImageSet, ProductSet, S
import math
import itertools
import functools

# Standard algebra objects
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

def is_bounded(witness):
    if isinstance(witness, (list, tuple, set)):
        return True
    try:
        if hasattr(witness, 'is_bounded'):
            val = witness.is_bounded() if callable(witness.is_bounded) else witness.is_bounded
            if val is not None:
                return bool(val)
    except Exception:
        pass
    try:
        if witness.is_finite is True:
            return True
    except Exception:
        pass
    try:
        if witness.inf.is_finite and witness.sup.is_finite:
            return True
    except Exception:
        pass
    return False

def is_infinite(witness):
    if isinstance(witness, (list, tuple, set)):
        return False
    try:
        if hasattr(witness, 'is_infinite'):
            val = witness.is_infinite() if callable(witness.is_infinite) else witness.is_infinite
            if val is not None:
                return bool(val)
    except Exception:
        pass
    try:
        if hasattr(witness, 'is_finite'):
            val = witness.is_finite() if callable(witness.is_finite) else witness.is_finite
            if val is not None:
                return not bool(val)
    except Exception:
        pass
    return False

def has_limit_point_in_Rn(witness):
    try:
        if hasattr(witness, 'has_limit_point_in_Rn'):
            val = witness.has_limit_point_in_Rn() if callable(witness.has_limit_point_in_Rn) else witness.has_limit_point_in_Rn
            if val is not None:
                return bool(val)
    except Exception:
        pass
    
    # Fallback for SymPy sets
    try:
        if witness.is_subset(sympy.S.Reals):
            if witness.is_bounded and witness.is_finite is False:
                return True
            try:
                if not witness.measure.is_zero:
                    return True
            except Exception:
                pass
            if witness in (sympy.S.Reals, sympy.S.Rationals):
                return True
    except Exception:
        pass
    try:
        if isinstance(witness, sympy.ProductSet):
            if all(arg.is_subset(sympy.S.Reals) for arg in witness.args):
                if witness.is_bounded and witness.is_finite is False:
                    return True
    except Exception:
        pass
        
    return False

def conditions(witness):
    try:
        h1 = bool(is_bounded(witness))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_infinite(witness))
    except Exception:
        h2 = False

    try:
        neg_q = not bool(has_limit_point_in_Rn(witness))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is bounded",
    "H_2: S contains infinitely many points",
    "¬Q: S has no limit point in R^n"
]

N_HYP = 2
NEG_Q_INDEX = 2