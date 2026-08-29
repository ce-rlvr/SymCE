import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: v_p(x) denotes the exponent of p in the prime factorization",
    "H_3: a and b are non-zero elements of R",
    "¬Q: v_p(ab) != v_p(a) + v_p(b)"
]

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                R_val, p, a, b = witness
            elif len(witness) == 3:
                p, a, b = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a unique factorization domain
    # We verify this by checking if the elements belong to Z, which is a known UFD.
    try:
        h1 = isinstance(p, (int, Integer)) and \
             isinstance(a, (int, Integer)) and \
             isinstance(b, (int, Integer))
    except Exception:
        h1 = False

    # H_2: v_p(x) denotes the exponent of p in the prime factorization
    # We require p to be a valid base for valuation (an integer with absolute value > 1).
    try:
        h2 = isinstance(p, (int, Integer)) and abs(int(p)) > 1
    except Exception:
        h2 = False

    # H_3: a and b are non-zero elements of R
    try:
        h3 = isinstance(a, (int, Integer)) and isinstance(b, (int, Integer)) and \
             int(a) != 0 and int(b) != 0
    except Exception:
        h3 = False

    # ¬Q: The valuation map fails to satisfy v_p(ab) = v_p(a) + v_p(b)
    try:
        def v(p_val, x_val):
            p_val = int(p_val)
            x_val = int(x_val)
            if x_val == 0 or abs(p_val) <= 1:
                return 0
            k = 0
            while x_val % (p_val**(k+1)) == 0:
                k += 1
            return k
        
        neg_q = v(p, a * b) != v(p, a) + v(p, b)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]