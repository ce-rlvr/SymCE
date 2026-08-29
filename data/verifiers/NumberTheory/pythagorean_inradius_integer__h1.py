import sympy

def conditions(witness):
    try:
        a, b, c = witness
    except Exception:
        return [False, False]
    
    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        c_sym = sympy.sympify(c)
        diff = sympy.simplify(a_sym**2 + b_sym**2 - c_sym**2)
        if diff == 0:
            h1 = True
        else:
            h1 = abs(float(diff)) < 1e-9
    except Exception:
        h1 = False
        
    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        c_sym = sympy.sympify(c)
        val = sympy.simplify((a_sym + b_sym - c_sym) / 2)
        if val.is_integer is not None:
            neg_q = not val.is_integer
        else:
            neg_q = not float(val).is_integer()
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a^2 + b^2 = c^2",
    "¬Q: (a + b - c) / 2 is not an integer"
]

N_HYP = 1
NEG_Q_INDEX = 1