import sympy

def conditions(witness) -> list[bool]:
    try:
        p, q = witness
    except Exception:
        return [False, False, False]
    
    # H1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False
        
    # H2: q divides 2^p - 1
    try:
        if q == 0 or int(p) != p or int(q) != q:
            h2 = False
        else:
            h2 = (pow(2, int(p), abs(int(q))) == 1 % abs(int(q)))
    except Exception:
        h2 = False
        
    # neg_Q: not (q = 1 mod 2p and q = +/- 1 mod 8)
    try:
        if int(p) != p or int(q) != q:
            neg_q = False
        else:
            p_int = int(p)
            q_int = int(q)
            
            q_mod_2p = q_int % (2 * p_int)
            q_mod_8 = q_int % 8
            
            cond_1 = (q_mod_2p == 1)
            cond_2 = (q_mod_8 == 1 or q_mod_8 == 7)
            
            neg_q = not (cond_1 and cond_2)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: q divides 2^p - 1",
    "¬Q: q is not 1 mod 2p or q is not +/- 1 mod 8"
]

N_HYP = 2
NEG_Q_INDEX = 2