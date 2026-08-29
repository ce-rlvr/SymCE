import sympy
from sympy.matrices import eye, zeros
import math

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _get_vec(witness):
    if isinstance(witness, (list, tuple)):
        return list(witness)
    elif hasattr(witness, '__iter__') and not isinstance(witness, (str, dict)):
        return list(witness)
    else:
        return [witness]

def conditions(witness) -> list[bool]:
    # H_1: x is a vector in R^n
    try:
        vec = _get_vec(witness)
        if len(vec) < 1:
            h1 = False
        else:
            h1 = True
            for v in vec:
                val = sympy.sympify(v)
                if val.is_real is False:
                    h1 = False
                    break
                if val.is_real is None:
                    try:
                        float(val)
                    except Exception:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # ¬Q: f is not continuously differentiable at x, or its gradient is not x/||x||
    # For the Euclidean norm, this is true if and only if x is the zero vector.
    try:
        vec = _get_vec(witness)
        neg_q = True
        for v in vec:
            if sympy.sympify(v) != 0:
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is a vector in R^n",
    "¬Q: f is not continuously differentiable at x, or its gradient is not x/||x||"
]

N_HYP = 1
NEG_Q_INDEX = 1