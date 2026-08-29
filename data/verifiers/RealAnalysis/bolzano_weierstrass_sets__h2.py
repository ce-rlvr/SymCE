import sympy
from sympy import S, Interval, FiniteSet, Union, Intersection, ImageSet, Lambda
from sympy.sets.fancysets import Range

# Top-level setup for witness expressions
Integers = S.Integers
Naturals = S.Naturals
Naturals0 = S.Naturals0
Reals = S.Reals
Rationals = S.Rationals

def conditions(witness) -> list[bool]:
    # H1: S is a subset of the real numbers.
    try:
        if not isinstance(witness, sympy.sets.Set):
            h1 = False
        else:
            h1 = bool(witness.is_subset(S.Reals))
    except Exception:
        h1 = False

    # H2: S is an infinite set.
    try:
        def is_inf(s):
            if s.is_finite is False:
                return True
            if s.is_finite is True:
                return False
            if s in (S.Integers, S.Naturals, S.Naturals0, S.Reals, S.Rationals):
                return True
            if isinstance(s, Interval):
                return s.inf < s.sup
            if isinstance(s, Range):
                return s.size == S.Infinity
            if isinstance(s, ImageSet):
                return is_inf(s.base_set)
            if isinstance(s, Union):
                return any(is_inf(arg) for arg in s.args)
            return False
            
        if not isinstance(witness, sympy.sets.Set):
            h2 = False
        else:
            h2 = is_inf(witness)
    except Exception:
        h2 = False

    # neg_Q: S has NO limit points in the real numbers.
    try:
        def has_limit_points(s):
            if s.is_finite is True:
                return False
            if s in (S.Integers, S.Naturals, S.Naturals0):
                return False
            if isinstance(s, Range):
                return False
            if isinstance(s, Interval):
                return s.inf < s.sup
            if isinstance(s, Union):
                return any(has_limit_points(arg) for arg in s.args)
            if s.is_subset(S.Integers):
                return False
            if isinstance(s, ImageSet):
                base_set = s.base_set
                if base_set in (S.Integers, S.Naturals, S.Naturals0):
                    expr = s.lamda.expr
                    var = s.lamda.variables[0]
                    try:
                        from sympy import poly
                        p = poly(expr, var)
                        if p.degree() >= 1:
                            return False
                    except Exception:
                        pass
            return True
        
        if not isinstance(witness, sympy.sets.Set):
            neg_q = False
        else:
            neg_q = not has_limit_points(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a subset of the real numbers",
    "H_2: S is an infinite set",
    "¬Q: S has no limit points in the real numbers"
]

N_HYP = 2
NEG_Q_INDEX = 2