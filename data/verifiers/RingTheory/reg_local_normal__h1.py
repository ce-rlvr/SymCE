import sympy
from sympy.abc import x, y, z
from sympy.polys.domains import QQ, ZZ

def check_regular_local(witness):
    for attr in ['is_regular_local_ring', 'is_regular_local']:
        if hasattr(witness, attr):
            v = getattr(witness, attr)
            return v() if callable(v) else bool(v)
            
    is_reg = None
    if hasattr(witness, 'is_regular'):
        v = witness.is_regular
        is_reg = v() if callable(v) else bool(v)
        
    is_loc = None
    if hasattr(witness, 'is_local'):
        v = witness.is_local
        is_loc = v() if callable(v) else bool(v)
        
    if is_reg is not None and is_loc is not None:
        return is_reg and is_loc
        
    if is_reg is False or is_loc is False:
        return False
        
    if hasattr(witness, 'is_Field') and witness.is_Field:
        return True
        
    raise ValueError("Cannot determine if witness is a regular local ring")

def check_integrally_closed_domain(witness):
    for attr in ['is_integrally_closed_domain', 'is_normal_domain']:
        if hasattr(witness, attr):
            v = getattr(witness, attr)
            return v() if callable(v) else bool(v)
            
    is_ic = None
    for attr in ['is_integrally_closed', 'is_normal']:
        if hasattr(witness, attr):
            v = getattr(witness, attr)
            is_ic = v() if callable(v) else bool(v)
            break
            
    is_dom = None
    for attr in ['is_domain', 'is_integral_domain']:
        if hasattr(witness, attr):
            v = getattr(witness, attr)
            is_dom = v() if callable(v) else bool(v)
            break
            
    if is_ic is not None and is_dom is not None:
        return is_ic and is_dom
        
    if is_ic is False or is_dom is False:
        return False
        
    if hasattr(witness, 'is_Field') and witness.is_Field:
        return True
    if hasattr(witness, 'is_UFD') and witness.is_UFD:
        return True
        
    raise ValueError("Cannot determine if witness is an integrally closed domain")

def conditions(witness) -> list[bool]:
    try:
        h1 = check_regular_local(witness)
    except Exception:
        h1 = False

    try:
        q = check_integrally_closed_domain(witness)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a regular local ring",
    "¬Q: R is not an integrally closed domain"
]

N_HYP = 1
NEG_Q_INDEX = 1