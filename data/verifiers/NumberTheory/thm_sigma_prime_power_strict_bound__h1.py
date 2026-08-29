import sympy
from sympy.ntheory import divisor_sigma

def conditions(witness):
    try:
        p, k = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = (int(k) == k) and (k > 0)
    except Exception:
        h1 = False
        
    try:
        if int(p) != p or int(k) != k:
            neg_q = False
        else:
            p_int = int(p)
            k_int = int(k)
            if p_int == 1:
                neg_q = True
            else:
                val = p_int ** k_int
                if val <= 0:
                    neg_q = False
                else:
                    lhs = divisor_sigma(val)
                    rhs = (p_int ** (k_int + 1)) / (p_int - 1)
                    neg_q = bool(lhs >= rhs)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "¬Q: sigma(p^k) >= p^(k+1) / (p - 1)"
]

N_HYP = 1
NEG_Q_INDEX = 1