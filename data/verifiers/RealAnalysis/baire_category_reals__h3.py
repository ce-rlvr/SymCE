import sympy
from sympy import Interval, Union, Intersection, Complement, S, Set

# Standard bindings for real analysis
Reals = S.Reals
EmptySet = S.EmptySet

def is_subset_reals(s):
    try:
        res = s.is_subset(S.Reals)
        if res is True:
            return True
        if res is False:
            return False
    except Exception:
        pass
    if isinstance(s, Interval):
        return True
    if isinstance(s, Union) or isinstance(s, Intersection):
        return all(is_subset_reals(arg) for arg in s.args)
    if s == S.Reals or s == S.EmptySet:
        return True
    return False

def is_open(s):
    try:
        if hasattr(s, 'is_open'):
            res = s.is_open
            if res is True:
                return True
            if res is False:
                return False
    except Exception:
        pass
    if s == S.Reals or s == S.EmptySet:
        return True
    if isinstance(s, Interval):
        return bool(s.left_open and s.right_open)
    if isinstance(s, Union) or isinstance(s, Intersection):
        # Finite union or intersection of open sets is open
        return all(is_open(arg) for arg in s.args)
    return False

def get_closure(s):
    try:
        if hasattr(s, 'closure') and s.closure is not None:
            return s.closure
    except Exception:
        pass
    if s == S.Reals:
        return S.Reals
    if s == S.EmptySet:
        return S.EmptySet
    if isinstance(s, Interval):
        left_open = True if s.start == S.NegativeInfinity else False
        right_open = True if s.end == S.Infinity else False
        return Interval(s.start, s.end, left_open, right_open)
    if isinstance(s, Union):
        return Union(*[get_closure(arg) for arg in s.args])
    if isinstance(s, Intersection):
        return Intersection(*[get_closure(arg) for arg in s.args])
    return s

def conditions(witness) -> list[bool]:
    # H_1: {U_n} is a countable collection of subsets of the real numbers
    try:
        h1 = isinstance(witness, (list, tuple, set)) and len(witness) > 0 and all(isinstance(s, Set) for s in witness)
        if h1:
            for s in witness:
                if not is_subset_reals(s):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: Every set U_n is open
    try:
        h2 = h1 and all(is_open(s) for s in witness)
    except Exception:
        h2 = False

    # ¬Q: The intersection of all U_n is NOT dense in the real numbers
    try:
        if h1:
            inter = Intersection(*witness)
            clos = get_closure(inter)
            neg_q = (clos != S.Reals)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: {U_n} is a countable collection of subsets of the real numbers",
    "H_2: Every set U_n is open",
    "¬Q: The intersection of all U_n is not dense in the real numbers"
]

N_HYP = 2
NEG_Q_INDEX = 2