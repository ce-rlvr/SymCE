import math
from sympy.ntheory import factorint
import sympy
from sympy import Rational, Integer
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        q, n = witness
    except Exception:
        return [False, False, False]
        
    # H_1: q is a prime power (size of a finite field)
    try:
        q_int = int(q)
        if q_int == q and q_int >= 2:
            factors = factorint(q_int)
            h1 = (len(factors) == 1)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: n is a non-negative integer (f(x) = x^n in F_q[x])
    try:
        n_int = int(n)
        h2 = (n_int == n) and (n_int >= 0)
    except Exception:
        h2 = False
        
    # ¬Q: The conclusion fails
    try:
        q_int = int(q)
        n_int = int(n)
        
        # In any finite field F_q, the polynomial f(x) = x^n induces a bijection
        # if and only if n > 0 and gcd(n, q - 1) == 1.
        # (If n = 0, f(x) = 1 for all x, which is not a bijection since q >= 2).
        is_bijection = (n_int > 0 and math.gcd(n_int, q_int - 1) == 1)
        
        # The conjecture claims it is a bijection if and only if gcd(n, q - 1) == 1.
        claimed_iff = (math.gcd(n_int, q_int - 1) == 1)
        
        q_holds = (is_bijection == claimed_iff)
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: q is a prime power (size of a finite field)",
    "H_2: n is a non-negative integer",
    "¬Q: The conclusion 'f(x) induces a bijection iff gcd(n, q-1) = 1' fails"
]

N_HYP = 2
NEG_Q_INDEX = 2