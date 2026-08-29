import sympy
from sympy.ntheory import totient
from sympy import gcd, lcm

def conditions(witness):
    try:
        m, n = witness
        if float(m) != int(m) or float(n) != int(n):
            h1 = False
        else:
            m = int(m)
            n = int(n)
            h1 = (m >= 1 and n >= 1)
    except Exception:
        h1 = False

    try:
        m, n = witness
        if float(m) != int(m) or float(n) != int(n):
            neg_q = False
        else:
            m = int(m)
            n = int(n)
            if m < 1 or n < 1:
                neg_q = False
            else:
                # The degree of Q(zeta_k) over Q is totient(k).
                # The composite of Q(zeta_m) and Q(zeta_n) is Q(zeta_{lcm(m,n)}).
                # Two finite extensions K, L of F are linearly disjoint over F 
                # iff [KL : F] == [K : F] * [L : F].
                deg_composite = totient(lcm(m, n))
                deg_m = totient(m)
                deg_n = totient(n)
                
                linearly_disjoint = (deg_composite == deg_m * deg_n)
                gcd_is_one = (gcd(m, n) == 1)
                
                # The conjecture states: linearly_disjoint <==> gcd_is_one
                # We want the negation of this conclusion.
                neg_q = (linearly_disjoint != gcd_is_one)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Q(zeta_m) and Q(zeta_n) are cyclotomic fields over Q",
    "¬Q: The fields are linearly disjoint iff gcd(m,n) = 1 FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1