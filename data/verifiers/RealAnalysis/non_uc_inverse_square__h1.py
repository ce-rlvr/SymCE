import sympy
from sympy import Symbol, limit, S, Interval
from sympy.calculus.singularities import singularities

# Top-level setup
x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        f = sympy.sympify(witness)
        
        # A continuous function on (0, 1) is uniformly continuous on (0, 1)
        # if and only if its limits at the endpoints exist and are finite.
        L0 = limit(f, x, 0, dir='+')
        L1 = limit(f, x, 1, dir='-')
        
        if not (L0.is_number and L0.is_real and L0.is_finite):
            neg_q = False
        elif not (L1.is_number and L1.is_real and L1.is_finite):
            neg_q = False
        else:
            try:
                # Check for any singularities strictly inside the interval (0, 1)
                sings = singularities(f, x)
                if sings.intersect(Interval(0, 1, left_open=True, right_open=True)) != S.EmptySet:
                    neg_q = False
                else:
                    neg_q = True
            except Exception:
                # Fallback if singularities cannot be computed
                if f.is_polynomial(x):
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: f is uniformly continuous on (0, 1)"
]

N_HYP = 0
NEG_Q_INDEX = 0