import sympy
import math

def conditions(witness):
    try:
        x_sym = sympy.sympify(witness)
        x_val = float(x_sym)
        h1 = x_val > 0
    except Exception:
        h1 = False

    try:
        x_sym = sympy.sympify(witness)
        x_val = float(x_sym)
        n = int(math.floor(x_val))
        
        q_val = 0
        for i in range(1, n + 1):
            if sympy.mobius(i) != 0:
                q_val += 1
                
        lhs = q_val / x_sym
        rhs = 6 / sympy.pi**2
        
        diff = sympy.simplify(lhs - rhs)
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is a positive real number",
    "¬Q: Q(x)/x != 6/pi^2"
]

N_HYP = 1
NEG_Q_INDEX = 1