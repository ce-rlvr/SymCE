import sympy
from sympy.ntheory import factorint

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            q = witness.get('q')
        else:
            n, q = witness
    except Exception:
        return [False, False]
        
    try:
        n_int = int(n)
        h1 = (n_int >= 2)
    except Exception:
        h1 = False
        
    try:
        q_int = int(q)
        if q_int < 2:
            neg_q = True
        else:
            factors = factorint(q_int)
            if len(factors) == 1:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = ['H_1: n is an integer such that n >= 2', '¬Q: The number of monic square-free polynomials is not exactly q**n - q**(n-1)']

N_HYP = 1
NEG_Q_INDEX = 1