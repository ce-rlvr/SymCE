import sympy
import math

def conditions(witness):
    try:
        a = sympy.sympify(witness)
        h1 = (getattr(a, 'is_extended_real', False) is True) or (a == sympy.oo) or isinstance(witness, (int, float))
    except Exception:
        h1 = False

    try:
        a = sympy.sympify(witness)
        neg_q = (a == sympy.oo) or (isinstance(witness, float) and math.isinf(witness) and witness > 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = ["H_1: f is defined by f(x) = exp(x) on the interval", "neg_Q: f is not uniformly continuous on the interval"]

N_HYP = 1
NEG_Q_INDEX = 1