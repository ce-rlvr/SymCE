import sympy

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            x = witness['x']
            y = witness['y']
        else:
            x, y = witness
    except Exception:
        return [False, False]
        
    try:
        if isinstance(x, int):
            h1 = True
        elif isinstance(x, sympy.Integer):
            h1 = True
        elif hasattr(x, 'is_integer') and x.is_integer:
            h1 = True
        elif isinstance(x, float) and x.is_integer():
            h1 = True
        elif isinstance(x, sympy.Rational) and x.q == 1:
            h1 = True
        else:
            try:
                h1 = bool(sympy.simplify(x).is_integer)
            except Exception:
                h1 = False
    except Exception:
        h1 = False

    try:
        val = x**2 - 3 * y**2
        if val == -1:
            neg_q = True
        else:
            diff = sympy.simplify(val + 1)
            neg_q = (diff == 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is an integer",
    "¬Q: x^2 - 3y^2 == -1"
]

N_HYP = 1
NEG_Q_INDEX = 1