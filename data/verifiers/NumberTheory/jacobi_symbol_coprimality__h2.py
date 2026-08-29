import sympy
from sympy.ntheory import jacobi_symbol

# Top-level setup
# (No named bindings needed for Number Theory; integers and rationals are used directly)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            n = witness.get('n')
            if a is None or n is None:
                return [False, False]
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            a, n = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        # Check if n is an odd positive integer
        if isinstance(n, str):
            h1 = False
        else:
            n_val = int(n)
            h1 = (n_val == n) and (n_val % 2 == 1) and (n_val > 0)
    except Exception:
        h1 = False

    try:
        # Evaluate if Jacobi symbol (a/n) is equal to 0
        try:
            j = jacobi_symbol(a, n)
            j_is_zero = (j == 0)
        except Exception:
            j_is_zero = False

        # Evaluate if gcd(a, n) > 1
        try:
            g = sympy.gcd(a, n)
            g_gt_1 = bool(g > 1)
        except Exception:
            g_gt_1 = False

        # The conclusion is that these two conditions are equivalent
        q = (j_is_zero == g_gt_1)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an odd positive integer",
    "¬Q: jacobi_symbol(a, n) == 0 is not equivalent to gcd(a, n) > 1"
]

N_HYP = 1
NEG_Q_INDEX = 1