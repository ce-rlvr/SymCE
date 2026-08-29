import sympy
from sympy import sympify, simplify

# Top-level setup
# (No specific named bindings required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            if 'x' not in witness or 'y' not in witness:
                return [False, False]
            x = witness['x']
            y = witness['y']
        elif hasattr(witness, 'x') and hasattr(witness, 'y'):
            x = witness.x
            y = witness.y
        else:
            x, y = witness
    except Exception:
        return [False, False]

    # H_1: y is an integer
    try:
        y_sym = sympify(y)
        if y_sym.is_integer is True:
            h1_ok = True
        elif y_sym.free_symbols:
            h1_ok = False
        else:
            val = complex(y_sym.evalf())
            h1_ok = bool(abs(val.imag) < 1e-12 and abs(val.real - round(val.real)) < 1e-12)
    except Exception:
        h1_ok = False

    # neg_Q: y^2 == x^3 + 7
    try:
        x_sym = sympify(x)
        y_sym = sympify(y)
        diff = simplify(y_sym**2 - (x_sym**3 + 7))
        if diff == 0:
            neg_q_ok = True
        elif diff.free_symbols:
            neg_q_ok = False
        else:
            neg_q_ok = bool(abs(complex(diff.evalf())) < 1e-12)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: y is an integer",
    "¬Q: y^2 = x^3 + 7"
]

N_HYP = 1
NEG_Q_INDEX = 1