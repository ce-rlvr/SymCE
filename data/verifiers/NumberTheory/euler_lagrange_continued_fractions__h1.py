import sympy
from sympy import minpoly, degree, continued_fraction_periodic

# Standard linear algebra objects
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Check if the witness is a counterexample to the conjecture:
    "The continued fraction expansion of x is eventually periodic if and only if 
    x is an irrational root of a quadratic polynomial with integer coefficients"
    """
    # Evaluate LHS: The continued fraction expansion of x is eventually periodic
    try:
        # continued_fraction_periodic returns (preperiod, period)
        # For rational numbers, period is empty (finite continued fraction).
        # For quadratic irrationals, period is non-empty.
        # For non-real numbers or others, it raises an exception.
        pre, per = continued_fraction_periodic(witness)
        lhs = len(per) > 0
    except Exception:
        lhs = False
        
    # Evaluate RHS: x is an irrational root of a quadratic polynomial with integer coefficients
    try:
        # It must not be rational
        if witness.is_rational:
            rhs = False
        else:
            # It must be a root of a quadratic polynomial with integer coefficients.
            # This is equivalent to its minimal polynomial over Q having degree 2.
            p = minpoly(witness)
            rhs = (degree(p) == 2)
    except Exception:
        rhs = False
        
    # The conclusion fails if LHS and RHS do not match
    neg_q = (lhs != rhs)
    
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The continued fraction expansion of x is eventually periodic iff x is an irrational root of a quadratic polynomial with integer coefficients"
]

N_HYP = 0
NEG_Q_INDEX = 0