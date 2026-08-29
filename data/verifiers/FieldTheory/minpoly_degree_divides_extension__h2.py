import sympy
from sympy import minpoly, degree, Integer, Rational, Poly
from sympy.abc import x

def get_degree(obj):
    if obj is None:
        return None
    if isinstance(obj, (int, Integer)):
        return int(obj)
    try:
        if hasattr(obj, 'degree') and callable(obj.degree):
            return int(obj.degree())
    except Exception:
        pass
    try:
        if hasattr(obj, 'free_symbols') and obj.free_symbols:
            return int(degree(obj))
        else:
            return int(degree(minpoly(obj, x)))
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            E_obj = witness.get('E', witness.get('deg_E', witness.get('gen_E')))
            alpha_obj = witness.get('alpha', witness.get('deg_alpha'))
        else:
            E_obj, alpha_obj = witness
    except Exception:
        return [False, False]

    deg_E = get_degree(E_obj)
    deg_alpha = get_degree(alpha_obj)

    try:
        h1 = (deg_E is not None and deg_E >= 1)
    except Exception:
        h1 = False

    try:
        neg_q = (deg_E is not None and deg_alpha is not None and deg_alpha >= 1 and deg_E % deg_alpha != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is a finite field extension",
    "¬Q: The degree of the minimal polynomial of alpha over F does not divide the degree of E over F"
]

N_HYP = 1
NEG_Q_INDEX = 1