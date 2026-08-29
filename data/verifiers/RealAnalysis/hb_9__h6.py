import sympy
from sympy import Interval, FiniteSet, Union, Intersection, oo, S, ProductSet

Reals = S.Reals
Integers = S.Integers
Naturals = S.Naturals

def is_subset_Rn(S_obj):
    try:
        if S_obj.is_subset(sympy.S.Reals):
            return True
        if isinstance(S_obj, sympy.ProductSet):
            return all(is_subset_Rn(arg) for arg in S_obj.args)
        if isinstance(S_obj, sympy.FiniteSet):
            for elem in S_obj:
                if isinstance(elem, (tuple, sympy.Tuple)):
                    if not all(sympy.sympify(e).is_real for e in elem):
                        return False
                else:
                    if not sympy.sympify(elem).is_real:
                        return False
            return True
        if isinstance(S_obj, sympy.Union) or isinstance(S_obj, sympy.Intersection):
            return all(is_subset_Rn(arg) for arg in S_obj.args)
    except Exception:
        pass
    return False

def is_closed(S_obj):
    try:
        if isinstance(S_obj, sympy.FiniteSet):
            return True
        if isinstance(S_obj, sympy.ProductSet):
            return all(is_closed(arg) for arg in S_obj.args)
        if isinstance(S_obj, sympy.Union) or isinstance(S_obj, sympy.Intersection):
            return all(is_closed(arg) for arg in S_obj.args)
        return S_obj.closure == S_obj
    except Exception:
        return False

def is_bounded(S_obj):
    try:
        if S_obj.is_empty:
            return True
        if isinstance(S_obj, sympy.FiniteSet):
            return True
        if isinstance(S_obj, sympy.ProductSet):
            return all(is_bounded(arg) for arg in S_obj.args)
        if isinstance(S_obj, sympy.Union):
            return all(is_bounded(arg) for arg in S_obj.args)
        if isinstance(S_obj, sympy.Intersection):
            return any(is_bounded(arg) for arg in S_obj.args)
        return S_obj.inf.is_finite and S_obj.sup.is_finite
    except Exception:
        return False

def distance_zero(K, C):
    try:
        if K.intersect(C).is_empty is False:
            return True
    except Exception:
        pass
    try:
        if K.closure.intersect(C.closure).is_empty is False:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False] * 6
        K, C = witness
    except Exception:
        return [False] * 6

    try:
        h1 = bool(is_subset_Rn(K) and is_subset_Rn(C))
    except Exception:
        h1 = False

    try:
        h2 = bool(K.is_empty is False)
    except Exception:
        h2 = False

    try:
        h3 = bool(is_closed(K) and is_bounded(K))
    except Exception:
        h3 = False

    try:
        h4 = bool(C.is_empty is False)
    except Exception:
        h4 = False

    try:
        h5 = bool(is_closed(C))
    except Exception:
        h5 = False

    try:
        neg_q = bool(distance_zero(K, C))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: K and C are subsets of R^n",
    "H_2: K is non-empty",
    "H_3: K is compact",
    "H_4: C is non-empty",
    "H_5: C is closed",
    "¬Q: Distance between K and C is 0"
]

N_HYP = 5
NEG_Q_INDEX = 5