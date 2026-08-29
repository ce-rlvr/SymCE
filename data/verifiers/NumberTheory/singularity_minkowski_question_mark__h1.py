import sympy
from sympy.abc import x

def conditions(witness):
    try:
        if callable(witness):
            expr = witness(x)
        else:
            expr = witness
            
        deriv = sympy.diff(expr, x)
        is_zero = (sympy.simplify(deriv) == 0)
        neg_q = not is_zero
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS: list[str] = ["¬Q: The derivative is not 0 for Lebesgue almost all x in the unit interval"]
N_HYP: int = 0
NEG_Q_INDEX: int = 0