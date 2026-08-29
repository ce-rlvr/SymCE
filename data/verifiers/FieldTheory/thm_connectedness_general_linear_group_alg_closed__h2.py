import sympy
from sympy import S, Symbol

# Top-level setup
CC = S.Complexes
QQbar = Symbol('QQbar')
Qbar = Symbol('Qbar')
Fp_bar = Symbol('Fp_bar')
C = S.Complexes

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "¬Q: GL_n(K) is not a connected topological space"
]

def get_field(w_list):
    for w in w_list:
        if w in (S.Complexes, S.Reals, S.Rationals):
            return w
        name = ''
        if isinstance(w, str):
            name = w
        elif hasattr(w, 'name'):
            name = str(w.name)
        elif hasattr(w, '__name__'):
            name = str(w.__name__)
        else:
            name = str(w)
        name = name.lower()
        if any(x in name for x in ['c', 'q', 'r', 'f', 'bar', 'closure', 'algebraic', 'complex', 'field']):
            return w
            
    for w in w_list:
        if not isinstance(w, int) and not (hasattr(w, 'is_integer') and w.is_integer):
            return w
            
    return w_list[0] if w_list else None

def is_alg_closed(w):
    if w == S.Complexes:
        return True
    if w in (S.Reals, S.Rationals, S.Integers, S.Naturals, S.Naturals0):
        return False
        
    name = ''
    if isinstance(w, str):
        name = w
    elif hasattr(w, 'name'):
        name = str(w.name)
    elif hasattr(w, '__name__'):
        name = str(w.__name__)
    else:
        name = str(w)
        
    name = name.lower()
    
    if name in ('c', 'cc', 'complexes', 'complex', 's.complexes'):
        return True
    if 'bar' in name or 'closure' in name or 'algebraic' in name:
        return True
    if 'puiseux' in name:
        return True
        
    return False

def is_gln_connected(w):
    if w == S.Complexes:
        return True
        
    name = ''
    if isinstance(w, str):
        name = w
    elif hasattr(w, 'name'):
        name = str(w.name)
    elif hasattr(w, '__name__'):
        name = str(w.__name__)
    else:
        name = str(w)
        
    name = name.lower()
    
    if name in ('c', 'cc', 'complexes', 'complex', 's.complexes'):
        return True
        
    return False

def conditions(witness) -> list[bool]:
    w_list = witness if isinstance(witness, (tuple, list)) else [witness]
    
    field = get_field(w_list)
    
    h1 = False
    try:
        if field is not None:
            h1 = bool(is_alg_closed(field))
    except Exception:
        h1 = False
        
    neg_q = False
    try:
        if field is not None:
            neg_q = not bool(is_gln_connected(field))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]