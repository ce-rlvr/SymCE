import sympy
from sympy import Interval, FiniteSet, Union, Intersection, ProductSet, S
from sympy.abc import x, y, z

Reals = S.Reals
EmptySet = S.EmptySet

def is_closed(s):
    if isinstance(s, FiniteSet):
        return True
    if isinstance(s, Interval):
        return not s.left_open and not s.right_open
    if isinstance(s, Union):
        return all(is_closed(arg) for arg in s.args)
    if isinstance(s, Intersection):
        return all(is_closed(arg) for arg in s.args)
    if isinstance(s, ProductSet):
        return all(is_closed(arg) for arg in s.args)
    if s == S.Reals or s == S.EmptySet:
        return True
    return False

def is_compact(s):
    if not isinstance(s, sympy.Set):
        return False
    if isinstance(s, FiniteSet):
        return True
    if isinstance(s, Interval):
        return not s.left_open and not s.right_open and s.inf.is_finite and s.sup.is_finite
    if isinstance(s, Union):
        return all(is_compact(arg) for arg in s.args)
    if isinstance(s, Intersection):
        return any(is_compact(arg) for arg in s.args)
    if isinstance(s, ProductSet):
        return all(is_compact(arg) for arg in s.args)
    if s == S.EmptySet:
        return True
    return False

def conditions(witness):
    try:
        K, C = witness
        C_list = list(C)
    except Exception:
        return [False, False, False]
    
    # H_1: K is a compact subset of R^d
    try:
        h1 = is_compact(K)
    except Exception:
        h1 = False
        
    # H_2: C is a collection of closed subsets of K
    try:
        if len(C_list) == 0:
            h2 = False
        else:
            h2 = True
            for c in C_list:
                if not is_closed(c):
                    h2 = False
                    break
                if not c.is_subset(K):
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    # neg_Q: The intersection of all sets in C is empty
    try:
        if len(C_list) == 0:
            intersection = K
        else:
            intersection = Intersection(*C_list)
            
        is_emp = intersection.is_empty
        if is_emp is None:
            neg_q = (intersection == S.EmptySet)
        else:
            neg_q = bool(is_emp)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a compact subset of R^d",
    "H_2: C is a collection of closed subsets of K",
    "¬Q: The intersection of all sets in C is empty"
]

N_HYP = 2
NEG_Q_INDEX = 2