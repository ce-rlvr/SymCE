import sympy
from sympy import Rational, Integer, oo
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: E is a field containing subfields K and L",
    "H_2: F = K intersection L",
    "H_3: K and L are linearly disjoint over F",
    "¬Q: deg(KL over L) != deg(K over F)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_val(obj, name, default=True):
    if isinstance(obj, dict):
        if name in obj:
            val = obj[name]
            return val() if callable(val) else val
        return default
    if hasattr(obj, name):
        val = getattr(obj, name)
        return val() if callable(val) else val
    return default

def is_degree(val):
    if isinstance(val, (int, float)):
        return True
    if val == oo:
        return True
    if type(val).__name__ == 'Aleph':
        return True
    if isinstance(val, Integer):
        return True
    return False

def conditions(witness):
    try:
        deg_KL_L = get_val(witness, "deg_KL_L", None)
        deg_K_F = get_val(witness, "deg_K_F", None)
        
        if deg_KL_L is not None and deg_K_F is not None:
            h1 = bool(get_val(witness, "E_is_field", True))
            h2 = bool(get_val(witness, "F_eq_K_cap_L", True))
            h3 = bool(get_val(witness, "linearly_disjoint", True))
            neg_q = (deg_KL_L != deg_K_F)
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 4 and all(is_degree(v) for v in witness):
                deg_K_F, deg_L_F, deg_KL_F, deg_KL_L = witness
                h1, h2, h3 = True, True, True
                neg_q = (deg_KL_L != deg_K_F)
                return [h1, h2, h3, neg_q]
            elif len(witness) == 2 and all(is_degree(v) for v in witness):
                deg_K_F, deg_KL_L = witness
                h1, h2, h3 = True, True, True
                neg_q = (deg_KL_L != deg_K_F)
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]