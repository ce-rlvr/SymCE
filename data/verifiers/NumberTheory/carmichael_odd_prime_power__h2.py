import sympy
from sympy.ntheory import reduced_totient

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: lambda(n) denotes the Carmichael function (and k is an integer)",
    "¬Q: lambda(p^k) != p^{k-1}(p-1)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            k = witness.get('k')
        else:
            p, k = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(isinstance(p, (int, sympy.Integer)) and sympy.isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False
        
    try:
        h2 = bool(isinstance(k, (int, sympy.Integer)))
    except Exception:
        h2 = False
        
    try:
        if k < 0:
            neg_q = True
        else:
            val1 = reduced_totient(p**k)
            if k - 1 < 0:
                val2 = sympy.Rational(p - 1, p**(1 - k))
            else:
                val2 = p**(k - 1) * (p - 1)
            neg_q = bool(val1 != val2)
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]