import sympy
from sympy import S, Interval, Union, Intersection, FiniteSet, oo

# Top-level setup for the namespace
# (No specific named groups or matrices are needed for this Real Analysis conjecture)

def is_subset_of_reals(s):
    if not isinstance(s, sympy.Set):
        return False
    try:
        if s.is_subset(S.Reals):
            return True
    except Exception:
        pass
    if s in (S.Reals, S.Integers, S.Naturals, S.Naturals0, S.EmptySet):
        return True
    if isinstance(s, Interval):
        return True
    if isinstance(s, Union) or isinstance(s, Intersection):
        return all(is_subset_of_reals(arg) for arg in s.args)
    if isinstance(s, FiniteSet):
        return all(getattr(arg, 'is_real', False) for arg in s.args)
    return False

def is_closed(s):
    if not isinstance(s, sympy.Set):
        return False
    try:
        if hasattr(s, 'is_closed') and s.is_closed is not None:
            return s.is_closed
    except Exception:
        pass
    if s in (S.Reals, S.Integers, S.Naturals, S.Naturals0, S.EmptySet):
        return True
    if isinstance(s, Interval):
        left_closed = (not s.left_open) or (s.start == -oo)
        right_closed = (not s.right_open) or (s.end == oo)
        return left_closed and right_closed
    if isinstance(s, Union):
        return all(is_closed(arg) for arg in s.args)
    if isinstance(s, Intersection):
        if all(is_closed(arg) for arg in s.args):
            return True
    if isinstance(s, FiniteSet):
        return True
    try:
        if s.boundary.is_subset(s):
            return True
    except Exception:
        pass
    return False

def is_bounded(s):
    if not isinstance(s, sympy.Set):
        return False
    try:
        if hasattr(s, 'is_bounded') and s.is_bounded is not None:
            return s.is_bounded
    except Exception:
        pass
    try:
        inf = s.inf
        sup = s.sup
        if inf == -oo or sup == oo:
            return False
        if getattr(inf, 'is_real', False) and getattr(sup, 'is_real', False):
            return True
    except Exception:
        pass
    if s in (S.Reals, S.Integers, S.Naturals, S.Naturals0):
        return False
    if s == S.EmptySet:
        return True
    if isinstance(s, Interval):
        return s.start != -oo and s.end != oo
    if isinstance(s, Union):
        return all(is_bounded(arg) for arg in s.args)
    if isinstance(s, Intersection):
        return any(is_bounded(arg) for arg in s.args)
    if isinstance(s, FiniteSet):
        return True
    return False

def conditions(witness) -> list[bool]:
    # H_1: S is a subset of the real numbers
    try:
        h1 = is_subset_of_reals(witness)
    except Exception:
        h1 = False

    # H_2: S is a closed set
    try:
        h2 = is_closed(witness)
    except Exception:
        h2 = False

    # ¬Q: S is not compact
    # In R, a set is compact if and only if it is closed and bounded.
    # Since H_2 requires the set to be closed, failing to be compact means it is not bounded.
    try:
        neg_q = not (is_closed(witness) and is_bounded(witness))
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: S is a subset of the real numbers",
    "H_2: S is a closed set",
    "¬Q: S is not compact (every open cover has a finite subcover fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2