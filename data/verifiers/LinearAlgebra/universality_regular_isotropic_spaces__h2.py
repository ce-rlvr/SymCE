import sympy
import itertools
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            M, p = witness
            p = int(p)
        else:
            M = witness
            p = 0
            
        if isinstance(M, sympy.Matrix) and M.is_square and M == M.T:
            if p == 0:
                if M.det() != 0:
                    h1 = True
            elif p > 2 and sympy.isprime(p):
                if M.det() % p != 0:
                    h1 = True
    except Exception:
        h1 = False

    try:
        if h1:
            n = M.shape[0]
            if p == 0:
                if n == 0:
                    neg_q = True
                elif M.is_positive_definite == True or M.is_negative_definite == True:
                    neg_q = True
                elif n == 1:
                    neg_q = True
            else:
                if n == 0:
                    neg_q = True
                elif p**n <= 100000:
                    represented = set()
                    for vec in itertools.product(range(p), repeat=n):
                        v = sympy.Matrix(vec)
                        val = (v.T * M * v)[0] % p
                        represented.add(val)
                    if len(represented) < p:
                        neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is a non-degenerate quadratic space over a field F of characteristic not 2",
    "¬Q: The quadratic form on V does not evaluate to every scalar in F"
]

N_HYP = 1
NEG_Q_INDEX = 1