import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def is_artinian(R):
    """
    Helper function to determine if a ring R is right Artinian.
    Returns True if Artinian (or if it cannot be determined, to be safe and reject the witness),
    and False if it is known to be non-Artinian.
    """
    if isinstance(R, str):
        R = R.replace(' ', '')
        if R in ['ZZ', 'Z']: 
            return False
        if R in ['QQ', 'Q', 'RR', 'R', 'CC', 'C']: 
            return True
        if '[x]' in R or '[t]' in R or '[y]' in R: 
            return False
        if R.startswith('Z/') or (R.startswith('Z') and R[1:].isdigit()): 
            return True
        if R.startswith('GF'): 
            return True
        if 'Z' in R and not ('/' in R or R[1:].isdigit()): 
            return False
        if '[' in R and ']' in R: 
            return False
        return True
        
    if R == ZZ: 
        return False
    if R == QQ: 
        return True
    
    try:
        if hasattr(R, 'is_Artinian'): 
            return bool(R.is_Artinian)
        if hasattr(R, 'is_artinian'): 
            return bool(R.is_artinian)
        if hasattr(R, 'is_Field') and R.is_Field: 
            return True
        if hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing: 
            return False
        if hasattr(R, 'domain'):
            if R.domain == ZZ: 
                return False
    except Exception:
        pass
        
    return True

def conditions(witness):
    """
    Given a witness (n, R) or {'n': n, 'R': R}, checks if it is a valid counterexample.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            R = witness.get('R')
        else:
            n, R = witness
    except Exception:
        return [False, False]
        
    # H_1: Let n be a positive integer
    try:
        n_val = float(n)
        h1 = n_val.is_integer() and n_val > 0
    except Exception:
        h1 = False
        
    # ¬Q: The matrix ring M_n(R) is NOT a right Artinian ring
    # M_n(R) is right Artinian iff R is right Artinian.
    try:
        neg_q = not is_artinian(R)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: M_n(R) is not a right Artinian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1