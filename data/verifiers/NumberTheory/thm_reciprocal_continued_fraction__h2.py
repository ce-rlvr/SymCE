import sympy

def conditions(witness):
    try:
        w = sympy.sympify(witness)
        h1 = bool(w.is_real and w > 1)
    except Exception:
        h1 = False
        
    try:
        w = sympy.sympify(witness)
        neg_q = bool(w.is_rational)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: alpha > 1 is a real number",
    "not_Q: The simple continued fraction expansion of 1/alpha is finite"
]

N_HYP = 1
NEG_Q_INDEX = 1