import sympy
from sympy import minpoly, degree

# Top-level setup
# No specific named bindings needed for this Number Theory conjecture.

def conditions(witness):
    try:
        w = sympy.sympify(witness)
        # The witness must be a number (not a matrix, symbol, etc.)
        if not w.is_number:
            return [False]
    except Exception:
        return [False]
        
    try:
        # Evaluate RHS: x is a quadratic irrational
        # A quadratic irrational is an algebraic number of degree 2 over Q.
        if w.is_rational:
            rhs = False
        else:
            p = minpoly(w)
            rhs = (degree(p) == 2)
    except Exception:
        rhs = False

    try:
        # Evaluate LHS: The simple continued fraction expansion of x is eventually periodic
        # A simple continued fraction is eventually periodic iff x is a REAL quadratic irrational.
        # If x is not real, it does not have a standard simple continued fraction expansion,
        # so it cannot be eventually periodic.
        is_real = w.is_real
        if is_real is None:
            is_real = w.evalf(chop=True).is_real
            
        if is_real is False:
            lhs = False
        elif w.is_rational:
            lhs = False
        else:
            p = minpoly(w)
            lhs = (degree(p) == 2)
    except Exception:
        lhs = False

    try:
        # The conclusion is the equivalence LHS <-> RHS.
        # The negated conclusion is that this equivalence fails.
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
    
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The equivalence (eventually periodic CF <-> quadratic irrational) fails"
]
N_HYP = 0
NEG_Q_INDEX = 0