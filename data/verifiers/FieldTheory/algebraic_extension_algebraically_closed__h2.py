import sympy
from sympy import Symbol, S
from sympy.polys.domains import CC, QQ, ZZ, RR

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        K, L = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = (K == S.Complexes or K == CC or str(K) in ['CC', 'Complexes', 'C'])
    except Exception:
        h1 = False
        
    try:
        neg_q = (L != K)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "¬Q: L is not K or the extension degree is not 1"
]

N_HYP = 1
NEG_Q_INDEX = 1