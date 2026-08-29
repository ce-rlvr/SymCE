import sympy
import math

# Top-level setup (no specific named objects required for this Number Theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            d = witness.get('d')
        else:
            a, b, d = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)) and a != 0 and b != 0
    except Exception:
        h1 = False

    try:
        if d == 0 or d is None:
            neg_q = False
        else:
            val_a = sympy.S(a) / sympy.S(d)
            val_b = sympy.S(b) / sympy.S(d)
            g = sympy.gcd(val_a, val_b)
            neg_q = (g != 1)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a and b are non-zero integers",
    "¬Q: gcd(a/d, b/d) != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1