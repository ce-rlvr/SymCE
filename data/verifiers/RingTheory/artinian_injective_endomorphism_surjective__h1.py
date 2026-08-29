import sympy
from sympy import ZZ, QQ, S
from sympy.abc import x, y, z

# Top-level setup
# The witness is expected to be a tuple (R, a) where R is a ring (like ZZ)
# and a is an element of R representing the endomorphism f(x) = a*x.

CONDITION_LABELS = [
    "H_1: f is an injective right R-module homomorphism from R to R",
    "¬Q: f is not surjective"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        R, a = witness
    except Exception:
        return [False, False]
        
    # H_1: f is an injective right R-module homomorphism
    try:
        if hasattr(R, 'zero'):
            zero = R.zero
        else:
            zero = 0
            
        in_R = False
        if hasattr(R, 'contains'):
            try:
                if R.contains(a) == True:
                    in_R = True
            except Exception:
                pass
        if not in_R:
            try:
                if a in R:
                    in_R = True
            except Exception:
                pass
                
        if not in_R:
            h1 = False
        else:
            # For f(x) = a*x to be injective in an integral domain, a != 0.
            h1 = (a != zero)
    except Exception:
        h1 = False
        
    # neg_Q: f is not surjective
    try:
        if hasattr(R, 'one'):
            one = R.one
        else:
            one = 1
            
        is_surj = False
        if hasattr(R, 'exquo'):
            try:
                R.exquo(one, a)
                is_surj = True
            except Exception:
                is_surj = False
        else:
            try:
                inv = 1 / a
                if hasattr(R, 'contains'):
                    if R.contains(inv) == True:
                        is_surj = True
                if not is_surj:
                    if inv in R:
                        is_surj = True
            except Exception:
                is_surj = False
                
        neg_q = not is_surj
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]