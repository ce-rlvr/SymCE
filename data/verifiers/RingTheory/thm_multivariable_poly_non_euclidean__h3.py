import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y, z
import sympy.polys

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n is an integer such that n >= 2",
    "¬Q: R is a Euclidean domain"
]

def conditions(witness):
    if isinstance(witness, dict):
        F = witness.get('F')
        n = witness.get('n')
        R = witness.get('R')
    else:
        try:
            F, n, R = witness
        except Exception:
            return [False, False, False]
            
    try:
        h1 = False
        if hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif F == QQ:
            h1 = True
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(n, int) and n >= 2
    except Exception:
        h2 = False
        
    try:
        neg_q = False
        if hasattr(R, 'is_Field') and R.is_Field:
            neg_q = True
        elif hasattr(R, 'is_PID') and R.is_PID:
            neg_q = True
        elif R == ZZ or R == QQ:
            neg_q = True
        elif hasattr(R, 'domain') and hasattr(R, 'gens'):
            if hasattr(R.domain, 'is_Field') and R.domain.is_Field and len(R.gens) == 1:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]