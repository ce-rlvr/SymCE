import sympy

def conditions(witness):
    try:
        # The witness should be a tuple (d, p)
        if len(witness) != 2:
            return [False, False]
        d, p = witness
    except Exception:
        return [False, False]
        
    try:
        if not isinstance(d, (int, sympy.Integer)) or not isinstance(p, (int, sympy.Integer)):
            h1 = False
        else:
            d_val = int(d)
            p_val = int(p)
            h1 = (d_val > 0) and ((p_val - 1) % d_val == 0)
    except Exception:
        h1 = False
        
    try:
        if not isinstance(d, (int, sympy.Integer)) or not isinstance(p, (int, sympy.Integer)):
            neg_q = False
        else:
            d_val = int(d)
            p_val = int(p)
            # Restrict p_val to a reasonable range to prevent timeouts
            if p_val < 1 or p_val > 100000 or d_val <= 0:
                neg_q = False
            else:
                sols = 0
                for x in range(p_val):
                    if pow(x, d_val, p_val) == 1 % p_val:
                        sols += 1
                neg_q = (sols != d_val)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: d is a positive integer that divides p - 1",
    "¬Q: The polynomial congruence x^d ≡ 1 (mod p) does NOT have exactly d distinct solutions modulo p"
]

N_HYP = 1
NEG_Q_INDEX = 1