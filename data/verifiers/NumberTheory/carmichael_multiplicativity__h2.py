import sympy
from sympy.ntheory import reduced_totient
from sympy import lcm

def conditions(witness):
    try:
        m, n = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = (int(m) == m) and (int(n) == n) and (m > 0) and (n > 0)
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            lhs = reduced_totient(m * n)
            rhs = lcm(reduced_totient(m), reduced_totient(n))
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "¬Q: lambda(mn) != lcm(lambda(m), lambda(n))"
]

N_HYP = 1
NEG_Q_INDEX = 1