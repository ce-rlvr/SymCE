import math
from sympy import Rational

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        values, probs, theta = witness
        values = list(values)
        probs = list(probs)
    except Exception:
        return [False, False, False, False]

    try:
        if len(values) != len(probs) or len(values) == 0:
            h1 = False
        else:
            sum_p = sum(float(p) for p in probs)
            h1 = all(float(p) >= 0 for p in probs) and math.isclose(sum_p, 1.0, abs_tol=1e-7)
    except Exception:
        h1 = False

    try:
        E_f2 = sum(float(p) * float(v)**2 for p, v in zip(probs, values))
        h2 = math.isfinite(E_f2)
    except Exception:
        h2 = False

    try:
        h3 = 0.0 <= float(theta) <= 1.0
    except Exception:
        h3 = False

    try:
        E_f = sum(float(p) * float(v) for p, v in zip(probs, values))
        E_f2 = sum(float(p) * float(v)**2 for p, v in zip(probs, values))
        
        if E_f2 == 0.0:
            neg_q = False
        else:
            threshold = float(theta) * E_f
            lhs = sum(float(p) for p, v in zip(probs, values) if float(v) > threshold)
            rhs = ((1.0 - float(theta))**2) * (E_f**2) / E_f2
            
            neg_q = lhs < rhs - 1e-9
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a probability space",
    "H_2: f belongs to L^2",
    "H_3: 0 <= theta <= 1",
    "¬Q: mu(f > theta * E(f)) < (1-theta)^2 * E(f)^2 / E(f^2)"
]

N_HYP = 3
NEG_Q_INDEX = 3