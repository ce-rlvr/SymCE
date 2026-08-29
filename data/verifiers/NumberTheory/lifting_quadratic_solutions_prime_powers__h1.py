import math
import sympy
from sympy.ntheory import factorint, jacobi_symbol

CONDITION_LABELS = [
    "H_1: a is an integer",
    "H_2: gcd(a, p) = 1",
    "H_3: (a|p) = 1",
    "¬Q: For some k >= 1, x^2 = a (mod p^k) does not have exactly 2 solutions"
]

N_HYP = 3
NEG_Q_INDEX = 3

def kronecker(a, n):
    a = int(a)
    n = int(n)
    if n == 0:
        return 1 if a in (1, -1) else 0
    if n < 0:
        return kronecker(a, -n) * (-1 if a < 0 else 1)
    
    v = 0
    while n % 2 == 0 and n > 0:
        v += 1
        n //= 2
        
    if v == 0:
        res = 1
    else:
        if a % 2 == 0:
            res = 0
        else:
            a_mod_8 = a % 8
            if a_mod_8 in (1, 7):
                res = 1
            else:
                res = -1
            if v % 2 == 0:
                res = 1
                
    if n == 1:
        return res
        
    return res * jacobi_symbol(a, n)

def conditions(witness):
    try:
        a, p = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(a, (int, sympy.Integer)) and not isinstance(a, bool)
    except Exception:
        h1 = False
        
    try:
        if not isinstance(p, (int, sympy.Integer)) or isinstance(p, bool):
            h2 = False
        else:
            h2 = math.gcd(int(a), int(p)) == 1
    except Exception:
        h2 = False
        
    try:
        h3 = kronecker(int(a), int(p)) == 1
    except Exception:
        h3 = False
        
    try:
        neg_q = False
        a_int = int(a)
        p_int = int(p)
        for k in range(1, 6):
            m = abs(p_int**k)
            if m == 0:
                if a_int < 0:
                    sols = 0
                elif a_int == 0:
                    sols = 1
                else:
                    sols = 2 if math.isqrt(a_int)**2 == a_int else 0
            elif m <= 100000:
                a_mod = a_int % m
                sols = sum(1 for x in range(m) if (x*x) % m == a_mod)
            else:
                factors_p = factorint(abs(p_int))
                sols = 1
                for q, e_p in factors_p.items():
                    e = e_p * k
                    if q == 2:
                        if a_int % 2 != 0:
                            if e == 1: s = 1
                            elif e == 2: s = 2 if a_int % 4 == 1 else 0
                            else: s = 4 if a_int % 8 == 1 else 0
                        else:
                            s = -1
                    else:
                        if a_int % q != 0:
                            s = 2 if jacobi_symbol(a_int, q) == 1 else 0
                        else:
                            s = -1
                    sols *= s
            if sols != 2:
                neg_q = True
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]