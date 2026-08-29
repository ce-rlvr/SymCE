import sympy
import math
from sympy.ntheory import continued_fraction_iterator

def conditions(witness) -> list[bool]:
    # H_1: x in (0, 1)
    try:
        val = float(witness)
        h1 = bool(0 < val < 1)
    except Exception:
        try:
            h1 = bool(witness > 0 and witness < 1)
        except Exception:
            h1 = False

    # H_2: x is an irrational number
    try:
        if witness.is_irrational is True:
            h2 = True
        elif witness.is_rational is False and witness.is_real is True:
            h2 = True
        else:
            from sympy import minpoly, degree
            p = minpoly(witness)
            if degree(p) > 1:
                h2 = True
            else:
                h2 = False
    except Exception:
        h2 = False

    # neg_Q: limit is not exactly 6*ln(2)*ln(10)/pi^2
    neg_q = False
    try:
        is_quad = False
        try:
            from sympy import minpoly, degree
            if witness.is_rational is False:
                p = minpoly(witness)
                if degree(p) == 2:
                    is_quad = True
        except Exception:
            pass
            
        if is_quad:
            # Quadratic irrationals have a limit that is algebraically independent 
            # from Levy's constant, so it can never be exactly equal.
            neg_q = True
        else:
            # For other numbers, we approximate the limit of ln(q_k)/k
            # which corresponds to Levy's constant pi^2 / (12 * ln(2))
            levy = math.pi**2 / (12 * math.log(2))
            cf_iter = continued_fraction_iterator(witness)
            q_prev = 0
            q_curr = 1
            k = 0
            for a in cf_iter:
                q_next = a * q_curr + q_prev
                q_prev = q_curr
                q_curr = q_next
                k += 1
                if k == 400:
                    break
            
            if k < 50:
                # Rational numbers or numbers with very short continued fractions
                neg_q = True
            else:
                val = math.log(q_curr) / k
                # If the limit is far from Levy's constant, it's a counterexample
                if abs(val - levy) > 0.15:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is in the interval (0, 1)",
    "H_2: x is an irrational number",
    "¬Q: The limit lim_{n->inf} k(n,x)/n is not exactly 6*ln(2)*ln(10)/pi^2"
]

N_HYP = 2
NEG_Q_INDEX = 2