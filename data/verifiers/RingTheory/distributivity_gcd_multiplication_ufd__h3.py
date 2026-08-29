import sympy
import math
from sympy.abc import x, y, z

def conditions(witness):
    try:
        # The witness should be a tuple (a, b, c, d)
        if len(witness) != 4:
            return [False, False, False]
        a, b, c, d = witness
    except Exception:
        return [False, False, False]
        
    try:
        # H_1: R is a unique factorization domain.
        # We verify that the elements belong to Z or a polynomial ring over a field,
        # both of which are UFDs. We check for integers or sympy expressions.
        h1 = all(isinstance(val, (int, sympy.Integer, sympy.Expr)) for val in (a, b, c, d))
    except Exception:
        h1 = False
        
    try:
        # H_2: a, b, and c are non-zero elements of R.
        h2 = a != 0 and b != 0 and c != 0
    except Exception:
        h2 = False
        
    try:
        # ¬Q: cd is not a greatest common divisor of ca and cb.
        ca = c * a
        cb = c * b
        cd = c * d
        
        # If all elements are integers, we can use exact integer arithmetic.
        if all(isinstance(val, (int, sympy.Integer)) for val in (a, b, c, d)):
            g = math.gcd(int(ca), int(cb))
            # In Z, x is a gcd of y and z iff abs(x) == math.gcd(y, z)
            is_gcd = (abs(int(cd)) == g)
        else:
            # For general sympy expressions (e.g., polynomials)
            g = sympy.gcd(ca, cb)
            if g == 0:
                is_gcd = (cd == 0)
            elif cd == 0:
                is_gcd = False
            else:
                # cd is a gcd iff it associates with the computed gcd g.
                # This means their ratio must be a unit (a non-zero constant).
                ratio = sympy.cancel(cd / g)
                is_gcd = ratio.is_constant() and ratio != 0
                
        neg_q = not is_gcd
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a, b, and c are non-zero elements of R",
    "¬Q: cd is not a greatest common divisor of ca and cb"
]

N_HYP = 2
NEG_Q_INDEX = 2