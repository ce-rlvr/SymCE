import sympy
import math

def is_int(val):
    return isinstance(val, int) or isinstance(val, sympy.Integer)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            x = witness.get('x')
            n = witness.get('n')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            a, x, n = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: a and x are integers
    try:
        h1 = bool(is_int(a) and is_int(x))
    except Exception:
        h1 = False

    # H2: a x \equiv 1 \pmod n
    try:
        if n == 0:
            h2 = bool(a * x == 1)
        else:
            h2 = bool((a * x - 1) % n == 0)
    except Exception:
        h2 = False

    # Conclusion: x(2 - a x) \equiv a^{-1} \pmod{n^2}
    try:
        if is_int(a) and is_int(n):
            inv_a = pow(int(a), -1, int(n)**2)
            val = int(x) * (2 - int(a) * int(x))
            q = bool((val - inv_a) % (int(n)**2) == 0)
        else:
            inv_a = pow(a, -1, n**2)
            val = x * (2 - a * x)
            q = bool((val - inv_a) % (n**2) == 0)
    except Exception:
        q = False

    neg_q = not q

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a and x are integers",
    "H_2: a x \\equiv 1 \\pmod n",
    "¬Q: x(2 - a x) \\not\\equiv a^{-1} \\pmod{n^2}"
]

N_HYP = 2
NEG_Q_INDEX = 2