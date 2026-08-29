import sympy
from sympy import QQ, RR, CC, ZZ

CONDITION_LABELS = [
    "H_1: F is an ordered field",
    "¬Q: There exists a field homomorphism from K to F"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_QQ(domain):
    return domain == QQ or type(domain).__name__ == 'RationalField'

def is_RR(domain):
    return domain == RR or type(domain).__name__ == 'RealField'

def is_CC(domain):
    return domain == CC or type(domain).__name__ == 'ComplexField'

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False]
        K, F = witness
    except Exception:
        return [False, False]
        
    # H_1: F is an ordered field
    try:
        h1 = is_QQ(F) or is_RR(F)
    except Exception:
        h1 = False
        
    # ¬Q: There exists a field homomorphism from K to F
    try:
        neg_q = False
        if K == F and (is_QQ(K) or is_RR(K) or is_CC(K)):
            neg_q = True
        else:
            if is_QQ(K) and (is_QQ(F) or is_RR(F) or is_CC(F)):
                neg_q = True
            elif is_RR(K) and (is_RR(F) or is_CC(F)):
                neg_q = True
            elif is_CC(K) and is_CC(F):
                neg_q = True
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]