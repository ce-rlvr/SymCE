import sympy

def conditions(witness):
    try:
        if isinstance(witness, dict):
            x = witness['x']
            y = witness['y']
        else:
            x, y = witness
    except Exception:
        return [False, False]
    
    try:
        x_sym = sympy.sympify(x)
        y_sym = sympy.sympify(y)
        diff = sympy.simplify(y_sym**2 - (x_sym**3 - 1))
        h1 = bool(diff == 0)
    except Exception:
        h1 = False
        
    try:
        x_sym = sympy.sympify(x)
        y_sym = sympy.sympify(y)
        x_is_1 = bool(sympy.simplify(x_sym - 1) == 0)
        y_is_0 = bool(sympy.simplify(y_sym) == 0)
        neg_q = not (x_is_1 and y_is_0)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: y^2 = x^3 - 1",
    "¬Q: x != 1 or y != 0"
]

N_HYP = 1
NEG_Q_INDEX = 1