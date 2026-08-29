import sympy
from sympy.ntheory import factorint
from sympy import Rational, Integer, Symbol
from sympy.abc import x

def conditions(witness):
    try:
        # Witness should be a tuple (q, n)
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        q, n = witness
    except Exception:
        return [False, False]

    # H_1: F_q is a finite field with q elements (q is a prime power) and n is a non-negative integer
    try:
        h1 = False
        if isinstance(q, (int, Integer)) and q >= 2 and isinstance(n, (int, Integer)) and n >= 0:
            factors = factorint(int(q))
            if len(factors) == 1:
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: The number of monic square-free polynomials of degree n is NOT exactly q^n - q^{n-1}
    try:
        q_int = int(q)
        n_int = int(n)
        
        # The actual number of monic square-free polynomials of degree n over F_q is:
        # 1 if n = 0
        # q if n = 1
        # q^n - q^{n-1} if n >= 2
        if n_int == 0:
            actual_count = 1
            formula = 1 - Rational(1, q_int)
        elif n_int == 1:
            actual_count = q_int
            formula = q_int - 1
        else:
            actual_count = q_int**n_int - q_int**(n_int - 1)
            formula = q_int**n_int - q_int**(n_int - 1)
            
        neg_q = (actual_count != formula)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements and n is a non-negative integer",
    "¬Q: The number of monic square-free polynomials of degree n is not exactly q^n - q^{n-1}"
]

N_HYP = 1
NEG_Q_INDEX = 1