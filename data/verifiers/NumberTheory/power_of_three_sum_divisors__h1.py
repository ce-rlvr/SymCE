import sympy

def conditions(witness):
    try:
        k = sympy.sympify(witness)
        if not k.is_number:
            return [False]
    except Exception:
        return [False]
        
    try:
        term = 3**k
        if term.is_Integer and term > 0:
            lhs = sympy.divisor_sigma(term)
        else:
            lhs = None
    except Exception:
        lhs = None

    try:
        rhs = (3**(k+1) - 1) / 2
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

CONDITION_LABELS = [
    "¬Q: \\sigma(3^k) \\neq \\frac{3^{k+1}-1}{2}"
]

N_HYP = 0
NEG_Q_INDEX = 0