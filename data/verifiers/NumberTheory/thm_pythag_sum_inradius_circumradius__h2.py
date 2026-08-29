import sympy
import math

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: (a, b, c) is a Pythagorean triple with hypotenuse c",
    "H_2: R is the circumradius of the corresponding right triangle",
    "¬Q: r + R is not equal to (a + b) / 2"
]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
            R = witness.get('R', witness.get('circumradius'))
            r = witness.get('r', witness.get('inradius'))
            if any(v is None for v in (a, b, c, R, r)):
                return [False, False, False]
        elif hasattr(witness, 'a') and hasattr(witness, 'b') and hasattr(witness, 'c'):
            a = witness.a
            b = witness.b
            c = witness.c
            R = getattr(witness, 'R', getattr(witness, 'circumradius', None))
            r = getattr(witness, 'r', getattr(witness, 'inradius', None))
            if R is None or r is None:
                return [False, False, False]
        else:
            a, b, c, R, r = witness
    except Exception:
        return [False, False, False]

    # H_1: (a, b, c) is a Pythagorean triple with hypotenuse c
    try:
        if int(a) != a or int(b) != b or int(c) != c:
            h1 = False
        else:
            a_int, b_int, c_int = int(a), int(b), int(c)
            h1 = (a_int > 0 and b_int > 0 and c_int > 0 and 
                  a_int**2 + b_int**2 == c_int**2)
    except Exception:
        h1 = False

    # H_2: R is the circumradius of the corresponding right triangle
    try:
        # For a right triangle, the circumradius is exactly half the hypotenuse
        h2 = (2 * R == c)
    except Exception:
        h2 = False

    # ¬Q: r + R != (a + b) / 2
    try:
        val1 = 2 * (r + R)
        val2 = a + b
        if isinstance(val1, float) or isinstance(val2, float):
            neg_q = abs(val1 - val2) > 1e-9
        else:
            neg_q = (val1 != val2)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]