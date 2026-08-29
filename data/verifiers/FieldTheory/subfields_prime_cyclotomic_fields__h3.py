import sympy

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness['p']
            d = witness['d']
        else:
            p, d = witness
    except Exception:
        return [False, False, False]
    
    try:
        p_val = sympy.S(p)
        h1_ok = bool(p_val.is_prime and p_val % 2 == 1)
    except Exception:
        h1_ok = False
        
    try:
        p_val = sympy.S(p)
        h2_ok = bool(p_val.is_integer and p_val > 0)
    except Exception:
        h2_ok = False
        
    try:
        p_val = sympy.S(p)
        d_val = sympy.S(d)
        if d_val.is_integer and d_val > 0 and (p_val - 1) % d_val == 0:
            exactly_one = True
        else:
            exactly_one = False
        neg_q_ok = not exactly_one
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: Q(zeta_p) is the p-th cyclotomic field",
    "not Q: There does not exist exactly one subfield K of Q(zeta_p) with degree over Q equal to d"
]

N_HYP = 2
NEG_Q_INDEX = 2