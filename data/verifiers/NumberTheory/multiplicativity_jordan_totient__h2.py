import sympy
from sympy.ntheory import factorint

def conditions(witness) -> list[bool]:
    try:
        k, a, b = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(k, (int, sympy.Integer)) and k > 0
    except Exception:
        h1 = False

    try:
        if not (isinstance(a, (int, sympy.Integer)) and a > 0 and 
                isinstance(b, (int, sympy.Integer)) and b > 0):
            neg_q = False
        elif not h1:
            neg_q = False
        else:
            k_int = int(k)
            a_int = int(a)
            b_int = int(b)
            
            def J(k_val, n_val):
                if n_val == 1:
                    return 1
                factors = factorint(n_val)
                res = n_val**k_val
                for p in factors:
                    res = res * (p**k_val - 1) // (p**k_val)
                return res
            
            lhs = J(k_int, a_int * b_int)
            rhs = J(k_int, a_int) * J(k_int, b_int)
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "¬Q: J_k(ab) != J_k(a)J_k(b)"
]

N_HYP = 1
NEG_Q_INDEX = 1