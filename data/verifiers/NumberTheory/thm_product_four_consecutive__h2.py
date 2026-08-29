import math
import sympy

# Top-level setup: no specific named bindings needed for this Number Theory conjecture.

def conditions(witness):
    """
    Checks whether the given witness satisfies the remaining hypotheses
    and falsifies the conclusion of the conjecture.
    """
    y = None
    if isinstance(witness, dict):
        if 'x' in witness:
            x = witness['x']
            y = witness.get('y')
        else:
            x = witness
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 2:
            x, y = witness
        elif len(witness) == 1:
            x = witness[0]
        else:
            x = witness
    else:
        x = witness

    # H_1: x is a positive integer
    h1_ok = False
    try:
        if isinstance(x, bool):
            h1_ok = False
        elif isinstance(x, int):
            h1_ok = x > 0
        elif isinstance(x, sympy.Integer):
            h1_ok = x > 0
        elif isinstance(x, float):
            h1_ok = x.is_integer() and x > 0
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # ¬Q: x(x+1)(x+2)(x+3) == y^2
    neg_q_ok = False
    try:
        x_val = int(x)
        val = x_val * (x_val + 1) * (x_val + 2) * (x_val + 3)
        if y is not None:
            if isinstance(y, sympy.Expr):
                neg_q_ok = bool(sympy.simplify(val - y**2) == 0)
            elif isinstance(y, bool):
                neg_q_ok = False
            elif isinstance(y, int):
                neg_q_ok = (val == y**2)
            elif isinstance(y, float):
                if y.is_integer():
                    neg_q_ok = (val == int(y)**2)
                else:
                    neg_q_ok = math.isclose(val, y**2, rel_tol=1e-9)
            else:
                neg_q_ok = math.isclose(val, float(y)**2, rel_tol=1e-9)
        else:
            if val >= 0:
                s = math.isqrt(val)
                neg_q_ok = (s * s == val)
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x is a positive integer",
    "¬Q: x(x+1)(x+2)(x+3) == y^2"
]

N_HYP = 1
NEG_Q_INDEX = 1