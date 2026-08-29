import sympy
from sympy import *

def conditions(witness) -> list[bool]:
    try:
        # P(x): The simple continued fraction expansion of x is purely periodic
        # Q(x): x is a quadratic irrational such that x > 1 and its algebraic conjugate x' satisfies -1 < x' < 0
        
        # We need to evaluate P(witness) <=> Q(witness)
        # If the conjecture is FALSE at the witness, P(witness) <=> Q(witness) must be False.
        # So we return `not (P_val == Q_val)`
        
        x = witness
        
        # Check if x is a quadratic irrational
        # A quadratic irrational is an irrational root of a quadratic polynomial with integer coefficients.
        # In sympy, we can check if it's an algebraic number of degree 2.
        try:
            min_poly = minpoly(x)
            is_quad_irr = (min_poly.degree() == 2) and not x.is_rational
        except Exception:
            is_quad_irr = False
            
        # Check if x > 1
        try:
            x_gt_1 = bool(x > 1)
        except Exception:
            x_gt_1 = False
            
        # Check if -1 < x' < 0
        try:
            if is_quad_irr:
                # Find the roots of the minimal polynomial
                roots = solve(min_poly)
                # The algebraic conjugate is the other root
                if len(roots) == 2:
                    if abs(roots[0] - x) < 1e-9:
                        x_prime = roots[1]
                    else:
                        x_prime = roots[0]
                    conj_cond = bool(-1 < x_prime and x_prime < 0)
                else:
                    conj_cond = False
            else:
                conj_cond = False
        except Exception:
            conj_cond = False
            
        Q_val = is_quad_irr and x_gt_1 and conj_cond
        
        # Check if the simple continued fraction of x is purely periodic
        try:
            # We can compute the continued fraction using sympy's continued_fraction_periodic
            # It returns a tuple: (pre_period, period)
            # If it's purely periodic, pre_period is empty.
            cf = continued_fraction_periodic(x)
            if cf is not None:
                pre_period, period = cf
                P_val = (len(pre_period) == 0 and len(period) > 0)
            else:
                P_val = False
        except Exception:
            P_val = False
            
        # The conclusion is P(x) <=> Q(x)
        # We want to return True if the conclusion FAILS (i.e., P_val != Q_val)
        neg_Q = (P_val != Q_val)
        
    except Exception:
        neg_Q = False
        
    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: The simple continued fraction expansion of x is purely periodic if and only if x is a quadratic irrational such that x > 1 and its algebraic conjugate x' satisfies -1 < x' < 0"
]

N_HYP = 0
NEG_Q_INDEX = 0