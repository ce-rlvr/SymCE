import sympy
from sympy.ntheory import n_order

def conditions(witness):
    try:
        a, p = witness
    except Exception:
        return [False, False, False]
        
    # H1: a is an integer coprime to p
    try:
        a = int(a)
        p = int(p)
        h1 = sympy.gcd(a, p) == 1
    except Exception:
        h1 = False
        
    # H2: a^{p-1} == 1 (mod p^2)
    try:
        if p - 1 < 0:
            inv_a = sympy.mod_inverse(a, p**2)
            h2 = pow(inv_a, -(p - 1), p**2) == 1
        else:
            h2 = pow(a, p - 1, p**2) == 1
    except Exception:
        h2 = False
        
    # neg_Q: The multiplicative order of a modulo p^2 is NOT equal to the multiplicative order of a modulo p
    try:
        def safe_order(base, mod):
            mod = abs(int(mod))
            if mod == 1:
                return 1
            return n_order(base, mod)
            
        order_p = safe_order(a, p)
        order_p2 = safe_order(a, p**2)
        neg_q = order_p != order_p2
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer coprime to p",
    "H_2: a^{p-1} == 1 (mod p^2)",
    "¬Q: The multiplicative order of a modulo p^2 is not equal to the multiplicative order of a modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2