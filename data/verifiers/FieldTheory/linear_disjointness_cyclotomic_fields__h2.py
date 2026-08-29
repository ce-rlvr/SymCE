import math
from sympy.ntheory import totient

# Top-level setup
# No special named objects are required for this number theory / field theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False]
        m, n = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(m, int) and isinstance(n, int) and m > 0 and n > 0
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            lcm_mn = (m * n) // math.gcd(m, n)
            
            # P: Q(zeta_m) and Q(zeta_n) are linearly disjoint over Q.
            # For cyclotomic fields, this holds if and only if the degree of their 
            # compositum Q(zeta_{lcm(m,n)}) equals the product of their degrees.
            P = (totient(lcm_mn) == totient(m) * totient(n))
            
            # R: gcd(m, n) == 1
            R = (math.gcd(m, n) == 1)
            
            # The conclusion is P <-> R. The negation is P XOR R.
            neg_q = bool(P != R)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "¬Q: Q(zeta_m) and Q(zeta_n) are linearly disjoint over Q XOR gcd(m,n) == 1"
]

N_HYP = 1
NEG_Q_INDEX = 1