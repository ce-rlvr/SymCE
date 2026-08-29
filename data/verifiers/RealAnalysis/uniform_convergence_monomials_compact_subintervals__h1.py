import sympy
import math

def get_a(witness):
    if isinstance(witness, dict) and 'a' in witness:
        return float(witness['a']), True
    elif isinstance(witness, sympy.Interval):
        return float(witness.end), (float(witness.start) == 0.0)
    elif isinstance(witness, (list, tuple)) and len(witness) == 2:
        return float(witness[1]), (float(witness[0]) == 0.0)
    else:
        return float(witness), True

def conditions(witness) -> list[bool]:
    try:
        a, valid_start = get_a(witness)
        h1 = bool(valid_start and (a >= 0) and math.isfinite(a))
    except Exception:
        h1 = False

    try:
        a, _ = get_a(witness)
        neg_q = bool(a >= 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is non-negative so the interval from 0 to a is valid",
    "¬Q: f_n(x) = x^n does not converge uniformly to 0 on the interval from 0 to a"
]

N_HYP = 1
NEG_Q_INDEX = 1