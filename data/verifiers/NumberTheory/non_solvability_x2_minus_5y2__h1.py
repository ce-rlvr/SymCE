import sympy

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            x = witness['x']
            y = witness['y']
        else:
            x, y = witness
            
        val = sympy.simplify(x**2 - 5*y**2)
        neg_q = bool(val == 2 or val == -2 or sympy.simplify(val - 2) == 0 or sympy.simplify(val + 2) == 0)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: x^2 - 5y^2 = 2 or x^2 - 5y^2 = -2"
]

N_HYP = 0
NEG_Q_INDEX = 0