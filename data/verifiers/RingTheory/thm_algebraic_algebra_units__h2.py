import sympy
from sympy import *

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: A is algebraic over K",
    "H_3: x is not a zero-divisor",
    "¬Q: x is not a unit in A"
]

N_HYP = 3
NEG_Q_INDEX = 3

def _check_prop(obj, prop_name, *args):
    if hasattr(obj, prop_name):
        attr = getattr(obj, prop_name)
        if callable(attr):
            return bool(attr(*args))
        else:
            return bool(attr)
    return None

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            K, A, x = witness
        else:
            K = witness.K
            A = witness.A
            x = witness.x
            
        # H1: K is a field
        h1 = _check_prop(K, 'is_Field')
        if h1 is None:
            h1 = _check_prop(K, 'is_field')
        if h1 is None:
            h1 = False
            
        # H2: A is algebraic over K
        h2 = _check_prop(A, 'is_algebraic_over', K)
        if h2 is None:
            h2 = False
            
        # H3: x is not a zero-divisor
        h3_val = _check_prop(A, 'is_zero_divisor', x)
        if h3_val is None:
            h3_val = _check_prop(x, 'is_zero_divisor')
        if h3_val is not None:
            h3 = not h3_val
        else:
            h3 = False
            
        # neg_Q: x is not a unit
        is_unit_val = _check_prop(A, 'is_unit', x)
        if is_unit_val is None:
            is_unit_val = _check_prop(x, 'is_unit')
        if is_unit_val is not None:
            neg_q = not is_unit_val
        else:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]