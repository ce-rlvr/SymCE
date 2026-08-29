import sympy

CONDITION_LABELS = [
    "¬Q: The Jacobi symbol (2/n) is not equal to (-1)^((n^2-1)/8)"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness) -> list[bool]:
    try:
        n = sympy.Integer(witness)
    except Exception:
        return [False]
        
    try:
        lhs = sympy.jacobi_symbol(2, n)
    except Exception:
        lhs = None
        
    try:
        rhs = (-1)**sympy.Rational(n**2 - 1, 8)
    except Exception:
        rhs = None
        
    try:
        if lhs is None or rhs is None:
            neg_q = True
        else:
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
        
    return [neg_q]