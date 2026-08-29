import sympy
from sympy import Interval, oo, FiniteSet, Union, Intersection, ProductSet, S

Reals = S.Reals
Integers = S.Integers
Naturals = S.Naturals
R2 = ProductSet(Reals, Reals)
R3 = ProductSet(Reals, Reals, Reals)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, sympy.sets.Set):
            return [False]
        
        def is_bounded(s):
            if s == sympy.S.EmptySet:
                return True
            if isinstance(s, sympy.FiniteSet):
                return True
            if isinstance(s, sympy.Union):
                return all(is_bounded(arg) for arg in s.args)
            if isinstance(s, sympy.Intersection):
                return any(is_bounded(arg) for arg in s.args)
            if isinstance(s, sympy.ProductSet):
                return all(is_bounded(arg) for arg in s.args)
            if hasattr(s, 'inf') and hasattr(s, 'sup'):
                return s.inf.is_finite and s.sup.is_finite
            return False
            
        neg_q = not is_bounded(witness)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The closure of S is not a compact subset of R^n"
]

N_HYP = 0
NEG_Q_INDEX = 0