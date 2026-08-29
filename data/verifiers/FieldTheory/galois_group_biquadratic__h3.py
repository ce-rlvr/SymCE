import sympy
from sympy import Rational, integer_nthroot, isprime

# Top-level setup
# The witness is expected to be a tuple: (char, a, b) or (a, b)
# where char is the characteristic of the field F (0 for QQ, p for GF(p)),
# and a, b are elements of F.

def is_square(x, char):
    if char == 0:
        x = Rational(x)
        if x < 0:
            return False
        num_is_sq = integer_nthroot(x.p, 2)[1]
        den_is_sq = integer_nthroot(x.q, 2)[1]
        return num_is_sq and den_is_sq
    else:
        x = int(x) % char
        if x == 0:
            return True
        return pow(x, (char - 1) // 2, char) == 1

def conditions(witness):
    try:
        if len(witness) == 3:
            char, a, b = witness
        elif len(witness) == 2:
            char = 0
            a, b = witness
        else:
            return [False] * 5 + [False]
    except Exception:
        return [False] * 5 + [False]

    # H_1: F is a field with characteristic not equal to 2
    try:
        if char == 0:
            h1 = True
        else:
            h1 = isprime(char) and char != 2
    except Exception:
        h1 = False

    # H_2: a and b are elements of F
    try:
        if char == 0:
            Rational(a)
            Rational(b)
            h2 = True
        else:
            int(a)
            int(b)
            h2 = True
    except Exception:
        h2 = False

    # H_3: There is no element y in F such that y^2 = b
    try:
        h3 = not is_square(b, char)
    except Exception:
        h3 = False

    # H_4: There is no element z in F such that z^2 = ab
    try:
        if char == 0:
            ab = Rational(a) * Rational(b)
        else:
            ab = (int(a) * int(b)) % char
        h4 = not is_square(ab, char)
    except Exception:
        h4 = False

    # H_5: K is the splitting field of the polynomial (x^2 - a)(x^2 - b) over F
    # This is a definitional hypothesis for K, which holds by construction.
    h5 = True

    # ¬Q: The field extension K/F is not Galois with degree 4 and Galois group V4
    # The degree [K:F] is 4 (and Gal(K/F) is V4) if and only if a, b, and ab are all non-squares in F.
    # Therefore, the conclusion fails (neg_q is True) if at least one of a, b, or ab is a square in F.
    try:
        if char == 0:
            ab = Rational(a) * Rational(b)
        else:
            ab = (int(a) * int(b)) % char
        
        a_sq = is_square(a, char)
        b_sq = is_square(b, char)
        ab_sq = is_square(ab, char)
        
        neg_q = a_sq or b_sq or ab_sq
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field with characteristic not equal to 2",
    "H_2: a and b are elements of F",
    "H_3: There is no element y in F such that y^2 = b",
    "H_4: There is no element z in F such that z^2 = ab",
    "H_5: K is the splitting field of the polynomial (x^2 - a)(x^2 - b) over F",
    "¬Q: The field extension K/F is not Galois with degree 4 and Galois group V4"
]

N_HYP = 5
NEG_Q_INDEX = 5