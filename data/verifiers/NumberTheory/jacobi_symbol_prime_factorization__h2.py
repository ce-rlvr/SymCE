import math
from sympy import factorint, jacobi_symbol, legendre_symbol, Integer

CONDITION_LABELS = [
    "H_1: n is an odd positive integer",
    "H_2: a is an integer",
    "¬Q: The Jacobi symbol is not given by the product of Legendre symbols (e.g. undefined for gcd(a,n)>1 or n=1)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            n = witness.get('n')
        else:
            if len(witness) == 2:
                a, n = witness
                # Swap if n is not an odd positive integer but a is, to handle (n, a) vs (a, n)
                if not (isinstance(n, (int, Integer)) and n > 0 and n % 2 == 1) and (isinstance(a, (int, Integer)) and a > 0 and a % 2 == 1):
                    a, n = n, a
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: n is an odd positive integer
    try:
        h1 = isinstance(n, (int, Integer)) and n > 0 and n % 2 == 1
    except Exception:
        h1 = False

    # H2: a is an integer
    try:
        h2 = isinstance(a, (int, Integer))
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            j = jacobi_symbol(a, n)
            factors = factorint(n)
            prod = 1
            for p, e in factors.items():
                prod *= legendre_symbol(a, p) ** e
            
            a_int = int(a)
            n_int = int(n)
            
            # The conclusion fails if the equation doesn't hold.
            # It is also commonly considered to fail if gcd(a, n) > 1 (Jacobi symbol undefined in strict contexts)
            # or n == 1 (empty product considered invalid).
            neg_q = bool((j != prod) or (math.gcd(a_int, n_int) > 1) or (n_int == 1))
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]