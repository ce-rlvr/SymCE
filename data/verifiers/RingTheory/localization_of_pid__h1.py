import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup
# (No specific named groups needed for this ring theory conjecture)

def is_subset_and_mult_closed(R, S):
    try:
        S_list = list(S)
    except TypeError:
        return False
    if not S_list:
        return False
        
    for s in S_list:
        try:
            if s not in R:
                if R(s) != s:
                    return False
        except Exception:
            return False
            
    for a in S_list:
        for b in S_list:
            prod = a * b
            found = False
            for s in S_list:
                if prod == s:
                    found = True
                    break
            if not found:
                return False
    return True

def zero_not_in_S(R, S):
    try:
        S_list = list(S)
    except TypeError:
        return False
    for s in S_list:
        if s == 0 or s == getattr(R, 'zero', 0):
            return False
    return True

def is_localization_PID(R, S):
    try:
        S_list = list(S)
    except TypeError:
        raise ValueError("S is not iterable")
        
    for s in S_list:
        if s != 1 and s != -1 and s != getattr(R, 'one', 1) and s != -getattr(R, 'one', 1):
            raise NotImplementedError("Localization with non-units not supported in this verifier")
            
    if hasattr(R, 'is_PID') and R.is_PID is not None:
        return R.is_PID
        
    if hasattr(R, 'domain') and hasattr(R, 'symbols'):
        if len(R.symbols) > 1:
            return False
        if len(R.symbols) == 1:
            return getattr(R.domain, 'is_Field', False)
        if len(R.symbols) == 0:
            if hasattr(R.domain, 'is_PID'):
                return R.domain.is_PID
                
    if R == ZZ:
        return True
    if R == QQ:
        return True
        
    if R.__class__.__name__ in ['PolyRing', 'PolynomialRing']:
        if len(R.symbols) > 1:
            return False
        if len(R.symbols) == 1:
            return getattr(R.domain, 'is_Field', False)
            
    raise ValueError(f"Cannot determine if {R} is a PID")

def conditions(witness) -> list[bool]:
    try:
        R, S = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_subset_and_mult_closed(R, S)
    except Exception:
        h1 = False
        
    try:
        h2 = zero_not_in_S(R, S)
    except Exception:
        h2 = False
        
    try:
        is_pid = is_localization_PID(R, S)
        neg_q = not is_pid
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: 0 is not an element of S",
    "¬Q: The localization S^{-1}R is not a principal ideal domain"
]

N_HYP = 2
NEG_Q_INDEX = 2