import sympy

def conditions(witness):
    try:
        if isinstance(witness, dict):
            x = witness['x']
            n = witness['n']
        else:
            x, n = witness
    except Exception:
        return [False, False]
        
    try:
        x_sym = sympy.sympify(x)
        n_sym = sympy.sympify(n)
        diff = sympy.simplify(x_sym**2 + 7 - 2**n_sym)
        h1 = bool(diff == 0 or diff.is_zero)
    except Exception:
        h1 = False
        
    try:
        n_sym = sympy.sympify(n)
        allowed_n = {sympy.sympify(k) for k in (3, 4, 5, 7, 15)}
        neg_q = bool(n_sym not in allowed_n)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x^2 + 7 = 2^n",
    "¬Q: n is not one of 3, 4, 5, 7, or 15"
]

N_HYP = 1
NEG_Q_INDEX = 1