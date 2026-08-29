import sympy
from sympy import Matrix, eye, zeros
from sympy.ntheory import isprime
import itertools
import functools
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            M_raw, p = witness
        else:
            M_raw = witness
            p = 2
            
        if isinstance(M_raw, list):
            M = Matrix(M_raw)
        else:
            M = M_raw
            
        try:
            if not isinstance(M, Matrix):
                h1_ok = False
            elif not M.is_square:
                h1_ok = False
            elif not isprime(p):
                h1_ok = False
            else:
                h1_ok = all(isinstance(x, (int, sympy.Integer)) for x in M)
        except Exception:
            h1_ok = False
            
        h2_ok = h1_ok
        
        try:
            if not h1_ok:
                neg_q = False
            else:
                n = M.shape[0]
                is_skew = True
                for i in range(n):
                    for j in range(n):
                        if (M[i, j] + M[j, i]) % p != 0:
                            is_skew = False
                            break
                    if not is_skew:
                        break
                
                is_alt = is_skew
                for i in range(n):
                    if M[i, i] % p != 0:
                        is_alt = False
                        break
                        
                neg_q = (is_alt != is_skew)
        except Exception:
            neg_q = False
            
        return [bool(h1_ok), bool(h2_ok), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F (witness is a square Matrix M, optionally with prime p, default p=2)",
    "H_2: B is a bilinear form on V (M represents a bilinear form on F^n)",
    "¬Q: B is alternating if and only if B is skew-symmetric (fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2