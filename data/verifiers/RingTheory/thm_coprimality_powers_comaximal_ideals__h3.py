import sympy
import math

# Top-level setup
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 5:
            R, I, J, m, n = witness
        elif len(witness) == 4:
            I, J, m, n = witness
            R = ZZ
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring
    try:
        h1 = (R == ZZ or str(R) == 'ZZ' or R == sympy.S.Integers)
    except Exception:
        h1 = False

    # H_2: I and J are ideals of R
    try:
        def is_int(x):
            return isinstance(x, int) or isinstance(x, sympy.Integer)
        h2 = h1 and is_int(I) and is_int(J)
    except Exception:
        h2 = False

    # H_3: m and n are positive integers
    try:
        def is_int(x):
            return isinstance(x, int) or isinstance(x, sympy.Integer)
        h3 = is_int(m) and is_int(n) and int(m) > 0 and int(n) > 0
    except Exception:
        h3 = False

    # neg_Q: I^m + J^n != R
    try:
        if h2 and h3:
            I_val = int(I)
            J_val = int(J)
            # In ZZ, ideals are comaximal iff their generators are coprime.
            # I^m + J^n != R iff gcd(I^m, J^n) != 1.
            # For m, n > 0, gcd(I^m, J^n) != 1 iff gcd(I, J) != 1.
            neg_q = math.gcd(I_val, J_val) != 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of R",
    "H_3: m and n are positive integers",
    "¬Q: I^m and J^n are not comaximal (I^m + J^n != R)"
]

N_HYP = 3
NEG_Q_INDEX = 3