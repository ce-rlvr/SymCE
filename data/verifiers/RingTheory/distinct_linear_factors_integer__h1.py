import sympy
from sympy import Rational, Integer, Symbol

x = Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
        elif isinstance(witness, (tuple, list)):
            if len(witness) != 2:
                return [False, False]
            a, b = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(a != b)
    except Exception:
        h1 = False
        
    try:
        def is_int(v):
            if isinstance(v, int): return True
            if isinstance(v, Integer): return True
            if isinstance(v, Rational) and v.q == 1: return True
            if hasattr(v, 'is_integer') and v.is_integer: return True
            return False
            
        if is_int(a) and is_int(b):
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = ["H_1: a is not equal to b", "¬Q: The factor ring is not isomorphic"]
N_HYP = 1
NEG_Q_INDEX = 1