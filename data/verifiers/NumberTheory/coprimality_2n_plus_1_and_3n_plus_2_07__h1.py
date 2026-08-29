import sympy

def conditions(witness):
    try:
        n = sympy.sympify(witness)
        neg_q = bool(sympy.gcd(2*n + 1, 3*n + 2) != 1)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: gcd(2n+1, 3n+2) != 1"
]

N_HYP = 0
NEG_Q_INDEX = 0