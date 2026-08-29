import sympy
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x, y

def is_pid(R):
    if hasattr(R, 'is_PID'):
        return bool(R.is_PID)
    return False

def is_pir(R):
    if hasattr(R, 'is_PIR'):
        return bool(R.is_PIR)
    if hasattr(R, 'is_PID'):
        return bool(R.is_PID)
    return False

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        R1, R2 = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = is_pid(R2)
    except Exception:
        h1 = False
        
    try:
        # The direct product R1 x R2 is a principal ideal ring (PIR) 
        # if and only if both R1 and R2 are PIRs.
        r1_pir = is_pir(R1)
        r2_pir = is_pir(R2)
        prod_is_pir = r1_pir and r2_pir
        neg_q = not prod_is_pir
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R_2 is a principal ideal domain",
    "¬Q: R_1 \\times R_2 is not a principal ideal ring"
]

N_HYP = 1
NEG_Q_INDEX = 1