import math
import sympy
from sympy import symbols, Rational, Integer

# Top-level setup
# Number theory: no named bindings needed; use integers directly

def conditions(witness) -> list[bool]:
    try:
        a, k, m = witness
    except Exception:
        return [False, False]
        
    try:
        if not isinstance(a, (int, sympy.Integer)) or not isinstance(k, (int, sympy.Integer)) or not isinstance(m, (int, sympy.Integer)):
            h1 = False
        else:
            a, k, m = int(a), int(k), int(m)
            if k > 10000 or k < -10000:
                h1 = False
            elif k < 0:
                if a == 1:
                    h1 = (m == 2)
                elif a == -1:
                    h1 = (m == (2 if k % 2 == 0 else 0))
                else:
                    h1 = False
            else:
                h1 = (m == a**k + 1)
    except Exception:
        h1 = False
        
    try:
        if not isinstance(a, (int, sympy.Integer)) or not isinstance(k, (int, sympy.Integer)) or not isinstance(m, (int, sympy.Integer)):
            neg_q = False
        else:
            a, k, m = int(a), int(k), int(m)
            if m == 0:
                neg_q = True
            elif math.gcd(a, m) != 1:
                neg_q = True
            else:
                inv_a = pow(a, -1, m)
                val = -pow(a, k - 1, m)
                neg_q = (inv_a % abs(m)) != (val % abs(m))
    except Exception:
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m = a^k + 1",
    "¬Q: The modular inverse of a modulo m is NOT congruent to -a^{k-1} (mod m)"
]

N_HYP = 1
NEG_Q_INDEX = 1