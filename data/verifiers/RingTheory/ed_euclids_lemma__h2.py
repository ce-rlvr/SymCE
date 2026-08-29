import sympy
from sympy import gcd, rem, div, simplify
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
ZZ = sympy.ZZ
QQ = sympy.QQ

def divides(a, b):
    if a == 0:
        return b == 0
    try:
        if b % a == 0:
            return True
    except Exception:
        pass
    try:
        if rem(b, a) == 0:
            return True
    except Exception:
        pass
    try:
        q, r = div(b, a)
        if r == 0:
            return True
    except Exception:
        pass
    try:
        res = simplify(b / a)
        if getattr(res, 'is_Integer', False):
            return True
        if getattr(res, 'is_polynomial', lambda: False)():
            return True
    except Exception:
        pass
    return False

def is_coprime(a, b):
    try:
        g = gcd(a, b)
        if g == 1 or g == -1:
            return True
        if hasattr(g, 'is_constant') and g.is_constant() and g != 0:
            return True
        if hasattr(g, 'is_unit') and g.is_unit:
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        # Witness can be (R, a, b, c) or just (a, b, c) with implicit domain
        if len(witness) == 4:
            R, a, b, c = witness
        elif len(witness) == 3:
            a, b, c = witness
            R = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: Let R be a Euclidean domain
    try:
        if R is not None:
            h1 = bool(getattr(R, 'is_PID', False) or getattr(R, 'is_Field', False))
            if not h1 and isinstance(R, str):
                h1 = R in ['ZZ', 'QQ', 'RR', 'CC'] or 'x' in R
        else:
            # If domain is not explicitly provided, assume the elements come from a valid one
            h1 = True
    except Exception:
        h1 = False

    # H_2: The element a divides the product bc
    try:
        h2 = bool(divides(a, b * c))
    except Exception:
        h2 = False

    # H_3: The elements a and b are coprime
    try:
        h3 = bool(is_coprime(a, b))
    except Exception:
        h3 = False

    # ¬Q: The element a does not divide c
    try:
        neg_q = not bool(divides(a, c))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: Let R be a Euclidean domain",
    "H_2: The element a divides the product bc",
    "H_3: The elements a and b are coprime",
    "¬Q: The element a does not divide c"
]

N_HYP: int = 3
NEG_Q_INDEX: int = 3