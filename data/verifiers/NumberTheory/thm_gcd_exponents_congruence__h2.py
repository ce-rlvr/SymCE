import math
import sympy
from sympy import Rational, Integer, Symbol

# Top-level setup
# No specific named bindings needed for this NumberTheory conjecture.

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness should be a dictionary {'m': m, 'n': n, 'k': k, 'a': a} 
    or a tuple (m, n, k, a).
    """
    try:
        if isinstance(witness, dict):
            m = witness.get('m')
            n = witness.get('n')
            k = witness.get('k')
            a = witness.get('a')
        else:
            m, n, k, a = witness
    except Exception:
        return [False, False, False]
        
    def is_int(x):
        if isinstance(x, int):
            return True
        if hasattr(x, 'is_integer'):
            if callable(x.is_integer):
                return x.is_integer()
            return x.is_integer
        return False
        
    # H_1: m is an integer greater than 1
    try:
        h1 = bool(is_int(m) and m > 1)
    except Exception:
        h1 = False
        
    # H_2: n and k are positive integers such that a^n ≡ 1 (mod m) and a^k ≡ 1 (mod m)
    try:
        h2 = bool(is_int(n) and is_int(k) and n > 0 and k > 0 and 
                  pow(a, n, m) == 1 and pow(a, k, m) == 1)
    except Exception:
        h2 = False
        
    # ¬Q: a^{\gcd(n,k)} ≢ 1 (mod m)
    try:
        g = math.gcd(int(n), int(k))
        neg_q = bool(pow(a, g, m) != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m is an integer greater than 1",
    "H_2: n and k are positive integers such that a^n ≡ 1 (mod m) and a^k ≡ 1 (mod m)",
    "¬Q: a^{\\gcd(n,k)} ≢ 1 (mod m)"
]

N_HYP = 2
NEG_Q_INDEX = 2