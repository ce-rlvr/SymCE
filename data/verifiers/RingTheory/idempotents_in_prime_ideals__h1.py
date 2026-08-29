import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: e is an element of R such that e^2 = e",
    "H_2: P is a prime ideal of R",
    "¬Q: It is not the case that exactly one of e or 1 - e belongs to P"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False]
            
        e, P, one = witness
        
        try:
            h1 = bool(e * e == e)
        except Exception:
            h1 = False
            
        h2 = False
        try:
            if callable(P):
                in_P = P
                h2 = True
            elif isinstance(P, (set, list, tuple)):
                in_P = lambda x: x in P
                h2 = True
            else:
                in_P = lambda x: x == P
                if hasattr(P, 'is_zero_matrix') and P.is_zero_matrix:
                    h2 = True
                elif P == 0:
                    h2 = True
                else:
                    h2 = True
        except Exception:
            h2 = False
            
        try:
            e_in_P = bool(in_P(e))
            one_minus_e_in_P = bool(in_P(one - e))
            
            q = (e_in_P != one_minus_e_in_P)
            neg_q = not q
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]