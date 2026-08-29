import sympy
from sympy import Rational, Integer

# Top-level setup
# No specific named bindings required for this number theory problem.

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        x, y = witness
    except Exception:
        return [False, False]
        
    try:
        # Check if y^2 = x^3 + 1
        diff = sympy.simplify(y**2 - (x**3 + 1))
        h1 = (diff == 0)
    except Exception:
        h1 = False
        
    try:
        # Check if (x, y) is not in the set of known solutions
        known_solutions = [(-1, 0), (0, 1), (0, -1), (2, 3), (2, -3)]
        is_known = False
        for kx, ky in known_solutions:
            if sympy.simplify(x - kx) == 0 and sympy.simplify(y - ky) == 0:
                is_known = True
                break
        neg_q = not is_known
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and y satisfy y^2 = x^3 + 1",
    "¬Q: (x, y) is not one of (-1, 0), (0, 1), (0, -1), (2, 3), (2, -3)"
]

N_HYP = 1
NEG_Q_INDEX = 1