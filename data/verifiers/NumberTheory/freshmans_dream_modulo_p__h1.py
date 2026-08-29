import sympy

def conditions(witness):
    try:
        a, b, p = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        if not isinstance(p, (int, sympy.Integer)):
            neg_q = False
        elif int(p) == 0:
            neg_q = False
        else:
            p_int = int(p)
            a_int = int(a)
            b_int = int(b)
            lhs = pow(a_int + b_int, p_int, p_int)
            rhs = (pow(a_int, p_int, p_int) + pow(b_int, p_int, p_int)) % p_int
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are integers",
    "¬Q: (a + b)^p is not congruent to a^p + b^p mod p"
]

N_HYP = 1
NEG_Q_INDEX = 1