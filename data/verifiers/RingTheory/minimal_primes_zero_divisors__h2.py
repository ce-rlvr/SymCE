import sympy
import math

Z = sympy.S.Integers
Q = sympy.S.Rationals

def conditions(witness) -> list[bool]:
    try:
        R, P = witness
    except Exception:
        return [False, False]

    h1_ok = False
    try:
        if isinstance(R, int) and R > 1:
            h1_ok = True
        elif R in (sympy.S.Integers, sympy.S.Rationals):
            h1_ok = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1_ok = True
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        for x in P:
            is_zd = False
            if isinstance(R, int) and R > 1:
                val = x % R
                if val == 0 or math.gcd(val, R) > 1:
                    is_zd = True
            elif R in (sympy.S.Integers, sympy.S.Rationals):
                if x == 0:
                    is_zd = True
            elif hasattr(R, 'is_zero_divisor'):
                if R.is_zero_divisor(x):
                    is_zd = True
            
            if not is_zd:
                neg_q_ok = True
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: Not every element of P is a zero divisor in R"
]

N_HYP = 1
NEG_Q_INDEX = 1