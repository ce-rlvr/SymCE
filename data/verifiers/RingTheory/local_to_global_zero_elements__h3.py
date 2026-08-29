import sympy
from sympy import S
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.polys.domains import Domain

# Top-level setup
Integers = S.Integers
Rationals = S.Rationals
Reals = S.Reals
Complexes = S.Complexes

def conditions(witness):
    try:
        R, x = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a commutative ring with identity
    try:
        if isinstance(R, Domain):
            h1 = True
        elif R in (S.Integers, S.Rationals, S.Reals, S.Complexes):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: x is an element of R
    try:
        res = x in R
        h2 = (res is True) or (res == True)
    except Exception:
        h2 = False
        
    # ¬Q: x != 0 in R
    try:
        if hasattr(R, 'zero'):
            is_zero = (x == R.zero)
        else:
            is_zero = (x == 0)
            
        if (is_zero is True) or (is_zero == True):
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: x is an element of R",
    "¬Q: x is not 0 in R"
]

N_HYP = 2
NEG_Q_INDEX = 2