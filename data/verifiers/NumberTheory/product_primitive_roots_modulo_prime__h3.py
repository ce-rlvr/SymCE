import sympy
from sympy.ntheory import isprime, totient
from sympy.ntheory.residue_ntheory import primitive_root

def conditions(witness):
    try:
        p_sym = sympy.sympify(witness)
        if not getattr(p_sym, 'is_integer', False):
            return [False, False, False]
        p = int(p_sym)
    except Exception:
        return [False, False, False]
    
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H_2: p > 3
    try:
        h2 = bool(p > 3)
    except Exception:
        h2 = False
        
    # neg_Q: P != 1 (mod p)
    try:
        if not h1:
            neg_q = False
        else:
            if p == 2:
                P_mod = 1
            else:
                g = int(primitive_root(p))
                exponent = int(((p - 1) // 2) * totient(p - 1))
                P_mod = pow(g, exponent, p)
            neg_q = bool(P_mod != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p > 3",
    "¬Q: Product of primitive roots modulo p is not congruent to 1 mod p"
]

N_HYP = 2
NEG_Q_INDEX = 2