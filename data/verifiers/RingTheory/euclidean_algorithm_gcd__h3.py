import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup
# ZZ and QQ are provided as standard Euclidean domains.
# x, y, z are provided for polynomial rings.

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            R, a, b, r = witness
        elif len(witness) == 3:
            R = ZZ
            a, b, r = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: R is a Euclidean domain
    try:
        h1 = False
        if hasattr(R, 'gcd') and hasattr(R, 'div'):
            is_pid = getattr(R, 'is_PID', False)
            is_field = getattr(R, 'is_Field', False)
            is_poly_over_field = False
            if hasattr(R, 'domain') and getattr(R.domain, 'is_Field', False):
                if hasattr(R, 'gens') and len(R.gens) == 1:
                    is_poly_over_field = True
            if is_pid or R == ZZ or is_field or is_poly_over_field:
                h1 = True
    except Exception:
        h1 = False
        
    # H_2: a and b are non-zero elements of R
    try:
        h2 = False
        if a in R and b in R:
            if a != R.zero and b != R.zero:
                h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: r is not a greatest common divisor of a and b
    try:
        def is_gcd(r, a, b, R):
            if r not in R:
                return False
            try:
                _, rem_a = R.div(a, r)
                if rem_a != R.zero:
                    return False
                _, rem_b = R.div(b, r)
                if rem_b != R.zero:
                    return False
                g = R.gcd(a, b)
                _, rem_r = R.div(r, g)
                if rem_r != R.zero:
                    return False
                return True
            except ZeroDivisionError:
                return False
            except Exception:
                return False
                
        neg_q = not is_gcd(r, a, b, R)
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: a and b are non-zero elements of R",
    "¬Q: r is not a greatest common divisor of a and b"
]

N_HYP = 2
NEG_Q_INDEX = 2