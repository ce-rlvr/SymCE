import sympy
from sympy.ntheory import factorint

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        p_val, d_val = witness
        if int(p_val) != p_val or int(d_val) != d_val:
            return [False, False, False]
        p = int(p_val)
        d = int(d_val)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = (p >= 1)
    except Exception:
        h1 = False
        
    try:
        h2 = (d >= 1) and ((p - 1) % d == 0)
    except Exception:
        h2 = False
        
    try:
        if p < 1 or d < 1:
            neg_q = False
        else:
            cyclic_factors = []
            if p > 2:
                for q, e in factorint(p).items():
                    if q == 2:
                        if e == 2:
                            cyclic_factors.append(2)
                        elif e >= 3:
                            cyclic_factors.append(2)
                            cyclic_factors.append(2**(e-2))
                    else:
                        cyclic_factors.append((q**(e-1)) * (q - 1))
            
            order_G = 1
            for f in cyclic_factors:
                order_G *= f
                
            if order_G % d != 0:
                conclusion_holds = False
            else:
                conclusion_holds = True
                for r, k in factorint(d).items():
                    r_parts = [f for f in cyclic_factors if f % r == 0]
                    n = 0
                    for f in r_parts:
                        temp = f
                        while temp > 0 and temp % r == 0:
                            n += 1
                            temp //= r
                    
                    if 0 < k < n and len(r_parts) > 1:
                        conclusion_holds = False
                        break
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Q(zeta_p) is the p-th cyclotomic field",
    "H_2: d is a positive integer that divides p-1",
    "¬Q: The number of subfields K of Q(zeta_p) with degree d is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2