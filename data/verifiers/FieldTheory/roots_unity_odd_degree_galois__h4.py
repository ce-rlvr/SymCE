import sympy
from sympy import isprime

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: The degree of L over K is an odd integer",
    "H_3: n >= 1 is an integer",
    "¬Q: L DOES contain a primitive 2^n-th root of unity"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            if isinstance(n, int) and n >= 1:
                h3 = True
                
                if 'p' in witness and 'd_K' in witness and 'd_L' in witness:
                    p = witness['p']
                    d_K = witness['d_K']
                    d_L = witness['d_L']
                    if isinstance(p, int) and isinstance(d_K, int) and isinstance(d_L, int):
                        if isprime(p) and d_K >= 1 and d_L >= 1:
                            if d_L % d_K == 0:
                                h1 = True
                                deg = d_L // d_K
                                if deg % 2 == 1:
                                    h2 = True
                                if p == 2:
                                    if n == 1:
                                        neg_q = True
                                else:
                                    if (p**d_L - 1) % (2**n) == 0:
                                        neg_q = True
                                        
                else:
                    L = witness.get('L')
                    K = witness.get('K')
                    if L in ('Q', sympy.QQ) and K in ('Q', sympy.QQ):
                        h1 = True
                        h2 = True
                        if n == 1:
                            neg_q = True
                        
        elif isinstance(witness, tuple) and len(witness) == 4:
            p, d_K, d_L, n = witness
            if isinstance(p, int) and isinstance(d_K, int) and isinstance(d_L, int) and isinstance(n, int):
                if n >= 1:
                    h3 = True
                if isprime(p) and d_K >= 1 and d_L >= 1 and d_L % d_K == 0:
                    h1 = True
                    if (d_L // d_K) % 2 == 1:
                        h2 = True
                    if p == 2:
                        if n == 1:
                            neg_q = True
                    else:
                        if (p**d_L - 1) % (2**n) == 0:
                            neg_q = True
                            
        elif isinstance(witness, tuple) and len(witness) == 3:
            L, K, n = witness
            if isinstance(n, int):
                if n >= 1:
                    h3 = True
                if L in ('Q', sympy.QQ) and K in ('Q', sympy.QQ):
                    h1 = True
                    h2 = True
                    if n == 1:
                        neg_q = True
                    
    except Exception:
        pass

    return [h1, h2, h3, neg_q]