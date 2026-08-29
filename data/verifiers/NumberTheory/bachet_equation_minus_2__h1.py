import sympy

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            x = witness.get('x')
            y = witness.get('y')
        else:
            x, y = witness
            
        if x is None or y is None:
            return [False, False]
            
        x = sympy.Rational(x)
        y = sympy.Rational(y)
        
        if not (x.is_integer and y.is_integer):
            return [False, False]
            
        x = int(x)
        y = int(y)
    except Exception:
        return [False, False]

    try:
        h1_ok = bool(y**2 == x**3 - 2)
    except Exception:
        h1_ok = False

    try:
        neg_q_ok = not (x == 3 and y == 5)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: y^2 = x^3 - 2",
    "¬Q: x != 3 or y != 5"
]

N_HYP = 1
NEG_Q_INDEX = 1