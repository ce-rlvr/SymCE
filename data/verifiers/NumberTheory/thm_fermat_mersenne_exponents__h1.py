import sympy
import math
from sympy import isprime

def conditions(witness):
    n = witness
    
    # H_1: 2^n - 1 is a prime number
    try:
        val = 2**n - 1
        if hasattr(val, 'simplify'):
            val = val.simplify()
            
        h1 = False
        if hasattr(val, 'is_Integer') and val.is_Integer:
            h1 = isprime(int(val))
        elif isinstance(val, int):
            h1 = isprime(val)
        else:
            try:
                val_f = float(val)
                if val_f.is_integer() or abs(round(val_f) - val_f) < 1e-12:
                    h1 = isprime(int(round(val_f)))
            except Exception:
                pass
    except Exception:
        h1 = False

    # ¬Q: n is not a prime number
    try:
        if hasattr(n, 'simplify'):
            n_simp = n.simplify()
        else:
            n_simp = n
            
        q = False
        if hasattr(n_simp, 'is_Integer') and n_simp.is_Integer:
            q = isprime(int(n_simp))
        elif isinstance(n_simp, int):
            q = isprime(n_simp)
        else:
            try:
                n_f = float(n_simp)
                if n_f.is_integer() or abs(round(n_f) - n_f) < 1e-12:
                    q = isprime(int(round(n_f)))
            except Exception:
                pass
        neg_q = not q
    except Exception:
        # If n cannot be evaluated as a prime, it is not a prime number.
        neg_q = True

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: 2^n - 1 is a prime number",
    "¬Q: n is not a prime number"
]

N_HYP = 1
NEG_Q_INDEX = 1