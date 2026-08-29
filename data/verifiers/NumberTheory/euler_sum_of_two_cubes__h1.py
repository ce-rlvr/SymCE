import sympy

def conditions(witness) -> list[bool]:
    """
    Given a witness (x, y, z), checks if it satisfies the remaining hypotheses
    and falsifies the conclusion.
    """
    try:
        x, y, z = witness
    except Exception:
        return [False, False]
        
    try:
        # H_1: x^3 + y^3 = z^3
        h1 = bool(sympy.simplify(x**3 + y**3 - z**3) == 0)
    except Exception:
        h1 = False
        
    try:
        # ¬Q: x y z != 0
        neg_q = bool(sympy.simplify(x * y * z) != 0)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x^3 + y^3 = z^3",
    "¬Q: x y z != 0"
]

N_HYP = 1
NEG_Q_INDEX = 1